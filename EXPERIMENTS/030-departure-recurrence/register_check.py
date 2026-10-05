#!/usr/bin/env python3
"""E030 gate A5 — do the artifact candidates name real artifacts?

Reader-free known-answer control (PROTOCOL-AMENDMENT-3, section 3). Resolves a
seeded sample of 40 treatment artifact candidates against GitHub's repository
index, with 12 nonsense names as the known-absent arm.

Writes raw/a5_register_check.jsonl and prints the two rates.
"""

import json
import os
import random
import time
import urllib.parse
import urllib.request

import common as C

GH = "https://api.github.com/search/repositories"
SAMPLE = 40
NONSENSE_N = 12

# Names that cannot be a repository. Built by prefixing a consonant cluster and a
# digit pattern that GitHub would match on nothing.
NONSENSE = [
    "zzqxvpn", "qqvxplm", "zzqxvkbd", "vvxqzpp", "zzqvxmbn", "qxzvbnpp",
    "zzqxvtk", "qvzxmbpn", "zzxqvbnp", "vqzxbmnp", "zzqxvbnt", "qzvxbnmp",
]


def gh_count(name):
    url = GH + "?" + urllib.parse.urlencode(
        {"q": "%s in:name" % name, "per_page": 1})
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "e030-research",
                              "Accept": "application/vnd.github+json"})
            with urllib.request.urlopen(req, timeout=45) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
                return r.getcode(), data.get("total_count", 0), None
        except Exception as exc:  # noqa: BLE001
            err = "%s" % exc
            time.sleep(2.0 * (attempt + 1))
    return None, None, err


def main():
    os.makedirs(C.RAW, exist_ok=True)
    treat = C.read_jsonl("treatment.jsonl")
    names = sorted({r["artifact"] for r in treat})
    rng = random.Random(3005)
    sample = rng.sample(names, min(SAMPLE, len(names)))
    rows = []
    for name in sample:
        status, count, err = gh_count(name)
        rows.append({"kind": "candidate", "name": name, "status": status,
                     "total_count": count, "error": err})
        C.log("a5_candidate", name=name, status=status, total_count=count)
        time.sleep(0.4)
    for name in NONSENSE[:NONSENSE_N]:
        status, count, err = gh_count(name)
        rows.append({"kind": "nonsense", "name": name, "status": status,
                     "total_count": count, "error": err})
        C.log("a5_nonsense", name=name, status=status, total_count=count)
        time.sleep(0.4)

    C.write_jsonl("a5_register_check.jsonl", rows)

    cand = [r for r in rows if r["kind"] == "candidate" and r["status"] == 200]
    nse = [r for r in rows if r["kind"] == "nonsense" and r["status"] == 200]
    k_c = sum(1 for r in cand if (r["total_count"] or 0) > 0)
    k_n = sum(1 for r in nse if (r["total_count"] or 0) > 0)
    n_c, n_n = len(cand), len(nse)
    lo_c, hi_c = C.wilson(k_c, n_c)
    lo_n, hi_n = C.wilson(k_n, n_n)
    d, dlo, dhi = C.diff_ci(k_c, n_c, k_n, n_n)
    C.log("a5_result", resolved=k_c, n_candidates=n_c, rate_c=round(k_c / n_c, 4) if n_c else None,
          ci_c=[round(lo_c, 4), round(hi_c, 4)],
          nonsense_hit=k_n, n_nonsense=n_n,
          diff=round(d, 4), diff_ci=[round(dlo, 4), round(dhi, 4)],
          gate_passes=bool(n_c and n_n and lo_c > hi_n))


if __name__ == "__main__":
    main()
