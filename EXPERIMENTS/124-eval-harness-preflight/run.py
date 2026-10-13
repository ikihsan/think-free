#!/usr/bin/env python3
"""E124 -- run the preflight checks against five committed harnesses.

Every input is a file this repository already contains. No case is hand-tuned,
and the checks are not told which defect a case carries: they are handed rows,
labels and predicates, and they measure.

Usage: python3 run.py [--out results.json]
"""

import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from preflight import alternate_form_fp, concordance, control_arm, render  # noqa: E402

E114 = os.path.join(ROOT, "EXPERIMENTS", "114-value-grounding")
E116 = os.path.join(ROOT, "EXPERIMENTS", "116-berka-service-test")


def load_jsonl(path):
    with open(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def import_from(path, name):
    """Import a sibling experiment module by path (they are not a package)."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------- E116, key join

def case_a():
    """The committed key, exactly as the scorer read it: integer account ids."""
    key = load_jsonl(os.path.join(E116, "key.jsonl"))
    answers = load_jsonl(os.path.join(E116, "answers.jsonl"))
    return {
        "name": "A: E116 scorer, committed integer key ids",
        "check": concordance(key, answers),
        "baseline": "the scorer printed TP=0, FP=0, FN=0 for every account; no gate fired",
    }


def case_b():
    """The same key after score.py's repair: the id composed from arm and number."""
    key = load_jsonl(os.path.join(E116, "key.jsonl"))
    answers = load_jsonl(os.path.join(E116, "answers.jsonl"))
    repaired = [dict(r, account_id="%s%03d" % (r["arm"], r["account_id"])) for r in key]
    return {
        "name": "B: E116 scorer, composed key ids (repaired)",
        "check": concordance(repaired, answers),
        "baseline": "recall 1.0000 on the R arm, F1 0.8242, printed normally",
    }


# ------------------------------------------------------------- E114, verifier arms

MONEY = re.compile(r"\$\s?\d[\d,]*(?:\.\d\d)?")
DATE = re.compile(r"(?:January|February|March|April|May|June|July|August|September|"
                  r"October|November|December)\s+\d{1,2},\s+\d{4}")


def _verbatim_items(numbers, rawdir):
    """Money and date strings copied out of the document itself.

    This is the control E114 already ran (false-alarm rate 0.0069 on 145
    values). It is regenerated here rather than quoted so the arm is measured
    from the documents, not copied from a summary.
    """
    items = []
    for num in numbers:
        text = open(os.path.join(rawdir, "text", num + ".txt"), "rb").read().decode("utf-8", "replace")
        seen = set()
        for pattern in (MONEY, DATE):
            for match in pattern.findall(text):
                value = match.strip()
                if value in seen:
                    continue
                seen.add(value)
                items.append({"arm": "verbatim", "document": num, "value": value, "correct": True})
        if len(items) >= 400:
            break
    return items


def _flagger(ground, rawdir):
    cache = {}

    def doc_for(num):
        if num not in cache:
            cache[num] = ground.load_doc(num, rawdir)
        return cache[num]

    def flagger(item):
        doc = doc_for(item["document"])
        probe = "The document states %s." % item["value"]
        for verdict in ground.judge(doc, probe):
            if verdict["value"].strip() == item["value"].strip():
                return verdict["verdict"]
        return None

    return flagger


def case_c(ground):
    answers = load_jsonl(os.path.join(E114, "answers.jsonl"))
    numbers = []
    for row in answers:
        if row["document_number"] not in numbers:
            numbers.append(row["document_number"])
    items = _verbatim_items(numbers, os.path.join(E114, "raw"))
    return {
        "name": "C: E114 verifier, values in the document's own form (bare probe sentence)",
        "check": alternate_form_fp(items, _flagger(ground, os.path.join(E114, "raw")), fp_ceiling=0.02),
        "baseline": "E114's own KG-C2 gate: false-alarm rate 0.0069, instruments_valid true",
        "n_items": len(items),
    }


def _sentence_around(text, value):
    """The sentence of a real answer that carries `value`."""
    at = text.find(value)
    if at < 0:
        return text
    start = max(text.rfind(".", 0, at), text.rfind(";", 0, at), text.rfind("\n", 0, at)) + 1
    end = text.find(".", at)
    if end < 0:
        end = min(len(text), at + 400)
    return text[start:end + 1].strip() or text[max(0, at - 200):at + 200]


def case_c2(ground):
    """AMENDMENT-1 case C': real values, real prose, independent label.

    The label is a string search of the document: `score.py`'s own
    normalisation (strip whitespace and commas, drop a leading `$`, lower case)
    applied to both sides. Nothing here consults the verifier's score, so the
    arm also re-derives, by string matching alone, E114's claim that the
    reader fabricated no value.
    """
    rawdir = os.path.join(E114, "raw")
    docs = {}
    items = []
    for row in load_jsonl(os.path.join(E114, "checked.jsonl")):
        num = row["document_number"]
        if num not in docs:
            docs[num] = ground.load_doc(num, rawdir)
        haystack = _plain(docs[num])
        for entry in row.get("checked", []):
            value = entry["value"]
            host = _sentence_around(row["answer"], value)
            items.append({
                "arm": "in_situ",
                "document": num,
                "value": value,
                "host": host,
                "correct": _plain(value) in haystack,
            })

    def flagger(item):
        probe = item.get("host") or "The document states %s." % item["value"]
        for verdict in ground.judge(docs[item["document"]], probe):
            if verdict["value"].strip() == item["value"].strip():
                return verdict["verdict"]
        return None

    present = [i for i in items if i["correct"]]
    return {
        "name": "C': E114 verifier, the reader's own values in the reader's own prose",
        "check": alternate_form_fp(items, flagger, fp_ceiling=0.02),
        "baseline": "E114 reported 0 of 374 values fabricated, by hand and by checker",
        "n_items": len(items),
        "independently_present": "%d/%d values found in the document by string search"
                                 % (len(present), len(items)),
    }


def _plain(text):
    return re.sub(r"[\s,]", "", text).replace("$", "").lower()


def case_d(ground):
    """Values a free assistant wrote, hand-read as present in the document."""
    rows = [r for r in load_jsonl(os.path.join(E114, "flags-verified.jsonl")) if r.get("all_parts_present")]
    items = [{"arm": "assistant_form", "document": r["document"], "value": r["value"],
              "correct": True, "missing": r.get("missing", [])} for r in rows]
    return {
        "name": "D: E114 verifier, values written by the reader being judged",
        "check": alternate_form_fp(items, _flagger(ground, os.path.join(E114, "raw")), fp_ceiling=0.02),
        "baseline": "every one of these 24 was flagged by the verifier; F118 read them back as present",
        "n_items": len(items),
    }


# ------------------------------------------------------------ E116, the control arm

RECURRING = re.compile(r"monthly.*identical amount", re.I)


def _positive_by_answer_detail(row):
    """True when the reader's own description of the extract says the account
    carries a standing order: a monthly pattern at an identical amount.

    Evidence is the answer's free-text `detail`, not the key. A predicate that
    read the key could only confirm the key.
    """
    detail = row.get("detail") or {}
    for name, value in detail.items():
        if name == "rejected":
            continue
        if isinstance(value, dict) and RECURRING.search(value.get("pattern", "")):
            return True
    return False


def case_e():
    answers = [r for r in load_jsonl(os.path.join(E116, "answers.jsonl")) if r["account_id"].startswith("C")]
    rows = [dict(r, id=r["account_id"], evidence=_first_pattern(r)) for r in answers]
    return {
        "name": "E: E116 G0_C_precision control arm",
        "check": control_arm(rows, _positive_by_answer_detail, premise=0.0, name="C accounts"),
        "baseline": "G0_C_precision = 0.0 for the assistant, the detector and the naive rule alike",
    }


def _first_pattern(row):
    for name, value in (row.get("detail") or {}).items():
        if name != "rejected" and isinstance(value, dict):
            return value.get("pattern", "")
    return row.get("detail", {}).get("note", "") if isinstance(row.get("detail"), dict) else ""


def main():
    ground = import_from(os.path.join(E114, "ground.py"), "e114_ground")
    cases = [case_a(), case_b(), case_c(ground), case_d(ground), case_c2(ground), case_e()]
    out = {"experiment": "E124", "cases": []}
    for case in cases:
        check = case["check"]
        text, code = render([check], rate="(not computed)")
        entry = {"name": case["name"], "verdict": check["verdict"], "exit": code,
                 "baseline": case["baseline"], "report": text, "check": check}
        for extra in ("n_items", "independently_present"):
            if extra in case:
                entry[extra] = case[extra]
        out["cases"].append(entry)
        print("=" * 78)
        print(case["name"])
        print(text)
        if "independently_present" in case:
            print("independent label: %s" % case["independently_present"])
        print("baseline: %s" % case["baseline"])
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("=" * 78)
    print("wrote results.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())