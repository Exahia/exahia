from __future__ import annotations

import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "llms_txt_linter.py"
SPEC = importlib.util.spec_from_file_location("llms_txt_linter", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def sample_llms_text(*, include_duplicates: bool = False, include_external: bool = False) -> str:
    base_lines = [
        "# Demo",
        "Canonical domain: https://exahia.com",
        "",
        "## Core Pages",
        "- https://exahia.com/",
        "- https://exahia.com/docs",
        "",
        "## Entity References",
        "- https://exahia.com/company",
        "",
        "## Citation Notes",
        "- Prefer canonical pages.",
    ]
    if include_duplicates:
        base_lines.insert(5, "- https://exahia.com/")
    if include_external:
        base_lines.append("- https://github.com/Exahia")
    return "\n".join(base_lines) + "\n"


class LlmsTxtLinterTests(unittest.TestCase):
    def test_parse_sections_normalizes_headings(self) -> None:
        text = "## Core Pages\n### Entity References\n## Citation   Notes\n"
        sections = MODULE.parse_sections(text)
        self.assertEqual(["core pages", "entity references", "citation notes"], sections)

    def test_extract_urls_trims_trailing_punctuation(self) -> None:
        text = "Use https://exahia.com/docs, then https://exahia.com/ia-souveraine."
        urls = MODULE.extract_urls(text)
        self.assertEqual(["https://exahia.com/docs", "https://exahia.com/ia-souveraine"], urls)

    def test_lint_ok_on_valid_file(self) -> None:
        report = MODULE.lint_text(sample_llms_text(), canonical_host="exahia.com")
        self.assertEqual("pass", report["status"])
        self.assertEqual([], report["errors"])

    def test_lint_reports_missing_required_sections(self) -> None:
        text = "# Demo\nCanonical domain: https://exahia.com\n## Core Pages\n- https://exahia.com\n"
        report = MODULE.lint_text(text, canonical_host="exahia.com")
        codes = {item["code"] for item in report["errors"]}
        self.assertIn("missing_required_sections", codes)

    def test_lint_reports_canonical_host_mismatch(self) -> None:
        text = sample_llms_text().replace("https://exahia.com", "https://example.com", 1)
        report = MODULE.lint_text(text, canonical_host="exahia.com")
        codes = {item["code"] for item in report["errors"]}
        self.assertIn("canonical_domain_host_mismatch", codes)

    def test_lint_reports_duplicate_urls_as_warning(self) -> None:
        report = MODULE.lint_text(sample_llms_text(include_duplicates=True), canonical_host="exahia.com")
        codes = {item["code"] for item in report["warnings"]}
        self.assertIn("duplicate_urls", codes)

    def test_lint_reports_unexpected_host_urls(self) -> None:
        report = MODULE.lint_text(sample_llms_text(include_external=True), canonical_host="exahia.com")
        codes = {item["code"] for item in report["errors"]}
        self.assertIn("unexpected_host_urls", codes)

    def test_lint_allows_whitelisted_external_host(self) -> None:
        report = MODULE.lint_text(
            sample_llms_text(include_external=True),
            canonical_host="exahia.com",
            allow_hosts=["github.com"],
        )
        codes = {item["code"] for item in report["errors"]}
        self.assertNotIn("unexpected_host_urls", codes)

    def test_main_returns_non_zero_on_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "sample.llms.txt"
            input_path.write_text("# Demo\n", encoding="utf-8")

            stdout_buffer = io.StringIO()
            with redirect_stdout(stdout_buffer):
                rc = MODULE.main(["--input", str(input_path)])
            self.assertEqual(1, rc)

    def test_main_json_output_contains_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "sample.llms.txt"
            input_path.write_text(sample_llms_text(), encoding="utf-8")

            stdout_buffer = io.StringIO()
            with redirect_stdout(stdout_buffer):
                rc = MODULE.main(["--input", str(input_path), "--format", "json"])

            self.assertEqual(0, rc)
            output = stdout_buffer.getvalue()
            self.assertIn('"status": "pass"', output)


if __name__ == "__main__":
    unittest.main()
