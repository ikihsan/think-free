#!/usr/bin/env python3
"""Render the G0a control sheet: the five control questions and every comment on
them, one per line, with the question's owner marked.

This exists so the hand-labelling that G0a requires happens against a flat
document rather than against a JSON blob, and so the hand labels and the lexicon
verdicts can be diffed afterwards. It reads only committed files.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
E177 = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                    "EXPERIMENTS", "177-evidence-gated-need")
TAG = re.compile(r"<[^>]+>")


def text(html):
    out = TAG.sub(" ", html or "")
    for a, b in (("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&"), ("&quot;", '"')):
        out = out.replace(a, b)
    return re.sub(r"\s+", " ", out).strip()


def owners():
    """question_id -> owner user_id, from E177's committed raw responses."""
    out = {}
    path = os.path.join(E177, "raw", "se.jsonl")
    for line in open(path):
        rec = json.loads(line)
        for it in rec["body"].get("items", []):
            if "question_id" in it and "owner" in it:
                out.setdefault(it["question_id"], it["owner"].get("user_id"))
    return out


def main():
    com = json.load(open(os.path.join(HERE, "comments.json")))
    own = owners()
    rows = {r["qid"]: r for r in
            json.load(open(os.path.join(E177, "rows.json")))["rows"]}
    lines = []
    for qid in com["control_set"]:
        items = sorted(com["control_comments"].get(str(qid), []),
                       key=lambda c: c.get("creation_date") or 0)
        lines.append("=" * 78)
        lines.append("QUESTION %d  comments=%d  owner=%s"
                     % (qid, len(items), own.get(qid)))
        lines.append("TITLE: %s" % rows[qid]["title"])
        lines.append("-" * 78)
        for i, c in enumerate(items, 1):
            o = c.get("owner") or {}
            mark = "OWNER" if o.get("user_id") == own.get(qid) else "      "
            lines.append("%s %2d | uid=%s rep=%s | %s | %s"
                         % (mark, i, o.get("user_id"), o.get("reputation"),
                            c.get("creation_date"), text(c.get("body"))))
    out = os.path.join(HERE, "raw", "view_g0a.txt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("%s: %d lines, %d control questions, %d comments"
          % (out, len(lines), len(com["control_set"]),
             sum(len(com["control_comments"].get(str(q), []))
                 for q in com["control_set"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())