#!/usr/bin/env python3
"""E134 driver -- preflight's three checks, and R1/R2/R3, on a real foreign run.

    python3 run_e134.py --armA <dir> --cache <hf cache> --armB <dir> --out results.json

Arm A is a run of ``EleutherAI/lm-evaluation-harness`` v0.4.4 produced by this
experiment. Arm B is a run output published by a third party. Arms C are copies
of Arm A's bytes with one defect each; the originals are never modified.

Nothing here is imported by ``preflight``. These are measurements beside the
gates, and ``preflight`` is pointed at the same bytes through the same adapter
so its verdicts can be read next to them.
"""

import argparse
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

from preflight import alternate_form_fp, concordance, wilson  # noqa: E402

import recompute  # noqa: E402
from dataset_key import build_key_rows  # noqa: E402
from lm_eval_adapter import adapt_lm_eval  # noqa: E402

#: C2 needs a flagger. On third-party output the only thing the run's own bytes
#: label independently is the verdict recomputed from its shipped inputs, so the
#: correct arm is well defined without the author. The flagger class available
#: against that arm is the abstention rule: flag a row whose winning loglikelihood
#: beats the runner-up by less than ``tau`` nats. Swept rather than fixed at one
#: number, because a single threshold would be a choice made after the result.
MARGIN_TAUS = (0.0, 0.05, 0.1, 0.25, 0.5, 1.0)


def _rows_by_task(outdir):
    return recompute.load_rows(outdir)


def _verdicts(rows, config):
    """``{doc_id: (acc, acc_norm)}`` recomputed from shipped inputs only."""
    out = {}
    for row in rows:
        per = {}
        for metric in ("acc", "acc_norm"):
            value, _ = recompute.recompute_multiple_choice([row], config, metric)
            per[metric] = round(value, 6)
        out[row["doc_id"]] = per
    return out


def _margin(row):
    """Winning minus runner-up loglikelihood, in nats."""
    lls = [recompute._num(pair[0]) for pair in row["filtered_resps"]]
    lls.sort(reverse=True)
    return lls[0] - lls[1] if len(lls) > 1 else float("inf")


def c2_foreign(rows, config):
    """C2 on foreign bytes: margin-abstention flagged against a recomputed arm.

    ``correct`` is labelled by recomputing the verdict from ``filtered_resps``,
    the ``target`` and the choice texts -- never by reading ``acc``. So the two
    arms are independent of the column the flagger never touches.
    """
    verdicts = _verdicts(rows, config)
    items = []
    for row in rows:
        shipped = recompute._num(row.get("acc"))
        correct = shipped is not None and abs(shipped - verdicts[row["doc_id"]]["acc"]) < 1e-9
        items.append({
            "arm": "multiple_choice",
            "value": "doc_id=%s" % row["doc_id"],
            "correct": correct,
            "margin": _margin(row),
            "shipped_acc": shipped,
        })
    out = []
    for tau in MARGIN_TAUS:
        def flagger(item, tau=tau):
            return "flagged" if item["margin"] < tau else "right"
        out.append(alternate_form_fp(items, flagger, fp_ceiling=0.02))
        out[-1]["tau"] = tau
        out[-1]["arms"]["multiple_choice"]["flag_rate_over_all_rows"] = round(
            sum(1 for i in items if i["margin"] < tau) / len(items), 4)
    return out, {"labelled_correct": sum(1 for i in items if i["correct"]),
                 "labelled_incorrect": sum(1 for i in items if not i["correct"]),
                 "n_rows": len(items)}


def _per_task_c1(armdir, cache):
    """C1 with the dataset side as key, per task, plus the split report.

    An adapter that raises is itself a result, so the failure is recorded in the
    same shape as a verdict rather than propagated.
    """
    try:
        key_rows, out_rows = adapt_lm_eval(armdir)
    except Exception as exc:
        return {"verdict": "ADAPTER_RAISES", "per_task": None,
                "adapter_error": {"raised": type(exc).__name__, "message": str(exc)}}
    results = recompute.load_results(armdir)
    out = {}
    for task in sorted(results["configs"]):
        ds_rows, report = build_key_rows(cache, results, task)
        subset = [r for r in out_rows if r["task"] == task]
        check = concordance(ds_rows, subset)
        out[task] = {"split_report": report, "check": check,
                     "dataset_rows_built": len(ds_rows)}
    return {"verdict": "OK", "adapter_error": None, "per_task": out}


def _inject(outdir, dest):
    """Copy a run's bytes. Defects are injected into the copy, never the original."""
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(outdir, dest)
    return dest


def _defect_c1(outdir, dest):
    """Rename an identifier field on the output side of one task's samples file."""
    _inject(outdir, dest)
    target = [p for p in sorted(os.listdir(dest)) if p.startswith("samples_piqa")][0]
    path = os.path.join(dest, target)
    with open(path) as handle:
        rows = [json.loads(line) for line in handle if line.strip()]
    evidence = []
    for row in rows:
        evidence.append({"doc_id": row["doc_id"], "renamed_to": "sample_index"})
        row["sample_index"] = row.pop("doc_id")
    with open(path, "w") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")
    return {"defect": "C1 identifier field renamed on the output side",
            "file": target, "rows_touched": len(rows), "evidence": evidence}


def _defect_c2(outdir, dest):
    """Drop the verdict columns from the final shipped row of one task."""
    _inject(outdir, dest)
    target = [p for p in sorted(os.listdir(dest)) if p.startswith("samples_openbookqa")][0]
    path = os.path.join(dest, target)
    with open(path) as handle:
        rows = [json.loads(line) for line in handle if line.strip()]
    dropped = [k for k in ("acc", "acc_norm") if k in rows[-1]]
    for key in dropped:
        rows[-1].pop(key)
    with open(path, "w") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")
    return {"defect": "C2 verdict column dropped from the final row",
            "file": target, "doc_id": rows[-1]["doc_id"], "dropped_fields": dropped}


def _r3_strict(results, rows_by_task, configs):
    """R3 asked of every row rather than any row. Added after Arm C-2 fired."""
    out = []
    for task in sorted(results["results"]):
        rows = rows_by_task.get(task, [])
        for key in sorted(results["results"][task]):
            metric = key.split(",")[0]
            if metric == "alias" or metric.endswith(recompute.STDERR_SUFFIX):
                continue
            missing = sum(1 for row in rows if metric not in row)
            out.append({"task": task, "metric": metric, "rows": len(rows),
                        "rows_missing_the_column": missing,
                        "status": "OK" if missing == 0 else "PARTIAL_COLUMN"})
    return out


def _arm_summary(armdir):
    """R1/R2/R3 for one run directory, plus the controls run cannot supply."""
    results = recompute.load_results(armdir)
    rows_by_task = recompute.load_rows(armdir)
    configs = results["configs"]
    return {
        "R1_R2_R3": recompute.run(armdir),
        "R3_per_row_coverage": _r3_strict(results, rows_by_task, configs),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--armA", required=True)
    parser.add_argument("--cache", required=True)
    parser.add_argument("--armB", default=None)
    parser.add_argument("--tmp", default="/tmp/opencode/armC")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    report = {"experiment": "E134", "arms": {}, "controls": {}}

    armA_key, armA_out = adapt_lm_eval(args.armA)
    report["arms"]["A"] = _arm_summary(args.armA)
    report["arms"]["A"]["C1_vacuous_emitted_files_only"] = concordance(armA_key, armA_out)
    report["arms"]["A"]["C1_dataset_key_per_task"] = _per_task_c1(args.armA, args.cache)
    armA_results = recompute.load_results(args.armA)
    c2_out, c2_meta = c2_foreign(
        recompute.load_rows(args.armA)["piqa"], armA_results["configs"]["piqa"])
    report["arms"]["A"]["C2_margin_abstention_sweep"] = c2_out
    report["arms"]["A"]["C2_arm_sizes"] = c2_meta
    report["arms"]["A"]["C3_control_arm"] = {
        "verdict": "NOT_COMPUTABLE",
        "reason": ("the run declares no negative arm and no sham input. C3 asks "
                   "whether a negative arm is negative by evidence the key does not "
                   "use, and a single-model run of three public datasets has no "
                   "negative arm. Nothing here was substituted for it.")}
    report["arms"]["A"]["baseline_1_harness_own_checks"] = {
        "lm_eval_emits": ["results.json aggregate", "samples_*.jsonl per-row",
                          "task_hashes", "doc_hash/prompt_hash/target_hash per row"],
        "lm_eval_verifies": ["that its own printed table matches its own rows (arithmetic)"],
        "lm_eval_does_not": ["recompute a verdict from the model's responses and the "
                             "gold label", "check that a split was recorded",
                             "check that every shipped row carries the verdict it reports",
                             "compare against the dataset the run names"],
        "source": "read from the committed run's own results.json and from "
                  "lm_eval/api/task.py; no code path in the harness that performs "
                  "any of the four absent checks was found"}

    # Arms C: the falsification arm. Built from copies of Arm A's real bytes.
    c1dir = os.path.join(args.tmp, "c1-identifier-renamed")
    c2dir = os.path.join(args.tmp, "c2-verdict-dropped")
    c1meta = _defect_c1(args.armA, c1dir)
    c2meta = _defect_c2(args.armA, c2dir)
    c1_key, c1_out = None, None
    c1_error = None
    try:
        c1_key, c1_out = adapt_lm_eval(c1dir)
    except Exception as exc:  # the adapter names fields; a renamed field must not be silent
        c1_error = {"raised": type(exc).__name__, "message": str(exc)}
    c1_results = recompute.load_results(c1dir)
    c2_rows = recompute.load_rows(c2dir)
    report["arms"]["C"] = {
        "C1_defect": c1meta,
        "C1_adapter_path": {
            "error": c1_error,
            "verdict": "ADAPTER_RAISES" if c1_error else "OK",
            "note": ("a loud failure on the renamed field. The alternative would be "
                     "an adapter that skips an unknown field, which is what would "
                     "turn this defect into a clean 1.0000."),
            "C1_dataset_key_per_task": _per_task_c1(c1dir, args.cache),
            "C1_vacuous": concordance(c1_key, c1_out) if c1_out else None,
        },
        "C2_defect": c2meta,
        "C2_R1_R2_R3": _arm_summary(c2dir),
    }
    c2_flagger, c2_arm_sizes = c2_foreign(c2_rows["openbookqa"],
                                           c1_results["configs"]["openbookqa"])
    report["arms"]["C"]["C2_margin_at_tau_0.1"] = c2_flagger[2]
    report["arms"]["C"]["C2_arm_sizes"] = c2_arm_sizes

    if args.armB:
        report["arms"]["B"] = _arm_summary(args.armB)
        b_key, b_out = adapt_lm_eval(args.armB)
        report["arms"]["B"]["C1_vacuous_emitted_files_only"] = concordance(b_key, b_out)
        b_results = recompute.load_results(args.armB)
        b_rows = recompute.load_rows(args.armB)
        b_c2, b_sizes = c2_foreign(b_rows["SGXSTest"],
                                   b_results["configs"]["SGXSTest"])
        report["arms"]["B"]["C2_margin_abstention_sweep"] = b_c2
        report["arms"]["B"]["C2_arm_sizes"] = b_sizes
        report["arms"]["B"]["C3_control_arm"] = {
            "verdict": "NOT_COMPUTABLE",
            "reason": "no negative arm is declared in a published single-model run"}

    with open(args.out, "w") as handle:
        json.dump(report, handle, indent=1, sort_keys=True)
    print("wrote %s (%d bytes)" % (args.out, os.path.getsize(args.out)))
    print("R1 entries: %d, R2 entries: %d"
          % (len(report["arms"]["A"]["R1_R2_R3"]["R1_row_recomputation"]),
             len(report["arms"]["A"]["R1_R2_R3"]["R2_row_count"])))
    for entry in report["arms"]["A"]["R1_R2_R3"]["R1_row_recomputation"]:
        print("  R1 %-12s %-16s printed=%s recomputed=%s agrees=%s"
              % (entry["task"], entry["metric"], entry.get("printed"),
                 entry.get("recomputed"), entry.get("agrees")))


if __name__ == "__main__":
    main()
