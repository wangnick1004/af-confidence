"""Day 1 check of the demo cases for the new scope (reads cached files in data/cache).

Confirms that the legacy literature numbering does NOT match the AlphaFold DB model sequence,
and that a fixed offset does. This is a manual check, not the tool itself.
"""
import json
from pathlib import Path

C = Path(__file__).resolve().parent.parent / "data" / "cache"


def load(acc):
    api = json.load(open(C / f"api_{acc}.json"))
    e = next(x for x in api if x["uniprotAccession"] == acc)
    conf = json.load(open(C / f"{e['modelEntityId']}-confidence_v{e['latestVersion']}.json"))
    return e, dict(zip(conf["residueNumber"], conf["confidenceScore"]))


# (accession, label, ref aa, literature position, offset expected to fix it)
cases = [
    ("P68871", "HBB  HbS 'E6V' (legacy, no initiator Met)", "E", 6, 1),
    ("P01009", "SERPINA1 Z 'E342K' (mature-protein numbering)", "E", 342, 24),
    ("P04637", "TP53 'R175H' (already canonical)", "R", 175, 0),
]
for acc, label, ref, pos, off in cases:
    e, plddt = load(acc)
    seq = e["sequence"]
    print(f"{label}  [{e['modelEntityId']} v{e['latestVersion']}, {len(seq)} aa]")
    print(f"   model residue at {pos}: {seq[pos-1]}  -> {'match' if seq[pos-1]==ref else 'MISMATCH'}")
    if off:
        p = pos + off
        print(f"   model residue at {pos}+{off}={p}: {seq[p-1]}  -> {'match' if seq[p-1]==ref else 'MISMATCH'}"
              f"  (pLDDT {plddt[p]})")
    else:
        print(f"   pLDDT {plddt[pos]}")
