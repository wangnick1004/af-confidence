from pathlib import Path

from af_confidence.cli import main

CACHE = str(Path(__file__).resolve().parent.parent / "data" / "cache")


def test_cli_text(capsys):
    code = main(["P68871", "E6V", "--cache", CACHE, "--offline"])
    out = capsys.readouterr().out
    assert code == 1 and "annotated_offset" in out and "E7V" in out


def test_cli_all_match_exit_zero(capsys):
    assert main(["P04637", "R175H,R248Q", "--cache", CACHE, "--offline"]) == 0


def test_cli_tsv_and_json(capsys):
    main(["P01009", "E342K", "--cache", CACHE, "--offline", "--format", "tsv"])
    assert capsys.readouterr().out.startswith("input\tstatus")
    main(["P01009", "E342K", "--cache", CACHE, "--offline", "--format", "json"])
    assert '"annotated_offset"' in capsys.readouterr().out


def test_cli_missing_offline(capsys):
    assert main(["Q99999", "A1V", "--cache", CACHE, "--offline"]) == 2
