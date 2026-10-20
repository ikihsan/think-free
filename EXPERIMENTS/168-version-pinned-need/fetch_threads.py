#!/usr/bin/env python3
"""E168 step 4: fetch the threads for the 24 sampled rows.

Runs only after `attempts_{a,b,c}.py` exist on disk, which is what makes
the blinding auditable: the attempt modules are written, and their mtimes
are recorded here, before a single answer body is read.
"""
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.stackexchange.com/2.3"
OUT = os.path.join(HERE, "threads.json")
MTIME = os.path.join(HERE, "attempts_written_before_fetch.json")


def get(path, **params):
    params.setdefault("site", "stackoverflow")
    params.setdefault("filter", "withbody")
    url = "%s/%s?%s" % (API, path, urllib.parse.urlencode(params))
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=45) as fh:
                return json.loads(fh.read().decode("utf-8"))
        except Exception as exc:                      # noqa: BLE001
            sys.stderr.write("retry %d %s: %s\n" % (attempt, path, exc))
            time.sleep(4 * (attempt + 1))
    raise SystemExit("fetch failed: %s" % path)


def main():
    rows = [json.loads(l) for l in open(os.path.join(HERE,
                                                      "classified.jsonl"))]
    want = [r for r in rows if r["vp"] == 1 and not r["in_e126_graded40"]]
    want.sort(key=lambda r: -r["views"])
    want = want[:24]
    qids = [r["qid"] for r in want]

    threads = {}
    for i in range(0, len(qids), 50):
        batch = qids[i:i + 50]
        data = get("questions/%s" % ";".join(str(q) for q in batch))
        items = data.get("items", [])
        if data.get("has_more"):
            sys.stderr.write("WARNING: has_more true, page truncated\n")
        for it in items:
            threads[str(it["question_id"])] = it
        time.sleep(1)

    # DEFECT FOUND AND REPAIRED, 2026-10-16. The first run of this script
    # called only `questions/{ids}` with `filter=withbody`, and every item
    # came back with `answers: []`. That filter populates the question body,
    # not the answers collection, so all 24 threads graded as having no
    # thread at all. Answers are therefore fetched from their own endpoint,
    # sorted by votes, and merged in. `answers_empty_first_fetch` records the
    # defect rather than hiding it.
    empty_first = sum(1 for t in threads.values()
                      if not (t.get("answers") or []))
    # The /answers endpoint does not accept a question list; fetch per
    # question id.
    byq = {}
    for q in qids:
        data = get("questions/%d/answers" % int(q))
        for a in data.get("items", []):
            byq.setdefault(int(q), []).append(a)
        time.sleep(1.1)
    for k, lst in byq.items():
        if str(k) in threads:
            threads[str(k)]["answers"] = lst

    with open(OUT, "w") as fh:
        json.dump(threads, fh, indent=1, sort_keys=True)

    # Audit trail: attempt-module mtimes must predate this fetch.
    marks = {}
    for name in ("attempts_a.py", "attempts_b.py", "attempts_c.py"):
        marks[name] = os.path.getmtime(os.path.join(HERE, name))
    marks["threads.json"] = os.path.getmtime(OUT)
    marks["all_attempts_predate_fetch"] = all(
        marks[n] <= marks["threads.json"]
        for n in ("attempts_a.py", "attempts_b.py", "attempts_c.py"))
    with open(MTIME, "w") as fh:
        json.dump(marks, fh, indent=2)

    print(json.dumps({
        "requested": len(qids),
        "fetched": len(threads),
        "answers_empty_first_fetch": empty_first,
        "threads_with_answers": sum(
            1 for t in threads.values() if t.get("answers")),
        "missing": sorted(set(str(q) for q in qids) - set(threads)),
        "all_attempts_predate_fetch": marks["all_attempts_predate_fetch"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    import urllib.parse                                  # noqa: E402
    sys.exit(main())