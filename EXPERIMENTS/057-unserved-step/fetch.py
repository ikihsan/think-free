"""E057 fetch: enumerate SE sites, apply the published exclusion list, take the 12
alphabetically first survivors, and pull the unanswered stratum in both arms."""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

API = "https://api.stackexchange.com/2.3"
UA = {"User-Agent": "think-free-research/0.1"}
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

EXCLUDE = """
meta language linguist software linux ubuntu unix windows server
web code program develop devops android ios apple google
mathemat physic chemi bioinformat comput cryptograph
signal data sci artificial intelligence llm quantum robot blender
game arduino raspberry internet of things bitcoin ethereum cardano
stack dba ux graphic video music sound design the workplace
project management drupal joomla magento salesforce sharepoint
sitecore wordpress network engineering information security
hardware recommendations vi and vim emacs tex elementary
retrocomput open source open data geographic information
operations research quantitative econom politic history literature
philosoph buddhis christian hindu islam mytholog skeptic
anime poker board card chess proof assistants worldbuilding
puzzling academia ask different my yodeya
""".split()

NSITES = 12
PAGESIZE = 100
WINDOW_DAYS = 36 * 30


def get(path, **params):
    q = urllib.parse.urlencode(sorted(params.items()))
    req = urllib.request.Request("%s/%s?%s" % (API, path, q), headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        d = json.load(r)
    if d.get("backoff"):
        time.sleep(d["backoff"] + 1)
    return d


def main():
    os.makedirs(RAW, exist_ok=True)

    sites = {}
    for page in range(1, 6):
        d = get("sites", pagesize=250, page=page)
        for it in d["items"]:
            sites[it["api_site_parameter"]] = it["name"]
        if not d.get("has_more"):
            break
        time.sleep(0.4)
    print("sites enumerated:", len(sites))

    kept = []
    for param, name in sites.items():
        low = name.lower()
        if any(tok in low for tok in EXCLUDE):
            continue
        kept.append((name, param))
    kept.sort()
    print("after exclusion list:", len(kept))
    picked = kept[:NSITES]
    print("population (alphabetically first %d of survivors):" % NSITES)
    for name, param in picked:
        print("   %-42s %s" % (name, param))

    with open(os.path.join(RAW, "population.json"), "w") as fh:
        json.dump({"sites_enumerated": len(sites), "kept": kept, "picked": picked}, fh, indent=1)

    fromdate = int((time.time() - WINDOW_DAYS * 86400))
    index = {"fromdate": fromdate, "window_days": WINDOW_DAYS, "sites": []}
    for name, param in picked:
        for arm, order in (("tail", "asc"), ("head", "desc")):
            rows = []
            for page in (1, 2):
                d = get("questions", site=param, pagesize=PAGESIZE, page=page,
                        sort="votes", order=order, fromdate=fromdate,
                        closed="no", hasaccepted="no")
                rows.extend(d["items"])
                if not d.get("has_more"):
                    break
                time.sleep(1.2)
            fn = os.path.join(RAW, "%s-%s.json" % (param, arm))
            with open(fn, "w") as fh:
                json.dump(rows, fh)
            users = len(set(r.get("owner", {}).get("user_id") for r in rows if r.get("owner")))
            print("%-42s %-4s rows=%4d users=%4d" % (name, arm, len(rows), users))
            index["sites"].append({"name": name, "param": param, "arm": arm,
                                   "file": os.path.basename(fn), "rows": len(rows),
                                   "users": users})
            time.sleep(1.2)
    with open(os.path.join(RAW, "index.json"), "w") as fh:
        json.dump(index, fh, indent=1)
    print("wrote", os.path.join(RAW, "index.json"))


if __name__ == "__main__":
    sys.exit(main())
