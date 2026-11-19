"""ChimeraX command script output (--format chimerax).

ChimeraX cannot run in CI, so these tests check the script against the syntax documented in the
ChimeraX User Guide: only known commands, residue specs without spaces, valid target names,
the exact AlphaFold DB identifier with version, and model numbering.
"""
import re
from pathlib import Path

import pytest

from af_confidence.chimerax import render_chimerax, residue_spec
from af_confidence.cli import main
from af_confidence.mapper import ProteinReport, Result, check_protein
from af_confidence.sources import Client
from af_confidence.variants import parse_variant

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
KNOWN_COMMANDS = {"close", "alphafold", "name", "show", "color", "label", "tile", "view"}
SPEC = r"#\d+/A:\d+(-\d+)?(,\d+(-\d+)?)*"


@pytest.fixture
def client():
    return Client(CACHE, offline=True)


def script(client, *pairs):
    return render_chimerax([check_protein(q, vs, client) for q, vs in pairs])


def commands(text):
    return [l for l in text.splitlines() if l.strip() and not l.lstrip().startswith("#")]


@pytest.mark.parametrize("residues,spec", [
    ([7], "#1/A:7"), ([366, 288], "#1/A:288,366"), ([693, 692, 673, 693], "#1/A:673,692-693")])
def test_residue_spec(residues, spec):
    assert residue_spec(1, residues) == spec


def test_hbs_script(client):
    s = script(client, ("HBB", ["E6V"]))
    assert commands(s) == [
        "close session",
        "alphafold fetch AF-P68871-F1-v6",
        "name afc_m1_fixed_medium #1/A:7",
        "show #1/A:7 atoms",
        "color #1/A:7 violet target a",
        'label #1/A:7 residues text "E6V"',
        "view",
    ]


def test_two_models_are_numbered_and_tiled(client):
    s = script(client, ("P43251", ["F108V", "A151T", "P371S"]))
    cmds = commands(s)
    assert "alphafold fetch AF-P43251-F1-v6" in cmds and "alphafold fetch AF-P43251-4-F1-v6" in cmds
    assert "color #1/A:128,171,391 magenta target a" in cmds
    assert "color #2/A:108,151,371 magenta target a" in cmds
    assert cmds[-2:] == ["tile", "view"]
    assert "# warning: the current UniProt sequence of P43251" in s


def test_ambiguous_and_shared_positions(client):
    s = script(client, ("APP", ["A2T", "A21G", "E22G", "E22Q", "D23N"]))
    cmds = commands(s)
    assert "color #1/A:673,692-693 magenta target a" in cmds
    assert "color #1/A:23,694 white target a" in cmds
    assert 'label #1/A:693 residues text "E22G/E22Q"' in cmds
    assert 'label #1/A:23 residues text "D23N?"' in cmds and 'label #1/A:694 residues text "D23N?"' in cmds


def test_errors_and_not_placed_are_comments(client):
    s = script(client, ("NOTAGENE123", ["A1V"]), ("TP53", ["F20L"]))
    assert commands(s) == ["close session"]
    assert "# NOTAGENE123: error:" in s and "# not placed: F20L:" in s


def test_model_numbering_uses_model_residue_numbers():
    # a model whose first residue is 11: the 5th residue of the model is residue 15 in the file
    v = parse_variant("A15V")
    rep = ProteinReport("X", "P11111", "AF-X-F1", results=[Result("A15V", v, "match", "AF-X-F1", "A")],
                        models={"AF-X-F1": (11, 50, "P11111")}, versions={"AF-X-F1": 6})
    assert "color #1/A:15 lime target a" in commands(render_chimerax([rep]))


@pytest.mark.parametrize("args", [
    ["-f", str(ROOT / "examples" / "mixed_proteins.txt")],
    ["APP", "-f", str(ROOT / "examples" / "app_abeta_numbering.txt")],
    ["P43251", "F108V", "A151T", "P371S"],
])
def test_scripts_use_only_documented_syntax(args, capsys):
    main(args + ["--cache", str(CACHE), "--offline", "--format", "chimerax"])
    out = capsys.readouterr().out
    cmds = commands(out)
    assert cmds[0] == "close session" and cmds[-1] == "view"
    for c in cmds:
        word = c.split()[0]
        assert word in KNOWN_COMMANDS, c
        if word == "alphafold":
            assert re.fullmatch(r"alphafold fetch AF-[A-Z0-9]+(-\d+)?-F\d+-v\d+", c), c
        if word == "name":
            assert re.fullmatch(rf"name afc_m\d+_(ok|fixed_strong|fixed_medium|ambiguous) {SPEC}", c), c
        if word in ("show", "color", "label"):
            assert re.match(rf"{word} {SPEC} ", c), c
    # every model referenced was fetched before
    fetched = sum(c.startswith("alphafold fetch") for c in cmds)
    used = {int(m) for m in re.findall(r"#(\d+)/", "\n".join(cmds))}
    assert used == set(range(1, fetched + 1))
