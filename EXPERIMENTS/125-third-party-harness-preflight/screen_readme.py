"""E125 step 2 -- the README arm of the screen declared in PROTOCOL.md.

`pool.py` applied the screen to GitHub's `description` field only. The declared
screen is "description **or** its README", and the README arm was not run, so
the population in `inspect.json` was drawn from half the declared rule. This
fetches the README for every repository that cleared the star floor and
re-applies the screen unchanged.

README text is fetched from `raw.githubusercontent.com`, not from the API, so
this costs no search or core budget and a refusal is recorded as a refusal: a
repository whose README could not be read is `unreadable`, and an unreadable
repository is never counted as passing or failing the screen. Screen coverage is
the fraction of the above-floor population where the screen could decide at all,
and it is the first term of G1.
"""

import json
import os
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
READMES = os.path.join(HERE, "readmes")

README_NAMES = ["README.md", "readme.md", "README.rst", "README.txt", "README"]


def fetch_readme(full_name, branch):
    for name in README_NAMES:
        url = "https://raw.githubusercontent.com/%s/%s/%s" % (full_name, branch, name)
        req = urllib.request.Request(url, headers={"User-Agent": "think-free-e125"})
        try:
            with urllib.request.urlopen(req, timeout=20) as fh:
                body = fh.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                continue
            return None, "http %s on %s" % (exc.code, name)
        except Exception as exc:  # noqa: BLE001 - a network failure is a reading
            return None, "error on %s: %s" % (name, type(exc).__name__)
        if body.strip():
            return body, name
    return None, "no README at any of %s" % ", ".join(README_NAMES)


def screen(*texts):
    from pool import NOUNS, VERBS
    blob = " ".join(t for t in texts if t).lower()
    return (any(v in blob for v in VERBS), any(n in blob for n in NOUNS))


def main():
    if not os.path.isdir(READMES):
        os.makedirs(READMES)
    with open(os.path.join(HERE, "pool.json")) as fh:
        pool = json.load(fh)

    above = [r for r in pool["rows"] if r["stars"] >= pool["declared"]["star_floor"]]
    rows = []
    for i, r in enumerate(above):
        body, status = fetch_readme(r["full_name"], r["default_branch"])
        if body is not None:
            with open(os.path.join(READMES, r["full_name"].replace("/", "__") + ".md"), "w") as fh:
                fh.write(body)
        verb, noun = screen(r["description"], body)
        rows.append({
            "full_name": r["full_name"],
            "stars": r["stars"],
            "default_branch": r["default_branch"],
            "description": r["description"],
            "pushed_at": r["pushed_at"],
            "queries": r["queries"],
            "readme": status,
            "readme_chars": len(body) if body else 0,
            "screen_description": bool(screen(r["description"])[0] and screen(r["description"])[1]),
            "screen_readme": (bool(verb and noun) if body is not None else None),
        })
        if i:
            time.sleep(0.4)
        print("%-42s readme=%-28s screen_readme=%s" % (
            r["full_name"], status[:28], rows[-1]["screen_readme"]))

    decidable = [r for r in rows if r["readme_chars"] > 0 or r["description"].strip()]
    passed = [r for r in decidable if r["screen_description"] or r["screen_readme"]]
    coverage = float(len(decidable)) / len(rows) if rows else 0.0
    chosen = passed[:30]

    with open(os.path.join(HERE, "inspect.json"), "w") as fh:
        json.dump({
            "experiment": "E125",
            "rule": ("top 30 by stars of (union of the 3 declared queries, stars>=300) "
                     "passing the declared screen on description OR README"),
            "counts": {
                "above_floor": len(rows),
                "screen_decidable": len(decidable),
                "screen_coverage": round(coverage, 4),
                "passed": len(passed),
                "inspection_set": len(chosen),
            },
            "inspection_set": [r["full_name"] for r in chosen],
            "rows": chosen,
            "rejected": [{"full_name": r["full_name"], "stars": r["stars"],
                          "reason": "screen did not decide" if r not in decidable else "screen failed"}
                         for r in rows if r not in chosen],
        }, fh, indent=1, sort_keys=True)

    print("\nabove floor %d, screen decidable %d, coverage %.4f, passed %d, inspection set %d"
          % (len(rows), len(decidable), coverage, len(passed), len(chosen)))
    for r in chosen:
        print("  %6d  %s" % (r["stars"], r["full_name"]))


if __name__ == "__main__":
    import sys
    sys.path.insert(0, HERE)
    main()