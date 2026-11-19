"""PyMOL script output (--format pymol).

The syntax tests need no PyMOL. If open-source PyMOL is importable (pip install
pymol-open-source-whl), the script is also run in PyMOL against the cached model files.
"""
import re
import subprocess
import sys
from pathlib import Path

import pytest

from af_confidence.cli import main
from af_confidence.mapper import ProteinReport, Result, check_protein
from af_confidence.pymol import object_name, render_pymol, resi_list
from af_confidence.sources import Client
from af_confidence.variants import parse_variant

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
KNOWN = {"delete", "set_color", "load", "hide", "show", "color", "select", "set", "label",
         "deselect", "orient"}


@pytest.fixture
def client():
    return Client(CACHE, offline=True)


def script(client, *pairs):
    return render_pymol([check_protein(q, vs, client) for q, vs in pairs])


def commands(text):
    return [l for l in text.splitlines() if l.strip() and not l.lstrip().startswith("#")]


def test_object_name_and_resi_list():
    assert object_name("AF-P43251-4-F1") == "AF_P43251_4_F1"
    assert resi_list([693, 692, 673, 693]) == "673+692-693"
    assert resi_list([7]) == "7"


def test_hbs_script(client):
    cmds = commands(script(client, ("HBB", ["E6V"])))
    assert cmds[0] == "delete all"
    assert "load https://alphafold.ebi.ac.uk/files/AF-P68871-F1-model_v6.cif, AF_P68871_F1" in cmds
    assert "color afc_plddt_vhigh, AF_P68871_F1 and b > 90" in cmds
    i = cmds.index("select afc_m1_fixed_medium, AF_P68871_F1 and chain A and resi 7")
    assert cmds[i + 1:i + 5] == [
        "show sticks, afc_m1_fixed_medium and not name N+C+O",
        "show spheres, afc_m1_fixed_medium and not name N+C+O+CA",
        "set sphere_scale, 0.6, afc_m1_fixed_medium",
        "color violet, afc_m1_fixed_medium and not name N+C+O+CA"]
    assert 'label AF_P68871_F1 and chain A and resi 7 and name CA, "E6V"' in cmds
    assert cmds[-3:] == ["deselect", "set grid_mode, 0", "orient"]


def test_two_models_use_grid_mode(client):
    cmds = commands(script(client, ("P43251", ["F108V", "A151T", "P371S"])))
    assert sum(c.startswith("load ") for c in cmds) == 2
    assert "select afc_m2_fixed_strong, AF_P43251_4_F1 and chain A and resi 108+151+371" in cmds
    assert "set grid_mode, 1" in cmds


def test_errors_and_not_placed_are_comments(client):
    s = script(client, ("NOTAGENE123", ["A1V"]), ("TP53", ["F20L"]))
    assert all(c.startswith(("delete", "set_color")) for c in commands(s))
    assert "# NOTAGENE123: error:" in s and "# not placed: F20L:" in s


def test_model_without_file_url_is_skipped():
    v = parse_variant("A15V")
    rep = ProteinReport("X", "P11111", "AF-X-F1", results=[Result("A15V", v, "match", "AF-X-F1", "A")],
                        models={"AF-X-F1": (11, 50, "P11111")}, versions={"AF-X-F1": 6})
    s = render_pymol([rep])
    assert "# AF-X-F1: no model file URL from AlphaFold DB; skipped" in s
    assert not any(c.startswith("load") for c in commands(s))


def test_model_numbering_uses_model_residue_numbers():
    v = parse_variant("A15V")
    rep = ProteinReport("X", "P11111", "AF-X-F1", results=[Result("A15V", v, "match", "AF-X-F1", "A")],
                        models={"AF-X-F1": (11, 50, "P11111")}, versions={"AF-X-F1": 6},
                        files={"AF-X-F1": "https://alphafold.ebi.ac.uk/files/AF-X-F1-model_v6.cif"})
    assert "select afc_m1_ok, AF_X_F1 and chain A and resi 15" in commands(render_pymol([rep]))


@pytest.mark.parametrize("args", [
    ["-f", str(ROOT / "examples" / "mixed_proteins.txt")],
    ["APP", "-f", str(ROOT / "examples" / "app_abeta_numbering.txt")],
    ["P43251", "F108V", "A151T", "P371S"],
])
def test_scripts_use_only_known_commands(args, capsys):
    main(args + ["--cache", str(CACHE), "--offline", "--format", "pymol"])
    cmds = commands(capsys.readouterr().out)
    objects = set()
    for c in cmds:
        word = c.split()[0]
        assert word in KNOWN, c
        if word == "load":
            m = re.fullmatch(r"load (https://alphafold\.ebi\.ac\.uk/files/AF-[A-Z0-9-]+-model_v\d+\.cif), (\w+)", c)
            assert m, c
            objects.add(m.group(2))
        if word == "select":
            m = re.fullmatch(r"select afc_m\d+_\w+, (\w+) and chain A and resi \d+(-\d+)?(\+\d+(-\d+)?)*", c)
            assert m and m.group(1) in objects, c
        if word == "label":
            assert re.fullmatch(r'label (\w+) and chain A and resi \d+ and name CA, "[^"]+"', c), c


def test_runs_in_pymol(client, tmp_path):
    pytest.importorskip("pymol")
    # same script, but loading the cached model files instead of downloading them
    s = script(client, ("HBB", ["E6V"]), ("P01009", ["E342K", "E264V"]), ("TP53", ["R175H", "R72P"]))
    for acc in ("P68871", "P01009", "P04637"):
        s = re.sub(rf"https://\S+AF-{acc}-F1-model_v6\.cif",
                   (CACHE / f"AF-{acc}-F1-model_v6.pdb").as_posix(), s)
    pml = tmp_path / "markers.pml"
    pml.write_text(s, encoding="utf-8")
    out = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_pymol.py"), str(pml)],
                         capture_output=True, text=True)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "VERIFY OK 3 models, 4 selections, 5 labels" in out.stdout
