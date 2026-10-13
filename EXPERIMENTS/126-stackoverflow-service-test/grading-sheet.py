#!/usr/bin/env python3
"""E126 grading sheet: each attempt beside its thread's
top answers, for the grading read. HTML is stripped;
answers are vote-sorted (the fetch already sorted them).
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TAG = re.compile(r"<[^>]+>")


def strip(body):
    return re.sub(r"\s+", " ", html.unescape(TAG.sub(" ", body or ""))).strip()


def main():
    threads = json.load(open(os.path.join(HERE, "threads.json")))
    attempts = {int(a["question_id"]): a
                for a in (json.loads(l)
                          for l in open(os.path.join(HERE, "attempts.jsonl"))
                          if l.strip())}
    out = []
    for qid_s in sorted(threads,
                        key=lambda q: -threads[q].get("question", {}).get("view_count", 0)):
        qid = int(qid_s)
        t = threads[qid_s]
        q = t.get("question", {})
        out.append(f"### id={qid} views={q.get('view_count')} "
                   f"answers={q.get('answer_count')} "
                   f"accepted={q.get('accepted_answer_id')}\n"
                   f"TITLE: {q.get('title')}\n")
        a = attempts.get(qid, {})
        out.append(f"ATTEMPT ({len(a.get('attempt', ''))} chars): "
                   f"{strip(a.get('attempt', 'MISSING'))[:600]}\n")
        for ans in t.get("answers", [])[:3]:
            out.append(f"ANSWER (score {ans.get('score')}): "
                       f"{strip(ans.get('body', ''))[:700]}\n")
        out.append("")
    with open(os.path.join(HERE, "grading-sheet.txt"), "w") as fh:
        fh.write("\n".join(out))
    print("wrote grading-sheet.txt")


if __name__ == "__main__":
    main()
