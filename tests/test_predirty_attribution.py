"""Whose change is a path the session found already dirty in its tree.

`session start` records the tree it opens on (`dirty_at_start`) because a diff
from `start_head` cannot separate two sessions' work: the file was already there,
and the only commit that touches it is the one the *current* session makes when
it preserves earlier sessions' evidence. Session 2026-10-21-003 did exactly
that — 6 236 files from seven closed sessions — and `session finish` reported
every one as work it had failed to declare, twice, for so long that both runs
were killed before the session could close (D305).

Three directions are asserted here.

* The repair: a file left behind before `session.start` is excluded from
  `unlogged`, and the exclusion is *visible* — one `note` counts it, so silence
  is never the mechanism.
* The boundary: a file written after `session.start` is still reported. A rule
  that excluded "whatever was dirty" by asking the current tree would swallow
  this session's own work along with the previous one.
* The legacy shape: sessions started before `--untracked-files=all` recorded
  `?? dir/`, a directory collapsed to one line. It is a prefix, and its ceiling
  — files created inside that directory after start are excluded too — is pinned
  here rather than left to be discovered by whoever meets it.
"""

from __future__ import annotations

import subprocess
import unittest

from harness import RepoTest

from originlib import predirty, session


class ExcludesWhatTheSessionFoundTest(RepoTest):
    def test_a_file_left_by_an_earlier_session_is_not_reported(self) -> None:
        self.write("left-behind.txt", "written before this session opened\n")
        active = session.start("attribution", agent="tester")
        result = session.finish("worked", "ok", "none")
        self.assertEqual(result["unlogged"], [])
        self.assertEqual(result["preexisting"], ["left-behind.txt"])
        self.assertNotIn(
            "left-behind.txt",
            [e["data"]["path"] for e in self.session_events(active.session)
             if e["kind"] == "unlogged_change"],
        )

    def test_the_exclusion_is_recorded_as_one_note(self) -> None:
        self.write("left-behind.txt", "written before this session opened\n")
        active = session.start("attribution", agent="tester")
        session.finish("worked", "ok", "none")
        notes = [e for e in self.session_events(active.session) if e["kind"] == "note"]
        self.assertEqual(len(notes), 1, notes)
        self.assertEqual(notes[0]["data"]["count"], 1)
        self.assertEqual(notes[0]["data"]["action"], "excluded-untracked-at-start")

    def test_a_file_written_after_the_start_is_still_reported(self) -> None:
        self.write("left-behind.txt", "written before this session opened\n")
        session.start("attribution", agent="tester")
        self.write("this-session.txt", "written after it opened\n")
        result = session.finish("worked", "ok", "none")
        self.assertEqual(result["unlogged"], ["this-session.txt"])
        self.assertEqual(result["preexisting"], ["left-behind.txt"])

    def test_capture_is_per_file_so_a_new_directory_is_not_preexisting(self) -> None:
        # The start event must name files, not `dir/`: a directory entry cannot
        # be told apart from files created after the session opened.
        self.write("left-behind.txt", "written before this session opened\n")
        active = session.start("attribution", agent="tester")
        lines = predirty.start_lines(active)
        exact, prefixes = predirty.load(active)
        self.assertTrue(any(line.endswith("left-behind.txt") for line in lines), lines)
        self.assertEqual(prefixes, [])
        self.assertTrue(predirty.is_untracked_at_start("left-behind.txt", exact, prefixes))
        # A directory that did not exist at start is not, and neither is a file
        # written into it afterwards.
        self.write("new-dir/inside.txt", "untracked\n")
        self.assertFalse(predirty.is_untracked_at_start("new-dir/inside.txt", exact, prefixes))

    def test_a_tracked_file_already_modified_at_start_is_still_reported(self) -> None:
        # The rule stops at untracked paths. A command run outside any session is
        # exactly the change `finish` exists to surface, so a tracked file
        # modified before start stays reported (`test_task_rewrite` pins the CLI
        # end to end).
        self.write("tracked.txt", "committed version\n")
        subprocess.run(["git", "add", "-A"], cwd=str(self.repo), check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "add a tracked file"], cwd=str(self.repo),
                       check=True, capture_output=True)
        self.write("tracked.txt", "modified before this session opened\n")
        session.start("attribution", agent="tester")
        result = session.finish("worked", "ok", "none")
        self.assertEqual(result["unlogged"], ["tracked.txt"])
        self.assertEqual(result["preexisting"], [])


class LegacyDirectoryEntryTest(unittest.TestCase):
    """The shape sessions started before `--untracked-files=all` recorded."""

    def test_a_collapsed_directory_is_a_prefix_not_a_path(self) -> None:
        path = predirty.split_line("?? EXPERIMENTS/E202-cli-tool-7030-entry/")
        self.assertTrue(path.endswith("/"), path)
        self.assertTrue(
            predirty.is_untracked_at_start(
                "EXPERIMENTS/E202-cli-tool-7030-entry/raw/recip_7A21_p19.json",
                set(), [path],
            )
        )

    def test_the_ceiling_files_created_inside_that_directory_are_excluded(self) -> None:
        # Pinned deliberately: this is the price of the legacy shape, and the
        # reason the capture is per-file now. A session that starts on a
        # collapsed directory and writes into it afterwards is not told.
        prefixes = ["EXPERIMENTS/0NN-left-over/"]
        self.assertTrue(
            predirty.is_untracked_at_start(
                "EXPERIMENTS/0NN-left-over/written-later.txt", set(), prefixes
            )
        )
        # Outside every collapsed directory the rule does not reach.
        self.assertFalse(
            predirty.is_untracked_at_start("EXPERIMENTS/E211-entry-survival/run.py",
                                    set(), prefixes)
        )

    def test_a_status_line_is_split_on_the_status_columns_only(self) -> None:
        self.assertEqual(predirty.split_line(" M STATE.md"), "STATE.md")
        self.assertEqual(predirty.split_line("?? STATE.md"), "STATE.md")
        # An untracked file whose *name* starts with something status-shaped.
        self.assertEqual(predirty.split_line("??  M notes.txt"), " M notes.txt")
        self.assertEqual(predirty.split_line("R  old.md -> new.md"), "new.md")


if __name__ == "__main__":
    unittest.main()
