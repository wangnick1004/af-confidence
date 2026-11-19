"""Command-line interface: ``af-confidence P68871 E6V``."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from . import __version__
from .mapper import Result, map_variants
from .sources import Client, SourceError

SYMBOL = {"match": "OK ", "mismatch": "XX ", "out_of_range": "XX ", "invalid": "?? "}


def _fmt_plddt(x: float | None) -> str:
    return f"{x:.2f}" if x is not None else "n/a"


def render_text(accession: str, results: list[Result]) -> str:
    lines = []
    entry = next((r.entry_id for r in results if r.entry_id), "")
    lines.append(f"{accession}  (AlphaFold DB model {entry})" if entry else accession)
    for r in results:
        if r.status == "match":
            lines.append(f"{SYMBOL[r.status]}{r.input}: matches the model sequence "
                         f"(pLDDT {_fmt_plddt(r.plddt)})")
        else:
            lines.append(f"{SYMBOL[r.status]}{r.input}: {r.message}")
        for s in r.suggestions:
            tail = f" [pLDDT {_fmt_plddt(s.plddt)}]" if s.plddt is not None else ""
            lines.append(f"     -> [{s.kind}] {s.note}{tail}")
    lines.append("")
    lines.append("pLDDT values are shown as provided by AlphaFold DB, not reinterpreted. "
                 "This tool does not predict variant effects.")
    return "\n".join(lines)


def render_tsv(results: list[Result]) -> str:
    rows = ["input\tstatus\tentry_id\tmodel_residue\tplddt\tsuggestion_kind\tsuggested_position\tnote"]
    for r in results:
        base = [r.input, r.status, r.entry_id, r.model_residue, _fmt_plddt(r.plddt)]
        if not r.suggestions:
            rows.append("\t".join(base + ["", "", r.message]))
        for s in r.suggestions:
            rows.append("\t".join(base + [s.kind, str(s.position), s.note]))
    return "\n".join(rows)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="af-confidence",
        description="Check protein variants (e.g. E6V, p.Glu6Val) against the AlphaFold DB model "
                    "sequence and explain numbering mismatches.")
    ap.add_argument("accession", help="UniProt accession, e.g. P68871")
    ap.add_argument("variants", nargs="+", help="variants, e.g. E6V p.Glu342Lys (commas allowed)")
    ap.add_argument("--format", choices=["text", "tsv", "json"], default="text")
    ap.add_argument("--cache", help="cache directory (default: ~/.cache/af-confidence)")
    ap.add_argument("--offline", action="store_true", help="use cached files only, no network")
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = ap.parse_args(argv)

    variants = [v for arg in args.variants for v in arg.replace(",", " ").split() if v]
    try:
        results = map_variants(args.accession, variants, Client(args.cache, offline=args.offline))
    except SourceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps([asdict(r) for r in results], indent=2, ensure_ascii=False))
    elif args.format == "tsv":
        print(render_tsv(results))
    else:
        print(render_text(args.accession, results))
    return 0 if all(r.status == "match" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
