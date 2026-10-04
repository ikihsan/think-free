"""`preflight` must run every gate a change in this repository can break.

`preflight` was lint, skills and session verification — the three an agent is told
to run before it commits. It did not run `release check`, which enforces
`RELEASE-MANIFEST.md`: every tracked top-level entry must be classified exactly
once. T-0042 added `DECISIONS-RECORDS.md` at the top level, declared nothing about
it, and its own `verify` command passed, because the gate that would have said so
was not in the command. Run `37191658964` at `c9e89e1` is red with one real
violation, named in an annotation because T-0040 made this readable without admin
rights — and it took the other VM's work to make this VM's omission visible.

The general form is already in this repository's record about generated files: a
generated-file invariant belongs below the layer that changes its input. This is
the same statement about gates — **a gate belongs in the one command the protocol
tells every agent to run**, or the next agent repeats the omission.

The falsification is the interesting half, and it is a negative one: preflight
passes on a repository carrying an unclassified root document, because the
pre-change `preflight` never asked. `CleanFixtureTest` is the control that must
stay silent — a repository that classifies everything still passes.
"""

from __future__ import annotations

import unittest

from harness import RepoTest

from test_release import STATE, render_manifest


class PreflightCoversReleaseTest(RepoTest):
    """One gate per clause, so a failure names which gate refused."""

    def setUp(self) -> None:
        super().setUp()
        self.write("RELEASE-MANIFEST.md", render_manifest())
        self.write("README.md", f"# Fixture\n\n<!-- origin-release-state: {STATE} -->\n")

    def preflight(self) -> tuple[int, str]:
        # Through the CLI, because that is how an agent runs it and because the
        # harness captures the process's stdout rather than a call's return.
        code = self.cli("preflight")
        return code, self.output()

    def test_an_unclassified_root_document_fails_preflight(self) -> None:
        # The defect's own shape: T-0042's file, and the state it left the tree
        # in. Before this change preflight never asked, so the release line was
        # absent from its output entirely — which is the falsification, and it is
        # why the assertion is about that line rather than the exit code: a
        # throwaway fixture is not clean for the other three gates.
        self.write("DECISIONS-RECORDS.md", "# Decisions — records\n")
        _, out = self.preflight()
        self.assertIn("release check:", out)
        self.assertIn("classified by neither manifest table", out)
        self.assertIn("DECISIONS-RECORDS.md", out)

    def test_a_classified_root_document_passes_preflight(self) -> None:
        # The control that must stay silent. If release check ran but always
        # failed, the first test would pass for the wrong reason.
        self.write("DECISIONS-RECORDS.md", "# Decisions — records\n")
        self.write(
            "RELEASE-MANIFEST.md",
            render_manifest(extra_internal="| `DECISIONS-RECORDS.md` | The decision log. |\n"),
        )
        _, out = self.preflight()
        self.assertIn("release check: OK", out)

    def test_preflight_says_which_gate_refused(self) -> None:
        # `preflight: FAILED` alone would send a reader to the wrong file; the
        # gate's own line is printed above the verdict, so the verdict names it.
        self.write("DECISIONS-RECORDS.md", "# Decisions — records\n")
        _, out = self.preflight()
        self.assertTrue(
            out.index("release check:") < out.index("preflight:"),
            "the gate's line must come before the verdict it decides",
        )


if __name__ == "__main__":
    unittest.main()