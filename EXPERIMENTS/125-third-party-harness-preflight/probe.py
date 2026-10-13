"""E125 step 4 -- the zero-adapter path, measured rather than asserted.

`load_rows` is the whole of what a third party is assumed to be able to do:
read a JSON array, read JSON-Lines, or read a CSV or TSV with a header row, of
flat records. It dispatches on the file extension and refuses everything else,
including YAML and Markdown -- there is no YAML parser in a standard-library-only
loader, and a file the loader cannot parse must never read as `clean` (F016,
AMENDMENT-1 correction 2).

Candidate selection runs over each repository's **full** listing, not a capped
prefix (AMENDMENT-1 correction 1), with declared patterns and a declared cap
applied identically to all 22 repositories.

A key/output pair is proposed only where the declared M4 rule holds
mechanically: the two files share an identifier-shaped field **name**, and their
row counts are within an order of magnitude. Every proposed pair is run through
`preflight.concordance` unmodified -- this is M3, at zero adapter cost.

Field vocabularies are **stem matching**, calibrated once against the
population's observed field names (`fieldnames.json`); the stems are declared
below with the count that motivated each.
"""

import io
import json
import os
import re
import subprocess
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "124-eval-harness-preflight"))
from preflight import concordance  # noqa: E402

SCRATCH = os.environ.get("E125_SCRATCH", "/tmp/opencode/e125")
CAP_PER_GROUP = 60
MAX_BYTES = 8_000_000

DATA_EXT = re.compile(r"\.(jsonl|json|csv|tsv)$", re.I)
# Selection patterns over paths, for the full listing.
KEYPATH = re.compile(r"(gold|answer|reference|expected|label|ground.?truth|solution|ideal|criteria|key|gt)", re.I)
OUTPATH = re.compile(r"(pred|result|output|response|completion|generat|actual|scored|graded|log|report)", re.I)

LFS = b"version https://git-lfs.github.com/spec/v1"

# --- stems, with the population count that motivated each -------------------
# id stems: id(20), question(15) is not an id, index(4), test_case_id(4), name(3)
ID_STEMS = ["id", "index", "idx", "uid", "uuid", "key", "name", "qid", "seq", "num", "no", "case"]
# key-side stems: answer(10), expected_behavior(8), ground_truth(7), expected_skill(5),
# expected_script(5), labels(1), criteria(1), ideal, target, reference, label, solution
KEY_STEMS = ["answer", "expected", "groundtruth", "label", "ideal", "target", "reference",
             "solution", "correct", "gold", "criteria", "acceptance", "accept"]
# output-side stems: response, prediction, pred, output, completion, generated, actual,
# result, modelanswer, modelresponse, extraction
OUT_STEMS = ["response", "prediction", "pred", "output", "completion", "generated",
             "actual", "result", "modelanswer", "extracted", "raw"]


def norm(field):
    return re.sub(r"[^a-z0-9]", "", str(field).lower())


def field_roles(names):
    ids = sorted(f for f in names if any(s in norm(f) for s in ID_STEMS))
    keys = sorted(f for f in names if any(s in norm(f) for s in KEY_STEMS))
    outs = sorted(f for f in names if any(s in norm(f) for s in OUT_STEMS))
    return ids, keys, outs


def blob(repo, commit, path):
    proc = subprocess.run(["git", "cat-file", "blob", "%s:%s" % (commit, path)],
                          cwd=os.path.join(SCRATCH, repo.replace("/", "__")),
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if proc.returncode != 0:
        return None
    return proc.stdout


def load_rows(raw, path):
    """The generic loader. Returns (rows, how). Never raises for bad input."""
    if raw is None:
        return None, "blob unavailable"
    if raw.startswith(LFS):
        return None, "git-lfs pointer; content not in this clone"
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, "not utf-8"
    ext = os.path.splitext(path)[1].lower()
    if ext not in (".json", ".jsonl", ".csv", ".tsv"):
        return None, "unsupported format (%s): no parser in a stdlib-only loader" % (ext or "no extension")
    if not text.strip():
        return None, "empty file"
    if ext in (".json", ".jsonl"):
        try:
            data = json.loads(text)
        except ValueError:
            rows = []
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    return None, "jsonl line does not parse"
            data = rows
        if isinstance(data, dict):
            # A mapping of id -> record needs a line of code to read; say so
            # rather than guessing which shape the caller wanted.
            return None, "top-level object, not an array or jsonl"
        if not isinstance(data, list):
            return None, "top-level %s" % type(data).__name__
        if not data or not all(isinstance(r, dict) for r in data):
            return None, "not a list of flat records"
        return data, ext[1:]
    import csv
    delim = "\t" if ext == ".tsv" else ","
    try:
        rows = list(csv.DictReader(io.StringIO(text), delimiter=delim))
    except Exception as exc:  # noqa: BLE001
        return None, "%s parse failed: %s" % (ext[1:], type(exc).__name__)
    if len(rows) < 2 or not all(isinstance(r, dict) for r in rows):
        return None, "%s has fewer than two rows" % ext[1:]
    return rows, ext[1:]


def fields_of(rows):
    """Field names in the first 20 rows.

    `csv.DictReader` puts surplus cells under a `None` key when a row is wider
    than the header. That is a real shape in committed data; such a key names
    nothing and is dropped.
    """
    out = []
    for r in rows[:20]:
        for k in r:
            if not isinstance(k, str) or not k:
                continue
            if k not in out:
                out.append(k)
    return out


def classify(rows):
    ids, keys, outs = field_roles(fields_of(rows))
    side = "unknown"
    if keys and not outs:
        side = "key-ish"
    elif outs and not keys:
        side = "output-ish"
    elif keys and outs:
        side = "both"
    return {"id_fields": ids, "key_fields": keys, "output_fields": outs,
            "side": side, "n": len(rows)}


def m4_qualifies(key, out):
    """The declared rule: shared identifier-shaped field NAME, counts within 10x."""
    shared = set(key["id_fields"]) & set(out["id_fields"])
    if not shared:
        return False, "no shared identifier-shaped field name (key %s / output %s)" % (
            ",".join(key["id_fields"][:3]) or "-", ",".join(out["id_fields"][:3]) or "-")
    if not key["n"] or not out["n"]:
        return False, "an empty side"
    lo, hi = sorted((key["n"], out["n"]))
    if hi > 10 * lo:
        return False, "row counts differ by more than 10x (%d vs %d)" % (key["n"], out["n"])
    return True, "shared id field(s) %s; counts %d vs %d" % (", ".join(sorted(shared)), key["n"], out["n"])


def listing(slug):
    out = []
    with open(os.path.join(HERE, "trees", slug + ".tsv")) as fh:
        for line in fh:
            size, path = line.rstrip("\n").split("\t", 1)
            out.append((int(size) if size.isdigit() else -1, path))
    return out


def main():
    with open(os.path.join(HERE, "trees.json")) as fh:
        trees = json.load(fh)

    field_freq = Counter()
    out_rows = []
    for repo in trees["repositories"]:
        slug = repo["full_name"].replace("/", "__")
        entry = {"full_name": repo["full_name"], "stars": repo["stars"],
                 "commit": repo.get("commit"), "readable": [], "unreadable": [],
                 "pairs": [], "both_sided": [], "rejected_pairs": []}
        if not repo.get("commit"):
            entry["pair_notes"] = "clone failed; nothing to read"
            out_rows.append(entry)
            print("%-38s no commit" % repo["full_name"])
            continue

        files = listing(slug)
        data_files = [(s, p) for s, p in files
                      if DATA_EXT.search(p) and 0 < s < MAX_BYTES]
        cands, seen = [], set()
        for group, rx in (("output-path", OUTPATH), ("key-path", KEYPATH)):
            picked = [p for s, p in data_files if rx.search(os.path.basename(p))][:CAP_PER_GROUP]
            entry["n_%s_candidates" % group] = len(picked)
            entry["n_%s_in_tree" % group] = len(
                [1 for s, p in data_files if rx.search(os.path.basename(p))])
            for p in picked:
                if p not in seen:
                    seen.add(p)
                    cands.append(p)

        classified, cache = [], {}
        for path in cands:
            raw = blob(repo["full_name"], repo["commit"], path)
            rows, how = load_rows(raw, path)
            if rows is None or len(rows) < 2:
                entry["unreadable"].append({"path": path, "reason": how})
                continue
            cache[path] = rows
            rec = {"path": path, "how": how, "bytes": len(raw)}
            rec.update(classify(rows))
            field_freq.update(fields_of(rows))
            entry["readable"].append(rec)
            classified.append(rec)

        entry["both_sided"] = [c["path"] for c in classified if c["side"] == "both"]

        for i, a in enumerate(classified):
            for b in classified[i + 1:]:
                if "both" in (a["side"], b["side"]):
                    continue
                if a["side"] == b["side"]:
                    continue
                key, outr = (a, b) if a["side"] == "key-ish" else (b, a)
                ok, why = m4_qualifies(key, outr)
                if not ok:
                    entry["rejected_pairs"].append({
                        "key": key["path"], "output": outr["path"], "reason": why})
                    continue
                primary = concordance(cache[key["path"]], cache[outr["path"]])
                swapped = concordance(cache[outr["path"]], cache[key["path"]])
                entry["pairs"].append({
                    "key": {"path": key["path"], "how": key["how"], "n": key["n"],
                            "id_fields": key["id_fields"], "key_fields": key["key_fields"]},
                    "output": {"path": outr["path"], "how": outr["how"], "n": outr["n"],
                               "id_fields": outr["id_fields"], "output_fields": outr["output_fields"]},
                    "adapter_lines": 0,
                    "m4": why,
                    "verdict": primary["verdict"],
                    "best_rate": primary["best_rate"],
                    "reason": primary["reason"],
                    "type_conflicts": primary["type_conflicts"],
                    "n_pairings": len(primary["pairings"]),
                    "swapped_verdict": swapped["verdict"],
                    "swapped_best_rate": swapped["best_rate"],
                })
        out_rows.append(entry)
        print("%-38s data %4d cands %3d readable %3d unreadable %3d pairs %d both %d rejected %d"
              % (repo["full_name"], len(data_files), len(cands), len(entry["readable"]),
                 len(entry["unreadable"]), len(entry["pairs"]), len(entry["both_sided"]),
                 len(entry["rejected_pairs"])))

    with open(os.path.join(HERE, "fieldnames.json"), "w") as fh:
        json.dump({"experiment": "E125",
                   "note": "field-name frequencies over the first 20 rows of every readable candidate file",
                   "counts": dict(field_freq.most_common())}, fh, indent=1, sort_keys=True)
    with open(os.path.join(HERE, "pairs.json"), "w") as fh:
        json.dump({"experiment": "E125",
                   "loader": "extension-dispatched: json | jsonl | csv | tsv of flat records",
                   "cap_per_group": CAP_PER_GROUP,
                   "repositories": out_rows}, fh, indent=1, sort_keys=True)
    total = sum(len(r["pairs"]) for r in out_rows)
    print("\n%d repositories, %d qualified pairs" % (len(out_rows), total))


if __name__ == "__main__":
    sys.exit(main())