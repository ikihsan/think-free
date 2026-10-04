"""The defect list is an identifier record, so a repeated number is a collision.

`doc lint` rule 7 read findings, findings index rows and decision spans, and not
the ordered list in `STATE-defects.md`. T-0034 and T-0035 were written on two VMs
in the same hour, both took **defect 7**, and nothing reported it: both copies
reached the shared base (`e53ca23`, `e701ad8`) and the unpushed side renumbered
by hand. This file tests the rule against those two commits' own bytes.

Two shapes of falsification are here on purpose. The fixtures must fire (a rule
that passes against the defect it was written for is worthless), and the controls
must stay silent (a rule that fires on prose, on an indented list, or on a
deliberately out-of-order list would have reddened CI on a correct tree — which
is what an earlier draft of the F/D rule did: 83 of 174 commits, including the
tip). See `test_identifier_enforcement.py` for where the rule has to be read.
"""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

from harness import SOURCE_ROOT, RepoTest

from originlib import defectlist, paths

# Verbatim from e53ca23:STATE-defects.md, lines 75 and 133 — the two entries that
# were both numbered 7. The first is VM 0944's credential-fixture defect, the
# second VM 0947's interpreter defect; the entries sit in different sections
# (`7` under the solved heading, `6` under `## Open`), which is why reading the
# file as one list is the only thing that catches it.
COLLIDING = """\
# Known defects

7. **A test fixture inherited the runner's environment** (solved in T-0035).
   `tests/pushcred_fixture.py` built a sandbox with a fresh `HOME`,

## Open

6. **Identifier allocation collides by construction** (both halves solved:

7. **The suite was red on every interpreter it had never run on** (solved in
   T-0034, F018). `tests/python-versions.json` named 3.9 to 3.11 as versions
"""

# The same two entries as 157e463 left them: the unpushed side renumbered 7 and
# 8 to 8 and 9, which is the standing rule for a collision.
REPAIRED = COLLIDING.replace(
    "7. **The suite was red on every interpreter it had never run on**",
    "8. **The suite was red on every interpreter it had never run on**",
)


class CollisionTest(RepoTest):
    """The bytes of the commit that reached the shared base must be reported."""

    def test_two_defects_with_one_number_are_reported(self) -> None:
        self.write(defectlist.DEFECT_FILE, COLLIDING)
        found = defectlist.report(self.repo)
        self.assertEqual(len(found), 1, found)
        # Both lines, or a reader cannot renumber without searching the file.
        self.assertIn("STATE-defects.md:3", found[0])
        self.assertIn("STATE-defects.md:10", found[0])
        self.assertIn("defect 7", found[0])
        self.assertIn("renumber", found[0].lower())

    def test_the_report_carries_both_subjects(self) -> None:
        # Two numbers side by side say nothing about *which* two defects collided,
        # and that is the question the reader has to answer before renumbering.
        self.write(defectlist.DEFECT_FILE, COLLIDING)
        found = defectlist.report(self.repo)[0]
        self.assertIn("A test fixture inherited the runner", found)
        self.assertIn("The suite was red on every interpreter", found)

    def test_the_hand_repair_one_commit_later_is_clean(self) -> None:
        self.write(defectlist.DEFECT_FILE, REPAIRED)
        self.assertEqual(defectlist.report(self.repo), [])

    def test_one_entry_per_number_is_clean(self) -> None:
        self.write(defectlist.DEFECT_FILE, "## Open\n\n6. **One**\n\n8. **Two**\n")
        self.assertEqual(defectlist.report(self.repo), [])


class ControlTest(RepoTest):
    """The shapes that must stay silent, each written because it is plausible."""

    def test_a_prose_mention_is_not_a_definition(self) -> None:
        # `STATE.md` and this file's own prose name defect numbers constantly.
        # Only a numbered list item with a bold subject defines one.
        self.write(
            defectlist.DEFECT_FILE,
            "# Known defects\n\n6. **The real entry**\n\n"
            "The rule about defect 5 and defect 7 lives in D025.\n",
        )
        self.assertEqual(defectlist.report(self.repo), [])

    def test_an_ordinary_numbered_list_is_not_a_definition(self) -> None:
        # A list without bold subjects is a list of steps, and reading it would
        # report every repeated step number in every document the file grows.
        # One real entry is present, so this is about the step list alone: with
        # none at all the "no entry could be read" rule below would fire, and
        # that is deliberate.
        self.write(
            defectlist.DEFECT_FILE,
            "# Known defects\n\n6. **The real entry**\n\n"
            "## How to renumber\n\n1. do this\n2. do that\n",
        )
        self.assertEqual(defectlist.report(self.repo), [])

    def test_an_indented_numbered_item_is_not_a_definition(self) -> None:
        # A sub-list of an entry's prose, indented under it. Three spaces is the
        # continuation indent this file uses, and a nested list would be
        # indistinguishable from a malformed entry if indentation were ignored.
        self.write(
            defectlist.DEFECT_FILE,
            "6. **An entry**\n   1. **Not an entry, a nested step**\n"
            "   2. **Also not an entry**\n",
        )
        self.assertEqual(defectlist.report(self.repo), [])

    def test_out_of_order_numbering_is_not_a_collision(self) -> None:
        # Deliberate: entries land under the heading they belong in when they
        # close, so the solved block is not ascending. A gate that required
        # ascending order would have reddened this repository's own history.
        self.write(defectlist.DEFECT_FILE, "7. **Seven**\n\n## Open\n\n6. **Six**\n\n8. **Eight**\n")
        self.assertEqual(defectlist.report(self.repo), [])

    def test_a_missing_file_is_not_a_collision(self) -> None:
        # The fixture repositories have no defect list, and a rule that reported
        # its absence would fail every test that lints one.
        self.assertFalse((self.repo / defectlist.DEFECT_FILE).exists())
        self.assertEqual(defectlist.report(self.repo), [])

    def test_a_file_with_no_readable_entry_is_reported(self) -> None:
        # The negative case that keeps the rule honest: a restructure into
        # headings leaves a parser matching nothing, which reports nothing, and
        # looks exactly like a clean tree (D025). Only the file that exists is
        # named — a tree with one list file has no second one to complain about.
        self.write(defectlist.DEFECT_FILE, "# Known defects\n\n## Defect 7\n\nProse.\n")
        found = defectlist.report(self.repo)
        self.assertEqual(len(found), 1, found)
        self.assertIn("no defect entry could be read", found[0])
        self.assertIn("STATE-defects.md", found[0])

    def test_a_split_file_with_no_readable_entry_is_also_reported(self) -> None:
        # The same obligation for the second file, in the shape that can happen:
        # after the split, both halves go quiet — the parent loses its bold
        # subjects too — and a list nothing can read from must say so rather
        # than reading as clean. Written this way because a *half* that went
        # quiet while the other still parses is reported by the next rule, not
        # this one; asserting the weaker case would have hidden the stronger.
        self.write(defectlist.DEFECT_FILE, "# Known defects\n\n## Defect 6\n\nProse.\n")
        self.write(defectlist.DEFECT_FILES[1], "# Known defects\n\n## Defect 7\n\nProse.\n")
        found = defectlist.report(self.repo)
        self.assertEqual(len(found), 2, found)
        for name in defectlist.DEFECT_FILES:
            self.assertTrue(
                any(name in str(item) for item in found), f"{name} was not reported"
            )


class SplitFileTest(RepoTest):
    """The list is two files since T-0056, and the rule must read both.

    The split was recorded as impossible without exactly this change — "it cannot
    be done inside its own numbered list without `defectlist.py` reading more
    than one file". So the load-bearing assertion here is the one that would fail
    if the reader had been left reading a single file: a duplicate number
    *spanning* the two halves, which is invisible to a reader of either.
    """

    OTHER = defectlist.DEFECT_FILES[1]

    def test_a_collision_spanning_the_two_files_is_reported(self) -> None:
        self.write(defectlist.DEFECT_FILE, "## Open\n\n7. **In the parent file**\n")
        self.write(self.OTHER, "7. **In the split file**\n")
        found = defectlist.report(self.repo)
        self.assertEqual(len(found), 1, found)
        self.assertIn(defectlist.DEFECT_FILE, found[0])
        self.assertIn(self.OTHER, found[0])
        self.assertIn("defect 7", found[0])

    def test_one_entry_per_number_across_both_files_is_clean(self) -> None:
        self.write(defectlist.DEFECT_FILE, "## Open\n\n6. **Six**\n")
        self.write(self.OTHER, "7. **Seven**\n")
        self.assertEqual(defectlist.report(self.repo), [])

    def test_reading_only_the_parent_would_have_missed_the_collision(self) -> None:
        """The control that proves the second file is load-bearing, not decorative."""
        self.write(defectlist.DEFECT_FILE, "## Open\n\n7. **In the parent file**\n")
        self.write(self.OTHER, "7. **In the split file**\n")
        parent_only = defectlist.entries(
            (self.repo / defectlist.DEFECT_FILE).read_text(encoding="utf-8"),
            defectlist.DEFECT_FILE,
        )
        self.assertEqual(
            defectlist.duplicate_issues(parent_only),
            [],
            "if one file were enough, this collision would not need the second read",
        )
        self.assertEqual(len(defectlist.read_all(self.repo)), 2)

    def test_only_the_parent_present_is_not_reported_as_unreadable(self) -> None:
        # A tree that has not been split yet is a tree with one list file, and
        # the "no entry could be read" rule must not fire on the file's absence.
        self.write(defectlist.DEFECT_FILE, "## Open\n\n6. **Six**\n")
        self.assertFalse((self.repo / self.OTHER).exists())
        self.assertEqual(defectlist.report(self.repo), [])

    def test_the_real_tree_holds_every_number_once_across_both_files(self) -> None:
        # `RepoTest.setUp` points ORIGIN_ROOT at the fixture, so the real tree is
        # read through `SOURCE_ROOT` rather than through `paths.repo_root()` —
        # which is also the lesson of F014: a fixture must not read the machine
        # it is standing in for.
        found = defectlist.read_all(SOURCE_ROOT)
        numbers = [entry.number for entry in found]
        self.assertGreaterEqual(len(numbers), 20, "the list lost entries in the split")
        self.assertEqual(len(numbers), len(set(numbers)), "a number appears in both files")
        sources = {entry.source for entry in found}
        self.assertEqual(sources, set(defectlist.DEFECT_FILES), "one file contributed nothing")


class RealHistoryTest(unittest.TestCase):
    """The rule, against this repository's own commits.

    The two commits that carried defect 7 twice are the whole point of the task,
    and so is the count: a rule that flags more than two of thirteen commits is
    a rule that would have reddened CI on a correct tree. The sweep starts at a
    pinned commit, so the claim is about history rather than about whatever HEAD
    happens to be when the suite runs, and it is skipped where the commits are not
    present rather than passing silently (the F010 shape).
    """

    HEAD = "e576e264"

    def root(self) -> Path:
        root = Path(paths.repo_root())
        if root != Path(__file__).resolve().parent.parent:
            self.skipTest("running against a fixture repository, not the real one")
        return root

    def show(self, commit: str, path: str) -> str | None:
        result = subprocess.run(
            ["git", "show", f"{commit}:{path}"],
            cwd=str(self.root()), capture_output=True, text=True,
        )
        return result.stdout if result.returncode == 0 else None

    def commits_touching(self, path: str) -> list[str]:
        result = subprocess.run(
            ["git", "rev-list", self.HEAD, "--", path],
            cwd=str(self.root()), capture_output=True, text=True, check=True,
        )
        if not result.stdout.strip():
            self.skipTest("history is shallow; the commits under test are not present")
        return result.stdout.split()

    def test_exactly_the_two_colliding_commits_are_flagged(self) -> None:
        flagged = []
        for commit in self.commits_touching(defectlist.DEFECT_FILE):
            text = self.show(commit, defectlist.DEFECT_FILE)
            if text is not None and defectlist.duplicate_issues(defectlist.entries(text)):
                flagged.append(commit[:7])
        self.assertEqual(
            sorted(flagged),
            ["e53ca23", "e701ad8"],
            f"these commits hold a defect number twice: {flagged}",
        )

    def test_the_fixture_quotes_the_commits_it_names(self) -> None:
        # If this stops matching, the fixture above is quoting something other
        # than what the fleet published, and the reason must be found rather than
        # the fixture quietly edited. One repeated number is the collision, not
        # two: two places, one number taken twice.
        for commit, expected in (("e53ca23", 1), ("e701ad8", 1), (self.HEAD, 0)):
            text = self.show(commit, defectlist.DEFECT_FILE)
            if text is None:
                self.skipTest(f"commit {commit} is not present")
            numbers = [entry.number for entry in defectlist.entries(text)]
            repeated = len(numbers) - len(set(numbers))
            self.assertEqual(
                repeated, expected, f"fixture drift at {commit}: {numbers}"
            )

    def test_this_repository_holds_no_repeated_defect_number(self) -> None:
        self.assertEqual(defectlist.report(self.root()), [])


if __name__ == "__main__":
    unittest.main()