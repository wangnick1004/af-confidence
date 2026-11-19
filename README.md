# af-confidence

把文獻中的突變位置，正確對應到 AFDB 模型上

Map protein-level variants written in the literature (e.g. `E6V`) onto the correct residue of the
AlphaFold DB model, and explain numbering mismatches with evidence before anyone interprets a
structure.

> Status: v0.1 complete on the command line; 85 offline tests pass on Python 3.9 and 3.13.
> Accuracy measured on 735 real UniProt variants: see [Benchmark](#benchmark).
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
     -> [medium] annotated_offset: +1: E7V matches; UniProt: initiator Met removed; mature chain
        'Hemoglobin subunit beta' starts at 2 (explains 1/1 mismatched input) [pLDDT 96.56]
```

### Input

The first word is the protein, the rest are variants:

| Protein as | Example |
|---|---|
| UniProt accession | `af-confidence P68871 E6V` |
| Gene name (human by default) | `af-confidence HBB E6V` |
| Isoform accession | `af-confidence P04637-2 R175H` |
| Gene name in another organism | `af-confidence Trp53 R172H --organism 10090` |

Variants: `E6V`, `p.E6V`, `Glu6Val`, `p.Glu6Val`, `p.(Glu6Val)`, nonsense `R213*` / `p.Arg213Ter`;
separate them with spaces or commas.

A list from one or more papers: `-f FILE` (can be repeated). One line per protein, `#` starts a
comment:

```
# variants collected from several papers
HBB      E6V            # sickle cell, legacy numbering
SERPINA1 E342K, E264V   # Z and S alleles
P04637   R175H R72P
```

```bash
af-confidence -f my_variants.txt
```

Lines without a protein use the one given on the command line, e.g.
`af-confidence APP -f examples/app_abeta_numbering.txt`. Entries for the same protein (by gene name
or accession) are checked together, so batch evidence uses all of them. A protein that cannot be
loaded is reported as an error without stopping the others.

Some gene names look like variants (`C1S`, `F2R`, `C4A`): at the start of a line in a file they are
read as the protein; when a protein is also given on the command line they are read as variants.
Use the UniProt accession if in doubt.

### Options and output

| Option | Meaning |
|---|---|
| `-f`, `--file FILE` | read `[PROTEIN] VARIANT ...` lines (repeatable) |
| `--organism TAXID` | NCBI taxonomy ID for gene-name lookup (default 9606, human; mouse 10090) |
| `--format text\|tsv\|json` | `tsv` opens in Excel; one row per suggestion |
| `--cache DIR` | cache directory (default `~/.cache/af-confidence`) |
| `--offline` | use cached files only |

The demo proteins are cached in `data/cache`, so `--cache data/cache --offline` works without network.
Network requests are retried 3 times with back-off; cache files are written atomically and a
corrupt cache file is fetched again.

Exit code: 0 if every variant matches unambiguously, 1 otherwise, 2 if a protein could not be
loaded or a network error occurred.

Run the tests: `python3 -m pip install pytest && python3 -m pytest`.

## What it checks

Status per variant: `OK` match, `!?` ambiguous match, `XX` mismatch or out of range, `??` unparseable.

For a mismatch, explanations that are exact sequence comparisons, each labelled with how likely it
is to be a coincidence (any single residue matches a random position about 1 time in 20):

| Kind | Meaning | Strength |
|---|---|---|
| `annotated_offset` | shifting by a UniProt processing feature (initiator Met, signal/transit peptide, propeptide, mature chain, other fragments), or by a UniProt sequence update the AlphaFold DB model has not caught up with, gives a match | **strong** if it explains ≥2 inputs and that many coincidences has probability < 0.05 / number of shifts tried; **medium** if a primary feature explains this one input and no other shift is strong; **weak** otherwise |
| `consistent_offset` | one unannotated shift makes *all* mismatched inputs match; expected number of such shifts by chance < 0.05 | **strong** (needs ≥2 inputs) |
| `isoform` | matches at the same number in an AlphaFold DB isoform model | **strong** if one isoform explains every mismatched input (≥2), else **weak** |
| `swapped` | the model already has the alternate residue | **medium** |
| `nearby` | the residue is within ±3 positions | **weak**, shown only if nothing stronger applies |

A variant that matches as written is flagged `ambiguous_match` when it also matches under a shift
that strongly explains the other inputs of the same batch.

Each suggestion shows the AlphaFold DB model and the pLDDT at that residue, as provided by
AlphaFold DB (not reinterpreted).

Warnings are printed when UniProt annotations could not be loaded (offsets not checked) or when
the AlphaFold DB model was built on an older UniProt sequence than the current one. In that case
the tool aligns the two sequences: if one is a stretch of the other (e.g. UniProt moved the
canonical start codon), UniProt annotations are converted to model positions and the shift is
offered as an explanation; otherwise UniProt annotations are not used.

For an isoform accession, UniProt annotates processing on the canonical entry only; N-terminal
features (initiator Met, signal/transit peptide, propeptide) are used for the isoform when its
N-terminus is identical over that stretch.

## Benchmark

`benchmark/run_benchmark.py` samples 200 reviewed human UniProt entries (fixed seed) with a signal
peptide or a removed initiator Met and uses their natural variants (positioned by UniProt, hence
ground truth) after rewriting them the way the literature often does. Full table:
[`benchmark/results.md`](benchmark/results.md); the sampled data: `benchmark/dataset.tsv`.

Main results (193 proteins, 735 variants, checked 2026-11-19):

| Scenario | True position is the top suggestion | A wrong position marked strong |
|---|---|---|
| Correct UniProt numbering (should simply match) | 735/735 match | – |
| Mature/legacy numbering, one variant at a time | 92.4% (as medium) | 0% |
| Mature/legacy numbering, whole list | 99.4% (92% strong) | 0% |
| Unannotated shift of 5–60, whole list (≥3 variants) | 81.6% | 0.3% |
| Unannotated shift or ±1–3 typo, one variant | – (cannot be known) | 0% |

What the numbers mean in practice:

- **Strong** suggestions pointed to a wrong position for 2 of 2,401 inputs. **Medium** (one variant, annotated
  shift) is right about 9 times in 10; the rest are coincidences that cannot be told apart from a
  single variant (e.g. a typo of −1 looks exactly like "initiator Met not counted").
- 7–9% of single variants written in legacy numbering match the model *by coincidence* and
  cannot be detected alone; in whole lists, most of these are flagged `ambiguous_match`
  (silent misses drop to < 1%). **Check whole lists, not single variants.**
- While building the benchmark the tool found a real discrepancy: UniProt changed the canonical
  sequence of biotinidase (P43251) in 2026, 20 residues shorter at the N-terminus, while the
  AlphaFold DB entry for P43251 still uses the old sequence, so all UniProt-numbered variants are
  off by 20 on that model. AlphaFold DB does have a model with the new sequence, filed under
  isoform 4 (AF-P43251-4-F1); the tool now points to it in its warning.

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
benchmark/      Accuracy benchmark on real UniProt variants (script, sampled data, results)
scripts/        Day-1 feasibility checks
docs/           Daily reports, demo commands, screenshots
```

## Data and licence

Structure predictions come from the AlphaFold Protein Structure Database (EMBL-EBI / Google DeepMind).
AlphaFold DB data are available under CC-BY-4.0; cite the AlphaFold and AlphaFold DB papers when
using the output. Processing-feature annotations come from UniProt. Code licence: MIT (see `LICENSE`).

Parts of the code and documentation were drafted with help from Claude (Anthropic).
