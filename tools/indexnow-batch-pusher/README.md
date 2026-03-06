# indexnow-batch-pusher

Small CLI to submit sitemap URLs to IndexNow (Bing/DDG/Yandex compatible).

## Why

When pages are created or updated, this tool pushes canonical URLs in one batch to IndexNow.
It is useful for GEO/SEO workflows where indexation latency matters.

## Quick start

Dry run from remote sitemap:

```bash
python3 tools/indexnow-batch-pusher/indexnow_batch_pusher.py \
  --site-url https://exahia.com \
  --key "$INDEXNOW_KEY" \
  --dry-run
```

Dry run from local sitemap file:

```bash
python3 tools/indexnow-batch-pusher/indexnow_batch_pusher.py \
  --site-url https://exahia.com \
  --key test-key \
  --sitemap-file /tmp/sitemap.xml \
  --dry-run
```

Real submission:

```bash
python3 tools/indexnow-batch-pusher/indexnow_batch_pusher.py \
  --site-url https://exahia.com \
  --key "$INDEXNOW_KEY"
```

## Options

- `--site-url`: canonical site root
- `--sitemap-url`: sitemap URL (default `<site-url>/sitemap.xml`)
- `--sitemap-file`: use local sitemap XML file
- `--key`: IndexNow key (or env `INDEXNOW_KEY`)
- `--key-location`: public key file URL
- `--urls`: extra comma-separated URLs
- `--limit`: max URLs in payload
- `--dry-run`: print URLs without API submission
- `--endpoint`: IndexNow endpoint override
- `--timeout`: HTTP timeout in seconds

## Tests

```bash
python3 -m unittest discover -s tools/indexnow-batch-pusher/tests -p "test_*.py"
```

## Smoke test (CI parity)

Run the same deterministic smoke test used in GitHub Actions:

```bash
bash tools/indexnow-batch-pusher/smoke_test.sh
```
