#!/usr/bin/env python3
"""E014 step 2: re-count each recurrence query restricted to the
repositories that passed the repository-signal filter."""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "think-free-research",
      "Accept": "application/vnd.github+json"}

queries = json.load(open(os.path.join(HERE, "raw", "repos_from_queries.json")))
classified = json.load(open(os.path.join(HERE, "raw", "scrape_classify.json")))
passing = {r for r, v in classified.items() if v.get("pass")}

out = {}
for label, v in queries.items():
    keep = [r for r in v["repos_full"] if r in passing]
    rec = {"unfiltered_total": v["total_count"],
           "passing_repos_in_first_page": len(keep), "passing_repos": keep}
    if keep:
        q = v["query"] + " " + " ".join("repo:" + r for r in keep)
        url = ("https://api.github.com/search/issues?"
               + urllib.parse.urlencode({"q": q, "per_page": 1}))
        try:
            req = urllib.request.Request(url, headers=UA)
            d = json.load(urllib.request.urlopen(req, timeout=30))
            rec["filtered_total_count"] = d["total_count"]
        except urllib.error.HTTPError as e:
            rec["filtered_error"] = "HTTP %s" % e.code
        time.sleep(7)
    out[label] = rec
    print(label, rec)
with open(os.path.join(HERE, "raw", "filtered_counts.json"), "w") as f:
    json.dump(out, f, indent=1, sort_keys=True)
