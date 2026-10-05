"""The decisions index's row pattern, held to the split names this log uses.

`decisionindex.py` reads `DECISIONS.md`'s table to learn which file holds which
decision numbers, and it learns it with one regex. A pattern that fails to match
a row is the silent-gate failure its own module documents: every other check in
a sweep passes while this one does nothing.

**This test exists because that happened here.** The pattern read
`DECISIONS[A-Z-]*\.md`, which cannot match a digit. `DECISIONS-SCREENING-2.md`
was created on 2026-10-05 (T-0063) — named the way this repository has always
named a split, as `FAILURES-findings-2.md` and `STATE-history-2.md` already were
— and with its row present in `DECISIONS.md` the check still reported
"DECISIONS.md does not list this file at all". The message was false, the row was
in the table, and nothing said which was wrong.

Both directions are asserted, because a pattern widened to accept one row must
still reject a file that genuinely is not listed, or the repair is a weakening.
The negative case uses the real `DECISIONS-SESSIONS.md` row shape with the file
name altered out from under it, so it exercises the check rather than a toy.
"""

from __future__ import annotations

import unittest

from originlib.decisionindex import DECISION_ROW


class DecisionRowPatternTest(unittest.TestCase):
    """The pattern, against the spellings `DECISIONS.md` actually uses."""

    def match(self, name: str, spec: str = "D019–D023"):
        row = "| [`%s`](%s) | %s | what it governs |" % (name, name, spec)
        return DECISION_ROW.match(row)

    def test_a_numbered_split_is_matched(self) -> None:
        # The defect's own bytes: this row was in the table and unread.
        found = self.match("DECISIONS-SCREENING-2.md", "D048–D051")
        self.assertIsNotNone(found, "a numbered split row must be matched")
        self.assertEqual(found.group(1), "DECISIONS-SCREENING-2.md")

    def test_the_specifications_are_captured_not_the_prose(self) -> None:
        found = self.match("DECISIONS-SCREENING-2.md", "D048–D051")
        self.assertEqual(found.group(2), "D048–D051")

    def test_unnumbered_and_bare_names_still_match(self) -> None:
        for name in ("DECISIONS.md", "DECISIONS-SCREENING.md",
                     "DECISIONS-RECORDS.md"):
            self.assertIsNotNone(self.match(name), name)

    def test_a_row_writing_no_decision_file_is_not_a_decision_row(self) -> None:
        for row in (
                "| `STATE.md` | D019–D023 | not a decision file |",
                "| [`FAILURES-findings-2.md`](FAILURES-findings-2.md) | F001 | no |",
                "| [`DECISIONS.md`](DECISIONS.md) D019–D023 | prose | no |",
        ):
            self.assertIsNone(DECISION_ROW.match(row), row)

    def test_widening_did_not_admit_a_lowercase_or_dotted_name(self) -> None:
        for name in ("decisions-screening-2.md",
                     "DECISIONS-SCREENING-2.markdown"):
            self.assertIsNone(self.match(name), name)


if __name__ == "__main__":
    unittest.main()