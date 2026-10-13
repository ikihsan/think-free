"""E125 step 1 -- draw the declared population, once.

Three queries, `sort=stars`, 40 per page, union by full_name, a 300-star floor,
and the screen from PROTOCOL.md. Raw search responses are kept beside the derived
pool so every row can be traced to the bytes it came from.

Unauthenticated GitHub search allows 10 requests a minute; the sleep is the
declared pacing, not politeness. A body that is not JSON is written to
`search-raw/` and the query is recorded as unreadable -- F036's shape, where a
rate-limit page arrives with HTTP 200 and reads as an answer.
"""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "search-raw")

QUERIES = ["llm eval framework", "llm evaluation harness", "agent evaluation framework"]
PER_PAGE = 40
STAR_FLOOR = 300

# The screen, verbatim from PROTOCOL.md: a scoring verb AND an evaluation noun.
VERBS = ["score", "scoring", "grade", "grading", "metric", "judge"]
NOUNS = ["eval", "evaluation", "benchmark", "test suite"]


def search(q):
    url = ("https://api.github.com/search/repositories?q="
           + urllib.parse.quote(q)
           + "&sort=stars&order=desc&per_page=%d" % PER_PAGE)
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "think-free-e125",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as fh:
            body = fh.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return {"query": q, "status": exc.code, "unreadable": True}
    try:
        payload = json.loads(body)
    except ValueError:
        with open(os.path.join(RAW, "nonjson-%s.txt" % q.replace(" ", "_")), "w") as fh:
            fh.write(body[:4000])
        return {"query": q, "status": "non-json body", "unreadable": True}
    if "items" not in payload:
        return {"query": q, "status": payload.get("message", "no items"), "unreadable": True}
    return {"query": q, "status": 200, "total_count": payload.get("total_count"),
            "items": payload["items"]}


def screen(*texts):
    blob = " ".join(t for t in texts if t).lower()
    return (any(v in blob for v in VERBS), any(n in blob for n in NOUNS))


def main():
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    responses = []
    for i, q in enumerate(QUERIES):
        if i:
            time.sleep(8)  # declared pacing against the 10/min search budget
        responses.append(search(q))
    with open(os.path.join(RAW, "search-responses.json"), "w") as fh:
        json.dump(responses, fh, indent=1, sort_keys=True)

    pool = {}
    unreadable_queries = []
    for r in responses:
        if r.get("unreadable"):
            unreadable_queries.append(r["query"])
            continue
        for item in r["items"]:
            pool[item["full_name"]] = {
                "full_name": item["full_name"],
                "stars": item["stargazers_count"],
                "default_branch": item["default_branch"],
                "description": item.get("description") or "",
                "pushed_at": item.get("pushed_at"),
                "queries": [],
            }
            pool[item["full_name"]]["queries"].append(r["query"])

    rows = []
    for name in sorted(pool):
        p = pool[name]
        verb, noun = screen(p["description"])
        rows.append({
            "full_name": p["full_name"],
            "stars": p["stars"],
            "default_branch": p["default_branch"],
            "description": p["description"],
            "pushed_at": p["pushed_at"],
            "queries": p["queries"],
            "screen_description": bool(verb and noun),
        })
    rows.sort(key=lambda r: (-r["stars"], r["full_name"]))

    with open(os.path.join(HERE, "pool.json"), "w") as fh:
        json.dump({
            "experiment": "E125",
            "declared": {
                "queries": QUERIES, "per_page": PER_PAGE, "star_floor": STAR_FLOOR,
                "verbs": VERBS, "nouns": NOUNS, "inspection_set": 30,
            },
            "unreadable_queries": unreadable_queries,
            "pool_size": len(rows),
            "rows": rows,
        }, fh, indent=1, sort_keys=True)

    above = [r for r in rows if r["stars"] >= STAR_FLOOR]
    passed = [r for r in above if r["screen_description"]]
    chosen = passed[:30]
    with open(os.path.join(HERE, "inspect.json"), "w") as fh:
        json.dump({
            "experiment": "E125",
            "rule": "top 30 by stars of (union of 3 queries) with stars>=300 passing the description screen",
            "counts": {"pool": len(rows), "above_floor": len(above),
                       "passed_description_screen": len(passed)},
            "inspection_set": [r["full_name"] for r in chosen],
            "rows": chosen,
        }, fh, indent=1, sort_keys=True)

    print("queries unreadable: %s" % (unreadable_queries or "none"))
    print("pool %d, above floor %d, pass description screen %d, inspection set %d"
          % (len(rows), len(above), len(passed), len(chosen)))
    for r in chosen:
        print("  %6d  %s" % (r["stars"], r["full_name"]))


if __name__ == "__main__":
    main()