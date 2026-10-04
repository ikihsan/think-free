"""How GitHub renders a workflow command, measured by the run that needs it.

T-0046, defect 18 in `STATE-defects.md`. `docs/operations/ci-diagnosis.md`
carried the claim that whether GitHub files a check-run annotation on a command's
`file=` property was `unmeasured`, and quoted run `37189825232` beside it — a run
whose `Tests` step failed, so the annotating steps were **skipped** and the
`::error file=…` string in its annotations was a unittest assertion diff rather
than an emitted command. Reading it was the D025 shape twice over, and it is
recorded as `FAILURES.md` F021.

What is left unmeasured is the rest of the rendering: `line=`, the escaping, and
what a fileless command looks like once a reader can compare it with a filed one.
`origin probe` measures those on every run by emitting one annotation per shape,
so the reference and the failure come from the same place. These tests hold the
probe to that: each shape it claims to measure, the properties the table says it
has, and the two properties that keep it usable — that it cannot inject a second
command, and that it cannot redden a run.
"""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

from test_annotate import props

from originlib import probe

LEVEL = re.compile(r"^::(?P<level>[a-z]+)(?P<rest>.*)$")

# The shape names, written out rather than read from `probe.SHAPES`. The table is
# otherwise its own contract: a shape dropped from it would take the assertion
# that reads it with it, and the probe would quietly stop measuring something the
# operations document still promises. Written here, and in
# `docs/operations/ci-diagnosis.md`, the three have to agree. Falsified by
# deleting `warning-level` from the table, which fails this.
SHAPE_NAMES = (
    "filed-with-line",
    "filed-no-line",
    "message-percent",
    "message-colon-comma",
    "message-newline",
    "warning-level",
    "no-file",
)


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parent.parents]:
        if (parent / "tasks").is_dir() and (parent / "tools").is_dir():
            return parent
    raise AssertionError("could not locate the repository root")


class ShapeTest(unittest.TestCase):
    """Every shape the table declares is emitted with the properties it declares."""

    def setUp(self) -> None:
        self.root = repo_root()
        self.lines = probe.commands(self.root)

    def named(self, name: str) -> str:
        """The one command carrying `annotation-probe/<name>`, matched on the message."""
        prefix = f"annotation-probe/{name}:"
        matches = [line for line in self.lines if prefix in line.split("::", 2)[-1]]
        self.assertEqual(len(matches), 1, f"{name}: expected exactly one line, got {matches}")
        return matches[0]

    def test_one_line_per_shape_and_nothing_else(self) -> None:
        self.assertEqual(len(self.lines), len(probe.SHAPES))

    def test_the_table_still_measures_every_shape_it_promises(self) -> None:
        self.assertEqual([name for name, *_rest in probe.SHAPES], list(SHAPE_NAMES))

    def test_every_shape_is_emitted_with_the_properties_it_declares(self) -> None:
        for name, path, line, level, _message in probe.SHAPES:
            command = self.named(name)
            match = LEVEL.match(command)
            self.assertIsNotNone(match, command)
            self.assertEqual(match.group("level"), level, command)
            properties = props(command)
            if path:
                self.assertEqual(properties.get("file"), path, command)
            else:
                self.assertNotIn("file", properties, command)
            if line:
                self.assertEqual(properties.get("line"), str(line), command)
            else:
                self.assertNotIn("line", properties, command)

    def test_the_paths_and_lines_are_real_so_the_probe_measures_rendering(self) -> None:
        # `finding.location` drops a `file=` that is not a file and a `line=` past
        # the end of one. A shape naming a path this repository does not have
        # would measure the drop instead of the rendering, which is the same
        # silent-absence D025's second obligation is about.
        for name, path, line, _level, _message in probe.SHAPES:
            if not path:
                continue
            target = self.root / path
            self.assertTrue(target.is_file(), f"{name} names {path}, which is not a file")
            self.assertLessEqual(line, len(target.read_text(encoding="utf-8").splitlines()), name)


class NoHazardTest(unittest.TestCase):
    """The two properties that make the probe safe to run on every push."""

    def setUp(self) -> None:
        self.lines = probe.commands(repo_root())

    def test_a_newline_cannot_inject_a_second_command(self) -> None:
        percent = [line for line in self.lines if "%0A" in line]
        self.assertEqual(len(percent), 1, percent)
        self.assertEqual(len(self.lines), len(probe.SHAPES))
        for line in self.lines:
            self.assertNotIn("\n", line, line)
            self.assertNotIn("\r", line, line)

    def test_a_percent_is_escaped_in_the_message(self) -> None:
        percent = [line for line in self.lines if "50%25 of this sentence" in line]
        self.assertEqual(len(percent), 1, percent)

    def test_it_never_emits_an_error_so_it_cannot_redden_a_run(self) -> None:
        # The one control that keeps the probe in the workflow. An `::error`
        # annotation on a clean tree has never been observed in this
        # repository's runs, and publishing that assumption on every push would
        # be the record asserting something it has not measured.
        for line in self.lines:
            self.assertNotEqual(LEVEL.match(line).group("level"), "error", line)

    def test_a_fileless_shape_is_included_because_it_is_the_control(self) -> None:
        # Arms B and C of `EXPERIMENTS/010-annotation-rendering` read `path
        # .github` off a *fileless* command and drew a conclusion about a filed
        # one. This shape is what makes the two cases distinguishable on the run
        # that needs them.
        names = [name for name, path, _line, _level, _message in probe.SHAPES if not path]
        self.assertEqual(names, ["no-file"])


class CommandTest(unittest.TestCase):
    """The CLI itself: it prints the shapes and exits 0 whatever the tree says."""

    def run_cli(self) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["tools/origin", "probe"],
            cwd=str(repo_root()), capture_output=True, text=True,
        )

    def test_it_prints_the_shapes_and_exits_zero(self) -> None:
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.strip().splitlines(), probe.commands(repo_root())
        )

    def test_it_exits_zero_even_with_violations_pending(self) -> None:
        # The tree this ran on has whatever violations it has; the probe does not
        # read a gate, so its exit code is not a function of them. Asserted
        # against the real tree because a probe that consulted a gate would be
        # the one thing that could redden a run.
        self.assertNotIn("doc lint", self.run_cli().stdout)


if __name__ == "__main__":
    unittest.main()