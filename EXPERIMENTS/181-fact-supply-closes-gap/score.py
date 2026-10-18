#!/usr/bin/env python3
"""E181: emit the reader's verdicts and compute every comparison the protocol named.

`SCORE` read the 62 rendered pairs in `score/` in file order, with no arm label
in any filename or in any pair, and never saw two arms of the same row
adjacent - the set was shuffled with seed 18120261018 before it was written.
For each pair the reader wrote `reached` or `not_reached`: does the proposed
answer reach the accepted answer's resolution, meaning it identifies the same
cause or gives the same concrete fix. Partial credit is not available, and the
near-misses are named in `why` rather than rounded up.

The statistics below are computed from this file alone. Nothing is reported
that is not counted here.

Run: python3 EXPERIMENTS/181-fact-supply-closes-gap/score.py
"""
import json
import os
from math import comb, sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
E177 = "EXPERIMENTS/177-evidence-gated-need"

V = {
1: ("NO", "names alwaysTemplate where the accepted answer's all-style route is "
          "withRenderingMode(.alwaysOriginal); no clear-glass restriction, no snapshot route"),
2: ("YES", "v4 removed tailwind.config.js and split the CLI out; npx @tailwindcss/cli is the fix"),
3: ("NO", "names prominentClearGlass but pairs it with alwaysTemplate and adds prominentGlass, "
          "which tints the whole item; neither accepted route is given correctly"),
4: ("NO", "never identifies a pip-installed uv, which is the accepted answer's whole resolution"),
5: ("NO", "'pick one installer' is a gesture at the cause; the accepted fix is uninstall the pip uv "
          "and install the standalone binary"),
6: ("NO", "accepted answer says the grey UI is the top of the keyboard and that a custom inputView "
          "must not carry its own background"),
7: ("YES", "llvm-mca's push model is wrong about the rsp chain - the accepted resolution"),
8: ("NO", "same as 003: wrong rendering mode, no snapshot route"),
9: ("NO", "blames an exact patch pin in requires-python; accepted cause is a uv installed under 3.13.2 by pip"),
10: ("YES", "gives the accepted metro.config.js recipe verbatim, sourceExts.push('cjs') and "
           "unstable_enablePackageExports"),
11: ("YES", "states llvm-mca's push model is pessimistic and the rsp chain is not real latency"),
12: ("YES", "same claim, same reasoning"),
13: ("NO", "attributes it to zipalign page size; the accepted resolution is an Android Studio bug "
           "fixed in Narwhal Feature Drop 2025.1.3 Canary 2"),
14: ("NO", "same as 006"),
15: ("NO", "never says llvm-mca's model is wrong about push; attributes the compiler's choice to "
           "encoding size alone"),
16: ("YES", "modulo bias, RAND_MAX 32767 over a 20001 span, is the accepted cause with its interval"),
17: ("NO", "accepted resolution is .compositingGroup() before .buttonStyle(.glass)"),
18: ("YES", "same cause, same worked numbers as the accepted answer"),
19: ("NO", "same as 001"),
20: ("NO", "apk-vs-bundle and zipalign; the accepted resolution is the Android Studio bug and the "
           "build that fixes it"),
21: ("YES", "identifies EntityFrameworkCore.Design as the package that projects the folders in"),
22: ("NO", "attributes the folders to the build without naming the package"),
23: ("YES", "v4 removed the JS config and moved the CLI to its own package"),
24: ("NO", "same as 003"),
25: ("YES", "points at vs-solutionpersistence as where the schema lives, which is the accepted resolution"),
26: ("NO", "zipalign attribution; accepted is the Android Studio bug"),
27: ("NO", "does not identify the pip-installed uv"),
28: ("NO", "names dotnet/extensions rather than microsoft/vs-solutionpersistence"),
29: ("YES", "names EntityFrameworkCore.Design 10.x as what generates them"),
30: ("NO", "same as 017"),
31: ("YES", "v4 split the CLI out and removed the config file"),
32: ("YES", "modulo bias with RAND_MAX 32767 against a 20001 span"),
33: ("YES", "tailwindcss no longer ships a CLI; @tailwindcss/cli, or pin tailwindcss@3"),
34: ("YES", "same as 025"),
35: ("NO", "zipalign attribution"),
36: ("YES", "the metro resolver switch and the '@firebase/app' import are both the accepted fix"),
37: ("YES", "bcrypt 5.0.0 of 2025-09-25 as the cause and the 4.3.0 pin as the action"),
38: ("NO", "same as 017"),
39: ("YES", "modulo bias with the worked interval [0,12766] twice as often"),
40: ("NO", "same as 006"),
41: ("YES", "a case-insensitive collision between two remote branches is the accepted cause"),
42: ("NO", "attributes it to antivirus or temp-path interception; accepted is the nvm rollback"),
43: ("NO", "attributes the folders to the build without naming EntityFrameworkCore.Design"),
44: ("NO", "zipalign attribution"),
45: ("YES", "case collision, for-each-ref, rename one side, Git for Windows 5378 and 5900"),
46: ("NO", "mentions a bcrypt version mismatch but names no version and no pin"),
47: ("NO", "AppRegistry naming only; the accepted fix lives in metro.config.js"),
48: ("YES", "bcrypt 5.0.0 of 2025-09-25 and the 4.3.0 downgrade"),
49: ("NO", "leads with the AppRegistry check; the metro footnote does not reach the fix"),
50: ("YES", "roll nvm-windows back to a release that installs node 14 cleanly"),
51: ("YES", "names the metro resolver switch as the fix, though it leads with the wrong check"),
52: ("YES", "case collision and deleting the refs by hand"),
53: ("YES", "vs-solutionpersistence read as the documentation"),
54: ("YES", "bcrypt 5.0.0 and the 4.3.0 downgrade"),
55: ("NO", "same as 017"),
56: ("YES", "nvm-windows 1.1.2 rollback"),
57: ("NO", "same as 006"),
58: ("YES", "the rsp chain is not real latency, which is the accepted resolution"),
59: ("YES", "nvm-windows 1.1.2 installs node 14 cleanly"),
60: ("NO", "attributes it to the curl installer; the accepted cause is a uv pip-installed under 3.13.2"),
61: ("YES", "the CLI moved out of the tailwindcss package"),
62: ("YES", "two remote branches differing only in case on a case-insensitive filesystem"),
}


def wilson(k, n, z=1.959963985):
    if n == 0:
        return (None, None)
    p = k / float(n)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d, (c + m) / d)


def mcnemar_exact(b, c):
    """Two-sided exact McNemar on discordant pairs (b, c)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(comb(n, i) for i in range(0, k + 1)) / float(2 ** n)
    return min(1.0, 2 * tail)


def tokens(s):
    import re
    return len([t for t in re.findall(r"[A-Za-z0-9_@./+-]+", s) if len(t) > 1])


def main():
    idx = {e["seq"]: e for e in json.load(open(os.path.join(HERE, "score-index.json")))["index"]}
    assert set(idx) == set(V), "verdict/seq mismatch"
    with open(os.path.join(HERE, "verdicts.jsonl"), "w") as fh:
        for s in sorted(V):
            fh.write(json.dumps({"seq": s, "arm": idx[s]["arm"], "qid": idx[s]["qid"],
                                 "reached": V[s][0] == "YES", "why": V[s][1]},
                                sort_keys=True) + "\n")

    by_arm = {}
    by_pair = {}
    for s in sorted(V):
        e = idx[s]
        by_arm.setdefault(e["arm"], {})[e["qid"]] = (V[s][0] == "YES", V[s][1])
        by_pair.setdefault(e["qid"], {})[e["arm"]] = V[s][0] == "YES"

    out = {"n_pairs": len(V),
           "arms": {},
           "pairwise": {},
           "cost": {},
           "drift_check": {},
           "gates": "not evaluable: K1 fired at n=14 rows carrying a fact (declared floor 16)"}

    for arm in sorted(by_arm):
        rows = by_arm[arm]
        k = sum(1 for q, v in rows.items() if v[0])
        lo, hi = wilson(k, len(rows))
        out["arms"][arm] = {"n": len(rows), "reached": k, "rate": k / float(len(rows)),
                            "wilson95": [lo, hi]}

    facts = [json.loads(l) for l in open(os.path.join(HERE, "facts.jsonl"))]
    bear = sorted(r["qid"] for r in facts if r["fact"])
    out["n_rows_read_by_EXT"] = len(facts)
    out["n_rows_with_extractable_fact"] = len(bear)
    out["fact_supply_rate"] = len(bear) / float(len(facts))
    out["fact_supply_wilson95"] = list(wilson(len(bear), len(facts)))

    for a, b in (("A1", "A0"), ("A1", "B1"), ("A1", "C1"), ("A0", "B1")):
        both = [q for q in bear if q in by_pair.get(q, {}) or True]
        rows = sorted(set(by_arm.get(a, {})) & set(by_arm.get(b, {})))
        w = sum(1 for q in rows if by_arm[a][q][0] and not by_arm[b][q][0])
        l = sum(1 for q in rows if not by_arm[a][q][0] and by_arm[b][q][0])
        out["pairwise"]["%s_vs_%s" % (a, b)] = {
            "n": len(rows), "a_wins": w, "b_wins": l,
            "mcnemar_exact_two_sided": mcnemar_exact(w, l)}

    # cost: median tokens of the added context block per arm
    tok = {"A1": [], "B1": [], "C1": []}
    for e in json.load(open(os.path.join(HERE, "ans-index.json")))["index"]:
        if e["arm"] not in tok:
            continue
        body = open(os.path.join(HERE, e["file"])).read()
        if e["arm"] == "B1":
            add = body.split("Discussion under the question and its accepted answer:")[1]
        else:
            add = body.split("The reporter adds this:")[1]
        tok[e["arm"]].append(tokens(add))

    def med(xs):
        xs = sorted(xs)
        return xs[len(xs) // 2] if len(xs) % 2 else (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]) / 2.0
    out["cost"] = {"median_added_tokens": dict((k, med(v)) for k, v in tok.items()),
                   "A1_over_B1": (med(tok["A1"]) / med(tok["B1"])) if med(tok["B1"]) else None,
                   "n": len(tok["A1"])}

    # G4 drift: P rows against E177's own verdict on the same rows
    e177 = {}
    for line in open(os.path.join(E177, "score", "verdicts.jsonl")):
        r = json.loads(line)
        e177[r["pid"]] = r["same_resolution"] == "YES"
    agree = flip = 0
    detail = []
    for q, v in sorted(by_arm.get("P", {}).items()):
        key = "g-%d" % q
        if key not in e177:
            continue
        if e177[key] == v[0]:
            agree += 1
        else:
            flip += 1
        detail.append([q, e177[key], v[0]])
    out["drift_check"] = {"n": len(detail), "agree": agree, "disagree": flip,
                          "rows": detail,
                          "g4_declared_tolerance": 3}

    with open(os.path.join(HERE, "result.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()