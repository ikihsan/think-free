#!/usr/bin/env python3
"""Build one reader's Step B view: requirements, that reader's own Step A
attribute, and the artifact documentation excerpts.

Bounds come from PROTOCOL-AMENDMENT-2: at most the first four artifacts in the
order the screen recorded them, at most 1,800 characters of each stored capture.
The mismatched control for row i is row (i + 1) mod n over the fit rows, so
every fit row contributes exactly one control and no artifact is ever paired
with its own requirement.
"""
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
MAX_ARTIFACTS = 4
CHARS = 1800


def read_jsonl(path):
    with open(path) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", required=True,
                    help="r1 or r2; the file whose Step A this view embeds")
    args = ap.parse_args()

    reqs = {r["row"]: r for r in read_jsonl(
        os.path.join(RAW, "requirements.jsonl"))}
    step_a = {r["row"]: r for r in read_jsonl(
        os.path.join(RAW, "step_a_%s.jsonl" % args.reader))}
    log = {}
    for rec in read_jsonl(os.path.join(RAW, "fetch_log.jsonl")):
        key = (rec["row"], rec["corpus"], rec["artifact"])
        if key not in log or (rec["has_text"]
                              and not log[key]["has_text"]):
            log[key] = rec

    # The fit population: rows for which the screen named at least one artifact.
    fit = sorted({row for (row, _c, _a) in log})
    shifted = {row: fit[(i + 1) % len(fit)] for i, row in enumerate(fit)}

    view = []
    for row in fit:
        req = reqs[row]
        att = step_a[row]
        # fetch_log order is the screen's order. The window is the first
        # MAX_ARTIFACTS artifacts the screen named. An artifact in that window
        # whose documentation could not be stored appears with an empty
        # `documentation_shown` rather than being swapped for one further down
        # the list, because the readers were shown this bundle and the record
        # has to be the bundle the readers saw.
        own = [k for k in log if k[0] == row]
        entries = []
        for key in own[:MAX_ARTIFACTS]:
            rec = log[key]
            body = ""
            if rec["has_text"]:
                with open(rec["path"]) as fh:
                    body = fh.read(CHARS)
            entries.append({
                "shown": True,
                "has_documentation": rec["has_text"],
                "corpus": rec["corpus"],
                "artifact": rec["artifact"],
                "documentation_path": rec["path"] if rec["has_text"] else None,
                "documentation_shown": body,
                "documentation_chars_shown": len(body),
                "documentation_chars_stored": rec["chars"],
                "fetch_http": rec["http"],
            })
        view.append({
            "row": row,
            "pairing": "own",
            "story_title": req["story_title"],
            "requirement_text": req["requirement_text"],
            "step_a": {k: att[k] for k in
                       ("category", "attribute", "attribute_stated",
                        "attribute_note")},
            "artifacts_shown": entries,
            "artifacts_named_but_not_shown": len(own) - len(entries),
        })
        # The mismatched control: this row's requirement, the next row's bundle.
        donor = shifted[row]
        foreign = sorted([k for k in log if k[0] == donor])
        ventries = []
        for key in foreign[:MAX_ARTIFACTS]:
            rec = log[key]
            body = ""
            if rec["has_text"]:
                with open(rec["path"]) as fh:
                    body = fh.read(CHARS)
            ventries.append({
                "corpus": rec["corpus"],
                "artifact": rec["artifact"],
                "documentation_path": rec["path"] if rec["has_text"] else None,
                "documentation_shown": body,
            })
        view.append({
            "row": row,
            "pairing": "mismatched_with",
            "mismatched_with": donor,
            "story_title": None,
            "requirement_text": req["requirement_text"],
            "step_a": {k: att[k] for k in
                       ("category", "attribute", "attribute_stated",
                        "attribute_note")},
            "artifacts_shown": ventries,
            "artifacts_named_but_not_shown": None,
        })

    out = os.path.join(RAW, "view_b_%s.json" % args.reader)
    with open(out, "w") as fh:
        json.dump({
            "schema": "origin.e028-step-b-view/1",
            "reader": args.reader,
            "fit_rows": fit,
            "mismatched_control_rule": "row i is paired with row (i+1) mod n",
            "max_artifacts_per_bundle": MAX_ARTIFACTS,
            "chars_per_artifact": CHARS,
            "declared_positive_control_row": "H03",
            "view": view,
        }, fh, indent=1)
    chars = sum(len(a.get("documentation_shown") or "")
                for v in view for a in v["artifacts_shown"])
    print(json.dumps({
        "view": out,
        "fit_rows": len(fit),
        "view_entries": len(view),
        "documentation_chars_in_view": chars,
        "rows_whose_first_four_named_artifacts_all_lack_text": sorted(
            {r["row"] for r in read_jsonl(os.path.join(RAW, "fetch_log.jsonl"))
             if not r["has_text"]} & set(fit)),
    }, indent=2))


if __name__ == "__main__":
    main()