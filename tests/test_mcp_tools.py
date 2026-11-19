"""The MCP tools as plain functions (no mcp package needed, runs on Python 3.9 too)."""
import sys
from pathlib import Path

import pytest

from af_confidence import mcp_server

CACHE = Path(__file__).resolve().parent.parent / "data" / "cache"


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    monkeypatch.setenv("AF_CONFIDENCE_CACHE", str(CACHE))
    monkeypatch.setenv("AF_CONFIDENCE_OFFLINE", "1")


def test_check_variants_structure():
    out = mcp_server.check_variants({"SERPINA1": ["E342K", "E264V"], "TP53": ["R72P", "F20L"]})
    serpina1, tp53 = out["proteins"]
    assert [v["best_suggestions"][0]["position"] for v in serpina1["variants"]] == [366, 288]
    r72p, f20l = tp53["variants"]
    assert r72p["best_suggestions"][0]["kind"] == "swapped"
    assert f20l["best_suggestions"][0]["strength"] == "weak" and f20l["other_suggestions"] == []


def test_offline_setting_from_environment(monkeypatch):
    assert mcp_server._client(9606).offline is True
    monkeypatch.setenv("AF_CONFIDENCE_OFFLINE", "0")
    assert mcp_server._client(9606).offline is False


@pytest.mark.parametrize("bad", [{}, {"HBB": []}, {" ": ["E6V"]}])
def test_invalid_input(bad):
    with pytest.raises(ValueError):
        mcp_server.check_variants(bad)


def test_export_formats():
    for fmt in ("afdb", "chimerax", "pymol"):
        out = mcp_server.export_markers({"HBB": ["E6V"]}, fmt)
        assert out["content"] and out["how_to_use"] == mcp_server.EXPORT_HELP[fmt]
    with pytest.raises(ValueError):
        mcp_server.export_markers({"HBB": ["E6V"]}, "pdf")


def test_main_explains_missing_requirements(monkeypatch, capsys):
    monkeypatch.setattr(sys, "version_info", (3, 9, 0))
    assert mcp_server.main() == 1 and "Python 3.10" in capsys.readouterr().err
    monkeypatch.setattr(sys, "version_info", (3, 12, 0))
    monkeypatch.setitem(sys.modules, "mcp", None)
    monkeypatch.setitem(sys.modules, "mcp.server.mcpserver", None)
    assert mcp_server.main() == 1 and "pip install" in capsys.readouterr().err


def test_errors_and_invalid_variants_in_results():
    out = mcp_server.check_variants({"NOTAGENE123": ["A1V"], "HBB": ["E6", "E6V"]})
    missing, hbb = out["proteins"]
    assert "error" in missing and "variants" not in missing
    assert hbb["variants"][0] == {"input": "E6", "status": "invalid",
                                  "message": "'E6': unsupported notation (use e.g. E6V or p.Glu6Val)"}


def test_build_server_registers_read_only_tools():
    pytest.importorskip("mcp")
    import anyio
    server = mcp_server.build_server()
    tools = anyio.run(server.list_tools)
    assert {t.name for t in tools} == {"check_variants", "export_markers"}
    assert all(t.annotations.read_only_hint for t in tools)
