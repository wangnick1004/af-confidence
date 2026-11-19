"""Python interface for notebooks and scripts.

    import af_confidence as afc

    report = afc.check("HBB", ["E6V"])                      # one protein
    reports = afc.check_list({"HBB": ["E6V"],               # several proteins
                              "SERPINA1": ["E342K", "E264V"]})
    reports = afc.check_list("my_variants.txt")             # or a list file

    print(afc.to_text(reports))   # the command-line report
    afc.to_records(reports)        # one dict per input variant (no extra packages)
    afc.to_dataframe(reports)      # the same as a pandas DataFrame (needs pandas)
    print(afc.afdb_tracks(reports))                         # paste into AlphaFold DB
    open("markers.cxc", "w").write(afc.chimerax_script(reports))   # open in ChimeraX

Every function takes the same optional settings as the command line: ``cache`` (directory),
``offline`` (cached files only) and ``organism`` (NCBI taxonomy ID for gene names), or a
ready ``client``. Data problems (unknown gene, no AlphaFold DB model) do not raise: they are
reported in ``ProteinReport.error``. Bad input (a list line without a protein) raises
``InputError``.
"""
from __future__ import annotations

import os
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, Union

from .afdb_tracks import render_afdb
from .chimerax import render_chimerax
from .inputs import group, parse_lines
from .mapper import ProteinReport, Result, Suggestion, check_protein
from .sources import HUMAN, Client

Variants = Union[str, Iterable[str]]
ListInput = Union[str, os.PathLike, Mapping[str, Variants], Iterable[tuple]]

STRENGTH_RANK = {"strong": 0, "medium": 1, "weak": 2}


def _client(client: Client | None, cache, offline: bool, organism: int) -> Client:
    return client or Client(cache, offline=offline, organism=organism)


def _variants(v: Variants) -> list[str]:
    if isinstance(v, str):
        v = [v]
    return [t for item in v for t in str(item).replace(",", " ").split() if t]


def check(protein: str, variants: Variants, *, cache=None, offline: bool = False,
          organism: int = HUMAN, client: Client | None = None) -> ProteinReport:
    """Check variants of one protein (gene name, UniProt accession or isoform accession).

    ``variants`` is a list such as ``["E6V", "p.Glu7Val"]`` or one string (``"E342K, E264V"``).
    """
    return check_protein(protein, _variants(variants), _client(client, cache, offline, organism))


def check_list(items: ListInput, *, protein: str | None = None, cache=None, offline: bool = False,
               organism: int = HUMAN, client: Client | None = None) -> list[ProteinReport]:
    """Check a whole list, merging entries for the same protein so batch evidence is used.

    ``items`` can be:

    - a path to a list file (``[PROTEIN] VARIANT ...`` lines, ``#`` comments), as for ``-f``;
    - a mapping ``{"HBB": ["E6V"], "P01009": "E342K, E264V"}``;
    - pairs ``[("HBB", ["E6V"]), ("APP", "A2T")]``.

    ``protein`` is used for file lines that have variants only (like ``af-confidence APP -f``).
    """
    c = _client(client, cache, offline, organism)
    if isinstance(items, (str, os.PathLike)):
        path = Path(items)
        with open(path, encoding="utf-8") as fh:
            pairs = parse_lines(fh, protein, str(path))
    elif isinstance(items, Mapping):
        pairs = [(p, _variants(v)) for p, v in items.items()]
    else:
        pairs = [(p, _variants(v)) for p, v in items]
    return [check_protein(p, vs, c) for p, vs in group(pairs, c)]


def _as_list(reports: ProteinReport | Iterable[ProteinReport]) -> list[ProteinReport]:
    return [reports] if isinstance(reports, ProteinReport) else list(reports)


def best_suggestions(result: Result) -> list[Suggestion]:
    """The suggestions of the highest strength present (e.g. all strong ones), or []."""
    if not result.suggestions:
        return []
    top = min(STRENGTH_RANK[s.strength] for s in result.suggestions)
    return [s for s in result.suggestions if STRENGTH_RANK[s.strength] == top]


def to_records(reports: ProteinReport | Iterable[ProteinReport],
               detail: str = "variant") -> list[dict[str, Any]]:
    """Flatten reports into plain dicts.

    ``detail="variant"`` (default): one row per input variant, with the best suggestion:
    ``protein, accession, input, status, entry_id, model_residue, plddt, best_position,
    best_kind, best_strength, best_entry_id, best_plddt, n_suggestions, message``.
    For a match, ``best_position`` is the position as written. Proteins that could not be
    loaded give one row with ``status="error"``.

    ``detail="suggestion"``: one row per suggestion (like ``--format tsv``).
    """
    if detail not in ("variant", "suggestion"):
        raise ValueError('detail must be "variant" or "suggestion"')
    rows: list[dict[str, Any]] = []
    for rep in _as_list(reports):
        base = {"protein": rep.query, "accession": rep.accession}
        if rep.error:
            rows.append({**base, "input": None, "status": "error", "message": rep.error})
            continue
        for r in rep.results:
            row = {**base, "input": r.input, "status": r.status, "entry_id": r.entry_id or None,
                   "model_residue": r.model_residue or None, "plddt": r.plddt}
            if detail == "suggestion":
                for s in r.suggestions or [None]:
                    rows.append({**row,
                                 "suggestion_kind": s.kind if s else None,
                                 "strength": s.strength if s else None,
                                 "suggested_position": s.position if s else None,
                                 "suggestion_entry_id": s.entry_id if s else None,
                                 "suggestion_plddt": s.plddt if s else None,
                                 "note": s.note if s else r.message or None})
                continue
            best = best_suggestions(r)
            b = best[0] if best else None
            if r.status == "match":
                row.update(best_position=r.variant.position, best_kind="as_written", best_strength=None,
                           best_entry_id=r.entry_id, best_plddt=r.plddt)
            else:
                row.update(best_position=b.position if b else None, best_kind=b.kind if b else None,
                           best_strength=b.strength if b else None, best_entry_id=b.entry_id if b else None,
                           best_plddt=b.plddt if b else None)
            row.update(n_suggestions=len(r.suggestions), message=r.message or None)
            rows.append(row)
    return rows


def to_dataframe(reports: ProteinReport | Iterable[ProteinReport], detail: str = "variant"):
    """``to_records`` as a pandas DataFrame (requires pandas: ``pip install pandas``)."""
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("to_dataframe needs pandas: pip install pandas "
                          "(or use to_records, which needs nothing extra)") from None
    return pd.DataFrame(to_records(reports, detail=detail))


def to_text(reports: ProteinReport | Iterable[ProteinReport]) -> str:
    """The same human-readable report the command line prints (``--format text``)."""
    from .cli import render_text          # imported here: cli is the command-line front end
    return render_text(_as_list(reports))


def afdb_tracks(reports: ProteinReport | Iterable[ProteinReport]) -> str:
    """Text with AlphaFold DB custom annotation tracks (same as ``--format afdb``)."""
    return render_afdb(_as_list(reports))


def chimerax_script(reports: ProteinReport | Iterable[ProteinReport]) -> str:
    """A ChimeraX command script (same as ``--format chimerax``); save it as ``.cxc``."""
    return render_chimerax(_as_list(reports))
