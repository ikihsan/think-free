"""E169 step 4: the four query arms, and the aggregation.

Arms, declared in PROTOCOL.md and AMENDMENT-1.md before any request:

  A1 phrase   -- the post's literal, quoted.  Skipped where the hand read says
                 there is no verbatim literal, because nobody quotes a paragraph.
  A2 keyword  -- the hand read's word form.  Always run, so both readings exist
                 for every row rather than the better one chosen per row.
  A3 null     -- the title's first eight words, carrying no error literal.  If
                 this reaches the target as often, the literal did nothing.
  A4 scoped   -- the same keyword inside the target repository, i.e. what a
                 developer does once they know which component it is.  Run only
                 after A1/A2 miss, so it costs queries only where they are
                 needed to bound the incumbent from above.

A miss is evidence about this index and this query.  A hit is a lower bound on
the incumbent: GitHub's issue index is what a general engine indexes for this
content, and A4 is the workflow a developer actually performs.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reach                                                     # noqa: E402

HAND = os.path.join(HERE, "hand-queries.jsonl")


def wilson(k, n, z=1.96):
    if not n:
        return [None, None]
    p = k / float(n)
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]


def share(k, n):
    return round(k / float(n), 4) if n else None


def load_hand():
    out = {}
    for line in open(HAND):
        if line.strip():
            r = json.loads(line)
            out[r["qid"]] = r
    return out


def load_plan():
    """The 13 tracker-target rows, with the hand read attached.

    Rebuilt from `run.load_rows` rather than read back from the dry-run file,
    because that file carries no `hand` field and step 5 needs one.
    """
    import run
    hand = load_hand()
    rows = [r for r in run.load_rows()
            if r["state"] == "ok" and r.get("target") and r["qid"] in hand]
    for r in rows:
        r["hand"] = hand.get(r["qid"], {})
    rows.sort(key=lambda r: -r["views"])
    return rows


def execute(plan):
    hand = load_hand()
    for i, r in enumerate(plan, 1):
        h = hand.get(r["qid"], {})
        r["hand"] = h
        r["extractor_literal"] = r.get("literal")
        r["extractor_matches_hand"] = bool(
            h.get("phrase") and h["phrase"].strip() ==
            (r.get("extractor_literal") or "").strip())
        r["arms"] = {}
        phrase = (h.get("phrase") or "").strip()
        if phrase:
            r["arms"]["A1_phrase"] = reach.search_once(phrase, r["target"])
        r["arms"]["A2_keyword"] = reach.search_once(h.get("keyword", ""),
                                                    r["target"])
        r["arms"]["A3_null"] = reach.search_once(
            " ".join(r["title"].split()[:8]), r["target"])
        if not any(a.get("rank") for a in r["arms"].values()):
            t = r["target"]
            r["arms"]["A4_scoped"] = reach.search_once(
                "%s repo:%s/%s" % (h.get("keyword", ""), t["owner"], t["repo"]),
                r["target"])
        sys.stderr.write("[%2d/%d] %s %s\n" % (
            i, len(plan), r["qid"],
            " ".join("%s=%s" % (k.split("_")[0], v.get("rank", "e"))
                     for k, v in r["arms"].items())))
    return plan


def summarise(plan):
    n = len(plan)
    def hit(arm):
        return [r for r in plan if (r["arms"].get(arm) or {}).get("rank")]
    def unread(arm):
        return [r for r in plan if (r["arms"].get(arm) or {}).get("unreadable")]
    a1_denom = [r for r in plan if "A1_phrase" in r["arms"]]
    a4 = [r for r in plan if "A4_scoped" in r["arms"]]
    a4_hit = [r for r in a4 if r["arms"]["A4_scoped"].get("rank")]
    either = [r for r in plan
              if (r["arms"].get("A1_phrase") or {}).get("rank")
              or (r["arms"].get("A2_keyword") or {}).get("rank")]
    return {
        "rows_queried": n,
        "A1_phrase": {"n": len(a1_denom), "hit": len(hit("A1_phrase")),
                      "share": share(len(hit("A1_phrase")), len(a1_denom)),
                      "wilson95": wilson(len(hit("A1_phrase")), len(a1_denom)),
                      "unreadable": len(unread("A1_phrase"))},
        "A2_keyword": {"n": n, "hit": len(hit("A2_keyword")),
                       "share": share(len(hit("A2_keyword")), n),
                       "wilson95": wilson(len(hit("A2_keyword")), n),
                       "unreadable": len(unread("A2_keyword"))},
        "A3_null_control": {"n": n, "hit": len(hit("A3_null")),
                            "share": share(len(hit("A3_null")), n),
                            "wilson95": wilson(len(hit("A3_null")), n)},
        "A4_repo_scoped_after_miss": {
            "n_run": len(a4), "hit": len(a4_hit),
            "rescued": len(a4_hit),
            "share_of_all_rows": share(len(a4_hit), n)},
        "any_global_arm": {"n": n, "hit": len(either),
                           "share": share(len(either), n),
                           "wilson95": wilson(len(either), n)},
        "incumbent_upper_bound": {
            "n": n, "hit": len(either) + len(a4_hit),
            "share": share(len(either) + len(a4_hit), n),
            "wilson95": wilson(len(either) + len(a4_hit), n)},
        "literal_types": {t: sum(1 for r in plan
                                 if (r.get("hand") or {}).get("literal_type") == t)
                          for t in ("error_message", "ui_string", "code_token",
                                    "symptom_only")},
        "extractor_matched_hand_phrase": sum(1 for r in plan
                                             if r.get("extractor_matches_hand")),
        "ranks_A2": sorted((r["arms"]["A2_keyword"].get("rank")
                            for r in plan if r["arms"]["A2_keyword"].get("rank"))),
    }


def main():
    plan = json.load(open(os.path.join(HERE, "raw", "query-plan.json")))["plan"]
    execute(plan)
    summary = summarise(plan)
    json.dump({"summary": summary, "rows": plan},
              open(os.path.join(HERE, "raw", "query-results.json"), "w"),
              indent=1)
    time.sleep(0.1)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())