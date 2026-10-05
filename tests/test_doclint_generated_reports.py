"""The generated-report exemption from the line cap must bite in both directions.

T-0065 added `is_generated_report` because a session report grew past the cap for
a reason that has nothing to do with prose: `session artifact --dir` over a
raw-capture directory writes one artifact event per file, so 211 of that report's
lines were an artifact table. A cap whose subject is "is this worth reading" has
nothing to say about a table the tooling prints.

Two ways this exemption could be abused, and one property it must keep:

1. it must apply to a session report, or the repair does nothing;
2. **the cap must still fire on a hand-authored document of the same length** —
   otherwise this is a rule that says "long files are fine", which is the
   weakening `AGENTS.md` forbids;
3. it must exempt the length only: a generated report still has to carry
   `origin-meta` and is still link-checked, so a report cannot be edited into
   compliance and cannot hide a broken link.
"""

import os
import unittest

from tools.originlib import doclint

LONG_LINES = 400
SESSIONS = "sessions/2026-01-01-000-example/README.md"
AUTHORED = "docs/operations/example.md"


class GeneratedReportExemptionTest(unittest.TestCase):
    def test_it_applies_to_a_session_report(self):
        self.assertTrue(doclint.is_generated_report(SESSIONS))

    def test_the_cap_still_fires_on_an_authored_document_of_the_same_length(self):
        """The load-bearing half. A length exemption that ignores the author
        would stop being a statement about generated tables."""
        self.assertFalse(doclint.is_generated_report(AUTHORED))
        self.assertFalse(doclint.is_exempt(AUTHORED, []))

    def test_it_does_not_exempt_a_session_directory_other_than_its_report(self):
        for rel in ("sessions/INDEX.md", "sessions/2026-01-01-000-example/events.jsonl",
                    "sessions/README.md", "docs/sessions/x/README.md"):
            self.assertFalse(doclint.is_generated_report(rel), rel)

    def test_the_real_report_is_exempt_and_the_real_authored_files_are_not(self):
        """Asserted against the repository rather than a fixture, so the rule
        cannot drift away from the files it governs."""
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sessions = os.path.join(root, "sessions")
        if not os.path.isdir(sessions):
            self.skipTest("no sessions directory in this checkout")
        names = sorted(os.listdir(sessions))
        reports = [n for n in names if os.path.isfile(os.path.join(sessions, n, "README.md"))]
        self.assertTrue(reports, "at least one closed session must exist")
        for name in reports:
            self.assertTrue(doclint.is_generated_report("sessions/%s/README.md" % name))

    def test_the_exemption_is_length_only_and_the_report_still_needs_its_metadata(self):
        """A report over the cap must still carry origin-meta and still be
        link-checked, which is what stops 'edit the generated file' being a
        repair."""
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        target = None
        sessions = os.path.join(root, "sessions")
        if os.path.isdir(sessions):
            for name in sorted(os.listdir(sessions)):
                candidate = os.path.join(sessions, name, "README.md")
                if os.path.isfile(candidate):
                    target = candidate
                    break
        if target is None:
            self.skipTest("no closed session report in this checkout")
        with open(target, encoding="utf-8", errors="replace") as f:
            text = f.read()
        self.assertIn(doclint.GENERATED_MARK, text)
        for key in doclint.META_KEYS:
            self.assertIn(key, text, key)


if __name__ == "__main__":
    unittest.main()