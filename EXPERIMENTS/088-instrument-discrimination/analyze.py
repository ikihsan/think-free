#!/usr/bin/env python3
"""E088 analysis: evaluate the gates declared in PROTOCOL.md.

Reads only bytes that exist before this script is run:
  * EXPERIMENTS/087-environmental-monitoring/outcome.py   (the instrument)
  * EXPERIMENTS/08[1-7]-*/raw/*-results.jsonl              (G2, G3, G4)
  * EXPERIMENTS/088-instrument-discrimination/raw/probe-results.jsonl (G1)

It writes no row and depends on nothing produced by a run in progress.

Usage:
    python3 analyze.py
"""

import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
E087 = os.path.join(REPO, "EXPERIMENTS", "087-environmental-monitoring")
sys.path.insert(0, E087)

from outcome import classify_served  # noqa: E402  (the instrument)

DOMAINS = [
    ("E081", "081-lab-instrument-error-codes"),
    ("E082", "082-medical-device-alarm-codes"),
    ("E083", "083-aviation-maintenance-fault-codes"),
    ("E084", "084-industrial-equipment-fault-codes"),
    ("E085", "085-building-automation-hvac"),
    ("E086", "086-building-code-compliance"),
    ("E087", "087-environmental-monitoring"),
]
GRADIENT_ORDER = ["E081", "E082", "E083", "E084", "E085"]

# Generic web-chrome words: present on any page, say nothing about the need.
CHROME = {
    "error", "code", "codes", "fault", "alarm", "troubleshooting", "fix",
    "meaning", "what", "does", "how", "the", "for", "and", "with", "manual",
    "guide", "message", "messages",
}


def wilson(k, n, z=1.959963985):
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - h), min(1.0, c + h))


def newcombe(k1, n1, k2, n2, z=1.959963985):
    """Newcombe hybrid-score CI for p1 - p2 (no continuity correction)."""
    _, l1, u1 = wilson(k1, n1, z)
    _, l2, u2 = wilson(k2, n2, z)
    p1, p2 = k1 / n1, k2 / n2
    lower = (p1 - p2) - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    upper = (p1 - p2) + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return (p1 - p2, lower, upper)


def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def content_terms(query):
    """Query tokens that carry meaning, with the sequence counter removed."""
    toks = re.findall(r"[a-z0-9]+", query.lower())
    return [t for t in toks if t not in CHROME and not t.isdigit()]


def is_relevant(query, titles, snippets):
    """True when some retrieved text actually mentions the query's subject."""
    terms = set(content_terms(query))
    if not terms:
        return False
    blob = " ".join(titles + snippets).lower()
    return any(t in blob for t in terms)


def gate1():
    path = os.path.join(HERE, "raw", "probe-results.jsonl")
    if not os.path.exists(path):
        print("G1: NOT RUN (raw/probe-results.jsonl absent)")
        return None
    rows = load_jsonl(path)
    served = [r for r in rows if r["arm"] == "known-served"]
    unserved = [r for r in rows if r["arm"] == "known-unserved"]

    s_hit = sum(1 for r in served if classify_served(r["snippets"], r["titles"]) == "served")
    u_hit = sum(1 for r in unserved if classify_served(r["snippets"], r["titles"]) == "served")
    diff, lo, hi = newcombe(s_hit, len(served), u_hit, len(unserved))
    u_frac = u_hit / len(unserved) if unserved else 0.0

    print("G1 discrimination (instrument unchanged, labels known by construction)")
    print(f"  known-served   called served: {s_hit}/{len(served)}")
    print(f"  known-unserved called served: {u_hit}/{len(unserved)}")
    print(f"  difference {diff:+.3f}  Newcombe CI95 [{lo:+.3f}, {hi:+.3f}]")
    print(f"  known-unserved retrieval returned >=1 block on "
          f"{sum(1 for r in unserved if r['num_results'] > 0)}/{len(unserved)} probes")
    passed = u_frac <= 0.30 and lo > 0
    print(f"  G1: {'PASS' if passed else 'FAIL'}  (needs served(unserved) <= 0.30 and CI lower > 0)")
    return {"s_hit": s_hit, "n_served": len(served), "u_hit": u_hit,
            "n_unserved": len(unserved), "diff": diff, "lo": lo, "hi": hi,
            "passed": passed, "rows": rows}


def gates_2_to_4():
    all_rows = {}
    for label, d in DOMAINS:
        p = os.path.join(REPO, "EXPERIMENTS", d, "raw")
        all_rows[label] = {
            arm: load_jsonl(os.path.join(p, f"{arm}-results.jsonl"))
            for arm in ("treatment", "control")
        }

    # --- G2: is the retrieved text about the query at all? -----------------
    print("\nG2 retrieval relevance (committed E081-E087 rows, no new network)")
    tot = rel = 0
    for label, _ in DOMAINS:
        rows = all_rows[label]["treatment"]
        r = sum(1 for x in rows if is_relevant(x["query_normalized"], x["titles"], x["snippets"]))
        tot += len(rows)
        rel += r
        print(f"  {label}: {r}/{len(rows)} rows with an on-topic result")
    frac = rel / tot if tot else 0.0
    _, lo, hi = wilson(rel, tot)
    print(f"  overall {rel}/{tot} = {frac:.3f}  Wilson CI95 [{lo:.3f}, {hi:.3f}]")
    g2 = frac >= 0.60
    print(f"  G2: {'PASS' if g2 else 'FAIL'}  (needs >= 0.60)")

    # --- G3: does the dose-response gradient survive on relevant rows? -----
    print("\nG3 gradient under relevance restriction")
    print("  domain  partial%% (all rows)  partial%% (relevant rows only)")
    rates_all, rates_rel = {}, {}
    for label, _ in DOMAINS:
        rows = all_rows[label]["treatment"]
        cls = [classify_served(x["snippets"], x["titles"]) for x in rows]
        pa = cls.count("partially_served") / len(rows) if rows else 0.0
        sub = [(x, c) for x, c in zip(rows, cls) if is_relevant(x["query_normalized"], x["titles"], x["snippets"])]
        pr = (sum(1 for _, c in sub if c == "partially_served") / len(sub)) if sub else None
        rates_all[label] = pa
        rates_rel[label] = pr
        print(f"  {label}      {pa:6.3f} (n={len(rows):3d})        "
              f"{'n/a' if pr is None else f'{pr:6.3f}'} (n={len(sub):3d})")

    def monotone(rates):
        vals = [rates[k] for k in GRADIENT_ORDER]
        if any(v is None for v in vals):
            return False, "a domain has no relevant rows"
        nondec = all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1))
        if nondec:
            return True, "non-decreasing, as the synthesis states"
        rank_asc = vals == sorted(vals)
        return False, ("non-decreasing" if rank_asc else
                       "the synthesis's declared order, reversed or reshuffled")

    ok_all, why_all = monotone(rates_all)
    ok_rel, why_rel = monotone(rates_rel)
    print(f"  ordering E081<=E082<=E083<=E084<=E085, all rows: "
          f"{'holds' if ok_all else 'DOES NOT hold'} ({why_all})")
    print(f"  ordering E081<=E082<=E083<=E084<=E085, relevant rows only: "
          f"{'holds' if ok_rel else 'DOES NOT hold'} ({why_rel})")
    g3 = ok_all and ok_rel
    print(f"  G3: {'PASS' if g3 else 'FAIL'}  (needs the declared ordering on both sets)")

    # --- G4: keyword attribution ------------------------------------------
    print("\nG4 keyword attribution (reported, not gated)")
    WEAK = ["app", "tool", "method", "guide", "solution", "fix"]
    t_rows = [x for label, _ in DOMAINS for x in all_rows[label]["treatment"]]
    called = [(x, classify_served(x["snippets"], x["titles"])) for x in t_rows]
    n_served = sum(1 for _, c in called if c == "served")
    flips = 0
    for x, c in called:
        if c != "served":
            continue
        trimmed = [t for t in x["titles"] if not any(k in t.lower() for k in WEAK)]
        snippets = [s for s in x["snippets"]]
        if classify_served(snippets, trimmed) != "served":
            flips += 1
    print(f"  treatment rows called served: {n_served}/{len(t_rows)}")
    print(f"  of those, {flips} stop being 'served' when weak-keyword page titles are removed")

    return {"g2": g2, "g2_frac": frac, "g2_rel": rel, "g2_tot": tot,
            "g3": g3, "rates_all": rates_all, "rates_rel": rates_rel,
            "g4_served": n_served, "g4_total": len(t_rows), "g4_flips": flips,
            "t_rows": t_rows}


def probe_diagnostic(g1):
    """POST-HOC reporting item, added after G1's result was read. Not a gate.

    For each probe, does any retrieved page actually mention the thing asked
    about? This separates two explanations of G1's failure:
      * the classifier calls an off-topic page set 'served', or
      * retrieval returned nothing about the subject and the classifier
        nevertheless said 'served'.
    """
    if g1 is None:
        return
    print("\nPOST-HOC DIAGNOSTIC (not a gate): does retrieval mention the subject?")
    for arm in ("known-served", "known-unserved"):
        rows = [r for r in g1["rows"] if r["arm"] == arm]
        # the distinctive token of the subject: longest non-chrome query token
        mention = 0
        called_served = 0
        called_served_and_offtopic = 0
        for r in rows:
            terms = sorted(set(content_terms(r["query"])), key=len, reverse=True)[:2]
            blob = " ".join(r["titles"] + r["snippets"]).lower()
            hit = any(t in blob for t in terms)
            if hit:
                mention += 1
            c = classify_served(r["snippets"], r["titles"])
            if c == "served":
                called_served += 1
                if not hit:
                    called_served_and_offtopic += 1
        n = len(rows)
        print(f"  {arm}: subject actually mentioned in {mention}/{n} retrievals; "
              f"called served {called_served}/{n}; "
              f"called served while off-topic {called_served_and_offtopic}/{n}")
    print("  Reading: 'called served while off-topic' counts needs whose only evidence")
    print("  of being served is a page that never mentions what was asked about.")


def main():
    print("=" * 72)
    print("E088 — instrument discrimination and gradient falsification")
    print("=" * 72)
    g1 = gate1()
    rest = gates_2_to_4()
    probe_diagnostic(g1)
    print("\n" + "=" * 72)
    print("SUMMARY")
    for name, key in (("G1 discrimination", "passed"), ("G2 relevance", "g2"), ("G3 gradient", "g3")):
        if name.startswith("G1"):
            v = g1[key] if g1 else None
        else:
            v = rest[key]
        print(f"  {name}: {'PASS' if v else 'FAIL' if v is not None else 'NOT RUN'}")
    if g1 is not None and g1["passed"] and rest["g2"] and rest["g3"]:
        verdict = "the generalisation line survives and further work is reasonable"
    else:
        verdict = ("the E081-E087 generalisation line is CLOSED; "
                   "synthesis-view-count-principle.md is corrected")
    print(f"\nVERDICT: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())