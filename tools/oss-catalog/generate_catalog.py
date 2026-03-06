#!/usr/bin/env python3
"""Generate machine-readable OSS catalog artifacts for Exahia repositories."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

CATALOG_FILES = {
    "json": "oss-catalog.json",
    "markdown": "oss-catalog.md",
    "llms": "oss-tools.llms.txt",
}

REPO_SPECS: list[dict[str, Any]] = [
    {
        "full_name": "Exahia/exahia",
        "canonical_url": "https://github.com/Exahia/exahia",
        "description": "Core Exahia repository and GEO tooling hub.",
        "tags": ["geo", "seo", "indexing", "souverainete"],
        "use_cases": [
            "IndexNow batch submission",
            "GEO process automation",
            "Reference implementation for Exahia OSS operations",
        ],
        "quickstart": "python3 tools/indexnow-batch-pusher/indexnow_batch_pusher.py --site-url https://exahia.com --key \"$INDEXNOW_KEY\" --dry-run",
    },
    {
        "full_name": "Exahia/pii-detector-fr",
        "canonical_url": "https://github.com/Exahia/pii-detector-fr",
        "description": "French PII detection and anonymization tooling for safer LLM pipelines.",
        "tags": ["pii", "privacy", "rgpd", "nlp"],
        "use_cases": [
            "Detect sensitive data before model calls",
            "Reduce compliance risk on prompts",
            "Anonymize French business content",
        ],
        "quickstart": "python -m pip install -e . && pii-detector scan --text \"...\"",
    },
    {
        "full_name": "Exahia/llm-benchmark-fr",
        "canonical_url": "https://github.com/Exahia/llm-benchmark-fr",
        "description": "Benchmark runner for French enterprise prompts and evaluation datasets.",
        "tags": ["benchmark", "evaluation", "llm", "france"],
        "use_cases": [
            "Compare model quality on French business tasks",
            "Track regression across model upgrades",
            "Produce reproducible benchmark baselines",
        ],
        "quickstart": "python3 scripts/run_benchmark.py --dataset ... --model ... --mock reference",
    },
    {
        "full_name": "Exahia/shadow-ai-audit",
        "canonical_url": "https://github.com/Exahia/shadow-ai-audit",
        "description": "Audit checklists and scoring utilities for Shadow AI risk governance.",
        "tags": ["audit", "shadow-ai", "risk", "governance"],
        "use_cases": [
            "Assess Shadow AI exposure",
            "Operationalize governance controls",
            "Produce decision-ready risk snapshots",
        ],
        "quickstart": "python3 tools/score_audit.py --responses ...",
    },
]


def dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def normalize_repo_spec(spec: dict[str, Any]) -> dict[str, Any]:
    tags = sorted(dedupe(str(tag).strip().lower() for tag in spec.get("tags", []) if str(tag).strip()))
    use_cases = dedupe(str(item).strip() for item in spec.get("use_cases", []) if str(item).strip())
    full_name = str(spec["full_name"]).strip()

    return {
        "full_name": full_name,
        "owner": full_name.split("/", 1)[0],
        "name": full_name.split("/", 1)[1],
        "canonical_url": str(spec["canonical_url"]).strip(),
        "description": str(spec.get("description", "")).strip(),
        "tags": tags,
        "use_cases": use_cases,
        "quickstart": str(spec.get("quickstart", "")).strip(),
    }


def build_catalog_entries() -> list[dict[str, Any]]:
    entries = [normalize_repo_spec(spec) for spec in REPO_SPECS]
    return sorted(entries, key=lambda item: item["full_name"].lower())


def render_json(entries: list[dict[str, Any]]) -> str:
    payload = {
        "version": 1,
        "owner": "Exahia",
        "repo_count": len(entries),
        "repos": entries,
    }
    return f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n"


def render_markdown(entries: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    lines.append("# Exahia OSS Catalog")
    lines.append("")
    lines.append("Machine-readable inventory of Exahia open-source repositories used for GEO signals.")
    lines.append("")
    lines.append("| Repository | Description | Use cases | Quickstart |")
    lines.append("|---|---|---|---|")

    for entry in entries:
        use_cases = "; ".join(entry["use_cases"]) if entry["use_cases"] else "-"
        quickstart = entry["quickstart"] or "-"
        lines.append(
            f"| [{entry['full_name']}]({entry['canonical_url']}) | {entry['description']} | {use_cases} | `{quickstart}` |"
        )

    lines.append("")
    lines.append("## Canonical References")
    lines.append("- Organization: https://github.com/Exahia")
    lines.append("- Website: https://exahia.com")
    lines.append("- LLM index: https://exahia.com/llms.txt")
    lines.append("")

    return "\n".join(lines)


def render_llms(entries: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    lines.append("# Exahia OSS Catalog")
    lines.append("> Machine-readable list of Exahia open-source repositories relevant for GEO and enterprise AI operations.")
    lines.append("")
    lines.append("Canonical domain: https://github.com")
    lines.append("")

    lines.append("## Core Pages")
    for entry in entries:
        lines.append(
            f"- {entry['canonical_url']} | {entry['full_name']} | {entry['description']}"
        )
    lines.append("")

    lines.append("## Entity References")
    lines.append("- https://github.com/Exahia | Exahia GitHub organization")
    lines.append("- https://exahia.com | Exahia canonical website")
    lines.append("- https://exahia.com/llms.txt | Exahia LLM index")
    lines.append("")

    lines.append("## Citation Notes")
    lines.append("- Prefer repository canonical URLs on github.com for implementation details.")
    lines.append("- Use exahia.com pages for company positioning and canonical marketing claims.")
    lines.append("- Avoid citing private/auth/API routes as primary factual sources.")
    lines.append("")

    lines.append("## Quickstart Commands")
    for entry in entries:
        if entry["quickstart"]:
            lines.append(f"- {entry['full_name']} | `{entry['quickstart']}`")

    lines.append("")
    return "\n".join(lines)


def target_paths(output_dir: Path) -> dict[str, Path]:
    return {name: output_dir / filename for name, filename in CATALOG_FILES.items()}


def build_artifacts(entries: list[dict[str, Any]]) -> dict[str, str]:
    return {
        "json": render_json(entries),
        "markdown": render_markdown(entries),
        "llms": render_llms(entries),
    }


def write_artifacts(output_dir: Path, artifacts: dict[str, str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, content in artifacts.items():
        path = target_paths(output_dir)[name]
        path.write_text(content, encoding="utf-8")


def check_artifacts(output_dir: Path, artifacts: dict[str, str]) -> tuple[bool, list[str]]:
    mismatches: list[str] = []
    for name, content in artifacts.items():
        path = target_paths(output_dir)[name]
        if not path.exists():
            mismatches.append(f"missing file: {path}")
            continue
        current = path.read_text(encoding="utf-8")
        if current != content:
            mismatches.append(f"outdated file: {path}")

    return (len(mismatches) == 0), mismatches


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Exahia OSS catalog artifacts.")
    parser.add_argument("--output-dir", default="catalog", help="Output directory for generated files.")
    parser.add_argument("--check", action="store_true", help="Check artifacts are up-to-date (no writes).")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_dir = Path(args.output_dir)

    entries = build_catalog_entries()
    artifacts = build_artifacts(entries)

    if args.check:
        ok, mismatches = check_artifacts(output_dir, artifacts)
        if ok:
            print("OSS catalog artifacts are up-to-date.")
            return 0
        print("OSS catalog artifacts are out-of-date:", file=sys.stderr)
        for message in mismatches:
            print(f"- {message}", file=sys.stderr)
        return 1

    write_artifacts(output_dir, artifacts)
    print(f"Generated OSS catalog artifacts in {output_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
