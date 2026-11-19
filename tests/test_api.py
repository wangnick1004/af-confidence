"""Public Python interface (import af_confidence as afc)."""
import sys
from pathlib import Path

import pytest

import af_confidence as afc

ROOT = Path(__file__).resolve().parent.parent
C = dict(cache=ROOT / "data" / "cache", offline=True)


def test_top_level_exports():
    for name in afc.__all__:
        assert hasattr(afc, name), name


def test_check_one_protein():
    rep = afc.check("HBB", ["E6V"], **C)
    assert rep.accession == "P68871" and rep.entry_id == "AF-P68871-F1"
    assert rep.results[0].suggestions[0].position == 7


def test_variants_as_one_string():
    rep = afc.check("P01009", "E342K, E264V", **C)
    assert [r.input for r in rep.results] == ["E342K", "E264V"]


def test_check_list_mapping_merges_gene_and_accession():
    reps = afc.check_list({"SERPINA1": ["E342K"], "P01009": "E264V"}, **C)
    assert len(reps) == 1 and [r.input for r in reps[0].results] == ["E342K", "E264V"]
    # merged, so batch evidence makes both strong
    assert all(r.suggestions[0].strength == "strong" for r in reps[0].results)


def test_check_list_pairs_and_errors():
    reps = afc.check_list([("HBB", "E6V"), ("NOTAGENE123", ["A1V"])], **C)
    assert reps[0].accession == "P68871" and reps[1].error


@pytest.mark.parametrize("as_path", [False, True])
def test_check_list_file(as_path):
    f = ROOT / "examples" / "app_abeta_numbering.txt"
    reps = afc.check_list(f if as_path else str(f), protein="APP", **C)
    assert [r.status for r in reps[0].results][-1] == "ambiguous_match"


def test_check_list_file_without_protein_raises():
    with pytest.raises(afc.InputError, match="no protein given"):
        afc.check_list(ROOT / "examples" / "app_abeta_numbering.txt", **C)


def test_shared_client():
    client = afc.Client(C["cache"], offline=True)
    assert afc.check("HBB", "E6V", client=client).accession == "P68871"


def test_to_records_variant_rows():
    reps = afc.check_list({"HBB": "E6V p.Glu7Val", "TP53": "F20L", "NOTAGENE123": "A1V"}, **C)
    rows = afc.to_records(reps)
    by = {(r["protein"], r["input"]): r for r in rows}
    assert by[("HBB", "E6V")]["best_position"] == 7 and by[("HBB", "E6V")]["best_strength"] == "medium"
    assert by[("HBB", "E6V")]["best_plddt"] == pytest.approx(96.56)
    match = by[("HBB", "p.Glu7Val")]
    assert match["status"] == "match" and match["best_kind"] == "as_written" and match["best_position"] == 7
    assert by[("TP53", "F20L")]["best_strength"] == "weak"
    assert by[("NOTAGENE123", None)]["status"] == "error"
    cols = {"protein", "accession", "input", "status", "entry_id", "model_residue", "plddt",
            "best_position", "best_kind", "best_strength", "best_entry_id", "best_plddt",
            "n_suggestions", "message"}
    assert cols == set(by[("HBB", "E6V")])


def test_to_records_suggestion_rows():
    rep = afc.check("P43251", ["F108V", "A151T", "P371S", "p.Phe128Val"], **C)
    rows = afc.to_records(rep, detail="suggestion")
    assert len(rows) == 3 * 2 + 1            # two strong suggestions each, plus one plain match
    assert {r["suggestion_entry_id"] for r in rows if r["input"] == "F108V"} == {"AF-P43251-F1",
                                                                                 "AF-P43251-4-F1"}
    plain = [r for r in rows if r["input"] == "p.Phe128Val"][0]
    assert plain["suggestion_kind"] is None


def test_to_records_rejects_unknown_detail():
    with pytest.raises(ValueError):
        afc.to_records([], detail="everything")


def test_best_suggestions_keeps_the_top_strength():
    r = afc.check("P43251", ["F108V", "A151T", "P371S"], **C).results[0]
    assert {s.strength for s in afc.best_suggestions(r)} == {"strong"}
    assert afc.best_suggestions(afc.check("HBB", "p.Glu7Val", **C).results[0]) == []


def test_to_dataframe():
    pd = pytest.importorskip("pandas")
    df = afc.to_dataframe(afc.check_list({"HBB": "E6V", "SERPINA1": "E342K E264V"}, **C))
    assert isinstance(df, pd.DataFrame) and len(df) == 3
    assert list(df.loc[df["protein"] == "SERPINA1", "best_position"]) == [366, 288]


def test_to_dataframe_without_pandas(monkeypatch):
    monkeypatch.setitem(sys.modules, "pandas", None)       # import pandas now fails
    with pytest.raises(ImportError, match="pip install pandas"):
        afc.to_dataframe([])


def test_integration_outputs_accept_one_report():
    rep = afc.check("HBB", "E6V", **C)
    assert "Residues or ranges:  7" in afc.afdb_tracks(rep)
    assert "alphafold fetch AF-P68871-F1-v6" in afc.chimerax_script(rep)
    assert "load https://alphafold.ebi.ac.uk/files/AF-P68871-F1-model_v6.cif, AF_P68871_F1" in afc.pymol_script(rep)


def test_to_text_matches_command_line(capsys):
    from af_confidence.cli import main
    rep = afc.check("HBB", "E6V", **C)
    main(["HBB", "E6V", "--cache", str(C["cache"]), "--offline"])
    assert afc.to_text(rep).strip() == capsys.readouterr().out.strip()
