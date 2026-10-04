"""The exercised-Python record is valid, pointed at by the docs, and can fail.

The git record this mirrors (`test_gitversions.py`) checks a schema and two
mentions. That is the minimum; this adds the clauses that keep the record
honest rather than merely well-formed: a version without a scope, a floor that
claims more than an entry supports, and a "not exercised" list that is silent
about the versions nobody has run are all ways this file could become a lie that
still parses.
"""

from __future__ import annotations

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


MINOR = re.compile(r"^3\.(\d+)(?:\.\d+)?$")


def minor_of(version: str) -> str:
    """`3.8.10` and `3.8` reduce to the same `3.8` for comparison."""
    match = MINOR.match(version)
    if not match:
        raise AssertionError(f"not a 3.x version: {version!r}")
    return f"3.{match.group(1)}"
DOCS = (
    "docs/operations/vm-execution.md",
    "docs/operations/ci.md",
    "tests/README.md",
)


def load() -> dict:
    return json.loads((repo_root() / "tests" / "python-versions.json").read_text())


class PythonVersionsRecordTest(unittest.TestCase):
    def test_schema_and_entries(self) -> None:
        record = load()
        self.assertEqual(record.get("schema"), "origin.python-versions/1")
        self.assertTrue(record.get("updated"), "record must carry an update date")
        verified = record.get("verified")
        self.assertIsInstance(verified, list)
        self.assertTrue(verified, "verified list must not be empty")
        seen = set()
        for entry in verified:
            self.assertRegex(entry["python"], r"^3\.\d+(\.\d+)?$")
            self.assertTrue(entry.get("scope"), f"{entry} must say how much it ran")
            self.assertTrue(entry.get("via"), entry)
            self.assertNotIn(entry["python"], seen, "duplicate version entry")
            seen.add(entry["python"])

    def test_the_floor_is_supported_by_an_entry(self) -> None:
        # A floor is a claim about the oldest minor version that works. If no
        # entry ran that minor version, the floor is a hope, which is what
        # T-0023 corrected. Compared by minor version on purpose: a claim of
        # "3.8" is supported by having run 3.8.10, and insisting on a patch-level
        # match would reject the honest form of the claim.
        floor = load()["floor"]
        claimed = floor["claim"].split()[0]
        self.assertIn(
            minor_of(claimed),
            [minor_of(entry["python"]) for entry in load()["verified"]],
            f"floor claims {claimed} but no entry recorded running that minor version",
        )
        self.assertTrue(floor.get("not_claimed"), "a floor must state what it does not cover")

    def test_unexercised_ranges_are_named(self) -> None:
        record = load()
        gaps = record.get("not_exercised")
        self.assertIsInstance(gaps, list)
        self.assertTrue(gaps, "an unexercised list that is empty says the fleet is complete")
        for gap in gaps:
            self.assertTrue(gap.get("range"))
            self.assertTrue(gap.get("why"))
            self.assertTrue(gap.get("consequence"))

    def test_ci_is_not_claimed_from_a_log_nobody_can_read(self) -> None:
        # The run log needs repository admin rights, so the CI entry may only
        # claim the minor version the workflow pins. If a future entry claims a
        # patch version, it has to say where that number came from.
        for entry in load()["verified"]:
            if "CI" not in entry.get("where", ""):
                continue
            self.assertIn("minor version only", entry["scope"], entry)
            self.assertIn(entry["python"], {"3.12"}, entry)

    def test_docs_point_at_the_record(self) -> None:
        root = repo_root()
        for relative in DOCS:
            self.assertIn(
                "python-versions.json",
                (root / relative).read_text(),
                f"{relative} must point at the record, or a VM reads the floor as prose",
            )

    def test_no_document_still_calls_the_record_unclaimed(self) -> None:
        # The gap statement this task closed. A document that still says the
        # work is unclaimed makes the next agent redo it.
        text = (repo_root() / "docs/operations/vm-execution.md").read_text()
        self.assertNotIn("closing it\nhere is unclaimed work", text)


if __name__ == "__main__":
    unittest.main()