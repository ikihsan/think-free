#!/usr/bin/env python3
"""`git check-ignore`'s exit code is not "is ignored", and this repository has
a rule that depends on it.

`tools/originlib/gitutil.is_ignored` decided whether a path was gitignored by
`git check-ignore --quiet` and comparing the exit code to 0. **git exits 0 for a
path whose last matching pattern is a *negation***, exactly as it does for a
genuinely ignored path. This repository's `.gitignore` ends its raw-data block
with `EXPERIMENTS/*/raw/**` and then re-includes `*.json`, `*.jsonl`, `*.csv`,
`*.tsv` — so every experiment's raw capture matched a rule and none of them was
ignored, while `is_ignored` reported all of them ignored.

The consequence is not cosmetic. `session artifact --dir EXPERIMENTS/nnn-…/`
prints "skipped (gitignored)" for those paths, so the session record never
declares an experiment's raw evidence — the same shape as F142, where material
sat on disk that the record did not account for.

Three directions, all against the real repository:

* the defect: a negated path reads as ignored (asserted on a path this
  repository's own `.gitignore` re-includes, not on a fixture)
* the repair: a genuinely ignored path still reads as ignored, so the rule that
  keeps build output out of the record is not weakened
* the boundary: a path no rule matches reads as not ignored, which is what git
  actually does with it

Run: `python3 tests/test_check_ignore_negation.py` (or via unittest discover)
"""

from __future__ import annotations

import unittest
from pathlib import Path

from originlib import gitutil, paths


class CheckIgnoreNegationTest(unittest.TestCase):
    """The real repository: the rules under test are this repository's own."""

    def root(self) -> Path:
        root = Path(paths.repo_root())
        if root != Path(__file__).resolve().parent.parent:
            self.skipTest("running against a fixture repository, not the real one")
        return root

    def setUp(self) -> None:
        self.root()
        self.rules = (self.root() / ".gitignore").read_text().splitlines()

    def negated_raw_pattern_exists(self) -> str:
        for line in self.rules:
            if line.startswith("!EXPERIMENTS/*/raw/"):
                return line
        self.fail(".gitignore no longer re-includes any EXPERIMENTS/*/raw/ path")

    # A filename no later, unanchored rule in .gitignore overrides. This
    # repository carries bare names (`results.json`, ...) that re-ignore a raw
    # capture *after* the negation block, which is a different case again.
    SAMPLE = "EXPERIMENTS/000-capability/raw/capture.json"

    def test_a_negated_raw_capture_is_not_ignored(self) -> None:
        """The defect: `EXPERIMENTS/*/raw/*.json` is negated, so not ignored."""
        pattern = self.negated_raw_pattern_exists()
        path = self.SAMPLE
        self.assertFalse(
            gitutil.is_ignored(path),
            "%s re-includes %s, so git tracks it and the check must say so"
            % (pattern, path),
        )

    def test_a_genuinely_ignored_path_is_still_ignored(self) -> None:
        """.origin/ is ignored outright; the repair must not weaken that rule."""
        self.assertTrue(
            any(line.strip() == ".origin/" for line in self.rules),
            ".gitignore no longer ignores .origin/, so this test is vacuous",
        )
        self.assertTrue(gitutil.is_ignored(".origin/doctor.json"))

    def test_a_path_no_rule_matches_is_not_ignored(self) -> None:
        self.assertFalse(gitutil.is_ignored("EXPERIMENTS/000-capability/capture.py"))

    def test_the_naive_exit_code_rule_would_be_wrong(self) -> None:
        """Pin the bug, so a refactor back to `--quiet` fails here, not silently."""
        raw = gitutil.run(["check-ignore", "--quiet", "--", self.SAMPLE])
        self.assertEqual(
            raw.returncode, 0,
            "git no longer exits 0 for a negated path, so this fixture no longer "
            "demonstrates the defect and the test above is proving less than it "
            "claims",
        )
        self.assertFalse(gitutil.is_ignored(self.SAMPLE))


if __name__ == "__main__":
    unittest.main()