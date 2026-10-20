"""R1, R2 and R3 on a run's own emitted bytes.

R1 recomputes each headline rate from the *inputs the run shipped* and compares
it to the printed aggregate, under AMENDMENT-1 and AMENDMENT-2 section A1. It
never reads a verdict column to do it. Where the run ships its own metric
function -- lm-eval puts ``process_results`` in ``results.json`` as source text
-- that shipped source is executed, so the recomputation uses the run's own
definition rather than a reimplementation of it. Where the run ships only a YAML
config, the generic path is reimplemented from
``lm_eval/api/task.py::ConfigurableTask.process_results`` and the source lines
are cited in ``REIMPLEMENTED`` below.

R2 compares the aggregate's declared row count to the rows actually shipped.
R3 asks whether every reported metric has a per-row column behind it.

Standard library only. Nothing here imports preflight: these are measurements
beside the gates, not gates.
"""

import glob
import json
import math
import os
import re

#: The generic metric path of ``ConfigurableTask.process_results``, which
#: lm-eval does *not* ship in results.json. Cited so a reader can check the
#: reimplementation: ``lm_eval/api/task.py`` multiple_choice branch --
#: ``acc = 1.0 if np.argmax(results) == gold``,
#: ``completion_len = [float(len(c)) for c in doc_to_choice(doc)]``,
#: ``acc_norm = 1.0 if np.argmax(results / completion_len) == gold``;
#: and ``lm_eval/api/metrics.py`` -- ``mean``, ``sample_stddev / sqrt(n)``,
#: ``weighted_mean = sum(a)/sum(b)``, ``weighted_perplexity = exp(-wm)``,
#: ``bits_per_byte = -wm / log(2)``.
REIMPLEMENTED = "lm_eval/api/task.py::ConfigurableTask.process_results, multiple_choice branch"

#: A metric ending in this suffix is an aggregate-only quantity by
#: construction. AMENDMENT-2 section A3 states the carve-out; the keys are
#: still reported, separately, rather than dropped.
STDERR_SUFFIX = "_stderr"

#: A task that ships this key in its config ships its own metric function as
#: source text, and R1 executes it instead of reimplementing it.
SHIPPED_METRIC_SOURCE = "process_results"

#: lm-eval appends its ISO run date to a sample filename.
_DATE_SUFFIX = re.compile(r"_\d{4}-\d{2}-\d{2}T[\d:.+-]+$")

#: Fields a run ships through ``lm_eval/utils.py::sanitize_list``, which
#: "recursively converts all inner component to strings". R1 must coerce these
#: back to float to read the metric's own input, and the run declares that
#: coercion nowhere. For IEEE-754 doubles Python's ``str`` round-trips exactly,
#: so the coercion is lossless here -- but it is *undeclared*, and it is the
#: same shape as F121, where a coercion made a join match nothing. Recorded so
#: the claim is scoped to what was observed rather than to loss in general.
SANITIZED_FIELDS = ("resps", "filtered_resps", "word_perplexity",
                    "byte_perplexity", "bits_per_byte")


def _num(value):
    """Read a shipped score. ``sanitize_list`` made it a string."""
    return float(value) if isinstance(value, str) else value


def _tol(printed, recomputed):
    """Relative tolerance for float agreement: 1e-9, well inside double noise."""
    if printed is None or isinstance(printed, str):
        return False
    scale = max(1.0, abs(printed))
    return abs(printed - recomputed) <= 1e-9 * scale


def _gold(row):
    """The row's label as an integer, from the shipped string target."""
    return int(row["target"])


def _choices(doc, config):
    """``doc_to_choice`` applied to a shipped doc, for the acc_norm lengths.

    Three forms are shipped in the wild and each is exact, so each is implemented
    rather than approximated. Anything else raises: a guessed denominator turns
    R1 into a number that agrees with nothing and means less than a refusal.
    """
    spec = config["doc_to_choice"]
    if spec == "{{choices.text}}":
        return doc["choices"]["text"]
    if spec == "{{[sol1, sol2]}}":
        return [doc["sol1"], doc["sol2"]]
    if isinstance(spec, list) and all(isinstance(text, str) for text in spec):
        # A literal list of constants, e.g. JailbreakBench's SGXSTest
        # ``['safe', 'unsafe']``. The choice text does not vary by row, so its
        # length does not either.
        return list(spec)
    raise KeyError("doc_to_choice %r not implemented; refusing to guess" % (spec,))


def recompute_multiple_choice(rows, config, metric):
    """R1 for one multiple-choice task, from shipped inputs only."""
    per_row = []
    for row in rows:
        lls = [_num(pair[0]) for pair in row["filtered_resps"]]
        if metric == "acc_norm":
            lls = [ll / float(len(choice))
                   for ll, choice in zip(lls, _choices(row["doc"], config))]
        pred = max(range(len(lls)), key=lambda i: lls[i])
        per_row.append(1.0 if pred == _gold(row) else 0.0)
    return sum(per_row) / len(per_row), per_row


def recompute_shipped_process_results(rows, config, metric):
    """R1 where the run ships its own metric function as source text."""
    namespace = {"re": re}
    exec(config[SHIPPED_METRIC_SOURCE], namespace)  # noqa: S102 -- the run's own source
    fn = namespace[SHIPPED_METRIC_SOURCE]
    pairs = []
    for row in rows:
        # A loglikelihood_rolling task issues one request per row, so its
        # ``filtered_resps`` is ``[ll]``, not the multiple-choice ``[[ll, cont]]``.
        loglikelihood = _num(row["filtered_resps"][0])
        value = fn(row["doc"], (loglikelihood,))[metric]
        pairs.append([_num(value[0]), _num(value[1])])
    total = sum(pair[0] for pair in pairs)
    weight = sum(pair[1] for pair in pairs)
    weighted = total / weight
    if metric == "bits_per_byte":
        return -weighted / math.log(2), pairs
    return math.exp(-weighted), pairs


def check_r1(results, rows_by_task, config_by_task):
    """Compare every printed rate with a recomputation from shipped inputs."""
    out = []
    for task in sorted(results["results"]):
        printed = results["results"][task]
        if task not in config_by_task:
            out.append({"task": task, "metric": "*", "status": "NO_CONFIG_IN_RUN",
                        "printed": {k: printed[k] for k in sorted(printed)}})
            continue
        config = config_by_task[task]
        rows = rows_by_task.get(task, [])
        for key in sorted(printed):
            metric = key.split(",")[0]
            if metric == "alias" or metric.endswith(STDERR_SUFFIX):
                continue
            if not rows:
                out.append({"task": task, "metric": metric, "status": "NO_ROWS",
                            "printed": printed[key]})
                continue
            if SHIPPED_METRIC_SOURCE in config:
                recomputed, _ = recompute_shipped_process_results(rows, config, metric)
                source = "run's own shipped process_results"
            else:
                recomputed, per_row = recompute_multiple_choice(rows, config, metric)
                source = REIMPLEMENTED
            agreement = _tol(printed[key], recomputed)
            entry = {"task": task, "metric": metric, "printed": printed[key],
                     "recomputed": recomputed, "source": source,
                     "n_rows": len(rows), "agrees": agreement}
            if metric in ("acc", "acc_norm") and SHIPPED_METRIC_SOURCE not in config:
                shipped = [row.get(metric) for row in rows]
                absent = [r["doc_id"] for r, v in zip(rows, shipped) if v is None]
                entry["rows_missing_the_verdict_column"] = absent
                present = [v for v in shipped if v is not None]
                if present and not absent:
                    entry["shipped_verdict_column_mean"] = sum(present) / len(present)
                    entry["recomputation_matches_verdict_column"] = _tol(
                        entry["shipped_verdict_column_mean"], recomputed)
            out.append(entry)
    return out


def check_r2(results, rows_by_task):
    """Declared row count against rows actually shipped."""
    out = []
    for task in sorted(results["n-samples"]):
        declared = results["n-samples"][task]["effective"]
        shipped = len(rows_by_task.get(task, []))
        out.append({"task": task, "declared_effective": declared,
                    "shipped_rows": shipped, "agrees": declared == shipped})
    return out


def check_r3(results, rows_by_task, config_by_task):
    """Every reported metric: is there a per-row column behind it?"""
    out = []
    for task in sorted(results["results"]):
        rows = rows_by_task.get(task, [])
        if task not in config_by_task:
            out.append({"task": task, "metric": "*", "per_row_column": False,
                        "declared_in_metric_list": False,
                        "status": "NO_CONFIG_IN_RUN"})
            continue
        declared = [m["metric"] for m in config_by_task[task]["metric_list"]]
        stderr_keys = []
        for key in sorted(results["results"][task]):
            metric = key.split(",")[0]
            if metric == "alias":
                continue
            if metric.endswith(STDERR_SUFFIX):
                stderr_keys.append(key)
                continue
            present = any(metric in row for row in rows)
            out.append({"task": task, "metric": metric,
                        "per_row_column": present,
                        "declared_in_metric_list": metric in declared,
                        "status": "OK" if present else "NO_PER_ROW_COLUMN"})
    return out, stderr_keys


def aggregation_notes(results, config_by_task):
    """Which metrics the run reports without declaring how they are aggregated.

    Not a gate. An observed property of the shipped config, recorded because it
    decides whether a third party holding ``results/`` can recompute anything at
    all without reading the harness's source.
    """
    notes = []
    for task in sorted(results["results"]):
        if task not in config_by_task:
            continue
        declared = {m["metric"]: m.get("aggregation")
                    for m in config_by_task[task]["metric_list"]}
        for key in sorted(results["results"][task]):
            metric = key.split(",")[0]
            if metric == "alias" or metric.endswith(STDERR_SUFFIX):
                continue
            if metric in declared and not declared[metric]:
                notes.append({"task": task, "metric": metric,
                              "aggregation_in_shipped_config": None,
                              "reported_value": results["results"][task][key]})
    return notes


def load_rows(outdir):
    """``{task: [shipped row, ...]}`` straight off the samples files."""
    rows_by_task = {}
    for path in sorted(glob.glob(os.path.join(outdir, "**", "samples_*.jsonl"),
                                 recursive=True)):
        name = os.path.basename(path)
        task = _DATE_SUFFIX.sub("", name[len("samples_"):-len(".jsonl")])
        with open(path) as handle:
            rows_by_task[task] = [json.loads(line) for line in handle if line.strip()]
    return rows_by_task


def load_results(outdir):
    """The one ``results_*.json`` a run wrote."""
    paths = sorted(glob.glob(os.path.join(outdir, "**", "results_*.json"),
                             recursive=True))
    if not paths:
        raise SystemExit("no results_*.json under %s" % outdir)
    with open(paths[-1]) as handle:
        return json.load(handle)


def coverage_notes(results, rows_by_task):
    """Which reported tasks this directory can and cannot be checked on.

    A published run output usually ships the aggregate for every task and the
    per-row file for some of them. The two sets differing is an ordinary fact
    about how run directories are published, not a defect in the run, so it is
    recorded as a denominator rather than as a finding: without it a rate over
    the tasks that happen to have rows reads as a rate over the run.
    """
    reported = set(results["results"])
    configured = set(results.get("configs", {}))
    shipped = set(rows_by_task)
    return {
        "tasks_reporting_a_number": len(reported),
        "tasks_with_a_config": len(configured),
        "tasks_with_per_row_file": len(shipped),
        "reported_with_no_config": sorted(reported - configured),
        "reported_with_no_per_row_file": sorted(reported - shipped),
        "per_row_file_without_a_number": sorted(shipped - reported),
    }


def run(outdir):
    """R1, R2 and R3 for one run directory."""
    results = load_results(outdir)
    rows_by_task = load_rows(outdir)
    configs = results["configs"]
    r3, stderr_keys = check_r3(results, rows_by_task, configs)
    return {
        "outdir": outdir,
        "tasks": sorted(rows_by_task),
        "R1_row_recomputation": check_r1(results, rows_by_task, configs),
        "R2_row_count": check_r2(results, rows_by_task),
        "R3_metric_presence": r3,
        "R3_stderr_keys_carved_out": stderr_keys,
        "aggregation_not_declared_in_config": aggregation_notes(results, configs),
        "coverage": coverage_notes(results, rows_by_task),
    }
