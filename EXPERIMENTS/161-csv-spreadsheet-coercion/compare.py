#!/usr/bin/env python3
"""E161 instrument test: does csvsafe's prediction match what the engine did?

Reads the engine's own cell-level changes (changes.tsv) and csvsafe's
independent prediction for the same cells, and reports precision and recall for
two questions:

  would-change : does the checker flag the cells an engine actually altered?
  damaging     : does it flag the damaging subset, and does it call anything
                 damaging that the engine left alone?

Also reports the disagreements, because a rule that fires on the wrong cells is
worth as much as a rule that fires on none.
"""
import collections
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csvsafe import classify, DAMAGING  # noqa: E402


def engine_changes(path):
    out = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            out[(row["file"], int(row["row"]), int(row["col"]))] = row
    return out


def compare(corpus, changes, limit_files=None):
    actual = engine_changes(changes)
    files = sorted(f for f in os.listdir(corpus) if f.endswith(".csv"))
    if limit_files:
        files = files[:limit_files]
    tp = fp = fn = tn = 0
    dmg_tp = dmg_fp = dmg_fn = 0
    misses = collections.Counter()
    false_alarms = collections.Counter()
    per_file = []
    for name in files:
        f_tp = f_fp = f_fn = 0
        with open(os.path.join(corpus, name), encoding="utf-8",
                  errors="replace", newline="") as f:
            for ri, row in enumerate(csv.reader(f)):
                for ci, cell in enumerate(row):
                    if cell == "":
                        continue
                    rule, harm = classify(cell)
                    predicted = rule is not None
                    hit = actual.get((name, ri, ci))
                    really = hit is not None
                    if predicted and really:
                        tp += 1
                        f_tp += 1
                    elif predicted and not really:
                        fp += 1
                        f_fp += 1
                        false_alarms[(rule, cell[:24])] += 1
                    elif really and not predicted:
                        fn += 1
                        f_fn += 1
                        misses[(hit["rule"], hit["source"][:24])] += 1
                    else:
                        tn += 1
                    if really:
                        eng_harm = hit["rule"] in ("leading_zero", "precision_loss",
                                                   "datetime_time_lost",
                                                   "formula_executed")
                        if harm and eng_harm:
                            dmg_tp += 1
                        elif harm and not eng_harm:
                            dmg_fp += 1
                            false_alarms[("DAMAGING-FP", cell[:24])] += 1
                        elif eng_harm and not harm:
                            dmg_fn += 1
                            misses[("DAMAGING-FN", hit["source"][:24])] += 1
        per_file.append({"file": name, "tp": f_tp, "fp": f_fp, "fn": f_fn})
    return {
        "engine_changes": tp + fn,
        "checker_flags": tp + fp,
        "precision": round(tp / float(tp + fp), 4) if tp + fp else None,
        "recall": round(tp / float(tp + fn), 4) if tp + fn else None,
        "damaging_precision": round(dmg_tp / float(dmg_tp + dmg_fp), 4) if dmg_tp + dmg_fp else None,
        "damaging_recall": round(dmg_fn and dmg_tp / float(dmg_tp + dmg_fn), 4) if dmg_tp + dmg_fn else None,
        "damaging_true_positives": dmg_tp,
        "damaging_false_positives": dmg_fp,
        "damaging_false_negatives": dmg_fn,
        "top_misses": misses.most_common(12),
        "top_false_alarms": false_alarms.most_common(12),
        "per_file": per_file,
    }


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    frames = sys.argv[1:] or ["controls", "corpus", "corpus-govuk", "corpus-census"]
    out = {}
    for f in frames:
        out[f] = compare(os.path.join(here, f), os.path.join(here, "changes-%s.tsv" % f))
        out[f]["cells_ok"] = None
        print("%-16s engine=%-7d checker=%-7d precision=%-6s recall=%-6s "
              "dmg P=%-6s R=%-6s (%d/%d/%d)"
              % (f, out[f]["engine_changes"], out[f]["checker_flags"],
                 out[f]["precision"], out[f]["recall"],
                 out[f]["damaging_precision"], out[f]["damaging_recall"],
                 out[f]["damaging_true_positives"], out[f]["damaging_false_positives"],
                 out[f]["damaging_false_negatives"]))
    with open(os.path.join(here, "instrument-test.json"), "w") as f:
        json.dump(out, f, indent=2, sort_keys=True, default=str)