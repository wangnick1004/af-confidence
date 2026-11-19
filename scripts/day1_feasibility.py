"""Day 1 feasibility checks (reads cached files in data/cache)."""
import json, sys
from pathlib import Path
from Bio.PDB import PDBParser, PPBuilder

C = Path(__file__).resolve().parent.parent / "data" / "cache"
api = json.load(open(C / "api_P04637.json"))
canon = next(e for e in api if e["uniprotAccession"] == "P04637")
conf = json.load(open(C / "AF-P04637-F1-confidence_v6.json"))
plddt = dict(zip(conf["residueNumber"], conf["confidenceScore"]))
cats = dict(zip(conf["residueNumber"], conf["confidenceCategory"]))

s = PDBParser(QUIET=True).get_structure("tp53", C / "AF-P04637-F1-model_v6.pdb")
pdb_seq = "".join(str(pp.get_sequence()) for pp in PPBuilder().build_peptides(s))
bfac = {r.id[1]: r["CA"].get_bfactor() for r in s[0]["A"]}

print("Check 1  API entry:", canon["modelEntityId"], "version", canon["latestVersion"], "length", canon["sequenceEnd"])
print("Check 2  pLDDT residues read:", len(plddt), "| max |JSON - PDB B-factor| =",
      round(max(abs(plddt[i] - bfac[i]) for i in plddt), 3))
print("         sequence: PDB == API sequence:", pdb_seq == canon["sequence"],
      "| API sequence == UniProt sequence:", canon["sequence"] == canon["uniprotSequence"])
for pos, wt in [(175, "R"), (72, "P"), (248, "R"), (273, "R"), (19, "F"), (20, "F")]:  # (20,"F") is a deliberate wrong input; residue 20 is S
    aa = canon["sequence"][pos - 1]
    print(f"Check 3  pos {pos}: expected {wt}, model has {aa} -> {'OK' if aa == wt else 'MISMATCH'} | pLDDT {plddt[pos]} ({cats[pos]})")
print("Check 4  Python", sys.version.split()[0])
