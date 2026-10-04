"""The `Tests` step must emit the exception line, not the frame above it.

`.github/workflows/ci.yml` re-emits each failing test as a check-run annotation
so a red run is diagnosable without repository admin rights (T-0040, F020). It
did that by taking a fixed 12-line window from the `FAIL:`/`ERROR:` header and
printing **one `::error` per line**, and **the exception is the last line of a
traceback** — so on every traceback longer than 12 frames the annotation named
the file and the line to open and stopped one frame short of the answer.

`observed` 2026-10-04, and it is not a theory: runs `37219755262` and
`37220040091` were red on **identical bytes** with three different tests failing
between them, and the public annotations for all three ended at a
`File ".../cli_repo.py", line 43` frame. Three failures on one tree is the shape of
an environmental fault, and the mechanism that should have explained it is the one
that removed the explanation. Defect 23, F025.

The property, and why each part is one:

| Property | Why it is not the obvious thing |
|---|---|
| the exception survives a traceback longer than the window | asserting on a short traceback passes with the old window too, because nothing was dropped — the defect only appears past the window's edge |
| the window keeps the *end* of the block | the naive repair is a bigger window, which still drops the exception at some length; a 24-frame traceback fails any window small enough to be worth having |
| the header and the exception are in **one** annotation | the old program emitted twelve, one per line, so twelve annotations for one failure; the repair joins them |
| the frames are joined with `%0A`, the toolkit's escape | a raw newline would end the command early and every frame after it would be read as ordinary output — and this is the bug the falsification found in the first attempt |
| a `%` in the message is escaped **before** the join | escaping after inserting `%0A` turns the newline escape into `%250A`, so the frames collapse onto the command line; the second bug the falsification found |

The awk program is read out of the workflow and run by the system awk, so this
holds the bytes CI runs rather than a copy of them that can drift.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

WORKFLOW = ".github/workflows/ci.yml"

# 24 frames is not a realistic traceback on its own; it is here so the test
# cannot pass by choosing a length that happens to fit the window.
LONG_TRACEBACK = "\n".join(
    ["ERROR: test_something (tests.test_x.Case)", "-" * 70, "Traceback (most recent call last):"]
    + [f'  File "/r/tests/test_x.py", line {n}, in test_something' for n in range(10, 34)]
    + ["IsADirectoryError: [Errno 21] Is a directory: '/tmp/x/self.md'", "-" * 70]
    + ["Ran 549 tests in 358.2s", "FAILED (errors=1)"]
)

SHORT_TRACEBACK = "\n".join(
    [
        "ERROR: test_something (tests.test_x.Case)",
        "-" * 70,
        "Traceback (most recent call last):",
        '  File "/r/tests/test_x.py", line 9, in test_something',
        "    boom()",
        "ValueError: 50% of the assertions",
        "-" * 70,
        "Ran 549 tests in 358.2s",
        "FAILED (errors=1)",
    ]
)

# The program as it was before T-0057, kept so the direction of the repair is
# falsified against the defect's own bytes rather than argued.
PREVIOUS = (
    "/^(FAIL|ERROR): / { grab = 12 }\n"
    "grab > 0 { gsub(/%/, \"%25\"); gsub(/\\r/, \"\"); "
    "printf \"::error title=Test failed::%s\\n\", $0; grab-- }\n"
)


def awk_in_workflow() -> str:
    """The awk program the `Tests` step runs, read out of the workflow itself."""
    root = Path(__file__).resolve().parent.parent
    text = (root / WORKFLOW).read_text(encoding="utf-8")
    match = re.search(r"awk -v WINDOW=\d+ '(?P<prog>.*?)' /tmp/unittest\.log", text, re.DOTALL)
    assert match, f"{WORKFLOW} no longer passes a unittest log through awk"
    return match.group("prog")


class AnnotationWindowTest(unittest.TestCase):
    """The awk, run by the system awk, on a log shaped like a real one."""

    def setUp(self) -> None:
        self.awk = shutil.which("awk") or shutil.which("gawk")
        if not self.awk:
            self.skipTest("no awk on this machine")

    def emit(self, program: str, log: str) -> list[str]:
        with tempfile.TemporaryDirectory() as work:
            path = Path(work) / "unittest.log"
            path.write_text(log, encoding="utf-8")
            result = subprocess.run(
                [self.awk, "-v", "WINDOW=14", program, str(path)],
                capture_output=True, text=True, check=True,
            )
        return [line for line in result.stdout.splitlines() if line.strip()]

    def test_the_exception_survives_a_traceback_longer_than_the_window(self) -> None:
        emitted = self.emit(awk_in_workflow(), LONG_TRACEBACK)
        self.assertEqual(len(emitted), 1, emitted)
        self.assertIn("IsADirectoryError", emitted[0])

    def test_a_short_traceback_is_emitted_whole(self) -> None:
        emitted = self.emit(awk_in_workflow(), SHORT_TRACEBACK)
        self.assertEqual(len(emitted), 1, emitted)
        self.assertIn("test_x.py", emitted[0])
        self.assertIn("ValueError", emitted[0])

    def test_each_failure_is_one_command_and_carries_its_header(self) -> None:
        emitted = self.emit(awk_in_workflow(), LONG_TRACEBACK + "\n" + SHORT_TRACEBACK)
        self.assertEqual(len(emitted), 2, emitted)
        self.assertTrue(all(line.startswith("::error title=Test failed::") for line in emitted))
        self.assertIn("IsADirectoryError", emitted[0])
        self.assertIn("ValueError", emitted[1])

    def test_the_frames_are_joined_with_the_toolkits_newline_escape(self) -> None:
        """A raw newline would end the command and lose every frame after it."""
        emitted = self.emit(awk_in_workflow(), SHORT_TRACEBACK)
        self.assertIn("%0A", emitted[0])
        self.assertNotIn("\\n", emitted[0])

    def test_a_percent_is_escaped_before_the_join_not_after(self) -> None:
        """Escaping after inserting `%0A` would render the escape as `%250A`."""
        emitted = self.emit(awk_in_workflow(), SHORT_TRACEBACK)
        self.assertIn("50%25", emitted[0])
        self.assertNotIn("%250A", emitted[0])

    def test_the_window_keeps_the_end_of_the_block_not_the_start(self) -> None:
        """The frame at the *top* is droppable; the exception at the bottom is not."""
        emitted = self.emit(awk_in_workflow(), LONG_TRACEBACK)
        self.assertNotIn("line 10, in test_something", emitted[0])
        self.assertIn("line 33, in test_something", emitted[0])


class ThePreviousProgramTest(unittest.TestCase):
    """Falsified against the defect's own bytes, in both directions."""

    def setUp(self) -> None:
        self.awk = shutil.which("awk") or shutil.which("gawk")
        if not self.awk:
            self.skipTest("no awk on this machine")

    def emit(self, program: str, log: str) -> list[str]:
        with tempfile.TemporaryDirectory() as work:
            path = Path(work) / "unittest.log"
            path.write_text(log, encoding="utf-8")
            result = subprocess.run(
                [self.awk, "-v", "WINDOW=14", program, str(path)],
                capture_output=True, text=True, check=True,
            )
        return [line for line in result.stdout.splitlines() if line.strip()]

    def test_the_previous_window_dropped_the_exception_and_split_the_failure(self) -> None:
        emitted = self.emit(PREVIOUS, LONG_TRACEBACK)
        self.assertEqual(len(emitted), 12, emitted)
        self.assertFalse([line for line in emitted if "IsADirectoryError" in line])

    def test_the_previous_window_was_correct_for_a_short_traceback(self) -> None:
        """The control: the old program was never wrong about a traceback that fit."""
        emitted = self.emit(PREVIOUS, SHORT_TRACEBACK)
        self.assertTrue([line for line in emitted if "ValueError" in line])

    def test_the_repair_changes_nothing_else_about_the_emission(self) -> None:
        emitted = self.emit(awk_in_workflow(), SHORT_TRACEBACK)
        self.assertEqual(len(emitted), 1, emitted)
        self.assertIn("::error title=Test failed::ERROR: test_something", emitted[0])


if __name__ == "__main__":
    unittest.main()