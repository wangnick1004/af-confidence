"""Execute a notebook top to bottom and fail on the first error (used by the weekly CI check).

    python scripts/check_notebook.py examples/colab_quickstart.ipynb [--local PATH]

--local PATH replaces the notebook's `%pip install git+https://...` cell with an install of PATH,
so the checked-out code is tested instead of what is on GitHub.
Needs: pip install nbclient nbformat ipykernel pandas
"""
import argparse
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("notebook")
    ap.add_argument("--local", help="install this path instead of the GitHub version")
    args = ap.parse_args()
    nb = nbformat.read(args.notebook, as_version=4)
    nbformat.validate(nb)
    if args.local:
        cells = [c for c in nb.cells if c.cell_type == "code" and "pip install" in c.source]
        if len(cells) != 1:
            print("expected exactly one install cell", file=sys.stderr)
            return 1
        cells[0].source = f"%pip install -q {args.local}"
    with tempfile.TemporaryDirectory() as work:
        try:
            NotebookClient(nb, timeout=600, kernel_name="python3",
                           resources={"metadata": {"path": work}}).execute()
        except CellExecutionError as exc:
            print(exc, file=sys.stderr)
            return 1
    n = sum(c.cell_type == "code" for c in nb.cells)
    print(f"{args.notebook}: all {n} code cells ran without errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
