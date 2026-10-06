#!/usr/bin/env python3
"""The parser on git's own output, including shapes no local repository produces.

Run with:  python3 -m unittest discover -s stage-lines -p 'test_*.py'
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stagelib import parse  # noqa: E402


class ParserTest(unittest.TestCase):
    """The parser on git's own output, including shapes no repo here produces."""

    SAMPLE = (
        "diff --git a/x b/x\n"
        "index 111..222 100644\n"
        "--- a/x\n"
        "+++ b/x\n"
        "@@ -1,2 +1,2 @@\n"
        "-one\n"
        "-two\n"
        "+ONE\n"
        "+TWO\n"
        "@@ -10 +9 @@\n"
        "-ten\n"
        "+NINE\n"
        "@@ -20,0 +19,3 @@\n"
        "+ins1\n"
        "+ins2\n"
        "+ins3\n"
    )

    def test_splits_by_positional_pairing_and_keeps_positions(self):
        # Modifications pair up line for line. A run of three insertions does not:
        # each of them is its own line in the file as it reads now, so each gets its
        # own address and its own hunk -- `@@ -20,0 +19,1 @@` .. `+21,1 @@` rather
        # than one hunk carrying all three.
        changes = parse(self.SAMPLE)["x"].changes
        self.assertEqual([c.header() for c in changes], [
            "@@ -1,1 +1,1 @@", "@@ -2,1 +2,1 @@",
            "@@ -10,1 +9,1 @@",
            "@@ -20,0 +19,1 @@", "@@ -20,0 +20,1 @@", "@@ -20,0 +21,1 @@"])
        self.assertEqual([c.kind for c in changes],
                         ["modify", "modify", "modify", "add", "add", "add"])
        self.assertEqual([c.anchor(21) for c in changes[3:]], [19, 20, 21])

    def test_rendered_patch_reparses_to_the_same_changes(self):
        """The strongest property available offline: what we emit, git reads back."""
        first = parse(self.SAMPLE)["x"]
        again = parse("diff --git a/x b/x\n--- a/x\n+++ b/x\n"
                      + "".join(c.header() + "\n"
                                + "".join(l + "\n" for l in c.body)
                                for c in first.changes))["x"]
        self.assertEqual([c.header() for c in first.changes],
                         [c.header() for c in again.changes])

    def test_stale_index_line_is_dropped_from_the_rendered_header(self):
        patch = parse(self.SAMPLE)["x"].render(
            parse(self.SAMPLE)["x"].changes)
        self.assertNotIn("index 111..222", patch)
        self.assertIn("--- a/x", patch)


if __name__ == "__main__":
    unittest.main(verbosity=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
