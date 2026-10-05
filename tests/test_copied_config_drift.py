"""E020 (T-0065) — drift is inconclusive; two figures are retracted.

Two properties are held here, both of them the way `docs/policy/gate-falsification.md`
requires: the number the results file carries, and the blindness of the readings it
retracts. A test that only asserted the surviving number would let either retraction
be quietly reinstated.

1. The marker-file probe's blindness. `.claude/agents/README.md` returning 404 does
   not mean `.claude/agents/` is absent; `validate_probe.py` recorded 8 of 8
   disagreements against the contents API. Asserting the blindness means the probe
   cannot be swapped back in as a directory listing.
2. The A4 version-record regex's blindness. It matched 17 of 31 repositories and
   every match pins a Claude Code CLI version, a hook event, or the repository's own
   release badge -- never the version of a copied configuration. The obvious rule,
   "does the README contain a version string", is green on all 17, which is exactly
   why the naive reading of 17/31 looks reasonable and is wrong.
"""

import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.join(os.path.dirname(HERE), "EXPERIMENTS", "020-copied-config-drift")


def load_results():
    with open(os.path.join(EXPERIMENT, "results.json")) as f:
        return json.load(f)


class ResultCarriesItsOwnUndecidable(unittest.TestCase):
    def test_verdict_is_inconclusive_not_a_number(self):
        r = load_results()
        self.assertEqual(r["verdict"], "inconclusive")
        self.assertEqual(r["A1_drift"]["status"], "inconclusive")
        self.assertIsNone(r["A1_drift"]["drift_rate"])

    def test_no_drift_gate_fires_rather_than_reporting_zero(self):
        """A zero and an unanswerable question must be different keys.

        017's H2 thresholds were satisfied by an empty read and the first run
        printed a verdict no evidence supported.
        """
        r = load_results()
        gate = r["gate"]
        self.assertEqual(gate["verdict"], "inconclusive")
        self.assertEqual(r["A1_drift"]["drift_rate"], None)
        self.assertIn("not a measurement of 'no drift'",
                      r["A1_drift"]["reason"].lower())

    def test_undiciides_are_never_folded_into_absence(self):
        """F036: an HTTP 200 means nothing until you know what answered it."""
        r = load_results()
        self.assertEqual(r["population"]["settings_state"]["UNDECIDABLE"], 0)
        self.assertIn(r["population"]["settings_state"]["ABSENT"],
                      list(r["population"]["settings_state"].values()))


class RetractedFiguresStayRetracted(unittest.TestCase):
    def test_a4_version_record_is_marked_retracted(self):
        r = load_results()
        a4 = r["A4_version_record"]
        self.assertEqual(a4["status"], "retracted")
        self.assertIn("must not be cited", a4["reason"])

    def test_marker_probe_is_marked_falsified(self):
        r = load_results()
        probe = r["instrument_falsification"]["marker_probe"]
        self.assertEqual(probe["status"], "falsified")
        self.assertEqual(probe["disagreements"], probe["checked_against_contents_api"])

    def test_the_naive_a4_rule_is_green_on_the_data_it_must_not_read(self):
        """The falsification of the rejected rule.

        If the obvious rule were red here, nobody would be tempted to reinstate it.
        The rule is green on every one of the 17 rows it matched, and every one of
        those rows is a pin on something other than a copied configuration.
        """
        r = load_results()
        # The rejected rule itself, imported from the instrument that used it, so
        # the test cannot drift away from the thing it is falsifying.
        sys.path.insert(0, EXPERIMENT)
        from analyse import VERSION_HINT
        naive = VERSION_HINT
        # Raw captures live in captured_bodies.json: they are third-party data, so
        # storing them as .md made doc lint check a stranger's links as ours.
        bodies_path = os.path.join(EXPERIMENT, "raw", "captured_bodies.json")
        self.assertTrue(os.path.exists(bodies_path),
                        "the raw capture must be committed for this to mean anything")
        with open(bodies_path) as f:
            bodies = json.load(f)["repos"]
        matched = 0
        for repo, paths in bodies.items():
            readme = paths.get("README.md")
            if readme and naive.search(readme):
                matched += 1
        self.assertGreater(matched, 0,
                           "the naive rule must be green on the corpus, or the "
                           "retraction is untested")
        # The rejected rule reproduces exactly the number the retraction is about,
        # which is why the figure looked trustworthy.
        self.assertEqual(matched, r["A4_version_record"]["recorded"])
        # ...and the retracted figure is nonetheless marked as unreadable.
        self.assertEqual(load_results()["A4_version_record"]["status"], "retracted")


class SurvivingFigureIsHeld(unittest.TestCase):
    def test_cross_author_bundles_is_zero_and_the_gate_wording_excludes_own_author(self):
        """The kill gate said "a different author's repository".

        Two of the repositories do overlap by >=50%, and a reader who sees only the
        count of 2 would conclude copying is common. The exclusion of one author's
        two repositories is load-bearing, so it is asserted here rather than left
        in prose.
        """
        r = load_results()
        a5 = r["A5_structural_attribution"]
        self.assertEqual(a5["cross_author_bundles"], 0)
        self.assertEqual(a5["n_repos_with_bundle_share_ge_0_5"], 2)
        self.assertEqual(a5["same_author_bundles"],
                         [["shanraisshan/claude-code-hooks",
                           "shanraisshan/claude-code-best-practice"]])
        authors = set()
        for pair in a5["same_author_bundles"]:
            for repo in pair:
                authors.add(repo.split("/")[0])
        self.assertEqual(len(authors), 1, "the excluded bundle must be one author")

    def test_nonsense_control_keeps_the_instrument_honest(self):
        """F036 again: a number means nothing without a row that must be zero."""
        r = load_results()
        q = r["documented_copying"]["queries"]
        self.assertEqual(q["nonsense_token_control"], 0)
        self.assertGreater(q['content:"cp -r .claude"'], 100)
        self.assertIn("not an artefact of matching everything",
                      r["documented_copying"]["note"])

    def test_control_population_confound_is_declared(self):
        """The 1/150 containment rate is NOT a prevalence, and says so."""
        r = load_results()
        self.assertIn("CANNOT be read as a prevalence",
                      r["control_population"]["confound"])


if __name__ == "__main__":
    unittest.main()