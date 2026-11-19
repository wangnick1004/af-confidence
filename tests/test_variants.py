import pytest

from af_confidence.variants import Variant, VariantParseError, parse_variant


@pytest.mark.parametrize("text", ["E6V", "p.E6V", "Glu6Val", "p.Glu6Val", "p.(Glu6Val)", " E6V "])
def test_equivalent_notations(text):
    v = parse_variant(text)
    assert (v.ref, v.position, v.alt) == ("E", 6, "V")


def test_nonsense():
    assert parse_variant("R213*").alt == "*"
    assert parse_variant("p.Arg213Ter").alt == "*"


@pytest.mark.parametrize("text", ["c.20A>T", "E6", "6V", "E0V", "Xyz6Val", "B6V", "E6del", "", "p.Glu6_Lys7del"])
def test_rejected(text):
    with pytest.raises(VariantParseError):
        parse_variant(text)


def test_str():
    assert str(Variant("p.Glu6Val", "E", 6, "V")) == "E6V"
