#!/usr/bin/env python3
"""E038 harvest: two open gates on E037's candidate, on named surfaces.

Every request is appended to raw/*.jsonl with its URL, params, status and body, so
the run is replayable, diffable and quotable. Nothing is derived here; readout.py
reads the raw bytes. The gates are in PROTOCOL.md, written before the first request.

  python3 harvest.py --probe      # which instruments answer unauthenticated
  python3 harvest.py --budget     # what is left, without spending a request
  python3 harvest.py poola        # the interface, by mechanism name (code index)
  python3 harvest.py poolb        # the capability in users' words (Stack Exchange)
  python3 harvest.py --status     # which declared requests are already on disk
"""
import os
import sys

from harvest_core import RAW, PROBE, budget, do, done
from harvest_pools import poola, poolb, poolc, poold  # noqa: E402


def probe():
    with open(os.path.join(RAW, "requests.jsonl"), "a") as fh:
        for name, url in PROBE:
            do(fh, name, url)


def status():
    seen = sorted(done())
    print("%d request(s) on disk" % len(seen))
    for m in seen:
        print("  ", m)

if __name__ == "__main__":
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--probe":
        probe()
    elif arg == "--budget":
        budget()
    elif arg == "--status":
        status()
    elif arg == "poola":
        poola()
    elif arg == "poolb":
        poolb()
    elif arg == "poolc":
        poolc()
    elif arg == "poold":
        poold()
    else:
        print(__doc__)
