"""Write a PyMOL script (.pml) that loads the right AlphaFold DB models and marks the checked
positions.

Run the output in PyMOL with ``File > Run Script...`` or ``@file.pml``. The script:

- deletes all objects first (``delete all``), so object names do not clash;
- loads each model from the exact mmCIF URL given by the AlphaFold DB API (the model the
  positions were checked against). PyMOL's ``fetch`` does not know AlphaFold DB identifiers;
- colors the cartoon by pLDDT (stored in the B-factor column) with the AlphaFold DB scheme:
  very high > 90, high 70-90, low 50-70, very low < 50;
- for each track, defines a named selection ``afc_m<model>_<track>``, shows side chains as
  sticks with small spheres (visible in the full view) and colors them (side-chain atoms only, so the cartoon keeps its pLDDT colors), and
  labels the C-alpha atoms with the variants as written;
- shows several models in grid mode and orients the view.

Tested with open-source PyMOL 3.2 (see scripts/check_pymol.py). Positions come from the same
tracks as ``--format afdb``.
"""
from __future__ import annotations

import re

from . import __version__
from .afdb_tracks import (TRACK_AMBIGUOUS, TRACK_MEDIUM, TRACK_OK, TRACK_ORDER, TRACK_STRONG,
                          build_tracks)
from .chimerax import TRACK_KEY
from .mapper import ProteinReport

# AlphaFold DB pLDDT colors (RGB 0-255), lowest band first
PLDDT_COLORS = [("afc_plddt_vlow", (255, 125, 69), None), ("afc_plddt_low", (255, 219, 19), 50),
                ("afc_plddt_high", (101, 203, 243), 70), ("afc_plddt_vhigh", (0, 83, 214), 90)]
TRACK_COLOR = {TRACK_OK: "green", TRACK_STRONG: "magenta", TRACK_MEDIUM: "violet",
               TRACK_AMBIGUOUS: "white"}
CHAIN = "A"
BACKBONE = "name N+C+O+CA"


def object_name(entry_id: str) -> str:
    """PyMOL object name: AF-P43251-4-F1 -> AF_P43251_4_F1."""
    return re.sub(r"[^A-Za-z0-9_]", "_", entry_id)


def resi_list(residues: list[int]) -> str:
    """PyMOL residue list: ``288+366``, ranges as ``692-693``."""
    ps = sorted(set(residues))
    parts, i = [], 0
    while i < len(ps):
        j = i
        while j + 1 < len(ps) and ps[j + 1] == ps[j] + 1:
            j += 1
        parts.append(str(ps[i]) if i == j else f"{ps[i]}-{ps[j]}")
        i = j + 1
    return "+".join(parts)


def _quote(text: str) -> str:
    return '"' + re.sub(r'["\\]', "", text) + '"'


def render_pymol(reports: list[ProteinReport]) -> str:
    L = [
        f"# PyMOL script written by af-confidence {__version__}",
        "# Run it in PyMOL with File > Run Script..., or type:  @/path/to/this_file.pml",
        "# NOTE: it starts with 'delete all', which removes all objects loaded in PyMOL.",
        "# Cartoon: AlphaFold DB pLDDT colors (dark blue > 90, light blue 70-90, yellow 50-70,",
        "#   orange < 50). Side chains of checked positions: green = OK as written,",
        "#   magenta = Fixed strong, violet = Fixed medium, white = Ambiguous (labels end with '?').",
        "# Named selections: afc_m<model>_<track>.",
        "delete all",
    ]
    for name, rgb, _ in PLDDT_COLORS:
        L.append(f"set_color {name}, [{rgb[0]}, {rgb[1]}, {rgb[2]}]")
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
            if not e.cif_url:
                L.append(f"# {e.entry_id}: no model file URL from AlphaFold DB; skipped")
                continue
            model += 1
            obj = object_name(e.entry_id)
            L.append(f"# Model {model}: {name}, {e.entry_id}  {e.url}")
            L.append(f"load {e.cif_url}, {obj}")
            L.append(f"hide everything, {obj}")
            L.append(f"show cartoon, {obj}")
            for cname, _, low in PLDDT_COLORS:
                L.append(f"color {cname}, {obj}" + (f" and b > {low}" if low is not None else ""))
            for n in e.notes:
                L.append(f"#   {n}")
            for track in TRACK_ORDER:
                if track not in e.tracks:
                    continue
                sel = f"afc_m{model}_{TRACK_KEY[track]}"
                resi = resi_list([e.model_number(r) for r in e.tracks[track]])
                L.append(f"select {sel}, {obj} and chain {CHAIN} and resi {resi}")
                L.append(f"show sticks, {sel} and not name N+C+O")
                L.append(f"show spheres, {sel} and not {BACKBONE}")
                L.append(f"set sphere_scale, 0.6, {sel}")
                L.append(f"color {TRACK_COLOR[track]}, {sel} and not {BACKBONE}")
            for residue, variants in sorted(e.labels.items()):
                L.append(f"label {obj} and chain {CHAIN} and resi {e.model_number(residue)} and name CA, "
                         f"{_quote('/'.join(variants))}")
        if not pt.entries:
            L.append(f"# {name}: nothing to mark")
        for n in pt.not_placed:
            L.append(f"# not placed: {n}")
    L.append("#")
    if model:
        L.append("deselect")
        L.append(f"set grid_mode, {1 if model > 1 else 0}")
        L.append("orient")
    return "\n".join(L) + "\n"
