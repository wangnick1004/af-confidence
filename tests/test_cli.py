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


EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_cli_file_input(capsys):
    code = main(["P05067", "-f", str(EXAMPLES / "app_abeta_numbering.txt"), "--cache", CACHE, "--offline"])
    out = capsys.readouterr().out
    assert code == 1 and out.count("+671") >= 5 and "!? D23N" in out


def test_cli_requires_variants(capsys):
    import pytest
    with pytest.raises(SystemExit):
        main(["P05067", "--cache", CACHE, "--offline"])


def test_cli_missing_file(capsys):
    assert main(["P05067", "-f", "no_such_file.txt", "--cache", CACHE, "--offline"]) == 2
