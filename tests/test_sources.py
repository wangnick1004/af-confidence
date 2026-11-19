"""Data-source behaviour: name resolution, isoforms, cache, retries, warnings (no network)."""
import io
import json
import shutil
import urllib.error
from pathlib import Path

import pytest

from af_confidence import sources
from af_confidence.sources import Client, NotFound, SourceError, is_accession

CACHE = Path(__file__).resolve().parent.parent / "data" / "cache"


@pytest.fixture
def client():
    return Client(CACHE, offline=True)


@pytest.fixture
def tmp_cache(tmp_path):
    shutil.copytree(CACHE, tmp_path / "cache")
    return tmp_path / "cache"


@pytest.mark.parametrize("text", ["P68871", "p68871", "P04637-2", "A0A024R161", "Q8WZ42"])
def test_accessions(text):
    assert is_accession(text)


@pytest.mark.parametrize("text", ["HBB", "TP53", "E6V", "P0463", "P04637-"])
def test_not_accessions(text):
    assert not is_accession(text)


@pytest.mark.parametrize("gene,acc", [("HBB", "P68871"), ("hbb", "P68871"), ("SERPINA1", "P01009"),
                                      ("APP", "P05067"), ("p53", "P04637")])
def test_gene_names(client, gene, acc):
    assert client.resolve(gene) == acc


def test_unknown_gene(client):
    with pytest.raises(SourceError, match="no reviewed UniProt entry"):
        client.resolve("NOTAGENE123")


def test_ambiguous_gene(tmp_cache):
    (tmp_cache / "gene_9606_XYZ1.json").write_text(json.dumps({"results": [
        {"primaryAccession": "P11111", "genes": [{"geneName": {"value": "XYZ1A"}}]},
        {"primaryAccession": "P22222", "genes": [{"geneName": {"value": "XYZ1B"}}]}]}))
    with pytest.raises(SourceError, match="ambiguous: P11111"):
        Client(tmp_cache, offline=True).resolve("XYZ1")


def test_exact_primary_name_wins(tmp_cache):
    (tmp_cache / "gene_9606_XYZ1.json").write_text(json.dumps({"results": [
        {"primaryAccession": "P11111", "genes": [{"geneName": {"value": "XYZ1"}}]},
        {"primaryAccession": "P22222", "genes": [{"geneName": {"value": "OTHER"}}]}]}))
    assert Client(tmp_cache, offline=True).resolve("XYZ1") == "P11111"


def test_isoform_accession_is_the_target(client):
    p = client.protein("P04637-2")
    assert p.canonical.entry_id == "AF-P04637-2-F1"
    assert "AF-P04637-F1" in [m.entry_id for m in p.models[1:]]


def test_isoform_inherits_identical_n_terminal_processing(client):
    p = client.protein("P01009-2")
    assert ("Signal", 1, 24, "") in p.processing


def test_missing_uniprot_gives_warning(tmp_cache):
    (tmp_cache / "uniprot_P68871.json").unlink()
    p = Client(tmp_cache, offline=True).protein("P68871")
    assert p.processing == [] and "annotated offsets were not checked" in p.warnings[0]


def test_old_sequence_warning(tmp_cache):
    f = tmp_cache / "api_P68871.json"
    data = json.loads(f.read_text())
    data[0]["uniprotSequence"] = "M" + data[0]["sequence"]
    f.write_text(json.dumps(data))
    p = Client(tmp_cache, offline=True).protein("P68871")
    assert any("older UniProt sequence" in w for w in p.warnings)


def test_no_model(tmp_cache):
    (tmp_cache / "api_Q8WZ42.json").write_text("[]")
    with pytest.raises(SourceError, match="no AlphaFold DB model"):
        Client(tmp_cache, offline=True).protein("Q8WZ42")


def test_corrupt_cache_offline_is_reported(tmp_cache):
    (tmp_cache / "api_P68871.json").write_text("{not json")
    with pytest.raises(SourceError, match="corrupt"):
        Client(tmp_cache, offline=True).protein("P68871")


# ---- network behaviour, with urlopen replaced ----

class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def fake_urlopen(outcomes, calls):
    def _open(req, timeout=None):
        calls.append(req)
        out = outcomes.pop(0)
        if isinstance(out, Exception):
            raise out
        return FakeResponse(json.dumps(out).encode())
    return _open


def http_error(code):
    return urllib.error.HTTPError("https://x", code, "err", {}, None)


def test_retries_then_succeeds(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(sources.urllib.request, "urlopen",
                        fake_urlopen([http_error(503), urllib.error.URLError("reset"), {"ok": 1}], calls))
    c = Client(tmp_path, retry_wait=0)
    assert c._get_json("https://alphafold.ebi.ac.uk/x", "x.json") == {"ok": 1}
    assert len(calls) == 3
    assert calls[0].get_header("User-agent").startswith("af-confidence/")
    assert json.loads((tmp_path / "x.json").read_text()) == {"ok": 1}    # cached
    assert not list(tmp_path.glob("*.tmp"))


def test_gives_up_after_retries(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(sources.urllib.request, "urlopen",
                        fake_urlopen([http_error(503)] * 3, calls))
    with pytest.raises(SourceError, match="after 3 attempts"):
        Client(tmp_path, retry_wait=0)._get_json("https://alphafold.ebi.ac.uk/x", "x.json")
    assert not (tmp_path / "x.json").exists()


def test_404_is_not_retried(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(sources.urllib.request, "urlopen", fake_urlopen([http_error(404)], calls))
    with pytest.raises(NotFound):
        Client(tmp_path, retry_wait=0)._get_json("https://alphafold.ebi.ac.uk/x", "x.json")
    assert len(calls) == 1


def test_corrupt_cache_is_refetched_online(tmp_path, monkeypatch):
    (tmp_path / "x.json").write_text("{broken")
    calls = []
    monkeypatch.setattr(sources.urllib.request, "urlopen", fake_urlopen([{"ok": 2}], calls))
    assert Client(tmp_path, retry_wait=0)._get_json("https://x.org/x", "x.json") == {"ok": 2}


def test_no_model_is_cached(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(sources.urllib.request, "urlopen", fake_urlopen([http_error(404)], calls))
    with pytest.raises(SourceError, match="no AlphaFold DB model"):
        Client(tmp_path, retry_wait=0).models("Q8WZ42")
    with pytest.raises(SourceError, match="no AlphaFold DB model"):   # offline: same answer
        Client(tmp_path, offline=True).models("Q8WZ42")
    assert len(calls) == 1


# ---- less common branches ----

def fake_entry(acc, seq, entry=None, entity="protein"):
    entry = entry or f"AF-{acc}-F1"
    return {"modelEntityId": entry, "uniprotAccession": acc, "latestVersion": 6, "sequence": seq,
            "uniprotSequence": seq, "sequenceStart": 1, "entityType": entity,
            "plddtDocUrl": f"https://alphafold.ebi.ac.uk/files/{entry}-confidence_v6.json"}


def write(cache, name, data):
    cache.mkdir(parents=True, exist_ok=True)
    (cache / name).write_text(json.dumps(data), encoding="utf-8")


def test_default_cache_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    assert sources.default_cache_dir() == tmp_path / "af-confidence"
    monkeypatch.delenv("XDG_CACHE_HOME")
    assert sources.default_cache_dir().name == "af-confidence"


def test_unaligned_uniprot_sequence_drops_annotations(tmp_path):
    # the current UniProt sequence is not a stretch of the model sequence (or vice versa)
    write(tmp_path, "api_P11111.json", [fake_entry("P11111", "MKTAYIAKQRQISFVKSHFSRQ")])
    write(tmp_path, "uniprot_P11111.json", {
        "features": [{"type": "Signal", "location": {"start": {"value": 1}, "end": {"value": 5}}}],
        "sequence": {"value": "MKTAYIAKQRQWSFVKSHFSRQ"}})                 # one substitution
    p = Client(tmp_path, offline=True).protein("P11111")
    assert p.processing == [] and p.uniprot_shift == 0
    assert any("cannot be aligned" in w for w in p.warnings)


def test_isoform_missing_from_base_list_is_fetched(tmp_path):
    write(tmp_path, "api_P11111.json", [fake_entry("P11111", "MKTAYIAK")])
    write(tmp_path, "api_P11111-2.json", [fake_entry("P11111-2", "MKTAYIAKQQ")])
    models = Client(tmp_path, offline=True).models("P11111-2")
    assert [m.accession for m in models] == ["P11111-2", "P11111"]


def test_non_protein_entries_are_skipped(tmp_path):
    write(tmp_path, "api_P11111.json", [fake_entry("P11111", "MKTAYIAK"),
                                        fake_entry("P11111", "ACGU", "AF-X-RNA", entity="rna")])
    assert [m.entry_id for m in Client(tmp_path, offline=True).models("P11111")] == ["AF-P11111-F1"]


def test_uniprot_entry_not_found_and_bad_features(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(sources.urllib.request, "urlopen", fake_urlopen([http_error(404)], calls))
    assert Client(tmp_path, retry_wait=0).processing_features("P11111") == []
    write(tmp_path, "uniprot_P22222.json", {"features": [
        {"type": "Signal", "location": {"start": {"value": None}, "end": {"value": 5}}},
        {"type": "Chain", "location": {"start": {"value": 6}, "end": {"value": 50}}}]})
    assert Client(tmp_path, offline=True).processing_features("P22222") == [("Chain", 6, 50, "")]


@pytest.mark.parametrize("query", ["bad name!", "x" * 40, ""])
def test_rejects_invalid_protein_names(client, query):
    with pytest.raises(SourceError, match="neither a UniProt accession nor a gene name"):
        client.resolve(query)


def test_other_http_errors_are_not_retried(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(sources.urllib.request, "urlopen", fake_urlopen([http_error(403)], calls))
    with pytest.raises(SourceError, match="HTTP 403"):
        Client(tmp_path, retry_wait=0)._get_json("https://alphafold.ebi.ac.uk/x", "x.json")
    assert len(calls) == 1


def test_timeouts_and_bad_json_are_retried(tmp_path, monkeypatch):
    calls = []

    class BadJson(FakeResponse):
        pass

    outcomes = [TimeoutError("timed out"), ConnectionResetError(), BadJson(b"<html>")]

    def _open(req, timeout=None):
        calls.append(req)
        out = outcomes.pop(0)
        if isinstance(out, Exception):
            raise out
        return out
    monkeypatch.setattr(sources.urllib.request, "urlopen", _open)
    with pytest.raises(SourceError, match="invalid JSON"):
        Client(tmp_path, retry_wait=0)._get_json("https://alphafold.ebi.ac.uk/x", "x.json")
    assert len(calls) == 3
