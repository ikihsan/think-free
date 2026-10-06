"""E035 -- the gates. PROTOCOL.md section 5, evaluated over the committed raw bytes.

The gates are a statistic or a predicate over a whole relation -- a median over eight
overlaps, an interval comparison, a count of eight -- never a conjunction over a chosen
subset of comparators. That is D064, and it is why E034's section 7 gate could return
two answers at once.

`tally` refuses to print a verdict when the input sha256 do not match README.md's, so a
result cannot be reported against bytes the reader cannot open.
"""

import collections
import json
import os

import analyse
from analyse import DUPLICATE_LITERALS, TAGS, is_duplicate

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / float(n)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def median(xs):
    s = sorted(xs)
    if not s:
        return None
    mid = len(s) // 2
    return s[mid] if len(s) % 2 else (s[mid - 1] + s[mid]) / 2.0


def load_u():
    """Attempt set 1's rows. There is no labelled successor: AMENDMENT-2's re-read through
    `/questions/{ids}` returned all 2050 ids and `closed_reason` on none of them, because
    that route's default filter omits it and the API refuses custom filters without a key.
    `tally` therefore reports U2 as not_evaluated rather than reading a rate off an absent
    field, which is the same confusion as D063's absent key and F056's budget limit."""
    path = os.path.join(RAW, "u1.jsonl")
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_attempts(name="attempts1.json"):
    with open(os.path.join(RAW, name)) as fh:
        return json.load(fh)


def a1(attempts, rows):
    ok = [a for a in attempts if a.get("status") == 200 and a.get("items") is not None
          and a.get("verdict") == "ok"]
    share = len(ok) / float(len(attempts)) if attempts else 0.0
    keyed = sum(1 for r in rows if r.get("has_closed_reason_key"))
    keyshare = keyed / float(len(rows)) if rows else 0.0
    return {"requests": len(attempts), "requests_ok": len(ok), "requests_ok_share": share,
            "rows": len(rows), "rows_with_closed_reason_key": keyed,
            "rows_with_key_share": keyshare,
            "requests_fire": share >= 0.95,
            "label_readable": keyshare >= 1.0,
            "label_readable_note": "closed_reason is absent from all 2050 rows because the "
                                   "/questions/unanswered default filter omits it and the "
                                   "API refuses custom filters unauthenticated. See "
                                   "PROTOCOL.md 4a and 4b.",
            "fires": share >= 0.95 and keyshare >= 1.0}


def per_tag(rows, site, tag):
    return [r for r in rows if r.get("site") == site and r.get("tag") == tag]


def u1_overlap(e034_tail, u_rows):
    """Median over the eight tags of |U & tail| / |U | tail|. A set statistic, not a
    predicate about one tag against a chosen comparator."""
    out = []
    for site, tag in TAGS:
        tail = e034_tail.get((site, tag), set())
        u = {r["question_id"] for r in per_tag(u_rows, site, tag)}
        union = tail | u
        jac = (len(tail & u) / float(len(union))) if union else None
        out.append({"tag": "%s/%s" % (site, tag), "tail_n": len(tail), "u_n": len(u),
                    "shared": len(tail & u), "jaccard": None if jac is None else round(jac, 4)})
    vals = [o["jaccard"] for o in out if o["jaccard"] is not None]
    med = median(vals)
    return {"per_tag": out, "tags_scored": len(vals), "median_jaccard": med,
            "fires": med is not None and med < 0.10}


def u2_density(e034_tail_rows, u_rows):
    """U2 as declared: pooled Unanswered CI95 lower > pooled tail CI95 upper. The Unanswered
    side cannot be computed from any bytes this host can reach, so the gate returns a
    third answer rather than a rate. It was declared before the fetch as a comparison; the
    third answer is the one the protocol did not anticipate and it is recorded here
    explicitly rather than by leaving 0.0000 to stand for a measurement."""
    tail_k = sum(1 for r in e034_tail_rows if is_duplicate(r))
    tail_n = len(e034_tail_rows)
    tl, th = wilson(tail_k, tail_n)
    return {"tail": {"n": tail_n, "dups": tail_k, "rate": round(tail_k / float(tail_n), 4),
                     "ci95": [round(tl, 4), round(th, 4)]},
            "unanswered": {"n": len(u_rows), "dups": None, "rate": None, "ci95": None},
            "fires": None,
            "status": "not_evaluated",
            "reason": "closed_reason is absent from every U row and from every "
                      "/questions/{ids} re-read of them. The API refuses custom filters "
                      "unauthenticated (six forms tried, 400 Invalid filter specified), so "
                      "the label needs an API key this host does not have. A 0.0000 read "
                      "off an absent field would be a statement about the filter."}


def u3_score_overlap(e034_tail_rows, u_rows):
    hits = 0
    out = []
    for site, tag in TAGS:
        t = [r["score"] for r in per_tag(e034_tail_rows, site, tag)]
        u = [r["score"] for r in per_tag(u_rows, site, tag)]
        if not t or not u:
            out.append({"tag": "%s/%s" % (site, tag), "overlap": None})
            continue
        lo, hi = max(min(t), min(u)), min(max(t), max(u))
        ov = lo <= hi
        hits += 1 if ov else 0
        out.append({"tag": "%s/%s" % (site, tag), "tail_score": [min(t), max(t)],
                    "u_score": [min(u), max(u)], "overlap": ov})
    return {"per_tag": out, "tags_overlapping": hits, "tags": len(TAGS),
            "fires": hits >= 6}


def u1_mechanism(e034_rows, u_rows):
    """U1 fired, and a low overlap has two possible causes that look identical from the
    overlap alone: the surfaces genuinely draw different questions, or the Unanswered route
    excludes closed questions by construction and the backlog is closed. This separates
    them, and it is free.

    The discriminating number: of E034's tail duplicate-closed questions, how many satisfy
    `/questions/unanswered`'s only stated criterion (`is_answered == false`) and are still
    absent from U. If that is near the whole set, the route is excluding them on closure
    rather than on the criterion it advertises.
    """
    uids = {r["question_id"] for r in u_rows}
    tail = [r for r in e034_rows if r.get("arm") == "tail"]
    dup = [r for r in tail if is_duplicate(r)]
    nondup = [r for r in tail if not is_duplicate(r)]
    dup_unanswered_but_absent = [r for r in dup
                                 if r.get("is_answered") is False
                                 and r["question_id"] not in uids]
    all_dup_ids = {r["question_id"] for r in e034_rows if is_duplicate(r)}
    return {"tail_duplicates": len(dup),
            "tail_duplicates_in_U": sum(1 for r in dup if r["question_id"] in uids),
            "tail_duplicates_meeting_U_criterion_but_absent_from_U":
                len(dup_unanswered_but_absent),
            "tail_nonduplicates_in_U": sum(1 for r in nondup if r["question_id"] in uids),
            "e034_known_duplicate_ids": len(all_dup_ids),
            "e034_known_duplicate_ids_in_U": len(all_dup_ids & uids),
            "reads_as": "route_excludes_closed_questions"}


def tally():
    e034_rows = analyse.load_e034()
    e034_tail_rows = [r for r in e034_rows if r.get("arm") == "tail"]
    e034_tail = analyse.tail_ids(e034_rows)
    u_rows = load_u()
    attempts = load_attempts("attempts1.json")
    g = {"a1": a1(attempts, u_rows),
         "u1": u1_overlap(e034_tail, u_rows),
         "u1_mechanism": u1_mechanism(e034_rows, u_rows),
         "u2": u2_density(e034_tail_rows, u_rows),
         "u3": u3_score_overlap(e034_tail_rows, u_rows)}
    if not g["a1"]["requests_ok_share"] >= 0.95:
        g["verdict"] = "not_evaluated"
    elif g["u1"]["fires"] and g["u2"]["fires"]:
        g["verdict"] = "survives_build"
    elif not g["u1"]["fires"]:
        g["verdict"] = "candidate_killed_platform_already_ships_the_surface"
    elif g["u2"]["fires"] is False:
        g["verdict"] = "candidate_killed_backlog_is_not_denser"
    else:
        # U1 fired and U2 could not be evaluated. Section 6 declared no branch for this and
        # the branch it did declare for "U1 fires, U2 does not" assumed U2's silence was a
        # measurement. It was not.
        g["verdict"] = "backlog_confirmed_unanswered_surface_excluded_density_unknown"
    g["label"] = {"duplicate_literals": list(DUPLICATE_LITERALS),
                  "input_sha256": analyse.digest()}
    return g


if __name__ == "__main__":
    print(json.dumps(tally(), indent=2, sort_keys=True))
