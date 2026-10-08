"""What the stream lock does to a stream that was already damaged.

A writer killed mid-line leaves a truncated final line. Two rules govern it and
they pull in opposite directions, so both are pinned here: the number in a line
that never landed is free, and the number in a line that did parse is never
handed out twice. Trusting the bytes of a truncated tail would skip a number on
every crash and leave a permanent gap; ignoring a parsed tail would overwrite an
event that really happened.
"""


from __future__ import annotations

import json
import multiprocessing
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from originlib import events  # noqa: E402


class MalformedTailTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = Path(self.dir.name) / "events.jsonl"

    def test_a_truncated_final_line_is_not_counted_as_a_used_number(self) -> None:
        """A half-written line from a killed writer never landed, so its number
        is free. The opposite choice — trusting the bytes — would skip a number
        on every crash and leave a permanent gap."""
        self.path.write_text(
            '{"schema":"origin.session.event/1","seq":1,"ts":"t","session":"s",'
            '"kind":"note","data":{}}\n{"seq":2,"kind":"trunc\n',
            encoding="utf-8",
        )
        self.assertEqual(events.next_seq(self.path), 2)
        events.append("s", "note", {"summary": "after the crash"}, path=self.path)
        self.assertEqual(self._numbers(), [1, 2])

    def test_a_valid_tail_number_is_never_reallocated(self) -> None:
        """The converse: a line that did parse must not be written over."""
        events.append("s", "note", {"summary": "one"}, path=self.path)
        events.append("s", "note", {"summary": "two"}, path=self.path)
        events.append("s", "note", {"summary": "three"}, path=self.path)
        self.assertEqual(self._numbers(), [1, 2, 3])

    def _numbers(self) -> list[int]:
        return [
            e["seq"]
            for e in events.read(self.path)
            if isinstance(e.get("seq"), int)
        ]


if __name__ == "__main__":
    unittest.main()

if __name__ == "__main__":
    unittest.main()
