"""The falsification half: T-0056's rule against the bytes the defect is in.

Split out of `test_result_numbers.py` at the 300-line cap, which the unit-shape
half reached. The division is by what each half needs: this one needs the real
repository's committed history, because the defect was repaired here and a test
that read the working tree would have started failing the moment the repair
landed — and would then have been deleted rather than kept, which is how a gate
loses its control.

Three things are asserted, and the first is the one that matters most:

* `LooseRuleTest` proves the **rejected** rule is blind. "Does this number occur
  anywhere in the artifact?" answers *yes* for `113`, because that value also
  sits at `patch_cost_sensitivity/*/cases` in the artifact that says
  `cases_with_oracle: 115`. A gate built on it would be green on the very defect
  it was written for.
* the same class asserts the rule **reports** the defect row and is **silent** on
  the repaired one. Only the second direction proves a rule can be satisfied.
* `RealTreeTest` holds the silence to a count of the rows actually read, so
  "reports nothing" cannot mean "read almost nothing" — the failure T-0030's
  decision-index check had across 174 commits.
"""

from __future__ import annotations

import json
import subprocess
import unittest

from harness import SOURCE_ROOT

from originlib import doclint, resultnumbers

REAL_ROOT = SOURCE_ROOT
SLUG = "005-knitting-bounded-search"
PATH = "docs/process/experiment-protocol.md"


def artifact() -> dict:
    return json.loads(
        (REAL_ROOT / "EXPERIMENTS" / SLUG / "results.json").read_text(encoding="utf-8")
    )


def row_in(text: str) -> str:
    """The one table row naming this experiment, out of a document's text."""
    for line in text.splitlines():
        if line.startswith("|") and SLUG in line:
            return line
    raise AssertionError(f"no row naming {SLUG}")


class LooseRuleTest(unittest.TestCase):
    """The rejected rule, asserted to be blind, on the defect's own bytes.

    The defect's bytes are read from the commit that published the artifact
    (`318374a`), not from the working tree: the tree is repaired by now.

    **The literal row is carried here as a fallback, and that is deliberate.**
    `tools/mutate_result_rule.py` runs this file in a throwaway copy of the tree
    with a single fresh commit, where `318374a` does not exist; without the
    literal, a green run there would depend on the ambient repository rather than
    on this file. `test_the_literal_matches_the_committed_defect` is what keeps
    the two from drifting, and it is skipped — not silently passed — when the
    commit is genuinely unreachable.
    """

    COMMIT = "318374a"
    LITERAL = (
        "| `005-knitting-bounded-search` | Whole-neighbourhood search reproduces "
        "the oracle on 113/113 checked cases; cheaper settings are not, and two "
        "\"optimal\" settings are exhaustive search in disguise. |"
    )

    def _committed(self):
        result = subprocess.run(
            ["git", "show", f"{self.COMMIT}:{PATH}"],
            cwd=str(REAL_ROOT),
            capture_output=True,
            text=True,
        )
        return row_in(result.stdout) if result.returncode == 0 else None

    def defect_row(self) -> str:
        return self._committed() or self.LITERAL

    def test_the_literal_matches_the_committed_defect(self) -> None:
        committed = self._committed()
        if committed is None:
            self.skipTest(f"{self.COMMIT} is not in this clone; the literal stands alone")
        self.assertEqual(committed, self.LITERAL)

    def test_a_number_occurring_anywhere_in_the_artifact_misses_the_defect(self) -> None:
        """The false negative, on the real bytes.

        If the loose rule ever *does* catch this, the declared-count restriction
        in `resultnumbers` is no longer carrying anything and this should say so.
        """
        data = artifact()
        self.assertTrue(
            resultnumbers.stated("113", resultnumbers.every_value(data)),
            "if 113 is no longer anywhere in the artifact, this control is void",
        )
        self.assertFalse(
            resultnumbers.stated("113", resultnumbers.declared_counts(data)),
            "the restriction must be what makes the rule see the defect",
        )

    def test_the_rule_reports_the_defect_row_it_is_given(self) -> None:
        """The positive direction, on the same bytes read out of git."""
        data = artifact()
        found = resultnumbers.row_issues(
            self.defect_row(),
            SLUG,
            resultnumbers.declared_counts(data),
            resultnumbers.every_value(data),
        )
        self.assertEqual(len(found), 1, [str(item) for item in found])
        self.assertIn("113/113", str(found[0]))

    def test_the_rule_is_silent_on_the_repaired_row(self) -> None:
        """A rule nobody can satisfy is a gate nobody runs.

        Read from the working tree rather than from `HEAD`, so it asserts the
        repair this task made and keeps asserting it once the repair is committed.
        """
        data = artifact()
        repaired = row_in((REAL_ROOT / PATH).read_text(encoding="utf-8"))
        self.assertIn("115/115", repaired, "the repaired row carries the artifact's count")
        self.assertEqual(
            resultnumbers.row_issues(
                repaired,
                SLUG,
                resultnumbers.declared_counts(data),
                resultnumbers.every_value(data),
            ),
            [],
        )


class RealTreeTest(unittest.TestCase):
    """The rule on this repository's own documents, where the repair has landed."""

    def setUp(self) -> None:
        self.files = doclint.tracked_files(REAL_ROOT)

    def rows_read(self) -> int:
        read = 0
        for path in self.files:
            if path.suffix != ".md" or "<!-- generated-by:" in path.read_text(
                encoding="utf-8", errors="replace"
            ):
                continue
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("|") and len(set(resultnumbers.SLUG.findall(line))) == 1:
                    read += 1
        return read

    def test_the_rule_reads_the_results_index_and_not_almost_nothing(self) -> None:
        self.assertGreaterEqual(self.rows_read(), 9, "the results index shrank")

    def test_doc_lint_is_silent_on_the_repaired_tree(self) -> None:
        found = resultnumbers.issues(REAL_ROOT, self.files)
        self.assertEqual([str(item) for item in found], [])

    def test_the_artifact_this_test_depends_on_still_declares_what_it_did(self) -> None:
        data = artifact()
        self.assertEqual(data["cases_with_oracle"], 115)
        self.assertEqual(data["cases_tested"], 118)


if __name__ == "__main__":
    unittest.main()