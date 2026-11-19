"""Command-line interface.

    af-confidence P68871 E6V
    af-confidence HBB E6V E7K
    af-confidence -f variants.txt          # lines like "HBB E6V" or "P01009 E342K, E264V"
    af-confidence APP -f abeta_list.txt    # lines with variants only use the given protein
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from . import __version__
from .mapper import ProteinReport, Result, check_protein
from .sources import HUMAN, Client, SourceError
from .variants import VariantParseError, parse_variant

SYMBOL = {"match": "OK ", "ambiguous_match": "!? ", "mismatch": "XX ", "out_of_range": "XX ",
          "invalid": "?? "}
FOOTER = ("Evidence: strong = several inputs agree and that is unlikely by chance; medium = one "
          "input fits (right about 9 times in 10 in the benchmark); weak = could easily be chance.\n"
          "pLDDT values are shown as provided by AlphaFold DB, not reinterpreted. "
          "This tool does not predict variant effects.")


class InputError(ValueError):
    pass


def _tokens(text: str) -> list[str]:
    return [t for t in text.replace(",", " ").replace(";", " ").split() if t]


def _is_variant(token: str) -> bool:
    try:
        parse_variant(token)
        return True
    except VariantParseError:
        return False


def parse_lines(lines, default_protein: str | None, source: str) -> list[tuple[str, list[str]]]:
    """Turn input lines into (protein, [variants]) pairs.

    A line is ``[PROTEIN] VARIANT [VARIANT ...]``; '#' starts a comment. The protein can be a
    UniProt accession or a gene name; lines without one use ``default_protein``.

    Some gene names look like variants (C1S, F2R, C4A). Without a default protein, the first
    word of a line with two or more words is always the protein; with a default protein, a
    variant-like first word is read as a variant (use the UniProt accession to avoid this).
    """
    out: list[tuple[str, list[str]]] = []
    for n, line in enumerate(lines, 1):
        toks = _tokens(line.split("#", 1)[0])
        if not toks:
            continue
        if _is_variant(toks[0]) and (default_protein is not None or len(toks) == 1):
            protein, variants = default_protein, toks
        else:
            protein, variants = toks[0], toks[1:]
        if protein is None:
            raise InputError(f"{source}, line {n}: no protein given for {' '.join(toks)!r} "
                             f"(start the line with a gene name or UniProt accession)")
        if not variants:
            raise InputError(f"{source}, line {n}: protein {protein!r} has no variants")
        out.append((protein, variants))
    return out


def group(pairs: list[tuple[str, list[str]]], client: Client) -> list[tuple[str, list[str]]]:
    """Merge entries for the same protein (accession and gene name count as the same), keeping
    first-seen order, so that batch evidence uses every variant of a protein."""
    order: list[str] = []
    variants: dict[str, list[str]] = {}
    label: dict[str, str] = {}
    for protein, vs in pairs:
        try:
            key = client.resolve(protein)
        except SourceError:
            key = protein                       # reported later by check_protein
        if key not in variants:
            order.append(key)
            variants[key] = []
            label[key] = protein
        variants[key].extend(vs)
    return [(label[k], variants[k]) for k in order]


def _fmt_plddt(x: float | None) -> str:
    return f"{x:.2f}" if x is not None else "n/a"


def _header(rep: ProteinReport) -> str:
    name = rep.query if rep.query.upper() == rep.accession else f"{rep.query} -> {rep.accession}"
    return f"{name}  (AlphaFold DB model {rep.entry_id})" if rep.entry_id else name


def render_text(reports: list[ProteinReport]) -> str:
    lines: list[str] = []
    for rep in reports:
        if lines:
            lines.append("")
        if rep.error:
            lines.append(f"{rep.query}: error: {rep.error}")
            continue
        lines.append(_header(rep))
        for w in rep.warnings:
            lines.append(f"  warning: {w}")
        for r in rep.results:
            if r.status == "match":
                lines.append(f"{SYMBOL[r.status]}{r.input}: matches the model sequence "
                             f"(pLDDT {_fmt_plddt(r.plddt)})")
            else:
                lines.append(f"{SYMBOL[r.status]}{r.input}: {r.message}")
            for s in r.suggestions:
                tail = f" [pLDDT {_fmt_plddt(s.plddt)}]" if s.plddt is not None else ""
                lines.append(f"     -> [{s.strength}] {s.kind}: {s.note}{tail}")
    lines.append("")
    lines.append(FOOTER)
    return "\n".join(lines)


def render_tsv(reports: list[ProteinReport]) -> str:
    rows = ["protein\taccession\tinput\tstatus\tentry_id\tmodel_residue\tplddt\tsuggestion_kind\t"
            "strength\tsuggested_position\tsuggestion_entry\tsuggestion_plddt\tnote"]
    for rep in reports:
        if rep.error:
            rows.append("\t".join([rep.query, "", "", "error"] + [""] * 8 + [rep.error]))
            continue
        for r in rep.results:
            base = [rep.query, rep.accession, r.input, r.status, r.entry_id, r.model_residue,
                    _fmt_plddt(r.plddt)]
            if not r.suggestions:
                rows.append("\t".join(base + ["", "", "", "", "", r.message]))
            for s in r.suggestions:
                rows.append("\t".join(base + [s.kind, s.strength, str(s.position), s.entry_id,
                                               _fmt_plddt(s.plddt), s.note]))
    return "\n".join(rows)


def exit_code(reports: list[ProteinReport]) -> int:
    if any(rep.error for rep in reports):
        return 2
    ok = all(r.status == "match" for rep in reports for r in rep.results)
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="af-confidence",
        description="Check protein variants (e.g. E6V, p.Glu6Val) against the AlphaFold DB model "
                    "sequence and explain numbering mismatches.",
        epilog="Examples:  af-confidence P68871 E6V    af-confidence HBB E6V    "
               "af-confidence -f variants.txt")
    ap.add_argument("items", nargs="*", metavar="PROTEIN VARIANT",
                    help="a gene name or UniProt accession (e.g. HBB, P68871, P04637-2), "
                         "followed by variants (e.g. E6V p.Glu342Lys; commas allowed)")
    ap.add_argument("-f", "--file", action="append", default=[],
                    help="read '[PROTEIN] VARIANT ...' lines from a text file ('#' starts a "
                         "comment); can be repeated")
    ap.add_argument("--organism", type=int, default=HUMAN, metavar="TAXID",
                    help="NCBI taxonomy ID used to look up gene names (default: 9606, human)")
    ap.add_argument("--format", choices=["text", "tsv", "json"], default="text")
    ap.add_argument("--cache", help="cache directory (default: ~/.cache/af-confidence)")
    ap.add_argument("--offline", action="store_true", help="use cached files only, no network")
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = ap.parse_args(argv)

    toks = [t for item in args.items for t in _tokens(item)]
    default_protein = toks[0] if toks else None       # the first word is always the protein
    toks = toks[1:]
    if default_protein and not toks and not args.file:
        ap.error(f"no variants given for {default_protein}")
    try:
        pairs = [(default_protein, toks)] if toks else []
        for path in args.file:
            try:
                with open(path, encoding="utf-8") as fh:
                    pairs += parse_lines(fh, default_protein, path)
            except OSError as exc:
                raise InputError(f"cannot read {path}: {exc.strerror}") from None
    except InputError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if not pairs:
        ap.error("give a protein and at least one variant, or --file")

    client = Client(args.cache, offline=args.offline, organism=args.organism)
    reports = [check_protein(p, vs, client) for p, vs in group(pairs, client)]
    if args.format == "json":
        print(json.dumps([asdict(r) for r in reports], indent=2, ensure_ascii=False))
    elif args.format == "tsv":
        print(render_tsv(reports))
    else:
        print(render_text(reports))
    return exit_code(reports)


if __name__ == "__main__":
    sys.exit(main())
