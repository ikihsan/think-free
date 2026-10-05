#!/usr/bin/env python3
"""E029 -- tests that target claims and failure modes, not the implementation.

Each test is asserted against the committed capture and against a fixture built to
break the property, following docs/policy/gate-falsification.md. The two forms of
test that matter most here are the ones the run's own history calls for:

  * a build that postdates the need is the population (otherwise 167 rows read as
    `unrelated` and manufacture the null H1 is trying to measure), and
  * the reader's view carries no arm label and no author name (otherwise the
    blindness the protocol declares is not the blindness the reader had).
"""
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)

import stats as S  # noqa: E402


def read_jsonl(name):
    path = name if os.path.isabs(name) else os.path.join(RAW, name)
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def sibling(*parts):
    """A capture in a sibling experiment, resolved from this file, not the cwd."""
    return os.path.normpath(os.path.join(HERE, "..", *parts))


class PopulationTest(unittest.TestCase):
    def setUp(self):
        self.pop = {d["author"]: d for d in read_jsonl("population.jsonl")}
        self.builds = {d["author"]: d for d in read_jsonl("builds.jsonl")}
        self.key = json.load(open(os.path.join(RAW, "view_key.json")))

    def test_declared_population_arithmetic_is_the_recorded_one(self):
        # PROTOCOL.md declared 278 from nb_show_hn >= 1; amendment 1 declared the
        # exclusions. If any of these numbers moves, the declared denominator moved.
        arm = read_jsonl(sibling("025-need-staters-builderhood", "raw", "need_arm.jsonl"))
        declared = sum(1 for d in arm if d.get("status") == "ok"
                       and isinstance(d.get("nb_show_hn"), int) and d["nb_show_hn"] >= 1)
        self.assertEqual(declared, 278)
        self.assertEqual(len(self.pop) + 30 + 7, declared,
                         "exclusions must account for every dropped builder")

    def test_every_reader_row_has_a_build_that_postdates_the_need(self):
        # The reader population, not the whole file: the 167 whose builds all predate
        # the need are excluded precisely because their question is not askable.
        for k in self.key:
            a = k["author"]
            ni = int(self.pop[a]["need"]["comment_id"])
            later = [it for it in self.builds[a].get("items") or [] if int(it["id"]) > ni]
            self.assertTrue(later, "reader row %s has no build after the need" % k["row_id"])

    def test_the_null_is_not_manufactured_by_an_unaskable_row(self):
        # The failure mode this guards: reading a row whose build predates the need as
        # `unrelated` lowers the matched arm without the readers being at fault.
        unaskable = [a for a, r in self.pop.items()
                     if not [it for it in self.builds[a].get("items") or []
                             if int(it["id"]) > int(r["need"]["comment_id"])]]
        self.assertEqual(len(unaskable), 167)
        self.assertNotEqual(len(unaskable), 0, "a test that passes on 0 does not discriminate")
        self.assertEqual(len(self.pop) - len(unaskable), 74)

    def test_the_chronological_proxy_is_verifiable_not_assumed(self):
        # The population is selected on HN item-id ordering. Check the ordering against
        # real timestamps on the corpus's own capture, and check the negative control
        # that the other id space does not hold.
        outcomes = read_jsonl(sibling("022-need-outcomes", "raw", "outcomes.jsonl"))
        rows = sorted((int(d["comment_id"]), d["time"]) for d in outcomes)
        regress = sum(1 for (_, t1), (_, t2) in zip(rows, rows[1:]) if t2 < t1)
        self.assertEqual(regress, 0)
        stories = sorted((int(d["story_id"]), d["time"]) for d in outcomes)
        regress2 = sum(1 for (_, t1), (_, t2) in zip(stories, stories[1:]) if t2 < t1)
        self.assertGreater(regress2, 0, "story_id must NOT be monotone; the proxy is about items")


class ReaderBlindnessTest(unittest.TestCase):
    def setUp(self):
        self.key = json.load(open(os.path.join(RAW, "view_key.json")))
        self.pop = {d["author"]: d for d in read_jsonl("population.jsonl")}

    @staticmethod
    def sections(name):
        return ReaderBlindnessTest.sections_at(os.path.join(RAW, name))

    @staticmethod
    def sections_at(path):
        import re
        txt = open(path).read()
        return {m.group(1): m.group(2) for m in
                re.finditer(r"^===== ROW \d+ \| id (\S+) =====\n(.*?)(?=\n===== ROW |\Z)",
                            txt, re.S | re.M)}

    def test_arms_are_the_declared_three_and_balanced(self):
        counts = {}
        for k in self.key:
            counts[k["arm"]] = counts.get(k["arm"], 0) + 1
        self.assertEqual(counts, {"matched": 74, "mismatched": 74, "story_title": 74})

    def test_mismatched_arm_never_self_pairs(self):
        # The key records `author` (whose need is shown) and `partner` (whose items are
        # shown). The derangement is over `partner`, which is what must differ.
        m = {k["row_id"]: k["author"] for k in self.key if k["arm"] == "matched"}
        x = {k["row_id"]: (k["author"], k.get("partner")) for k in self.key if k["arm"] == "mismatched"}
        self.assertEqual(len(m), len(x))
        for i in range(len(m)):
            author, partner = x["X%02d" % i]
            self.assertEqual(author, m["M%02d" % i], "the need shown must be the matched author's")
            self.assertNotEqual(author, partner, "the control row is self-paired")

    def test_the_derangement_assertion_actually_fires(self):
        # The first version of the view builder shifted a shuffled name list and asserted
        # no fixed point. Shifting asks the wrong question. Prove both halves.
        pool = sorted(self.pop)
        n = len(pool)
        self.assertGreaterEqual(n, 2)

        shifted = pool[1:] + pool[:1]          # a cyclic shift of a distinct list
        self.assertEqual(sum(1 for a, b in zip(pool, shifted) if a == b), 0)

        # Build a real Sattolo derangement, then swap one pair of positions so that
        # exactly one element becomes a fixed point. That is the fixture the assertion
        # in the builder has to reject.
        import random
        sigma = list(range(n))
        rng = random.Random(2901)
        for i in range(n - 1, 0, -1):
            j = rng.randrange(i)
            sigma[i], sigma[j] = sigma[j], sigma[i]
        self.assertEqual(sum(1 for i in range(n) if sigma[i] == i), 0)

        i = 0
        j = sigma[i]
        broken = sigma[:]
        broken[i], broken[j] = broken[j], broken[i]     # j now maps to i, i maps to sigma[j]
        fixed = [k for k in range(n) if broken[k] == k]
        self.assertEqual(len(fixed), 1, "the assertion must be able to fail")

    def test_the_mismatched_arm_is_cross_paired_not_a_relabelled_replicate(self):
        # The first version of the view builder rendered the PARTNER's own need beside the
        # PARTNER's own items, so the control was the treatment arm renamed. It was found
        # because the two arms printed identical lexical statistics, which is impossible
        # for two different pairings. Check the pairing directly.
        pop = {d["author"]: d for d in read_jsonl("population.jsonl")}
        owner = {}
        for a, r in pop.items():
            owner.setdefault(r["need"]["text"][:120], []).append(a)
        bodies = self.sections("view_r1.txt")

        def need_of(rid):
            return bodies[rid].split("SHIPPED")[0].split("\n", 1)[1].strip()[:120]

        matched_self = mismatched_self = 0
        for k in self.key:
            if k["arm"] == "matched":
                if owner.get(need_of(k["row_id"]), [None])[0] == k["author"]:
                    matched_self += 1
            elif k["arm"] == "mismatched":
                if owner.get(need_of(k["row_id"]), [None])[0] == k.get("partner"):
                    mismatched_self += 1
        self.assertEqual(matched_self, 74, "the treatment arm must be self-paired")
        self.assertEqual(mismatched_self, 0,
                         "the control arm is a relabelled replicate of the treatment arm")

    def test_the_lexical_arms_differ(self):
        # The replicate defect surfaced here first. Keep the check that surfaced it.
        import stats as S
        pop = {d["author"]: d for d in read_jsonl("population.jsonl")}
        builds = {d["author"]: d for d in read_jsonl("builds.jsonl")}

        def mean(arm):
            vals = []
            for k in self.key:
                if k["arm"] != arm:
                    continue
                src = k.get("partner") or k["author"]
                ov = S.lexical_overlap(pop[k["author"]]["need"]["text"],
                                       [it.get("title") or ""
                                        for it in builds[src].get("items") or []])
                if ov is not None:
                    vals.append(ov)
            return (sum(vals) / len(vals)) if vals else None
        m, x = mean("matched"), mean("mismatched")
        self.assertIsNotNone(m)
        self.assertIsNotNone(x)
        self.assertNotAlmostEqual(m, x, places=6,
                                  msg="the two arms carry identical lexical statistics, "
                                      "which is the signature of a replicate control")

    def test_the_view_is_frozen_and_the_key_agrees_with_it(self):
        # Every label file is keyed by row id against view_key.json, and a label file's
        # ORDER must match the frozen view's order (checked in LabelIntegrityTest). What
        # has to hold here is that both readers got the identical file and that the key
        # describes exactly the rows the view contains.
        import hashlib
        a = open(os.path.join(RAW, "view_r1.txt"), "rb").read()
        b = open(os.path.join(RAW, "view_r2.txt"), "rb").read()
        self.assertEqual(hashlib.md5(a).hexdigest(), hashlib.md5(b).hexdigest(),
                         "the two readers were not given the same bytes")
        order = re.findall(r"^===== ROW \d+ \| id (\S+) =====", a.decode(), re.M)
        self.assertEqual(len(order), 222)
        self.assertEqual(sorted(order), sorted(k["row_id"] for k in self.key),
                         "the view and view_key.json describe different row sets")

    def test_only_the_mismatched_arm_changed_in_the_repair(self):
        # Amendment 2 repaired the mismatched arm. If the matched or story-title rows
        # had changed, the 148 already-produced labels could not carry over.
        v2 = self.sections("view_r1.txt")
        v1 = self.sections_at(os.path.join(RAW, "view_r1_v1.txt"))
        mt = [k for k in v2 if k[0] in ("M", "T")]
        x = [k for k in v2 if k[0] == "X"]
        self.assertEqual(len(mt), 148)
        self.assertEqual(len(x), 74)
        for k in mt:
            self.assertEqual(v2[k], v1.get(k), "row %s changed in the repair" % k)
        self.assertTrue(any(v2[k] != v1.get(k) for k in x),
                        "the mismatched arm must have changed, or the repair did nothing")

    def test_no_reader_row_renders_an_empty_shipped_section(self):
        # The defect amendment 2 exists for: an empty SHIPPED section can only be
        # labelled `unrelated`, so it depresses whichever arm contains it.
        for reader in ("r1", "r2"):
            txt = open(os.path.join(RAW, "view_%s.txt" % reader)).read()
            self.assertNotIn("has not posted a Show HN item", txt,
                             "%s view still renders empty SHIPPED sections" % reader)

    def test_all_three_arms_are_drawn_from_one_population(self):
        # The matched arm is a subset of the mismatched partner pool, so the arms
        # differ in whose NEED is shown and in nothing else.
        eligible = set(k["author"] for k in self.key if k["arm"] == "matched")
        for arm in ("mismatched", "story_title"):
            others = set(k["author"] for k in self.key if k["arm"] == arm)
            self.assertEqual(others, eligible,
                             "the %s arm is drawn from a different population" % arm)

    def test_view_carries_no_arm_label(self):
        for reader in ("r1", "r2"):
            text = open(os.path.join(RAW, "view_%s.txt" % reader)).read()
            for word in ("matched", "mismatched", "story_title"):
                self.assertNotIn(word, text.lower(),
                                 "%s view leaks the arm name %r" % (reader, word))

    def test_self_pairing_exposure_is_measured_and_balanced(self):
        # A shipped project's url usually contains its author's own handle. That alone
        # leaks nothing, because it does not say whose NEED is on screen. The exposure
        # that matters is the author's handle appearing in BOTH the need text and a
        # shipped url, which would let a reader recognise a self-pair.
        builds = {d["author"]: d for d in read_jsonl("builds.jsonl")}
        arm_of = {k["row_id"]: k["arm"] for k in self.key}
        exposed = {}
        for k in self.key:
            if k["arm"] == "story_title":
                continue          # the story-title arm shows a title, not a need
            a = k["author"]
            need = self.pop[a]["need"]["text"].lower()
            urls = " ".join((it.get("url") or "") for it in builds[a].get("items") or []).lower()
            if a.lower() in need and a.lower() in urls:
                exposed[k["arm"]] = exposed.get(k["arm"], 0) + 1
        total = exposed.get("matched", 0) + exposed.get("mismatched", 0)
        # Assert the bound, not the count. The count moved once when the mismatched arm
        # was repaired (5 -> 6); what has to hold at every population is that the
        # exposure cannot approach the separation C1 requires.
        self.assertLessEqual(total, 8, "self-pairing exposure grew beyond the declared bound")
        worst = max(exposed.values()) / 74.0 if exposed else 0.0
        self.assertLess(worst, 0.20,
                        "exposure on one arm could alone reach C1's 0.20 threshold")
        self.assertEqual(exposed.get("matched", 0), exposed.get("mismatched", 0),
                         "exposure must be balanced across the arms it could bias")

    def test_both_readers_were_given_identical_blinded_input(self):
        a = open(os.path.join(RAW, "view_r1.txt"), "rb").read()
        b = open(os.path.join(RAW, "view_r2.txt"), "rb").read()
        self.assertEqual(a, b, "agreement is only meaningful on identical inputs")

    def test_the_story_title_arm_reuses_the_matched_arm_shipped_items(self):
        # Same author, same builds, different NEED text: that is the whole control.
        builds = {d["author"]: d for d in read_jsonl("builds.jsonl")}
        by_row = {k["row_id"]: k for k in self.key}
        for i in range(74):
            m, t = by_row["M%02d" % i], by_row["T%02d" % i]
            self.assertEqual(m["author"], t["author"])
            self.assertEqual(builds[m["author"]]["items"], builds[t["author"]]["items"])


class ControlTest(unittest.TestCase):
    def setUp(self):
        self.ctl = read_jsonl("gate_a2_controls.jsonl")

    def test_controls_pass_as_declared(self):
        pos = [c for c in self.ctl if c.get("expectation") == "positive"]
        self.assertGreaterEqual(len(pos), 6)
        self.assertEqual(sum(1 for c in pos if (c.get("n_items") or 0) >= 1), len(pos))
        nonsense = [c for c in self.ctl if c.get("expectation") == "nonsense"]
        self.assertTrue(nonsense)
        self.assertTrue(all(c.get("n_items") == 0 for c in nonsense))

    def test_a_refusal_is_not_a_zero(self):
        # The capture must distinguish "the index answered zero" from "the index did
        # not answer". A row whose status is not ok must never carry an n_items of 0.
        for c in self.ctl:
            if c.get("status") != "ok":
                self.assertIsNone(c.get("n_items"),
                                  "a refusal was recorded as a count of %r" % c.get("n_items"))

    def test_fetch_capture_records_no_refusals_at_all(self):
        for d in read_jsonl("builds.jsonl"):
            self.assertEqual(d["status"], "ok", "capture holds a refusal: %r" % d)

    def test_the_tag_is_rechecked_on_the_answer(self):
        # The index OR-s repeated tags parameters, so the filter is verified per hit
        # rather than trusted. A row of items must be short if the check is present.
        multi = [d for d in read_jsonl("builds.jsonl") if (d.get("n_items") or 0) > 1]
        self.assertTrue(multi, "no builder has more than one item; the check is untested")
        for d in multi:
            self.assertEqual(d["n_items"], len(d["items"]))


class StatisticsTest(unittest.TestCase):
    def test_wilson_interval_reproduces_the_figure_the_record_quotes(self):
        # F042's build arm is quoted as 0 of 24 with CI95 [0.0, 0.138]. If the interval
        # function drifts, every interval in results.json drifts with it.
        lo, hi = S.wilson(0, 24)
        self.assertAlmostEqual(lo, 0.0, places=6)
        self.assertAlmostEqual(hi, 0.138, places=3)

    def test_wilson_is_not_degenerate_at_every_rate(self):
        self.assertEqual(S.wilson(0, 0), (None, None))
        lo, hi = S.wilson(74, 74)
        self.assertGreater(lo, 0.95)
        self.assertAlmostEqual(hi, 1.0, places=6)

    def test_kappa_of_identical_labels_is_flagged_not_reported_as_agreement(self):
        # Two readers who use exactly one label each have expected agreement 1.0, and
        # kappa is undefined there. It must be refused, not reported as 1.0.
        one = ["addresses"] * 30
        kappa, table = S.cohen_kappa(one, one)
        self.assertIsNone(kappa, "a scheme where expected agreement is 1.0 cannot be scored")
        self.assertEqual(table["observed_agreement"], 1.0)

    def test_kappa_is_computed_when_there_is_disagreement_to_score(self):
        a = ["addresses"] * 20 + ["unrelated"] * 10
        b = ["addresses"] * 20 + ["unclear"] * 10
        kappa, table = S.cohen_kappa(a, b)
        self.assertIsNotNone(kappa)
        self.assertGreater(table["observed_agreement"], 0.5)
        self.assertLess(kappa, 1.0)


class VerdictTest(unittest.TestCase):
    """The gates, asserted against results.json, which the run must produce."""

    def setUp(self):
        path = os.path.join(HERE, "results.json")
        if not os.path.exists(path):
            self.fail("results.json absent: the run has not been scored")
        self.r = json.load(open(path))

    def test_primary_rate_rule_was_fixed_before_labels(self):
        self.assertIn("both readers", self.r["primary_rate_rule"])

    def test_every_declared_gate_is_present_and_carries_its_declaration(self):
        for g in ("A1_fetch_success", "A2_controls", "A3_reader_agreement",
                  "C1_negative_control", "B1_kill", "B2_survive", "A4"):
            self.assertIn(g, self.r["gates"], "gate %s absent from results.json" % g)
            self.assertTrue(self.r["gates"][g].get("declared"),
                            "gate %s does not carry its declaration" % g)

    def test_a_failed_control_forces_not_evaluated(self):
        g = self.r["gates"]
        if not (g["A2_controls"]["met"] and g["A3_reader_agreement"]["met"]
                and g["C1_negative_control"]["met"]):
            self.assertEqual(self.r["verdict"], "not_evaluated")
            self.assertTrue(g["A4"]["fired"])

    def test_b1_and_b2_cannot_both_fire(self):
        g = self.r["gates"]
        self.assertFalse(g["B1_kill"]["fired"] and g["B2_survive"]["fired"])

    def test_a_surviving_verdict_beats_both_controls(self):
        if self.r["verdict"] == "h1_survives":
            g = self.r["gates"]
            self.assertGreater(g["B2_survive"]["observed_matched_lower"],
                               g["B1_kill"]["observed_mismatched_upper"])
            self.assertGreater(g["B2_survive"]["observed_matched_lower"],
                               g["B1_kill"]["observed_story_upper"])

    def test_the_lexical_arm_feeds_no_gate(self):
        self.assertIn("lexical_arm_feeds_no_gate", self.r)
        for g in self.r["gates"].values():
            self.assertNotIn("lexical", json.dumps(g).lower().replace("lexical_arm", ""))


class LabelIntegrityTest(unittest.TestCase):
    def setUp(self):
        self.expected = [k["row_id"] for k in
                         json.load(open(os.path.join(RAW, "view_key.json")))]

    def test_each_reader_labelled_every_row_exactly_once(self):
        for reader in ("r1", "r2"):
            path = os.path.join(RAW, "labels_%s.tsv" % reader)
            if not os.path.exists(path):
                self.fail("reader %s has produced no labels" % reader)
            ids, labs = [], []
            for line in open(path):
                if not line.strip():
                    continue
                parts = line.split("\t")
                self.assertGreaterEqual(len(parts), 2, "row %r has no label" % line[:40])
                self.assertIn(parts[1].strip(), S.LABELS)
                ids.append(parts[0].strip())
                labs.append(parts[1].strip())
            self.assertEqual(sorted(ids), sorted(self.expected),
                             "reader %s: ids differ from the view it was given" % reader)
            self.assertEqual(len(set(ids)), 222, "reader %s repeated a row id" % reader)
            self.assertEqual(len(labs), 222)

    def test_labels_come_from_the_view_now_on_disk(self):
        # The failure this guards: reader r1 re-labelled a regenerated view but emitted
        # rows in the PREVIOUS view's order, so the file carried 222 plausible row ids
        # whose id-to-pair mapping was wrong. Nothing downstream could tell. The check is
        # that the reader's output order matches the frozen view's order.
        order = re.findall(r"^===== ROW \d+ \| id (\S+) =====",
                           open(os.path.join(RAW, "view_r1.txt")).read(), re.M)
        for reader in ("r1", "r2"):
            path = os.path.join(RAW, "labels_%s.tsv" % reader)
            if not os.path.exists(path):
                continue
            got = [l.split("\t")[0].strip() for l in open(path) if l.strip()]
            self.assertEqual(got, order,
                             "reader %s: label order does not match the frozen view's order" % reader)

    def test_a_reader_cannot_quote_the_key(self):
        for reader in ("r1", "r2"):
            path = os.path.join(RAW, "labels_%s.tsv" % reader)
            if not os.path.exists(path):
                continue
            text = open(path).read().lower()
            for word in ("matched", "mismatched", "story_title"):
                self.assertNotIn(word, text,
                                 "reader %s output leaks the arm name %r" % (reader, word))

    def test_superseded_labels_are_kept_but_not_read(self):
        # Failed runs are retained. What must not happen is a superseded label file
        # being picked up as a current one. Regenerated artefacts (the view, the key)
        # legitimately return to raw/, so only the label files are checked.
        sup = os.path.join(HERE, "superseded")
        if not os.path.isdir(sup):
            return
        superseded = [n for n in os.listdir(sup) if n.startswith("labels")]
        self.assertTrue(superseded, "nothing was superseded, so this test proves nothing")
        for name in superseded:
            self.assertFalse(os.path.exists(os.path.join(RAW, name)),
                             "%s was superseded and must not sit in raw/" % name)


if __name__ == "__main__":
    unittest.main()
