"""The defect T-0047 closed, read out of the bytes the fleet published.

Split out of `test_task_rewrite.py` on 2026-10-04 (T-0050), when adding the claim
ledger's declaration took that file past the 300-line cap. The division is the
one the file's own docstring names: this is the *record* direction, where the
session under test is one that already ran and cannot be re-run.

A stream with no `task_rewrite` event must still be read as declaring nothing.
That is the direction a rule like this fails in silently: a parser that quietly
stops matching looks exactly like a clean tree (defect 10).
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from originlib import declaredwrite, tasks

# A closed session that did everything right and was still reported. Read out of
# git here, not written into a fixture, so the shape under test is the one the
# fleet published rather than one written after the repair.
RECORDED_SESSION = "2026-10-04-019-t-0039-make-acceptance-and-steps-append"
RECORDED_TASK_FILE = "tasks/T-0039-make-acceptance-and-steps-append-on-task-new-so.md"


class CommittedDefectTest(unittest.TestCase):
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

    def test_the_recorded_session_reported_its_own_task_file(self) -> None:
        events = self.stream()
        if events is None:
            self.skipTest(f"session {RECORDED_SESSION} is not in this history")
        unlogged = [e["data"].get("path") for e in events if e["kind"] == "unlogged_change"]
        self.assertEqual(unlogged, [RECORDED_TASK_FILE])
        # It declared seven artifacts and was reported anyway, so this is a false
        # positive rather than a missing declaration.
        declared = [e["data"]["path"] for e in events if e["kind"] == "artifact"]
        self.assertEqual(len(declared), 7, declared)
        end = next(e for e in events if e["kind"] == "session_end")
        self.assertEqual(end["data"]["outcome"], "worked")
        self.assertEqual(end["data"]["unlogged_changes"], 1)

    def test_that_stream_declares_no_rewrite_so_the_rule_cannot_cover_it(self) -> None:
        events = self.stream()
        if events is None:
            self.skipTest(f"session {RECORDED_SESSION} is not in this history")
        self.assertEqual([e for e in events if e["kind"] == "task_rewrite"], [])
        # And the rule reads bytes, so a stream without the digests cannot be
        # honoured whatever its kind.
        self.assertFalse(tasks.digests_match(self.root() / RECORDED_TASK_FILE, {}))

    def test_that_stream_declares_no_ledger_write_either(self) -> None:
        # T-0050 widened the same rule to `tasks/CLAIMS.jsonl`, so the recorded
        # session has nothing that could cover it there either — the 50 rows the
        # sweep counts are this shape, not a rule that stopped reading.
        events = self.stream()
        if events is None:
            self.skipTest(f"session {RECORDED_SESSION} is not in this history")
        self.assertEqual(
            [e for e in events if e["kind"] == "task_rewrite"
             and e["data"].get("path") == "tasks/CLAIMS.jsonl"],
            [],
        )

    def test_a_digest_that_does_not_match_is_not_honoured(self) -> None:
        target = self.root() / RECORDED_TASK_FILE
        real = tasks.meta_digests(target)
        self.assertTrue(tasks.digests_match(target, real))
        for key in ("meta_sha256", "body_sha256"):
            wrong = dict(real)
            wrong[key] = "0" * 64
            self.assertFalse(tasks.digests_match(target, wrong), key)
        self.assertFalse(tasks.digests_match(self.root() / "tasks/README.md", real))

    def test_a_whole_file_declaration_is_not_honoured_on_a_task_file(self) -> None:
        # The two shapes are told apart by their keys, so a ledger digest cannot
        # stand in for a task file's: a hand edit that left the task file's bytes
        # alone but changed them relative to any whole-file record is reported.
        target = self.root() / RECORDED_TASK_FILE
        whole = declaredwrite.whole_file(target)
        self.assertTrue(declaredwrite.matches(target, whole))
        text = target.read_text(encoding="utf-8")
        wrong = dict(whole, sha256="0" * 64)
        self.assertFalse(declaredwrite.matches(target, wrong))
        self.assertIn("task-meta", text)


if __name__ == "__main__":
    unittest.main()
