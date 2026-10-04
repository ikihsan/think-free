"""A red gate must name the file it rejected, in GitHub's own vocabulary.

T-0040, defect 12 in `STATE-defects.md`. Before this, CI's `Tests` step
re-emitted a failing test as a `::error` line and the four file-reading gate
steps emitted nothing: a red `Documentation lint` named a step and nothing more,
and the run log that says which rule failed needs repository admin rights.
`FAILURES.md` F020 measured that from the public API and cost an hour of
elimination to establish.

So the claim under test is narrow and stated as a property:

    every violation a gate reports becomes one workflow command naming the
    violating file, and a tree every gate accepts produces no command at all.

Both halves are here, because the second is the one that is easy to leave out: a
renderer that always emits is indistinguishable from one that found something.

The location is read from the *structured* field, never parsed out of the
message. `ShapeTest.test_the_structured_path_wins_over_the_text` is the control
for that, and it is the shape of mistake D025 describes — a reader concludes
about the property from the field it happened to look at.
"""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

from harness import RepoTest, git, write_doc

from originlib import annotate, finding
from originlib.usage import Usage

WORKFLOW = ".github/workflows/ci.yml"
# `::error file=…,line=…::message`, in the order the documentation gives.
COMMAND = re.compile(r"^::(?P<level>[a-z]+)(?P<props>[^:]*)?::(?P<message>.*)$")


def props(command: str) -> dict[str, str]:
    match = COMMAND.match(command)
    assert match is not None, command
    out = {}
    for item in (match.group("props") or "").lstrip().split(","):
        if "=" in item:
            key, value = item.split("=", 1)
            out[key] = value
    return out


class ShapeTest(unittest.TestCase):
    """The renderer, on findings built by hand rather than by a gate."""

    def setUp(self) -> None:
        import tempfile

        self.root = Path(tempfile.mkdtemp(prefix="origin-annotate-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(self.root, ignore_errors=True))
        (self.root / "docs").mkdir()
        (self.root / "docs" / "a.md").write_text("one\ntwo\nthree\n", encoding="utf-8")
        (self.root / "docs" / "b.md").write_text("only\n", encoding="utf-8")

    def one(self, item: finding.Finding, **kwargs) -> str:
        lines = finding.render([item], self.root, **kwargs)
        self.assertEqual(len(lines), 1, lines)
        return lines[0]

    def test_a_known_file_and_line_become_properties(self) -> None:
        command = self.one(finding.Finding("docs/a.md: broken link", "docs/a.md", 2))
        self.assertEqual(props(command)["file"], "docs/a.md")
        self.assertEqual(props(command)["line"], "2")
        self.assertTrue(command.endswith("::docs/a.md: broken link"))

    def test_a_file_level_verdict_carries_no_line(self) -> None:
        # A whole-file verdict knows the file and nothing narrower. Publishing
        # a line anyway would be inventing a position.
        self.assertNotIn("line", props(self.one(finding.Finding.at("docs/a.md", "too long"))))

    def test_no_violations_means_no_command(self) -> None:
        self.assertEqual(finding.render([], self.root), [])

    def test_a_violation_with_no_path_is_emitted_without_one(self) -> None:
        command = self.one(finding.Finding("the record could not be read at all"))
        self.assertEqual(props(command), {})
        self.assertTrue(command.startswith("::error::"))

    def test_a_directory_gets_no_file_property(self) -> None:
        # `skills check` reports `.claude/skills/<name>` for a mirror that is a
        # real directory. A `file=` pointing at a directory is not something a
        # reader can open, so the property is dropped and the text still names
        # it. Observed end to end, not hypothetical.
        (self.root / "claude").mkdir()
        (self.root / "claude" / "skills").mkdir()
        command = self.one(finding.Finding("claude/skills/x: real directory without SKILL.md"))
        self.assertEqual(props(command), {})
        self.assertIn("claude/skills/x", command)

    def test_a_path_that_does_not_exist_gets_no_file_property(self) -> None:
        command = self.one(finding.Finding.at("docs/nowhere.md", "gone"))
        self.assertEqual(props(command), {})

    def test_a_line_past_the_end_of_the_file_is_dropped(self) -> None:
        # A generated index shorter than the line the previous commit recorded
        # would publish a position that cannot exist.
        command = self.one(finding.Finding.at("docs/b.md", "stale", 99))
        self.assertEqual(props(command), {"file": "docs/b.md"})

    def test_the_structured_path_wins_over_the_text(self) -> None:
        # The control for the whole design. The message begins with something
        # that looks like a different path, which is what every `doc lint`
        # violation looks like, and a renderer that parsed the first token would
        # file this one under the wrong document.
        command = self.one(
            finding.Finding("docs/b.md: orphan document", "docs/a.md")
        )
        self.assertEqual(props(command)["file"], "docs/a.md")

    def test_percent_in_a_message_is_escaped(self) -> None:
        # `actions/toolkit`'s `escapeData`: `%` -> `%25`. The workflow's own
        # awk doubled it instead, which renders one percent as two
        # (`source-supported`, defect 13).
        command = self.one(finding.Finding("coverage 90% of lines"))
        self.assertIn("90%25", command)
        self.assertNotIn("%%", command)

    def test_newlines_in_a_message_cannot_end_the_command(self) -> None:
        # One command, one line: a violation whose text contains a newline must
        # not be able to inject a second workflow command after it.
        command = self.one(finding.Finding("first\n::warning::forged"))
        self.assertNotIn("\n", command)
        self.assertTrue(command.startswith("::error::first%0A::warning::forged"))

    def test_separators_in_a_file_property_are_escaped(self) -> None:
        (self.root / "docs" / "c,d.md").write_text("x\n", encoding="utf-8")
        command = self.one(finding.Finding.at("docs/c,d.md", "odd name"))
        self.assertEqual(props(command)["file"], "docs/c%2Cd.md")

    def test_the_cap_is_reported_rather_than_silently_applied(self) -> None:
        lines = finding.render(
            [finding.Finding(f"violation {n}") for n in range(5)], self.root, cap=2
        )
        self.assertEqual(len(lines), 3, lines)
        self.assertIn("3 further violation(s)", lines[-1])
        self.assertTrue(lines[-1].startswith("::warning"))

    def test_a_finding_is_still_the_string_the_report_prints(self) -> None:
        # Every gate in this repository reports strings and every existing test
        # asserts on them. A Finding that were not a `str` would have changed
        # the rendered report; this is what says it did not.
        item = finding.Finding.at("docs/a.md", "broken link")
        self.assertIsInstance(item, str)
        self.assertEqual(item, "docs/a.md: broken link")
        # Every gate here formats this into `  FAIL  {problem}`, so a
        # violation that is not usable as a string would break 300-odd
        # assertions across the suite rather than one of them.
        self.assertIn(f"  FAIL  {item}", "  FAIL  docs/a.md: broken link")


class GateTest(RepoTest):
    """The wrapper over a real gate, in a real repository."""

    def annotations(self, *args: str) -> list[str]:
        code = self.cli("annotate", *args)
        self.assertIn(code, (0, 2, 4), f"unexpected exit: {self.errors()}")
        return [line for line in self.output().splitlines() if line.startswith("::")]

    def test_a_clean_gate_emits_nothing_at_all(self) -> None:
        # The half of the claim that is easy to leave out. `release check` is
        # not in this list because the fixture repository's manifest declares
        # no tables, which is a real violation rather than a rendering problem;
        # `test_release.py` builds its own manifest for that gate.
        self.write_generated()
        self.assertEqual(self.annotations("--", "doc lint"), [])

    def test_a_planted_violation_is_named_by_file_and_line(self) -> None:
        write_doc(self.repo / "docs" / "policy" / "lonely.md", "Lonely", "docs/INDEX.md")
        path = self.repo / "STATE.md"
        text = path.read_text(encoding="utf-8").splitlines()
        text.insert(3, "See [nothing](nowhere.md) for the detail.")
        path.write_text("\n".join(text) + "\n", encoding="utf-8")
        git(self.repo, "add", "-A")
        found = self.annotations("--", "doc lint")
        broken = [line for line in found if "broken link" in line]
        self.assertEqual(len(broken), 1, found)
        self.assertEqual(props(broken[0])["file"], "STATE.md")
        self.assertEqual(props(broken[0])["line"], "4")
        orphan = [
            line
            for line in found
            if props(line).get("file") == "docs/policy/lonely.md"
            and "orphan document" in line
        ]
        self.assertEqual(len(orphan), 1, found)
        # A whole-file verdict: the file is named and no line is invented.
        self.assertNotIn("line", props(orphan[0]))
        # Every violation got exactly one command, so nothing is dropped.
        failures = [
            line for line in self.output().splitlines() if line.startswith("  FAIL  ")
        ]
        self.assertEqual(len(found), len(failures), (found, failures))

    def test_the_gates_own_exit_code_is_kept(self) -> None:
        # CI and VM scripts branch on 2 versus 4. A wrapper that normalised it
        # would silently change what every caller does.
        self.assertEqual(annotate.GATES["doc lint"].failure, 2)
        self.assertEqual(annotate.GATES["release check"].failure, 2)
        self.assertEqual(annotate.GATES["skills verify"].failure, 4)
        self.assertEqual(annotate.GATES["session verify"].failure, 4)

    def test_a_gate_that_fails_still_exits_with_its_own_code(self) -> None:
        self.write("STATE.md", "# State\n\n<!-- origin-meta\nowner: x\n-->\n")
        git(self.repo, "add", "-A")
        code = self.cli("annotate", "--", "doc lint")
        self.assertEqual(code, 2)
        self.assertTrue(self.output().strip().splitlines()[-1].startswith("::error"))

    def test_an_unknown_gate_is_refused_with_one_line(self) -> None:
        self.assertEqual(self.cli("annotate", "nonsense"), 1)
        self.assertIn("name a gate", self.errors())
        self.assertNotIn("Traceback", self.errors())

    def test_a_flag_the_gate_does_not_read_is_refused(self) -> None:
        # Silently not applying it is the same failure as a rule that quietly
        # stops matching: a gate that ran, and was not the one asked for.
        self.assertEqual(self.cli("annotate", "doc", "lint", "--quiet"), 1)
        self.assertIn("--quiet", self.errors())
        self.assertEqual(self.cli("annotate", "session", "verify", "--nope"), 1)

    def test_the_separator_is_accepted_because_the_gates_own_flags_follow_it(self) -> None:
        # Both shapes a caller writes: the gate as two words, and the gate
        # quoted as one, which is what a shell loop over the names produces.
        self.assertEqual(annotate.resolve(["--", "doc", "lint"]), ("doc lint", []))
        self.assertEqual(annotate.resolve(["doc", "lint"]), ("doc lint", []))
        self.assertEqual(annotate.resolve(["--", "doc lint"]), ("doc lint", []))
        self.assertEqual(
            annotate.resolve(["session", "verify", "--strict"]),
            ("session verify", ["--strict"]),
        )
        # Longest name first, so `release check` is never read as `release`.
        self.assertEqual(annotate.resolve(["skills", "verify"]), ("skills verify", []))

    def test_session_verify_reads_its_own_lease_flag(self) -> None:
        self.write_generated()
        text, violations, code = annotate.GATES["session verify"].report(["--lease-hours", "6"])
        self.assertIn("session verify:", text)
        self.assertEqual(violations, [])
        self.assertEqual(code, 4)
        with self.assertRaises(Usage):
            annotate.GATES["session verify"].report(["--lease-hours"])

    def test_every_registered_gate_runs_against_this_repository(self) -> None:
        # A gate that cannot run is a gate that cannot fail (F010). The registry
        # is the list, so a name added to it is exercised here or not at all.
        for name in annotate.GATES:
            text, violations, failure = annotate.GATES[name].report([])
            self.assertTrue(text.strip(), name)
            self.assertIsInstance(violations, list, name)
            self.assertIn(failure, (0, 2, 4), name)
