# oss-catalog generator

Generate machine-readable OSS catalog files for Exahia repositories.

## Outputs

- `catalog/oss-catalog.json`
- `catalog/oss-catalog.md`
- `catalog/oss-tools.llms.txt`

## Generate

```bash
python3 tools/oss-catalog/generate_catalog.py
```

## Check (CI mode)

```bash
python3 tools/oss-catalog/generate_catalog.py --check
```

## Tests

```bash
python3 -m unittest discover -s tools/oss-catalog/tests -p "test_*.py"
```
