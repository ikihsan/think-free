"""Task files, the claim ledger, and verification execution."""

from __future__ import annotations

import unittest

from harness import RepoTest, write_doc

from originlib import taskops, tasks


class TaskCreationTest(RepoTest):
    def test_create_writes_a_template_with_meta(self) -> None:
        task = taskops.create("measure the thing", "tools/origin doc lint", rationale="why")
        self.assertEqual(task.task_id, "T-0001")
        self.assertTrue(task.path.name.endswith("-measure-the-thing.md"))
        text = task.path.read_text(encoding="utf-8")
        self.assertIn("status: open", text)
        self.assertIn("verify: tools/origin doc lint", text)
        self.assertIn("origin-meta", text)

    def test_ids_increment(self) -> None:
        first = taskops.create("first task", "true")
        second = taskops.create("second task", "true")
        self.assertEqual(first.task_id, "T-0001")
        self.assertEqual(second.task_id, "T-0002")

    def test_empty_goal_is_refused(self) -> None:
        with self.assertRaises(tasks.TaskError):
            taskops.create("   ", "true")

    def test_find_returns_the_task(self) -> None:
        created = taskops.create("findable", "true")
        self.assertEqual(tasks.find("T-0001").path, created.path)

    def test_find_unknown_task_raises(self) -> None:
        with self.assertRaises(tasks.TaskError):
            tasks.find("T-9999")

    def test_status_is_readable_from_meta(self) -> None:
        task = taskops.create("readable", "true")
        self.assertEqual(tasks.load(task.path).status, "open")


class ClaimLedgerTest(RepoTest):
    def test_claim_records_holder(self) -> None:
        taskops.create("claimable", "true")
        claimed = taskops.claim("T-0001", agent="agent-a", vm="vm-1")
        self.assertEqual(claimed.status, "claimed")
        self.assertEqual(claimed.meta["claim-agent"], "agent-a")
        self.assertEqual(tasks.active_claims()["T-0001"]["agent"], "agent-a")

    def test_second_agent_cannot_claim(self) -> None:
        taskops.create("contended", "true")
        taskops.claim("T-0001", agent="agent-a", vm="vm-1")
        with self.assertRaises(tasks.TaskError):
            taskops.claim("T-0001", agent="agent-b", vm="vm-2")

    def test_same_agent_may_reclaim(self) -> None:
        taskops.create("reclaimable", "true")
        taskops.claim("T-0001", agent="agent-a")
        again = taskops.claim("T-0001", agent="agent-a", vm="vm-3")
        self.assertEqual(again.meta["claim-vm"], "vm-3")

    def test_completion_releases_the_claim(self) -> None:
        taskops.create("completable", "true")
        taskops.claim("T-0001", agent="agent-a")
        taskops.transition("T-0001", "done", "finished")
        self.assertNotIn("T-0001", tasks.active_claims())
        taskops.claim("T-0001", agent="agent-b")

    def test_ledger_is_append_only_jsonl(self) -> None:
        taskops.create("ledgered", "true")
        taskops.claim("T-0001", agent="agent-a")
        taskops.transition("T-0001", "done", "ok")
        lines = (self.repo / "tasks" / "CLAIMS.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 3)
        actions = [tasks.claims()[i]["action"] for i in range(3)]
        self.assertEqual(actions, ["create", "claim", "complete"])

    def test_unknown_status_is_refused(self) -> None:
        taskops.create("bad status", "true")
        with self.assertRaises(tasks.TaskError):
            taskops.transition("T-0001", "vibing", "no")


class VerificationTest(RepoTest):
    def test_passing_verification_reports_zero(self) -> None:
        task = taskops.create("passes", "true")
        outcome = taskops.run_verification(task)
        self.assertTrue(outcome["ran"])
        self.assertEqual(outcome["exit_code"], 0)

    def test_failing_verification_reports_the_code(self) -> None:
        task = taskops.create("fails", "exit 7")
        outcome = taskops.run_verification(task)
        self.assertEqual(outcome["exit_code"], 7)

    def test_missing_verify_command_is_reported(self) -> None:
        task = taskops.create("no verify", "true")
        task._meta_override = None  # attribute only; ensure no side effects
        path = self.repo / "tasks" / task.path.name
        path.write_text(path.read_text(encoding="utf-8").replace("verify: true\n", ""), encoding="utf-8")
        outcome = taskops.run_verification(tasks.load(path))
        self.assertFalse(outcome["ran"])


class RepeatedFlagTest(RepoTest):
    """A flag a user would reasonably repeat must not discard what came first.

    Defect 11 in `STATE-defects.md`: `task new` took five `--acceptance` values
    and wrote one, silently, because both it and `--steps` were declared with a
    string default and no `action="append"`. The task file is the record of what
    "done" means, so a truncated one makes a completed task look complete against
    a definition no reader can see.
    """

    def acceptance_lines(self, filename: str) -> list[str]:
        text = (self.repo / "tasks" / filename).read_text(encoding="utf-8")
        body = text.split("## Acceptance criteria", 1)[1]
        return [line for line in body.splitlines() if line.startswith("- [ ]")]

    def test_three_acceptance_flags_produce_three_lines(self) -> None:
        code = self.cli(
            "task", "new", "--goal", "five criteria", "--verify", "true",
            "--acceptance", "- [ ] one",
            "--acceptance", "- [ ] two",
            "--acceptance", "- [ ] three",
        )
        self.assertEqual(code, 0, self.errors())
        lines = self.acceptance_lines("T-0001-five-criteria.md")
        self.assertEqual(len(lines), 3, lines)
        self.assertIn("one", lines[0])
        self.assertIn("three", lines[2])

    def test_three_steps_flags_produce_three_numbered_lines(self) -> None:
        code = self.cli(
            "task", "new", "--goal", "three steps", "--verify", "true",
            "--steps", "1. first",
            "--steps", "2. second",
            "--steps", "3. third",
        )
        self.assertEqual(code, 0, self.errors())
        path = self.repo / "tasks" / "T-0001-three-steps.md"
        body = path.read_text(encoding="utf-8").split("## Steps", 1)[1]
        for step in ("1. first", "2. second", "3. third"):
            self.assertIn(step, body)

    def test_one_flag_is_unchanged(self) -> None:
        # The control: the repair must not alter the shape a single flag produces,
        # or a fix for a silent loss becomes a change of format.
        code = self.cli(
            "task", "new", "--goal", "one criterion", "--verify", "true",
            "--acceptance", "- [ ] only",
        )
        self.assertEqual(code, 0, self.errors())
        self.assertEqual(len(self.acceptance_lines("T-0001-one-criterion.md")), 1)

    def test_no_flag_leaves_the_section_empty_rather_than_inventing_one(self) -> None:
        # `taskops.create` defaults `acceptance` to a bare `- [ ] `, but the CLI
        # always passes a value, so that default is unreachable. This test pins
        # what actually happens and says why it is right: nothing was asked for,
        # so nothing is claimed. A bare empty checkbox would be worse — it is a
        # checkable item nobody wrote, and somebody can tick it.
        code = self.cli("task", "new", "--goal", "no criteria", "--verify", "true")
        self.assertEqual(code, 0, self.errors())
        text = (self.repo / "tasks" / "T-0001-no-criteria.md").read_text(encoding="utf-8")
        section = text.split("## Acceptance criteria", 1)[1].split("## Verification", 1)[0]
        self.assertEqual(section.strip(), "", section)


class TaskIndexTest(RepoTest):
    def test_index_lists_tasks(self) -> None:
        taskops.create("indexed", "true")
        text = tasks.render_tasks_index()
        self.assertIn("T-0001", text)
        self.assertIn("generated-by: origin", text)

    def test_index_marks_owner_and_status(self) -> None:
        taskops.create("marked", "true")
        text = tasks.render_tasks_index()
        self.assertIn("status: active", text)
        self.assertIn("owner: docs/INDEX.md", text)

    def test_print_list_does_not_raise(self) -> None:
        taskops.create("listed", "true")
        tasks.print_list("")
        tasks.print_list("open")


if __name__ == "__main__":
    unittest.main()