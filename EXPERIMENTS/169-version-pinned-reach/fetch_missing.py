"""E169 step 1: fetch the 61 `vp = 1` rows E168 never fetched.

E168 fetched threads for its 24-row graded sample only.  G2 needs a larger
population, and unlike an assistant attempt a search query cannot be
contaminated by reading a thread -- so the whole `vp = 1` stratum is used and
E168's 24 are reused from `threads.json` rather than refetched.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.stackexchange.com/2.3"
OUT = os.path.join(HERE, "threads-all.json")
E168 = os.path.join(os.path.dirname(HERE), "168-version-pinned-need",
                    "threads.json")


def get(path, **params):
    params.setdefault("site", "stackoverflow")
    params.setdefault("filter", "withbody")
    url = "%s/%s?%s" % (API, path, urllib.parse.urlencode(params))
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as fh:
                return json.loads(fh.read().decode("utf-8"))
        except Exception as exc:                                 # noqa: BLE001
            sys.stderr.write("retry %d %s: %s\n" % (attempt, path, exc))
            time.sleep(4 * (attempt + 1))
    raise SystemExit("fetch failed: %s" % path)


def main():
    rows = [json.loads(l) for l in open(os.path.join(
        HERE, "..", "168-version-pinned-need", "classified.jsonl"))]
    want = [str(r["qid"]) for r in rows if r["vp"] == 1]
    threads = {}
    reused = 0
    if os.path.exists(E168):
        old = json.load(open(E168))
        for q, t in old.items():
            threads[q] = t
            reused += 1
    todo = [q for q in want if q not in threads]
    sys.stderr.write("population %d, reused %d, to fetch %d\n"
                     % (len(want), reused, len(todo)))

    empty_body = []
    for q in todo:
        qi = int(q)
        data = get("questions/%d" % qi)
        items = data.get("items", [])
        if not items:
            empty_body.append(q)
            time.sleep(1.0)
            continue
        it = items[0]
        a = get("questions/%d/answers" % qi, sort="votes")
        it["answers"] = a.get("items", [])
        if not it.get("body"):
            empty_body.append(q)
        threads[q] = it
        time.sleep(1.1)

    with open(OUT, "w") as fh:
        json.dump(threads, fh, indent=1, sort_keys=True)
    print(json.dumps({
        "population_vp1": len(want),
        "reused_from_e168": reused,
        "fetched_now": len(todo),
        "in_file": len(threads),
        "missing": sorted(set(want) - set(threads)),
        "no_question_body": sorted(empty_body),
        "with_answers": sum(1 for t in threads.values() if t.get("answers")),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())