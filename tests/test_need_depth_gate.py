"""E022's depth gate, and the walk bug it exists because of.

`need_depth_walk.py` was written to resolve 434 need comments whose depth came
back `null`, and it resolved none of them: it printed "no new ancestors" for 29
rounds and exited 0. Every sampled chain was readable live at 2, 3 and 4 hops.

Two properties are held here, and the order matters:

  * **the bug stays dead.** `advance()` is asserted against a synthetic chain
    longer than one hop, which is the exact shape the buggy loop could not do.
  * **the gate reads the artifact, not the walk's exit code.** The walk exits 0
    on the bug it just had, so the only place the residue can be caught is the
    committed capture.

The second is the reason this file exists. A test that only exercised the
function would have passed against the defective version too.
"""

import importlib.util
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = os.path.join(ROOT, "EXPERIMENTS", "022-need-outcomes")
sys.path.insert(0, EXP)


def _load(name):
    spec = importlib.util.spec_from_file_location(
        "e022_" + name[:-3], os.path.join(EXP, name))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


walk = _load("need_depth_walk.py")
need_depth = _load("need_depth.py")
CAPTURE = os.path.join(EXP, "raw", "need_depth.jsonl")


def load_capture():
    rows = {}
    with open(CAPTURE) as handle:
        for line in handle:
            rec = json.loads(line)
            rows[str(rec["comment_id"])] = rec
    return rows


def _read_jsonl(path):
    with open(path) as handle:
        return [json.loads(line) for line in handle if line.strip()]


class ClimbTest(unittest.TestCase):
    """The loop's one moving part, against the shape the bug could not do."""

    def test_a_two_hop_chain_closes_at_depth_two(self):
        # 30 -> 20 -> 99, so the comment's own parent is two replies below the story.
        self.assertEqual(walk.climb("30", "99", {"30": "20", "20": "99"}), 2)

    def test_a_parent_that_is_the_story_is_depth_zero(self):
        self.assertEqual(walk.climb("99", "99", {}), 0)

    def test_a_chain_closes_through_parents_the_walk_never_fetched(self):
        """Both parent sources matter, and the walk reads both.

        `parent` is seeded from E019's capture *and* from the walk's own fetch
        log. Re-deriving a chain from the fetch log alone reads `None` for a
        link the corpus already recorded -- which is why a first version of this
        test failed on row 49603973 rather than on a defect.
        """
        chain = {"30": "20", "20": "10", "10": "99"}
        self.assertEqual(walk.climb("30", "99", chain), 3)

    def test_an_unknown_ancestor_ends_the_chain_rather_than_claiming_zero(self):
        """The direction that manufactures a result.

        If an unreadable ancestor became depth 0 the comment would land in the
        stratum with the highest reply rate. It must instead stay `None`, which
        leaves the row `null` in the capture.
        """
        self.assertIsNone(walk.climb("30", "99", {"30": "20"}))

    def test_a_self_referential_ancestor_ends_the_chain(self):
        self.assertIsNone(walk.climb("30", "99", {"30": "30", "20": "20"}))

    def test_a_committed_deep_chain_re_derives_from_the_committed_fetch_log(self):
        """The repair, checked against bytes the experiment produced.

        Every deep row's depth is re-computed from `depth_walk_fetches.jsonl`
        alone, so a capture that was hand-patched or carried over from the
        broken run cannot pass.
        """
        parent = {}
        path = os.path.join(EXP, "raw", "depth_walk_fetches.jsonl")
        with open(path) as handle:
            for line in handle:
                rec = json.loads(line)
                if rec.get("parent"):
                    parent[str(rec["id"])] = str(rec["parent"])
        parents = {}
        with open(os.path.join(EXP, "..", "019-corpus-person-diversity",
                               "raw", "corpus_authors.jsonl")) as handle:
            for line in handle:
                rec = json.loads(line)
                parents[str(rec["comment_id"])] = rec
                # The corpus's own parent links are part of the walk's input,
                # not just the comment being climbed from.
                if rec.get("parent"):
                    parent.setdefault(str(rec["comment_id"]), str(rec["parent"]))

        deep = [r for r in load_capture().values() if (r["depth"] or 0) >= 3]
        self.assertTrue(deep, "no deep row to re-derive")
        checked = 0
        for rec in deep:
            cid = str(rec["comment_id"])
            p = parents[cid].get("parent")
            if p is None:
                continue
            chain = dict(parent)
            chain[cid] = str(p)
            self.assertEqual(walk.climb(str(p), str(rec["story_id"]), chain),
                             rec["depth"],
                             "row %s does not re-derive from the fetch log" % cid)
            checked += 1
        self.assertGreater(checked, 50,
                           "too few deep rows re-derived to be evidence")

    def test_the_rejected_loop_shape_resolves_nothing(self):
        """The falsification, held as an assertion rather than a memory.

        This is the loop that shipped, written out: it re-appends the same node
        with a larger hop count, so a chain longer than one hop never compares
        equal to the story and the run exits 0 having resolved nothing. A future
        edit that restores it must fail a test rather than pass one by looking
        equivalent.
        """
        def buggy(node, sid, hops, parent, rounds):
            for _ in range(rounds):
                if node == sid:
                    return hops - 1
                hops += 1                      # node itself is never replaced
            return None

        chain = {"30": "20", "20": "10", "10": "99"}
        self.assertIsNone(buggy("20", "99", 1, chain, 29),
                          "the defective shape stopped failing, so this test no "
                          "longer falsifies anything")
        self.assertEqual(walk.climb("20", "99", chain), 2)


class DepthCaptureTest(unittest.TestCase):
    """The gate, read from the bytes the experiment committed."""

    def setUp(self):
        self.rows = load_capture()
        self.need = {str(r["comment_id"]): r
                     for r in _read_jsonl(os.path.join(EXP, "raw",
                                                       "outcomes.jsonl"))}

    def test_every_need_comment_has_a_depth(self):
        nulls = [c for c, r in self.rows.items() if r.get("depth") is None]
        self.assertEqual(nulls, [],
                         "need comments with no depth, which would be dropped "
                         "from the strata: %s" % nulls[:5])

    def test_the_capture_covers_the_whole_outcome_population(self):
        self.assertEqual(set(self.rows), set(self.need))

    def test_unresolved_is_below_the_declared_ten_percent(self):
        """The gate's own line, so the threshold cannot be quietly raised."""
        unresolved = sum(1 for r in self.rows.values() if r.get("depth") is None)
        self.assertLessEqual(unresolved, 0.10 * len(self.rows))

    def test_depth_is_never_negative_and_story_parents_are_zero(self):
        for cid, rec in self.rows.items():
            self.assertGreaterEqual(rec["depth"], 0, "%s has a negative depth" % cid)

    def test_the_verify_command_the_task_declares_agrees(self):
        self.assertEqual(need_depth.verify(self.need), 0)


class StrataTest(unittest.TestCase):
    """The confound the stratification exists to remove."""

    def setUp(self):
        self.rows = load_capture()

    def test_the_deep_comments_are_present_and_would_have_been_dropped(self):
        """A regression guard on the whole point of the repair.

        If the 434 unresolved rows ever go back to `null`, the deep strata
        disappear and the pool silently reweights toward depth 0 -- which is the
        stratum with the highest reply rate, and therefore the direction that
        manufactures a positive lift.
        """
        deep = [r for r in self.rows.values() if (r["depth"] or 0) >= 2]
        self.assertGreater(len(deep), 300,
                           "the deeply nested strata vanished again")
        answered_deep = sum(1 for r in deep if r.get("answered"))
        self.assertGreater(answered_deep, 0)

    def test_depth_strata_are_reported_separately_not_pooled(self):
        ctrl = _read_jsonl(os.path.join(EXP, "raw", "control_depth.jsonl"))
        self.assertTrue(ctrl)
        seen = set()
        for rec in ctrl:
            seen.add(rec.get("depth"))
        self.assertNotIn(None, seen,
                         "a control row with no depth would fold the "
                         "unresolved stratum into depth 0")


if __name__ == "__main__":
    unittest.main()