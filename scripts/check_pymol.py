"""Run an af-confidence PyMOL script in PyMOL and check the result (used by the weekly CI check).

    python scripts/check_pymol.py markers.pml [--png out.png]

Runs `pymol -cq markers.pml` plus a verification step in the same session, and fails if PyMOL
printed an error, a model did not load, a named selection is empty, a marked side chain has
the wrong color, a marked residue lost its pLDDT cartoon color, or labels are missing.
Run it with a Python that has open-source PyMOL: pip install pymol-open-source-whl
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

VERIFY = r'''
from pymol import cmd
import re, sys
script = open(SCRIPT, encoding="utf-8").read()
problems = []
objects = re.findall(r"^load \S+, (\S+)$", script, re.M)
for obj in objects:
    if cmd.count_atoms(obj) == 0:
        problems.append(f"model {obj} has no atoms")
colors = {"green": "green", "magenta": "magenta", "violet": "violet", "white": "white"}
plddt = {cmd.get_color_index(n) for n in ("afc_plddt_vlow", "afc_plddt_low", "afc_plddt_high", "afc_plddt_vhigh")}
sels = re.findall(r"^select (\S+), (.+)$", script, re.M)
for sel, _ in sels:
    n = cmd.count_atoms(sel)
    if n == 0:
        problems.append(f"selection {sel} is empty")
        continue
    want = re.search(r"^color (\S+), " + re.escape(sel) + r" and not", script, re.M).group(1)
    side, ca = [], []
    cmd.iterate(sel + " and not name N+C+O+CA", "side.append(color)", space={"side": side})
    cmd.iterate(sel + " and name CA", "ca.append(color)", space={"ca": ca})
    if not side or any(c != cmd.get_color_index(want) for c in side):
        problems.append(f"{sel}: side-chain color is not {want}")
    if not ca or any(c not in plddt for c in ca):
        problems.append(f"{sel}: C-alpha (cartoon) lost its pLDDT color")
labels = re.findall(r"^label (.+), \"", script, re.M)
labelled = []
cmd.iterate("all", "labelled.append(label)", space={"labelled": labelled})
if len([l for l in labelled if l]) != len(labels):
    problems.append(f"expected {len(labels)} labels, found {len([l for l in labelled if l])}")
if PNG:
    cmd.set("ray_opaque_background", 1)
    cmd.png(PNG, width=1200, height=900, dpi=150, ray=1)
print("VERIFY", "OK" if not problems else "FAILED", len(objects), "models,", len(sels), "selections,", len(labels), "labels")
for p in problems:
    print("PROBLEM", p)
'''


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--png", help="also render an image")
    ap.add_argument("--pymol", help="PyMOL executable (default: run PyMOL with this Python, "
                                     "python -m pymol)")
    args = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        verify = os.path.join(tmp, "verify.py")
        with open(verify, "w", encoding="utf-8") as fh:
            fh.write(f"SCRIPT = {os.path.abspath(args.script)!r}\nPNG = {args.png and os.path.abspath(args.png)!r}\n")
            fh.write(VERIFY)
        launcher = [args.pymol] if args.pymol else [sys.executable, "-m", "pymol"]
        out = subprocess.run(launcher + ["-cq", args.script, verify], capture_output=True, text=True)
    text = out.stdout + out.stderr
    print(text.strip())
    errors = [l for l in text.splitlines() if re.search(r"Error|Exception|Traceback|Unknown command", l)]
    if out.returncode or errors or "VERIFY OK" not in text:
        print("check_pymol: FAILED", file=sys.stderr)
        return 1
    print("check_pymol: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
