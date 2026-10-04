#!/usr/bin/env python3
"""Falsification tests for `tools/measure_allocation.py`.

The script prices a finding about this repository's own allocation, so its own
numbers must be checkable rather than trusted. Two properties are asserted here,
each against a synthetic history built in a temporary repository, so the test
does not depend on this repository's real commit graph.

1. **The per-day counts are per day, not cumulative.** The first version
   initialised each day's row from the running totals, so day two inherited day
   one's counts and the printed share was nonsense while the totals looked
   plausible. The assertion below is the shape that fails on that version: the
   two days sum to the total, and each day reports only its own commits.
2. **A commit touching no recognised zone is still counted once.** Otherwise a
   repository of record-keeping commits would report a total smaller than its
   history, and the share would be computed against the wrong denominator.

Run: python3 -m unittest tests.test_allocation_measurement -v
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "tools", "measure_allocation.py")


def load_module():
    spec = importlib.util.spec_from_file_location("measure_allocation", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(cwd, *args):
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid",
        "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+0000",
        "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+0000",
    })
    subprocess.run(["git"] + list(args), cwd=cwd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)


class SyntheticHistoryTest(unittest.TestCase):
    """A hand-built history with a known shape, so the expected numbers are
    derived from the commits rather than from the script's own output."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="allocation-")
        git(cls.tmp, "init", "-q")
        # `git init -b <branch>` needs git 2.28 and this fleet has run the suite
        # on 2.25.1, so the branch name is set through a ref instead. F019's
        # shape: the fixture must build the machine it claims to, not the one
        # the author happens to have.
        git(cls.tmp, "symbolic-ref", "HEAD", "refs/heads/main")
        plan = [
            # (date, [(path, content)])
            ("2026-01-01", [("EXPERIMENTS/001-a/results.json", "{}")]),
            ("2026-01-02", [("EXPERIMENTS/001-a/results.json", '{"n":1}')]),
            ("2026-01-02", [("tools/originlib/x.py", "x = 1\n")]),
            ("2026-01-03", [("sessions/a.jsonl", "{}\n")]),
            ("2026-01-04", [("EXPERIMENTS/002-b/results.json", "{}"),
                            ("tools/originlib/y.py", "y = 2\n")]),
        ]
        for i, (date, files) in enumerate(plan):
            for path, content in files:
                full = os.path.join(cls.tmp, path)
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, "w", encoding="utf-8") as fh:
                    fh.write(content)
            git(cls.tmp, "add", "-A")
            env_date = "%sT00:00:00+0000" % date
            e = dict(os.environ)
            e.update({"GIT_AUTHOR_DATE": env_date,
                      "GIT_COMMITTER_DATE": env_date})
            subprocess.run(["git", "commit", "-q", "-m", "c%d" % i], cwd=cls.tmp,
                           check=True, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, env=e)
        cls.mod = load_module()

    @classmethod
    def tearDownClass(cls):
        subprocess.run(["rm", "-rf", cls.tmp])

    def test_counts_are_per_day_and_sum_to_the_total(self):
        cwd = os.getcwd()
        os.chdir(self.tmp)
        try:
            zones, per_day = self.mod.commits_by_zone("main", None)
        finally:
            os.chdir(cwd)

        self.assertEqual(sum(r["commits"] for r in per_day.values()), 5,
                         "per-day commit counts must sum to the history")
        # Day two has two commits; the cumulative version reported three.
        self.assertEqual(per_day["2026-01-02"]["commits"], 2)
        # The first day has one commit touching EXPERIMENTS/ and nothing else.
        self.assertEqual(per_day["2026-01-01"]["world"], 1)
        self.assertEqual(per_day["2026-01-01"]["machinery"], 0)
        # The last commit touches both zones and is counted in both.
        self.assertEqual(per_day["2026-01-04"]["world"], 1)
        self.assertEqual(per_day["2026-01-04"]["machinery"], 1)
        # Totals: commits 1, 2 and 5 touch EXPERIMENTS/; commits 3 and 5 touch
        # tools/; commit 4 touches no recognised zone. Day two holds commits 2
        # and 3, one in each of the first two zones.
        self.assertEqual(per_day["2026-01-02"]["world"], 1)
        self.assertEqual(per_day["2026-01-02"]["machinery"], 1)
        self.assertEqual(zones["world"], 3)
        self.assertEqual(zones["machinery"], 2)

    def test_unrecognised_zones_still_count_toward_the_total(self):
        cwd = os.getcwd()
        os.chdir(self.tmp)
        try:
            _, per_day = self.mod.commits_by_zone("main", None)
        finally:
            os.chdir(cwd)
        # 2026-01-03 touches only sessions/, which is in no zone, and is still
        # a commit in the history.
        self.assertEqual(per_day["2026-01-03"]["commits"], 1)
        self.assertEqual(per_day["2026-01-03"]["world"], 0)
        self.assertEqual(per_day["2026-01-03"]["machinery"], 0)


class RealRepositoryTest(unittest.TestCase):
    """The numbers quoted in `FAILURES.md` F025, re-derived rather than copied."""

    def test_quoted_split_reproduces(self):
        mod = load_module()
        cwd = os.getcwd()
        try:
            out = subprocess.run(
                [sys.executable, SCRIPT, "--ref", "origin/research/origin",
                 "--json"],
                cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        finally:
            os.chdir(cwd)
        self.assertEqual(out.returncode, 0, out.stderr.decode("utf-8", "replace"))
        data = json.loads(out.stdout.decode("utf-8"))
        per_day = data["per_day"]
        # The per-day rows must reconcile with the totals, which is the property
        # the first version of the script got wrong.
        for zone in ("world", "machinery", "prose"):
            self.assertEqual(
                sum(r[zone] for r in per_day.values()),
                data["commits_by_zone"][zone],
                "%s: per-day rows must sum to the total" % zone)
        self.assertEqual(sum(r["commits"] for r in per_day.values()),
                         data["total_commits"])
        # F025's claim: measurement of the world is a small minority of commits,
        # and it shrank on the second day. Assert the direction, not the digits,
        # so the finding survives honest further work.
        days = sorted(per_day)
        self.assertGreaterEqual(len(days), 2,
                                "expected at least two days of history")
        first = 100.0 * per_day[days[0]]["world"] / per_day[days[0]]["commits"]
        last = 100.0 * per_day[days[-1]]["world"] / per_day[days[-1]]["commits"]
        self.assertLess(last, first,
                        "F025 claims the world share fell; it rose instead")
        ratio = data["lines"]["ratio_machinery_to_experiment"]
        self.assertIsNotNone(ratio)
        self.assertGreater(ratio, 1.0,
                           "machinery should outweigh experiment code")


if __name__ == "__main__":
    unittest.main()
