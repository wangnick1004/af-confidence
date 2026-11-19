"""The research scenarios in README.md must show what the tool really prints.

Every ```bash block in the scenarios section that runs `python3 -m af_confidence ...` and is
followed by a ```text block is executed (offline, demo cache); every line shown in the text
block (except '...') must appear in the real output. Commands that write a file (`> file`)
must run and write something. Scenario 5's table is checked against the MCP tool directly.
"""
import re
import shlex
from pathlib import Path

import pytest

from af_confidence import mcp_server
from af_confidence.cli import main

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
README = (ROOT / "README.md").read_text(encoding="utf-8")
SECTION = README[README.index("## 研究情境"):README.index("## 專案目標")]
PAIRS = re.findall(r"```bash\n(python3 -m af_confidence [^\n]+)\n```\s*\n```text\n(.*?)```", SECTION, re.S)
WRITES = re.findall(r"```bash\n(python3 -m af_confidence [^\n]+ > \S+)\n```", SECTION)


def run(command, capsys, monkeypatch):
    monkeypatch.chdir(ROOT)
    args = shlex.split(command)[3:]                     # drop "python3 -m af_confidence"
    code = main(args + ["--cache", str(CACHE), "--offline"])
    return code, capsys.readouterr().out


def test_scenarios_are_found():
    assert len(PAIRS) == 5 and len(WRITES) == 2      # update when scenarios change


@pytest.mark.parametrize("command,shown", PAIRS, ids=[c[25:70] for c, _ in PAIRS])
def test_shown_output_is_real(command, shown, capsys, monkeypatch):
    code, out = run(command, capsys, monkeypatch)
    assert code in (0, 1)
    real = out.splitlines()
    for line in shown.splitlines():
        if line.strip() and line.strip() != "...":
            assert line in real, f"README shows a line the tool does not print:\n{line}"


@pytest.mark.parametrize("command", WRITES)
def test_file_writing_commands_run(command, capsys, monkeypatch, tmp_path):
    cmd, target = command.rsplit(" > ", 1)
    code, out = run(cmd, capsys, monkeypatch)
    assert code in (0, 1) and len(out) > 100


def test_scenario_5_table(monkeypatch):
    monkeypatch.setenv("AF_CONFIDENCE_CACHE", str(CACHE))
    monkeypatch.setenv("AF_CONFIDENCE_OFFLINE", "1")

    def by_input(variants):
        out = mcp_server.check_variants({"APP": variants})
        return {v["input"]: v for v in out["proteins"][0]["variants"]}

    two = by_input(["E22G", "D23N"])
    assert two["E22G"]["best_suggestions"][0]["position"] == 693
    assert two["E22G"]["best_suggestions"][0]["strength"] == "weak"
    assert two["D23N"]["status"] == "match"
    full = by_input(["A2T", "A21G", "E22G", "E22Q", "D23N"])
    assert full["E22G"]["best_suggestions"][0]["strength"] == "strong"
    d23n = full["D23N"]
    assert d23n["status"] == "ambiguous_match"
    assert d23n["message"] in SECTION
    assert (d23n["best_suggestions"][0]["position"], d23n["best_suggestions"][0]["strength"],
            d23n["best_suggestions"][0]["plddt"]) == (694, "medium", 39.81)
