# llms-txt-linter

CLI to lint `llms.txt` / `llms-full.txt` files with GEO-focused checks.

## What it checks

- required sections: `Core Pages`, `Entity References`, `Citation Notes`
- absolute URL validity (`http://` or `https://`)
- duplicate URLs
- canonical host consistency (example: `exahia.com`)

## Quick start

```bash
python3 tools/llms-txt-linter/llms_txt_linter.py \
  --input tools/llms-txt-linter/sample.llms.txt
```

JSON output:

```bash
python3 tools/llms-txt-linter/llms_txt_linter.py \
  --input tools/llms-txt-linter/sample.llms.txt \
  --format json
```

Allow additional external hosts:

```bash
python3 tools/llms-txt-linter/llms_txt_linter.py \
  --input /tmp/llms.txt \
  --canonical-host exahia.com \
  --allow-host github.com \
  --allow-host www.linkedin.com
```

## Output modes

- `--format text` (default)
- `--format json`
- `--format both`
- optional report file: `--json-out /tmp/report.json`

## Example text output

```text
LLMS TXT Linter Report
Input: tools/llms-txt-linter/sample.llms.txt
Status: PASS
Canonical host: exahia.com
Allowed hosts: exahia.com
```

## Tests

```bash
python3 -m unittest discover -s tools/llms-txt-linter/tests -p "test_*.py"
```
