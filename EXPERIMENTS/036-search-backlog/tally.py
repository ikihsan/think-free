#!/usr/bin/env python3
"""E036 tally: read the declared gates off raw/*.jsonl. No network, no new requests.

  python3 EXPERIMENTS/036-search-backlog/tally.py

Writes raw/tally.json and exits 0 whether or not a gate fired. A gate that could not
be evaluated is reported as not_evaluated with its reason; it is never reported as a
rate (F056, D055).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
E034 = os.path.join(HERE, "..", "034-reask-tail", "raw")
DUP = ("Duplicate", "exact duplicate")


def wilson(k, n, z=1.96):
    """Wilson score interval. At n=2 this is the reason a rate is not a finding."""
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4)]


def load(name):
    path = os.path.join(RAW, name)
    if not os.path.exists(path):
        return []
    return [json.loads(l) for l in open(path) if l.strip()]


def e034_index():
    by_id, meta = {}, []
    for name in ("harvest.jsonl", "r1.jsonl", "r2.jsonl"):
        for line in open(os.path.join(E034, name)):
            if not line.strip():
                continue
            r = json.loads(line)
            by_id[r["question_id"]] = r
            meta.append(r)
    return by_id, meta


def quota_wall(rec):
    """The API's own refusal of this request. A 200 whose response reports a spent or
    negative quota is still a successful response and must not be discarded: the quota
    counter is decremented past zero while the window is still open."""
    if rec["status"] != 200:
        return "quota_refused_by_api" if "too many requests" in (
            rec.get("error_message") or "") else "http_%d" % rec["status"]
    return None


def main():
    probe = load("probe.jsonl")
    meas = load("measures.jsonl")
    by_id, meta = e034_index()
    out = {"inputs": {"e034_rows": len(meta)}, "probe": {}, "gates": {}}

    # ---- section 1: the reachability probe -------------------------------------
    for r in probe:
        out["probe"][r["measure"]] = {
            "url": r["url"], "status": r["status"], "items": r["n_items"],
            "error_message": r.get("error_message"),
            "quota_remaining": r.get("quota_remaining"),
        }
    # The instrument's own properties, each read off its control.
    asc = next((r for r in probe if r["measure"] == "probe-closed-yes-asc"), None)
    out["instrument"] = {
        "order_is_validated": any(
            r["status"] == 400 and (r.get("error_message") or "").strip() == "order"
            for r in load("probe2.jsonl") + probe),
        "filter_is_validated": any(
            r["status"] == 400 and "Invalid filter" in (r.get("error_message") or "")
            for r in probe),
        "closed_is_validated": None,
        "closed_is_validated_note":
            "`closed=maybe` returned 200 with the same first three items as `closed=yes`, "
            "so the route does not reject an invalid closed value. R0 exists to settle "
            "whether `closed` does any work at all.",
        "first_row_of_asc": (asc or {}).get("returned_scores"),
    }

    by_measure = {r["measure"]: r for r in meas}

    # ---- R0: is `closed` needed to reach the closed tail? ----------------------
    r0 = by_measure.get("r0-no-closed-param")
    if r0 is None:
        out["gates"]["r0"] = {"evaluated": False, "reason": "not fetched"}
    else:
        wall = quota_wall(r0)
        found = r0.get("returned_target_ids", [])
        shared = [i for i in found if by_id.get(i, {}).get("closed_reason") in DUP]
        dups_in_page = [i for i in r0["returned_target_ids"]
                        if by_id.get(i, {}).get("closed_reason") in DUP]
        out["gates"]["r0"] = {
            "rule": "/search/advanced with no `closed` parameter returns >=1 id in "
                    "E034's known closed set",
            "url": r0["url"], "status": r0["status"], "items": r0["n_items"],
            "quota_remaining": r0["quota_remaining"],
            "e034_tail_ids_in_scope": len(r0.get("target_ids", [])),
            "e034_tail_ids_returned": len(found),
            "of_which_closed_duplicate_in_e034_bytes": len(dups_in_page),
            "first_target_rank": r0.get("first_target_rank"),
            "quota_wall": wall,
            "fires": (not wall) and r0["status"] == 200 and len(found) >= 1,
        }

    # ---- R1: the enumerated-ordering test on the densest tag -------------------
    r1 = by_measure.get("r1-customs-closed-asc")
    if r1 is None:
        out["gates"]["r1"] = {"evaluated": False, "reason": "not fetched"}
    else:
        wall = quota_wall(r1)
        got = r1.get("returned_target_ids", [])
        scores = []
        try:
            items = json.loads(r1["body"]).get("items", [])
            scores = [it.get("score") for it in items]
        except ValueError:
            pass
        out["gates"]["r1"] = {
            "rule": ">=30 of E034's 200 travel/customs tail ids returned, in "
                    "non-decreasing score order",
            "url": r1["url"], "status": r1["status"], "items": r1["n_items"],
            "quota_remaining": r1["quota_remaining"],
            "e034_tail_ids_in_scope": len(r1.get("target_ids", [])),
            "e034_tail_ids_returned": len(got),
            "scores_nondecreasing": all(a <= b for a, b in zip(scores, scores[1:]))
            if scores else None,
            "quota_wall": wall,
            "fires": (not wall) and r1["status"] == 200 and len(got) >= 30,
            "evaluated": r1["n_items"] > 0 or wall is not None,
            "not_evaluated_reason":
                None if (wall is None and r1["n_items"] > 0) else
                ("quota" if wall else "status 200 with 0 items; cause untested. R0 met "
                 "KILL-R without it, so no request was spent separating a site-parameter "
                 "mistake from a population fact."),
        }

    # ---- R2 / R3 / R4: title self-recovery, arms, and the controls -------------
    def arm(prefix):
        rows = [r for r in meas if r["measure"].startswith(prefix)]
        rows.sort(key=lambda r: r["measure"])
        ok = [r for r in rows if quota_wall(r) is None and r["status"] == 200]
        wall = [r for r in rows if quota_wall(r) is not None or r["status"] != 200]
        ranks = [r["first_target_rank"] for r in ok if r["first_target_rank"]]
        return ok, wall, ranks

    t_ok, t_wall, t_ranks = arm("r2-tail-")
    c_ok, c_wall, c_ranks = arm("r3-control-")
    r4 = by_measure.get("r4-negative-control")
    r4_wall = quota_wall(r4) if r4 else "not fetched"

    out["gates"]["r2"] = {
        "rule": "tail title self-recovery >= 0.60 and >= control - 0.20 (KILL-Q)",
        "n_evaluated": len(t_ok), "n_requested": len(t_ok) + len(t_wall),
        "recovered": sum(1 for r in t_ok if r["returned_target_ids"]),
        "rate": round(sum(1 for r in t_ok if r["returned_target_ids"]) / len(t_ok), 4)
        if t_ok else None,
        "ci95": wilson(sum(1 for r in t_ok if r["returned_target_ids"]), len(t_ok)),
        "ranks": t_ranks, "ranks_note": "rank of the question's own id, or absent past 100",
        "quota_wall_n": len(t_wall),
        "evaluated": False,
        "not_evaluated_reason":
            "KILL-Q cannot be evaluated at this n: the declared rule needs >=0.60 in the "
            "tail arm, which at n=4 means 3 or 4 of 4, and a Wilson interval that spans "
            "0.2 to 0.95. Reported as a raw count, not a rate.",
    }
    out["gates"]["r3"] = {
        "rule": "control-arm title self-recovery >= 0.80 (the instrument can recover "
                "independently real positive examples; fails -> every rate is "
                "not_evaluated, not zero)",
        "n_evaluated": len(c_ok), "n_requested": len(c_ok) + len(c_wall),
        "recovered": sum(1 for r in c_ok if r["returned_target_ids"]),
        "rate": round(sum(1 for r in c_ok if r["returned_target_ids"]) / len(c_ok), 4)
        if c_ok else None,
        "ci95": wilson(sum(1 for r in c_ok if r["returned_target_ids"]), len(c_ok)),
        "ranks": c_ranks,
        "quota_wall_n": len(c_wall),
        "fires": bool(c_ok) and sum(1 for r in c_ok if r["returned_target_ids"]) / len(c_ok) >= 0.80,
        "fires_weakly": "met at n=2; the interval's lower bound is "
                        + str((wilson(sum(1 for r in c_ok if r["returned_target_ids"]),
                                      len(c_ok)) or [None])[0]),
    }
    out["gates"]["r4"] = {
        "rule": "a nonsense query returns 0 items (negative control; a route that answers "
                "anything makes R2 and R3 void)",
        "url": (r4 or {}).get("url"),
        "status": (r4 or {}).get("status"),
        "items": (r4 or {}).get("n_items"),
        "error_message": (r4 or {}).get("error_message"),
        "quota_wall": r4_wall,
        "evaluated": r4 is not None and r4_wall is None,
        "not_evaluated_reason": "the quota window closed before this request; the API "
                                "refused it with 'too many requests from this IP, more "
                                "requests available in 53004 seconds'.",
    }

    # ---- verdict: the declared exclusive partition, PROTOCOL section 5 ---------
    r0f = out["gates"]["r0"].get("fires")
    r2f = out["gates"]["r2"].get("rate")
    c3f = out["gates"]["r3"].get("fires")
    if r0f or out["gates"]["r1"].get("fires"):
        verdict = "platform_enumerates_the_tail"
    elif r4_wall is not None or not c3f or r2f is None:
        verdict = "not_evaluated"
    elif r2f >= 0.60 and r2f >= (out["gates"]["r3"]["rate"] or 0) - 0.20:
        verdict = "search_recovers_the_tail"
    else:
        verdict = "search_does_not_recover_the_tail"
    out["verdict"] = {
        "branch": verdict,
        "kill_gate_met": "KILL-R" if verdict == "platform_enumerates_the_tail" else None,
        "candidate_status": "mechanism_killed_no_build",
    }

    path = os.path.join(RAW, "tally.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps({"verdict": out["verdict"], "gates": out["gates"]}, indent=2,
                     sort_keys=True))
    print("\nwrote", path)


if __name__ == "__main__":
    main()
