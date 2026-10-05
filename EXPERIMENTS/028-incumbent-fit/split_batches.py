#!/usr/bin/env python3
"""Split one reader's Step B view into batches, so a batch fits a reader
context. Mechanical: rows are taken in the view's order and the `own` /
`mismatched_with` pair for a row always travels together, so no batch can see
half of a row's evidence.
"""
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", required=True)
    ap.add_argument("--batch", type=int, required=True)
    ap.add_argument("--batches", type=int, required=True)
    args = ap.parse_args()
    assert 1 <= args.batch <= args.batches
    with open(os.path.join(RAW, "view_b_%s.json" % args.reader)) as fh:
        view = json.load(fh)
    entries = view["view"]
    rows = view["fit_rows"]
    size = (len(rows) + args.batches - 1) // args.batches
    mine = set(rows[(args.batch - 1) * size: args.batch * size])
    chunk = [e for e in entries if e["row"] in mine]
    out = dict(view)
    out["view"] = chunk
    out["batch"] = args.batch
    out["batches"] = args.batches
    out["rows_in_batch"] = sorted(mine)
    path = os.path.join(RAW, "view_b_%s_batch%d.json"
                        % (args.reader, args.batch))
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({
        "path": path,
        "rows": sorted(mine),
        "entries": len(chunk),
        "documentation_chars": sum(len(a.get("documentation_shown") or "")
                                   for e in chunk
                                   for a in e["artifacts_shown"]),
    }))


if __name__ == "__main__":
    main()