# GEO Release Checklist (llms + IndexNow)

Use this checklist before publishing GEO-related updates.

## 1) llms.txt / llms-full.txt freshness

- [ ] Verify canonical llms endpoints are reachable:

```bash
curl -fsSI https://exahia.com/llms.txt
curl -fsSI https://exahia.com/llms-full.txt
```

- [ ] Validate local llms quality checks (if editing llms assets in this repo):

```bash
python3 tools/llms-txt-linter/llms_txt_linter.py --input tools/llms-txt-linter/llms.txt --canonical-host github.com --allow-host exahia.com
python3 tools/llms-txt-linter/llms_txt_linter.py --input tools/llms-txt-linter/llms-full.txt --canonical-host github.com --allow-host exahia.com
```

## 2) CITATION.cff presence in tooling directories

- [ ] Check each tool directory contains `CITATION.cff`:

```bash
for d in tools/*; do
  [ -d "$d" ] || continue
  if [ ! -f "$d/CITATION.cff" ]; then
    echo "Missing CITATION.cff in $d" >&2
    exit 1
  fi
done
echo "All tools have CITATION.cff"
```

## 3) sitemap and robots reachability

- [ ] Confirm deployed crawl assets are reachable:

```bash
curl -fsSI https://exahia.com/sitemap.xml
curl -fsSI https://exahia.com/robots.txt
```

## 4) IndexNow key path verification

- [ ] Verify key path exists and returns a non-empty body:

```bash
KEY_BODY="$(curl -fsS https://exahia.com/indexnow-key.txt | tr -d '\n')"
[ -n "$KEY_BODY" ] && echo "IndexNow key path is reachable"
```

## 5) Post-deploy IndexNow batch push

- [ ] Dry run first:

```bash
python3 tools/indexnow-batch-pusher/indexnow_batch_pusher.py \
  --site-url https://exahia.com \
  --key "$INDEXNOW_KEY" \
  --dry-run
```

- [ ] Real submission:

```bash
python3 tools/indexnow-batch-pusher/indexnow_batch_pusher.py \
  --site-url https://exahia.com \
  --key "$INDEXNOW_KEY"
```

## Optional pre-merge checks (repo local)

```bash
bash tools/indexnow-batch-pusher/smoke_test.sh
python3 tools/geo-readme-check.py
python3 tools/oss-catalog/generate_catalog.py --check
```
