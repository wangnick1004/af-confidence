"""Turn results into AlphaFold DB custom annotation tracks.

Since November 2025 (AFDB v8.2.1) an AlphaFold DB entry page can show user-defined tracks:
in the annotations viewer, the dialog "Add your annotation track" takes a *Track name* and
*Residues or ranges* such as ``1, 56, 24-52, 367-458``. Tracks are typed in by hand (no file
upload) and live only in the browser tab. This module produces exactly those two strings,
with positions already corrected to the model's numbering, so they can be pasted in.

Only confident positions are placed: matches, and strong or medium suggestions. Variants with
only weak evidence (or none) are listed as not placed, with the reason.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .mapper import ProteinReport

AFDB_ENTRY_URL = "https://alphafold.ebi.ac.uk/entry/{entry}"

# Track names are kept to 14 characters: the AFDB viewer truncates names of 15 or more.
TRACK_OK = "OK as written"
TRACK_STRONG = "Fixed strong"
TRACK_MEDIUM = "Fixed medium"
TRACK_AMBIGUOUS = "Ambiguous"
TRACK_ORDER = (TRACK_OK, TRACK_STRONG, TRACK_MEDIUM, TRACK_AMBIGUOUS)

# The validation AlphaFold DB applies to the "Residues or ranges" field.
AFDB_RESIDUES_RE = re.compile(r"^(\d+(-\d+)?)(\s*,\s*(\d+(-\d+)?))*$")


@dataclass
class EntryTracks:
    entry_id: str
    accession: str
    url: str
    length: int
    tracks: dict[str, list[int]] = field(default_factory=dict)        # track -> residues
    notes: list[str] = field(default_factory=list)                    # "E6V -> 7 (...)"
    start: int = 1                                                    # model numbering offset
    version: int = 0                                                  # AlphaFold DB version
    labels: dict[int, list[str]] = field(default_factory=dict)        # residue -> variants

    def model_number(self, residue: int) -> int:
        """Residue number as written in the model file (what ChimeraX or PyMOL use)."""
        return residue + self.start - 1

    def residues(self, track: str) -> str:
        return format_residues(self.tracks[track])


@dataclass
class ProteinTracks:
    query: str
    accession: str
    entries: list[EntryTracks] = field(default_factory=list)
    not_placed: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    error: str = ""


def format_residues(positions: list[int]) -> str:
    """Sorted, de-duplicated positions with consecutive runs collapsed: ``7, 288-290``."""
    out: list[str] = []
    ps = sorted(set(positions))
    i = 0
    while i < len(ps):
        j = i
        while j + 1 < len(ps) and ps[j + 1] == ps[j] + 1:
            j += 1
        out.append(str(ps[i]) if i == j else f"{ps[i]}-{ps[j]}")
        i = j + 1
    return ", ".join(out)


def build_tracks(rep: ProteinReport) -> ProteinTracks:
    pt = ProteinTracks(rep.query, rep.accession, warnings=list(rep.warnings), error=rep.error)
    if rep.error:
        return pt
    entries: dict[str, EntryTracks] = {}

    def place(entry_id: str, track: str, position: int, note: str | None, label: str = "") -> bool:
        start, length, acc = rep.models.get(entry_id, (1, 0, ""))
        residue = position - start + 1            # AFDB counts residues of the model from 1
        if not 1 <= residue <= length:
            return False
        e = entries.get(entry_id)
        if e is None:
            e = entries[entry_id] = EntryTracks(entry_id, acc, AFDB_ENTRY_URL.format(entry=entry_id),
                                                length, start=start,
                                                version=rep.versions.get(entry_id, 0))
        e.tracks.setdefault(track, []).append(residue)
        if label and label not in e.labels.setdefault(residue, []):
            e.labels[residue].append(label)
        if note:
            e.notes.append(note)
        return True

    for r in rep.results:
        if r.status == "invalid":
            pt.not_placed.append(f"{r.input}: not a supported variant notation")
            continue
        if r.status == "match":
            place(r.entry_id, TRACK_OK, r.variant.position, f"{r.input} -> {r.variant.position} (as written)",
                  r.input)
            continue
        if r.status == "ambiguous_match":
            others = " or ".join(str(s.position) for s in r.suggestions)
            place(r.entry_id, TRACK_AMBIGUOUS, r.variant.position,
                  f"{r.input} -> {r.variant.position} as written, or {others} (ambiguous_match)",
                  f"{r.input}?")
            for s in r.suggestions:
                place(s.entry_id, TRACK_AMBIGUOUS, s.position, None, f"{r.input}?")
            continue
        # mismatch or out of range: place the best suggestions only
        strong = [s for s in r.suggestions if s.strength == "strong"]
        best = strong or [s for s in r.suggestions if s.strength == "medium"]
        track = TRACK_STRONG if strong else TRACK_MEDIUM
        placed = [place(s.entry_id, track, s.position, f"{r.input} -> {s.position} ({s.kind}, {s.strength})",
                        r.input)
                  for s in best]
        if not any(placed):
            why = ("only weak suggestions" if r.suggestions else "no explanation found")
            pt.not_placed.append(f"{r.input}: {r.message}; {why}")

    order = [rep.entry_id] + sorted(k for k in entries if k != rep.entry_id)
    pt.entries = [entries[k] for k in order if k in entries]
    return pt


def render_afdb(reports: list[ProteinReport]) -> str:
    lines = [
        "AlphaFold DB custom annotations",
        "Open each entry page below, go to the annotations viewer and open the dialog",
        "\"Add your annotation track\". Copy the Track name and the Residues or ranges, then",
        "click \"Add track\". Repeat for each track. AlphaFold DB keeps tracks only in that",
        "browser tab. Positions are already converted to the numbering of that model.",
    ]
    for rep in reports:
        pt = build_tracks(rep)
        lines.append("")
        name = pt.query if not pt.accession or pt.query.upper() == pt.accession else f"{pt.query} -> {pt.accession}"
        if pt.error:
            lines.append(f"== {name}: error: {pt.error}")
            continue
        for w in pt.warnings:
            lines.append(f"   warning: {w}")
        for e in pt.entries:
            lines.append(f"== {name}  {e.url}")
            for track in TRACK_ORDER:
                if track in e.tracks:
                    lines.append(f"   Track name:          {track}")
                    lines.append(f"   Residues or ranges:  {e.residues(track)}")
            lines.append("   from:")
            lines.extend(f"     {n}" for n in e.notes)
        if not pt.entries:
            lines.append(f"== {name}: nothing to place")
        for n in pt.not_placed:
            lines.append(f"   not placed: {n}")
    return "\n".join(lines).rstrip() + "\n"
