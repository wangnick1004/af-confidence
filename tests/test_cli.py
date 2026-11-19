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
    assert capsys.readouterr().out.startswith("protein\taccession\tinput\tstatus")
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


# ---- multi-protein input ----
from af_confidence.cli import InputError, parse_lines  # noqa: E402


def test_parse_lines_mixed():
    lines = ["# comment", "HBB E6V", "P01009 E342K, E264V  # Z and S", "", "R175H"]
    assert parse_lines(lines, "TP53", "f") == [("HBB", ["E6V"]), ("P01009", ["E342K", "E264V"]),
                                                ("TP53", ["R175H"])]


def test_parse_lines_variant_like_gene_names():
    # C1S is a real gene name that also looks like a variant
    assert parse_lines(["C1S R534H"], None, "f") == [("C1S", ["R534H"])]
    assert parse_lines(["C1S R534H"], "P09871", "f") == [("P09871", ["C1S", "R534H"])]


def test_parse_lines_needs_protein():
    import pytest
    with pytest.raises(InputError, match="line 1: no protein"):
        parse_lines(["E6V"], None, "f")
    with pytest.raises(InputError, match="has no variants"):
        parse_lines(["HBB"], None, "f")


def test_cli_multi_protein_file(tmp_path, capsys):
    f = tmp_path / "list.txt"
    f.write_text("HBB E6V\nP01009 E342K\nSERPINA1 E264V\nTP53 R175H\n")
    code = main(["-f", str(f), "--cache", CACHE, "--offline"])
    out = capsys.readouterr().out
    assert code == 1
    assert "HBB -> P68871" in out and "E7V" in out
    # SERPINA1 given by gene name and by accession is one protein: batch evidence 2/2
    assert out.count("SERPINA1") == 0 or "P01009" in out
    assert "explains 2/2" in out
    assert "OK R175H" in out


def test_cli_gene_name(capsys):
    assert main(["HBB", "p.Glu7Val", "--cache", CACHE, "--offline"]) == 0
    assert "HBB -> P68871" in capsys.readouterr().out


def test_cli_bad_protein_does_not_stop_others(tmp_path, capsys):
    f = tmp_path / "list.txt"
    f.write_text("NOTAGENE123 A1V\nHBB E6V\n")
    code = main(["-f", str(f), "--cache", CACHE, "--offline"])
    out = capsys.readouterr().out
    assert code == 2 and "NOTAGENE123: error" in out and "E7V" in out


def test_cli_protein_only_errors(capsys):
    import pytest
    with pytest.raises(SystemExit):
        main(["HBB", "--cache", CACHE, "--offline"])


def test_cli_isoform_input(capsys):
    # P01009-2 is 359 aa and identical to the canonical sequence up to 355; its N-terminal
    # signal peptide annotation carries over, so the S allele (E264V) still maps to E288V
    assert main(["P01009-2", "E264V", "--cache", CACHE, "--offline"]) == 1
    out = capsys.readouterr().out
    assert "AF-P01009-2-F1" in out and "E288V" in out
