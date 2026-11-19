"""Check protein variants against an AlphaFold DB model sequence and explain mismatches.

Every check here is an exact sequence comparison. No structural judgement is made: the
pLDDT value of the matched residue is reported as AlphaFold DB provides it.

With ~20 amino acids, any single residue matches at a random position about 1 time in 20,
so an explanation is only called *strong* when it is unlikely to be a coincidence:

``annotated_offset``   shift by a UniProt-annotated processing feature (initiator Met,
                       signal/transit peptide, propeptide, mature chain, other fragments such
                       as amyloid-beta), or by a UniProt sequence update the AlphaFold DB model
                       has not caught up with.
                       strong: the shift explains >= 2 of the mismatched variants and that
                               many coincidental matches has probability < 0.05 divided by
                               the number of annotated shifts tried.
                       medium: a primary feature (not a minor fragment) explains this variant
                               only, and no other shift explains >= 2 variants.
                       weak:   otherwise.
``consistent_offset``  one unannotated shift makes *all* mismatched variants match and the
                       expected number of such shifts by chance is < 0.05 (needs >= 2 variants).
                       strong.
``isoform``            the residue matches at the same number in an isoform model.
                       strong when one isoform explains every mismatched variant (>= 2);
                       weak otherwise.
``swapped``            the model already has the alternate residue. medium.
``nearby``             the residue is within +/-3 positions. weak; only shown when nothing
                       stronger explains the mismatch.

A variant that matches as written is marked ``ambiguous_match`` when it *also* matches under
a shift that strongly explains the other inputs of the same batch: the source probably uses
that numbering, and the match at the written position is a coincidence.
"""
from __future__ import annotations

from collections import Counter
from math import comb
from dataclasses import dataclass, field

from .sources import Client, Model, ProteinData, SourceError
from .variants import Variant, VariantParseError, parse_variant

NEARBY_WINDOW = 3
CHANCE_THRESHOLD = 0.05      # report an unannotated offset only if expected random hits < this

STRENGTH_ORDER = {"strong": 0, "medium": 1, "weak": 2}
_PRIMARY = {
    "Initiator methionine": "initiator Met removed",
    "Signal": "signal peptide",
    "Propeptide": "propeptide",
    "Transit peptide": "transit peptide",
}


@dataclass
class Suggestion:
    kind: str
    strength: str              # strong | medium | weak
    position: int
    entry_id: str
    note: str
    plddt: float | None = None


@dataclass
class Result:
    input: str
    variant: Variant | None
    status: str        # match | ambiguous_match | mismatch | out_of_range | invalid
    entry_id: str = ""
    model_residue: str = ""
    plddt: float | None = None
    message: str = ""
    suggestions: list[Suggestion] = field(default_factory=list)


@dataclass(frozen=True)
class Offset:
    shift: int
    reason: str
    primary: bool              # initiator Met / signal / pro / transit / main mature chain


def _residue(model: Model, pos: int) -> str | None:
    i = pos - model.start
    if 0 <= i < len(model.sequence):
        return model.sequence[i]
    return None


def annotated_offsets(protein: ProteinData) -> dict[int, Offset]:
    """Offsets implied by UniProt processing features, keyed by shift.

    A feature starting at residue s implies that numbering which starts at that feature is
    shifted by s-1. Features implying the same shift are merged into one reason.
    """
    chains = [(s, e, d) for t, s, e, d in protein.processing if t == "Chain"]
    main_chain = max(chains, key=lambda c: (c[1] - c[0], -c[0])) if chains else None
    primary: dict[int, list[str]] = {}
    fragments: dict[int, list[str]] = {}
    for ftype, start, end, desc in protein.processing:
        if ftype == "Initiator methionine" and start == 1:
            primary.setdefault(1, []).append(_PRIMARY[ftype])
        elif ftype in _PRIMARY and start == 1:
            primary.setdefault(end, []).append(f"{_PRIMARY[ftype]} 1-{end}")
        elif ftype in ("Chain", "Peptide") and start > 1:
            name = f"'{desc}'" if desc else ftype.lower()
            if ftype == "Chain" and (start, end, desc) == main_chain:
                primary.setdefault(start - 1, []).append(f"mature chain {name} starts at {start}")
            else:
                fragments.setdefault(start - 1, []).append(name)
    found = {k: Offset(k, "UniProt: " + "; ".join(v), True) for k, v in primary.items()}
    for k, names in fragments.items():
        if k not in found:
            found[k] = Offset(k, f"UniProt: {', '.join(names)} start{'s' if len(names) == 1 else ''} "
                                 f"at {k + 1}", False)
    k = protein.uniprot_shift
    if k:
        found[k] = Offset(k, f"the AlphaFold DB model uses an older sequence; current UniProt "
                             f"residue n is model residue n{k:+d}", True)
    return found


def expected_by_chance(sequence: str, refs: list[str], n_offsets: int) -> float:
    """Expected number of offsets at which all ``refs`` would match purely by chance,
    using the amino-acid composition of ``sequence``."""
    comp = Counter(sequence)
    p = 1.0
    for r in refs:
        p *= comp.get(r, 0) / len(sequence)
    return p * n_offsets


def chance_of_support(sequence: str, refs: list[str], support: int) -> float:
    """Probability that a fixed shift matches at least ``support`` of the variants with
    reference residues ``refs`` by chance (binomial tail, mean residue frequency)."""
    comp = Counter(sequence)
    n = len(refs)
    p = sum(comp.get(r, 0) for r in refs) / (n * len(sequence))
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(support, n + 1))


def consistent_offset(model: Model, variants: list[Variant]) -> tuple[int, float] | None:
    """Find the single non-zero shift that makes every variant match.

    Searches every shift that keeps the variants inside the model. Returns
    (shift, expected_by_chance), or None when there are fewer than two variants, no shift or
    several shifts work, or a hit is plausible by chance.
    """
    if len(variants) < 2:
        return None
    n = len(model.sequence)
    shifts = range(-n, n + 1)
    hits = [k for k in shifts
            if k != 0 and all(_residue(model, v.position + k) == v.ref for v in variants)]
    if len(hits) != 1:
        return None
    chance = expected_by_chance(model.sequence, [v.ref for v in variants], len(shifts) - 1)
    if chance >= CHANCE_THRESHOLD:
        return None
    return hits[0], chance


@dataclass
class ProteinReport:
    query: str                         # what the user typed for the protein
    accession: str = ""
    entry_id: str = ""
    results: list[Result] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    error: str = ""                    # set when the protein itself could not be loaded
    # AlphaFold DB models of this protein: entry_id -> (first residue number, length, accession)
    models: dict[str, tuple[int, int, str]] = field(default_factory=dict)
    versions: dict[str, int] = field(default_factory=dict)    # entry_id -> AlphaFold DB version


def check_protein(query: str, variant_texts: list[str], client: Client | None = None) -> ProteinReport:
    """Like map_variants, but never raises for data problems: errors go into the report."""
    client = client or Client()
    try:
        protein = client.protein(query)
    except SourceError as exc:
        return ProteinReport(query, error=str(exc))
    return ProteinReport(query, protein.accession, protein.canonical.entry_id,
                         _map(protein, variant_texts, client), list(protein.warnings),
                         models={m.entry_id: (m.start, len(m.sequence), m.accession)
                                 for m in protein.models},
                         versions={m.entry_id: m.version for m in protein.models})


def map_variants(query: str, variant_texts: list[str], client: Client | None = None) -> list[Result]:
    """Check variants of one protein (accession or gene name). Raises SourceError."""
    client = client or Client()
    return _map(client.protein(query), variant_texts, client)


def _map(protein: ProteinData, variant_texts: list[str], client: Client) -> list[Result]:
    canon = protein.canonical

    def plddt_at(model: Model, pos: int) -> float | None:
        d = client.load_plddt(model)
        return d.get(pos) if d else None

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
            r = Result(text, v, "match", canon.entry_id, aa, plddt_at(canon, v.position))
        else:
            r = Result(text, v, "mismatch", canon.entry_id, aa,
                       message=f"model has {aa} at {v.position}, not {v.ref}")
        results.append(r)
        parsed.append((r, v))

    problems = [(r, v) for r, v in parsed if r.status in ("mismatch", "out_of_range")]
    if not problems:
        return results
    n_prob = len(problems)
    pvars = [v for _, v in problems]

    # how many mismatched variants each candidate explains
    offsets = annotated_offsets(protein)
    off_support = {k: sum(_residue(canon, v.position + k) == v.ref for v in pvars) for k in offsets}
    isoforms = protein.models[1:]
    iso_support = {m.entry_id: sum(_residue(m, v.position) == v.ref for v in pvars) for m in isoforms}
    batch = consistent_offset(canon, pvars)
    # an annotated shift is strong when that many matches would be unlikely by chance,
    # corrected for the number of annotated shifts tried (Bonferroni)
    refs = [v.ref for v in pvars]
    alpha = CHANCE_THRESHOLD / max(1, len(offsets))
    off_chance = {k: chance_of_support(canon.sequence, refs, s) if s else 1.0
                  for k, s in off_support.items()}
    supported = ({k for k, s in off_support.items() if s >= 2 and off_chance[k] < alpha}
                 | ({batch[0]} if batch else set()))

    def support_note(k: int) -> str:
        return f"explains {k}/{n_prob} mismatched input{'s' if n_prob > 1 else ''}"

    for r, v in problems:
        sugg: list[Suggestion] = []
        for k, off in sorted(offsets.items()):
            p = v.position + k
            if _residue(canon, p) != v.ref:
                continue
            # A single coincidental match happens ~1 time in 20, so one variant alone is only
            # medium evidence; agreement of >= 2 variants makes it strong.
            if k in supported:
                strength = "strong"
            elif off.primary and not (supported - {k}):
                strength = "medium"
            else:
                strength = "weak"
            sugg.append(Suggestion(
                "annotated_offset", strength, p, canon.entry_id,
                f"{k:+d}: {v.ref}{p}{v.alt} matches; {off.reason} "
                f"({support_note(off_support[k])})", plddt_at(canon, p)))
        if batch and batch[0] not in offsets:
            k, chance = batch
            p = v.position + k
            sugg.append(Suggestion(
                "consistent_offset", "strong", p, canon.entry_id,
                f"{k:+d}: the same shift makes all {n_prob} mismatched inputs match "
                f"(expected by chance: {chance:.2g}); no UniProt annotation explains it",
                plddt_at(canon, p)))
        for iso in isoforms:
            if _residue(iso, v.position) != v.ref:
                continue
            sup = iso_support[iso.entry_id]
            strong = n_prob >= 2 and sup == n_prob
            note = (f"{v.ref}{v.position} matches isoform {iso.accession} ({iso.entry_id}); "
                    f"{support_note(sup)}")
            if not strong:
                note += f"; {len(isoforms)} isoforms checked, could be chance"
            sugg.append(Suggestion("isoform", "strong" if strong else "weak", v.position,
                                   iso.entry_id, note, plddt_at(iso, v.position)))
        if r.status == "mismatch" and v.alt != "*" and r.model_residue == v.alt:
            sugg.append(Suggestion(
                "swapped", "medium", v.position, canon.entry_id,
                f"model already has {v.alt} at {v.position}: did the source mean "
                f"{v.alt}{v.position}{v.ref}? (ref/alt may be swapped)",
                plddt_at(canon, v.position)))
        if not any(s.strength in ("strong", "medium") for s in sugg):
            for d in range(1, NEARBY_WINDOW + 1):
                for p in (v.position - d, v.position + d):
                    if _residue(canon, p) == v.ref:
                        sugg.append(Suggestion(
                            "nearby", "weak", p, canon.entry_id,
                            f"{v.ref} found at {p} ({p - v.position:+d}); could be chance",
                            plddt_at(canon, p)))
        else:
            sugg = [s for s in sugg if s.strength != "weak"]
        sugg.sort(key=lambda s: STRENGTH_ORDER[s.strength])
        r.suggestions = sugg

    # matches that would also fit the shift that explains the rest of the batch
    batch_shifts: dict[int, str] = {}
    for k, off in offsets.items():
        if k in supported:
            batch_shifts[k] = off.reason
    if batch and batch[0] not in batch_shifts:
        batch_shifts[batch[0]] = "consistent shift of the other inputs"
    for r, v in parsed:
        if r.status != "match":
            continue
        for k, reason in sorted(batch_shifts.items()):
            p = v.position + k
            if _residue(canon, p) == v.ref:
                r.status = "ambiguous_match"
                r.message = (f"matches as written, but {v.ref}{p}{v.alt} ({k:+d}) also matches, "
                             f"the shift that explains {off_support.get(k, n_prob)}/{n_prob} "
                             f"mismatched inputs")
                r.suggestions.append(Suggestion(
                    "ambiguous_match", "medium", p, canon.entry_id,
                    f"{k:+d}: if the source uses the same numbering as the other inputs, the "
                    f"variant is {v.ref}{p}{v.alt} ({reason})", plddt_at(canon, p)))
    return results
