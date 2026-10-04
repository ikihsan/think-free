"""A restated experiment number, held to the artifact it names (T-0056).

Defect 22 in `STATE-defects.md`. `docs/process/experiment-protocol.md` said
`005-knitting-bounded-search` "reproduces the oracle on 113/113 checked cases"
while that experiment's `results.json` says `cases_with_oracle = 115` and
`cases_tested = 118`. The wrong number was published in the same commit as the
artifact (`318374a`), so no later edit introduced it and every gate passed.

The falsifications here are the ones the defect demands, and two of them are
about the rule rather than the record:

* **CommittedDefectTest** reads the row out of git rather than from a fixture
  written after the repair, and asserts the rule reports it — then that the
  repaired row is silent.
* **LooseRuleTest** asserts the *rejected* rule cannot see the defect. The
  obvious repair — "does this number occur anywhere in the artifact?" — answers
  yes, because `113` also sits at `patch_cost_sensitivity/*/cases`. A gate that
  passes here would be D025's shape again: reading a field that happens to hold
  the value and concluding about the property being claimed.
* **NoRegressionTest** counts what the rule read. A gate that reports nothing on
  a tree it has never examined is indistinguishable from a gate that cannot fail,
  which is the failure T-0030's decision-index check had.
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from harness import SOURCE_ROOT, RepoTest, git

from originlib import doclint, resultnumbers

REAL_ROOT = SOURCE_ROOT
SLUG = "005-knitting-bounded-search"
ROW = (
    "| `005-knitting-bounded-search` | Whole-neighbourhood search reproduces the "
    "oracle on 115/115 checked cases; cheaper settings are not. |"
)


def row_in(text: str) -> str:
    """The one table row naming this experiment, out of a document's text."""
    for line in text.splitlines():
        if line.startswith("|") and SLUG in line:
            return line
    raise AssertionError(f"no row naming {SLUG}")


def committed_row(path: str) -> str:
    """One line of a document, read out of git rather than from the tree."""
    out = subprocess.run(
        ["git", "show", f"HEAD:{path}"],
        cwd=str(REAL_ROOT),
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return row_in(out)


def tree_row(path: str) -> str:
    """The same row as the working tree currently holds it — the repair."""
    return row_in((REAL_ROOT / path).read_text(encoding="utf-8"))


class ResultFixture(RepoTest):
    """A throwaway tree with an experiment artifact and a results index to check."""

    def artifact(self, slug: str, data: dict) -> None:
        directory = self.repo / "EXPERIMENTS" / slug
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "results.json").write_text(json.dumps(data), encoding="utf-8")

    def raw_artifact(self, slug: str, text: str) -> None:
        directory = self.repo / "EXPERIMENTS" / slug
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "results.json").write_text(text, encoding="utf-8")

    def index(self, body: str, rel: str = "results.md") -> Path:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"# Results\n\n<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\n"
            f"last-verified: 2026-10-04\n-->\n\n{body}\n",
            encoding="utf-8",
        )
        return path

    def check(self) -> list:
        return resultnumbers.issues(self.repo, doclint.tracked_files(self.repo))


class UnitTest(ResultFixture):
    """The rule on artifacts built for it, including the shapes it must reject."""

    def test_a_fraction_whose_denominator_is_not_a_declared_count_is_reported(self) -> None:
        self.artifact("900-example", {"cases_tested": 10, "cases_with_oracle": 9})
        self.index("| `900-example` | exact on 11/11 cases. |")
        found = self.check()
        self.assertEqual(len(found), 1, [str(item) for item in found])
        self.assertIn("11/11", found[0])

    def test_a_fraction_the_artifact_declares_is_silent(self) -> None:
        self.artifact("900-example", {"cases_tested": 10, "cases_with_oracle": 9})
        self.index("| `900-example` | exact on 9/9 cases. |")
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_decimal_the_artifact_states_is_silent_however_deeply_it_sits(self) -> None:
        # `006`'s 0.833 is three levels down, under its own kill gate. A decimal
        # is distinctive, so it is matched against every value rather than only
        # the top-level ones a "headline" restriction would allow.
        self.artifact("900-example", {"kill_gate": {"1": {"fixed": 0.833, "adaptive": 0.792}}})
        self.index("| `900-example` | fixed 0.833 beats adaptive 0.792. |")
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_decimal_the_artifact_does_not_state_is_reported(self) -> None:
        self.artifact("900-example", {"cases_tested": 10})
        self.index("| `900-example` | met at 0.965. |")
        found = self.check()
        self.assertEqual(len(found), 1, [str(item) for item in found])
        self.assertIn("0.965", found[0])

    def test_a_row_naming_two_experiments_is_not_attributed(self) -> None:
        # Which experiment a number belongs to is undecidable here, so the rule
        # must not guess: a guessed attribution is a false report.
        self.artifact("900-example", {"cases_tested": 10})
        self.index("| `900-example` and `901-other` | 99/99 cases. |")
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_row_naming_an_experiment_with_no_artifact_is_silent(self) -> None:
        self.index("| `900-example` | 99/99 cases. |")
        self.assertEqual([str(item) for item in self.check()], [])

    def test_an_artifact_that_cannot_be_read_is_reported_not_skipped(self) -> None:
        # D025's second obligation: a parser that quietly stops matching looks
        # exactly like a clean tree.
        self.raw_artifact("900-example", "{not json")
        self.index("| `900-example` | exact on 9/9 cases. |")
        found = self.check()
        self.assertEqual(len(found), 1, [str(item) for item in found])
        self.assertIn("cannot be read", found[0])

    def test_a_generated_document_is_not_a_claim(self) -> None:
        self.artifact("900-example", {"cases_tested": 10})
        self.index(
            "<!-- generated-by: origin; do not edit by hand -->\n"
            "| `900-example` | exact on 11/11 cases. |"
        )
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_bare_integer_is_not_checked(self) -> None:
        # A bare small integer is ambiguous — a threshold, a version, a count of
        # something else — so the rule reads only fractions and decimals. Stated
        # as a ceiling rather than left to surprise the next reader.
        self.artifact("900-example", {"cases_tested": 10})
        self.index("| `900-example` | declared 5% gate. |")
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_decimal_ending_a_sentence_is_still_read(self) -> None:
        # The first version of the decimal guard rejected any following dot,
        # which silently discarded every number that ended a sentence — and a
        # gate that reads nothing looks exactly like a clean tree.
        self.artifact("900-example", {"cases_tested": 10})
        self.index("| `900-example` | met at 0.965. |")
        found = self.check()
        self.assertEqual(len(found), 1, [str(item) for item in found])
        self.assertIn("0.965", found[0])

    def test_a_three_part_version_is_not_read_as_a_decimal(self) -> None:
        self.artifact("900-example", {"cases_tested": 10})
        self.index("| `900-example` | ran on CPython 3.8.10. |")
        self.assertEqual([str(item) for item in self.check()], [])

    def test_a_version_written_in_a_results_row_is_reported_not_exempt(self) -> None:
        # `2.30` is a real git version and is not in this artifact. A version and
        # a measurement are the same shape, and no rule can tell them apart, so
        # this is reported rather than exempted behind a keyword list — which is
        # a stated ceiling with a stated remedy (environment belongs outside the
        # results table), not a silent false positive. Asserted so the ceiling is
        # a tested property rather than a surprise for the next writer.
        self.artifact("900-example", {"cases_tested": 10})
        self.index("| `900-example` | measured on git 2.30 |")
        found = self.check()
        self.assertEqual(len(found), 1, [str(item) for item in found])
        self.assertIn("2.30", found[0])


class LooseRuleTest(unittest.TestCase):
    """The rejected rule, asserted to be blind, on the defect's own bytes.

    The defect's bytes are read from the commit that published the artifact
    (`318374a`), not from the working tree: the tree is repaired by now, and a
    test that read the tree would start failing the moment the repair landed and
    would then be deleted rather than kept — which is how a gate loses its
    control.

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

    def _committed(self, ref: str):
        result = subprocess.run(
            ["git", "show", f"{ref}:docs/process/experiment-protocol.md"],
            cwd=str(REAL_ROOT),
            capture_output=True,
            text=True,
        )
        return row_in(result.stdout) if result.returncode == 0 else None

    def defect_row(self) -> str:
        return self._committed(self.COMMIT) or self.LITERAL

    def test_the_literal_matches_the_committed_defect(self) -> None:
        committed = self._committed(self.COMMIT)
        if committed is None:
            self.skipTest(f"{self.COMMIT} is not in this clone; the literal stands alone")
        self.assertEqual(committed, self.LITERAL)

    def test_the_defect_is_in_the_commit_that_published_the_artifact(self) -> None:
        self.assertIn("113/113", self.defect_row())

    def test_a_number_occurring_anywhere_in_the_artifact_misses_the_defect(self) -> None:
        """The false negative, on the real bytes.

        If the loose rule ever *does* catch this, the declared-count restriction
        in `resultnumbers` is no longer carrying anything and this should say so.
        """
        artifact = json.loads(
            (REAL_ROOT / "EXPERIMENTS" / SLUG / "results.json").read_text(encoding="utf-8")
        )
        self.assertTrue(
            resultnumbers.stated("113", resultnumbers.every_value(artifact)),
            "if 113 is no longer anywhere in the artifact, this control is void",
        )
        self.assertFalse(
            resultnumbers.stated("113", resultnumbers.declared_counts(artifact)),
            "the restriction must be what makes the rule see the defect",
        )

    def test_the_rule_reports_the_defect_row_it_is_given(self) -> None:
        """The positive direction, on the same bytes read out of git."""
        artifact = json.loads(
            (REAL_ROOT / "EXPERIMENTS" / SLUG / "results.json").read_text(encoding="utf-8")
        )
        found = resultnumbers.row_issues(
            self.defect_row(),
            SLUG,
            resultnumbers.declared_counts(artifact),
            resultnumbers.every_value(artifact),
        )
        self.assertEqual(len(found), 1, [str(item) for item in found])
        self.assertIn("113/113", str(found[0]))

    def test_the_rule_is_silent_on_the_repaired_row(self) -> None:
        """The second direction: a rule nobody can satisfy is a gate nobody runs.

        Read from the working tree rather than from `HEAD`, so it asserts the
        repair this task made and keeps asserting it once the repair is
        committed — which is the whole point of asserting the silent direction.
        """
        artifact = json.loads(
            (REAL_ROOT / "EXPERIMENTS" / SLUG / "results.json").read_text(encoding="utf-8")
        )
        repaired = tree_row("docs/process/experiment-protocol.md")
        self.assertIn("115/115", repaired, "the repaired row should carry the artifact's count")
        self.assertEqual(
            resultnumbers.row_issues(
                repaired,
                SLUG,
                resultnumbers.declared_counts(artifact),
                resultnumbers.every_value(artifact),
            ),
            [],
        )


class RealTreeTest(unittest.TestCase):
    """The rule on this repository's own documents, where the repair has landed.

    Silent here is the required result, and it is only meaningful next to the
    count of rows the rule actually read — otherwise "reports nothing" and
    "read almost nothing" are the same sentence, which is how T-0030's
    decision-index check passed for 174 commits while matching no row at all.
    """

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
        artifact = json.loads(
            (REAL_ROOT / "EXPERIMENTS" / SLUG / "results.json").read_text(encoding="utf-8")
        )
        self.assertEqual(artifact["cases_with_oracle"], 115)
        self.assertEqual(artifact["cases_tested"], 118)


if __name__ == "__main__":
    unittest.main()