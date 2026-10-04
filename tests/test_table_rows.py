"""A row a document's own table already contains is a merge artefact, not a fact.

Commit `eff1126` carried `STATE.md` with a byte-identical duplicate of its
`Implemented (2)` dashboard row: one copy from the VM that added the row, one from
the VM that had already added it before the rebase concatenated the two branches.
Every gate passed — line cap, metadata, links, orphans, generated freshness,
identifier agreement — so the reload point a cold session reads first showed two
rows that are one fact, and the next session removed one by hand.

The property is decidable and the blast radius is nil: on the tree this was
written against, 47 documents contain a repeated table row and **every one is a
generated session report**, where a row repeats because an artifact was declared
or rewritten twice and the report is telling the truth. Hand-authored documents
had zero, once this one was repaired. That is why the rule is scoped by the
`generated-by: origin` marker rather than by file name — see
`tests/test_link_escape.py` for the same scoping decision on a different rule, and
`docs/policy/gate-falsification.md` for the falsification method both share.

**Ceiling.** Rows are compared as their exact Markdown text, so a row that
differs in one cell is a different row; and only pipes-delimited tables inside
`.md` files are read at all.
"""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

from harness import RepoTest, git

from originlib import doclint, doclint_table, paths

# The commit that published the duplicate, and the two lines it landed on. Read
# out of git rather than written here, so the shape under test is the one the
# fleet published and not a fixture invented after the repair.
RECORDED_COMMIT = "eff1126"
RECORDED_FILE = "STATE.md"
DUPLICATE_LINE = 44
ORIGINAL_LINE = 37
# Where those bytes are read from. `RepoTest` points `ORIGIN_ROOT` at a synthetic
# repository with one commit and no history, so the recorded commit has to come
# from the real tree this file ships in.
RECORD_ROOT = Path(__file__).resolve().parent.parent

META = (
    "<!-- origin-meta\n"
    "owner: docs/INDEX.md\n"
    "status: active\n"
    "last-verified: 2026-10-04\n"
    "-->\n"
)

MODEL_ROW = "| Implemented (2) | every diagnostic step runs whenever the job runs |"
DASHBOARD = (
    META
    + "\n# State\n\n"
    "| Area | Verified status |\n"
    "|---|---|\n"
    + MODEL_ROW
    + "\n"
    + MODEL_ROW
    + "\n| Continuous integration | green |\n"
)

# What a generated report really looks like: an artifact declared, then rewritten
# by a command, appears twice and that is the truth rather than a defect.
GENERATED = (
    "<!-- generated-by: origin; do not edit by hand -->\n"
    + META
    + "\n# probe\n\n"
    "| path | sha256 | size |\n|---|---|---|\n"
    "| docs/INDEX.md | aaaaaa | 6119 |\n"
    "| docs/INDEX.md | bbbbbb | 6119 |\n"
)


def duplicate_rows(path: Path) -> list:
    """The rule's findings for one document, with the rest of the lint out of the way."""
    result = doclint.Result()
    doclint_table.check_table_rows(result, [path])
    return list(result.violations)


class CommittedDefectTest(RepoTest):
    """The shape under test is the record's own bytes, not a fixture.

    Read from the repository this test runs in, rather than from the harness's
    empty one: the harness repository has a single synthetic commit and no
    history, so `git show eff1126:STATE.md` there is a commit that does not
    exist. A fixture written after the repair would pass against a rule that
    never worked; these bytes are the ones the fleet published.
    """

    def committed(self, commit: str, name: str) -> str:
        done = subprocess.run(
            ["git", "show", f"{commit}:{name}"],
            cwd=str(RECORD_ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        return done.stdout

    def listed(self, commit: str) -> list[str]:
        done = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", commit],
            cwd=str(RECORD_ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        return done.stdout.split()

    def test_state_md_at_eff1126_is_reported(self) -> None:
        text = self.committed(RECORDED_COMMIT, RECORDED_FILE)
        repeated = text.splitlines()[DUPLICATE_LINE - 1]
        original = text.splitlines()[ORIGINAL_LINE - 1]
        # The two lines are byte-identical, which is the whole shape: a rebase
        # concatenated two VMs' additions of one row.
        self.assertEqual(repeated, original)
        self.assertIn("Implemented (2)", repeated)
        self.write(RECORDED_FILE, text)
        found = duplicate_rows(self.repo / RECORDED_FILE)
        self.assertEqual(len(found), 1, [str(item) for item in found])
        self.assertIn(f"repeated from line {ORIGINAL_LINE}", str(found[0]))
        self.assertIn("Implemented (2)", str(found[0]))
        # The location is structured, per D025: the annotation points at the
        # second copy, because that is the one a reader deletes.
        self.assertEqual(found[0].path, RECORDED_FILE)
        self.assertEqual(found[0].line, DUPLICATE_LINE)

    def test_the_same_commit_reports_nothing_else(self) -> None:
        """One finding on the whole tree at that commit, so the rule is not merely loud."""
        result = doclint.Result()
        written = []
        for name in self.listed(RECORDED_COMMIT):
            if not name.endswith(".md"):
                continue
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.committed(RECORDED_COMMIT, name), encoding="utf-8")
            written.append(path)
        doclint_table.check_table_rows(result, written)
        found = [str(item) for item in result.violations]
        self.assertEqual(len(found), 1, found[:6])
        self.assertTrue(found[0].startswith(f"{RECORDED_FILE}:"), found[0])

    def test_the_repaired_commit_reports_nothing(self) -> None:
        """The other direction: silent on the repair, or the rule is unsatisfiable."""
        self.write(RECORDED_FILE, self.committed("HEAD", RECORDED_FILE))
        self.assertEqual(duplicate_rows(self.repo / RECORDED_FILE), [])


class TableRowRuleTest(RepoTest):
    """The rule itself, on documents this test writes."""

    def write_doc(self, body: str) -> str:
        self.write("docs/probe.md", body)
        return "docs/probe.md"

    def test_a_repeated_row_is_reported_with_both_lines_and_the_row(self) -> None:
        relative = self.write_doc(DASHBOARD)
        found = duplicate_rows(self.repo / relative)
        self.assertEqual(len(found), 1, [str(item) for item in found])
        text = str(found[0])
        self.assertTrue(text.startswith(f"{relative}: "), text)
        # The row's own first cell, not the whole line: a reader is told which
        # row to delete rather than that two rows match.
        self.assertIn("(Implemented (2))", text)
        self.assertIn("repeated from line 11", text)
        self.assertIn("delete one", text)

    def test_the_same_row_in_two_different_tables_is_silent(self) -> None:
        """Repetition across tables is not repetition within one: they are separate lists."""
        # DASHBOARD carries a duplicate within its own table, so the second copy
        # has to be removed first or this test would be measuring that instead.
        head, _, tail = DASHBOARD.partition("| Continuous integration | green |")
        single = head.replace(
            "| Implemented (2) | every diagnostic step runs whenever the job runs |\n", "", 1
        )
        relative = self.write_doc(
            single
            + "| Continuous integration | green |\n"
            + "\nSome prose that ends the table.\n\n"
            + "| Area | Verified status |\n|---|---|\n"
            + "| Implemented (2) | every diagnostic step runs whenever the job runs |"
            + tail
        )
        self.assertEqual(duplicate_rows(self.repo / relative), [])

    def test_a_generated_document_is_silent(self) -> None:
        """A report that lists an artifact twice is reporting, not repeating itself."""
        relative = self.write_doc(GENERATED)
        self.assertEqual(duplicate_rows(self.repo / relative), [])

    def test_a_row_inside_a_code_fence_is_silent(self) -> None:
        relative = self.write_doc(
            META
            + "\n# probe\n\nA table, and then the same rows as an example:\n\n"
            "```\n| path | sha256 |\n|---|---|\n"
            "| docs/INDEX.md | aaaaaa |\n| docs/INDEX.md | aaaaaa |\n```\n"
        )
        self.assertEqual(duplicate_rows(self.repo / relative), [])

    def test_a_table_of_only_a_separator_is_silent(self) -> None:
        """`|---|---|` is structural. Comparing it to itself is not a finding."""
        relative = self.write_doc(
            META
            + "\n# probe\n\n| Area | Status |\n|---|---|\n| one | ok |\n"
            "\nAnd again, in prose:\n\n| Area | Status |\n|---|---|\n"
        )
        self.assertEqual(duplicate_rows(self.repo / relative), [])

    def test_rows_differing_in_one_cell_are_different_rows(self) -> None:
        relative = self.write_doc(
            META
            + "\n# probe\n\n| Area | Status |\n|---|---|\n"
            "| Implemented | green |\n| Implemented | red |\n"
        )
        self.assertEqual(duplicate_rows(self.repo / relative), [])

    def test_the_finding_is_published_as_a_check_run_annotation(self) -> None:
        # T-0040's mechanism: a red run names the file from its own annotations,
        # because the run log needs admin rights.
        self.write("docs/probe.md", DASHBOARD)
        git(self.repo, "add", "-A")
        exit_code = self.cli("annotate", "--", "doc lint")
        self.assertEqual(exit_code, 2, self.output())
        published = [
            line
            for line in self.output().splitlines()
            if line.startswith("::") and "repeated from line" in line
        ]
        self.assertEqual(len(published), 1, self.output())
        self.assertIn("file=docs/probe.md", published[0])
        # The second copy's line, which is the one a reader deletes.
        self.assertIn(f"line={DASHBOARD.splitlines().index(MODEL_ROW) + 2}", published[0])


class NoRegressionTest(unittest.TestCase):
    """The control that cannot fire: this repository repeats no hand-authored row."""

    def test_no_hand_authored_document_repeats_a_row(self) -> None:
        from originlib import docfiles, paths
        from originlib.reconcile import GENERATED_MARK

        base = paths.repo_root()
        files = docfiles.tracked_files(base)
        rows_read = 0
        result = doclint.Result()
        for path in files:
            if path.suffix != ".md":
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if GENERATED_MARK in text[:2048]:
                continue
            rows_read += sum(1 for line in text.splitlines() if doclint_table.TABLE_ROW.match(line))
        self.assertGreater(rows_read, 500, "the scan read almost nothing")
        doclint_table.check_table_rows(result, files)
        found = [str(item) for item in result.violations]
        self.assertEqual(found, [], f"{len(found)} repeated rows in {rows_read} read")


if __name__ == "__main__":
    unittest.main()
