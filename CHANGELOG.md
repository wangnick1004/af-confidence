# Changelog

All notable changes to this project. Versions follow [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-11-19

First release: a command-line tool that maps protein-level variants written in the literature
onto AlphaFold DB models and explains numbering mismatches with graded evidence.

### Added
- Variant notation: `E6V`, `p.E6V`, `Glu6Val`, `p.Glu6Val`, `p.(Glu6Val)`, nonsense (`*`, `Ter`).
- Protein input as UniProt accession, isoform accession (`P04637-2`) or gene name
  (`--organism` for non-human); lists from files with one protein per line (`-f`).
- Explanations for mismatches: annotated offset (UniProt processing features or a UniProt
  sequence update), consistent offset, isoform, swapped ref/alt, nearby residue; detection of
  coincidental matches in a batch (`ambiguous_match`).
- Evidence levels strong / medium / weak based on the probability of a coincidence (binomial
  tail with Bonferroni correction; expected chance hits for unannotated shifts).
- Detection of AlphaFold DB models built on an older UniProt sequence, with conversion of
  UniProt annotations to model positions and a pointer to a model that has the current sequence.
- Output as text, TSV or JSON; exit codes 0 / 1 / 2.
- Local cache, `--offline` mode, retries with back-off, atomic cache writes, cached "no model"
  answers; no third-party dependencies; Python 3.9+.
- Accuracy benchmark on 735 UniProt natural variants (`benchmark/`).
- 104 offline tests; continuous integration on Linux, macOS and Windows with Python 3.9–3.13,
  and a weekly check against the live AlphaFold DB and UniProt APIs.

[0.1.0]: https://github.com/wangnick1004/af-confidence/releases/tag/v0.1.0
