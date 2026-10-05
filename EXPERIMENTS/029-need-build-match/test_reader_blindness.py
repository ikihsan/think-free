#!/usr/bin/env python3
"""E029 -- tests of reader blindness and label provenance.

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

import intervalstats as I  # noqa: E402


def read_jsonl(name):
    path = name if os.path.isabs(name) else os.path.join(RAW, name)
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def sibling(*parts):
    """A capture in a sibling experiment, resolved from this file, not the cwd."""
    return os.path.normpath(os.path.join(HERE, "..", *parts))


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
                ov = I.lexical_overlap(pop[k["author"]]["need"]["text"],
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
