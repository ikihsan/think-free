#!/usr/bin/env python3
"""stg against real git repositories: every assertion is made on real git state.
No mocks. The claim this tool makes is that the index it leaves behind is a real
index git will commit, so nothing here asserts on a model of git.
Run with:  python3 -m unittest discover -s stage-lines -p 'test_*.py'
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tests_support import STG, Repo, git, run  # noqa: E402,F401
class StageTest(unittest.TestCase):
    def setUp(self):
        self.r = Repo()
        self.addCleanup(self.r.cleanup)
    # ---------------------------------------------------------------- basics
    def test_single_line_modify_stages_only_that_line(self):
        self.r.write("f", "a\nb\nc\nd\ne\n")
        self.r.commit()
        self.r.write("f", "A\nb\nc\nD\ne\n")
        p = self.r.stg("stage", "f:1")
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertEqual(self.r.staged_body("f"), "".join([
            "diff --git a/f b/f\n",
            "--- a/f\n", "+++ b/f\n",
            "@@ -1 +1 @@\n", "-a\n", "+A\n"]))
    def test_staging_a_line_leaves_the_others_unstaged(self):
        self.r.write("f", "a\nb\nc\n")
        self.r.commit()
        self.r.write("f", "A\nB\nC\n")
        self.r.stg("stage", "f:2")
        self.assertEqual(self.r.unstaged_hunks("f"),
                         ["@@ -1 +1 @@", "@@ -3 +3 @@"])
    def test_range_selects_several_changes(self):
        self.r.write("f", "a\nb\nc\nd\ne\nf\ng\n")
        self.r.commit()
        self.r.write("f", "A\nb\nC\nD\ne\nF\ng\n")
        self.r.stg("stage", "f:1-4")
        # lines 1, 3 and 4 are staged; F is still unstaged, and in the
        # index-to-worktree diff F sits at line 6 of the working tree
        # git merges the two adjacent staged lines back into one hunk when it
        # displays the index, so two hunks is the right expectation
        self.assertEqual(self.r.hunks("f", cached=True),
                         ["@@ -1 +1 @@", "@@ -3,2 +3,2 @@"])
        self.assertEqual(self.r.unstaged_hunks("f"), ["@@ -6 +6 @@"])
    def test_multiple_files_in_one_call(self):
        for n in "12":
            self.r.write(n, "a\nb\n")
        self.r.commit()
        for n in "12":
            self.r.write(n, "A\nb\n")
        p = self.r.stg("stage", "1:1,2:1")
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertIn("stage 1:1", p.stdout)
        self.assertIn("stage 2:1", p.stdout)
        self.assertEqual(self.r.unstaged_hunks(), [])
    def test_whole_file_when_no_range_given(self):
        self.r.write("f", "a\nb\n")
        self.r.commit()
        self.r.write("f", "A\nB\n")
        self.r.stg("stage", "f:")
        self.assertEqual(self.r.unstaged_hunks(), [])
    # ------------------------------------------------------------ the splits
    def test_adjacent_modified_lines_split_per_line(self):
        # git emits one hunk for lines 1-2; each must be stageable alone
        self.r.write("f", "a\nb\nc\n")
        self.r.commit()
        self.r.write("f", "A\nB\nc\n")
        self.r.stg("stage", "f:1")
        self.assertEqual(self.r.staged_body("f"), "".join([
            "diff --git a/f b/f\n", "--- a/f\n", "+++ b/f\n",
            "@@ -1 +1 @@\n", "-a\n", "+A\n"]))
        self.assertEqual(self.r.unstaged_hunks("f"), ["@@ -2 +2 @@"])
    def test_a_multi_line_insertion_splits_per_line(self):
        # Two inserted lines are two changes to a reader, and git apply takes each
        # on its own: `@@ -1,0 +2,1 @@` then `@@ -1,0 +3,1 @@`. An earlier version
        # of this file asserted the opposite -- "there is no valid hunk for half of
        # a two-line insertion" -- and that premise was wrong; verified against git
        # in EXPERIMENTS/038-staging-prior-art (F063).
        self.r.write("f", "a\n")
        self.r.commit()
        self.r.write("f", "a\nh1\nh2\n")
        rows = json.loads(self.r.stg("list", "--json").stdout)
        changes = [r["change"] for r in rows if r.get("change")]
        self.assertEqual(len(changes), 2)
        self.assertEqual([c["anchor"] for c in changes], [2, 3])
        self.assertEqual([c["added"] for c in changes], [1, 1])
    def test_staging_one_line_of_a_two_line_insertion_stages_one_line(self):
        self.r.write("f", "a\n")
        self.r.commit()
        self.r.write("f", "a\nh1\nh2\n")
        self.r.stg("stage", "f:2")
        self.assertEqual(self.r.staged_body("f"), "".join([
            "diff --git a/f b/f\n", "--- a/f\n", "+++ b/f\n",
            "@@ -1,0 +2 @@\n", "+h1\n"]))
        self.assertEqual(self.r.unstaged_hunks("f"), ["@@ -2,0 +3 @@"])
    def test_a_multi_line_deletion_stays_one_change(self):
        # Two consecutive deletions share an address: both are named by the line
        # whose content moved up into the gap, so no coordinate selects one of them
        # alone. Splitting the run would not add reach, only make `stg list` longer.
        self.r.write("f", "a\nb\nc\nd\n")
        self.r.commit()
        self.r.write("f", "a\nd\n")
        rows = json.loads(self.r.stg("list", "--json").stdout)
        changes = [r["change"] for r in rows if r.get("change")]
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]["removed"], 2)
    def test_a_two_line_deletion_is_staged_whole_at_its_one_address(self):
        self.r.write("f", "a\nb\nc\nd\n")
        self.r.commit()
        self.r.write("f", "a\nd\n")
        self.r.stg("stage", "f:2")
        self.assertEqual(self.r.staged_file_content("f"), "a\nd\n")
    def test_one_removal_beside_two_additions_splits(self):
        # "-a +a2 +b2": the a->a2 edit is separable, the extra add is not
        self.r.write("f", "x\na\ny\n")
        self.r.commit()
        self.r.write("f", "x\na2\ny\nb2\n")
        self.r.stg("stage", "f:2")
        self.assertEqual(self.r.staged_body("f"), "".join([
            "diff --git a/f b/f\n", "--- a/f\n", "+++ b/f\n",
            "@@ -2 +2 @@\n", "-a\n", "+a2\n"]))
        self.assertEqual(self.r.unstaged_hunks("f"), ["@@ -3,0 +4 @@"])
    # ------------------------------------------------------------- deletions
    def test_deletion_is_anchored_on_the_line_that_took_its_place(self):
        self.r.write("f", "l1\nl2\nl3\nl4\n")
        self.r.commit()
        self.r.write("f", "l1\nl4\n")
        # l3 was deleted, so l4 moved up to line 2 -- that is the addressable line
        p = self.r.stg("list")
        self.assertIn("f:2\tdelete", p.stdout)
        self.r.stg("stage", "f:2")
        self.assertIn("-l3", self.r.staged_body("f"))
    def test_deletion_at_end_of_file_anchors_on_the_last_line(self):
        self.r.write("f", "a\nb\nc\n")
        self.r.commit()
        self.r.write("f", "a\nb\n")
        p = self.r.stg("list")
        self.assertIn("f:2\tdelete", p.stdout)
    def test_deletion_at_top_of_file_anchors_on_line_one(self):
        self.r.write("f", "a\nb\nc\n")
        self.r.commit()
        self.r.write("f", "c\n")
        p = self.r.stg("list")
        self.assertIn("f:1\tdelete", p.stdout)
    # --------------------------------------------------------- awkward files
    def test_file_without_trailing_newline(self):
        self.r.write("f", "no-newline")
        self.r.commit()
        self.r.write("f", "no-newline-CHANGED")
        self.r.stg("stage", "f:1")
        self.assertIn("\\ No newline at end of file", self.r.staged_body("f"))
        self.assertEqual(self.r.unstaged_hunks(), [])
    def test_crlf_file(self):
        self.r.write("f", "r1\r\nr2\r\nr3\r\n")
        self.r.commit()
        self.r.write("f", "r1\r\nr2-EDIT\r\nr3\r\n")
        self.r.stg("stage", "f:2")
        self.assertIn("r2-EDIT", self.r.staged_body("f"))
    def test_binary_file_is_refused_with_a_usable_message(self):
        with open(os.path.join(self.r.dir, "bin"), "wb") as fh:
            fh.write(b"\x00\x01\x02\x03")
        self.r.commit()
        with open(os.path.join(self.r.dir, "bin"), "wb") as fh:
            fh.write(b"\x00\x01\x02\x04\x05")
        p = self.r.stg("stage", "bin:1")
        self.assertEqual(p.returncode, 2)
        self.assertIn("binary", p.stderr)
    def test_tabs_and_long_lines_are_handled(self):
        self.r.write("f", "a\n\tb\n" + "x" * 500 + "\n")
        self.r.commit()
        self.r.write("f", "a\n\tB\n" + "y" * 500 + "\n")
        self.r.stg("stage", "f:2")
        self.assertIn("+", self.r.staged_body("f"))
    # -------------------------------------------------------------- unstage
    def test_unstage_is_addressed_by_index_line(self):
        self.r.write("f", "a\nb\nc\nd\n")
        self.r.commit()
        self.r.write("f", "A\nB\nc\nD\n")
        self.r.stg("stage", "f:1,2,4")
        # lines 1 and 2 are adjacent, so git shows them as one hunk in the index
        self.assertEqual(len(self.r.hunks("f", cached=True)), 2)
        self.r.stg("unstage", "f:2")
        self.assertNotIn("B", self.r.staged_body("f"))
        self.assertIn("+B", self.r.staged_body("f") and git(["diff", "-U0", "--", "f"], self.r.dir))
    def test_stage_then_unstage_round_trips_to_an_empty_index(self):
        self.r.write("f", "a\nb\nc\nd\ne\n")
        self.r.commit()
        self.r.write("f", "A\nb\nC\nd\nE\n")
        for spec in ("f:1", "f:3", "f:5"):
            self.assertEqual(self.r.stg("stage", spec).returncode, 1)
        # staging the whole file again has nothing left to do, and says so
        # rather than reporting success
        again = self.r.stg("stage", "f:")
        self.assertEqual(again.returncode, 2)
        self.assertEqual(len(self.r.hunks("f", cached=True)), 3)
        self.assertEqual(self.r.stg("unstage", "f:").returncode, 1)
        # the index is back to HEAD, so everything is unstaged again
        self.assertEqual(self.r.staged_body("f"), "")
        self.assertEqual(self.r.unstaged_hunks(),
                         ["@@ -1 +1 @@", "@@ -3 +3 @@", "@@ -5 +5 @@"])
        self.assertEqual(git(["status", "--porcelain"], self.r.dir), " M f\n")
    # ----------------------------------------------------------------- list
    def test_list_reports_untracked_files(self):
        self.r.write("f", "a\n")
        self.r.commit()
        self.r.write("newfile", "hello\n")
        self.assertIn("newfile\t(new file", self.r.stg("list").stdout)
    def test_list_is_empty_and_exits_zero_on_a_clean_tree(self):
        self.r.write("f", "a\n")
        self.r.commit()
        p = self.r.stg("list")
        self.assertEqual(p.returncode, 0)
        self.assertEqual(p.stdout, "")
    def test_json_list_is_parseable_and_self_describing(self):
        self.r.write("f", "a\nb\nc\n")
        self.r.commit()
        self.r.write("f", "A\nb\nC\n")
        rows = json.loads(self.r.stg("list", "--json").stdout)
        self.assertEqual([r["change"]["anchor"] for r in rows], [1, 3])
        self.assertEqual([r["change"]["kind"] for r in rows],
                         ["modify", "modify"])
    # --------------------------------------------------------------- errors
    def test_line_past_the_end_of_the_file_is_refused_with_the_length(self):
        self.r.write("f", "a\nb\n")
        self.r.commit()
        self.r.write("f", "A\nb\n")
        p = self.r.stg("stage", "f:40")
        self.assertEqual(p.returncode, 2)
        self.assertIn("has 2 lines", p.stderr)
    def test_unchanged_line_is_refused(self):
        self.r.write("f", "a\nb\nc\n")
        self.r.commit()
        self.r.write("f", "A\nb\nc\n")
        p = self.r.stg("stage", "f:2")
        self.assertEqual(p.returncode, 2)
        self.assertIn("no stage change matches", p.stderr)
    def test_file_with_no_change_is_refused(self):
        self.r.write("f", "a\n")
        self.r.commit()
        p = self.r.stg("stage", "f:1")
        self.assertEqual(p.returncode, 2)
    def test_outside_a_repository_is_refused(self):
        d = tempfile.mkdtemp(prefix="stg-norepo-")
        self.addCleanup(shutil.rmtree, d, True)
        p = run([sys.executable, STG, "list"], d)
        self.assertEqual(p.returncode, 2)
        self.assertIn("not inside a git repository", p.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
