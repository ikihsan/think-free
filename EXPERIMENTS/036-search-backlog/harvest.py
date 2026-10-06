#!/usr/bin/env python3
"""E036 harvest: does Stack Overflow's own search return the score-tail backlog?

Every request is appended to raw/*.jsonl with the URL, the status and the body, so
the run is replayable and diffable. Nothing is derived here; tally.py reads the
raw bytes. See PROTOCOL.md section 3 for the declared gates and sample sizes.

  python3 harvest.py --probe     # the 6 reachability requests of PROTOCOL section 1
  python3 harvest.py             # the 11 declared measurement requests
  python3 harvest.py --budget    # report quota_remaining without spending a request
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.stackexchange.com/2.3"
UA = "think-free-research/1.0"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
E034 = os.path.join(HERE, "..", "034-reask-tail", "raw")

DUP = ("Duplicate", "exact duplicate")


def rows(path):
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


def e034_rows():
    out = []
    for name in ("harvest.jsonl", "r1.jsonl", "r2.jsonl"):
        out.extend(rows(os.path.join(E034, name)))
    return out


def clean(title):
    """Undo the HTML entities the API returns, so the query is the question's words."""
    for a, b in (("&quot;", '"'), ("&#39;", "'"), ("&amp;", "&"),
                 ("&lt;", "<"), ("&gt;", ">"), ("&hellip;", "...")):
        title = title.replace(a, b)
    return " ".join(title.split())


def get(path, params):
    qs = urllib.parse.urlencode(params, doseq=True)
    url = BASE + path + "?" + qs
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            status, body = r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        status, body = e.code, e.read().decode("utf-8", "replace")
    except Exception as e:                                    # noqa: BLE001
        status, body = -1, repr(e)
    elapsed = round(time.time() - t0, 3)
    try:
        parsed = json.loads(body)
    except ValueError:
        parsed = {"_unparsed": body[:400]}
    return {
        "url": url,
        "path": path,
        "params": params,
        "status": status,
        "elapsed_s": elapsed,
        "body": body,
        "n_items": len(parsed.get("items", [])) if isinstance(parsed, dict) else 0,
        "quota_remaining": parsed.get("quota_remaining") if isinstance(parsed, dict) else None,
        "error_message": parsed.get("error_message") if isinstance(parsed, dict) else None,
    }


def emit(handle, record):
    handle.write(json.dumps(record, sort_keys=True) + "\n")
    handle.flush()


def pick(data, arm, n, per_cell=3, only_dup=True):
    """Declared selection: first n rows of the arm in E034's byte order, at most
    per_cell per (site, tag), duplicates only where the arm has them."""
    chosen, seen = [], {}
    for r in data:
        if r.get("arm") != arm:
            continue
        if only_dup and r.get("closed_reason") not in DUP:
            continue
        cell = (r["site"], r["tag"])
        if seen.get(cell, 0) >= per_cell:
            continue
        seen[cell] = seen.get(cell, 0) + 1
        chosen.append(r)
        if len(chosen) >= n:
            break
    return chosen


PROBE = [
    ("probe-info", "/info", {"site": "stackoverflow"}),
    ("probe-advanced", "/search/advanced", {"site": "stackoverflow", "q": "python", "pagesize": 3}),
    ("probe-excerpts", "/search/excerpts", {"site": "stackoverflow", "q": "python", "pagesize": 3}),
    ("probe-closed-yes", "/search/advanced",
     {"site": "stackoverflow", "tagged": "git", "closed": "yes", "pagesize": 5}),
    ("probe-closed-yes-asc", "/search/advanced",
     {"site": "stackoverflow", "tagged": "git", "closed": "yes", "sort": "votes",
      "order": "asc", "pagesize": 5}),
    ("probe-closed-maybe", "/search/advanced",
     {"site": "stackoverflow", "tagged": "git", "closed": "maybe", "pagesize": 5}),
]


def run_probe():
    with open(os.path.join(RAW, "probe.jsonl"), "a") as fh:
        for name, path, params in PROBE:
            rec = get(path, params)
            rec["measure"] = name
            rec["ts"] = int(time.time())
            emit(fh, rec)
            print("%-24s %-16s %3d items=%-3d quota=%s" % (
                name, path, rec["status"], rec["n_items"], rec["quota_remaining"]))
            time.sleep(0.35)


def run(stage="all"):
    data = e034_rows()
    tail_ids = set(r["question_id"] for r in data
                   if r["arm"] == "tail" and r["closed_reason"] in DUP)
    customs_tail = [r for r in data
                    if r["arm"] == "tail" and r["site"] == "travel" and r["tag"] == "customs"]
    customs_ids = set(r["question_id"] for r in customs_tail)
    git_ids = set(r["question_id"] for r in data
                  if r["arm"] == "tail" and r["site"] == "stackoverflow"
                  and r["tag"] == "git")
    tail = pick(data, "tail", 8)
    ctrl = pick(data, "default", 8, only_dup=False)
    print("population: tail duplicates=%d (git=%d) customs tail ids=%d; selected tail=%d control=%d"
          % (len(tail_ids), len(git_ids), len(customs_ids), len(tail), len(ctrl)))

    reach = [
        # R0: is `closed` decorative? Does the route enumerate the closed tail with no
        # closed parameter at all?
        ("r0-no-closed-param", "/search/advanced",
         {"site": "stackoverflow", "tagged": "git", "sort": "votes", "order": "asc",
          "pagesize": 100}, git_ids),
        # R1: the decisive reachability test, on the densest tag.
        ("r1-customs-closed-asc", "/search/advanced",
         {"site": "travel", "tagged": "customs", "closed": "yes", "sort": "votes",
          "order": "asc", "pagesize": 100}, customs_ids),
    ]
    # n is set by the quota actually available at run time, never chosen after seeing
    # a rate. See PROTOCOL.md section 3 and README.md "Ceiling".
    per_arm = 4 if stage == "all" else int(os.environ.get("E036_N", "2"))
    retrieval = []
    for i, r in enumerate(tail[:per_arm]):
        retrieval.append(("r2-tail-%d" % (i + 1), "/search/advanced",
                          {"site": r["site"], "q": clean(r["title"]), "pagesize": 100},
                          {r["question_id"]}))
    for i, r in enumerate(ctrl[:per_arm]):
        retrieval.append(("r3-control-%d" % (i + 1), "/search/advanced",
                          {"site": r["site"], "q": clean(r["title"]), "pagesize": 100},
                          {r["question_id"]}))
    retrieval.append(("r4-negative-control", "/search/advanced",
                      {"site": "stackoverflow", "q": "zzqxwv nonexistent phrase 4198",
                       "pagesize": 100}, set()))
    plan = reach if stage == "reach" else retrieval
    print("stage=%s requests=%d n_per_arm=%d" % (stage, len(plan), per_arm))

    with open(os.path.join(RAW, "measures.jsonl"), "a") as fh:
        for name, path, params, targets in plan:
            rec = get(path, params)
            rec["measure"] = name
            rec["target_ids"] = sorted(targets)
            rec["ts"] = int(time.time())
            try:
                items = json.loads(rec["body"]).get("items", [])
            except ValueError:
                items = []
            ids = [it.get("question_id") for it in items]
            rec["returned_target_ids"] = [i for i in ids if i in targets]
            rec["returned_scores"] = [it.get("score") for it in items][:12]
            rec["first_target_rank"] = next(
                (k + 1 for k, i in enumerate(ids) if i in targets), None)
            emit(fh, rec)
            print("%-24s %3d items=%-4d quota=%-5s targets_found=%d/%d rank=%s" % (
                name, rec["status"], rec["n_items"], rec["quota_remaining"],
                len(rec["returned_target_ids"]), len(targets), rec["first_target_rank"]))
            time.sleep(0.35)


def budget():
    rec = get("/info", {"site": "stackoverflow"})
    print("status", rec["status"], "quota_remaining", rec["quota_remaining"])


if __name__ == "__main__":
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--probe":
        run_probe()
    elif arg == "--budget":
        budget()
    else:
        run(arg if arg in ("reach", "all") else "all")
