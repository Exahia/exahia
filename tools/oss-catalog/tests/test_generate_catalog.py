from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "generate_catalog.py"
SPEC = importlib.util.spec_from_file_location("generate_catalog", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GenerateCatalogTests(unittest.TestCase):
    def test_build_catalog_entries_sorted(self) -> None:
        entries = MODULE.build_catalog_entries()
        names = [entry["full_name"] for entry in entries]
        self.assertEqual(sorted(names), names)
        self.assertEqual(4, len(entries))

    def test_render_json_contains_repo_count(self) -> None:
        entries = MODULE.build_catalog_entries()
        text = MODULE.render_json(entries)
        self.assertIn('"repo_count": 4', text)
        self.assertIn('"full_name": "Exahia/exahia"', text)

    def test_render_markdown_has_table(self) -> None:
        entries = MODULE.build_catalog_entries()
        text = MODULE.render_markdown(entries)
        self.assertIn("| Repository | Description | Use cases | Quickstart |", text)
        self.assertIn("https://github.com/Exahia", text)

    def test_render_llms_has_required_sections(self) -> None:
        entries = MODULE.build_catalog_entries()
        text = MODULE.render_llms(entries)
        self.assertIn("## Core Pages", text)
        self.assertIn("## Entity References", text)
        self.assertIn("## Citation Notes", text)

    def test_write_and_check_artifacts_up_to_date(self) -> None:
        entries = MODULE.build_catalog_entries()
        artifacts = MODULE.build_artifacts(entries)

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            MODULE.write_artifacts(output_dir, artifacts)
            ok, mismatches = MODULE.check_artifacts(output_dir, artifacts)
            self.assertTrue(ok)
            self.assertEqual([], mismatches)

    def test_check_artifacts_detects_drift(self) -> None:
        entries = MODULE.build_catalog_entries()
        artifacts = MODULE.build_artifacts(entries)

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            MODULE.write_artifacts(output_dir, artifacts)

            markdown_path = output_dir / MODULE.CATALOG_FILES["markdown"]
            markdown_path.write_text("drift\n", encoding="utf-8")

            ok, mismatches = MODULE.check_artifacts(output_dir, artifacts)
            self.assertFalse(ok)
            self.assertTrue(any("outdated file" in msg for msg in mismatches))


if __name__ == "__main__":
    unittest.main()
