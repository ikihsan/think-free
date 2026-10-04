"""The shapes T-0056's rule must read, and the ones it must decline (T-0056).

Defect 22 in `STATE-defects.md`. `docs/process/experiment-protocol.md` said
`005-knitting-bounded-search` "reproduces the oracle on 113/113 checked cases"
while that experiment's `results.json` says `cases_with_oracle = 115` and
`cases_tested = 118`. The wrong number was published in the same commit as the
artifact (`318374a`), so no later edit introduced it and every gate passed: no
rule read a number in a mission record against the result it restates.

The half that reads real committed bytes — the false negative of the obvious
rule, and the two directions of the repair — is in
`test_result_numbers_falsified.py`, split at the line cap. This half builds the
shapes, including every one the rule must **not** report, because a rule tested
only on what it should catch says nothing about whether it can be satisfied.
"""

from __future__ import annotations

import json
import unittest

from harness import RepoTest

from originlib import doclint, resultnumbers

SLUG = "900-example"


class ResultFixture(RepoTest):
    """A throwaway tree with an experiment artifact and a results index to check."""

    def artifact(self, data: dict, slug: str = SLUG) -> None:
        directory = self.repo / "EXPERIMENTS" / slug
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "results.json").write_text(json.dumps(data), encoding="utf-8")

    def raw_artifact(self, text: str, slug: str = SLUG) -> None:
        directory = self.repo / "EXPERIMENTS" / slug
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "results.json").write_text(text, encoding="utf-8")

    def index(self, body: str, rel: str = "results.md") -> None:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"# Results\n\n<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\n"
            f"last-verified: 2026-10-04\n-->\n\n{body}\n",
            encoding="utf-8",
        )

    def check(self) -> list:
        return resultnumbers.issues(self.repo, doclint.tracked_files(self.repo))


class ReportedTest(ResultFixture):
    """The shapes that must be reported, one per decidable reading of a number."""

    def test_a_fraction_whose_denominator_is_not_a_declared_count_is_reported(self) -> None:
        self.artifact({"cases_tested": 10, "cases_with_oracle": 9})
        self.index("| `900-example` | exact on 11/11 cases. |")
        found = self.check()
        self.assertEqual(len(found), 1, [str(item) for item in found])
        self.assertIn("11/11", found[0])
        self.assertEqual(found[0].path, "results.md")

    def test_a_decimal_the_artifact_does_not_state_is_reported(self) -> None:
        self.artifact({"cases_tested": 10})
        self.index("| `900-example` | met at 0.965. |")
        found = self.check()
        self.assertEqual(len(found), 1, [str(item) for item in found])
        self.assertIn("0.965", found[0])

    def test_a_decimal_ending_a_sentence_is_still_read(self) -> None:
        # The first version of the decimal guard rejected any following dot, so
        # it silently discarded every number that ended a sentence — and a gate
        # that reads nothing looks exactly like a clean tree. Found by this test
        # returning zero findings.
        self.artifact({"cases_tested": 10})
        self.index("| `900-example` | met at 0.965. |")
        found = self.check()
        self.assertEqual(len(found), 1, [str(item) for item in found])

    def test_a_version_written_in_a_results_row_is_reported_not_exempt(self) -> None:
        # `2.30` is a real git version and is not in this artifact. A version and
        # a measurement are the same shape and no rule can tell them apart, so
        # this is reported rather than exempted behind a keyword list — which is
        # a stated ceiling with a stated remedy, not a silent false positive.
        self.artifact({"cases_tested": 10})
        self.index("| `900-example` | measured on git 2.30 |")
        found = self.check()
        self.assertEqual(len(found), 1, [str(item) for item in found])
        self.assertIn("2.30", found[0])

    def test_an_artifact_that_cannot_be_read_is_reported_not_skipped(self) -> None:
        # D025's second obligation: a parser that quietly stops matching looks
        # exactly like a clean tree.
        self.raw_artifact("{not json")
        self.index("| `900-example` | exact on 9/9 cases. |")
        found = self.check()
        self.assertEqual(len(found), 1, [str(item) for item in found])
        self.assertIn("cannot be read", found[0])


class SilentTest(ResultFixture):
    """The shapes that must stay quiet, which is what makes the rule runnable."""

    def test_a_fraction_the_artifact_declares_is_silent(self) -> None:
        self.artifact({"cases_tested": 10, "cases_with_oracle": 9})
        self.index("| `900-example` | exact on 9/9 cases. |")
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_denominator_named_only_by_a_per_setting_count_is_silent(self) -> None:
        # The negative half of the defect's own false negative: `patch_cost` in
        # 005 holds 3, and a row may legitimately state 3 without the rule
        # objecting, because `3` there is not a claim about how many cases.
        self.artifact({"cases_tested": 10, "patch_cost": 3})
        self.index("| `900-example` | at patch cost 3. |")
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_decimal_the_artifact_states_is_silent_however_deeply_it_sits(self) -> None:
        # `006`'s 0.833 is three levels down, under its own kill gate. A decimal
        # is distinctive, so it is matched against every value rather than only
        # the top-level ones a "headline" restriction would allow.
        self.artifact({"kill_gate": {"1": {"fixed": 0.833, "adaptive": 0.792}}})
        self.index("| `900-example` | fixed 0.833 beats adaptive 0.792. |")
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_three_part_version_is_not_read_as_a_decimal(self) -> None:
        self.artifact({"cases_tested": 10})
        self.index("| `900-example` | ran on CPython 3.8.10. |")
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_bare_integer_is_not_checked(self) -> None:
        # A bare small integer is ambiguous — a threshold, a version, a count of
        # something else — so the rule reads only fractions and decimals. Stated
        # as a ceiling rather than left to surprise the next reader.
        self.artifact({"cases_tested": 10})
        self.index("| `900-example` | declared 5% gate. |")
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_row_naming_two_experiments_is_not_attributed(self) -> None:
        # Which experiment a number belongs to is undecidable here, so the rule
        # must not guess: a guessed attribution is a false report.
        self.artifact({"cases_tested": 10})
        self.index("| `900-example` and `901-other` | 99/99 cases. |")
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_row_naming_an_experiment_with_no_artifact_is_silent(self) -> None:
        self.index("| `900-example` | 99/99 cases. |")
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_generated_document_is_not_a_claim(self) -> None:
        self.artifact({"cases_tested": 10})
        self.index(
            "<!-- generated-by: origin; do not edit by hand -->\n"
            "| `900-example` | exact on 11/11 cases. |"
        )
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_prose_line_is_not_read(self) -> None:
        # A stated ceiling: only a row is an attributable claim. Asserted so it
        # reads as a decision rather than as an oversight.
        self.artifact({"cases_tested": 10})
        self.index("The `900-example` experiment was exact on 11/11 cases.")
        self.assertEqual([str(item) for item in self.check()], [])


if __name__ == "__main__":
    unittest.main()