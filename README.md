# af-confidence

把文獻中的突變位置，正確對應到 AFDB 模型上

Map protein-level variants written in the literature (e.g. `E6V`) onto the correct residue of the
AlphaFold DB model, and explain numbering mismatches with evidence before anyone interprets a
structure.

> Status: Day 3 of 7 — v0.1 works on the command line; 44 offline tests pass on Python 3.9–3.13.
> Daily reports with sources and review checklists are in `docs/`.

## Why

The same variant is often numbered differently in different sources:

| Variant as usually written | AlphaFold DB model residue at that number | Actual position | Reason (UniProt annotation) |
|---|---|---|---|
| HBB `E6V` (sickle-cell, HbS) | P | E7 | initiator Met removed |
| SERPINA1 `E342K` (Z allele) | L | E366 | signal peptide 1–24 |
| APP `E22G` (Arctic, amyloid-beta numbering) | T | E693 | amyloid-beta starts at 672 |
| APP `D23N` (Iowa, amyloid-beta numbering) | **D (matches by coincidence)** | D694 | amyloid-beta starts at 672 |

AlphaFold DB itself shows whatever residue sits at the number you look up. Full annotation tools
do check the reference residue: for `P68871 E6V`, EBI ProtVar (UI 2.0, checked 2026-11-19) warns that
Glu does not match Pro at position 6, then **continues with Pro6** and does not point to Glu7
(screenshot: `docs/images/protvar_P68871_E6V.webp`). And when the residue matches by coincidence,
as for `D23N`, no single-variant check can notice.

This tool adds the missing step: *why* it does not match and *where* the residue probably is,
with an explicit strength of evidence.

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

```
P68871  (AlphaFold DB model AF-P68871-F1)
XX E6V: model has P at 6, not E
     -> [strong] annotated_offset: +1: E7V matches; UniProt: initiator Met removed; mature chain
        'Hemoglobin subunit beta' starts at 2, so E6V may use numbering that starts there
        (explains 1/1 mismatched input) [pLDDT 96.56]
```

A list of variants from a paper or a review, one or more per line, `#` for comments:

```bash
af-confidence P05067 -f examples/app_abeta_numbering.txt
```

Options: `-f/--file FILE`, `--format text|tsv|json`, `--cache DIR`, `--offline` (cached files only).
The demo proteins are cached in `data/cache`, so `--cache data/cache --offline` works without network.
Exit code: 0 if every variant matches unambiguously, 1 otherwise, 2 on a data/network error.

Run the tests: `python3 -m pip install pytest && python3 -m pytest`.

## What it checks

Status per variant: `OK` match, `!?` ambiguous match, `XX` mismatch or out of range, `??` unparseable.

For a mismatch, explanations that are exact sequence comparisons, each labelled with how likely it
is to be a coincidence (any single residue matches a random position about 1 time in 20):

| Kind | Meaning | Strength |
|---|---|---|
| `annotated_offset` | shifting by a UniProt processing feature gives a match | **strong** for initiator Met, signal/transit peptide, propeptide, main mature chain, or any fragment that explains ≥2 inputs; **weak** for a fragment explaining one input |
| `consistent_offset` | one unannotated shift makes *all* mismatched inputs match; expected number of such shifts by chance < 0.05 | **strong** (needs ≥2 inputs) |
| `isoform` | matches at the same number in an AlphaFold DB isoform model | **strong** if one isoform explains every mismatched input (≥2), else **weak** |
| `swapped` | the model already has the alternate residue | **medium** |
| `nearby` | the residue is within ±3 positions | **weak**, shown only if nothing stronger applies |

A variant that matches as written is flagged `ambiguous_match` when it also matches under a shift
that strongly explains the other inputs of the same batch.

Each suggestion shows the AlphaFold DB model and the pLDDT at that residue, as provided by
AlphaFold DB (not reinterpreted).

## What it does NOT do

- It does not judge structural confidence beyond showing AlphaFold's own pLDDT.
- It does not predict whether a variant is pathogenic. AlphaFold DB models are wild-type
  structures; the mutation itself is not modelled.
- A single variant that matches by coincidence cannot be detected; give the whole list from the
  source so batch evidence can be used.
- No DNA/transcript notation (`c.20A>T`) or genomic coordinates: use Ensembl VEP or EBI ProtVar.
- Model-organism numbering (e.g. mouse) is reported as a mismatch but not corrected.

## Repository layout

```
af_confidence/  The tool (variant parser, data sources, mapper, CLI)
tests/          Offline tests against data/cache
examples/       Variant lists for the demo (APP amyloid-beta numbering, SERPINA1 alleles)
data/cache/     AlphaFold DB and UniProt responses for the demo proteins
scripts/        Day-1 feasibility checks
docs/           Daily reports, demo commands, screenshots
```

## Data and licence

Structure predictions come from the AlphaFold Protein Structure Database (EMBL-EBI / Google DeepMind).
AlphaFold DB data are available under CC-BY-4.0; cite the AlphaFold and AlphaFold DB papers when
using the output. Processing-feature annotations come from UniProt. Code licence: MIT (see `LICENSE`).

Parts of the code and documentation were drafted with help from Claude (Anthropic).
