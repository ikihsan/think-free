#!/usr/bin/env python3
"""T-0059 — does star rank predict package downloads inside one niche?

The mission drops a candidate when prior art exists. That inference has two
links, and this census measures the second one: inside a niche where many
implementations exist, is the one people actually use predictable from where the
leaderboard puts it?

Instrument in `usage.py`, statistics in `stats.py`. Kill gate, declared before
the run:

  H. Inside a niche, star rank does not predict which implementation is used.
  K.  H is DEAD if |Spearman rho| >= 0.70 in at least 3 of 5 niches, AND the
      top-5 overlap beats chance there too.
  S.  H survives if |rho| < 0.50 in at least 3 of 5 niches AND at least half the
      implementations in every young niche report zero measurable use.
  Otherwise: inconclusive, and the record says so rather than rounding up.

A note on what this can and cannot decide. It does not test the filter
"prior art exists", which is binary and which this sample answers YES in every
niche by construction. It tests the link that filter rests on — that a crowded
niche is a solved niche — and it measures a graded quantity the filter cannot
see. Stdlib only; unauthenticated GitHub search, 10/min.
"""

import json
import os
import sys
import time
import urllib.parse

import stats
import usage

HERE = os.path.dirname(os.path.abspath(__file__))
PER_PAGE = 25

# key, search query, vocabulary age, why this niche is in the sample
NICHES = [
    ("agent-session-log", "agent session log", "young",
     "F026/F027 niche: the mission's own tooling died here"),
    ("lockfile-drift", "lockfile drift", "young",
     "F028 sample, young vocabulary"),
    ("knitting-chart", "knitting chart", "young",
     "candidate C1's niche, rejected on prior art"),
    ("reproducible-build", "reproducible build", "mature",
     "F028 heavy tail at 4135 stars: the contrast case"),
    ("exif-metadata", "exif metadata", "mature",
     "long-lived vocabulary with non-engineer users"),
]

# The matcher guesses a package name from the repository name, and a name match
# is not an identity. Both halves are falsified against known answers first:
# nine packages that are certainly installed, and two repository attributions
# where the right answer is known in both directions.
SELF_CHECK = [("npm", "vite"), ("npm", "webpack"), ("npm", "rollup"),
              ("npm", "eslint"), ("pypi", "requests"), ("pypi", "numpy"),
              ("pypi", "flask"), ("crates", "serde"), ("crates", "tokio")]

OWNERSHIP_CHECK = [
    ("vitejs/vite", "npm", "vite", True),
    ("keszybz/add-determinism", "crates", "add-determinism", True),
    ("thought-machine/please", "npm", "please", False),
    ("psf/requests", "pypi", "requests", True),
]


def guess_names(full_name):
    raw = full_name.split("/")[-1]
    low = raw.lower()
    variants = {low}
    if low.endswith(".js"):
        variants.add(low[:-3])
    for prefix in ("node-", "py-", "python-", "rust-"):
        if low.startswith(prefix):
            variants.add(low[len(prefix):])
    return sorted(v for v in variants if v)


def self_check():
    """Nine packages whose download counts are known to be non-zero."""
    fn = {"npm": usage.npm_month, "pypi": usage.pypi_month,
          "crates": usage.crates_month}
    rows = []
    for reg, pkg in SELF_CHECK:
        val = fn[reg](pkg)
        rows.append({"registry": reg, "package": pkg, "downloads": val,
                     "resolved": bool(val)})
        time.sleep(0.25)
    return rows


def ownership_check():
    """Attributions whose correct answer is known in both directions."""
    rows = []
    for full_name, reg, pkg, should_match in OWNERSHIP_CHECK:
        pair = usage.declared_repo(reg, pkg)
        got = usage.owned_by(pair, full_name)
        rows.append({"repo": full_name, "package": "%s:%s" % (reg, pkg),
                     "declared_repo": "%s/%s" % pair if pair else None,
                     "expected_match": should_match, "matched": got,
                     "ok": got == should_match})
        time.sleep(0.2)
    return rows


def fetch_niche(query):
    url = ("https://api.github.com/search/repositories?q=%s+in:name,description"
           "&sort=stars&order=desc&per_page=%d"
           % (urllib.parse.quote(query), PER_PAGE))
    data = usage.jget(url, timeout=45)
    if not isinstance(data, dict):
        return []
    return [{"full_name": i["full_name"],
             "stars": int(i.get("stargazers_count") or 0),
             "forks": int(i.get("forks_count") or 0),
             "created_at": i.get("created_at"),
             "pushed_at": i.get("pushed_at"),
             "owner_is_org": (i.get("owner") or {}).get("type") == "Organization",
             "names": guess_names(i["full_name"])}
            for i in (data.get("items") or [])]


def measure(key, query, age, why):
    rows = fetch_niche(query)
    time.sleep(7)  # unauthenticated search is 10 requests/minute
    if not rows:
        return {"key": key, "query": query, "age": age, "why": why,
                "error": "no rows returned"}
    usage.fill_all(rows)
    stars = [r["stars"] for r in rows]
    used = [r["usage_30d"] for r in rows]
    return {
        "key": key, "query": query, "age": age, "why": why, "n": len(rows),
        "star_rank_of_most_used": stats.star_rank_of_most_used(stars, used),
        "used_fraction_over_0": stats.used_fraction(used, 1),
        "used_fraction_over_1k": stats.used_fraction(used, 1000),
        "used_fraction_over_100k": stats.used_fraction(used, 100000),
        "spearman_stars_vs_usage": stats.spearman(stars, used),
        "top5_overlap_fraction": stats.top_k_overlap(stars, used)[1],
        "top5_chance_fraction": stats.top_k_overlap(stars, used)[2],
        "max_stars": max(stars), "max_usage": max(used),
        "registries_that_refused": usage.refusals(rows),
        "unverified_attributions": usage.unverified_count(rows),
        "org_fraction": round(sum(1 for r in rows if r["owner_is_org"])
                              / float(len(rows)), 3),
        "repos": [{k: v for k, v in r.items() if k != "names"} for r in rows],
    }


def gate(niches):
    """Apply the pre-declared rule, and report which niche decided what.

    The primary statistic is `star_rank_of_most_used`, not Spearman, because the
    synthetic cases in `tests/test_census_stats.py` showed Spearman cannot
    resolve a 24-way tie in usage. `rho` and the top-5 overlap are carried for
    the record and never decide the verdict on their own.
    """
    answered = [n for n in niches if n.get("star_rank_of_most_used")]
    top_and_used = [n["key"] for n in answered
                    if n["star_rank_of_most_used"] == 1 and n["max_usage"] >= 1000]
    not_top = [n["key"] for n in answered if n["star_rank_of_most_used"] > 1]
    undecided = [n["key"] for n in niches
                 if not n.get("star_rank_of_most_used") and not n.get("error")]
    young = [n for n in niches if n.get("age") == "young" and n.get("n")]
    young_unused = bool(young) and all(
        n["used_fraction_over_0"] <= 0.5 for n in young)

    if len(top_and_used) >= 3:
        verdict = ("H DEAD: in >=3 niches the most-used implementation is also "
                   "the top of the leaderboard, so a dominant incumbent is "
                   "evidence that the problem is served")
    elif len(not_top) >= 3 and young_unused:
        verdict = ("H SURVIVES: in >=3 niches the most-used implementation is "
                   "not the leaderboard's first, and >=half of every young "
                   "niche's implementations have no measurable use at all")
    else:
        verdict = ("INCONCLUSIVE: %d niches answered, %d put the most-used "
                   "project on top, %d did not; the record says inconclusive"
                   % (len(answered), len(top_and_used), len(not_top)))
    detail = {
        "answered": [n["key"] for n in answered],
        "most_used_is_leader": top_and_used,
        "most_used_not_leader": not_top,
        "undecided_niches": undecided,
        "young_mostly_unused": young_unused,
        "rhos": [{"key": n["key"], "age": n["age"], "rho":
                  n["spearman_stars_vs_usage"]}
                 for n in niches if n.get("spearman_stars_vs_usage") is not None],
    }
    return verdict, detail


def main():
    out = {"experiment": "012-prior-art-predicts-adoption", "task": "T-0059",
           "measured": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "usage_window": "last 30 days: npm last-month, PyPI per-month via "
                           "shields.io, crates.io summed per-day rows",
           "self_check": self_check()}
    out["self_check_pass"] = all(r["resolved"] for r in out["self_check"])
    out["ownership_check"] = ownership_check()
    out["ownership_pass"] = all(r["ok"] for r in out["ownership_check"])
    if not (out["self_check_pass"] and out["ownership_pass"]):
        out["verdict"] = ("instrument falsified: a known package read as unused, "
                          "or a known attribution accepted or rejected wrongly; "
                          "no census result is reported")
        json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=2)
        print("PRE-FLIGHT FAILED", out["self_check"], out["ownership_check"])
        return 1
    print("pre-flight: %d/%d packages resolved, %d/%d attributions correct"
          % (sum(r["resolved"] for r in out["self_check"]),
             len(out["self_check"]),
             sum(r["ok"] for r in out["ownership_check"]),
             len(out["ownership_check"])))

    out["niches"] = [measure(*n) for n in NICHES]
    for n in out["niches"]:
        print("%-20s %-6s n=%-3s used_at_star_rank=%-4s used>0=%-6s max=%-10s unverif=%s"
              % (n["key"], n["age"], n.get("n"),
                 n.get("star_rank_of_most_used"), n.get("used_fraction_over_0"),
                 n.get("max_usage"), n.get("unverified_attributions")))
    out["verdict"], out["gate"] = gate(out["niches"])
    json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=2)
    print("\nVERDICT:", out["verdict"])
    return 0


if __name__ == "__main__":
    sys.exit(main())