"""Adapter for `EleutherAI/lm-evaluation-harness` v0.4.4 run output.

Reads ONLY the bytes a run emitted: ``results_*.json`` and ``samples_*.jsonl``
under one output directory. Returns ``(key_rows, out_rows)`` for
``preflight.concordance``.

    from lm_eval_adapter import adapt_lm_eval
    key_rows, out_rows = adapt_lm_eval("/path/to/output_path")

G2 counts the adapter tax. Per the convention the other four adapters use,
*reading JSON and JSON-Lines is free* -- ``json.load`` and a line loop are the
generic loader. What is counted is the schema mapping, and it is the 6 lines of
``_identity`` plus ``_verdict`` below: which shipped fields are the identity,
and which are the verdict.

This adapter is deliberately **emitted-files-only**, so on a
``--log_samples`` run both sides of the C1 join come out of the same file and
the check cannot fail. That vacuity is measured and reported by
``run_e134.py`` rather than left implicit; the load-bearing key side is built by
``dataset_key.py`` under AMENDMENT-2 section A2.
"""

import glob
import json
import os
import re

#: Shipped fields that are the verdict. lm-eval's ``metric_list`` for a
#: multiple-choice task is exactly ``acc`` and ``acc_norm``; a loglikelihood
#: task such as ``wikitext`` ships none of these and its rows are scored by a
#: rolling aggregate instead.
VERDICT_FIELDS = ("acc", "acc_norm")

#: The date the harness appends to a sample filename, e.g.
#: ``samples_piqa_2026-10-14T00-52-55.068909.jsonl``. A task name may itself
#: contain underscores, so the date is stripped by pattern and not by position.
_DATE_SUFFIX = re.compile(r"_\d{4}-\d{2}-\d{2}T[\d:.+-]+$")


def _identity(task, row):
    """Counted schema mapping, key side: what the run says it evaluated."""
    return {"task": task, "doc_id": row["doc_id"], "target": row["target"]}


def _verdict(identity, row):
    """Counted schema mapping, output side: identity plus what it scored."""
    rec = dict(identity)
    for field in VERDICT_FIELDS:
        if field in row:
            rec[field] = row[field]
    return rec


def _sample_files(outdir):
    """Every ``samples_<task>_<date>.jsonl`` a run wrote, with its task name."""
    pattern = os.path.join(outdir, "**", "samples_*.jsonl")
    for path in sorted(glob.glob(pattern, recursive=True)):
        name = os.path.basename(path)
        stem = name[len("samples_"):-len(".jsonl")]
        yield _DATE_SUFFIX.sub("", stem), path


def load_results(outdir):
    """The one ``results_*.json`` a run wrote, by glob rather than by filename."""
    paths = sorted(glob.glob(os.path.join(outdir, "**", "results_*.json"),
                             recursive=True))
    if not paths:
        raise SystemExit("no results_*.json under %s" % outdir)
    with open(paths[-1]) as handle:
        return json.load(handle)


def adapt_lm_eval(outdir):
    """Return ``(key_rows, out_rows)`` for one run's emitted output.

    ``key_rows``: one ``{"task", "doc_id", "target"}`` per shipped row.
    ``out_rows``: the same identity plus whatever verdict columns the run
    shipped for that task.
    """
    key_rows, out_rows = [], []
    for task, path in _sample_files(outdir):
        with open(path) as handle:
            for line in handle:
                if line.strip():
                    row = json.loads(line)
                    identity = _identity(task, row)
                    key_rows.append(identity)
                    out_rows.append(_verdict(identity, row))
    return key_rows, out_rows
