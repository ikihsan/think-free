"""A file's extension must not decide whether a session declared it.

The false negative defect 12's entry names and never measured: `reconcile`
excluded every `*.json`, `*.jsonl` and `*.log` path from the undeclared-change
report, because it asked `doclint.is_exempt` — the *line cap's* question, which
answers yes for those three suffixes. Content the cap ignores was treated as
content no session can change silently, so `tests/python-versions.json`,
`tests/git-versions.json` and `tasks/CLAIMS.jsonl` could be edited with nothing
declared and nothing reported. The two questions are different: the cap asks
whether a file's length is worth reading, and reconciliation asks whether a
session accounts for a change.

Three directions are falsified here.

* The defect: a data-suffix path changed without declaring is reported. This is
  the direction that fails on the unrepaired code — all three suffixes, because a
  rule that fixed only `.json` would leave the ledger and the session streams.
* The repair: a *declared* data file, a generated one and the session's own
  directory are still silent, and a vendored path is still covered by the
  declared globs. A rule nobody can satisfy is a gate nobody runs.
* The record: `RecordedSilenceTest` reads the session that closed this
  repository's last merge. It contains another VM's experiment captures and
  three other sessions' streams, declares none of them, and reports one
  undeclared path — so the exemption is visible on the bytes the fleet published
  and not only in a fixture written after the repair.
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from harness import RepoTest

from originlib import session, taskops

# Session 030 on VM 0947 finished at c41dc20 with the other VM's T-0046, T-0048
# and T-0049 work already in its tree, and reported a single undeclared path.
RECORDED_SESSION = "2026-10-04-030-attribute-a-task-file-that-a-task-comman"
# Data-suffix paths its window contained. Two are its own session's directory
# (`commands.log` is written by tools/x) and two are experiment captures; the
# rest are other sessions' streams, which only the suffix exemption hid.
RECORDED_SILENT = (
    "EXPERIMENTS/010-annotation-rendering/raw/summary.json",
    "EXPERIMENTS/010-annotation-rendering/raw/rate_limit.json",
    "sessions/2026-10-04-029-measure-how-github-files-an-annotation-o/events.jsonl",
    "sessions/2026-10-04-031-record-the-measured-ci-state-on-the-tip/commands.log",
)


class DataSuffixIsNotADeclaration(RepoTest):
    """The rule as repaired, on a repository the harness builds."""

    def setUp(self) -> None:
        super().setUp()
        taskops.create("declare a data file or report it", "true")
        self.commit("add task")
        self.active = session.start("change a data file", agent="tester", task="T-0001")

    # -------------------------------------------------------------- helpers
    def commit(self, message: str) -> None:
        subprocess.run(["git", "add", "-A"], cwd=str(self.repo), check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=str(self.repo), check=True,
                       capture_output=True)

    def change(self, relative: str, content: str, declare: bool = False) -> str:
        self.write(relative, content)
        if declare:
            session.artifact(relative)
        self.commit(f"change {relative}")
        return relative

    def unlogged(self, **kwargs) -> list[str]:
        return session.finish(kwargs.pop("outcome", "worked"), "changed data files",
                              "none")["unlogged"]

    # ------------------------------------------------------- the defect, repaired
    def test_a_json_changed_without_declaring_is_reported(self) -> None:
        path = self.change("work/state.json", "{}\n")
        self.assertEqual(self.unlogged(), [path])

    def test_a_jsonl_changed_without_declaring_is_reported(self) -> None:
        path = self.change("work/ledger.jsonl", '{"a": 1}\n')
        self.assertEqual(self.unlogged(), [path])

    def test_a_log_changed_without_declaring_is_reported(self) -> None:
        path = self.change("work/commands.log", "$ echo hi\n")
        self.assertEqual(self.unlogged(), [path])

    def test_a_changed_data_file_is_reported_alongside_a_declared_one(self) -> None:
        self.change("work/declared.json", "{}\n", declare=True)
        path = self.change("work/quiet.json", "{}\n")
        self.assertEqual(self.unlogged(), [path])

    # ------------------------------------------------------------ the controls
    def test_a_declared_data_file_is_not_reported(self) -> None:
        self.change("work/declared.json", "{}\n", declare=True)
        self.assertEqual(self.unlogged(), [])

    def test_a_generated_file_is_not_reported(self) -> None:
        # The generated mark is the other exemption, and it is a real one: an
        # index no session wrote is not undeclared work. The mark is the form a
        # generator in this repository actually writes — a `.json` variant is
        # asserted *not* to exist, because no generator emits one and a rule
        # written against a form nothing produces is a rule nothing exercises.
        self.change("work/index.md",
                    "<!-- generated-by: origin; do not edit by hand -->\n{}\n")
        self.assertEqual(self.unlogged(), [])

    def test_a_json_carrying_no_generator_mark_is_reported(self) -> None:
        # The control for the control: a `.json` file that *claims* to be
        # generated in a syntax nothing here writes gets no exemption.
        path = self.change("work/pretend.json", '{"generated-by": "origin"}\n')
        self.assertEqual(self.unlogged(), [path])

    def test_a_vendored_path_is_still_exempt(self) -> None:
        from originlib import reconcile

        self.write("vendor/MANIFEST.md", "exempt: vendor/covered.json\n")
        self.assertTrue(reconcile._is_own_session_file(self.active, "vendor/covered.json"))
        self.assertFalse(reconcile._is_own_session_file(self.active, "vendor/other.json"))

    def test_the_line_cap_still_exempts_a_data_file(self) -> None:
        # The cap's question is unchanged by the split: a 400-line JSON is an
        # `info`, not a violation. Losing this would be a different defect.
        from originlib import doclint

        long_json = self.write("work/big.json", "\n".join(["{}"] * 400) + "\n")
        result = doclint.Result()
        doclint.check_line_cap(result, [long_json], [])
        self.assertEqual(result.violations, [])
        self.assertEqual(len(result.infos), 1, result.infos)


class LedgerIsDeclaredByItsAppender(RepoTest):
    """`tasks/CLAIMS.jsonl` is a command's write, declared the way a task file is."""

    def setUp(self) -> None:
        super().setUp()
        taskops.create("append to the ledger", "true")
        self.commit("add task")
        self.active = session.start("run a task to completion", agent="tester", task="T-0001")

    def commit(self, message: str) -> None:
        subprocess.run(["git", "add", "-A"], cwd=str(self.repo), check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=str(self.repo), check=True,
                       capture_output=True)

    def rewrites(self) -> list[dict]:
        return [
            event["data"]
            for event in self.session_events(self.active.session)
            if event["kind"] == "task_rewrite"
        ]

    def test_the_ledger_appends_are_not_reported(self) -> None:
        taskops.claim("T-0001", "tester", "vm-x", self.active.session)
        self.commit("claim")
        taskops.transition("T-0001", "done", "done")
        self.commit("complete")
        result = session.finish("worked", "ran a task", "none")
        self.assertEqual(result["unlogged"], [], result["unlogged"])
        # Named rather than dropped, for the reason the task file's declaration
        # is named: an excluded path an operator cannot see cannot be checked.
        self.assertIn("tasks/CLAIMS.jsonl", result["rewritten"])

    def test_the_declaration_carries_the_bytes_the_append_wrote(self) -> None:
        taskops.claim("T-0001", "tester", "vm-x", self.active.session)
        recorded = [e for e in self.rewrites() if e["path"] == "tasks/CLAIMS.jsonl"]
        self.assertEqual(len(recorded), 1, recorded)
        entry = recorded[0]
        self.assertEqual(len(entry["sha256"]), 64)
        self.assertEqual(entry["size"], (self.repo / "tasks/CLAIMS.jsonl").stat().st_size)
        self.assertEqual(entry["action"], "claim")

    def test_a_hand_edit_to_the_ledger_after_the_append_is_reported(self) -> None:
        taskops.claim("T-0001", "tester", "vm-x", self.active.session)
        self.commit("claim")
        ledger = self.repo / "tasks/CLAIMS.jsonl"
        ledger.write_text(ledger.read_text().replace('"action": "claim"', '"action": "create"'))
        result = session.finish("worked", "ran a task and edited the ledger", "none")
        self.assertEqual(result["unlogged"], ["tasks/CLAIMS.jsonl"])
        # The declaration no longer describes the tree. The task file's own
        # declaration still does, which is why this asserts the ledger's absence
        # rather than an empty list.
        self.assertNotIn("tasks/CLAIMS.jsonl", result["rewritten"])

    def test_a_later_append_does_not_lose_the_declaration(self) -> None:
        # Two commands, one file: the second declaration must not read as a
        # rewrite of the *file* rather than of the bytes it wrote.
        taskops.claim("T-0001", "tester", "vm-x", self.active.session)
        self.commit("claim")
        taskops.transition("T-0001", "blocked", "waiting")
        self.commit("block")
        result = session.finish("worked", "claimed and blocked a task", "none")
        self.assertEqual(result["unlogged"], [], result["unlogged"])


class RecordedSilenceTest(unittest.TestCase):
    """The exemption on the bytes the fleet published, not on a new fixture."""

    def root(self) -> Path:
        here = Path(__file__).resolve()
        for parent in [here.parent, *here.parent.parents]:
            if (parent / "tasks").is_dir() and (parent / "tools").is_dir():
                return parent
        raise AssertionError("could not locate the repository root")

    def stream(self) -> list[dict] | None:
        result = subprocess.run(
            ["git", "show", f"HEAD:sessions/{RECORDED_SESSION}/events.jsonl"],
            cwd=str(self.root()), capture_output=True, text=True,
        )
        if result.returncode != 0:
            return None
        return [json.loads(line) for line in result.stdout.splitlines() if line.strip()]

    def test_that_session_reported_one_path_and_declared_none_of_these(self) -> None:
        events = self.stream()
        if events is None:
            self.skipTest(f"session {RECORDED_SESSION} is not in this history")
        unlogged = [e["data"].get("path") for e in events if e["kind"] == "unlogged_change"]
        declared = {e["data"].get("path") for e in events if e["kind"] == "artifact"}
        self.assertEqual(unlogged, ["ROADMAP.md"])
        for path in RECORDED_SILENT:
            self.assertNotIn(path, declared, path)
            self.assertNotIn(path, unlogged, path)

    def test_the_two_questions_give_different_answers_on_those_paths(self) -> None:
        from originlib import doclint

        globs = doclint.declared_exemptions()
        for path in RECORDED_SILENT:
            self.assertTrue(doclint.is_exempt(path, globs), path)
            self.assertFalse(doclint.is_declared_exempt(path, globs), path)

    def test_reconciliation_reads_the_declared_question_for_them(self) -> None:
        from originlib import reconcile

        for path in RECORDED_SILENT:
            self.assertFalse(reconcile._is_vendored(path), path)


if __name__ == "__main__":
    unittest.main()
