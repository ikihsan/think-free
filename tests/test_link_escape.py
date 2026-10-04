"""A link's verdict must be a function of the repository, not of its neighbours.

T-0047 shipped the link `../../docs/reference/identifier-allocation.md` from a
task file, and recorded in that task file that `doc lint` passed on it in the
worktree the branch was built in and failed on the same bytes in the main
checkout after landing — and that it could not reproduce which run decided it.
That is not a run's property. It is the rule's: `check_links` resolved a
relative link with `Path.exists()`, so a link that escapes the repository root
was decided by whatever the checkout's *parent directory* happened to hold.

`ParentDependenceTest` is that reproduction, built from two checkouts of one
commit whose parents differ, so the surroundings are the only variable. The
previous rule is written out in that test rather than imported, because after the
repair the production code can no longer demonstrate its own defect, and a test
that only asserted the new behaviour would pass just as happily against a rule
that had never been broken.

**Ceiling.** Only inline Markdown links are read, and only containment is judged
here: a link that resolves inside the repository but to the wrong document, a
reference link (`[x][1]`) and a bare autolink are all still unexamined.
"""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from harness import RepoTest, git, make_repo

from originlib import doclint

# The escaping link T-0047 shipped, byte for byte. From `tasks/` it leaves the
# repository; from `.worktrees/<name>/tasks/` it lands back inside the main
# checkout, which is the whole accident.
ESCAPING_TARGET = "../../docs/reference/identifier-allocation.md"
ROOT_RELATIVE_TARGET = "docs/policy/doc-standards.md"
ESCAPING = f"[allocation]({ESCAPING_TARGET})"
ROOT_RELATIVE = f"[standards]({ROOT_RELATIVE_TARGET})"

PROBE = (
    "<!-- origin-meta\n"
    "owner: docs/INDEX.md\n"
    "status: active\n"
    "last-verified: 2026-10-04\n"
    "-->\n\n"
    "# probe\n\n"
    f"{ESCAPING}\n\n"
    f"{ROOT_RELATIVE}\n"
)

BODY = (
    "<!-- origin-meta\n"
    "owner: docs/INDEX.md\n"
    "status: active\n"
    "last-verified: 2026-10-04\n"
    "-->\n\n"
    "# probe\n\n"
    "{body}\n"
)


def probe_body(link: str) -> str:
    return BODY.replace("{body}", link)


def link_findings(path: Path) -> list[str]:
    """Only this rule's findings, for one document, with the rest of the lint out of the way."""
    result = doclint.Result()
    doclint.check_links(result, [path])
    return [str(item) for item in result.violations]


def previous_rule(path: Path, base: Path) -> dict[str, str]:
    """The rule as it was before the repair, written out rather than imported.

    `check_links` resolved each candidate with `exists()` and reported a broken
    link when neither existed — a question about the filesystem, and the
    filesystem includes whatever sits above the checkout.
    """
    verdicts: dict[str, str] = {}
    for target, _line in doclint._links(path.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean = target.split("#", 1)[0]
        if not clean:
            continue
        candidates = [(path.parent / clean), (base / clean)]
        verdicts[target] = (
            "ok" if any(candidate.exists() for candidate in candidates) else "broken"
        )
    return verdicts


class ParentDependenceTest(RepoTest):
    """Two checkouts of one commit, differing only in what sits above them."""

    def setUp(self) -> None:
        super().setUp()
        # One checkout whose parent holds the document the escaping link names,
        # and one whose parent does not. Identical bytes in both.
        neighbourhood = Path(tempfile.mkdtemp(prefix="origin-neighbourhood-"))
        self.addCleanup(shutil.rmtree, neighbourhood, ignore_errors=True)
        rich, bare = neighbourhood / "rich", neighbourhood / "bare"
        (rich / "docs" / "reference").mkdir(parents=True, exist_ok=True)
        (rich / "docs" / "reference" / "identifier-allocation.md").write_text(
            "a neighbour of the checkout, not part of it\n", encoding="utf-8"
        )
        self.rich = make_repo(self, _existing=rich / "checkout")
        self.bare = make_repo(self, _existing=bare / "checkout")
        for root in (self.rich, self.bare):
            (root / "tasks" / "probe.md").write_text(PROBE, encoding="utf-8")
            git(root, "add", "-A")
            git(root, "commit", "-qm", "the same bytes in two neighbourhoods")

    def verdicts(self, root: Path) -> list[str]:
        self.use(root)
        return link_findings(root / "tasks" / "probe.md")

    def test_the_same_document_is_judged_the_same_wherever_the_checkout_sits(self) -> None:
        rich, bare = self.verdicts(self.rich), self.verdicts(self.bare)
        self.assertEqual(
            rich, bare, "one document, linted at two checkout locations, disagreed"
        )
        self.assertEqual(len(rich), 1, f"expected exactly one finding, got {rich}")
        self.assertIn("leaves the repository", rich[0])
        # The neighbouring document is what the old rule consulted; it is still
        # there, so the equality above is not the rule refusing to look.
        self.assertTrue((self.rich.parent / "docs" / "reference" / "identifier-allocation.md").is_file())

    def test_the_previous_rule_disagreed_on_those_same_bytes(self) -> None:
        """The witness. A control that cannot fail is not a falsification."""
        self.use(self.rich)
        rich = previous_rule(self.rich / "tasks" / "probe.md", self.rich)
        self.use(self.bare)
        bare = previous_rule(self.bare / "tasks" / "probe.md", self.bare)
        self.assertEqual(rich[ESCAPING_TARGET], "ok", rich)
        self.assertEqual(bare[ESCAPING_TARGET], "broken", bare)
        # And the same rule agreed about the root-relative link in both, which is
        # why the disagreement above is the escaping one and not the rule at large.
        self.assertEqual(rich[ROOT_RELATIVE_TARGET], bare[ROOT_RELATIVE_TARGET])


class LinkRuleTest(RepoTest):
    """The rule itself, in one checkout."""

    def verdicts(self, link: str) -> list[str]:
        self.write("tasks/probe.md", probe_body(link))
        return link_findings(self.repo / "tasks" / "probe.md")

    def test_a_relative_link_out_of_the_repository_is_reported_with_its_place(self) -> None:
        found = self.verdicts(ESCAPING)
        self.assertEqual(len(found), 1, f"expected one finding, got {found}")
        self.assertIn("link leaves the repository -> ../../docs", found[0])
        self.assertTrue(found[0].startswith("tasks/probe.md: "), found[0])

    def test_an_absolute_path_out_of_the_repository_is_reported(self) -> None:
        found = self.verdicts("[host](/etc/hostname)")
        self.assertEqual(len(found), 1, f"expected one finding, got {found}")
        self.assertIn("link leaves the repository -> /etc/hostname", found[0])

    def test_a_missing_link_inside_the_repository_is_still_broken(self) -> None:
        found = self.verdicts("[gone](../docs/reference/not-here.md)")
        self.assertEqual(len(found), 1, f"expected one finding, got {found}")
        self.assertIn("broken link -> ../docs/reference/not-here.md", found[0])
        self.assertNotIn("leaves the repository", found[0])

    def test_a_link_inside_the_repository_is_silent(self) -> None:
        self.assertEqual(self.verdicts("[standards](../docs/policy/doc-standards.md)"), [])

    def test_a_root_relative_link_is_still_resolved_against_the_root(self) -> None:
        """`docs/policy/…` from `tasks/` resolves only through the root candidate."""
        self.assertEqual(self.verdicts(ROOT_RELATIVE), [])

    def test_the_finding_carries_the_line_the_link_is_on(self) -> None:
        self.write("tasks/probe.md", PROBE)
        git(self.repo, "add", "-A")
        escapes = [
            item
            for item in doclint.lint().violations
            if "leaves the repository" in str(item) and item.path == "tasks/probe.md"
        ]
        self.assertEqual(len(escapes), 1, [str(i) for i in doclint.lint().violations])
        self.assertEqual(escapes[0].line, PROBE.splitlines().index(ESCAPING) + 1)

    def test_annotate_publishes_it_as_a_check_run_annotation(self) -> None:
        # T-0040's mechanism on this violation: a red run must name the file from
        # its own annotations, since the run log needs admin rights. A violation
        # whose rule knows its location must carry it, or it is reported in text
        # only and the annotation points nowhere.
        self.write("tasks/probe.md", PROBE)
        git(self.repo, "add", "-A")
        exit_code = self.cli("annotate", "--", "doc lint")
        self.assertEqual(exit_code, 2, self.output())
        published = [
            line
            for line in self.output().splitlines()
            if line.startswith("::") and "leaves the repository" in line
        ]
        self.assertEqual(len(published), 1, self.output())
        self.assertTrue(published[0].startswith("::error "), published[0])
        self.assertIn("file=tasks/probe.md", published[0])
        self.assertIn(f"line={PROBE.splitlines().index(ESCAPING) + 1}", published[0])


class NoRegressionTest(unittest.TestCase):
    """The control that cannot fire: this repository has no escaping link.

    Measured with the rule in place on 2026-10-04: 577 inline links across the
    tracked Markdown, none of which leaves the repository. The rule therefore
    adds a verdict without adding a violation, and this is where that is stated
    rather than assumed — a rule that only ever fires is indistinguishable from a
    rule that is broken, which is the mistake the previous mutation made in
    T-0047's session.
    """

    def test_no_tracked_link_leaves_the_repository(self) -> None:
        from originlib import docfiles, paths

        root = paths.repo_root()
        files = docfiles.tracked_files(root)
        examined = 0
        for path in files:
            if path.suffix != ".md":
                continue
            examined += len(doclint._links(path.read_text(encoding="utf-8", errors="replace")))
        # 577 on 2026-10-04. The floor is well below that so the assertion cannot
        # pass by reading almost nothing, and well above a scan that found no
        # `.md` files at all.
        self.assertGreaterEqual(examined, 100, "the scan read almost nothing")
        result = doclint.Result()
        doclint.check_links(result, files)
        escapes = [str(i) for i in result.violations if "leaves the repository" in str(i)]
        broken = [str(i) for i in result.violations if "broken link" in str(i)]
        self.assertEqual(escapes, [], f"{len(escapes)} of {examined} links leave the repository")
        # The other half of the same control: without it, a rule that stopped
        # checking links entirely would pass the assertion above.
        self.assertEqual(broken, [], f"{len(broken)} broken links in the repository itself")


if __name__ == "__main__":
    unittest.main()
