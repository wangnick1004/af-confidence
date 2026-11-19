"""MCP server (af-confidence-mcp), tested end to end through a real MCP client over stdio.

Skipped when the mcp package is not installed (it needs Python 3.10+):
pip install "af-confidence[mcp]".
"""
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"


def call(tool=None, arguments=None, list_only=False):
    """Start the server over stdio (offline, demo cache), call one tool, return the result."""
    pytest.importorskip("mcp")
    import anyio
    from mcp.client.session import ClientSession
    from mcp.client.stdio import StdioServerParameters, stdio_client

    params = StdioServerParameters(
        command=sys.executable, args=["-m", "af_confidence.mcp_server"], cwd=str(ROOT),
        env={**os.environ, "AF_CONFIDENCE_CACHE": str(CACHE), "AF_CONFIDENCE_OFFLINE": "1",
             "PYTHONPATH": str(ROOT)})

    async def run():
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                init = await session.initialize()
                if list_only:
                    return init, await session.list_tools()
                return await session.call_tool(tool, arguments)
    return anyio.run(run)


def payload(result):
    assert not result.is_error, result.content
    return json.loads(result.content[0].text)


def test_server_lists_tools_with_instructions():
    init, tools = call(list_only=True)
    assert init.server_info.name == "af-confidence"
    assert "BEFORE you locate" in init.instructions
    by_name = {t.name: t for t in tools.tools}
    assert set(by_name) == {"check_variants", "export_markers"}
    for t in by_name.values():
        assert t.annotations.read_only_hint is True and t.description
        assert "variants_by_protein" in t.input_schema["required"]
    assert by_name["export_markers"].input_schema["properties"]["format"]["enum"] == ["afdb", "chimerax", "pymol"]


def test_check_variants_hbs():
    out = payload(call("check_variants", {"variants_by_protein": {"HBB": ["E6V"]}}))
    (p,) = out["proteins"]
    assert p["uniprot_accession"] == "P68871" and p["alphafold_model"] == "AF-P68871-F1"
    (v,) = p["variants"]
    assert v["status"] == "mismatch" and v["model_residue_at_written_position"] == "P"
    (best,) = v["best_suggestions"]
    assert best["position"] == 7 and best["strength"] == "medium" and best["plddt"] == pytest.approx(96.56)
    assert "strong" in out["evidence_levels"]


def test_check_variants_batch_and_errors():
    out = payload(call("check_variants", {"variants_by_protein": {
        "APP": ["A2T", "A21G", "E22G", "E22Q", "D23N"], "NOTAGENE123": ["A1V"], "HBB": ["p.Glu7Val", "E6"]}}))
    app, missing, hbb = out["proteins"]
    assert [v["status"] for v in app["variants"]][-1] == "ambiguous_match"
    assert app["variants"][0]["best_suggestions"][0] == {**app["variants"][0]["best_suggestions"][0],
                                                         "position": 673, "strength": "strong"}
    assert "error" in missing
    assert hbb["variants"][0] == {"input": "p.Glu7Val", "status": "match",
                                  "model_residue_at_written_position": "E", "position": 7,
                                  "plddt": pytest.approx(96.56)}
    assert hbb["variants"][1]["status"] == "invalid"


def test_check_variants_reports_sequence_update_warning():
    out = payload(call("check_variants", {"variants_by_protein": {"P43251": ["F108V", "A151T", "P371S"]}}))
    (p,) = out["proteins"]
    assert "AF-P43251-4-F1" in p["warnings"][0]
    assert {s["alphafold_model"] for s in p["variants"][0]["best_suggestions"]} == {"AF-P43251-F1", "AF-P43251-4-F1"}


@pytest.mark.parametrize("fmt,expected", [
    ("afdb", "Residues or ranges:  7"),
    ("chimerax", "alphafold fetch AF-P68871-F1-v6"),
    ("pymol", "load https://alphafold.ebi.ac.uk/files/AF-P68871-F1-model_v6.cif, AF_P68871_F1"),
])
def test_export_markers(fmt, expected):
    out = payload(call("export_markers", {"variants_by_protein": {"HBB": ["E6V"]}, "format": fmt}))
    assert out["format"] == fmt and expected in out["content"] and out["how_to_use"]


def test_bad_input_is_a_tool_error():
    assert call("check_variants", {"variants_by_protein": {}}).is_error
    assert call("check_variants", {"variants_by_protein": {"HBB": []}}).is_error
    assert call("export_markers", {"variants_by_protein": {"HBB": ["E6V"]}, "format": "pdf"}).is_error
