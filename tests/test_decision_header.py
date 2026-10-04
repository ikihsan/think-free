"""A decision record's own header, held to the decisions that file defines.

The rule this tests exists because a decision number is written in three places
that must agree — the `## Dnnn — …` heading, the index row in `DECISIONS.md`,
and the `Decisions **…**` line the record opens with — and T-0030 and T-0036
read the first two while the third went unchecked. Two of the five decision
records were false on the shared base while every gate passed (defect 14 in
`STATE-defects.md`, T-0042):

* `DECISIONS-GATING.md` said `D013, D024–D029` and defines D024, D025, D026,
  D029, D030, D032 and D035;
* `DECISIONS-PRACTICE.md` said `D011–D018, D027–D028` and defines D011, D012,
  D014–D018, D031, D033 and D034 — the three entries that moved to
  `DECISIONS-SESSIONS.md` when the split T-0030 attempted was reversed, named by
  a range that had not been narrowed.

`CommittedBytesTest` reads those files out of git at the commit that carried
them, so the rule is falsified against the defect's own bytes on every run
rather than against a fixture written today. The controls are the shapes that
must stay silent: a range spelled with a different dash, a record whose
decisions are all named, and a file that defines nothing.
"""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from harness import RepoTest

from originlib import decisionheader, doclint, paths, sync, syncland

# The commit that published T-0042's task file. Both decision records were
# already false in it, and it is on the shared base, so `git show` can read the
# bytes back for as long as the history is there.
STALE_COMMIT = "d451169"
STALE_FILES = ("DECISIONS-GATING.md", "DECISIONS-PRACTICE.md")

# Quoted from that commit's DECISIONS-GATING.md, header and the three headings
# its range stopped short of. D027 and D028 are in the message because the header
# spells them inside `D024–D029`, not because anybody typed them.
STALE_GATING = """\
# Decisions — how this repository's own gates are written and run

Decisions **D013, D024–D029**. Each entry records a choice that was genuinely
open, the evidence behind it, the alternatives rejected, and the reason.

## D024 — A gate clause must be implemented as written (2026-10-03)

Prose.

## D030 — A diagnostic must distinguish two states (2026-10-04)

Prose.

## D032 — An identifier collision is refused before publication (2026-10-04)

Prose.

## D035 — CI runs every minor version the floor claim covers (2026-10-04)

Prose.
"""

CORRECT_GATING = """\
# Decisions — how this repository's own gates are written and run

Decisions **D024–D026, D030, D032, D035**. Each entry records a choice that was
genuinely open.

## D024 — A gate clause must be implemented as written (2026-10-03)

Prose.

## D025 — A gate must read the property it claims to check (2026-10-03)

Prose.

## D026 — A task's verification must be runnable while its own session is open (2026-10-03)

Prose.

## D030 — A diagnostic must distinguish two states (2026-10-04)

Prose.

## D032 — An identifier collision is refused before publication (2026-10-04)

Prose.

## D035 — CI runs every minor version the floor claim covers (2026-10-04)

Prose.
"""


class HeaderAgreementTest(RepoTest):
    """What the rule must fire on, in a throwaway repository."""

    def report(self) -> list[str]:
        return decisionheader.report(self.repo)

    def test_a_decision_the_header_omits_is_reported(self) -> None:
        self.write("DECISIONS-GATING.md", STALE_GATING)
        found = self.report()
        self.assertTrue(
            any("D032" in line and "its own header does not name it" in line for line in found),
            found,
        )

    def test_a_decision_the_header_names_but_the_file_lacks_is_reported(self) -> None:
        self.write("DECISIONS-GATING.md", STALE_GATING)
        found = self.report()
        self.assertTrue(any("D013" in line and "does not define" in line for line in found), found)

    def test_the_report_names_the_file_and_the_line_to_edit(self) -> None:
        self.write("DECISIONS-GATING.md", STALE_GATING)
        for line in self.report():
            self.assertIn("DECISIONS-GATING.md:3:", line)

    def test_a_correct_header_is_silent(self) -> None:
        self.write("DECISIONS-GATING.md", CORRECT_GATING)
        self.assertEqual(self.report(), [])

    def test_a_record_with_no_readable_header_is_reported(self) -> None:
        # The obligation D025's second half records, and the failure defect 10's
        # control found: a parser that quietly stops matching is
        # indistinguishable from a clean tree, so "nothing readable" has to be a
        # finding rather than a pass.
        self.write("DECISIONS-GATING.md", "# Decisions\n\n## D030 — a decision\n")
        found = self.report()
        self.assertTrue(any("names none in its own header" in line for line in found), found)


class ControlTest(RepoTest):
    """The shapes that must stay silent, or the rule is a gate nobody runs."""

    def test_a_range_spelled_with_a_hyphen_is_the_same_set(self) -> None:
        body = "## D011 — a\n\n## D012 — b\n\n## D014 — c\n"
        self.write("DECISIONS-PRACTICE.md", f"Decisions **D011-D012, D014**.\n\n{body}")
        self.assertEqual(decisionheader.report(self.repo), [])

    def test_a_file_that_defines_no_decision_is_not_asked_for_a_header(self) -> None:
        # `DECISIONS.md` is the index: it lists identifiers and defines none, so
        # asking it to name its own decisions would be the rule reading a
        # property the file does not have.
        self.write("DECISIONS.md", "| File | Decisions | Governs |\n|---|---|---|\n")
        self.assertEqual(decisionheader.report(self.repo), [])

    def test_a_prose_mention_outside_the_bold_span_is_not_a_declaration(self) -> None:
        self.write(
            "DECISIONS-GATING.md",
            "Decisions **D030**. See also D099 for the note it replaced.\n\n## D030 — a\n",
        )
        self.assertEqual(decisionheader.report(self.repo), [])

    def test_order_and_spacing_are_not_compared(self) -> None:
        self.write(
            "DECISIONS-GATING.md",
            "Decisions **D032,  D030,  D024**.\n\n## D024 — a\n\n## D030 — b\n\n## D032 — c\n",
        )
        self.assertEqual(decisionheader.report(self.repo), [])


class CommittedBytesTest(unittest.TestCase):
    """The rule must fire on the bytes the shared base actually carried."""

    def test_the_defect_fires_on_the_committed_bytes(self) -> None:
        repo_root = Path(paths.repo_root())
        if repo_root != Path(__file__).resolve().parent.parent:
            self.skipTest("running against a fixture repository, not the real one")
        present = subprocess.run(
            ["git", "cat-file", "-e", f"{STALE_COMMIT}^{{commit}}"],
            cwd=str(repo_root), capture_output=True, text=True,
        )
        if present.returncode != 0:
            self.skipTest(f"history is shallow; commit {STALE_COMMIT} is not present")
        found: list[str] = []
        with tempfile.TemporaryDirectory() as tmp:
            tree = Path(tmp)
            for name in STALE_FILES:
                text = subprocess.run(
                    ["git", "show", f"{STALE_COMMIT}:{name}"],
                    cwd=str(repo_root), capture_output=True, text=True, check=True,
                ).stdout
                (tree / name).write_text(text, encoding="utf-8")
            found = decisionheader.report(tree)
        self.assertTrue(found, f"{STALE_COMMIT} carried the false headers and none was reported")
        for name in STALE_FILES:
            self.assertTrue(any(line.startswith(name + ":") for line in found), found)
        for ident in ("D013", "D030", "D032", "D035"):
            self.assertTrue(any(ident in line for line in found), found)

    def test_the_repair_commit_is_silent(self) -> None:
        # The other half of a falsification, and the half that is easy to leave
        # out: a rule that fires on the defect and also on the repair is a rule
        # nobody can satisfy.
        repo_root = Path(paths.repo_root())
        if repo_root != Path(__file__).resolve().parent.parent:
            self.skipTest("running against a fixture repository, not the real one")
        self.assertEqual(decisionheader.report(repo_root), [])


class WiringTest(RepoTest):
    """The third source has to be read by both gates, not by its own tests."""

    def test_doc_lint_fails_on_a_stale_decision_header(self) -> None:
        self.write("DECISIONS-GATING.md", STALE_GATING)
        result = doclint.lint()
        self.assertFalse(result.ok)
        self.assertTrue(
            any("identifier collision" in problem and "D032" in problem
                for problem in result.violations),
            result.violations,
        )

    def test_land_refuses_to_publish_a_stale_decision_header(self) -> None:
        # `land` reads `idcheck.report(paths.repo_root())`, which is this
        # repository's own root because the fixture sets `ORIGIN_ROOT`. A stale
        # header is therefore a refusal, not a lint warning nobody has to read.
        self.write("DECISIONS-GATING.md", STALE_GATING)
        with self.assertRaises(sync.SyncError) as caught:
            syncland._refuse_identifier_collision()
        self.assertIn("DECISIONS-GATING.md", str(caught.exception))


if __name__ == "__main__":
    unittest.main()