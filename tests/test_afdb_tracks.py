"""AlphaFold DB custom annotation tracks (--format afdb)."""
from pathlib import Path

import pytest

from af_confidence.afdb_tracks import (AFDB_RESIDUES_RE, TRACK_AMBIGUOUS, TRACK_MEDIUM, TRACK_OK,
                                       TRACK_ORDER, TRACK_STRONG, build_tracks, format_residues,
                                       render_afdb)
from af_confidence.cli import main
from af_confidence.mapper import ProteinReport, Result, check_protein
from af_confidence.sources import Client
from af_confidence.variants import parse_variant

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"


@pytest.fixture
def client():
    return Client(CACHE, offline=True)


def tracks(query, variants, client):
    return build_tracks(check_protein(query, variants, client))


@pytest.mark.parametrize("positions,text", [
    ([7], "7"), ([693, 692, 673, 693], "673, 692-693"), ([1, 2, 3, 5], "1-3, 5"),
    ([10, 9, 8, 7], "7-10"), ([], "")])
def test_format_residues(positions, text):
    assert format_residues(positions) == text


def test_track_names_are_not_truncated_by_afdb():
    # the AFDB viewer truncates track names of 15 characters or more
    assert all(len(t) < 15 for t in TRACK_ORDER)


def test_hbs_single_variant(client):
    pt = tracks("HBB", ["E6V"], client)
    (e,) = pt.entries
    assert e.entry_id == "AF-P68871-F1" and e.url.endswith("/entry/AF-P68871-F1")
    assert e.tracks == {TRACK_MEDIUM: [7]}


def test_serpina1_alleles_are_strong(client):
    (e,) = tracks("P01009", ["E342K", "E264V"], client).entries
    assert e.residues(TRACK_STRONG) == "288, 366"


def test_app_list_with_ambiguous_match(client):
    (e,) = tracks("APP", ["A2T", "A21G", "E22G", "E22Q", "D23N"], client).entries
    assert e.residues(TRACK_STRONG) == "673, 692-693"
    assert e.residues(TRACK_AMBIGUOUS) == "23, 694"
    assert TRACK_OK not in e.tracks


def test_matches_and_swapped(client):
    (e,) = tracks("TP53", ["R175H", "R72P"], client).entries
    assert e.tracks == {TRACK_OK: [175], TRACK_MEDIUM: [72]}


def test_sequence_update_gives_two_models(client):
    pt = tracks("P43251", ["F108V", "A151T", "P371S"], client)
    assert [e.entry_id for e in pt.entries] == ["AF-P43251-F1", "AF-P43251-4-F1"]
    assert pt.entries[0].residues(TRACK_STRONG) == "128, 171, 391"
    assert pt.entries[1].residues(TRACK_STRONG) == "108, 151, 371"
    assert pt.warnings and "AF-P43251-4-F1" in pt.warnings[0]


def test_weak_or_unresolved_variants_are_not_placed(client):
    pt = tracks("TP53", ["F20L", "E999K", "c.1A>T"], client)
    assert pt.entries == []
    assert [n.split(":")[0] for n in pt.not_placed] == ["F20L", "E999K", "c.1A>T"]


def test_protein_error(client):
    pt = tracks("NOTAGENE123", ["A1V"], client)
    assert pt.error and pt.entries == []


def test_positions_are_converted_to_model_residues():
    # a model that starts at residue 11: residue 15 is the 5th residue AFDB shows
    v = parse_variant("A15V")
    rep = ProteinReport("X", "P11111", "AF-X-F1",
                        results=[Result("A15V", v, "match", "AF-X-F1", "A")],
                        models={"AF-X-F1": (11, 50, "P11111")})
    (e,) = build_tracks(rep).entries
    assert e.tracks == {TRACK_OK: [5]}


@pytest.mark.parametrize("args", [
    ["-f", str(ROOT / "examples" / "mixed_proteins.txt")],
    ["APP", "-f", str(ROOT / "examples" / "app_abeta_numbering.txt")],
    ["P01009", "-f", str(ROOT / "examples" / "serpina1_alleles.txt")],
    ["P43251", "F108V", "A151T", "P371S"],
])
def test_every_residue_string_passes_afdb_validation(client, args, capsys):
    main(args + ["--cache", str(CACHE), "--offline", "--format", "afdb"])
    out = capsys.readouterr().out
    lines = [l for l in out.splitlines() if l.strip().startswith("Residues or ranges:")]
    assert lines
    for l in lines:
        assert AFDB_RESIDUES_RE.match(l.split(":", 1)[1].strip()), l


def test_residues_stay_within_model_length(client):
    for query, vs in [("APP", ["A2T", "A21G", "E22G", "E22Q", "D23N"]), ("P43251", ["F108V", "A151T", "P371S"])]:
        for e in tracks(query, vs, client).entries:
            assert all(1 <= p <= e.length for ps in e.tracks.values() for p in ps)


def test_render_mentions_dialog_and_urls(client):
    out = render_afdb([check_protein("HBB", ["E6V"], client)])
    assert "Add your annotation track" in out and "https://alphafold.ebi.ac.uk/entry/AF-P68871-F1" in out
    assert "Track name:          Fixed medium" in out and "Residues or ranges:  7" in out


def test_render_lists_not_placed(client):
    out = render_afdb([check_protein("TP53", ["F20L"], client)])
    assert "TP53 -> P04637: nothing to place" in out
    assert "not placed: F20L: model has S at 20, not F; only weak suggestions" in out


def test_suggestion_outside_the_model_is_not_placed():
    from af_confidence.mapper import Suggestion
    v = parse_variant("A15V")
    r = Result("A15V", v, "mismatch", "AF-X-F1", "G", message="model has G at 15, not A",
               suggestions=[Suggestion("annotated_offset", "strong", 100, "AF-X-F1", "+85")])
    rep = ProteinReport("X", "P11111", "AF-X-F1", results=[r], models={"AF-X-F1": (1, 50, "P11111")})
    pt = build_tracks(rep)
    assert pt.entries == [] and pt.not_placed[0].startswith("A15V: model has G at 15")
