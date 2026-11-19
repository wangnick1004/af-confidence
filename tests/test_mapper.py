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
