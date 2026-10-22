"""Which files git's index calls repository content, read by git itself.

`docfiles.tracked_files` used to walk the tree and ask `git check-ignore` about
every path. On this repository (~49 000 files, git 2.25.1) that one call past
~10 000 paths blocks, so `doc lint` stalled with no output at all. It now reads
`ls-files -co --exclude-standard`. This pins the behaviour the change must not
lose: the `.gitignore` negation that re-includes a raw JSON, which `check-ignore`
reported as ignored and the old walk therefore dropped.
"""

from __future__ import annotations

import unittest

from harness import RepoTest

from originlib import docfiles


def rels(repo) -> set[str]:
    return {p.relative_to(repo).as_posix() for p in docfiles.tracked_files(repo)}


class IndexIsTheAuthorityTest(RepoTest):
    def test_a_negation_re_included_path_is_repository_content(self) -> None:
        gitignore = self.repo / ".gitignore"
        gitignore.write_text(
            gitignore.read_text(encoding="utf-8")
            + "EXPERIMENTS/*/raw/**\n"
            + "!EXPERIMENTS/*/raw/*.json\n",
            encoding="utf-8",
        )
        self.write("EXPERIMENTS/E999-x/raw/keep.json", "{}\n")
        self.write("EXPERIMENTS/E999-x/raw/drop.bin", "not json\n")
        found = rels(self.repo)
        self.assertIn("EXPERIMENTS/E999-x/raw/keep.json", found)
        self.assertNotIn("EXPERIMENTS/E999-x/raw/drop.bin", found)

    def test_an_ignored_path_is_not_repository_content(self) -> None:
        gitignore = self.repo / ".gitignore"
        gitignore.write_text(
            gitignore.read_text(encoding="utf-8") + "*.scratch\n",
            encoding="utf-8",
        )
        self.write("notes.scratch", "ignored\n")
        self.write("notes.txt", "tracked\n")
        found = rels(self.repo)
        self.assertNotIn("notes.scratch", found)
        self.assertIn("notes.txt", found)


if __name__ == "__main__":
    unittest.main()
