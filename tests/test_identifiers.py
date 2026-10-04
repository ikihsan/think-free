"""Identifier-collision detection: what must fire, what must not, and the control.

The rule this tests exists because two VMs allocate a finding, decision or task
number from their own tree, so the same number reaches the shared base twice. It
happened seven times in two days (defect 5 in `STATE-defects.md`), and commit
`e6eb992` carries the result: two different findings both numbered `F010`. No
gate reported it.

This file tests the rule. `test_identifier_enforcement.py` tests where it is read:
this repository's own record, `doc lint`, and `sync land`.

The fixture text below is quoted from that commit's own bytes. A rule that has
only been checked against a tree an author just built is a rule nobody trusts
(D025), so `ThisRepositoryTest` reads the real record and `ControlTest` carries
the one shape that must stay silent — the two index rows this repository
deliberately paraphrases. Comparing wording instead of identity flagged 83 of 162
commits including the tip, which is how the control was found.
"""

from __future__ import annotations

import unittest

from harness import RepoTest

from originlib import identifiers

# Verbatim from e6eb992:FAILURES-findings-2.md, both headings, in the order the
# file holds them. The first was VM 0944's E3 census finding, the second VM
# 0947's sync-land defect, and both claimed F010 within the same hour.
COLLIDING_FINDINGS = """\
# Failures — recorded findings, part 2 (F009 onwards)

## F009 — The knitting planner's algorithmic advantage is prior art, not a gap

Prose that mentions F010 in passing is not a definition.

## F010 — E3's predeclared timestamp gate is near-vacuous: prevalence measured, attribution not

Source: `EXPERIMENTS/007-build-timestamps/`, T-0013.

## F010 — `sync land` broke on git >= 2.26, and 60 CI runs failed for that reason

Source: T-0016, `tools/originlib/sync.py`.
"""

# Verbatim from e6eb992:FAILURES.md, whose index also carried the id twice.
COLLIDING_INDEX = """\
# Failures and negative results

| Id | Subject |
|---|---|
| F009 | Knitting repair planner: the algorithmic advantage is prior art |
| F010 | E3's predeclared timestamp gate is near-vacuous: prevalence measured, attribution not |
| F010 | `sync land` broke on git >= 2.26, and every CI run failed for that reason |
"""

# The state the same tree reached one commit later, in 8a4ab8cef: the newer
# finding renumbered to F011 in the body and in the index together.
REPAIRED_FINDINGS = COLLIDING_FINDINGS.replace(
    "## F010 — `sync land` broke on git >= 2.26, and 60 CI runs failed for that reason",
    "## F011 — `sync land` broke on git >= 2.26, and 60 CI runs failed for that reason",
)
REPAIRED_INDEX = COLLIDING_INDEX.replace(
    "| F010 | `sync land` broke on git >= 2.26, and every CI run failed for that reason |",
    "| F011 | `sync land` broke on git >= 2.26, and every CI run failed for that reason |",
)


class CollisionTest(RepoTest):
    """The bytes of the commit that reached the shared base must be reported."""

    def colliding(self) -> None:
        self.write("FAILURES-findings-2.md", COLLIDING_FINDINGS)
        self.write("FAILURES.md", COLLIDING_INDEX)

    def test_two_findings_with_one_number_are_reported(self) -> None:
        self.colliding()
        found = identifiers.report(self.repo)
        self.assertEqual(len(found), 2, found)
        self.assertIn("F010: defined more than once", found[0])
        # The report must locate both definitions, or a reader cannot renumber
        # without opening the file and searching.
        self.assertIn("FAILURES-findings-2.md:7", found[0])
        self.assertIn("FAILURES-findings-2.md:11", found[0])

    def test_the_duplicate_index_row_is_reported_too(self) -> None:
        self.colliding()
        found = identifiers.report(self.repo)
        self.assertTrue(any("indexed on 2 lines" in line for line in found), found)

    def test_the_hand_repair_one_commit_later_is_clean(self) -> None:
        self.write("FAILURES-findings-2.md", REPAIRED_FINDINGS)
        self.write("FAILURES.md", REPAIRED_INDEX)
        self.assertEqual(identifiers.report(self.repo), [])

    def test_a_collision_across_two_files_is_one_collision(self) -> None:
        self.write("FAILURES-findings.md", "## F013 — Three mission records kept a conflict marker\n")
        self.write("FAILURES-findings-3.md", "## F013 — A different finding with the same number\n")
        self.write("FAILURES.md", "| Id | Subject |\n|---|---|\n| F013 | one |\n")
        found = identifiers.report(self.repo)
        self.assertEqual(len(found), 1, found)
        self.assertIn("defined more than once", found[0])


class IndexAgreementTest(RepoTest):
    """An index row and the body it points at are one record, not two."""

    BODY = "## F001 — The motivating example is not evidence\n"

    def test_a_finding_with_no_index_row_is_reported(self) -> None:
        self.write("FAILURES-findings.md", self.BODY)
        self.write("FAILURES.md", "| Id | Subject |\n|---|---|\n")
        found = identifiers.report(self.repo)
        self.assertTrue(any("absent from the FAILURES.md index" in line for line in found), found)

    def test_an_index_row_with_no_finding_is_reported(self) -> None:
        self.write("FAILURES-findings.md", self.BODY)
        self.write("FAILURES.md", "| Id | Subject |\n|---|---|\n| F001 | x |\n| F002 | y |\n")
        found = identifiers.report(self.repo)
        self.assertTrue(any("F002" in line and "nothing defines it" in line for line in found), found)

    def test_no_index_at_all_is_not_a_collision(self) -> None:
        # The index arrived after the first findings. A tree with findings and no
        # index is a gap the orphan and link rules read, not a collision.
        self.write("FAILURES-findings.md", self.BODY)
        self.assertEqual(identifiers.report(self.repo), [])

    def test_a_decision_missing_from_the_index_is_reported(self) -> None:
        self.write("DECISIONS-GATING.md", "## D030 — first\n")
        self.write(
            "DECISIONS.md",
            "| File | Decisions | Governs |\n|---|---|---|\n"
            "| [`DECISIONS-FOUNDATION.md`](DECISIONS-FOUNDATION.md) | D001-D010 | mission |\n",
        )
        found = identifiers.report(self.repo)
        self.assertTrue(
            any("D030" in line or "DECISIONS-GATING.md" in line for line in found), found
        )
        self.assertTrue(
            any("lists D001" in line and "no decision record defines it" in line
                for line in found), found
        )

    def test_an_index_range_covers_the_entries_it_names(self) -> None:
        body = "## D030 — first\n\n## D031 — second\n"
        self.write("DECISIONS-GATING.md", body)
        self.write(
            "DECISIONS.md",
            "| File | Decisions | Governs |\n|---|---|---|\n"
            "| [`DECISIONS-GATING.md`](DECISIONS-GATING.md) | D030-D031 | gates |\n",
        )
        self.assertEqual(identifiers.report(self.repo), [])

    def test_a_single_decision_outside_the_declared_range_is_reported(self) -> None:
        self.write("DECISIONS-GATING.md", "## D030 — first\n\n## D032 — third\n")
        self.write(
            "DECISIONS.md",
            "| File | Decisions | Governs |\n|---|---|---|\n"
            "| [`DECISIONS-GATING.md`](DECISIONS-GATING.md) | D030-D031 | gates |\n",
        )
        found = identifiers.report(self.repo)
        self.assertTrue(any("D032" in line for line in found), found)


class TaskTest(RepoTest):
    """Task numbers are allocated from the local tree too, so they collide too."""

    def test_two_task_files_with_one_number_are_reported(self) -> None:
        self.write("tasks/T-0001-first-claim.md", "# T-0001\n")
        self.write("tasks/T-0001-second-claim.md", "# T-0001\n")
        found = identifiers.report(self.repo)
        self.assertEqual(len(found), 1, found)
        self.assertIn("T-0001: defined more than once", found[0])

    def test_one_task_file_per_number_is_clean(self) -> None:
        self.write("tasks/T-0001-first-claim.md", "# T-0001\n")
        self.write("tasks/T-0002-second-claim.md", "# T-0002\n")
        self.assertEqual(identifiers.report(self.repo), [])


class ControlTest(RepoTest):
    """The control: a rule reading wording instead of identity would fail here."""

    def test_a_deliberate_paraphrase_of_an_index_row_is_not_a_collision(self) -> None:
        # These two rows exist in this repository today, shortened on purpose:
        # `F009` drops "not a gap", `F011` says "every CI run" where its heading
        # says "60 CI runs". String equality flagged 83 of 162 commits on this.
        body = (
            "## F009 — The knitting planner's algorithmic advantage is prior art, not a gap\n\n"
            "## F011 — `sync land` broke on git >= 2.26, and 60 CI runs failed for that reason\n"
        )
        self.write("FAILURES-findings-2.md", body)
        self.write(
            "FAILURES.md",
            "| Id | Subject |\n|---|---|\n"
            "| F009 | Knitting repair planner: the algorithmic advantage is prior art |\n"
            "| F011 | `sync land` broke on git >= 2.26, and every CI run failed for that reason |\n",
        )
        self.assertEqual(identifiers.report(self.repo), [])

    def test_a_prose_mention_is_not_a_definition(self) -> None:
        # Sessions, tables and cross-references talk about F010 constantly. Only
        # a level-2 heading in a root record defines it.
        self.write("FAILURES-findings.md", "## F010 — The real finding\n")
        self.write("RESEARCH/E.md", "## F010 is cited here, and ## F011 too\n")
        self.write("STATE.md", "F010 and F011 are both referenced in prose.\n")
        self.write("FAILURES.md", "| Id | Subject |\n|---|---|\n| F010 | The real finding |\n")
        self.assertEqual(identifiers.report(self.repo), [])


if __name__ == "__main__":
    unittest.main()