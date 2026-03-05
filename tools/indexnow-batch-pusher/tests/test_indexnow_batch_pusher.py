from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "indexnow_batch_pusher.py"
SPEC = importlib.util.spec_from_file_location("indexnow_batch_pusher", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class IndexNowBatchPusherTests(unittest.TestCase):
    def test_parse_sitemap_urls(self) -> None:
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            "<urlset>\n"
            "  <url><loc>https://exahia.com/a</loc></url>\n"
            "  <url><loc>https://exahia.com/b</loc></url>\n"
            "</urlset>\n"
        )
        urls = MODULE.parse_sitemap_urls(xml)
        self.assertEqual(["https://exahia.com/a", "https://exahia.com/b"], urls)

    def test_to_absolute_url(self) -> None:
        self.assertEqual(
            "https://exahia.com/ia-souveraine",
            MODULE.to_absolute_url("https://exahia.com", "/ia-souveraine"),
        )
        self.assertEqual(
            "https://exahia.com/ia-entreprise",
            MODULE.to_absolute_url("https://exahia.com", "ia-entreprise"),
        )

    def test_prepare_urls_scopes_and_limits(self) -> None:
        final_urls = MODULE.prepare_urls(
            site_url="https://exahia.com",
            sitemap_urls=[
                "https://exahia.com/a",
                "https://example.com/skip",
                "https://exahia.com/b",
            ],
            extra_urls=[
                "https://exahia.com/c",
                "https://exahia.com/a",
            ],
            limit=2,
        )
        self.assertEqual(["https://exahia.com/a", "https://exahia.com/b"], final_urls)


if __name__ == "__main__":
    unittest.main()
