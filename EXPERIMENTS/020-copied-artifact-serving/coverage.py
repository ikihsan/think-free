#!/usr/bin/env python3
"""C2 -- what fraction of the 61 repositories 017 already read is in the index?

This is the control that can refuse the whole experiment.  A large copy count on
a thin index is still a floor; a SMALL count on a thin index is a fact about the
index and not about the field, and reading it as a finding is the error this
repository has already made twice (F032).

The population list is read from 017's committed artifacts.  No GitHub request is
made here: the repositories are already known, and only their presence in
Sourcegraph's index is in question.

Pacing is a declared parameter, not an afterthought.  The first pass issued 61
queries as fast as curl would run them and the anti-bot challenge armed part way
through, so 33 rows -- every young and every placebo row -- came back as HTML.
Those are recorded as `refused`, never as absent, and this pass retries exactly
the refused rows with a delay.
"""

import argparse
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
RESULTS_015 = os.path.join(HERE, "..", "015-incumbent-serving", "results.json")
RESULTS_017 = os.path.join(HERE, "..", "017-incumbent-artifact-type", "results.json")

# 61 queries with no delay armed the challenge after ~28. The delay is what makes
# C2 answerable at all, so it is stated here rather than tuned silently.
DEFAULT_DELAY = 6.0


def arms():
    """The 61 rows of 017, by arm, taken from its own results.json."""
    with open(RESULTS_017) as handle:
        results = json.load(handle)
    out = {"mature": [], "young": [], "placebo": []}
    for arm, classes in results["arms"].items():
        for rows in classes.values():
            out[arm].extend(rows["repos"])
    return out


def install_totals():
    """Every install reading 015 and 017 hold, for the young arm's four channels.

    H1's ratio is against a figure this repository already measured, so it is
    read from those artifacts rather than re-fetched.  Refusals are carried with
    it: a channel that answered nothing can only lower the denominator, which is
    the direction that helps H1.
    """
    with open(RESULTS_015) as handle:
        fifteen = json.load(handle)
    rows = []
    for entry in fifteen["cluster"]:
        rates = {r["channel"].split(":", 1)[0]: r["value"] for r in entry["rate"]}
        rows.append(
            {
                "repo": entry["repo"],
                "rate": rates,
                "refused": entry.get("refused", []),
            }
        )
    total = sum(v for r in rows for v in r["rate"].values())
    return total, rows


def probe_name(repo):
    return "coverage-%s" % re.sub(r"[^A-Za-z0-9]+", "-", repo)


def repo_probe(repo):
    """Is one repository in the index at all?

    A `repo:` filter with `select:repo` answers 1 for a repository the index knows
    and 0 for one it does not.  Verified on a known repository and on an invented
    name before this file was written; both probes are in the protocol.
    """
    from copycount import fetch

    pattern = "repo:^github\\.com/%s$ select:repo count:5" % re.escape(repo)
    return fetch(pattern, name=probe_name(repo))


def load_existing():
    """Read prior passes, so a retry touches only what is still unanswered."""
    path = os.path.join(HERE, "coverage.json")
    if not os.path.exists(path):
        return {}
    with open(path) as handle:
        prior = json.load(handle)
    answered = {}
    for arm, block in prior.get("coverage", {}).items():
        for row in block.get("rows", []):
            if row.get("state") == "ok":
                answered[row["repo"]] = row
    return answered


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY)
    parser.add_argument("--rounds", type=int, default=3)
    args = parser.parse_args()

    population = arms()
    total = sum(len(v) for v in population.values())
    sys.stderr.write("population: %d rows, delay %.1fs, up to %d rounds\n"
                     % (total, args.delay, args.rounds))

    answered = load_existing()
    sys.stderr.write("carried forward from a previous pass: %d\n" % len(answered))

    for round_no in range(1, args.rounds + 1):
        pending = [
            repo for repos in population.values() for repo in repos
            if repo not in answered
        ]
        if not pending:
            break
        sys.stderr.write("round %d: %d unanswered\n" % (round_no, len(pending)))
        refused_streak = 0
        for repo in pending:
            rec = repo_probe(repo)
            sys.stderr.write("  %-46s %-9s %s\n"
                             % (repo[:46], rec["state"], rec.get("count")))
            sys.stderr.flush()
            if rec["state"] == "ok":
                answered[repo] = {
                    "repo": repo,
                    "in_index": rec.get("count") == 1,
                    "state": "ok",
                    "count": rec.get("count"),
                }
                refused_streak = 0
                time.sleep(args.delay)
                continue
            refused_streak += 1
            # Back off hard and stop early: a challenge is positional, and
            # continuing to hammer it wastes the round.
            time.sleep(args.delay * 4)
            if refused_streak >= 8:
                sys.stderr.write("  challenge still armed; ending this round\n")
                break

    out = {"population": population, "coverage": {}, "install_totals": {}}
    for arm, repos in population.items():
        rows = []
        for repo in repos:
            rows.append(answered.get(repo, {"repo": repo, "in_index": None, "state": "refused"}))
        out["coverage"][arm] = {
            "n": len(rows),
            "in_index": sum(1 for r in rows if r["in_index"] is True),
            "unanswered": sum(1 for r in rows if r["in_index"] is None),
            "rows": rows,
        }

    install_total, young_rows = install_totals()
    out["install_totals"] = {"young_monthly_total": install_total, "rows": young_rows}

    with open(os.path.join(HERE, "coverage.json"), "w") as handle:
        json.dump(out, handle, indent=1, sort_keys=True)
        handle.write("\n")

    grand = sum(b["in_index"] for b in out["coverage"].values())
    unanswered = sum(b["unanswered"] for b in out["coverage"].values())
    print("in index: %d of %d (%d still unanswered)" % (grand, total, unanswered))
    for arm, c in sorted(out["coverage"].items()):
        print("  %-8s %2d/%2d in index, %d unanswered" % (arm, c["in_index"], c["n"], c["unanswered"]))
    print("young arm monthly install total: %d" % install_total)
    return 0


if __name__ == "__main__":
    sys.exit(main())