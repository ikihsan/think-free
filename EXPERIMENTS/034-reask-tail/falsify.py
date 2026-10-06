"""E034 — the mutations that must break the checks in `check.py`. Split out at the
300-line cap: the checks and the things they are proved against are different artefacts
with different owners, and a single file makes it easy to weaken the checks while keeping
the mutations.

Each entry is (label, target|anchor, replacement); `label|module.py` names the file the
anchor lives in, because a mutation of one module cannot be caught by inspecting another.
`run(check)` copies the experiment's modules into a temp directory, applies each mutation
to its own target there, and re-runs the checks against the copy. A mutation that still
passes is a blind spot in `check.py` and is reported as such.
"""

import os
import shutil
import sys
import tempfile

import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
MODULES = ("reask.py", "harvest.py", "measures.py", "tally.py")


def _load(path, name="reask_mutant"):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MUTATIONS = [
    ("tail reads the head",
     '("tail", "votes", "asc")', '("tail", "votes", "desc")'),
    ("both score arms read the head",
     '("head", "votes", "desc")', '("head", "votes", "asc")'),
    ("the Active tab reads the score head instead",
     '("default", "activity", "desc")', '("default", "votes", "desc")'),
    ("a missing closure reason counts as a duplicate",
     'r["closed_reason"] == "Duplicate"',
     'r["closed_reason"] in ("Duplicate", None)'),
    ("the case is dropped from the literal",
     'r["closed_reason"] == "Duplicate"',
     'r["closed_reason"] == "duplicate"'),
    ("an arm is capped at one page inside report",
     "k, n, p, lo, hi = _rate(rs)", "k, n, p, lo, hi = _rate(rs[:25])"),
    ("an arm is capped at one page in the pooled section",
     "pooled[arm] += rs", "pooled[arm] += rs[:25]"),
    ("the score range is printed upside down",
     '"[%4d,%4d]" % (min(scores), max(scores))', '"[%4d,%4d]" % (max(scores), min(scores))'),
    ("the tail arm is dropped from the population",
     '("tail", "votes", "asc"),', ""),
    ("a stratum loses a declared tag",
     '("S4", "math", "probability"),', ""),
    ("an amended R2 tag is quietly promoted into the declared list",
     '"probability"]', '"probability", "baggage"]'),
    ("the R2 sample is dropped from the registry",
     '    ("R2", ("tail", ["baggage", "calculus"], 1)),', ""),
    ("R2's tail arm is declared as the score head",
     '("R2", ("tail", ["baggage", "calculus"], 1))',
     '("R2", ("head", ["baggage", "calculus"], 1))'),
    ("a tag is fetched in two samples at once",
     '["baggage", "calculus"]', '["baggage", "customs"]'),
    ("R1 silently stops being an out-of-sample re-read",
     '("R1", ("tail", ["customs", "excel-formula"], 5))',
     '("R1", ("tail", ["customs", "excel-formula"], 1))'),
    ("a sample with no rows is skipped instead of declared",
     'if not sub:\n            out("\\n%s: no rows committed (raw/%s.jsonl absent or empty)\\n"',
     'if False:\n            out("\\n%s: no rows committed (raw/%s.jsonl absent or empty)\\n"'),
    ("the declared gates absorb the amendment samples|measures.py",
     'declared = reask.load_sample("declared")', 'declared = reask.load()'),
]


def falsify(here=None):
    """Apply each mutation to a copy of the module it names, in a temp directory holding
    the whole experiment's modules and a link to the committed raw bytes, then run the
    checks against that copy. A mutation of one file cannot be caught by inspecting
    another, so each names its target."""
    here = here or HERE
    sources = [n for n in ("reask.py", "harvest.py", "measures.py", "tally.py")
               if os.path.exists(os.path.join(here, n))]
    raw = os.path.join(here, "raw")
    rows = []
    for name, before, after in MUTATIONS:
        target = name.split("|", 1)[1] if "|" in name else None
        label, _, anchor = name.partition("|")
        target = target or "reask.py"
        src = open(os.path.join(here, target)).read()
        if before not in src:
            rows.append((label, "NOT APPLIED", "%s: anchor not found: %r" % (target, before)))
            continue
        tmp = tempfile.mkdtemp(prefix="e034-")
        try:
            for mod in sources:
                shutil.copy(os.path.join(here, mod), os.path.join(tmp, mod))
            if os.path.isdir(raw):
                os.symlink(raw, os.path.join(tmp, "raw"))
            with open(os.path.join(tmp, target), "w") as fh:
                fh.write(src.replace(before, after, 1))
            saved = list(sys.path)
            sys.path.insert(0, tmp)
            for mod in ("reask", "harvest", "measures", "tally"):
                sys.modules.pop(mod, None)
            try:
                res = check(_load(os.path.join(tmp, "reask.py"), "reask_mutant"))
            except Exception as exc:
                res = [("crash", False, "%s: %s" % (type(exc).__name__, exc))]
            finally:
                sys.path[:] = saved
                for mod in ("reask", "harvest", "measures", "tally"):
                    sys.modules.pop(mod, None)
            failed = [n for n, ok, _d in res if not ok]
            rows.append((label, "caught" if failed else "MISSED",
                         ", ".join(failed[:4]) if failed else "no check fired"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return rows


def run(check, here=None):
    here = here or HERE
    sources = [n for n in MODULES if os.path.exists(os.path.join(here, n))]
    raw = os.path.join(here, "raw")
    rows = []
    for name, before, after in MUTATIONS:
        label, _, target = name.partition("|")
        target = target or "reask.py"
        src = open(os.path.join(here, target)).read()
        if before not in src:
            rows.append((label, "NOT APPLIED",
                         "%s: anchor not found: %r" % (target, before)))
            continue
        tmp = tempfile.mkdtemp(prefix="e034-")
        try:
            for mod in sources:
                shutil.copy(os.path.join(here, mod), os.path.join(tmp, mod))
            if os.path.isdir(raw):
                os.symlink(raw, os.path.join(tmp, "raw"))
            with open(os.path.join(tmp, target), "w") as fh:
                fh.write(src.replace(before, after, 1))
            saved = list(sys.path)
            sys.path.insert(0, tmp)
            for mod in ("reask", "harvest", "measures", "tally"):
                sys.modules.pop(mod, None)
            try:
                res = check(_load(os.path.join(tmp, "reask.py")))
            except Exception as exc:
                res = [("crash", False, "%s: %s" % (type(exc).__name__, exc))]
            finally:
                sys.path[:] = saved
                for mod in ("reask", "harvest", "measures", "tally"):
                    sys.modules.pop(mod, None)
            failed = [n for n, ok, _d in res if not ok]
            rows.append((label, "caught" if failed else "MISSED",
                         ", ".join(failed[:4]) if failed else "no check fired"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return rows
