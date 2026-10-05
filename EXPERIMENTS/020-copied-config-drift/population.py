"""E020 population fetch.

Declared in EXPERIMENTS/020-copied-config-drift/README.md before the first
population fetch. Three states, never two: PRESENT, ABSENT (a 404 is an answer),
UNDECIDABLE (anything else -- a 403, a 429, a 5xx, a timeout).  F036: an HTTP 200
means nothing until you know what answered it, and 017's H2 thresholds were once
satisfied by an empty read.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

RAW = "https://raw.githubusercontent.com/{repo}/HEAD/{path}"
SEARCH = "https://api.github.com/search/repositories"

# Declared population rule 1: the term set. Read in the API's own order, capped
# per term, no curation.
TERMS = [
    "claude code hooks",
    "claude code subagents",
    ".claude settings.json",
    "claude code agents",
    "claude code skills",
]

PER_TERM = 40
UA = "think-free-research"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")

# Delay between core requests. raw.githubusercontent is not the rate-limited API,
# but the search endpoint is 10/min unauthenticated.
SEARCH_DELAY = 7.0
RAW_DELAY = 0.4


def fetch(url, tries=3):
    """Return (state, body). state is one of PRESENT / ABSENT / UNDECIDABLE.

    Never collapses UNDECIDABLE into ABSENT: that is the defect this repository
    has now paid for twice.
    """
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return "PRESENT", r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return "ABSENT", ""
            # 403 (rate limited), 429, 5xx: refused, not absent.
            last = "UNDECIDABLE"
            time.sleep(2 * (attempt + 1))
        except Exception:
            last = "UNDECIDABLE"
            time.sleep(2 * (attempt + 1))
    return "UNDECIDABLE", ""


def search(term, per_term=PER_TERM):
    params = {"q": term, "per_page": str(min(per_term, 100))}
    url = SEARCH + "?" + urllib.parse.urlencode(params)
    state, body = fetch(url)
    if state != "PRESENT":
        return None, state
    try:
        d = json.loads(body)
    except ValueError:
        return None, "UNDECIDABLE"
    if "items" not in d:
        return None, "UNDECIDABLE"
    return [i["full_name"] for i in d["items"]], "PRESENT"


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    repos = []
    per_term_state = {}
    for term in TERMS:
        names, state = search(term)
        per_term_state[term] = state
        if names is None:
            continue
        for n in names:
            repos.append((n, term))
        sys.stderr.write("search %-28s -> %s (%d repos)\n" % (term, state, len(names)))
        time.sleep(SEARCH_DELAY)

    # Ordered, deduplicated: first term wins, so the rule is reproducible.
    seen = set()
    ordered = []
    for name, term in repos:
        if name in seen:
            continue
        seen.add(name)
        ordered.append({"repo": name, "entry_term": term})

    for row in ordered:
        row["settings_state"] = fetch(RAW.format(repo=row["repo"], path=".claude/settings.json"))[0]
        row["readme_state"] = fetch(RAW.format(repo=row["repo"], path="README.md"))[0]
        if row["readme_state"] == "PRESENT":
            state, body = fetch(RAW.format(repo=row["repo"], path="README.md"))
            row["readme_bytes"] = len(body)
        time.sleep(RAW_DELAY)

    out = {
        "population_rule": "repository search over the declared term set; .claude/settings.json 200 is entry",
        "terms": TERMS,
        "per_term": PER_TERM,
        "search_state_per_term": per_term_state,
        "n_considered": len(ordered),
        "rows": ordered,
    }
    path = os.path.join(OUT, "population.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("considered %d repos -> %s" % (len(ordered), path))

    states = {}
    for r in ordered:
        states[r["settings_state"]] = states.get(r["settings_state"], 0) + 1
    print("settings.json state:", states)


if __name__ == "__main__":
    main()