#!/usr/bin/env python3
"""The need's exact semantics, implemented minimally.

One annotation per call site; a runtime-read mode variable per path
(off / metric / log / trace); the emitter chosen on every call. ``--run``
flips modes between calls of the same annotated function and asserts the
emission kinds change accordingly.
"""

import sys
import time

_MODES = ("off", "metric", "log", "trace")

# The runtime control: read on every instrumented call.
_mode_by_path = {}


def emission(path, duration):
    mode = _mode_by_path.get(path, "off")
    if mode == "metric":
        return {"kind": "metric", "path": path, "name": "call_duration_ms", "value": duration * 1000}
    if mode == "log":
        return {"kind": "log", "path": path, "line": f"{path} took {duration:.4f}s"}
    if mode == "trace":
        return {"kind": "trace", "path": path, "span": path, "duration": duration}
    return None


EMITTED = []


def annotate(path):
    def wrap(fn):
        def inner(*args, **kwargs):
            start = time.perf_counter()
            result = fn(*args, **kwargs)
            duration = time.perf_counter() - start
            record = emission(path, duration)
            if record is not None:
                EMITTED.append(record)
            return result

        return inner

    return wrap


@annotate("checkout")
def checkout():
    return 42


@annotate("search")
def search():
    return []


def main():
    _mode_by_path["checkout"] = "metric"
    checkout()
    _mode_by_path["checkout"] = "log"
    checkout()
    _mode_by_path["checkout"] = "trace"
    checkout()
    _mode_by_path["checkout"] = "off"
    checkout()
    _mode_by_path["search"] = "trace"
    search()

    kinds = [r["kind"] for r in EMITTED]
    expected = ["metric", "log", "trace", "trace"]
    assert kinds == expected, (kinds, expected)
    assert all(r["path"] in ("checkout", "search") for r in EMITTED)
    if "--run" in sys.argv:
        for r in EMITTED:
            print(r)
    print("sigsel: OK — runtime per-path flip observed", [r["kind"] for r in EMITTED])


if __name__ == "__main__":
    main()
