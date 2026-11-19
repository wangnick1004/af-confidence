"""Reading variant lists: ``[PROTEIN] VARIANT ...`` lines, and merging entries per protein."""
from __future__ import annotations

from .sources import Client, SourceError
from .variants import VariantParseError, parse_variant


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
