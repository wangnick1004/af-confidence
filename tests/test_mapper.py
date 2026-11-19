"""Tests run offline against the AlphaFold DB / UniProt files cached in data/cache.

Expected residues were checked against UniProt on 2026-11-19 (see docs/day1_report.md).
"""
from pathlib import Path

import pytest

from af_confidence.mapper import consistent_offset, expected_by_chance, map_variants
from af_confidence.sources import Client, SourceError
from af_confidence.variants import parse_variant

CACHE = Path(__file__).resolve().parent.parent / "data" / "cache"


@pytest.fixture
def client():
    return Client(CACHE, offline=True)


def kinds(result):
    return [s.kind for s in result.suggestions]


def test_hbs_legacy_numbering(client):
    (r,) = map_variants("P68871", ["E6V"], client)
    assert r.status == "mismatch" and r.model_residue == "P"
    (s,) = r.suggestions
    assert s.kind == "annotated_offset" and s.position == 7
    assert s.plddt == pytest.approx(96.56)


def test_hbs_hgvs_numbering_matches(client):
    (r,) = map_variants("P68871", ["p.Glu7Val"], client)
    assert r.status == "match" and r.plddt == pytest.approx(96.56)


def test_z_allele_mature_numbering(client):
    (r,) = map_variants("P01009", ["E342K"], client)
    assert r.status == "mismatch" and r.model_residue == "L"
    assert r.suggestions[0].kind == "annotated_offset" and r.suggestions[0].position == 366


def test_z_and_s_alleles_together(client):
    # S allele: E264V in mature numbering = E288V in precursor numbering
    results = map_variants("P01009", ["E342K", "E264V"], client)
    assert [r.suggestions[0].position for r in results] == [366, 288]
    assert all(r.suggestions[0].kind == "annotated_offset" for r in results)


def test_tp53_canonical(client):
    (r,) = map_variants("P04637", ["R175H"], client)
    assert r.status == "match" and r.plddt == pytest.approx(96.62)


def test_off_by_one_is_weak_nearby(client):
    (r,) = map_variants("P04637", ["F20L"], client)
    assert r.model_residue == "S"
    assert kinds(r) == ["nearby"] and r.suggestions[0].position == 19


def test_swapped_ref_alt(client):
    (r,) = map_variants("P04637", ["R72P"], client)
    assert "swapped" in kinds(r)


def test_isoform_match(client):
    # canonical has I at 332; isoform P04637-3 has M there
    (r,) = map_variants("P04637", ["M332L"], client)
    iso = [s for s in r.suggestions if s.kind == "isoform"]
    assert [s.entry_id for s in iso] == ["AF-P04637-3-F1"]


def test_consistent_offset_without_annotation(client):
    # TP53 hotspots written 5 positions too low; TP53 has no processing annotation
    results = map_variants("P04637", ["R170H", "R243Q", "R268H", "R243W"], client)
    for r, true_pos in zip(results, [175, 248, 273, 248]):
        assert r.status == "mismatch"
        assert any(s.kind == "consistent_offset" and s.position == true_pos for s in r.suggestions)


def test_single_variant_never_gets_consistent_offset(client):
    model = client.models("P04637")[0]
    assert consistent_offset(model, [parse_variant("R170H")]) is None


def test_expected_by_chance_is_composition_based():
    assert expected_by_chance("AAAA", ["A", "A"], 10) == pytest.approx(10.0)
    assert expected_by_chance("ACDE", ["A"], 4) == pytest.approx(1.0)


def test_invalid_and_out_of_range(client):
    r1, r2 = map_variants("P04637", ["c.524G>A", "E999K"], client)
    assert r1.status == "invalid" and r2.status == "out_of_range"


def test_offline_missing_protein(client):
    with pytest.raises(SourceError):
        map_variants("Q99999", ["A1V"], client)


# ---- day 3: evidence strength, fragments, ambiguous matches, isoform pLDDT ----

def strengths(result):
    return [(s.kind, s.strength) for s in result.suggestions]


def test_single_variant_annotated_offset_is_medium(client):
    # one variant can match an annotated shift by coincidence (~1 in 20): medium, not strong
    (r,) = map_variants("P68871", ["E6V"], client)
    assert strengths(r) == [("annotated_offset", "medium")]


def test_two_variants_on_same_annotated_offset_are_strong(client):
    results = map_variants("P01009", ["E342K", "E264V"], client)
    assert all(strengths(r) == [("annotated_offset", "strong")] for r in results)


def test_primary_offset_with_one_variant_is_weak_when_batch_points_elsewhere(client):
    # A2T and E22G share +671 (amyloid-beta); F19L alone fits... nothing primary, so check that
    # no primary single-match is promoted when another shift explains >= 2 inputs
    results = map_variants("P05067", ["A2T", "E22G", "L4V"], client)
    for r in results:
        for s in r.suggestions:
            if s.kind == "annotated_offset" and "explains 1/" in s.note:
                assert s.strength == "weak"


def test_app_abeta_batch(client):
    # Abeta numbering: Abeta residue 1 = APP770 residue 672 (UniProt chains start at 672)
    results = map_variants("P05067", ["A2T", "A21G", "E22G", "E22Q"], client)
    for r, true_pos in zip(results, [673, 692, 693, 693]):
        assert r.status == "mismatch"
        assert strengths(r) == [("annotated_offset", "strong")]
        assert r.suggestions[0].position == true_pos
        assert "Amyloid-beta protein 42" in r.suggestions[0].note


def test_uniprot_sequence_update_is_detected(client):
    # Biotinidase: UniProt changed the canonical sequence in 2026 (now 20 residues shorter at
    # the N-terminus); the AlphaFold DB model still uses the old 543-aa sequence
    p = client.protein("P43251")
    assert p.uniprot_shift == 20
    assert any("current UniProt sequence" in w for w in p.warnings)
    # AlphaFold DB also has the new canonical sequence, filed under isoform 4
    assert any("AF-P43251-4-F1" in w and "use it" in w for w in p.warnings)
    results = map_variants("P43251", ["F108V", "A151T", "P371S"], client)
    for r, true_pos in zip(results, [128, 171, 391]):
        assert r.status == "mismatch"
        assert r.suggestions[0].kind == "annotated_offset"
        assert r.suggestions[0].strength == "strong" and r.suggestions[0].position == true_pos


def test_app_single_fragment_offset_is_weak(client):
    (r,) = map_variants("P05067", ["A2T"], client)
    assert r.suggestions and all(s.strength == "weak" for s in r.suggestions)
    assert 673 in [s.position for s in r.suggestions]


def test_coincidental_match_flagged_in_batch(client):
    # Iowa D23N (Abeta numbering) = D694N; residue 23 of APP770 also happens to be D
    # (with ~16 annotated APP fragments, two agreeing variants are not enough for strong
    # evidence after correction for multiple shifts; three are)
    results = map_variants("P05067", ["A2T", "A21G", "E22G", "D23N"], client)
    d23n = results[3]
    assert d23n.status == "ambiguous_match"
    assert [s.position for s in d23n.suggestions] == [694]


def test_coincidental_match_alone_is_not_detectable(client):
    (r,) = map_variants("P05067", ["D23N"], client)
    assert r.status == "match"


def test_isoform_plddt_shown_when_cached(client):
    (r,) = map_variants("P04637", ["M332L"], client)
    (s,) = [s for s in r.suggestions if s.kind == "isoform"]
    assert s.strength == "weak" and s.plddt == pytest.approx(79.88)


def test_weak_hidden_when_strong_exists(client):
    # E6V has a strong explanation, so no 'nearby' noise is shown
    (r,) = map_variants("P68871", ["E6V"], client)
    assert "nearby" not in kinds(r)


def test_two_variants_not_enough_with_many_fragments(client):
    results = map_variants("P05067", ["A2T", "E22G"], client)
    assert all(s.strength != "strong" for r in results for s in r.suggestions)


def test_chance_of_support():
    from af_confidence.mapper import chance_of_support
    seq = "ACDEFGHIKLMNPQRSTVWY"           # every residue 1/20
    assert chance_of_support(seq, ["A"], 1) == pytest.approx(0.05)
    assert chance_of_support(seq, ["A", "C"], 2) == pytest.approx(0.0025)
    assert chance_of_support(seq, ["A", "C"], 0) == pytest.approx(1.0)


def test_consistent_offset_rejected_when_plausible_by_chance():
    from af_confidence.mapper import consistent_offset
    from af_confidence.sources import Model
    # 20 distinct residues: shift -1 is the only one that fits both variants, but with 40
    # shifts tried and p = 1/20 per residue, 40 * (1/20)**2 = 0.1 expected coincidences
    m = Model("AF-T-F1", "T", 6, "ACDEFGHIKLMNPQRSTVWY", 1, "")
    variants = [parse_variant("A2V"), parse_variant("C3V")]
    assert consistent_offset(m, variants) is None
