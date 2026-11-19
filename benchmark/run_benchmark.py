"""Accuracy benchmark for af-confidence on real UniProt variants.

UniProt natural variants are positioned on the canonical sequence, so they are the ground
truth. Each scenario rewrites them the way the literature often does (legacy / mature-protein
numbering, an unannotated shift, a typo) and checks whether the tool finds the true position
without presenting coincidences as strong evidence.

    python3 benchmark/run_benchmark.py --cache /tmp/afc-bench     # downloads ~200 proteins
    python3 benchmark/run_benchmark.py --cache /tmp/afc-bench --offline

Writes benchmark/dataset.tsv (the sampled proteins and variants) and benchmark/results.md.
Not part of the installed package; needs network access to rest.uniprot.org and
alphafold.ebi.ac.uk on the first run.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from af_confidence.mapper import annotated_offsets, map_variants  # noqa: E402
from af_confidence.sources import Client, SourceError  # noqa: E402

SEED = 20261119
N_SIGNAL, N_INITMET = 150, 50
MAX_VARIANTS = 10              # per protein, like a variant table in a paper
SEARCH = "https://rest.uniprot.org/uniprotkb/search?"
FIELDS = "accession,ft_init_met,ft_signal,ft_chain,ft_peptide,ft_propep,ft_transit,ft_variant,sequence"
QUERIES = {
    "signal": "reviewed:true AND organism_id:9606 AND ft_signal:* AND ft_variant:*",
    "init_met": "reviewed:true AND organism_id:9606 AND ft_init_met:* AND ft_variant:* NOT ft_signal:*",
}


# ---------------------------------------------------------------- dataset
def _search_all(client: Client, query: str, fields: str, cache_name: str) -> list[dict]:
    path = client.cache_dir / cache_name
    if path.exists():
        return json.loads(path.read_text())
    if client.offline:
        raise SourceError(f"offline: {path} missing")
    url = SEARCH + urllib.parse.urlencode({"query": query, "fields": fields, "format": "json",
                                           "size": "500", "sort": "accession asc"})
    out = []
    while url:
        req = urllib.request.Request(url, headers={"User-Agent": "af-confidence-benchmark"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            out += json.loads(resp.read())["results"]
            m = re.search(r'<([^>]+)>;\s*rel="next"', resp.headers.get("Link", ""))
            url = m.group(1) if m else None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out))
    return out


skipped_uncertain: list[str] = []


def build_dataset(client: Client) -> list[dict]:
    rng = random.Random(SEED)
    proteins = []
    for kind, n in (("signal", N_SIGNAL), ("init_met", N_INITMET)):
        ids = [r["primaryAccession"] for r in
               _search_all(client, QUERIES[kind], "accession", f"bench_ids_{kind}.json")]
        chosen = sorted(rng.sample(ids, n))
        entries = []
        for i in range(0, len(chosen), 50):
            q = "accession:(" + " OR ".join(chosen[i:i + 50]) + ")"
            entries += _search_all(client, q, FIELDS, f"bench_entries_{kind}_{i}.json")
        for e in entries:
            acc = e["primaryAccession"]
            feats = e.get("features", [])
            # pre-populate the tool's UniProt cache with the same data
            uni = client.cache_dir / f"uniprot_{acc}.json"
            if not uni.exists():
                uni.write_text(json.dumps({"features": [f for f in feats if f["type"] != "Natural variant"],
                                           "sequence": e["sequence"]}))
            if kind == "signal":
                shift = next(f["location"]["end"].get("value") for f in feats if f["type"] == "Signal")
            else:
                shift = 1
            if not isinstance(shift, int):        # uncertain boundary ("?"): no clear numbering
                skipped_uncertain.append(acc)
                continue
            variants = []
            for f in feats:
                if f["type"] != "Natural variant":
                    continue
                loc, alt = f["location"], f.get("alternativeSequence", {})
                ref, alts = alt.get("originalSequence", ""), alt.get("alternativeSequences", [])
                pos = loc["start"].get("value")
                if (isinstance(pos, int) and loc["end"].get("value") == pos and len(ref) == 1 and len(alts) == 1 and len(alts[0]) == 1
                        and pos > shift + 1):
                    variants.append(f"{ref}{pos}{alts[0]}")
            variants = sorted(set(variants), key=lambda v: int(v[1:-1]))
            if len(variants) > MAX_VARIANTS:
                variants = sorted(rng.sample(variants, MAX_VARIANTS), key=lambda v: int(v[1:-1]))
            if variants:
                proteins.append({"accession": acc, "kind": kind, "shift": shift, "variants": variants})
    return proteins


# ---------------------------------------------------------------- scoring
def shifted(v: str, k: int) -> str:
    return f"{v[0]}{int(v[1:-1]) + k}{v[-1]}"


class Tally:
    def __init__(self):
        self.c = Counter()

    def score(self, result, true_pos: int, expect_strong: bool = True) -> None:
        self.c["n"] += 1
        strong = [s for s in result.suggestions if s.strength == "strong"]
        if result.status == "match":
            self.c["silent_match"] += 1             # coincidence, nothing flagged
        if result.status == "ambiguous_match":
            self.c["flagged_ambiguous"] += 1
        if any(s.position == true_pos for s in strong):
            self.c["recovered_strong"] += 1
        if any(s.position == true_pos for s in result.suggestions):
            self.c["recovered_any"] += 1
        if result.suggestions and result.suggestions[0].position == true_pos:
            self.c["top_correct"] += 1
        if any(s.position != true_pos for s in strong):
            self.c["wrong_strong"] += 1
        if strong and all(s.position == true_pos for s in strong):
            self.c["only_correct_strong"] += 1
        if not expect_strong and strong:
            self.c["unexpected_strong"] += 1


def run(client: Client, proteins: list[dict]):
    rng = random.Random(SEED + 1)
    t = defaultdict(Tally)
    skipped = Counter()
    for i, p in enumerate(proteins, 1):
        acc, k0, vs = p["accession"], p["shift"], p["variants"]
        try:
            protein = client.protein(acc)
        except SourceError as exc:
            skipped["no AlphaFold DB model or load error"] += 1
            p["skip"] = str(exc)
            continue
        if not protein.canonical.uniprot_sequence_matches:
            skipped["AlphaFold DB model built on an older UniProt sequence"] += 1
            p["skip"] = "older sequence"
            continue
        print(f"[{i}/{len(proteins)}] {acc} ({len(vs)} variants)", file=sys.stderr)
        tag = p["kind"]

        # A. correct numbering, whole list
        for r in map_variants(acc, vs, client):
            t[f"A_{tag}"].c["n"] += 1
            t[f"A_{tag}"].c["status_" + r.status] += 1

        # B. legacy numbering, one variant at a time
        for v in vs:
            (r,) = map_variants(acc, [shifted(v, -k0)], client)
            t[f"B_{tag}"].score(r, int(v[1:-1]))

        # C. legacy numbering, whole list (needs >= 2 variants)
        if len(vs) >= 2:
            for v, r in zip(vs, map_variants(acc, [shifted(v, -k0) for v in vs], client)):
                t[f"C_{tag}"].score(r, int(v[1:-1]))

        # D. an unannotated shift
        ann = set(annotated_offsets(protein))
        cand = [k for k in range(5, 61) if k not in ann and all(int(v[1:-1]) > k + 1 for v in vs)]
        if cand:
            k = rng.choice(cand)
            if len(vs) >= 3:
                for v, r in zip(vs, map_variants(acc, [shifted(v, -k) for v in vs], client)):
                    t["D_batch"].score(r, int(v[1:-1]))
            v = vs[0]
            (r,) = map_variants(acc, [shifted(v, -k)], client)
            t["D_single"].score(r, int(v[1:-1]), expect_strong=False)

        # E. negative control: a typo of 1-3 positions
        v = rng.choice(vs)
        d = rng.choice([-3, -2, -1, 1, 2, 3])
        if int(v[1:-1]) + d > 0:
            (r,) = map_variants(acc, [shifted(v, d)], client)
            t["E_typo"].score(r, int(v[1:-1]), expect_strong=False)
    return t, skipped


# ---------------------------------------------------------------- report
def pct(a: int, b: int) -> str:
    return f"{a}/{b} ({100 * a / b:.1f}%)" if b else "–"


def write_report(t, skipped, proteins, path: Path, elapsed: float) -> None:
    used = [p for p in proteins if "skip" not in p]
    nv = sum(len(p["variants"]) for p in used)
    L = []
    L.append("# Benchmark results\n")
    L.append(f"Generated by `benchmark/run_benchmark.py` (seed {SEED}) in {elapsed:.0f} s.\n")
    L.append(f"Proteins sampled: {len(proteins)}; used: {len(used)} "
             f"({sum(p['kind'] == 'signal' for p in used)} with a signal peptide, "
             f"{sum(p['kind'] == 'init_met' for p in used)} with only the initiator Met removed); "
             f"variants used: {nv}.\n")
    if skipped_uncertain:
        L.append(f"- skipped {len(skipped_uncertain)}: signal-peptide end not known exactly in UniProt")
    for reason, n in skipped.items():
        L.append(f"- skipped {n}: {reason}")
    L.append("")
    L.append("## A. Correct (UniProt) numbering — should all match\n")
    L.append("| set | variants | match | ambiguous_match | mismatch / other |")
    L.append("|---|---|---|---|---|")
    for key in ("A_signal", "A_init_met"):
        c = t[key].c
        other = c["n"] - c["status_match"] - c["status_ambiguous_match"]
        L.append(f"| {key[2:]} | {c['n']} | {pct(c['status_match'], c['n'])} | "
                 f"{pct(c['status_ambiguous_match'], c['n'])} | {pct(other, c['n'])} |")
    L.append("")
    L.append("## B–D. Wrong numbering — should recover the true position\n")
    L.append("| scenario | inputs | true position as strong suggestion | true position is top suggestion "
             "| only the true position is strong | a wrong position is strong | silent match "
             "(coincidence, not flagged) | flagged as ambiguous_match |")
    L.append("|---|---|---|---|---|---|---|---|")
    names = {
        "B_signal": "B. signal-peptide numbering, one variant",
        "B_init_met": "B. no-initiator-Met numbering, one variant",
        "C_signal": "C. signal-peptide numbering, whole list",
        "C_init_met": "C. no-initiator-Met numbering, whole list",
        "D_batch": "D. unannotated shift (5–60), whole list (≥3)",
    }
    for key, name in names.items():
        c = t[key].c
        n = c["n"]
        L.append(f"| {name} | {n} | {pct(c['recovered_strong'], n)} | {pct(c['top_correct'], n)} | "
                 f"{pct(c['only_correct_strong'], n)} | {pct(c['wrong_strong'], n)} | "
                 f"{pct(c['silent_match'], n)} | {pct(c['flagged_ambiguous'], n)} |")
    L.append("")
    L.append("## D/E. Cases where no strong evidence should be given\n")
    L.append("| scenario | inputs | any strong suggestion (should be ~0) | true position among weak suggestions "
             "| silent match |")
    L.append("|---|---|---|---|---|")
    for key, name in (("D_single", "D. unannotated shift, one variant"),
                      ("E_typo", "E. typo of ±1–3 positions, one variant")):
        c = t[key].c
        n = c["n"]
        L.append(f"| {name} | {n} | {pct(c['unexpected_strong'], n)} | {pct(c['recovered_any'], n)} | "
                 f"{pct(c['silent_match'], n)} |")
    L.append("")
    path.write_text("\n".join(L) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache", required=True, help="cache directory for downloads")
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()
    client = Client(args.cache, offline=args.offline)
    start = time.time()
    proteins = build_dataset(client)
    t, skipped = run(client, proteins)
    out = Path(__file__).resolve().parent
    with open(out / "dataset.tsv", "w") as fh:
        fh.write("accession\tset\tshift\tvariants\tskipped\n")
        for p in proteins:
            fh.write(f"{p['accession']}\t{p['kind']}\t{p['shift']}\t{','.join(p['variants'])}\t"
                     f"{p.get('skip', '')}\n")
    write_report(t, skipped, proteins, out / "results.md", time.time() - start)
    print((out / "results.md").read_text())
    return 0


if __name__ == "__main__":
    sys.exit(main())
