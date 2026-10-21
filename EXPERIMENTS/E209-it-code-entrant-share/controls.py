#!/usr/bin/env python3
"""E209 controls C1/C2 -- one well-formed non-existent code and one malformed code.

Both are single-page probes against the same endpoint and window as the
experiment, so a confident wrong answer cannot pass a threshold unnoticed.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch  # noqa: E402  (same directory)


def run(code, capture_prefix):
    payload = {
        "filters": fetch.base_filters(
            fetch.WINDOWS["current"], psc_codes=[code]),
        "limit": 100, "page": 1, "spending_level": "awards",
    }
    st, parsed, meta = fetch.call(payload, capture_prefix)
    results = (parsed or {}).get("results") if isinstance(parsed, dict) else None
    return {"status": st,
            "n_results": len(results) if results is not None else None,
            "messages": (parsed or {}).get("messages") if isinstance(parsed, dict) else None}


def main():
    out = {
        "C1_zzzz": run("ZZZZ", "ctl_zzzz"),
        "C2_not_a_code": run("not-a-code", "ctl_notacode"),
    }
    path = os.path.join(fetch.RAW, "controls.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
