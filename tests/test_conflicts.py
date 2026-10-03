"""Conflict-marker detection: what must fire, and what must not.

The rule this tests exists because three mission records reached the shared base
with a conflict marker in them while every gate passed (`FAILURES.md` F013).
The shapes in `HISTORICAL` are quoted from that commit so a reader can see what
has to be caught without a git history, and the shapes in `FalsePositiveTest`
are quoted from what already exists in this repository and is not a conflict.

The markers below sit mid-line inside string literals, so this file needs no
waiver of its own; the waiver's clauses are exercised against throwaway
repositories in `WaiverTest`.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from harness import RepoTest, write_doc

from originlib import conflicts, doclint, paths

HEAD_LABEL = "renumber the E3 attribution finding to F012"

# The committed regions of fd7b4a1, one per file, with the line numbers the
# rule reports. DECISIONS-GATING.md had two defects: the block, and a
# terminator left behind with nothing open.
HISTORICAL: tuple[tuple[str, str, tuple[int, ...]], ...] = (
    (
        "FAILURES.md",
        "| F010 | census gate |\n"
        "<<<<<<< HEAD\n"
        "| F011 | sync land broke |\n"
        "=======\n"
        f">>>>>>> {HEAD_LABEL}\n"
        "| F012 | ordering claim holds |\n",
        (2,),
    ),
    (
        "FAILURES-findings-2.md",
        "even well defined.\n"
        "\n"
        "<<<<<<< HEAD\n"
        "## F011 - sync land broke on git >= 2.26\n"
        "\n"
        "Source: T-0016.\n"
        "=======\n"
        f">>>>>>> {HEAD_LABEL}\n"
        "## F012 - E3's ordering claim holds\n",
        (3,),
    ),
    (
        "DECISIONS-GATING.md",
        "was indistinguishable from picking the result.\n"
        "\n"
        "<<<<<<< HEAD\n"
        "Consequence: the first run is kept as `first-failure.json`,\n"
        "=======\n"
        "Consequence: the first run is kept as `first-failure.json`, and both README and\n"
        f">>>>>>> {HEAD_LABEL}\n"
        "`FAILURES.md` F012 name the defect.\n"
        f">>>>>>> {HEAD_LABEL}\n",
        (3, 9),
    ),
)


class MarkerTest(unittest.TestCase):
    """Every shape git can leave behind is reported."""

    def test_a_complete_block_is_reported(self) -> None:
        # The first implementation of this rule reported only malformed blocks
        # and passed all three corrupted files. This clause is the regression.
        found = conflicts.scan("<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> topic\n")
        self.assertEqual([item.line for item in found], [1])
        self.assertIn("terminator on line 5", found[0].detail)

    def test_a_block_with_no_terminator_is_reported(self) -> None:
        found = conflicts.scan("prose\n<<<<<<< HEAD\nours\n=======\ntheirs\n")
        self.assertEqual([item.line for item in found], [2])
        self.assertIn("no terminator", found[0].detail)

    def test_a_block_with_no_divider_is_reported(self) -> None:
        found = conflicts.scan("<<<<<<< HEAD\nours\n>>>>>>> topic\n")
        self.assertEqual([item.line for item in found], [1])
        self.assertIn("no ======= divider", found[0].detail)

    def test_a_terminator_with_no_open_block_is_reported(self) -> None:
        found = conflicts.scan("prose\n>>>>>>> topic\nmore prose\n")
        self.assertEqual([item.line for item in found], [2])
        self.assertIn("no open block", found[0].detail)

    def test_a_second_opening_closes_the_first_block(self) -> None:
        text = "<<<<<<< HEAD\na\n=======\nb\n<<<<<<< HEAD\nc\n=======\nd\n>>>>>>> t\n"
        found = conflicts.scan(text)
        self.assertEqual([item.line for item in found], [1, 5])
        self.assertIn("opens again", found[0].detail)

    def test_a_diff3_base_marker_stays_inside_the_block(self) -> None:
        found = conflicts.scan("<<<<<<< HEAD\na\n||||||| base\ncommon\n=======\nb\n>>>>>>> t\n")
        self.assertEqual([item.line for item in found], [1])
        self.assertIn("terminator on line 7", found[0].detail)

    def test_a_clean_document_reports_nothing(self) -> None:
        self.assertEqual(conflicts.scan("# Title\n\nprose with < and > and =\n"), [])

    def test_every_committed_region_is_reported(self) -> None:
        for name, text, lines in HISTORICAL:
            with self.subTest(file=name):
                self.assertEqual([item.line for item in conflicts.scan(text)], list(lines))


class FalsePositiveTest(unittest.TestCase):
    """What already exists in this repository and must stay silent."""

    def test_seven_equals_alone_is_not_a_marker(self) -> None:
        # sessions/*/commands.log is full of these separators.
        self.assertEqual(conflicts.scan("=======\n"), [])
        self.assertEqual(conflicts.scan("a\n=======\nb\n"), [])

    def test_a_setext_underline_is_not_a_marker(self) -> None:
        self.assertEqual(conflicts.scan("Title\n=======\n\nprose\n"), [])

    def test_fewer_or_more_than_seven_characters_is_prose(self) -> None:
        # Eight of each is not git's marker, so an opening and its divider are
        # prose. The closing line still has to be reported: a bare terminator is
        # a defect whether or not anything opened it.
        self.assertEqual(conflicts.scan("<<<<<<<< HEAD\n========\nprose\n"), [])
        found = conflicts.scan("<<<<< HEAD\n=====\n>>>>>>> t\n")
        self.assertEqual([item.line for item in found], [3])
        self.assertIn("no open block", found[0].detail)

    def test_an_indented_marker_is_prose(self) -> None:
        # git's text driver writes markers at column 0. An indented example in
        # a document must not redden the build; the limitation is documented.
        self.assertEqual(conflicts.scan("```diff\n  <<<<<<< HEAD\n  =======\n  >>>>>>> t\n```\n"), [])

    def test_eight_equals_with_a_space_is_not_a_marker(self) -> None:
        self.assertEqual(conflicts.scan("======= trailing\n"), [])


class WaiverTest(RepoTest):
    """A file that must quote a marker declares it, visibly."""

    BLOCK = "<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> topic\n"

    def write_block(self, header: str) -> Path:
        return self.write("docs/policy/quoted.md", f"# Quoted\n\n{header}\n{self.BLOCK}")

    def test_a_declaration_suppresses_the_findings(self) -> None:
        path = self.write_block("<!-- origin-allow-conflict-markers -->")
        self.assertTrue(conflicts.waived(path.read_text(encoding="utf-8")))
        violations, infos = conflicts.report([path], self.repo)
        self.assertEqual(violations, [])
        self.assertEqual(len(infos), 1)

    def test_without_a_declaration_the_same_file_is_a_violation(self) -> None:
        path = self.write_block("prose")
        violations, infos = conflicts.report([path], self.repo)
        self.assertEqual(len(violations), 1)
        self.assertEqual(infos, [])

    def test_a_declaration_is_scoped_to_its_own_file(self) -> None:
        self.write_block("<!-- origin-allow-conflict-markers -->")
        other = self.write("docs/policy/other.md", f"# Other\n\nprose\n{self.BLOCK}")
        violations, _ = conflicts.report([other], self.repo)
        self.assertEqual(len(violations), 1)

    def test_a_declaration_below_the_window_does_not_apply(self) -> None:
        filler = "\n".join(["prose"] * conflicts.WAIVER_WINDOW_LINES)
        path = self.write("docs/policy/late.md", f"# Late\n\n{filler}\n# origin-allow-conflict-markers\n")
        self.assertFalse(conflicts.waived(path.read_text(encoding="utf-8")))

    def test_a_hash_and_slash_form_are_accepted(self) -> None:
        self.assertTrue(conflicts.waived("# origin-allow-conflict-markers\n"))
        self.assertTrue(conflicts.waived("// origin-allow-conflict-markers\n"))

    def test_a_declaration_may_say_why(self) -> None:
        self.assertTrue(
            conflicts.waived("<!-- origin-allow-conflict-markers: quotes the marker -->\n")
        )

    def test_a_longer_name_is_not_the_directive(self) -> None:
        self.assertFalse(conflicts.waived("# origin-allow-conflict-markers-and-more\n"))


class LintTest(RepoTest):
    """The rule behaves as a doc lint rule: violation, or visible info."""

    def test_a_conflicted_document_fails_doc_lint(self) -> None:
        path = write_doc(
            self.repo / "docs" / "policy" / "conflicted.md",
            "Conflicted",
            "docs/INDEX.md",
            extra="\n<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> topic\n",
        )
        marker_line = path.read_text(encoding="utf-8").splitlines().index("<<<<<<< HEAD") + 1
        result = doclint.lint()
        self.assertFalse(result.ok)
        self.assertTrue(
            any(f"conflicted.md:{marker_line}" in problem and "unresolved conflict block" in problem
                for problem in result.violations),
            result.violations,
        )

    def test_a_waived_conflict_is_reported_as_info(self) -> None:
        write_doc(
            self.repo / "docs" / "policy" / "quoted.md",
            "Quoted",
            "docs/INDEX.md",
            extra="\n<!-- origin-allow-conflict-markers -->\n\n<<<<<<< HEAD\nours\n>>>>>>> topic\n",
        )
        result = doclint.lint()
        self.assertFalse(
            any("unresolved conflict" in problem or "terminator" in problem
                for problem in result.violations),
            result.violations,
        )
        self.assertTrue(any("quoted.md" in info and "waived" in info for info in result.infos), result.infos)

    def test_a_binary_file_is_skipped(self) -> None:
        target = self.repo / "EXPERIMENTS" / "001-probe" / "wheel.bin"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"\x00binary\x00<<<<<<< HEAD\n=======\n>>>>>>> t\n")
        violations, _ = conflicts.report([target], self.repo)
        self.assertEqual(violations, [])

    def test_a_gitignored_file_is_not_repository_content(self) -> None:
        ignored = self.repo / "EXPERIMENTS" / "001-probe" / "build"
        ignored.mkdir(parents=True)
        (ignored / "out.txt").write_text("<<<<<<< HEAD\n=======\n>>>>>>> t\n", encoding="utf-8")
        (self.repo / ".gitignore").write_text(
            "__pycache__/\n*.py[cod]\n.origin/\nsessions/active.json\nbuild/\n", encoding="utf-8"
        )
        result = doclint.lint()
        self.assertFalse(any("out.txt" in problem for problem in result.violations), result.violations)


class ThisRepositoryTest(unittest.TestCase):
    """The tree these tests run in must hold no marker of its own."""

    def test_no_tracked_file_holds_an_unresolved_conflict(self) -> None:
        from originlib.docfiles import tracked_files

        root = paths.repo_root()
        if Path(root) != Path(__file__).resolve().parent.parent:
            self.skipTest("running against a fixture repository, not the real one")
        violations, infos = conflicts.report(tracked_files(root), root)
        self.assertEqual(violations, [])
        self.assertEqual(infos, [])


if __name__ == "__main__":
    unittest.main()