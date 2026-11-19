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
            variants = sorted(set(variants), key=lambda v: (int(v[1:-1]), v))
            if len(variants) > MAX_VARIANTS:
                variants = sorted(rng.sample(variants, MAX_VARIANTS), key=lambda v: (int(v[1:-1]), v))
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
        confident = [s for s in result.suggestions if s.strength in ("strong", "medium")]
        if any(s.position == true_pos for s in confident):
            self.c["recovered_confident"] += 1
        if any(s.position != true_pos for s in confident):
            self.c["wrong_confident"] += 1
        if not expect_strong and confident:
            self.c["unexpected_confident"] += 1
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
            skipped["AlphaFold DB 沒有模型或資料讀取失敗"] += 1
            p["skip"] = str(exc)
            continue
        if not protein.canonical.uniprot_sequence_matches:
            skipped["AlphaFold DB 模型使用舊版 UniProt 序列"] += 1
            p["skip"] = "older sequence"
            continue
        print(f"[{i}/{len(proteins)}] {acc} ({len(vs)} variants)", file=sys.stderr)
        tag = p["kind"]
        if protein.uniprot_shift or any("differs from the AlphaFold DB model" in w
                                        for w in protein.warnings):
            # UniProt positions are not model positions here, so they are no ground truth.
            res = map_variants(acc, vs, client)
            p["discrepancy"] = (protein.warnings[0], sum(r.status != "match" for r in res), len(vs),
                                protein.uniprot_shift, protein.canonical.entry_id)
            skipped["現行 UniProt 序列與 AlphaFold DB 模型不同（見下方）"] += 1
            p["skip"] = "UniProt sequence differs from AlphaFold DB model"
            continue

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
    L.append("# 準確度驗證結果\n")
    L.append(f"由 `benchmark/run_benchmark.py` 產生（亂數種子 {SEED}；AlphaFold DB 與 UniProt 資料於 "
             f"2026-11-19 下載）。\n")
    L.append(f"抽樣蛋白質 {len(proteins)} 個，實際使用 {len(used)} 個"
             f"（{sum(p['kind'] == 'signal' for p in used)} 個有訊號胜肽，"
             f"{sum(p['kind'] == 'init_met' for p in used)} 個只有起始甲硫胺酸被移除），"
             f"共 {nv} 個突變。\n")
    if skipped_uncertain:
        L.append(f"- 略過 {len(skipped_uncertain)} 個：UniProt 中訊號胜肽的結束位置不確定")
    for reason, n in skipped.items():
        L.append(f"- 略過 {n} 個：{reason}")
    L.append("")
    disc = [p for p in proteins if "discrepancy" in p]
    if disc:
        L.append("\n### 建立驗證資料時發現的真實資料不一致\n")
        for p in disc:
            w, n_bad, n, shift, entry = p["discrepancy"]
            L.append(f"- **{p['accession']}**：現行 UniProt 序列與 AlphaFold DB 模型 {entry} 不同，"
                     f"位置相差 {shift:+d}。它的 {n} 個 UniProt 突變中有 {n_bad} 個照原寫法對不上模型；"
                     f"工具以序列更新造成的位移說明了這些突變。工具的警告原文：`{w}`")
        L.append("")
    L.append("## 名詞說明\n")
    L.append("- **正確答案**：UniProt 天然變異的位置（依標準序列標註）。")
    L.append("- **第一個建議**：工具列出的第一個建議指向正確位置。")
    L.append("- **碰巧對上（未標示）**：改寫後的位置剛好是同一種胺基酸，工具判為對得上、沒有任何提醒。")
    L.append("- **標示為 ambiguous_match**：照寫法對得上，但工具發現它也符合整批的共同位移而提出警告。")
    L.append("")
    L.append("## A. 照 UniProt 正確編號輸入：應該全部對得上\n")
    L.append("| 組別 | 突變數 | 對得上 | 標示為 ambiguous_match | 對不上或其他 |")
    L.append("|---|---|---|---|---|")
    groups = {"A_signal": "有訊號胜肽", "A_init_met": "只有起始甲硫胺酸被移除"}
    for key, name in groups.items():
        c = t[key].c
        other = c["n"] - c["status_match"] - c["status_ambiguous_match"]
        L.append(f"| {name} | {c['n']} | {pct(c['status_match'], c['n'])} | "
                 f"{pct(c['status_ambiguous_match'], c['n'])} | {pct(other, c['n'])} |")
    L.append("")
    L.append("## B–D. 編號錯誤：應該找回正確位置\n")
    L.append("| 情境 | 輸入數 | 正確位置是第一個建議 | 正確位置標為 strong "
             "| 正確位置標為 strong 或 medium | 錯誤位置標為 strong "
             "| 錯誤位置標為 strong 或 medium | 碰巧對上（未標示） "
             "| 標示為 ambiguous_match |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    names = {
        "B_signal": "B. 訊號胜肽編號（從成熟蛋白質算起），一次一個突變",
        "B_init_met": "B. 不算起始甲硫胺酸的編號，一次一個突變",
        "C_signal": "C. 訊號胜肽編號，整份清單一起輸入",
        "C_init_met": "C. 不算起始甲硫胺酸的編號，整份清單一起輸入",
        "D_batch": "D. 沒有標註依據的位移（5～60 格），整份清單（至少 3 個）",
    }
    for key, name in names.items():
        c = t[key].c
        n = c["n"]
        L.append(f"| {name} | {n} | {pct(c['top_correct'], n)} | {pct(c['recovered_strong'], n)} | "
                 f"{pct(c['recovered_confident'], n)} | {pct(c['wrong_strong'], n)} | "
                 f"{pct(c['wrong_confident'], n)} | {pct(c['silent_match'], n)} | "
                 f"{pct(c['flagged_ambiguous'], n)} |")
    L.append("")
    L.append("## D/E. 原理上無法判斷的情況：不應該出現 strong\n")
    L.append("只有一個突變時，無法分辨「沒有標註依據的位移」或「打錯字」與真正的編號差異，所以工具不應該給 "
             "strong。medium 偶爾會因為巧合出現（例如打錯 −1 格，看起來和「不算起始甲硫胺酸」一模一樣），"
             "這正是 medium 只有「大約 10 次對 9 次」的原因。\n")
    L.append("| 情境 | 輸入數 | 出現 strong 建議 | 出現 strong 或 medium 建議 "
             "| 正確位置出現在任一建議中 | 碰巧對上（未標示） |")
    L.append("|---|---|---|---|---|---|")
    for key, name in (("D_single", "D. 沒有標註依據的位移，一次一個突變"),
                      ("E_typo", "E. 位置打錯 1～3 格，一次一個突變")):
        c = t[key].c
        n = c["n"]
        L.append(f"| {name} | {n} | {pct(c['unexpected_strong'], n)} | "
                 f"{pct(c['unexpected_confident'], n)} | {pct(c['recovered_any'], n)} | "
                 f"{pct(c['silent_match'], n)} |")
    L.append("")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


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
    with open(out / "dataset.tsv", "w", encoding="utf-8") as fh:
        fh.write("accession\tset\tshift\tvariants\tskipped\n")
        for p in proteins:
            fh.write(f"{p['accession']}\t{p['kind']}\t{p['shift']}\t{','.join(p['variants'])}\t"
                     f"{p.get('skip', '')}\n")
    write_report(t, skipped, proteins, out / "results.md", time.time() - start)
    print((out / "results.md").read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
