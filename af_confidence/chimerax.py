"""Write a ChimeraX command script (.cxc) that opens the right AlphaFold DB models and marks
the checked positions.

Run the output in ChimeraX with ``open file.cxc``. The script:

- closes the current ChimeraX session first, so that model numbers start at #1;
- fetches each model with its exact AlphaFold DB identifier and version
  (``alphafold fetch AF-P68871-F1-v6``), i.e. the same model the positions were checked
  against; the cartoon is colored by pLDDT (ChimeraX default for fetched models);
- for each track, shows the side chains, colors them (atoms only, so the pLDDT cartoon
  coloring stays), labels them with the variants as written, and defines a named target
  (``name afc_m1_fixed_strong ...``) that appears under Select > User-Defined Selectors;
- tiles several models side by side and fits the view.

Commands and options follow the ChimeraX User Guide (alphafold, name, show, color with
``target a``, label with ``residues text``, tile, view, close session; comment lines start
with ``#``). Positions come from the same tracks as ``--format afdb``.
"""
from __future__ import annotations

import re

from . import __version__
from .afdb_tracks import (TRACK_AMBIGUOUS, TRACK_MEDIUM, TRACK_OK, TRACK_ORDER, TRACK_STRONG,
                          build_tracks)
from .mapper import ProteinReport

TRACK_COLOR = {TRACK_OK: "lime", TRACK_STRONG: "magenta", TRACK_MEDIUM: "violet",
               TRACK_AMBIGUOUS: "white"}
TRACK_KEY = {TRACK_OK: "ok", TRACK_STRONG: "fixed_strong", TRACK_MEDIUM: "fixed_medium",
             TRACK_AMBIGUOUS: "ambiguous"}
CHAIN = "A"          # AlphaFold DB monomer models have a single chain A


def residue_spec(model: int, residues: list[int]) -> str:
    """``#1/A:7,288-290`` (no spaces: ChimeraX does not allow a space next to a hyphen)."""
    ps = sorted(set(residues))
    parts, i = [], 0
    while i < len(ps):
        j = i
        while j + 1 < len(ps) and ps[j + 1] == ps[j] + 1:
            j += 1
        parts.append(str(ps[i]) if i == j else f"{ps[i]}-{ps[j]}")
        i = j + 1
    return f"#{model}/{CHAIN}:{','.join(parts)}"


def _quote(text: str) -> str:
    return '"' + re.sub(r'["\\]', "", text) + '"'


def render_chimerax(reports: list[ProteinReport]) -> str:
    L = [
        f"# ChimeraX command script written by af-confidence {__version__}",
        "# Run it in ChimeraX with:  open /path/to/this_file.cxc",
        "# NOTE: it starts with 'close session', which closes everything open in ChimeraX.",
        "# Cartoon: AlphaFold pLDDT colors. Side chains of checked positions:",
        "#   lime = OK as written, magenta = Fixed strong, violet = Fixed medium,",
        "#   white = Ambiguous (labels end with '?'). Labels show the variants as written.",
        "# Named selections (Select > User-Defined Selectors): afc_m<model>_<track>.",
        "close session",
    ]
    model = 0
    for rep in reports:
        pt = build_tracks(rep)
        name = pt.query if not pt.accession or pt.query.upper() == pt.accession else f"{pt.query} -> {pt.accession}"
        L.append("#")
        if pt.error:
            L.append(f"# {name}: error: {pt.error}")
            continue
        for w in pt.warnings:
            L.append(f"# warning: {w}")
        for e in pt.entries:
            model += 1
            fetch_id = f"{e.entry_id}-v{e.version}" if e.version else e.entry_id
            L.append(f"# Model #{model}: {name}, {e.entry_id}  {e.url}")
            L.append(f"alphafold fetch {fetch_id}")
            for n in e.notes:
                L.append(f"#   {n}")
            for track in TRACK_ORDER:
                if track not in e.tracks:
                    continue
                spec = residue_spec(model, [e.model_number(r) for r in e.tracks[track]])
                L.append(f"name afc_m{model}_{TRACK_KEY[track]} {spec}")
                L.append(f"show {spec} atoms")
                L.append(f"color {spec} {TRACK_COLOR[track]} target a")
            for residue, variants in sorted(e.labels.items()):
                spec = residue_spec(model, [e.model_number(residue)])
                L.append(f"label {spec} residues text {_quote('/'.join(variants))}")
        if not pt.entries:
            L.append(f"# {name}: nothing to mark")
        for n in pt.not_placed:
            L.append(f"# not placed: {n}")
    L.append("#")
    if model > 1:
        L.append("tile")
    if model:
        L.append("view")
    return "\n".join(L) + "\n"
