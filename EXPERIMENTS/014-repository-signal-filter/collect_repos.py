#!/usr/bin/env python3
"""Collect the unique owner/name repository set behind E012's four
recurrence queries, this time keeping the owner so a repository can
be addressed."""
import json
import os
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "think-free-research",
      "Accept": "application/vnd.github+json"}
QUERIES = [
    ("agent-unrequested-edits",
     'is:issue is:open created:>2025-01-01 "not asked for" in:title,body'),
    ("agent-unrelated-changes",
     'is:issue is:open created:>2025-01-01 "unrelated changes" in:title,body'),
    ("agent-scope-creep",
     'is:issue is:open created:>2025-01-01 "scope creep" agent in:title,body'),
    ("copilot-unrelated-file",
     'is:issue is:open created:>2025-01-01 "unrelated file" copilot in:title,body'),
]

out = {}
for label, q in QUERIES:
    url = ("https://api.github.com/search/issues?"
           + urllib.parse.urlencode({"q": q, "per_page": 30}))
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
    repos = sorted({it["repository_url"].split("/repos/")[-1]
                    for it in d.get("items", [])})
    out[label] = {"query": q, "total_count": d.get("total_count"),
                  "repos_full": repos}
    print(label, d.get("total_count"), len(repos), flush=True)
    time.sleep(7)
p = os.path.join(HERE, "raw", "repos_from_queries.json")
with open(p, "w") as f:
    json.dump(out, f, indent=1)
print("wrote", p)
