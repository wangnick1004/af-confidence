"""Check protein variants against an AlphaFold DB model sequence and explain mismatches.

Every check here is an exact sequence comparison. No structural judgement is made: the
pLDDT value of the matched residue is reported as AlphaFold DB provides it.

Mismatch explanations, from strongest to weakest evidence:

1. ``annotated_offset``  - shifting by the length of a UniProt-annotated processing feature
   (removed initiator Met, signal peptide, propeptide, transit peptide) gives a match.
   Typical cause: legacy or mature-protein numbering.
2. ``consistent_offset`` - one shift makes *all* mismatched variants in the batch match,
   and that is unlikely to happen by chance (see ``expected_by_chance``).
3. ``isoform``           - the residue matches at the same number in an isoform model.
4. ``swapped``           - the model has the *alternate* residue: ref/alt may be swapped.
5. ``nearby``            - the residue appears within +/-3 positions. Weak: with ~20 amino
   acids this happens by chance about a quarter of the time.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .sources import Client, Model, ProteinData
from .variants import Variant, VariantParseError, parse_variant

NEARBY_WINDOW = 3
OFFSET_SEARCH = 100          # consistent-offset search range: -100..+100
CHANCE_THRESHOLD = 0.05      # report a consistent offset only if expected random hits < this

PROCESSING_TYPES = {
    "Initiator methionine": "initiator Met removed",
    "Signal": "signal peptide",
    "Propeptide": "propeptide",
    "Transit peptide": "transit peptide",
}


@dataclass
class Suggestion:
    kind: str
    position: int
    entry_id: str
    note: str
    plddt: float | None = None


@dataclass
class Result:
    input: str
    variant: Variant | None
    status: str                       # match | mismatch | out_of_range | invalid
    entry_id: str = ""
    model_residue: str = ""
    plddt: float | None = None
    message: str = ""
    suggestions: list[Suggestion] = field(default_factory=list)


def _residue(model: Model, pos: int) -> str | None:
    i = pos - model.start
    if 0 <= i < len(model.sequence):
        return model.sequence[i]
    return None


def annotated_offsets(protein: ProteinData) -> dict[int, str]:
    """Offsets implied by UniProt processing features: {offset: reason}."""
    offsets: dict[int, str] = {}
    for ftype, start, end, desc in protein.processing:
        if ftype == "Initiator methionine" and start == 1:
            offsets.setdefault(1, PROCESSING_TYPES[ftype])
        elif ftype in PROCESSING_TYPES and start == 1:
            offsets.setdefault(end, f"{PROCESSING_TYPES[ftype]} 1-{end}")
        elif ftype == "Chain" and start > 1:
            offsets.setdefault(start - 1, f"mature chain starts at {start}")
    return offsets


def expected_by_chance(sequence: str, refs: list[str], n_offsets: int) -> float:
    """Expected number of offsets at which all ``refs`` would match purely by chance,
    using the amino-acid composition of ``sequence``."""
    comp = Counter(sequence)
    p = 1.0
    for r in refs:
        p *= comp.get(r, 0) / len(sequence)
    return p * n_offsets


def consistent_offset(model: Model, variants: list[Variant]) -> tuple[int, float] | None:
    """Find a single non-zero offset that makes every variant match.

    Returns (offset, expected_by_chance) for the unique such offset, or None when there is
    no such offset, more than one, fewer than two variants, or the result could be chance.
    """
    if len(variants) < 2:
        return None
    hits = [k for k in range(-OFFSET_SEARCH, OFFSET_SEARCH + 1)
            if k != 0 and all(_residue(model, v.position + k) == v.ref for v in variants)]
    if len(hits) != 1:
        return None
    chance = expected_by_chance(model.sequence, [v.ref for v in variants], 2 * OFFSET_SEARCH)
    if chance >= CHANCE_THRESHOLD:
        return None
    return hits[0], chance


def map_variants(accession: str, variant_texts: list[str], client: Client | None = None) -> list[Result]:
    client = client or Client()
    protein = client.protein(accession)
    canon = protein.canonical
    plddt = client.load_plddt(canon)

    results: list[Result] = []
    parsed: list[tuple[Result, Variant]] = []
    for text in variant_texts:
        try:
            v = parse_variant(text)
        except VariantParseError as exc:
            results.append(Result(text, None, "invalid", message=str(exc)))
            continue
        aa = _residue(canon, v.position)
        if aa is None:
            r = Result(text, v, "out_of_range", canon.entry_id,
                       message=f"position {v.position} is outside the model "
                               f"({canon.start}-{canon.start + len(canon.sequence) - 1})")
        elif aa == v.ref:
            r = Result(text, v, "match", canon.entry_id, aa,
                       plddt.get(v.position) if plddt else None)
        else:
            r = Result(text, v, "mismatch", canon.entry_id, aa,
                       message=f"model has {aa} at {v.position}, not {v.ref}")
        results.append(r)
        parsed.append((r, v))

    problems = [(r, v) for r, v in parsed if r.status in ("mismatch", "out_of_range")]
    if not problems:
        return results

    ann = annotated_offsets(protein)
    batch = consistent_offset(canon, [v for _, v in problems])

    def pl(model: Model, pos: int) -> float | None:
        d = client.load_plddt(model) if model is canon else None
        return d.get(pos) if d else None

    for r, v in problems:
        explained = False
        for k, reason in sorted(ann.items()):
            if _residue(canon, v.position + k) == v.ref:
                p = v.position + k
                r.suggestions.append(Suggestion(
                    "annotated_offset", p, canon.entry_id,
                    f"+{k}: {v.ref}{p}{v.alt} matches; UniProt annotates {reason}, "
                    f"so {v} is probably numbered without it", pl(canon, p)))
                explained = True
        if batch and not any(s.kind == "annotated_offset" and s.position == v.position + batch[0]
                             for s in r.suggestions):
            k, chance = batch
            p = v.position + k
            r.suggestions.append(Suggestion(
                "consistent_offset", p, canon.entry_id,
                f"{k:+d}: shifting all {len(problems)} mismatched variants by {k:+d} makes them all "
                f"match (expected by chance: {chance:.3f})", pl(canon, p)))
            explained = True
        for iso in protein.models[1:]:
            if _residue(iso, v.position) == v.ref:
                r.suggestions.append(Suggestion(
                    "isoform", v.position, iso.entry_id,
                    f"{v.ref}{v.position} matches isoform {iso.accession} ({iso.entry_id}); "
                    f"check which isoform the source used"))
        if r.status == "mismatch" and v.alt != "*" and r.model_residue == v.alt:
            r.suggestions.append(Suggestion(
                "swapped", v.position, canon.entry_id,
                f"model already has {v.alt} at {v.position}: did the source write "
                f"{v.alt}{v.position}{v.ref}? (ref/alt may be swapped)", pl(canon, v.position)))
        if not explained:
            for d in range(1, NEARBY_WINDOW + 1):
                for p in (v.position - d, v.position + d):
                    if _residue(canon, p) == v.ref:
                        r.suggestions.append(Suggestion(
                            "nearby", p, canon.entry_id,
                            f"{v.ref} found at {p} ({p - v.position:+d}); weak evidence, "
                            f"could be chance", pl(canon, p)))
    return results
