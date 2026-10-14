"""E130 — preflight adapter prototype on third harness formats.

Tests that preflight.concordance works correctly across three harness formats:
1. Single JSONL (adapters/jsonl_adapter.py) — 4 adapter lines
2. CSV with header (adapters/csv_adapter.py) — 3 adapter lines
3. SILENT_NO_MATCH when no shared identifier field exists

See RESULT.md for full experiment record.
"""

import unittest
import sys
import os

# Add the adapters module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from preflight import concordance
from preflight.report import render


class TestJsonLAdapter(unittest.TestCase):
    """JSONL format: each line is {"id": "...", "prediction": "...", "answer": "..."}."""

    def test_concordance_ok(self):
        from adapters.jsonl_adapter import adapt_jsonl

        key_rows, out_rows = adapt_jsonl(
            os.path.join(os.path.dirname(__file__), '..', 'test-harness', 'output.jsonl')
        )
        c1 = concordance(key_rows, out_rows)
        text, code = render([c1], rate="(not computed)")
        self.assertEqual(c1["verdict"], "OK")
        self.assertEqual(c1["best_rate"], 1.0)
        self.assertIn("20/20", c1["summary"])


class TestCsvAdapter(unittest.TestCase):
    """CSV format with header ``id,prediction,answer``."""

    def test_concordance_ok(self):
        from adapters.csv_adapter import adapt_csv

        key_rows, out_rows = adapt_csv(
            os.path.join(os.path.dirname(__file__), '..', 'test-harness', 'output.csv')
        )
        c1 = concordance(key_rows, out_rows)
        text, code = render([c1], rate="(not computed)")
        self.assertEqual(c1["verdict"], "OK")
        self.assertEqual(c1["best_rate"], 1.0)
        # CSV has 10 data rows (header + 10 samples)
        self.assertIn("10/10", c1["summary"])


class TestNoSharedIdentifier(unittest.TestCase):
    """When key_rows and out_rows have no shared identifier field,
    concordance should fire SILENT_NO_MATCH."""

    def test_silent_no_match(self):
        # key_rows with "code" field, out_rows with "model_output" field — no shared id
        key_rows = [{"code": "abc123"}, {"code": "def456"}]
        out_rows = [{"model_output": "some prediction"}, {"model_output": "another prediction"}]

        c1 = concordance(key_rows, out_rows)
        self.assertEqual(c1["verdict"], "SILENT_NO_MATCH")
        # The reason should mention no shared field name
        self.assertIn("no field name", c1.get("reason", "").lower())


class TestTypeConflict(unittest.TestCase):
    """When shared field holds different types on key vs output side,
    concordance should report type conflicts."""

    def test_type_conflict_reported(self):
        key_rows = [{"id": 1}, {"id": 2}]  # actual ints
        out_rows = [{"id": "1"}, {"id": "2"}]  # strings

        c1 = concordance(key_rows, out_rows)
        # Should report type conflicts
        self.assertTrue(
            c1.get("type_conflicts") is not None or c1["verdict"] != "OK"
        )


if __name__ == "__main__":
    unittest.main()