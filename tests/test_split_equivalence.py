#!/usr/bin/env python3
"""Verify the doc-lint line-cap split of three experiment classifiers.

The three `classify.py` files on the stopped view-count line exceeded the
repository's 300-line cap, and the repair was to move coherent sections into
sibling modules (`vocab.py`, `stats.py`, `classify_core.py`, `harvest.py`).
This checks the only property that matters for an experiment record: **the
refactor changed no classification.**

Each side is loaded in its own subprocess, because all three directories carry
sibling modules of the same name and importing two of them in one interpreter
would have the second silently receive the first's `vocab` (this happened, and
is why the comparison is not written as an in-process import).

Run: `python3 tests/test_split_equivalence.py`  (or via unittest discover)

Ceiling, stated: `EXPERIMENTS/*/raw/` is gitignored except for a few suffixes,
and two of these three experiments committed none, so most probes are built
from each classifier's own vocabulary rather than from a harvested population.
This proves the refactor moved code without moving behaviour over the strings
the classifier is built around; it is not a population-level equivalence proof.
"""

import ast
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
HERE = os.path.dirname(os.path.abspath(__file__))

# Blob ids of each `classify.py` **as committed before the split**. Pinned by id
# rather than read from HEAD, so the comparison cannot go vacuous the moment the
# refactor itself is committed.
PRE_SPLIT_BLOBS = {
    "116-viewcount-classifier-prototype": "929dc3577cba2c28a07beb63f1e58635bb33f2d0",
    "118-pypi-viewcount-matched-harvest": "dc53115592b5361cd0400b05fed979ff2eb8d48b",
    "119-hexpm-viewcount-matched-harvest": "a32bea6f2e2a851c14034946f15b576ccce5cb29",
}
EXPERIMENTS = sorted(PRE_SPLIT_BLOBS)
SIBLINGS = ("vocab.py", "stats.py", "classify_core.py", "harvest.py")

WORKER = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import classify
probes = json.load(open(sys.argv[2]))
out = []
for description in probes:
    row = None
    for fn in ("classify_description", "classify_repo"):
        f = getattr(classify, fn, None)
        if f is None:
            continue
        try:
            row = [fn, repr(f(description))]
        except TypeError:
            try:
                row = [fn, repr(f("pkg", description))]
            except Exception as exc:
                row = [fn, "raised %s: %s" % (type(exc).__name__, exc)]
        except Exception as exc:
            row = [fn, "raised %s: %s" % (type(exc).__name__, exc)]
        break
    out.append(row)
json.dump(out, open(sys.argv[3], "w"))
'''


def _vocab_words(expdir, name):
    """Read a vocabulary set out of the refactored `vocab.py` without importing."""
    path = os.path.join(ROOT, "EXPERIMENTS", expdir, "vocab.py")
    with open(path) as fh:
        tree = ast.parse(fh.read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", None) == name for t in node.targets):
            value = ast.literal_eval(node.value)
            return list(value) if isinstance(value, (set, list, tuple)) else list(value)
    return []


def _harvested_descriptions(expdir):
    out = []
    raw = os.path.join(ROOT, "EXPERIMENTS", expdir, "raw")
    for dirpath, _dirs, files in os.walk(raw):
        for fname in files:
            if not fname.endswith(".json"):
                continue
            try:
                with open(os.path.join(dirpath, fname)) as fh:
                    rows = json.load(fh)
            except ValueError:
                continue
            if isinstance(rows, dict):
                rows = rows.get("results") or rows.get("packages") or []
            for row in rows if isinstance(rows, list) else []:
                if isinstance(row, dict) and row.get("description"):
                    out.append(row["description"])
    return out


def _probes(expdir):
    """Real descriptions first, then every vocabulary term alone, in a sentence,
    and glued to its neighbour -- the classifier disambiguates on a token
    window, so a probe set that never puts two terms together would not
    exercise the part most likely to move."""
    probes = list(_harvested_descriptions(expdir))
    need = _vocab_words(expdir, "NEED_INDICATORS")
    generic = _vocab_words(expdir, "GENERIC_TERMS")
    for word in need:
        probes += ["A library to %s your project." % word,
                   "%s helper for production use" % word,
                   "the word %s appears here" % word]
    for word in generic:
        probes += ["utility %s module" % word, "%s only, nothing else" % word]
    for i, word in enumerate(need):
        probes.append("%s and %s together in one library" % (word, need[(i + 1) % len(need)]))
    for i, word in enumerate(generic):
        probes.append("%s %s package for everyday work" % (word, generic[(i + 1) % len(generic)]))
    probes += ["", "   ", "a" * 500, "utility: tool for parse and format",
               "AI email database base cache parse", "Ünïcodé prøbe ﬁle", "12345", "!!!???"]
    return probes


def _run_side(directory, probes, worker_dir):
    """Execute the worker against `directory`, isolated from every other one."""
    worker = os.path.join(worker_dir, "worker.py")
    if not os.path.exists(worker):
        with open(worker, "w") as fh:
            fh.write(WORKER)
    probes_path = os.path.join(worker_dir, "probes.json")
    out_path = os.path.join(worker_dir, "out.json")
    with open(probes_path, "w") as fh:
        json.dump(probes, fh)
    proc = subprocess.run([sys.executable, worker, directory, probes_path, out_path],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise AssertionError("worker failed on %s:\n%s" % (directory, proc.stderr.decode("utf-8", "replace")))
    with open(out_path) as fh:
        return json.load(fh)


def _pre_split_dir(expdir, target):
    """The pre-split blob plus the current siblings, in a directory of its own."""
    text = subprocess.check_output(["git", "-C", ROOT, "cat-file", "blob", PRE_SPLIT_BLOBS[expdir]])
    for sibling in SIBLINGS:
        src = os.path.join(ROOT, "EXPERIMENTS", expdir, sibling)
        if os.path.exists(src):
            with open(src) as fh:
                body = fh.read()
            with open(os.path.join(target, sibling), "w") as fh:
                fh.write(body)
    with open(os.path.join(target, "classify.py"), "wb") as fh:
        fh.write(text)


class SplitEquivalence(unittest.TestCase):
    def test_refactor_changed_no_classification(self):
        for expdir in EXPERIMENTS:
            probes = _probes(expdir)
            self.assertGreaterEqual(len(probes), 100, expdir)
            worker_dir = tempfile.mkdtemp(prefix="split-eq-worker-")
            old_dir = tempfile.mkdtemp(prefix="split-eq-old-")
            _pre_split_dir(expdir, old_dir)
            new_dir = os.path.join(ROOT, "EXPERIMENTS", expdir)

            old = _run_side(old_dir, probes, worker_dir)
            new = _run_side(new_dir, probes, worker_dir)
            self.assertEqual(len(old), len(new))
            compared = 0
            for description, before, after in zip(probes, old, new):
                compared += 1
                self.assertEqual(before, after,
                                 "%s differs on %r\n  pre-split %r\n  refactored %r"
                                 % (expdir, description[:70], before, after))
            self.assertEqual(compared, len(probes))
            sys.stderr.write("%s: %d probes identical\n" % (expdir, compared))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":  # pragma: no cover
        exec(WORKER)
    unittest.main(verbosity=2)