#!/usr/bin/env python3
"""Lint llms.txt / llms-full.txt files for GEO quality guardrails."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence
from urllib.parse import urlparse

REQUIRED_SECTIONS = (
    "core pages",
    "entity references",
    "citation notes",
)

SECTION_PATTERN = re.compile(r"^\s{0,3}##+\s+(.+?)\s*$")
CANONICAL_DOMAIN_PATTERN = re.compile(r"^\s*canonical\s+domain\s*:\s*(\S+)\s*$", re.IGNORECASE)
URL_PATTERN = re.compile(r"https?://[^\s<>'\"\]\[\)\(]+", re.IGNORECASE)


def normalize_section_name(value: str) -> str:
    return " ".join(value.strip().lower().split())


def normalize_host(value: str) -> str:
    host = value.strip().lower().rstrip(".")
    if ":" in host:
        host = host.split(":", 1)[0]
    return host


def parse_sections(text: str) -> list[str]:
    sections: list[str] = []
    for line in text.splitlines():
        match = SECTION_PATTERN.match(line)
        if not match:
            continue
        sections.append(normalize_section_name(match.group(1)))
    return sections


def extract_urls(text: str) -> list[str]:
    urls: list[str] = []
    for match in URL_PATTERN.findall(text):
        cleaned = match.rstrip(".,;:")
        if cleaned:
            urls.append(cleaned)
    return urls


def extract_canonical_domain_value(text: str) -> str | None:
    for line in text.splitlines():
        match = CANONICAL_DOMAIN_PATTERN.match(line)
        if match:
            return match.group(1).strip()
    return None


def is_valid_http_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except Exception:  # noqa: BLE001
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def build_issue(code: str, message: str, **details: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "code": code,
        "message": message,
    }
    if details:
        payload["details"] = details
    return payload


def lint_text(
    text: str,
    *,
    canonical_host: str,
    allow_hosts: Sequence[str] | None = None,
) -> dict[str, Any]:
    canonical_host_norm = normalize_host(canonical_host)
    allowed_hosts = {canonical_host_norm}
    if allow_hosts:
        allowed_hosts.update(normalize_host(host) for host in allow_hosts if host.strip())

    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    sections = parse_sections(text)
    section_set = set(sections)
    missing_sections = [section for section in REQUIRED_SECTIONS if section not in section_set]
    if missing_sections:
        errors.append(
            build_issue(
                "missing_required_sections",
                "Missing required section(s).",
                missing=missing_sections,
            )
        )

    raw_urls = extract_urls(text)
    invalid_urls = [url for url in raw_urls if not is_valid_http_url(url)]
    valid_urls = [url for url in raw_urls if is_valid_http_url(url)]

    if invalid_urls:
        errors.append(
            build_issue(
                "invalid_urls",
                "Found invalid absolute URL(s).",
                urls=dedupe(invalid_urls),
            )
        )

    if not valid_urls:
        warnings.append(build_issue("no_urls_found", "No absolute URLs found in file."))

    duplicate_urls = [url for url, count in Counter(valid_urls).items() if count > 1]
    if duplicate_urls:
        warnings.append(
            build_issue(
                "duplicate_urls",
                "Found duplicate URL(s).",
                urls=sorted(duplicate_urls),
            )
        )

    canonical_domain_value = extract_canonical_domain_value(text)
    if canonical_domain_value is None:
        warnings.append(
            build_issue(
                "missing_canonical_domain_line",
                "Canonical domain line not found (expected: 'Canonical domain: https://<host>').",
            )
        )
    else:
        if not is_valid_http_url(canonical_domain_value):
            errors.append(
                build_issue(
                    "invalid_canonical_domain_url",
                    "Canonical domain line is not a valid absolute URL.",
                    value=canonical_domain_value,
                )
            )
        else:
            found_host = normalize_host(urlparse(canonical_domain_value).netloc)
            if found_host != canonical_host_norm:
                errors.append(
                    build_issue(
                        "canonical_domain_host_mismatch",
                        "Canonical domain host does not match expected canonical host.",
                        expected=canonical_host_norm,
                        found=found_host,
                    )
                )

    hosts_by_url: list[tuple[str, str]] = []
    for url in valid_urls:
        hosts_by_url.append((url, normalize_host(urlparse(url).netloc)))

    urls_on_canonical_host = [url for url, host in hosts_by_url if host == canonical_host_norm]
    if not urls_on_canonical_host:
        errors.append(
            build_issue(
                "canonical_host_not_found",
                "No URL found on canonical host.",
                expected=canonical_host_norm,
            )
        )

    unexpected_host_urls = [url for url, host in hosts_by_url if host not in allowed_hosts]
    if unexpected_host_urls:
        unexpected_hosts = sorted({normalize_host(urlparse(url).netloc) for url in unexpected_host_urls})
        errors.append(
            build_issue(
                "unexpected_host_urls",
                "Found URL(s) outside canonical/allowed hosts.",
                allowed=sorted(allowed_hosts),
                unexpected_hosts=unexpected_hosts,
                sample_urls=dedupe(unexpected_host_urls)[:10],
            )
        )

    return {
        "status": "pass" if not errors else "fail",
        "canonical_host": canonical_host_norm,
        "allowed_hosts": sorted(allowed_hosts),
        "sections": {
            "required": list(REQUIRED_SECTIONS),
            "found": sections,
            "missing": missing_sections,
        },
        "stats": {
            "url_count": len(raw_urls),
            "unique_url_count": len(set(raw_urls)),
            "duplicate_url_count": len(duplicate_urls),
        },
        "errors": errors,
        "warnings": warnings,
    }


def format_text_report(report: dict[str, Any], input_path: str) -> str:
    lines: list[str] = []
    lines.append("LLMS TXT Linter Report")
    lines.append(f"Input: {input_path}")
    lines.append(f"Status: {report['status'].upper()}")
    lines.append(f"Canonical host: {report['canonical_host']}")
    lines.append(f"Allowed hosts: {', '.join(report['allowed_hosts'])}")
    lines.append("")

    lines.append("Stats:")
    stats = report["stats"]
    lines.append(f"- URLs: {stats['url_count']}")
    lines.append(f"- Unique URLs: {stats['unique_url_count']}")
    lines.append(f"- Duplicate URLs: {stats['duplicate_url_count']}")
    lines.append("")

    lines.append("Required sections:")
    missing = report["sections"]["missing"]
    if missing:
        lines.append(f"- Missing: {', '.join(missing)}")
    else:
        lines.append("- Missing: none")
    lines.append("")

    lines.append(f"Errors ({len(report['errors'])}):")
    if report["errors"]:
        for issue in report["errors"]:
            lines.append(f"- [{issue['code']}] {issue['message']}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append(f"Warnings ({len(report['warnings'])}):")
    if report["warnings"]:
        for issue in report["warnings"]:
            lines.append(f"- [{issue['code']}] {issue['message']}")
    else:
        lines.append("- none")

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lint llms.txt and llms-full.txt files for GEO quality checks.")
    parser.add_argument("--input", required=True, help="Path to llms text file.")
    parser.add_argument("--canonical-host", default="exahia.com", help="Expected canonical host.")
    parser.add_argument(
        "--allow-host",
        action="append",
        default=[],
        help="Additional allowed host (can be repeated).",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json", "both"),
        default="text",
        help="Report output format.",
    )
    parser.add_argument("--json-out", default=None, help="Optional path to write JSON report.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    input_path = Path(args.input)
    if not input_path.exists() or not input_path.is_file():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 2

    text = input_path.read_text(encoding="utf-8")
    report = lint_text(
        text,
        canonical_host=args.canonical_host,
        allow_hosts=args.allow_host,
    )

    report_payload = {
        "input": str(input_path),
        **report,
    }

    if args.format in {"text", "both"}:
        print(format_text_report(report_payload, str(input_path)))

    json_text = json.dumps(report_payload, ensure_ascii=False, indent=2)
    if args.format in {"json", "both"}:
        print(json_text)

    if args.json_out:
        Path(args.json_out).write_text(f"{json_text}\n", encoding="utf-8")

    return 0 if not report_payload["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
