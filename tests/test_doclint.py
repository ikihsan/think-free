"""Documentation lint: line cap, metadata, links, orphans, stale generated files."""

from __future__ import annotations

import unittest

from harness import RepoTest, write_doc

from originlib import doclint, report, session, tasks


class LineCapTest(RepoTest):
    def test_a_long_document_fails(self) -> None:
        write_doc(self.repo / "docs" / "policy" / "long.md", "Long", "docs/INDEX.md", extra="x\n" * 400)
        result = doclint.lint()
        self.assertFalse(result.ok)
        self.assertTrue(any("long.md" in problem and "300-line cap" in problem for problem in result.violations))

    def test_a_document_at_the_limit_passes(self) -> None:
        header = [
            "# Limit",
            "",
            "<!-- origin-meta",
            "owner: docs/INDEX.md",
            "status: active",
            "last-verified: 2026-10-03",
            "-->",
            "",
        ]
        pad = 300 - len(header) - 2  # closing prose plus a blank line
        lines = header + [f"line {index}" for index in range(pad)] + ["", "End."]
        target = self.repo / "docs" / "policy" / "limit.md"
        target.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.assertEqual(len(target.read_text(encoding="utf-8").splitlines()), 300)
        result = doclint.lint()
        self.assertFalse(any("300-line cap" in problem for problem in result.violations))

    def test_declared_vendor_exemption_is_reported_as_info(self) -> None:
        vendor = self.repo / "vendor"
        vendor.mkdir(exist_ok=True)
        (vendor / "MANIFEST.md").write_text(
            "# Vendor\n\n<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\n"
            "last-verified: 2026-10-03\n-->\n\nexempt: vendor/huge/**\n",
            encoding="utf-8",
        )
        huge = vendor / "huge"
        huge.mkdir()
        (huge / "big.md").write_text("# Big\n\n" + "x\n" * 400, encoding="utf-8")
        result = doclint.lint()
        self.assertFalse(any("300-line cap" in problem and "big.md" in problem for problem in result.violations))
        self.assertTrue(any("big.md" in info and "exempt" in info for info in result.infos))

    def test_data_files_are_exempt_by_extension(self) -> None:
        target = self.repo / "docs" / "data.json"
        target.write_text('{"pad": "' + "x" * 400 + '"}', encoding="utf-8")
        result = doclint.lint()
        self.assertFalse(any("data.json" in problem for problem in result.violations))

    def test_a_gitignored_file_is_not_repository_content(self) -> None:
        # An experiment that downloads its inputs pins them by hash instead of
        # committing them. Before doclint honoured .gitignore, those tarballs
        # were linted as documents and failed the line cap.
        ignored = self.repo / "EXPERIMENTS" / "000-probe" / "sdists"
        ignored.mkdir(parents=True)
        (ignored / "input.tar.gz").write_text("x\n" * 900, encoding="utf-8")
        (self.repo / ".gitignore").write_text(
            "__pycache__/\n*.py[cod]\n.origin/\nsessions/active.json\n"
            "EXPERIMENTS/*/sdists/\n",
            encoding="utf-8",
        )
        result = doclint.lint()
        self.assertFalse(
            any("input.tar.gz" in problem for problem in result.violations),
            result.violations,
        )

    def test_an_unignored_long_file_still_fails(self) -> None:
        # The point of the gitignore change is not to weaken the cap: a file that
        # is *not* ignored is still linted.
        kept = self.repo / "EXPERIMENTS" / "000-probe" / "kept.md"
        kept.parent.mkdir(parents=True)
        write_doc(kept, "Kept", "docs/INDEX.md", extra="x\n" * 400)
        result = doclint.lint()
        self.assertTrue(any("kept.md" in problem and "300-line cap" in problem
                            for problem in result.violations))


class MetadataTest(RepoTest):
    def test_missing_meta_fails(self) -> None:
        (self.repo / "docs" / "policy" / "bare.md").write_text("# Bare\n\nno meta here\n", encoding="utf-8")
        result = doclint.lint()
        self.assertTrue(any("bare.md" in problem and "origin-meta" in problem for problem in result.violations))

    def test_incomplete_meta_fails(self) -> None:
        path = self.repo / "docs" / "policy" / "partial.md"
        path.write_text("# Partial\n\n<!-- origin-meta\nowner: docs/INDEX.md\n-->\n", encoding="utf-8")
        result = doclint.lint()
        self.assertTrue(any("partial.md" in problem and "missing key" in problem for problem in result.violations))

    def test_missing_title_fails(self) -> None:
        path = self.repo / "docs" / "policy" / "untitled.md"
        path.write_text(
            "<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\nlast-verified: 2026-10-03\n-->\n",
            encoding="utf-8",
        )
        result = doclint.lint()
        self.assertTrue(any("untitled.md" in problem and "title" in problem for problem in result.violations))


class LinkTest(RepoTest):
    def test_broken_relative_link_fails(self) -> None:
        write_doc(
            self.repo / "docs" / "process" / "linky.md",
            "Linky",
            "docs/INDEX.md",
            extra="\nSee [missing](nowhere.md).\n",
        )
        result = doclint.lint()
        self.assertTrue(any("broken link" in problem and "nowhere.md" in problem for problem in result.violations))

    def test_external_link_is_not_checked(self) -> None:
        write_doc(
            self.repo / "docs" / "process" / "webby.md",
            "Webby",
            "docs/INDEX.md",
            extra="\nSee [example](https://example.invalid/page).\n",
        )
        result = doclint.lint()
        self.assertFalse(any("example.invalid" in problem for problem in result.violations))

    def test_link_inside_a_code_fence_is_ignored(self) -> None:
        write_doc(
            self.repo / "docs" / "process" / "fenced.md",
            "Fenced",
            "docs/INDEX.md",
            extra="\n```markdown\n[not a link](missing-inside-fence.md)\n```\n",
        )
        result = doclint.lint()
        self.assertFalse(any("missing-inside-fence" in problem for problem in result.violations))

    def test_repo_root_relative_link_resolves(self) -> None:
        self.write("STATE.md", "# State\n\n<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\n"
                               "last-verified: 2026-10-03\n-->\n\nSee [README](README.md).\n")
        write_doc(
            self.repo / "docs" / "process" / "rootrel.md",
            "Root relative",
            "docs/INDEX.md",
            extra="\nSee [state](STATE.md).\n",
        )
        result = doclint.lint()
        self.assertFalse(any("STATE.md" in problem and "broken" in problem for problem in result.violations))


class OrphanTest(RepoTest):
    def test_unlinked_document_fails(self) -> None:
        write_doc(self.repo / "docs" / "policy" / "orphan.md", "Orphan", "docs/INDEX.md")
        result = doclint.lint()
        self.assertTrue(any("orphan.md" in problem and "orphan" in problem for problem in result.violations))

    def test_linked_document_passes(self) -> None:
        write_doc(self.repo / "docs" / "policy" / "linked.md", "Linked", "docs/INDEX.md")
        write_doc(
            self.repo / "docs" / "INDEX.md",
            "Documentation index",
            "docs/INDEX.md",
            extra="\nSee [linked](policy/linked.md).\n",
        )
        result = doclint.lint()
        self.assertFalse(any("linked.md" in problem for problem in result.violations))


class GeneratedFileTest(RepoTest):
    def test_missing_generated_files_fail(self) -> None:
        result = doclint.lint()
        self.assertTrue(any("generated file missing" in problem for problem in result.violations))

    def test_stale_index_fails(self) -> None:
        from originlib import docindex

        self.write_generated()
        result = doclint.lint()
        self.assertFalse([p for p in result.violations if "generated file" in p], result.violations)

    def test_hand_edited_index_is_detected(self) -> None:
        self.write_generated()
        index = self.repo / "tasks" / "INDEX.md"
        index.write_text(index.read_text(encoding="utf-8") + "\nhand-edited\n", encoding="utf-8")
        result = doclint.lint()
        self.assertTrue(any("stale" in problem for problem in result.violations))


class OpenSessionLintTest(RepoTest):
    """A session in progress must not make `doc lint` fail.

    `check_generated` already skips the open session's report, because a report
    written while a session runs cannot match a final render. The metadata and
    orphan rules did not have that exemption, and `session start` rendered the
    report *before* appending its first event: the stub carried no `origin-meta`
    block, and `sessions/INDEX.md` was rebuilt while the session directory held
    no `events.jsonl`, so the index did not list the report either. Every lint
    run in a tree with a live session therefore failed on the two files the
    session had just created. `observed` on instance-20260717-0944, while
    running T-0031's own verification command.
    """

    def setUp(self) -> None:
        super().setUp()
        # The fixture ships placeholder documents and no generated indexes, so
        # the clean baseline is established first: the rule under test is the
        # session's own report, not the fixture.
        self.write_generated()

    def test_lint_passes_while_a_session_is_open(self) -> None:
        session.start("lint while working", agent="agent-a")
        self.assertEqual(self.cli("doc", "lint"), 0, self.output())

    def test_the_report_is_metadata_bearing_and_indexed_from_the_first_moment(self) -> None:
        active = session.start("report immediately", agent="agent-a")
        report = self.repo / "sessions" / active.session / "README.md"
        self.assertIn("origin-meta", report.read_text(encoding="utf-8"))
        index = (self.repo / "sessions" / "INDEX.md").read_text(encoding="utf-8")
        self.assertIn(active.session, index)


if __name__ == "__main__":
    unittest.main()