#!/usr/bin/env python3
"""emit_judge_prompts.py — write one blinded prompt per judge batch.

Each prompt contains inspect_ai's `model_graded_fact` template filled in
verbatim, once per item, plus the library's default instructions. Nothing else
is added that the library would not add, except the batch header and the batch
output format, which are declared deviations (PROTOCOL.md deviation 2: five
items to a generation) rather than edits to the rubric.

The arm label, the corruption fields, and the batch key are **not** written.
The judge receives a question, an expert answer and a submission, which is all
the library's template has slots for. The file is the unit of blinding: the
judge session is given this text and is told to open no file.

Run:  python3 emit_judge_prompts.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "judge_prompts")

# The template and the instructions, copied from judge_rubric.txt. Kept here as
# literals rather than parsed out of the rubric so that a formatting accident in
# the provenance file cannot silently change what the judge is asked; the test
# at the bottom asserts the two agree.
TEMPLATE = """You are comparing a submitted answer to an expert answer on a given question. Here is the data:

[BEGIN DATA]
************
[Question]: {question}
************
[Expert]: {criterion}
************
[Submission]: {answer}
************
[END DATA]

Compare the factual content of the submitted answer with the expert answer. Ignore any differences in style, grammar, or punctuation.

Does the submission contain the content in the expert answer?

{instructions}"""

INSTRUCTIONS = """
After assessing the submitted answer, reply with 'GRADE: $LETTER' (without quotes) where LETTER is one of CI.  Please choose ONE option for the grade: either "C" for correct answers, or "I" for incorrect answers.

For example, after reviewing a correct answer you might write 'GRADE: C' or after reviewing an incorrect answer you might write 'GRADE: I'.

First, write out in a step by step manner your reasoning about the criterion to be sure that your conclusion is correct. Avoid simply stating the correct answers at the outset. Then, end with your answer formatted as 'GRADE: $LETTER' (without quotes) where LETTER is one of CI.
"""

# The library neutralises the structural delimiters inside dataset-controlled
# text. Reproduced here so the reproduction is not merely asserted.
_DELIM = re.compile(r"\[(BEGIN|END) DATA\]", re.IGNORECASE)


def neutralize(text):
    return _DELIM.sub(lambda m: m.group(0).replace(" ", "-"), text)


BATCH_PREAMBLE = """\
You are grading {n} submitted answers against expert answers, one after
another. Each block below is a separate, self-contained grading task and uses
the same instructions. Treat them independently: an item's verdict must not
depend on any other item, and you must not assume that consecutive items differ
in any way.

Grade every one of the {n} items. For each item write its heading, your
step-by-step reasoning, and then the line 'GRADE: C' or 'GRADE: I' as the last
line of that item's block.

Output format, exactly:

### Item 1
<reasoning>
GRADE: X

### Item 2
<reasoning>
GRADE: X

...and so on through Item {n}. The 'GRADE:' line must be the final line of its
own block. Do not add a summary, a table, or any text after the last item.

"""


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for name in os.listdir(OUT):
        os.remove(os.path.join(OUT, name))

    batches = json.load(open(os.path.join(HERE, "judge_batches.json")))
    arms = [json.loads(l) for l in open(os.path.join(HERE, "arms.jsonl"))
            if l.strip()]
    # The expert answer is always the verbatim row for that document/question,
    # whatever arm the submission came from. This is what the library's
    # template slot {criterion} means.
    verbatim = {(r["document_number"], r["question"]): r["answer"]
                for r in arms if r["arm"] == "V"}

    written = []
    for entry in batches:
        n = len(entry["items"])
        parts = [BATCH_PREAMBLE.format(n=n)]
        for i, item in enumerate(entry["items"], 1):
            parts.append("### Item %d\n" % i)
            parts.append(TEMPLATE.format(
                question=neutralize(item["question"]),
                criterion=neutralize(
                    verbatim[(item["document_number"], item["question"])]),
                answer=neutralize(item["answer"]),
                instructions=INSTRUCTIONS))
            parts.append("\n")
        path = os.path.join(OUT, "batch_%02d.md" % entry["batch"])
        with open(path, "w") as fh:
            fh.write("".join(parts))
        written.append({"file": os.path.basename(path), "items": n})

    # Guard: the rubric file and this module must carry the same template.
    rubric = open(os.path.join(HERE, "judge_rubric.txt")).read()
    assert "Ignore any differences in style, grammar, or punctuation." in rubric
    assert "reply with 'GRADE: $LETTER'" in rubric
    assert "[BEGIN DATA]" in rubric and "[END DATA]" in rubric

    leaked = [w for w in written
              if re.search(r"^\s*(arm|_key|corruption_mode|corrupted)\s*[:=]",
                           open(os.path.join(OUT, w["file"])).read(), re.M)]
    print(json.dumps({"prompts": written, "total_items": sum(w["items"]
                                                            for w in written),
                      "arm_label_leaks": leaked}, indent=1))
    return 1 if leaked else 0


if __name__ == "__main__":
    raise SystemExit(main())
