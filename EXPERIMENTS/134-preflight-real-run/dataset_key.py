"""The load-bearing key side for C1 on lm-eval output: the dataset the run names.

Declared in AMENDMENT-2 section A2. **Not** stdlib-only: it reads Arrow files
because Arrow is the format the run itself read, so the key side comes from the
same bytes the harness used. It is a separate module from ``lm_eval_adapter`` on
purpose, so the adapter's stdlib ceiling (G2) is still measured as declared and
this dependency is visible rather than smuggled into the counted tax.

The question this makes C1 ask is the useful one: *do the identifiers and
targets a run shipped actually name the rows of the dataset that run says it
evaluated?*

One thing the run does not record is which split it evaluated. ``results.json``
names all three splits (``training_split``, ``validation_split``,
``test_split``) and records the row count of the one it chose as
``n-samples[task]["original"]``, but records no field saying which. So the split
is *resolved by matching that count*, and an ambiguous or unresolvable match is
reported rather than guessed -- ``resolve_split`` returns a list of candidates,
not a choice.
"""

import glob
import os
import re

import pyarrow.ipc as ipc
import pyarrow as pa

#: Keys under ``results.json -> configs[task]`` that name a split.
SPLIT_KEYS = ("training_split", "validation_split", "test_split")


def _target(doc, config):
    """The target lm-eval's own ``doc_to_target`` yields for this dataset row.

    Dispatch is on the *declared* spec, never on a guess about the dataset. Three
    forms are shipped in the wild and each is exact:

    * Python source -- lm-eval ships a task's ``doc_to_target`` body verbatim when
      the task defines one (``wikitext`` detokenizes its page), so the run's own
      source is executed here rather than a reimplementation of it.
    * ``label`` -- the plain column name.
    * ``{{choices.label.index(answerKey.lstrip())}}`` -- a letter naming
      ``choices.label``, which is the integer the multiple-choice scorer wants.

    Anything else raises. A key side built by guessing is the F121 shape: a join
    that matches nothing and reads as a defect in the run.
    """
    spec = config["doc_to_target"]
    if isinstance(spec, str) and spec.lstrip().startswith("def "):
        namespace = {"re": re}
        exec(spec, namespace)  # noqa: S102 -- the run's own shipped source
        return namespace["wikitext_detokenizer"](doc)
    if spec == "label":
        return int(doc["label"])
    if spec == "{{choices.label.index(answerKey.lstrip())}}":
        return doc["choices"]["label"].index(doc["answerKey"].lstrip())
    raise KeyError("doc_to_target %r not implemented; refusing to guess" % (spec,))


def _choice_lengths(doc):
    """Character length of each choice, the ``acc_norm`` denominator."""
    if "choices" in doc and isinstance(doc["choices"], dict):
        return [float(len(text)) for text in doc["choices"]["text"]]
    if "sol1" in doc:
        return [float(len(doc["sol1"])), float(len(doc["sol2"]))]
    raise KeyError("no choices in this row: %r" % sorted(doc))


def read_split(cache_dir, dataset_path, dataset_name, split):
    """Read one split of one dataset out of the Hugging Face Arrow cache."""
    stem = dataset_path.replace("/", "___")
    pattern = os.path.join(cache_dir, stem, dataset_name or "*", "*", "*",
                           "%s-%s.arrow" % (stem.split("___")[-1], split))
    paths = sorted(glob.glob(pattern))
    if not paths:
        raise SystemExit("no arrow file for %s/%s split %r under %s"
                         % (dataset_path, dataset_name, split, cache_dir))
    with pa.memory_map(paths[-1], "rb") as source:
        return ipc.open_stream(source).read_all().to_pylist()


def resolve_split(cache_dir, config, n_samples):
    """Which split did this run evaluate? Return every split whose size matches.

    Returning a list is the point: the run does not say, so a reader who picks
    one of two equal-sized splits has made an assumption, and this module does
    not make it silently.
    """
    matches = []
    for key in SPLIT_KEYS:
        split = config.get(key)
        if not split:
            continue
        rows = read_split(cache_dir, config["dataset_path"],
                          config.get("dataset_name"), split)
        if len(rows) == n_samples:
            matches.append((key, split, rows))
    return matches


def build_key_rows(cache_dir, results, task):
    """``key_rows`` for one task, from the dataset the run names for it.

    lm-eval's ``doc_iterator`` is ``enumerate(eval_docs)``, so the dataset row
    index **is** the ``doc_id`` the run shipped. That mapping is the whole
    adapter tax on this side, and it is why the check can fail: if the shipped
    ``doc_id`` were not the enumeration index, or the shipped ``target`` were
    not the row's label, nothing would match.
    """
    config = results["configs"][task]
    n_samples = results["n-samples"][task]["original"]
    candidates = resolve_split(cache_dir, config, n_samples)
    report = {
        "task": task,
        "dataset_path": config["dataset_path"],
        "dataset_name": config.get("dataset_name"),
        "n_samples_original": n_samples,
        "declared_splits": {k: config[k] for k in SPLIT_KEYS if k in config},
        "eval_split_declared_in_results": None,
        "eval_split_resolved_by_row_count": None,
        "split_candidates": [{"field": f, "split": s} for f, s, _ in candidates],
    }
    if len(candidates) != 1:
        report["split_resolution"] = ("AMBIGUOUS" if candidates else "UNRESOLVED")
        return [], report
    field, split, rows = candidates[0]
    report["split_resolution"] = "UNIQUE"
    report["eval_split_resolved_by_row_count"] = split
    report["eval_split_field"] = field
    rows = rows[:results["n-samples"][task]["effective"]]
    key_rows = [{"task": task, "doc_id": index, "target": str(_target(doc, config))}
                for index, doc in enumerate(rows)]
    report["key_rows"] = len(key_rows)
    return key_rows, report
