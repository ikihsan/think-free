"""The exercised-git-versions record is valid, pointed at by the docs, and can fail.

The Python record this mirrors (`test_pythonversions.py`) checks honesty clauses
rather than a schema alone, because a schema check passes just as happily on a
record that lies. Two clauses were added in T-0034 after the same class of defect
hit this file's sibling: the record named two git versions and said nothing about
the rest of the line, and a test asserted that the git on whichever machine ran
the suite was one of them — so every CI run was red, because the runner ships a
git this record did not name (`FAILURES.md` F019). An unexercised list that is
non-empty, and a scope on every entry, are what make that gap nameable.
"""

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
            # A version that ran an older suite is not evidence about this one,
            # so the count is part of the entry rather than a matter of taste.
            self.assertRegex(entry["scope"], r"\d+ tests", entry)

    def test_the_unexercised_ranges_are_named(self) -> None:
        # The clause whose absence cost two hours of red CI (F019). An empty list
        # reads as "the fleet is complete", and two entries with no gaps between
        # them read as a claim about a line nobody measured.
        record = json.loads((repo_root() / "tests" / "git-versions.json").read_text())
        gaps = record.get("not_exercised")
        self.assertIsInstance(gaps, list)
        self.assertTrue(gaps, "an unexercised list that is empty says the fleet is complete")
        for gap in gaps:
            self.assertTrue(gap.get("range"))
            self.assertTrue(gap.get("why"))
            self.assertTrue(gap.get("consequence"))

    def test_a_recorded_version_says_which_machine_it_ran_on(self) -> None:
        # `doctor` prints this field, so an entry without it produces a report
        # that says `exercised` and cannot say where.
        for entry in json.loads(
            (repo_root() / "tests" / "git-versions.json").read_text()
        )["verified"]:
            self.assertTrue(entry.get("where"), entry)

    def test_docs_point_at_the_record(self):
        root = repo_root()
        readme = (root / "tests" / "README.md").read_text()
        self.assertIn("git-versions.json", readme)
        ci = (root / "docs" / "operations" / "ci.md").read_text()
        self.assertIn("git-versions.json", ci)


if __name__ == "__main__":
    unittest.main()
