#!/usr/bin/env python3
"""Submit sitemap URLs to IndexNow in one batch."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def parse_sitemap_urls(xml_text: str) -> list[str]:
    return [value.strip() for value in re.findall(r"<loc>(.*?)</loc>", xml_text, flags=re.IGNORECASE)]


def to_absolute_url(site_url: str, value: str) -> str:
    if value.startswith("http://") or value.startswith("https://"):
        return value
    prefix = site_url.rstrip("/")
    if value.startswith("/"):
        return f"{prefix}{value}"
    return f"{prefix}/{value}"


def _dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def prepare_urls(
    *,
    site_url: str,
    sitemap_urls: list[str],
    extra_urls: list[str],
    limit: int,
) -> list[str]:
    host = urlparse(site_url).netloc
    merged = _dedupe(sitemap_urls + extra_urls)
    scoped = []
    for url in merged:
        try:
            if urlparse(url).netloc == host:
                scoped.append(url)
        except Exception:  # noqa: BLE001
            continue
    if limit > 0:
        return scoped[:limit]
    return scoped


def fetch_sitemap(sitemap_url: str, timeout: int) -> str:
    req = Request(
        sitemap_url,
        headers={"Accept": "application/xml,text/xml;q=0.9,*/*;q=0.8"},
    )
    try:
        with urlopen(req, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            body = response.read().decode("utf-8", errors="replace")
    except URLError as exc:
        raise RuntimeError(f"Failed to fetch sitemap at {sitemap_url}: {exc}") from exc
    if status >= 400:
        raise RuntimeError(f"Sitemap request failed with HTTP {status}: {sitemap_url}")
    return body


def submit_indexnow(payload: dict[str, object], endpoint: str, timeout: int) -> tuple[int, str]:
    body = json.dumps(payload).encode("utf-8")
    req = Request(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            text = response.read().decode("utf-8", errors="replace")
            return status, text
    except HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        return exc.code, text
    except URLError as exc:
        raise RuntimeError(f"Failed to submit payload to {endpoint}: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Batch submit sitemap URLs to IndexNow.")
    parser.add_argument("--site-url", default=os.getenv("SITE_URL", "https://exahia.com"))
    parser.add_argument("--sitemap-url", default=None, help="Defaults to <site-url>/sitemap.xml")
    parser.add_argument("--sitemap-file", default=None, help="Read sitemap XML from a local file instead.")
    parser.add_argument("--key", default=os.getenv("INDEXNOW_KEY"), help="IndexNow key.")
    parser.add_argument(
        "--key-location",
        default=os.getenv("INDEXNOW_KEY_LOCATION"),
        help="Public URL that serves the key file.",
    )
    parser.add_argument("--urls", default="", help="Extra comma-separated URLs to include.")
    parser.add_argument("--limit", type=int, default=10000, help="Maximum URLs per batch.")
    parser.add_argument("--endpoint", default="https://api.indexnow.org/indexnow")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    site_url = args.site_url.rstrip("/")
    host = urlparse(site_url).netloc
    if not host:
        print("Invalid --site-url (host is empty).", file=sys.stderr)
        return 2

    if not args.key:
        print("Missing IndexNow key. Use --key or INDEXNOW_KEY.", file=sys.stderr)
        return 2

    key_location = args.key_location or f"{site_url}/indexnow-key.txt"
    sitemap_url = args.sitemap_url or f"{site_url}/sitemap.xml"

    if args.sitemap_file:
        path = Path(args.sitemap_file)
        if not path.exists():
            print(f"Sitemap file not found: {path}", file=sys.stderr)
            return 2
        sitemap_xml = path.read_text(encoding="utf-8")
    else:
        try:
            sitemap_xml = fetch_sitemap(sitemap_url, timeout=args.timeout)
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            return 2

    sitemap_urls = parse_sitemap_urls(sitemap_xml)
    extra_urls = [
        to_absolute_url(site_url, value.strip())
        for value in args.urls.split(",")
        if value.strip()
    ]

    final_urls = prepare_urls(
        site_url=site_url,
        sitemap_urls=sitemap_urls,
        extra_urls=extra_urls,
        limit=args.limit,
    )
    if not final_urls:
        print("No eligible URLs found for submission.", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"Dry run: {len(final_urls)} URL(s) to submit for host {host}.")
        for url in final_urls[:20]:
            print(f"- {url}")
        if len(final_urls) > 20:
            print(f"... and {len(final_urls) - 20} more")
        return 0

    payload = {
        "host": host,
        "key": args.key,
        "keyLocation": key_location,
        "urlList": final_urls,
    }

    try:
        status, text = submit_indexnow(payload, endpoint=args.endpoint, timeout=args.timeout)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if status >= 400:
        print(f"IndexNow submission failed (HTTP {status}).", file=sys.stderr)
        if text:
            print(text[:1000], file=sys.stderr)
        return 2

    print(f"IndexNow submission OK: {len(final_urls)} URL(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
