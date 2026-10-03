# origin-allow-secret-patterns: github-token
"""Release-manifest enforcement, falsified clause by clause.

Every test here seeds exactly one defect into a throwaway repository and asserts
the check reports it. That is the shape T-0021 established (D025): a gate added
for a defect is run against that defect's own bytes before it is trusted, because
the first version of the conflict-marker rule reported 1 of 4 committed defects
and would have passed the very files it was written for.

The `CleanFixtureTest` case is the other half — a check that only ever fails is
not a check either.

The waiver above is D012's mechanism, and `release check` found the need for it:
the token-shaped fixtures below live in `tests/`, which the manifest classifies
public, and rule 3 has no reading in which a fake credential in a fixture is an
exposure.
"""

from __future__ import annotations

import unittest

from harness import RepoTest

from originlib import release

STATE = "no-public-product"

MANIFEST = """<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Release manifest

<!-- origin-release-state: %(state)s -->

## Public by default

| Path | Why |
|---|---|
| `README.md` | The front door. |
| `AGENTS.md` | The agent contract. |
| `docs/` | Policy and process. |
| `tools/` `tests/` | The tooling and its suite. |
| `.gitignore` | Ignore rules. |
| `RELEASE-MANIFEST.md` | This file. |
| `LICENSE` (pending) | Absent until a release exists. |
%(extra_public)s| | A row with no backticked path classifies nothing: the promise of a future path. |

## Internal by default

| Path | Why |
|---|---|
| `sessions/` | Raw run history. |
| `tasks/` | Dispatch state. |
| `STATE.md` `MISSION.md` | Mission control records. |
%(extra_internal)s"""


def render_manifest(state: str = STATE, extra_public: str = "", extra_internal: str = "") -> str:
    return MANIFEST % {"state": state, "extra_public": extra_public, "extra_internal": extra_internal}


class ReleaseTest(RepoTest):
    """A repository that passes, so each test can break exactly one thing."""

    def setUp(self) -> None:
        super().setUp()
        self.write("RELEASE-MANIFEST.md", render_manifest())
        self.write("README.md", f"# Fixture\n\n<!-- origin-release-state: {STATE} -->\n")

    def manifest(self, text: str) -> None:
        self.write("RELEASE-MANIFEST.md", text)

    def assertClean(self) -> None:
        result = release.check()
        self.assertTrue(result.ok, result.render())

    def assertFails(self, fragment: str) -> None:
        result = release.check()
        self.assertFalse(result.ok, "expected a violation, got a pass")
        self.assertTrue(
            any(fragment in problem for problem in result.violations),
            f"{fragment!r} not in {result.violations}",
        )


class CleanFixtureTest(ReleaseTest):
    def test_a_complete_manifest_passes(self) -> None:
        self.assertClean()

    def test_the_check_counts_declared_paths(self) -> None:
        result = release.check()
        self.assertEqual(result.checked, 12)
        self.assertEqual(result.violations, [])

    def test_the_cli_exits_zero_then_two(self) -> None:
        self.assertEqual(self.cli("release", "check"), 0)
        self.assertIn("release check: OK", self.output())
        self.write("README.md", "# Fixture\n")
        self.assertEqual(self.cli("release", "check"), 2)
        self.assertIn("release check: 1 violation(s)", self.output())


class WildcardTest(ReleaseTest):
    def test_a_public_glob_fails(self) -> None:
        self.manifest(render_manifest(extra_public="| `src/*` | A glob. |\n"))
        self.assertFails("uses a wildcard")

    def test_an_internal_glob_fails(self) -> None:
        self.manifest(render_manifest().replace("`sessions/`", "`session*`"))
        self.assertFails("uses a wildcard")


class CoverageTest(ReleaseTest):
    def test_a_new_unclassified_root_file_fails(self) -> None:
        self.write("NOTES.md", "# Notes\n\n<!-- origin-meta\nowner: docs/INDEX.md\n"
                               "status: active\nlast-verified: 2026-10-03\n-->\n")
        self.assertFails("NOTES.md: tracked at the top level but classified by neither")

    def test_a_new_unclassified_root_directory_fails(self) -> None:
        (self.repo / "scratch").mkdir()
        self.write("scratch/plan.md", "# Plan\n")
        self.assertFails("scratch: tracked at the top level but classified by neither")

    def test_two_tables_claiming_one_path_fails(self) -> None:
        self.manifest(render_manifest(extra_internal="| `README.md` | Also internal. |\n"))
        self.assertFails("classified as both public and internal")

    def test_a_declared_file_does_not_classify_its_directory(self) -> None:
        # If `docs/policy/one.md` counted as classifying `docs/`, then adding
        # `docs/private.md` would publish it with nobody deciding to.
        self.manifest(render_manifest().replace("| `docs/` |", "| `docs/policy/` |"))
        self.assertFails("docs: tracked at the top level but classified by neither")

    def test_a_declared_directory_classifies_its_tree(self) -> None:
        self.write("docs/policy/extra.md", "# Extra\n")
        self.assertClean()


class ExistenceTest(ReleaseTest):
    def test_a_declared_public_path_that_is_absent_fails(self) -> None:
        self.write("docs/policy/extra.md", "# Extra\n")
        self.manifest(render_manifest(extra_public="| `MISSING.md` | Absent. |\n"))
        self.assertFails("MISSING.md: declared public but absent")

    def test_a_pending_path_that_exists_fails(self) -> None:
        self.write("LICENSE", "MIT\n")
        self.assertFails("LICENSE: declared public and marked pending, but it exists")

    def test_dropping_the_pending_mark_makes_it_a_real_requirement(self) -> None:
        self.manifest(render_manifest().replace("`LICENSE` (pending)", "`LICENSE`"))
        self.assertFails("LICENSE: declared public but absent")

    def test_a_present_public_path_passes(self) -> None:
        self.manifest(render_manifest(extra_public="| `docs/reference/` | Present. |\n"))
        self.assertClean()


class ContainmentTest(ReleaseTest):
    def test_a_public_file_inside_an_internal_directory_fails(self) -> None:
        (self.repo / "sessions").mkdir(exist_ok=True)
        self.write("sessions/summary.md", "# Summary\n")
        self.manifest(render_manifest(extra_public="| `sessions/summary.md` | Leaks. |\n"))
        self.assertFails("sessions/summary.md: declared public but sits inside internal")

    def test_an_internal_file_inside_a_public_directory_fails(self) -> None:
        self.write("docs/notes.md", "# Notes\n")
        self.manifest(render_manifest(extra_internal="| `docs/notes.md` | Misfiled. |\n"))
        self.assertFails("docs/notes.md: declared internal but sits inside public")


class SecretTest(ReleaseTest):
    def test_a_credential_in_a_public_path_fails(self) -> None:
        self.write("docs/credentials.md", "# Key\n\ntoken: ghp_abcdefghijklmnopqrstuvwx\n")
        self.assertFails("docs/credentials.md: credential-shaped text (github-token)")

    def test_a_credential_in_an_internal_path_fails(self) -> None:
        self.write("sessions/key.txt", "token: ghp_abcdefghijklmnopqrstuvwx\n")
        self.assertFails("sessions/key.txt: credential-shaped text (github-token)")

    def test_an_unclassified_path_is_not_scanned(self) -> None:
        # It is not published either, so a violation there is the coverage
        # check's business, not the scanner's.
        self.write("scratch/key.txt", "token: ghp_abcdefghijklmnopqrstuvwx\n")
        result = release.check()
        self.assertFalse(any("credential" in problem for problem in result.violations))
        self.assertTrue(any("scratch:" in problem for problem in result.violations))


class FrontDoorTest(ReleaseTest):
    def test_a_front_door_without_the_directive_fails(self) -> None:
        self.write("README.md", "# Fixture\n")
        self.assertFails("README.md: no <!-- origin-release-state:")

    def test_a_disagreeing_state_fails(self) -> None:
        self.write("README.md", "# Fixture\n\n<!-- origin-release-state: public-product -->\n")
        self.assertFails("README.md: declares release state `public-product` but")

    def test_an_unknown_state_fails(self) -> None:
        self.manifest(render_manifest(state="shipped"))
        self.assertFails("release state `shipped` is not one of")

    def test_a_manifest_without_the_directive_fails(self) -> None:
        self.manifest(render_manifest().replace(f"<!-- origin-release-state: {STATE} -->", "no directive here"))
        self.assertFails("no <!-- origin-release-state: ... --> directive, so there is")

    def test_a_missing_manifest_fails_rather_than_passing_empty(self) -> None:
        (self.repo / "RELEASE-MANIFEST.md").unlink()
        result = release.check()
        self.assertFalse(result.ok)
        self.assertEqual(result.checked, 0)
        self.assertTrue(any("no <!-- origin-release-state" in problem for problem in result.violations))

    def test_both_moving_together_is_the_way_through(self) -> None:
        self.manifest(render_manifest(state="public-product"))
        self.write("README.md", "# Fixture\n\n<!-- origin-release-state: public-product -->\n")
        self.assertClean()


class ParseTest(unittest.TestCase):
    """The table grammar, without a repository."""

    def test_a_row_without_a_backticked_path_classifies_nothing(self) -> None:
        entries = release.parse_entries(
            "| Path | Why |\n|---|---|\n| Product source | Not created yet. |\n"
        )
        self.assertEqual(entries, [])

    def test_several_paths_in_one_row_are_separate_entries(self) -> None:
        entries = release.parse_entries("| `a.md` `b/` | Why. |\n")
        self.assertEqual([item.path for item in entries], ["a.md", "b/"])

    def test_pending_is_read_from_the_cell(self) -> None:
        entries = release.parse_entries("| `LICENSE` (pending) | Absent. |\n")
        self.assertTrue(entries[0].pending)
        self.assertEqual(entries[0].covered, "`LICENSE` (pending)")

    def test_a_missing_section_yields_no_entries(self) -> None:
        self.assertEqual(release.parse_entries("no table here"), [])


if __name__ == "__main__":
    unittest.main()
