# Contributing

Bug reports and suggestions are welcome as GitHub issues. Most useful: a variant list where the
tool gives a wrong or misleading answer, with the source (paper or database) of the numbering.

## Development

```bash
git clone https://github.com/wangnick1004/af-confidence
cd af-confidence
python3 -m pip install -e . pytest
python3 -m pytest
```

- The tool must keep working with the Python standard library only (no runtime dependencies)
  and on Python 3.9+.
- Tests run offline against the real AlphaFold DB and UniProt responses in `data/cache`. To add
  a protein for a test, run the tool once with `--cache data/cache` (online) and commit the new
  files.
- Every suggestion is an exact sequence comparison. Changes to how evidence is graded should be
  checked with the benchmark before and after:

  ```bash
  python3 benchmark/run_benchmark.py --cache /path/to/benchmark-cache
  ```

- Keep the scope: the tool maps numbering; it does not reinterpret pLDDT or predict variant
  effects.
