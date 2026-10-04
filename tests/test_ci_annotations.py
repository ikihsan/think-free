"""What the annotation mechanism is measured against: real bytes, real workflow.

Split out of `test_annotate.py` on 2026-10-04 (T-0040) when that file passed
the 300-line cap, and by invariant: `test_annotate` holds the mechanism — how a
violation becomes a command, and what the wrapper does with a gate — while this
file holds the two things the mechanism is *for*.

The first is falsification against the defect's own bytes. `e53ca23` is a
commit the fleet published on which two VMs had taken **defect 7**, and the rule
that reads the numbered list came two commits later. Running today's rules over
that commit's real file is the strongest available input, and it is committed
as a test rather than left in a session log, so the next change to
`defectlist.py` cannot quietly stop reporting it. The second direction — this
repository's tip reports nothing and annotates nothing — is the half that is
easy to leave out.

The second class is the workflow: a gate step added without the annotator is
the shape of the defect itself, a gate that runs and says nothing a reader
without admin rights can see. Both directions are checked, including that the
wrapper has not quietly replaced a gate with a different one.
"""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

from test_annotate import props

from originlib import annotate, defectlist, finding, idcheck  # noqa: F401

WORKFLOW = ".github/workflows/ci.yml"


class TheRealDefectTest(unittest.TestCase):
    """Falsified against the defect's own bytes, in both directions.

    `e53ca23` is the commit on which two VMs had taken **defect 7**; the rule
    that reads the list came two commits later. Running today's rules over that
    commit's real tree is the strongest available input: the bytes are the ones
    the fleet published, and the second direction — this repository's tip — is
    the half that is easy to leave out.
    """

    COMMIT = "e53ca23"

    def root(self) -> Path:
        here = Path(__file__).resolve()
        for parent in [here.parent, *here.parent.parents]:
            if (parent / "tasks").is_dir() and (parent / "tools").is_dir():
                return parent
        raise AssertionError("could not locate the repository root")

    def show(self, path: str) -> str | None:
        result = subprocess.run(
            ["git", "show", f"{self.COMMIT}:{path}"],
            cwd=str(self.root()), capture_output=True, text=True,
        )
        return result.stdout if result.returncode == 0 else None

    def test_the_commits_named_are_present_and_hold_the_collision(self) -> None:
        text = self.show("STATE-defects.md")
        if text is None:
            self.skipTest(f"commit {self.COMMIT} is not in this history")
        numbers = [entry.number for entry in defectlist.entries(text)]
        repeated = len(numbers) - len(set(numbers))
        self.assertEqual(repeated, 1, f"fixture drift at {self.COMMIT}: {numbers}")

    def test_the_rules_report_it_and_the_annotation_names_the_file(self) -> None:
        text = self.show("STATE-defects.md")
        if text is None:
            self.skipTest(f"commit {self.COMMIT} is not in this history")
        found = defectlist.duplicate_issues(defectlist.entries(text))
        self.assertEqual(len(found), 1, found)
        # The repository at that commit holds `STATE-defects.md`, so the
        # structured path is a real file and the annotation may name it.
        lines = finding.render(found, self.root())
        self.assertEqual(len(lines), 1, lines)
        self.assertEqual(props(lines[0])["file"], "STATE-defects.md")
        self.assertIn("defect 7 defines 2 defects", lines[0])

    def test_the_tip_reports_nothing_and_annotates_nothing(self) -> None:
        found = idcheck.report(self.root())
        self.assertEqual(found, [], found)
        self.assertEqual(finding.render(found, self.root()), [])


class WorkflowWiringTest(unittest.TestCase):
    """The workflow is held to the wrapper, in both directions.

    A gate step added without `annotate` is the shape of the defect itself: a
    gate that runs, reports nothing a reader can see, and is green when it
    should be red. So the check is on every step that is not the matrix.
    """

    ROW_WIDE = ("Show toolchain", "Tests")

    def workflow(self) -> str:
        path = Path(__file__).resolve().parent.parent / WORKFLOW
        return path.read_text(encoding="utf-8")

    def steps(self, text: str) -> list[tuple[str, str]]:
        found = list(re.finditer(r"^ {6}- name: (?P<name>.+)$", text, re.MULTILINE))
        out = []
        for index, match in enumerate(found):
            end = found[index + 1].start() if index + 1 < len(found) else len(text)
            out.append((match.group("name").strip(), text[match.start():end]))
        return out

    def test_every_gate_step_runs_through_the_annotator(self) -> None:
        # "Annotates" rather than "runs a gate": the probe step added in T-0046
        # emits annotations without running a gate, and the property this file
        # exists for is that a step does not run, report, and say nothing a
        # reader without admin rights can see.
        for name, block in self.steps(self.workflow()):
            if name in self.ROW_WIDE:
                continue
            self.assertTrue(self.emits_annotations(block), f"{name} emits no annotation")

    def test_the_tests_step_escapes_a_percent_as_the_toolkit_does(self) -> None:
        # One `%` is `%25` in a message, per `actions/toolkit`'s `escapeData`.
        # The doubling that was here renders one percent as two; see defect 13
        # and the evidence in `FAILURES.md`.
        block = dict(self.steps(self.workflow()))["Tests"]
        self.assertNotIn('"%%"', block)
        self.assertIn("%25", block)

    def test_a_diagnostic_step_is_not_skipped_by_an_earlier_failure(self) -> None:
        # A step whose `if:` names no status function gets an implicit
        # `success()`, so a red `Tests` step skipped all five gate steps: the
        # annotator was silent on runs `37189825232` and `37190842104`, and a
        # skipped gate is indistinguishable from a passing gate in the
        # annotations. Falsified against the workflow as it was on 2026-10-04,
        # where every one of these steps failed this assertion.
        for name, block in self.steps(self.workflow()):
            if not self.emits_annotations(block):
                continue
            guard = re.search(r"^ {8}if: (?P<expr>.+)$", block, re.MULTILINE)
            self.assertIsNotNone(guard, f"{name} emits annotations with no guard at all")
            expression = guard.group("expr")
            self.assertTrue(
                any(f"{name}()" in expression for name in ("always", "failure", "cancelled")),
                f"{name} emits annotations but {expression!r} carries no status function, "
                "so it is skipped when an earlier step fails",
            )

    @staticmethod
    def emits_annotations(block: str) -> bool:
        return "tools/origin annotate -- " in block or "tools/origin probe" in block

    def test_the_workflow_still_runs_those_gates_it_names(self) -> None:
        # The other half: the wrapper must not have quietly replaced a gate
        # with a different one. Each name resolves to something runnable.
        for name, _ in self.steps(self.workflow()):
            self.assertNotIn("annotate -- doc index", name)
        for gate in annotate.GATES:
            self.assertIn(gate, self.workflow(), f"{gate} no longer runs on CI")