"""Where the identifier rule is enforced, and what the real record holds.

Split from `test_identifiers.py` at the line cap. That file tests the rule; this
one tests the three places it has to be read: this repository's own record, `doc
lint`, and `sync land`.

`land` is the only publishing operation gated, and the reason is a property of the
fleet rather than a choice: two VMs allocate a number from their own tree, so the
collision appears in the merged result and nowhere else. `push` and `task claim`
stay ungated on purpose — refusing them would block a VM from publishing the
session record it needs in order to renumber out of the collision (D031).
"""

from __future__ import annotations

import unittest
from pathlib import Path

from harness import RepoTest

from originlib import doclint, identifiers, paths, sync, syncland

COLLIDING_BODY = "## F020 — one\n"
COLLIDING_OTHER = "## F020 — two\n"
COLLIDING_INDEX = "| Id | Subject |\n|---|---|\n| F020 | one |\n"


class ThisRepositoryTest(unittest.TestCase):
    """The real record must hold no collision of its own."""

    def real_root(self) -> Path:
        root = Path(paths.repo_root())
        if root != Path(__file__).resolve().parent.parent:
            self.skipTest("running against a fixture repository, not the real one")
        return root

    def test_this_repository_has_no_identifier_collision(self) -> None:
        self.assertEqual(identifiers.report(self.real_root()), [])

    def test_every_decision_this_repository_holds_is_listed_in_the_index(self) -> None:
        # The rule reported D030 missing from its index row on its first run,
        # ten minutes after it was written. Reading both halves is the property;
        # the rule's own report is the assertion.
        root = self.real_root()
        defined = {d.ident for d in identifiers.definitions(root) if d.ident.startswith("D")}
        listed = set().union(*identifiers._decision_index(root).values())
        self.assertEqual(sorted(defined - listed), [], "a decision no index row lists")
        self.assertEqual(sorted(listed - defined), [], "an index row nothing defines")

    def test_the_colliding_commit_is_the_one_the_fixture_quotes(self) -> None:
        # If this stops matching, the fixture in `test_identifiers.py` is quoting
        # something other than what the fleet actually published, and the reason
        # must be found rather than the fixture quietly edited.
        import subprocess

        root = self.real_root()
        present = subprocess.run(
            ["git", "cat-file", "-e", "e6eb992^{commit}"],
            cwd=str(root), capture_output=True, text=True,
        )
        if present.returncode != 0:
            self.skipTest("history is shallow; commit e6eb992 is not present")
        text = subprocess.run(
            ["git", "show", "e6eb992:FAILURES-findings-2.md"],
            cwd=str(root), capture_output=True, text=True, check=True,
        ).stdout
        # The rule matches line by line, as `identifiers.definitions` does.
        headings = [
            match.group(1)
            for match in (identifiers.DEFINITION.match(line) for line in text.splitlines())
            if match
        ]
        duplicates = sorted({i for i in headings if headings.count(i) > 1})
        self.assertEqual(duplicates, ["F010"], f"fixture drift: {headings}")


class DocLintWiringTest(RepoTest):
    """The rule has to be registered, or it is a module nothing calls."""

    def colliding(self) -> None:
        self.write("FAILURES-findings.md", COLLIDING_BODY)
        self.write("FAILURES-findings-3.md", COLLIDING_OTHER)
        self.write("FAILURES.md", COLLIDING_INDEX)

    def test_doc_lint_fails_on_the_colliding_tree(self) -> None:
        self.colliding()
        result = doclint.lint()
        self.assertFalse(result.ok)
        self.assertTrue(
            any("identifier collision" in problem and "F020" in problem
                for problem in result.violations),
            result.violations,
        )


class LandRefusalTest(RepoTest):
    """`land` refuses the collision, and the refusal names the way out."""

    def record(self) -> None:
        from harness import git

        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "record")

    def land(self, pushed):
        """Drive `land` with the remote faked and the tree state left real.

        `dirty_paths`, `rev_list` and `rebase_in_progress` stay real so a mocked
        truthiness cannot stand in for the state `land` refuses on. Mocking the
        whole `gitutil` module was the first attempt and it refused on a dirty
        tree that did not exist.
        """
        import unittest.mock as mock

        with mock.patch.object(syncland, "remote_name", return_value="origin"), mock.patch.object(
            syncland, "fetch"
        ), mock.patch.object(syncland.gitutil, "text", return_value="abc123"), mock.patch.object(
            syncland.gitutil, "run"
        ) as run, mock.patch.object(syncland, "push", pushed):
            run.return_value.returncode = 0
            run.return_value.stdout = ""
            run.return_value.stderr = ""
            return syncland.land()

    def test_land_refuses_to_publish_a_colliding_tree(self) -> None:
        import unittest.mock as mock

        self.write("FAILURES-findings.md", COLLIDING_BODY)
        self.write("FAILURES-findings-3.md", COLLIDING_OTHER)
        self.write("FAILURES.md", COLLIDING_INDEX)
        self.record()
        with mock.patch.object(syncland, "push") as pushed:
            with self.assertRaises(sync.SyncError) as caught:
                self.land(pushed)
        message = str(caught.exception)
        self.assertIn("identifier record collides", message)
        self.assertIn("F020", message)
        pushed.assert_not_called()

    def test_the_refusal_names_the_way_out(self) -> None:
        # A refusal that only names the finding makes the reader do the work.
        import unittest.mock as mock

        self.write("FAILURES-findings.md", COLLIDING_BODY)
        self.write("FAILURES-findings-3.md", COLLIDING_OTHER)
        self.write("FAILURES.md", COLLIDING_INDEX)
        self.record()
        with mock.patch.object(syncland, "push"):
            with self.assertRaises(sync.SyncError) as caught:
                self.land(mock.Mock())
        self.assertIn("land again", str(caught.exception))

    def test_land_publishes_a_clean_tree(self) -> None:
        import unittest.mock as mock

        self.write("FAILURES-findings.md", COLLIDING_BODY)
        self.write("FAILURES.md", COLLIDING_INDEX)
        self.record()
        pushed = mock.Mock(return_value={"pushed": True, "head": "abc123"})
        outcome = self.land(pushed)
        self.assertTrue(outcome["pushed"])
        self.assertTrue(pushed.called)


if __name__ == "__main__":
    unittest.main()