#!/usr/bin/env python3
"""E039 statistics: every figure in results.json, from the raw captures only.

The gates are evaluated as declared in PROTOCOL.md and are evaluated by this
script rather than read off by hand, so a later reader can re-derive the verdict
from the capture without trusting the prose.
"""
import json, os, statistics, datetime
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
AGE_DAYS = 180
NOW_I = int(datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc).timestamp())

# Declared in PROTOCOL.md.
GATE_A1_RECOVERY = 0.95
GATE_A2_COVERAGE = 0.90
KILL_RATIO = 1.5
SECOND_KILL_LINK_FLOOR = 0.02
NOVELTY_HOST_SHARE = 0.01
H4_FLOOR = 0.10


def load(name):
    p = os.path.join(RAW, name)
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in open(p)]


def age_days(rec):
    if not rec.get("created_at_i"):
        return None
    return (NOW_I - rec["created_at_i"]) / 86400.0


def rate(recs):
    if not recs:
        return None
    return sum(1 for r in recs if r["has_subtree"]) / len(recs)


def main():
    corpus = os.path.join(HERE, "..", "012-candidate-harvest", "raw",
                          "hn_needs_2026-10-04.jsonl")
    needs = [json.loads(l) for l in open(corpus)]
    need_ids = {str(r["id"]) for r in needs}
    story_ids = []
    seen = set()
    for r in needs:
        if str(r["story_id"]) not in seen:
            seen.add(str(r["story_id"]))
            story_ids.append(str(r["story_id"]))

    arm_a = load("arms.jsonl")
    arm_b = load("control.jsonl")
    comments = load("comments.jsonl")
    log = load("fetch_log.jsonl")

    done_path = os.path.join(RAW, "stories.done")
    done = {l.strip() for l in open(done_path)} if os.path.exists(done_path) else set()

    out = {
        "schema": "origin.e021.results/1",
        "computed_by": "stats.py from raw/ only",
        "capture": {
            "stories_in_corpus": len(story_ids),
            "stories_in_ledger": len(done),
            "comment_rows": len(comments),
            "fetch_log_rows": len(log),
            "fetch_log_kinds": dict(Counter(e["kind"] for e in log)),
            "stories_with_truncation": sorted({e["story_id"] for e in log
                                               if e["kind"] == "truncated"}),
            "needs_recovered": len(arm_a),
            "gate_a1_recovery": len(arm_a) / float(len(needs)),
            "gate_a1_met": (len(arm_a) / float(len(needs))) >= GATE_A1_RECOVERY,
        },
    }

    # Gate A2: control coverage. The denominator is what the index says exists.
    by_story_total = Counter(r["story_id"] for r in comments)
    logged_total = {e["story_id"]: e["nbHits"] for e in log
                    if e.get("kind") == "truncated" and e.get("nbHits")}
    expected = sum(max(by_story_total[s], logged_total.get(s, 0)) for s in by_story_total)
    out["capture"]["gate_a2_control_coverage"] = len(comments) / float(expected) \
        if expected else None
    out["capture"]["gate_a2_met"] = bool(expected) and \
        (len(comments) / float(expected)) >= GATE_A2_COVERAGE

    def summ(recs, label):
        sub = [r for r in recs if r["has_subtree"]]
        return {
            "label": label,
            "comments": len(recs),
            "replied": len(sub),
            "reply_rate": rate(recs),
            "median_replies_when_replied": statistics.median([r["direct_replies"] for r in sub]) if sub else None,
            "max_subtree": max([r["subtree"] for r in recs] or [0]),
            "with_link_reply": sum(1 for r in recs if r["link_replies"] > 0),
            "with_link_reply_share": (sum(1 for r in recs if r["link_replies"] > 0) / len(recs)) if recs else None,
            "with_novel_host": sum(1 for r in recs if r["novel_hosts"]),
            "with_novel_host_share": (sum(1 for r in recs if r["novel_hosts"]) / len(recs)) if recs else None,
            "median_story_total": statistics.median([r["story_total"] for r in recs]) if recs else None,
        }

    a_old = [r for r in arm_a if (age_days(r) or 0) >= AGE_DAYS]
    b_old = [r for r in arm_b if (age_days(r) or 0) >= AGE_DAYS]

    out["arms"] = {
        "all": {"need": summ(arm_a, "need, all ages"), "control": summ(arm_b, "control, all ages")},
        "aged_%dd" % AGE_DAYS: {"need": summ(a_old, "need, >=180d"),
                                 "control": summ(b_old, "control, >=180d")},
    }
    out["arms"]["age_note"] = (
        "needs aged by the same clock as controls: created_at_i against 2026-10-05")

    # ---- the kill gate ----
    gates = {}
    for band in ("all", "aged_%dd" % AGE_DAYS):
        ra = out["arms"][band]["need"]["reply_rate"]
        rb = out["arms"][band]["control"]["reply_rate"]
        ratio = (ra / rb) if (ra is not None and rb) else None
        gates[band] = {
            "need_reply_rate": ra, "control_reply_rate": rb, "ratio": ratio,
            "kill_gate_ratio_required": KILL_RATIO,
            "kill_gate_met": bool(ratio is not None and ratio < KILL_RATIO),
            "positive_gate_met": bool(ratio is not None and ratio >= KILL_RATIO),
        }
    out["gates"] = gates

    # ---- second kill gate: link floor ----
    lshare = out["arms"]["all"]["need"]["with_link_reply_share"]
    out["gates"]["second_kill_link_floor"] = {
        "need_link_reply_share": lshare,
        "floor": SECOND_KILL_LINK_FLOOR,
        "kill_gate_met": bool(lshare is not None and lshare < SECOND_KILL_LINK_FLOOR),
    }

    # ---- H4: did the requester come back ----
    linked = [r for r in arm_a if r["link_replies"] > 0]
    returned = sum(1 for r in linked if r["asker_returned"])
    withsub = [r for r in arm_a if r["has_subtree"]]
    out["h4_asker_returned"] = {
        "needs_with_link_reply": len(linked),
        "of_which_asker_replied_again": returned,
        "share": returned / len(linked) if linked else None,
        "floor": H4_FLOOR,
        "floor_met": bool(linked and returned / len(linked) >= H4_FLOOR),
        "note": "an asker returning is not evidence the need was satisfied; "
                "the protocol declares it a floor, not a satisfaction measure",
        "all_needs_with_subtree": len(withsub),
        "all_needs_asker_replied_again": sum(1 for r in withsub if r["asker_returned"]),
    }

    # ---- per-trigger stratification, declared in the protocol ----
    trig_by_id = {}
    for r in needs:
        trig_by_id[str(r["id"])] = r["trigger"]
    per = defaultdict(lambda: {"need_n": 0, "need_replied": 0})
    for r in arm_a:
        t = trig_by_id.get(r["id"], "?")
        per[t]["need_n"] += 1
        per[t]["need_replied"] += 1 if r["has_subtree"] else 0
    out["per_trigger"] = {
        t: {"need_comments": v["need_n"], "replied": v["need_replied"],
            "reply_rate": v["need_replied"] / v["need_n"]}
        for t, v in sorted(per.items(), key=lambda kv: -kv[1]["need_n"])
        if v["need_n"] >= 20
    }

    # ---- within-story expectation, which is a sharper estimator than a global
    # rate. Each need is compared to the reply rate of the *other* comments in
    # its own story, so thread size and traffic are matched exactly rather than
    # on average. This is the comparison the protocol promised; the global ratio
    # above is reported beside it because a global ratio is what a reader will
    # check first, and the two can disagree.
    story_ctrl = defaultdict(list)
    for r in arm_b:
        story_ctrl[r["story_id"]].append(r["has_subtree"])
    within = []
    for r in arm_a:
        peers = story_ctrl.get(r["story_id"]) or []
        if len(peers) < 20:
            continue
        pr = sum(peers) / float(len(peers))
        within.append({"id": r["id"], "story_id": r["story_id"],
                       "peers": len(peers), "peer_reply_rate": pr,
                       "replied": r["has_subtree"]})
    with_peers = [w for w in within if w["peers"] >= 20]
    out["within_story"] = {
        "needs_with_at_least_20_controls": len(with_peers),
        "need_reply_rate": (sum(1 for w in with_peers if w["replied"]) / len(with_peers))
        if with_peers else None,
        "mean_peer_reply_rate": (sum(w["peer_reply_rate"] for w in with_peers) / len(with_peers))
        if with_peers else None,
        "ratio": ((sum(1 for w in with_peers if w["replied"]) / len(with_peers)) /
                  (sum(w["peer_reply_rate"] for w in with_peers) / len(with_peers)))
        if with_peers and sum(w["peer_reply_rate"] for w in with_peers) else None,
        "silent_in_a_live_thread": sum(
            1 for w in with_peers
            if not w["replied"] and w["peer_reply_rate"] >= 0.4),
        "silent_in_a_live_thread_definition":
            "a need with no reply in a story where at least 40% of other comments "
            "did get one: silence that thread size does not explain",
    }

    # ---- the residual: needs with no reply at all, at scale ----
    silent = [r for r in arm_a if not r["has_subtree"]]
    silent_old = [r for r in a_old if not r["has_subtree"]]
    out["residual"] = {
        "needs_with_no_reply": len(silent),
        "share": len(silent) / len(arm_a) if arm_a else None,
        "needs_with_no_reply_aged180": len(silent_old),
        "median_story_total_of_silent": statistics.median(
            [r["story_total"] for r in silent]) if silent else None,
        "median_story_total_of_answered": statistics.median(
            [r["story_total"] for r in arm_a if r["has_subtree"]]) if withsub else None,
        "silent_in_truncated_stories": sum(
            1 for r in silent if r["story_id"] in set(out["capture"]["stories_with_truncation"])),
    }

    # ---- verdict, evaluated by the script ----
    verdicts = []
    for band in ("all", "aged_%dd" % AGE_DAYS):
        g = gates[band]
        verdicts.append({
            "band": band,
            "verdict": ("H0: thread position explains reply presence; instrument closed"
                        if g["kill_gate_met"] else
                        "need statements are answered above the matched control rate"),
        })
    out["verdicts"] = verdicts

    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps(out["capture"], indent=1, sort_keys=True))
    print(json.dumps(out["gates"], indent=1, sort_keys=True))
    print(json.dumps(out["residual"], indent=1, sort_keys=True))


if __name__ == "__main__":
    main()