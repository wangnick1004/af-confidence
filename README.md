# af-confidence

把文獻中的突變位置，正確對應到 AFDB 模型上

Map protein-level variants written in the literature (e.g. `E6V`) onto the correct residue of the
AlphaFold DB model, and catch numbering mistakes before anyone interprets a structure.

> Status: Day 2 of 7 — v0.1 works on the command line; 34 offline tests pass. See `docs/`.

## Why

The same variant is often numbered differently in different sources, and AlphaFold DB will
happily show you the wrong residue without any warning:

| Variant as usually written | AlphaFold DB model residue at that number | Where the residue actually is | Reason |
|---|---|---|---|
| HBB `E6V` (sickle-cell, HbS) | P | E7 | Legacy numbering skips the initiator Met |
| SERPINA1 `E342K` (Z allele) | L | E366 | Mature-protein numbering skips the 24-aa signal peptide |
| TP53 `R175H` | R | R175 | Already canonical |

(Checked on 2026-11-19 against AlphaFold DB v6 models; reproduce with `python3 scripts/day1_demo_cases.py`.)

## Install and run

Requires Python 3.9+; no third-party packages. On macOS and most Linux systems the command is
`python3` (not `python`); on Windows it is usually `py`.

```bash
git clone https://github.com/wangnick1004/af-confidence
cd af-confidence
python3 -m pip install .
af-confidence P68871 E6V
```

Without installing: `python3 -m af_confidence P68871 E6V`.

Example output:

```
P68871  (AlphaFold DB model AF-P68871-F1)
XX E6V: model has P at 6, not E
     -> [annotated_offset] +1: E7V matches; UniProt annotates initiator Met removed, so E6V is probably numbered without it [pLDDT 96.56]
```

Options: `--format text|tsv|json`, `--cache DIR`, `--offline` (cached files only).
The demo proteins are cached in `data/cache`, so `--cache data/cache --offline` works with no network.
Exit code: 0 if every variant matches, 1 if any does not, 2 on a data/network error.

Run the tests: `python3 -m pip install pytest && python3 -m pytest`.

## Scope (v0.1)

Input: a UniProt accession plus one or more protein-level variants (`E6V`, `p.Glu6Val`).

For each variant the tool reports:
- whether the reference residue matches the AlphaFold DB model sequence;
- if not, likely explanations it can check objectively:
  - **annotated offset**: shifting by a UniProt-annotated processing feature (removed initiator
    Met, signal peptide, propeptide, transit peptide) gives a match;
  - **consistent offset**: one shift makes *all* mismatched variants match, and the chance of that
    happening at random (from the protein's amino-acid composition) is below 0.05. Never
    reported for a single variant;
  - **isoform**: the residue matches in one of the isoform models AlphaFold DB provides;
  - **swapped**: the model already has the alternate residue;
  - **nearby**: the residue is within ±3 positions. Weak evidence, shown only when nothing
    stronger explains the mismatch;
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
af_confidence/  The tool (variant parser, data sources, mapper, CLI)
tests/          Offline tests against data/cache
data/cache/     AlphaFold DB and UniProt responses for the demo proteins (offline demo and tests)
scripts/        Day-1 feasibility checks
docs/           Daily reports with source tables and review checklists
```

## Data and licence

Structure predictions come from the AlphaFold Protein Structure Database (EMBL-EBI / Google DeepMind).
AlphaFold DB data are available under CC-BY-4.0; cite the AlphaFold and AlphaFold DB papers when
using the output. Processing-feature annotations come from UniProt. Code licence: MIT (see `LICENSE`).

Parts of the code and documentation were drafted with help from Claude (Anthropic).
