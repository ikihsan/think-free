#!/usr/bin/env python3
"""E014 step 1b: classify the recurrent cluster's repositories without the
core REST API (exhausted: 60/hr unauthenticated, reset ~22 min out).

Fetches each repository's public HTML page and reads the description meta
tag and the topic tags the page itself renders. The filter terms and the
verdict rule are identical to signal_filter.py; only the source of the
metadata changes, which is recorded in the report. A page that returns no
description is treated as not passing unless its name matches a term.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "think-free-research",
      "Accept": "text/html,application/xhtml+xml"}

TERMS = ["agent", "copilot", "claude", "llm", "coding assistant", "ai coding",
         "ai-agent", "ai agent", "ai assistant", "pair-programming", "cursor"]


def path(*parts):
    return os.path.join(HERE, *parts)


def main():
    partial = json.load(open(path("raw", "repos_full.json"))) \
        if os.path.exists(path("raw", "repos_full.json")) else None
    if partial is None:
        # rebuild the unique repo set from the recorded queries
        now = json.load(open(path("raw", "repos_from_queries.json")))
        repos = sorted({r for v in now.values() for r in v["repos_full"]})
        with open(path("raw", "repos_full.json"), "w") as f:
            json.dump(repos, f, indent=1)
    else:
        repos = partial
    out = {}
    for i, full in enumerate(repos):
        url = "https://github.com/" + full
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                html = r.read(2_000_000).decode("utf-8", "replace")
            m = re.search(r'<meta name="description" content="([^"]*)"', html)
            desc = m.group(1) if m else ""
            topics = re.findall(r'class="[^"]*topic-tag[^"]*"[^>]*>\s*([^<]+)', html)
            hay = (full + " " + desc + " " + " ".join(topics)).lower()
            out[full] = {"description": desc, "topics": [t.strip() for t in topics],
                         "pass": any(t in hay for t in TERMS)}
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            out[full] = {"error": str(e), "pass": None}
        time.sleep(2)
        if (i + 1) % 20 == 0:
            print("fetched", i + 1, flush=True)
            with open(path("raw", "scrape_partial.json"), "w") as f:
                json.dump(out, f, indent=1)
    with open(path("raw", "scrape_classify.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    npass = sum(1 for v in out.values() if v.get("pass"))
    print("pass:", npass, "of", len(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
