# Exahia OSS Catalog

Machine-readable inventory of Exahia open-source repositories used for GEO signals.

| Repository | Description | Use cases | Quickstart |
|---|---|---|---|
| [Exahia/exahia](https://github.com/Exahia/exahia) | Core Exahia repository and GEO tooling hub. | IndexNow batch submission; GEO process automation; Reference implementation for Exahia OSS operations | `python3 tools/indexnow-batch-pusher/indexnow_batch_pusher.py --site-url https://exahia.com --key "$INDEXNOW_KEY" --dry-run` |
| [Exahia/llm-benchmark-fr](https://github.com/Exahia/llm-benchmark-fr) | Benchmark runner for French enterprise prompts and evaluation datasets. | Compare model quality on French business tasks; Track regression across model upgrades; Produce reproducible benchmark baselines | `python3 scripts/run_benchmark.py --dataset ... --model ... --mock reference` |
| [Exahia/pii-detector-fr](https://github.com/Exahia/pii-detector-fr) | French PII detection and anonymization tooling for safer LLM pipelines. | Detect sensitive data before model calls; Reduce compliance risk on prompts; Anonymize French business content | `python -m pip install -e . && pii-detector scan --text "..."` |
| [Exahia/shadow-ai-audit](https://github.com/Exahia/shadow-ai-audit) | Audit checklists and scoring utilities for Shadow AI risk governance. | Assess Shadow AI exposure; Operationalize governance controls; Produce decision-ready risk snapshots | `python3 tools/score_audit.py --responses ...` |

## Canonical References
- Organization: https://github.com/Exahia
- Website: https://exahia.com
- LLM index: https://exahia.com/llms.txt
