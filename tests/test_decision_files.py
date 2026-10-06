"""Two hand-maintained lists of the decision log, held to the files on disk.

`tools/originlib/paths.py` and `tools/originlib/reconcile.py` each name every
`DECISIONS*.md` file, for different reasons: the first decides which records a
session's documentation obligation covers, the second which of them satisfy a
recorded `decision` event. The log was split six times, and each split added a
file to both lists by hand — the sixth, `DECISIONS-RECORDS.md` on 2026-10-04
(T-0042), is the first that did not have to be remembered in two places at once,
because a list nobody checks is the same shape as the identifier list T-0036
found unread.

`DECISION_FILES` below is a *third* copy, and it is the one that earns its keep:
T-0054 added `DECISIONS-PUBLISHING.md` to the two tuples and this module failed
until the third was updated, naming the file rather than a count. A gate that
compares counts tells you a number changed; this one tells you which file.
`DECISIONS-SCREENING-2.md` is the seventh split and it earned its keep twice: it
is the first split whose name carries a digit, and `decisionindex.py`'s row
pattern could not read it until T-0063 widened it — see
`test_decision_row_pattern.py`. `DECISIONS-SCREENING-3.md` is the eighth, added
2026-10-05 for D052, and it earned the gate its keep immediately: creating the
file left all three lists short of it and this module failed naming the file.
`DECISIONS-SCREENING-4.md` is the ninth, added 2026-10-05 for D059–D060, and it
did the same thing the third time: the file existed, the three lists did not
name it, and this module failed with the file's name in the message rather than
a count. `DECISIONS-SCREENING-5.md` is the tenth, added 2026-10-06 for D062, and
it earned the gate its keep a fourth time in exactly the same way.

This is bookkeeping hygiene and says nothing about any candidate. What it buys
is narrow and real: a seventh split cannot leave a decision file that no
documentation obligation reaches, which would make a recorded decision satisfy a
gate by changing nothing.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from originlib import paths, reconcile

DECISION_FILES = (
    "DECISIONS.md",
    "DECISIONS-FOUNDATION.md",
    "DECISIONS-PRACTICE.md",
    "DECISIONS-SCREENING.md",
    "DECISIONS-SCREENING-2.md",
    "DECISIONS-SCREENING-3.md",
    "DECISIONS-SCREENING-4.md",
    "DECISIONS-SCREENING-5.md",
    "DECISIONS-GATING.md",
    "DECISIONS-SESSIONS.md",
    "DECISIONS-PUBLISHING.md",
    "DECISIONS-RECORDS.md",
)


class DecisionFileListTest(unittest.TestCase):
    """The real repository, because the lists name this repository's files."""

    def root(self) -> Path:
        root = Path(paths.repo_root())
        if root != Path(__file__).resolve().parent.parent:
            self.skipTest("running against a fixture repository, not the real one")
        return root

    def on_disk(self) -> set[str]:
        return {p.name for p in self.root().glob("DECISIONS*.md") if p.is_file()}

    def test_the_mission_record_list_covers_every_decision_file(self) -> None:
        listed = {name for name in paths.MISSION_RECORDS if name.startswith("DECISIONS")}
        self.assertEqual(sorted(self.on_disk() - listed), [], "a decision file no session obligation reaches")

    def test_the_mission_record_list_names_nothing_absent(self) -> None:
        listed = {name for name in paths.MISSION_RECORDS if name.startswith("DECISIONS")}
        self.assertEqual(sorted(listed - self.on_disk()), [], "a decision file listed but not present")

    def test_both_lists_name_the_same_files(self) -> None:
        records = {name for name in paths.MISSION_RECORDS if name.startswith("DECISIONS")}
        records.add("DECISIONS.md")
        self.assertEqual(sorted(records), sorted(DECISION_FILES))

    def test_a_decision_event_is_satisfied_by_any_decision_file(self) -> None:
        mode, records = reconcile.IMPLICATIONS["decision"]
        self.assertEqual(mode, "any")
        self.assertEqual(sorted(records), sorted(DECISION_FILES))


if __name__ == "__main__":
    unittest.main()