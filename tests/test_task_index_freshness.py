"""A created task must be reachable from the index that makes it non-orphan.

Two CI runs failed on 2026-10-03 (`37163434868`, `37163438950`) because this VM
pushed a task file whose generated index had not been rebuilt: `doc lint` rule 4
calls an unlinked document an orphan, and the Documentation lint step exits 2.
The rule is right; the command that creates the document was the thing missing.

These tests pin the sequence rather than the rule: create a task, lint, and the
tree must be clean with no `doc index` in between.
"""

from __future__ import annotations

import unittest

from harness import RepoTest

from originlib import tasks


class TaskIndexFreshnessTest(RepoTest):
    def setUp(self) -> None:
        super().setUp()
        # The fixture ships placeholder documents and no generated indexes, so
        # the baseline is established first: without it every document reads as
        # an orphan and the rule under test is not what is being measured.
        self.write_generated()

    def committed_index(self) -> str:
        return (self.repo / "tasks" / "INDEX.md").read_text(encoding="utf-8")

    def test_a_new_task_leaves_no_orphan_behind(self) -> None:
        # The whole defect in one call: create, then lint, with nothing between.
        self.assertEqual(self.cli("task", "new", "--goal", "reachable at once", "--verify", "true"), 0)
        result = self.cli("doc", "lint")
        self.assertEqual(result, 0, self.output())

    def test_the_index_on_disk_matches_the_generator_after_create(self) -> None:
        self.cli("task", "new", "--goal", "index bytes", "--verify", "true")
        self.assertEqual(self.committed_index(), tasks.render_tasks_index())

    def test_claiming_and_completing_keep_the_index_current(self) -> None:
        # Both change a row in the same table; a stale row would misreport who
        # holds the task to the next VM that reads the index.
        self.cli("task", "new", "--goal", "rows move", "--verify", "true")
        self.cli("task", "claim", "T-0001", "--agent", "agent-a", "--vm", "vm-a", "--no-push")
        self.assertIn("agent-a", self.committed_index())
        self.cli("task", "complete", "T-0001", "--summary", "done")
        self.assertIn("done", self.committed_index())
        self.assertEqual(self.committed_index(), tasks.render_tasks_index())
        self.assertEqual(self.cli("doc", "lint"), 0, self.output())

    def test_a_file_nobody_created_is_still_an_orphan(self) -> None:
        # The negative control: the fix is an omission repaired, not a rule
        # relaxed. A document no command wrote has no reason to be indexed.
        self.write("tasks/T-0009-stray.md", "# Stray\n")
        result = self.cli("doc", "lint")
        self.assertEqual(result, 2)
        self.assertIn("orphan", self.output())

    def test_regeneration_is_idempotent(self) -> None:
        self.cli("task", "new", "--goal", "written once", "--verify", "true")
        first = self.committed_index()
        self.cli("task", "list")
        self.assertEqual(first, self.committed_index())
        self.assertEqual(first, tasks.render_tasks_index())


if __name__ == "__main__":
    unittest.main()