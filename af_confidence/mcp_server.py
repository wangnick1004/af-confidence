"""MCP server: lets AI assistants (Claude Desktop, Claude Code, ...) check variant numbering
against AlphaFold DB models before they talk about a residue.

Install and run (needs Python 3.10+, for the official ``mcp`` package)::

    pip install "af-confidence[mcp] @ git+https://github.com/wangnick1004/af-confidence"
    af-confidence-mcp            # speaks MCP over stdio

Settings come from environment variables (set them in the MCP client configuration):
``AF_CONFIDENCE_CACHE`` (cache directory), ``AF_CONFIDENCE_OFFLINE=1`` (cached files only).

Tools:

- ``check_variants`` - check protein-level variants and explain numbering mismatches;
- ``export_markers`` - AlphaFold DB custom annotation tracks, or a ChimeraX / PyMOL script.

Built on the ``mcp`` SDK 2.x (``mcp.server.mcpserver.MCPServer``).
"""
from __future__ import annotations

import os
import sys
from typing import Any, Literal

from . import __version__
from .api import afdb_tracks, best_suggestions, check_list, chimerax_script, pymol_script
from .mapper import ProteinReport
from .sources import HUMAN, Client

SERVER_INSTRUCTIONS = """\
af-confidence checks protein-level variants as written in papers or databases (E6V, p.Glu6Val)
against the sequence of the AlphaFold DB model, and explains numbering mismatches.

Use check_variants BEFORE you locate, describe or discuss a variant position on an AlphaFold DB
or UniProt structure, especially numbers taken from the literature: legacy numbering often skips
the initiator Met, a signal peptide (mature-protein numbering) or uses a fragment's own numbering
(amyloid-beta), so the residue at the written number is often a different amino acid.

- Send all variants from the same source in one call: agreement between variants is the main
  evidence, and it reveals variants that match the model only by coincidence (ambiguous_match).
- Evidence levels: strong = several variants agree, very unlikely by chance; medium = one variant
  fits, right about 9 times in 10; weak = could easily be chance. State medium or weak results as
  likely or possible, never as certain, and suggest checking the source's numbering.
- Read the warnings: the AlphaFold DB model can lag behind a UniProt sequence update.
- pLDDT values are AlphaFold DB's own and are not reinterpreted. This tool does not predict
  whether a variant is pathogenic, and AlphaFold DB models are wild-type structures.
"""

EVIDENCE_LEVELS = ("strong = several variants agree, very unlikely by chance; medium = one variant "
                   "fits, right about 9 times in 10; weak = could easily be chance")

EXPORT_HELP = {
    "afdb": "Open each URL, add a track in the annotations viewer ('Add your annotation track'), "
            "paste the Track name and the Residues or ranges. Tracks stay only in that browser tab.",
    "chimerax": "Save as a .cxc file and open it in ChimeraX (File > Open). It first closes the "
                "current ChimeraX session.",
    "pymol": "Save as a .pml file and run it in PyMOL (File > Run Script...). It first deletes all "
             "loaded objects.",
}


def _client(organism: int) -> Client:
    return Client(os.environ.get("AF_CONFIDENCE_CACHE") or None,
                  offline=os.environ.get("AF_CONFIDENCE_OFFLINE", "") not in ("", "0"),
                  organism=organism)


def _validate(variants_by_protein: dict[str, list[str]]) -> dict[str, list[str]]:
    if not variants_by_protein:
        raise ValueError("give at least one protein with variants, e.g. {\"HBB\": [\"E6V\"]}")
    for protein, variants in variants_by_protein.items():
        if not str(protein).strip():
            raise ValueError("protein names must not be empty")
        if not variants:
            raise ValueError(f"protein {protein!r} has no variants")
    return variants_by_protein


def _suggestion(s) -> dict[str, Any]:
    return {"position": s.position, "kind": s.kind, "strength": s.strength,
            "alphafold_model": s.entry_id, "plddt": s.plddt, "note": s.note}


def _report_dict(rep: ProteinReport) -> dict[str, Any]:
    out: dict[str, Any] = {"protein": rep.query, "uniprot_accession": rep.accession or None}
    if rep.error:
        out["error"] = rep.error
        return out
    out["alphafold_model"] = rep.entry_id
    out["alphafold_url"] = f"https://alphafold.ebi.ac.uk/entry/{rep.entry_id}"
    out["warnings"] = rep.warnings
    variants = []
    for r in rep.results:
        v: dict[str, Any] = {"input": r.input, "status": r.status}
        if r.status == "invalid":
            v["message"] = r.message
            variants.append(v)
            continue
        v["model_residue_at_written_position"] = r.model_residue or None
        if r.status == "match":
            v["position"] = r.variant.position
            v["plddt"] = r.plddt
        else:
            best = best_suggestions(r)
            v["message"] = r.message
            v["best_suggestions"] = [_suggestion(s) for s in best]
            v["other_suggestions"] = [_suggestion(s) for s in r.suggestions if s not in best]
        variants.append(v)
    out["variants"] = variants
    return out


def check_variants(variants_by_protein: dict[str, list[str]], organism: int = HUMAN) -> dict[str, Any]:
    """Check protein variants against the AlphaFold DB model sequence; explain numbering mismatches.

    Args:
        variants_by_protein: protein -> variants, e.g. {"HBB": ["E6V"], "SERPINA1": ["E342K",
            "E264V"]}. A protein is a gene name, UniProt accession or isoform accession
            (P04637-2). Variants are protein-level: E6V, p.E6V, Glu6Val, p.Glu6Val, R213*.
            Put all variants from the same source in one call.
        organism: NCBI taxonomy ID used for gene names (9606 human, 10090 mouse).

    Returns, per protein: the AlphaFold DB model checked, warnings, and per variant its status
    (match, ambiguous_match, mismatch, out_of_range, invalid) with the best suggested positions
    and their evidence strength (strong / medium / weak).
    """
    reports = check_list(_validate(variants_by_protein), client=_client(organism))
    return {"proteins": [_report_dict(r) for r in reports], "evidence_levels": EVIDENCE_LEVELS,
            "note": "pLDDT values are AlphaFold DB's own. This tool does not predict variant effects."}


def export_markers(variants_by_protein: dict[str, list[str]],
                   format: Literal["afdb", "chimerax", "pymol"] = "afdb",
                   organism: int = HUMAN) -> dict[str, Any]:
    """Make files that show the checked positions on the AlphaFold DB models.

    Args:
        variants_by_protein: same as for check_variants.
        format: "afdb" - track names and residue lists to paste into an AlphaFold DB entry page
            (custom annotations); "chimerax" - a .cxc script; "pymol" - a .pml script. The scripts
            load the same AlphaFold DB models that were checked and mark the positions.
        organism: NCBI taxonomy ID used for gene names.

    Only positions with strong or medium evidence (or matches) are marked. Returns the content
    and how to use it; give the content to the user as is.
    """
    renderers = {"afdb": afdb_tracks, "chimerax": chimerax_script, "pymol": pymol_script}
    if format not in renderers:
        raise ValueError('format must be "afdb", "chimerax" or "pymol"')
    reports = check_list(_validate(variants_by_protein), client=_client(organism))
    return {"format": format, "how_to_use": EXPORT_HELP[format], "content": renderers[format](reports)}


def build_server():
    """Create the MCP server (imports the mcp package)."""
    from mcp.server.mcpserver import MCPServer
    from mcp.types import ToolAnnotations

    server = MCPServer("af-confidence", instructions=SERVER_INSTRUCTIONS, version=__version__,
                       website_url="https://github.com/wangnick1004/af-confidence")
    hints = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True,
                            openWorldHint=True)    # reads AlphaFold DB and UniProt
    server.tool(annotations=hints)(check_variants)
    server.tool(annotations=hints)(export_markers)
    return server


def main() -> int:
    if sys.version_info < (3, 10):
        print("af-confidence-mcp needs Python 3.10 or later (the mcp package does). "
              "The command-line tool itself works on Python 3.9.", file=sys.stderr)
        return 1
    try:
        server = build_server()
    except ImportError:
        print('af-confidence-mcp needs the mcp package: pip install "af-confidence[mcp]" '
              "(or pip install mcp)", file=sys.stderr)
        return 1
    server.run()                                   # stdio
    return 0


if __name__ == "__main__":
    sys.exit(main())
