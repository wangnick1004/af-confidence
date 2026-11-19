"""Parse protein-level variant notation such as ``E6V`` or ``p.Glu6Val``."""
from __future__ import annotations

import re
from dataclasses import dataclass

THREE_TO_ONE = {
    "Ala": "A", "Arg": "R", "Asn": "N", "Asp": "D", "Cys": "C", "Gln": "Q", "Glu": "E",
    "Gly": "G", "His": "H", "Ile": "I", "Leu": "L", "Lys": "K", "Met": "M", "Phe": "F",
    "Pro": "P", "Ser": "S", "Thr": "T", "Trp": "W", "Tyr": "Y", "Val": "V",
    "Sec": "U", "Ter": "*",
}
ONE_LETTER = set("ACDEFGHIKLMNPQRSTVWYU")

_ONE = re.compile(r"^([A-Z])(\d+)([A-Z*])$")
_THREE = re.compile(r"^([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2}|\*)$")


class VariantParseError(ValueError):
    """Raised when a variant string is not in a supported notation."""


@dataclass(frozen=True)
class Variant:
    raw: str
    ref: str
    position: int
    alt: str

    def __str__(self) -> str:
        return f"{self.ref}{self.position}{self.alt}"


def parse_variant(text: str) -> Variant:
    """Parse ``E6V``, ``p.E6V``, ``Glu6Val``, ``p.Glu6Val`` or ``p.(Glu6Val)``.

    Only missense/nonsense substitutions are supported; deletions, insertions,
    frameshifts and DNA notation (``c.20A>T``) raise VariantParseError.
    """
    raw = text
    s = text.strip()
    if s.startswith("p."):
        s = s[2:]
    if s.startswith("(") and s.endswith(")"):
        s = s[1:-1]
    m = _ONE.match(s)
    if m:
        ref, pos, alt = m.group(1), int(m.group(2)), m.group(3)
        if ref not in ONE_LETTER or (alt != "*" and alt not in ONE_LETTER):
            raise VariantParseError(f"{raw!r}: unknown amino-acid letter")
    else:
        m = _THREE.match(s)
        if not m:
            raise VariantParseError(
                f"{raw!r}: unsupported notation (use e.g. E6V or p.Glu6Val)")
        try:
            ref, alt = THREE_TO_ONE[m.group(1)], THREE_TO_ONE.get(m.group(3), m.group(3))
        except KeyError:
            raise VariantParseError(f"{raw!r}: unknown amino-acid code") from None
        if alt not in ONE_LETTER and alt != "*":
            raise VariantParseError(f"{raw!r}: unknown amino-acid code")
        pos = int(m.group(2))
    if pos < 1:
        raise VariantParseError(f"{raw!r}: position must be >= 1")
    return Variant(raw=raw, ref=ref, position=pos, alt=alt)
