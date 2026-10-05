"""E028's capture integrity: what was fetched, what was refused, and what a
reader was shown.

Split from `test_gates_falsified.py` at the 300-line cap, by invariant: this file
holds the *capture* — reader separation, the rubric's neutrality, the stored
documentation and the refusals recorded beside it. The sibling holds the *gates*
— the verdict, the controls, agreement, and the arithmetic.

Both are asserted against committed bytes. Every defect listed in the README as
found by these tests was found by one of them.
"""
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


def read_jsonl(name):
    with open(os.path.join(RAW, name)) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def fetch_log():
    """One record per artifact: a capture holding text is never overwritten by
    a later refusal (F041), so the last text-bearing record wins."""
    best = {}
    for rec in read_jsonl("fetch_log.jsonl"):
        key = (rec["row"], rec["corpus"], rec["artifact"])
        if key not in best or (rec["has_text"] and not best[key]["has_text"]):
            best[key] = rec
    return best


class TestNoArtifactIsPairedWithItsOwnRequirement(unittest.TestCase):
    """Amendment 1 §4. A control that could pass by construction proves nothing."""

    def test_no_view_entry_pairs_a_row_with_its_own_bundle(self):
        for reader in ("r1", "r2"):
            with open(os.path.join(RAW, "view_b_%s.json" % reader)) as fh:
                view = json.load(fh)
            log = {}
            for rec in read_jsonl("fetch_log.jsonl"):
                key = (rec["row"], rec["corpus"], rec["artifact"])
                if key not in log or (rec["has_text"]
                                      and not log[key]["has_text"]):
                    log[key] = rec
            for entry in view["view"]:
                own = {rec["artifact"] for key, rec in log.items()
                       if key[0] == entry["row"]}
                if entry["pairing"] == "mismatched_with":
                    self.assertNotEqual(entry["mismatched_with"], entry["row"])
                    donor = {rec["artifact"] for key, rec in log.items()
                             if key[0] == entry["mismatched_with"]}
                    self.assertFalse(own & donor,
                                     "%s: control shares an artifact with its "
                                     "own row" % entry["row"])

    def test_control_rule_is_the_declared_shift(self):
        with open(os.path.join(RAW, "view_b_r1.json")) as fh:
            view = json.load(fh)
        rows = view["fit_rows"]
        for entry in view["view"]:
            if entry["pairing"] == "mismatched_with":
                i = rows.index(entry["row"])
                self.assertEqual(entry["mismatched_with"],
                                 rows[(i + 1) % len(rows)])


class TestReadersCannotSeeTheVerdict(unittest.TestCase):
    """The separation the whole measurement rests on."""

    def test_requirements_carry_no_verdict_and_no_artifact(self):
        for row in read_jsonl("requirements.jsonl"):
            self.assertNotIn("cause", row)
            self.assertNotIn("reason", row)
            self.assertNotIn("verdict", row)
            self.assertNotIn("artifacts", row)
            self.assertNotIn("note", row)

    def test_record_facts_is_the_only_place_a_verdict_appears(self):
        facts = read_jsonl("record_facts.json")
        self.assertEqual(len(facts), 19)
        for row in facts:
            self.assertIn("verdict", row)
            self.assertIn("e016_note", row)

    def test_step_a_names_no_incumbent_the_screen_named(self):
        """F047's shape: a reader who has already met a product cannot read the
        requirement cleanly again.

        The check is against the incumbents actually named for that row, not
        against a word list. A requirement that mentions GitHub in passing
        (`attribute_note` quotes it) is not contamination; a reader naming
        `mem0ai/mem0` in `category` or `attribute` before the product pass is.
        """
        reqs = {r["row"]: r["requirement_text"].lower()
                for r in read_jsonl("requirements.jsonl")}
        named = {}
        for rec in read_jsonl("fetch_log.jsonl"):
            named.setdefault(rec["row"], set()).add(rec["artifact"])
        checked = 0
        for reader in ("r1", "r2"):
            for row in read_jsonl("step_a_%s.jsonl" % reader):
                decided = " ".join(str(row.get(k) or "")
                                   for k in ("category", "attribute")).lower()
                for artifact in named.get(row["row"], ()):
                    # Two checks, neither needing an exemption list of English
                    # words. The owner segment is a proper name no reader
                    # would coin ("muni-town", "mem0ai"), and the
                    # separator-stripped artifact is a string no prose
                    # contains ("muniatprotohandleResolver"). A word like
                    # "handle" that is both a product token and ordinary
                    # English is not evidence of anything, so it is not the
                    # thing checked.
                    owner = re.split(r"[/.]", artifact.strip())[0].lower()
                    squashed = re.sub(r"[^A-Za-z0-9]", "",
                                      artifact).lower()
                    for token in (owner, squashed):
                        if len(token) < 5:
                            continue
                        if token in reqs[row["row"]]:
                            continue
                        checked += 1
                        self.assertNotIn(
                            token, decided,
                            "%s %s names incumbent %r in Step A"
                            % (reader, row["row"], artifact))
        self.assertGreater(checked, 20, "too few checks for the test to read")


class TestTheRubricDidNotLeakARecordedVerdict(unittest.TestCase):
    def test_rubric_defines_the_labels_but_names_no_row(self):
        """The rubric must define every label and must not point at one. A rubric
        that says `H03 here is obviously served` is a rubric with an answer in
        it, and the declared positive control then tests nothing."""
        with open(os.path.join(HERE, "RUBRIC.md")) as fh:
            rubric = fh.read().lower()
        for label in ("serves", "partial", "does_not_serve", "unreadable",
                      "no_distinguishing_attribute"):
            self.assertIn(label, rubric)
        for token in ("h03", "h08", "h26", "webp", "sharp", "uptime",
                      "notion", "anki", "pattern projector"):
            self.assertNotIn(token, rubric,
                             "rubric names %r, which points at a row" % token)

class TestAnEmptyCaptureIsARefusalNotACapture(unittest.TestCase):
    """The defect this run found in itself.

    Eight `openweb` fetches returned HTTP 200 with a body that stripped to zero
    bytes. The first version of `store()` wrote the file, and a later reader
    reads an empty file as *"this product's documentation says nothing"* rather
    than *"we did not get it."* The two are opposite readings and only one of
    them is true.
    """

    def test_a_200_that_stripped_to_nothing_is_recorded_as_a_refusal(self):
        refused = [r for r in fetch_log().values() if not r["has_text"]]
        self.assertTrue(refused)
        for rec in refused:
            self.assertEqual(rec["chars"], 0)
            self.assertIn("how", rec)
            self.assertTrue(rec["how"].strip())

    def test_no_refused_artifact_has_a_file_on_disk(self):
        """An empty file must be removed, not merely marked in the log: a later
        reader opens the path, not the log."""
        docs = os.path.join(RAW, "docs")
        for rec in fetch_log().values():
            if rec["has_text"]:
                continue
            self.assertFalse(os.path.exists(rec["path"]),
                             "%s has no text but a file exists at %s"
                             % (rec["artifact"], rec["path"]))

    def test_the_declared_character_cap_holds(self):
        for rec in fetch_log().values():
            if not rec["has_text"]:
                continue
            self.assertLessEqual(rec["chars"], 12000, rec["artifact"])

    def test_every_artifact_the_screen_named_appears_in_the_log(self):
        """A named artifact that was never attempted would silently shrink a
        bundle, and a shrunken bundle reads as a smaller incumbent set."""
        named = {}
        for bundle in read_jsonl("incumbents.jsonl"):
            for entry in bundle["artifacts"]:
                key = (bundle["row"], entry["corpus"], entry["artifact"])
                named[key] = True
        attempted = set(fetch_log())
        self.assertEqual(set(named) - attempted, set())
        self.assertEqual(len(named), 90)


class TestTheBundleIsTheScreenOrderNotTheReadersOrder(unittest.TestCase):
    """Amendment 2 §4: the first four artifacts the screen listed. A cap chosen
    after the labels would be a cap fitted to a result."""

    def test_bundles_are_the_first_four_named_in_log_order(self):
        """The window is the screen's first four, and an artifact inside the
        window whose documentation is missing stays in the window with an empty
        body. Swapping in an artifact from further down would change what the
        reader was shown after the fact, which is the one thing the bundle's
        reproducibility is for."""
        log = fetch_log()
        for reader in ("r1", "r2"):
            with open(os.path.join(RAW, "view_b_%s.json" % reader)) as fh:
                view = json.load(fh)
            for entry in view["view"]:
                if entry["pairing"] != "own":
                    continue
                window = [k[2] for k in log if k[0] == entry["row"]][:4]
                shown = [a["artifact"] for a in entry["artifacts_shown"]]
                self.assertEqual(shown, window,
                                 "%s %s: bundle is not the screen's window"
                                 % (reader, entry["row"]))

    def test_an_artifact_without_documentation_is_flagged_in_the_bundle(self):
        """A reader must be able to tell "no documentation" from "documentation
        that says nothing", because the rubric routes them to different labels."""
        log = fetch_log()
        flagged = 0
        for reader in ("r1", "r2"):
            with open(os.path.join(RAW, "view_b_%s.json" % reader)) as fh:
                view = json.load(fh)
            for entry in view["view"]:
                for a in entry["artifacts_shown"]:
                    key = (entry["row"], a["corpus"], a["artifact"])
                    if key not in log:
                        continue
                    self.assertEqual(a["has_documentation"],
                                     log[key]["has_text"])
                    if not a["has_documentation"]:
                        flagged += 1
                        self.assertEqual(a["documentation_shown"], "")
        self.assertGreater(flagged, 0,
                           "no bundle carries a missing document, so the "
                           "flag is untested")

    def test_the_number_named_but_not_shown_is_published(self):
        for reader in ("r1", "r2"):
            with open(os.path.join(RAW, "view_b_%s.json" % reader)) as fh:
                view = json.load(fh)
            for entry in view["view"]:
                if entry["pairing"] == "mismatched_with":
                    continue
                self.assertIsInstance(entry["artifacts_named_but_not_shown"],
                                      int)
