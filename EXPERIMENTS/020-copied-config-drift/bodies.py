"""E020 body fetch.

Second declared step: fetch the contents behind the population's two paths so
attribution and comparison can run offline. Results are written per repo so a
later session can re-derive a figure without re-fetching, and so a fetch that
was refused stays visibly refused rather than becoming an empty file.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from population import RAW, fetch  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "raw")

PATHS = [".claude/settings.json", "README.md", ".claude/settings.local.json"]


def main():
    pop = json.load(open(os.path.join(OUT, "population.json")))
    rows = [r for r in pop["rows"] if r["settings_state"] == "PRESENT"]
    store = {}
    for r in rows:
        repo = r["repo"]
        entry = {}
        for p in PATHS:
            state, body = fetch(RAW.format(repo=repo, path=p))
            entry[p] = {"state": state, "bytes": len(body) if body else 0}
            if body:
                with open(os.path.join(OUT, "body--%s--%s" % (repo.replace("/", "__"), p.replace("/", "__"))), "w") as f:
                    f.write(body)
            time.sleep(0.4)
        store[repo] = entry
        sys.stderr.write("%-52s %s\n" % (repo, " ".join("%s=%s" % (p.split("/")[-1], entry[p]["state"]) for p in PATHS)))

    with open(os.path.join(OUT, "bodies.json"), "w") as f:
        json.dump({"paths": PATHS, "rows": store}, f, indent=1, sort_keys=True)
    print("fetched bodies for %d repos" % len(store))


if __name__ == "__main__":
    main()