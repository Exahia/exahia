.PHONY: geo-oss-catalog geo-oss-catalog-check test-oss-catalog test-llms-txt-linter

geo-oss-catalog:
	python3 tools/oss-catalog/generate_catalog.py

geo-oss-catalog-check:
	python3 tools/oss-catalog/generate_catalog.py --check

test-oss-catalog:
	python3 -m unittest discover -s tools/oss-catalog/tests -p "test_*.py"

test-llms-txt-linter:
	python3 -m unittest discover -s tools/llms-txt-linter/tests -p "test_*.py"
