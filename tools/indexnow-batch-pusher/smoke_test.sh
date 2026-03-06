#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

SITEMAP_FIXTURE="tools/indexnow-batch-pusher/tests/fixtures/sitemap-smoke.xml"

OUTPUT="$(python3 tools/indexnow-batch-pusher/indexnow_batch_pusher.py \
  --site-url https://exahia.com \
  --key test-key \
  --sitemap-file "$SITEMAP_FIXTURE" \
  --urls /shadow-ai,https://example.org/not-allowed \
  --dry-run)"

printf '%s\n' "$OUTPUT"

EXPECTED_HEADER="Dry run: 3 URL(s) to submit for host exahia.com."
ACTUAL_HEADER="$(printf '%s\n' "$OUTPUT" | head -n 1)"
if [[ "$ACTUAL_HEADER" != "$EXPECTED_HEADER" ]]; then
  echo "Unexpected dry-run header." >&2
  exit 1
fi

URL_LINE_COUNT="$(printf '%s\n' "$OUTPUT" | grep -c '^- https://')"
if [[ "$URL_LINE_COUNT" -ne 3 ]]; then
  echo "Expected exactly 3 URL lines, got $URL_LINE_COUNT." >&2
  exit 1
fi

printf '%s\n' "$OUTPUT" | grep -Fq -- "- https://exahia.com/ia-souveraine"
printf '%s\n' "$OUTPUT" | grep -Fq -- "- https://exahia.com/docs"
printf '%s\n' "$OUTPUT" | grep -Fq -- "- https://exahia.com/shadow-ai"

echo "IndexNow smoke test passed."
