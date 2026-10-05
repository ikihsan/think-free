#!/usr/bin/env python3
"""E030 step 3 — clause recurrence at the pair level.

AMENDMENT-7 withdrew every cluster-level figure: single-linkage chaining put 259
of 919 treatment accounts into one component through the tokens `2014`, `2022`,
`anyways`. The declared rule is about PAIRS, and this file reads it literally.

  signature  = word tokens of length >= 4, minus the story title's tokens, minus
               the departing artifact candidate's tokens, minus every token
               occurring in more than 2% of that arm
  rare       = signature tokens occurring in <= 5 accounts of the arm
  recur(a,b) = >= 2 shared rare tokens, different authors, and (declared variant
               only) different departing artifacts
  R_pair     = accounts with >= 1 recurring partner / |arm|
  mutual     = greedy clique over the same pair graph, seeded by objectID order

Writes raw/pairs_<arm>.jsonl, raw/mutual_<arm>.jsonl, raw/recurrence.json
"""

import json
import os
import re
import sys

import common as C

COMMON_FRACTION = 0.02
RARE_MAX_DF = 5
SHARED_MIN = 2
SNIPPET = 200

# AMENDMENT-4 section 5: the mechanical completed-first-person-departure test.
FIRST_PERSON = re.compile(
    r"\b(?:I|we|my|our)\b[^.!?]{0,120}?"
    r"\b(?:switched|migrated|migrating|moved|replaced|replacing|quit|left|"
    r"dropped|stopped|abandoned|ported)\b", re.I)


def signature(row):
    toks = set(C.words(row["text"]))
    for src in (row.get("story_title") or "", row.get("artifact") or ""):
        for w in re.split(r"\W+", src.lower()):
            if len(w) >= 4:
                toks.discard(w)
    return toks


def build_pairs(rows, require_distinct_artifact):
    n = len(rows)
    sigs = [signature(r) for r in rows]
    df = {}
    for s in sigs:
        for t in s:
            df[t] = df.get(t, 0) + 1
    cutoff = max(1, int(round(n * COMMON_FRACTION)))
    sigs = [s - set(t for t in s if df[t] > cutoff) for s in sigs]
    rare = set(t for t in df if df[t] <= RARE_MAX_DF)

    index = {}
    for i, s in enumerate(sigs):
        for t in s & rare:
            index.setdefault(t, []).append(i)

    shared = {}
    for t, bucket in index.items():
        if len(bucket) < 2:
            continue
        for ai in range(len(bucket)):
            for bi in range(ai + 1, len(bucket)):
                a, b = bucket[ai], bucket[bi]
                if rows[a]["author"] == rows[b]["author"]:
                    continue
                if require_distinct_artifact:
                    if not rows[a].get("artifact") or not rows[b].get("artifact"):
                        continue
                    if rows[a]["artifact"].lower() == rows[b]["artifact"].lower():
                        continue
                key = (a, b) if a < b else (b, a)
                shared.setdefault(key, []).append(t)

    pairs = [(a, b, sorted(ts)) for (a, b), ts in shared.items()
             if len(ts) >= SHARED_MIN]
    pairs.sort(key=lambda p: (rows[p[0]]["objectID"], rows[p[1]]["objectID"]))
    meta = {"n_accounts": n, "common_fraction_cutoff": cutoff,
            "rare_max_df": RARE_MAX_DF, "shared_min": SHARED_MIN,
            "distinct_signature_tokens": len(df), "rare_tokens": len(rare),
            "artifact_condition": bool(require_distinct_artifact),
            "artifact_field_defined": any(r.get("artifact") for r in rows)}
    return pairs, meta, rows


def pair_stats(rows, pairs, label, meta):
    n = len(rows)
    partners = {}
    for a, b, toks in pairs:
        partners.setdefault(a, []).append((b, toks))
        partners.setdefault(b, []).append((a, toks))
    k = len(partners)
    lo, hi = C.wilson(k, n)

    multi_art = set()
    for a, b, _ in pairs:
        ra, rb = rows[a].get("artifact"), rows[b].get("artifact")
        if ra and rb and ra.lower() != rb.lower():
            multi_art.add(a)
            multi_art.add(b)

    out = {"arm": label, "n_accounts": n, "n_pairs": len(pairs),
           "accounts_with_a_partner": k, "R_pair": k / float(n) if n else 0.0,
           "R_pair_ci95": [lo, hi],
           "accounts_in_distinct_artifact_pairs": len(multi_art),
           "R_distinct_artifact_pair": len(multi_art) / float(n) if n else 0.0}
    out.update(meta)
    C.log("pair_stats", arm=label, n=n, pairs=len(pairs),
          accounts_with_partner=k, R_pair=round(out["R_pair"], 4),
          ci=[round(lo, 4), round(hi, 4)],
          distinct_artifact_pairs=len(multi_art))
    return out, partners


def mutual_groups(rows, pairs, label):
    """Greedy cliques, seeded by objectID order. No chaining by construction."""
    adj = {}
    for a, b, toks in pairs:
        adj.setdefault(a, {})[b] = toks
        adj.setdefault(b, {})[a] = toks
    order = sorted(adj, key=lambda i: rows[i]["objectID"])
    assigned = set()
    groups = []
    for v in order:
        if v in assigned:
            continue
        members = [v]
        assigned.add(v)
        cands = set(adj[v])
        while True:
            best, best_key = None, None
            for c in sorted(cands, key=lambda i: rows[i]["objectID"]):
                ok = all(c in adj[m] for m in members)
                if not ok:
                    continue
                deg = sum(1 for d in adj[c] if d in cands or d in members)
                key = (-deg, rows[c]["objectID"])
                if best_key is None or key < best_key:
                    best, best_key = c, key
            if best is None:
                break
            members.append(best)
            assigned.add(best)
            cands &= set(adj[best])
        toks = sorted({t for m in members for t in adj[m].values()
                       for t in t})[:10]
        groups.append({
            "size": len(members),
            "shared_tokens": toks,
            "members": [{"objectID": rows[m]["objectID"], "author": rows[m]["author"],
                         "artifact": rows[m].get("artifact"),
                         "story_id": rows[m]["story_id"],
                         "snippet": rows[m]["text"][:SNIPPET].replace("\n", " ")}
                        for m in members],
        })
    groups.sort(key=lambda g: (-g["size"], g["members"][0]["objectID"]))
    dist = {}
    for g in groups:
        dist[str(g["size"])] = dist.get(str(g["size"]), 0) + 1
    accounts_ge3 = sum(g["size"] for g in groups if g["size"] >= 3)
    C.log("mutual_groups", arm=label, groups=len(groups),
          size_distribution=dist, largest=groups[0]["size"] if groups else 0,
          accounts_in_groups_ge3=accounts_ge3)
    C.write_jsonl("mutual_%s.jsonl" % label, groups)
    return {"arm": label, "n_groups": len(groups),
            "size_distribution": dist,
            "largest_group": groups[0]["size"] if groups else 0,
            "accounts_in_groups_ge3": accounts_ge3}


def run_arm(rows, label, require_distinct_artifact):
    pairs, meta, rows = build_pairs(rows, require_distinct_artifact)
    stats, partners = pair_stats(rows, pairs, label, meta)
    stats["mutual"] = mutual_groups(rows, pairs, label)
    C.write_jsonl("pairs_%s.jsonl" % label,
                  [{"a": rows[a]["objectID"], "b": rows[b]["objectID"],
                    "a_author": rows[a]["author"], "b_author": rows[b]["author"],
                    "a_artifact": rows[a].get("artifact"),
                    "b_artifact": rows[b].get("artifact"),
                    "a_story": rows[a]["story_id"], "b_story": rows[b]["story_id"],
                    "shared_tokens": toks}
                   for a, b, toks in pairs])
    return stats


def first_person_subset(rows):
    out = []
    for row in rows:
        m = FIRST_PERSON.search(row["text"])
        if m:
            new = dict(row)
            new["first_person_match"] = m.group(0)[:120]
            out.append(new)
    C.write_jsonl("first_person_treatment.jsonl", out)
    C.log("first_person_subset", matched=len(out), of=len(rows))
    return out


def main():
    os.makedirs(C.RAW, exist_ok=True)
    treat = C.read_jsonl("treatment.jsonl")
    ctrl = C.read_jsonl("control.jsonl")

    results = {}
    results["treatment_declared"] = run_arm(treat, "treatment", True)
    results["control_declared"] = run_arm(ctrl, "control", False)
    results["treatment_matched"] = run_arm(treat, "treatment_matched", False)
    results["treatment_first_person"] = run_arm(
        first_person_subset(treat), "treatment_first_person", True)

    def diff(key, a, b):
        d = C.diff_ci(results[a]["accounts_with_a_partner"], results[a]["n_accounts"],
                      results[b]["accounts_with_a_partner"], results[b]["n_accounts"])
        results["diff_%s" % key] = {"diff": d[0], "ci95": [d[1], d[2]]}
        C.log("diff_pair", variant=key, diff=round(d[0], 4),
              ci95=[round(d[1], 4), round(d[2], 4)])
        return results["diff_%s" % key]

    diff("declared", "treatment_declared", "control_declared")
    diff("matched", "treatment_matched", "control_declared")

    t = results["treatment_declared"]
    c = results["control_declared"]
    lo_t, hi_t = t["R_pair_ci95"]
    lo_c, hi_c = c["R_pair_ci95"]
    groups_ge3 = sum(v for k, v in t["mutual"]["size_distribution"].items()
                      if int(k) >= 3)
    multi_art_clusters = sum(1 for g in C.read_jsonl("mutual_treatment.jsonl")
                             if g["size"] >= 3
                             and len({(m["artifact"] or "").lower() for m in g["members"]
                                      if m["artifact"]}) >= 2)
    overlap = not (hi_t < lo_c or hi_c < lo_t)
    b1 = (t["R_pair"] - c["R_pair"] >= 0.10) and \
         (results["diff_declared"]["ci95"][0] > 0 or results["diff_declared"]["ci95"][1] < 0) and \
         multi_art_clusters >= 3
    b2 = overlap or multi_art_clusters < 2
    results["verdict"] = {
        "b1_fires": bool(b1), "b2_fires": bool(b2),
        "verdict": "H1_survives" if b1 else ("H1_dies" if b2 else "inconclusive"),
        "ci_overlap": bool(overlap),
        "multi_artifact_mutual_groups_ge3": multi_art_clusters,
        "mutual_groups_ge3": groups_ge3,
        "gate_b1_diff_threshold": 0.10,
        "gate_b1_min_groups": 3,
    }
    C.log("verdict", **results["verdict"])

    with open(os.path.join(C.RAW, "recurrence.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    sys.exit(main())
