"""The exercised-git-versions record is valid and pointed at by the docs."""

import json
import re
import unittest
from pathlib import Path


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parent.parents]:
        if (parent / "tasks").is_dir() and (parent / "tools").is_dir():
            return parent
    raise AssertionError("could not locate the repository root")


VERSION = re.compile(r"^\d+\.\d+(\.\d+)?$")


class GitVersionsRecordTest(unittest.TestCase):
    def test_schema_and_entries(self):
        record = json.loads((repo_root() / "tests" / "git-versions.json").read_text())
        self.assertEqual(record.get("schema"), "origin.git-versions/1")
        self.assertTrue(record.get("updated"), "record must carry an update date")
        verified = record.get("verified")
        self.assertIsInstance(verified, list)
        self.assertTrue(verified, "verified list must not be empty")
        seen = set()
        for entry in verified:
            self.assertTrue(VERSION.match(entry["git"]), entry)
            self.assertTrue(entry.get("scope"), entry)
            self.assertTrue(entry.get("via"), entry)
            self.assertNotIn(entry["git"], seen, "duplicate version entry")
            seen.add(entry["git"])

    def test_docs_point_at_the_record(self):
        root = repo_root()
        readme = (root / "tests" / "README.md").read_text()
        self.assertIn("git-versions.json", readme)
        ci = (root / "docs" / "operations" / "ci.md").read_text()
        self.assertIn("git-versions.json", ci)


if __name__ == "__main__":
    unittest.main()
