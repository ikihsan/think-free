#!/usr/bin/env python3
"""E029 -- score the three arms and apply every gate declared in PROTOCOL.md.

Reads the committed captures and the two readers' labels; writes results.json.

Which reader's rate feeds B1 and B2 was fixed here, BEFORE any label existed, and
is the strict choice: a row counts in the primary rate only when **both** readers
say `addresses`. The `either`-reader rate is reported beside it. Choosing the
conservative arm after seeing the two disagree would be moving a threshold.

The lexical arm is computed and printed with its mismatched control and feeds no
gate, because E028 measured lexical coverage as `informative: false` and F043's
lesson is that a bare rate without its base rate is not a finding.
"""
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")
DECLARED_POPULATION = 278      # PROTOCOL.md, fixed before the fetch
LABELS = {"addresses", "unrelated", "unclear"}


def read_jsonl(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def wilson(k, n, z=1.96):
    """Wilson score interval. Returns (lo, hi) or (None, None) for an empty arm."""
    if not n:
        return None, None
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, (c - m) / d), min(1.0, (c + m) / d)


def cohen_kappa(a, b):
    """Unweighted Cohen's kappa over the shared label set. Returns (kappa, table)."""
    cats = sorted(LABELS)
    n = len(a)
    if n == 0:
        return None, {}
    obs = {x: {y: 0 for y in cats} for x in cats}
    for x, y in zip(a, b):
        obs[x][y] += 1
    agree = sum(obs[x][x] for x in cats) / float(n)
    ra = {x: sum(obs[x].values()) / float(n) for x in cats}
    ca = {y: sum(obs[x][y] for x in cats) / float(n) for y in cats}
    exp = sum(ra[x] * ca[x] for x in cats)
    kappa = None if abs(1 - exp) < 1e-12 else (agree - exp) / (1 - exp)
    return kappa, {"observed_agreement": round(agree, 6), "expected": round(exp, 6),
                   "table": obs, "n": n}


STOP = set("""a an the is are was were be been being do does did doing have has had having
i you he she it we they them his her its their my your our this that these those there here
what which who whom when where why how all any some no not but if then than so as by for
from with without into onto about over under again more most other such only own same too
very can will just should now im ive dont doesnt isnt arent id like get got would could one
two also using use used make made get thing things way ways really something anything lot
know think want need looking look time people person way good great nice better best also
thing even still much many because while although though ever never always often sometimes
""".split())


def content_words(text):
    ws = re.findall(r"[a-z][a-z0-9+#.-]{2,}", (text or "").lower())
    return {w.strip(".-") for w in ws} - STOP


def lexical_overlap(need_text, titles):
    nw = content_words(need_text)
    if not nw:
        return None
    tw = set()
    for t in titles:
        tw |= content_words(t or "")
    if not tw:
        return None
    return len(nw & tw) / float(len(nw))


def main():
    pop = {d["author"]: d for d in read_jsonl(os.path.join(RAW, "population.jsonl"))}
    builds = {d["author"]: d for d in read_jsonl(os.path.join(RAW, "builds.jsonl"))}
    key = json.load(open(os.path.join(RAW, "view_key.json")))

    labels = {}
    for reader in ("r1", "r2"):
        path = os.path.join(RAW, "labels_%s.tsv" % reader)
        if not os.path.exists(path):
            print("missing %s" % path)
            return 1
        got = {}
        for lineno, line in enumerate(open(path), 1):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.split("\t")
            rid = parts[0].strip()
            lab = parts[1].strip() if len(parts) > 1 else ""
            if lab not in LABELS:
                print("%s line %d: label %r is not one of %s" % (path, lineno, lab, sorted(LABELS)))
                return 1
            if rid in got:
                print("%s line %d: duplicate row_id %s" % (path, lineno, rid))
                return 1
            got[rid] = lab
        labels[reader] = got

    expected_ids = [k["row_id"] for k in key]
    completeness = {}
    for reader in ("r1", "r2"):
        missing = [r for r in expected_ids if r not in labels[reader]]
        extra = [r for r in labels[reader] if r not in set(expected_ids)]
        completeness[reader] = {"missing": missing, "extra": extra,
                                "n": len(labels[reader])}
        if missing or extra:
            print("reader %s: %d missing, %d extra row ids" % (reader, len(missing), len(extra)))
            return 1

    arm_of = {k["row_id"]: k["arm"] for k in key}
    author_of = {k["row_id"]: k["author"] for k in key}
    story_of = {k["row_id"]: k["story_id"] for k in key}
    arms = ["matched", "mismatched", "story_title"]
    rows_by_arm = {a: [r for r in expected_ids if arm_of[r] == a] for a in arms}

    # ---- rates per reader, per arm, on both the strict and the lenient rule ----
    rates = {}
    for a in arms:
        ids = rows_by_arm[a]
        n = len(ids)
        both = sum(1 for r in ids if labels["r1"][r] == labels["r2"][r] == "addresses")
        either = sum(1 for r in ids if "addresses" in (labels["r1"][r], labels["r2"][r]))
        rates[a] = {
            "n": n,
            "both_readers_addresses": both,
            "either_reader_addresses": either,
            "both_rate": round(both / n, 6) if n else None,
            "both_ci95": [round(v, 6) for v in wilson(both, n)],
            "either_rate": round(either / n, 6) if n else None,
            "either_ci95": [round(v, 6) for v in wilson(either, n)],
            "label_counts_r1": {lab: sum(1 for r in ids if labels["r1"][r] == lab) for lab in sorted(LABELS)},
            "label_counts_r2": {lab: sum(1 for r in ids if labels["r2"][r] == lab) for lab in sorted(LABELS)},
        }

    # ---- agreement, over every row the readers saw ----
    k_all, tab_all = cohen_kappa([labels["r1"][r] for r in expected_ids],
                                 [labels["r2"][r] for r in expected_ids])
    k_arm = {}
    for a in arms:
        ids = rows_by_arm[a]
        k_arm[a], _ = cohen_kappa([labels["r1"][r] for r in ids],
                                  [labels["r2"][r] for r in ids])

    # ---- gates ----
    ctl = read_jsonl(os.path.join(RAW, "gate_a2_controls.jsonl"))
    pos = [c for c in ctl if c.get("expectation") == "positive"]
    nonsense = [c for c in ctl if c.get("expectation") == "nonsense"]
    a2_pos = sum(1 for c in pos if (c.get("n_items") or 0) >= 1)
    a2_nonsense_ok = all((c.get("n_items") == 0) for c in nonsense) and len(nonsense) >= 1

    fetch_ok = sum(1 for a in builds if builds[a].get("status") == "ok")
    n_fetched = len(builds)
    a1_fetch = (fetch_ok / float(n_fetched)) if n_fetched else 0.0
    a1_join = (n_fetched / float(DECLARED_POPULATION))

    # The temporal split: no reader, no label. A build cannot answer a need stated
    # after it, so 167 of 241 are not askable and the reader population is the 74.
    later, earlier = len(rows_by_arm["matched"]), 0
    story_have = {d["story_id"] for d in read_jsonl(os.path.join(RAW, "stories.jsonl"))
                  if d.get("status") == "ok" and (d.get("title") or "").strip()}
    story_cover = sum(1 for r in rows_by_arm["story_title"] if story_of[r] in story_have)

    ctl_ok = (a2_pos == len(pos) and len(pos) >= 6 and a2_nonsense_ok)
    k_ok = (k_all is not None and k_all >= 0.6)

    m_rate = rates["matched"]["both_rate"]
    x_rate = rates["mismatched"]["both_rate"]
    t_rate = rates["story_title"]["both_rate"]
    m_hi = rates["matched"]["both_ci95"][1]
    x_hi = rates["mismatched"]["both_ci95"][1]
    t_hi = rates["story_title"]["both_ci95"][1]
    m_lo = rates["matched"]["both_ci95"][0]

    separation = None
    if m_rate is not None and x_rate is not None:
        separation = round(m_rate - x_rate, 6)
    c1_ok = separation is not None and separation >= 0.20

    b1_kill = (m_hi <= x_hi) or (m_hi <= t_hi)
    b2_survive = (m_lo > x_hi) and (m_lo > t_hi)

    verdict = "not_evaluated" if not (ctl_ok and k_ok and c1_ok) else (
        "h1_survives" if b2_survive else ("h1_dies" if b1_kill else "inconclusive"))

    # ---- the lexical arm: reported with its control, feeds no gate ----
    # The mismatched row shows the MATCHED author's need beside the PARTNER's items, so
    # the items are sourced from `partner` there and from `author` elsewhere. The first
    # version sourced both from `author`, which is why the two arms printed identical
    # statistics and that is how the replicate defect was found.
    lex = {}
    for a in ("matched", "mismatched"):
        vals = []
        for k in key:
            if k["arm"] != a:
                continue
            src = k.get("partner") or k["author"]
            ov = lexical_overlap(pop[k["author"]]["need"]["text"],
                                 [it.get("title") or "" for it in builds[src].get("items") or []])
            if ov is not None:
                vals.append(ov)
        lex[a] = {"n": len(vals),
                  "mean_content_word_overlap": round(sum(vals) / len(vals), 6) if vals else None,
                  "zero_overlap_rows": sum(1 for v in vals if v == 0)}

    results = {
        "experiment": "029-need-build-match",
        "declared_before_any_reader": True,
        "primary_rate_rule": "both readers say 'addresses' (fixed before labels existed)",
        "declared_population": DECLARED_POPULATION,
        "population_reached_fetch": n_fetched,
        "temporal_split": {
            "eligible_build_postdates_need": later,
            "build_predates_need_only": 241 - later,
            "note": "HN item-id ordering; verified monotone on the corpus's own 1401 "
                    "need statements, 0 of 1400 adjacent pairs regressing",
        },
        "gates": {
            "A1_fetch_success": {"declared": ">= 0.95 of attempted rows answer",
                                 "observed": round(a1_fetch, 6), "n_attempted": n_fetched,
                                 "met": a1_fetch >= 0.95},
            "A1b_declared_coverage": {"declared": DECLARED_POPULATION,
                                      "reached": n_fetched, "ratio": round(a1_join, 6),
                                      "note": "the shortfall is PROTOCOL.md's declared "
                                              "exclusions (30 multi-need, 7 too short), "
                                              "not fetch failures"},
            "A2_controls": {"declared": "6 of 6 positive accounts return >= 1 item and the "
                                        "nonsense account returns 0",
                            "positive_recovered": a2_pos, "positive_total": len(pos),
                            "nonsense_zero": a2_nonsense_ok, "met": ctl_ok},
            "A3_reader_agreement": {"declared": "Cohen kappa >= 0.6 over all rows",
                                    "kappa": round(k_all, 6) if k_all is not None else None,
                                    "per_arm": {a: (round(v, 6) if v is not None else None)
                                                for a, v in k_arm.items()},
                                    "observed_agreement": tab_all.get("observed_agreement"),
                                    "met": k_ok},
            "C1_negative_control": {"declared": "matched minus mismatched >= 0.20, else "
                                                "not_evaluated",
                                    "separation": separation, "met": c1_ok},
            "B1_kill": {"declared": "matched CI95 upper <= mismatched upper, or <= "
                                    "story-title upper", "observed_matched_upper": m_hi,
                        "observed_mismatched_upper": x_hi, "observed_story_upper": t_hi,
                        "fired": bool(b1_kill)},
            "B2_survive": {"declared": "matched CI95 lower > both control uppers",
                           "observed_matched_lower": m_lo, "fired": bool(b2_survive)},
            "A4": {"fires_when": "A2, A3 or C1 fails", "fired": verdict == "not_evaluated"},
        },
        "verdict": verdict,
        "rates": rates,
        "story_title_coverage": {"rows": len(rows_by_arm["story_title"]),
                                 "with_a_readable_title": story_cover},
        "lexical_arm_feeds_no_gate": lex,
        "labels": {"r1": labels["r1"], "r2": labels["r2"]},
    }
    with open(os.path.join(ROOT, "results.json"), "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
        f.write("\n")

    print("verdict: %s" % verdict)
    for a in arms:
        r = rates[a]
        print("  %-12s n=%3d both=%3d (%.4f, CI95 %s) either=%3d (%.4f)"
              % (a, r["n"], r["both_readers_addresses"], r["both_rate"],
                 r["both_ci95"], r["either_reader_addresses"], r["either_rate"]))
    print("  kappa all rows: %s   per arm: %s"
          % (round(k_all, 4) if k_all is not None else None,
             {a: (round(v, 4) if v is not None else None) for a, v in k_arm.items()}))
    print("  C1 separation (both-rule): %s" % separation)
    print("  lexical arm (feeds no gate): %s" % lex)
    return 0


if __name__ == "__main__":
    sys.exit(main())
