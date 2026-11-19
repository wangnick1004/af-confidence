# af-confidence

把文獻中的突變位置，正確對應到 AFDB 模型上

Map protein-level variants written in the literature (e.g. `E6V`) onto the correct residue of the
AlphaFold DB model, and catch numbering mistakes before anyone interprets a structure.

> Status: Day 1 of 7 — feasibility checks passed, tool not written yet. See `docs/day1_report.md`.

## Why

The same variant is often numbered differently in different sources, and AlphaFold DB will
happily show you the wrong residue without any warning:

| Variant as usually written | AlphaFold DB model residue at that number | Where the residue actually is | Reason |
|---|---|---|---|
| HBB `E6V` (sickle-cell, HbS) | P | E7 | Legacy numbering skips the initiator Met |
| SERPINA1 `E342K` (Z allele) | L | E366 | Mature-protein numbering skips the 24-aa signal peptide |
| TP53 `R175H` | R | R175 | Already canonical |

(Checked on 2026-11-19 against AlphaFold DB v6 models; reproduce with `python3 scripts/day1_demo_cases.py`.)

## Planned scope (v0.1)

Input: a UniProt accession plus one or more protein-level variants (`E6V`, `p.Glu6Val`).

The tool will report, for each variant:
- whether the reference residue matches the AlphaFold DB model sequence;
- if not, likely explanations it can check objectively:
  - a **consistent offset** across the variants (initiator Met, signal peptide, ...);
  - a **neighbouring residue** (off by a few positions);
  - **swapped reference/alternate** residues;
  - a match in one of the **isoform models** AlphaFold DB provides;
- the matched AlphaFold DB model ID and the pLDDT value at that residue (shown as-is, not reinterpreted).

Out of scope for v0.1: DNA/transcript notation (`c.20A>T`), genomic coordinates, pathogenicity
prediction, 3D viewer, PAE analysis.

## What this tool does NOT do

- It does not judge structural confidence beyond showing AlphaFold's own pLDDT.
- It does not predict whether a variant is pathogenic. AlphaFold DB models are wild-type
  structures; the mutation itself is not modelled.
- If you have genomic coordinates or HGVS DNA notation, use a full annotation tool
  (e.g. Ensembl VEP or EBI ProtVar) instead.

## Repository layout

```
data/cache/   AlphaFold DB API responses and model files for the demo proteins (offline demo)
scripts/      Day-1 feasibility checks
docs/         Daily reports with source tables and review checklists
```

## Data and licence

Structure predictions come from the AlphaFold Protein Structure Database (EMBL-EBI / Google DeepMind).
Cite the AlphaFold and AlphaFold DB papers when using the output; check the AlphaFold DB site for the
current data licence terms. Code licence: MIT (to be added).

Parts of the code and documentation were drafted with help from Claude (Anthropic).
