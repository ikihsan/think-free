#!/usr/bin/env python3
"""E143 classify: record the agent's screening of all 300 rows.

Each row is classified by shape (question/execution/other) and sub
(answerable/specific for question; program/manual for execution).
The classification was done by reading screening-sheet.txt (title+body
only) before any answer or comment was read.

Codes: qa=question-answerable, qs=question-specific,
ep=execution-program, em=execution-manual, o=other
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# idx -> (shape, sub). shape in {question, execution, other};
# sub in {answerable, specific, program, manual, none}
C = {}
for i in range(300):
    C[i] = ("question", "answerable")

# --- question-specific rows (need the asker's data/output/environment) ---
SPECIFIC = [
    15, 20, 23, 26, 35, 37, 44, 46, 55, 58, 63, 64, 67, 71, 72, 74, 79,
    81, 84, 88, 89, 90, 91, 93, 94, 95, 97, 104, 105, 106, 107, 109,
    113, 114, 117, 118, 120, 121, 122, 124, 126, 127, 128, 129, 131,
    133, 135, 137, 139, 140, 141, 142, 145, 148, 153, 155, 156, 158,
    163, 164, 165, 166, 167, 168, 169, 170, 171, 173, 174, 175, 176,
    177, 178, 179, 181, 184, 185, 187, 188, 189, 190, 191, 192, 193,
    198, 199,
    # Arm B
    202, 203, 204, 206, 208, 209, 211, 215, 216, 218, 219, 220, 221,
    222, 223, 227, 228, 229, 231, 232, 233, 235, 238, 239, 240, 241,
    242, 245, 246, 247, 248, 251, 252, 253, 255, 258, 259, 260, 261,
    262, 263, 264, 265, 266, 267, 268, 270, 271, 272, 273, 274, 275,
    276, 277, 278, 280, 281, 282, 283, 284, 285, 286, 287, 289, 292,
    293, 294, 295, 296, 298, 299,
]
for i in SPECIFIC:
    C[i] = ("question", "specific")

# --- execution-shaped rows: NONE found across all 300 ---
# --- other rows: NONE found across all 300 ---


def main():
    rows = []
    for i in range(300):
        shape, sub = C[i]
        rows.append({"idx": i, "shape": shape, "sub": sub})
    with open(os.path.join(HERE, "screening.jsonl"), "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")

    # composition
    from collections import Counter
    armA = [C[i] for i in range(200)]
    armB = [C[i] for i in range(200, 300)]
    pooled = [C[i] for i in range(300)]

    def comp(rows_):
        c = Counter(rows_)
        n = len(rows_)
        return {
            "n": n,
            "question": c[("question", "answerable")] + c[("question", "specific")],
            "question_answerable": c[("question", "answerable")],
            "question_specific": c[("question", "specific")],
            "execution": c[("execution", "program")] + c[("execution", "manual")],
            "execution_program": c[("execution", "program")],
            "execution_manual": c[("execution", "manual")],
            "other": c[("other", "none")],
        }

    print("Arm A (votes):", json.dumps(comp(armA)))
    print("Arm B (creation):", json.dumps(comp(armB)))
    print("Pooled:", json.dumps(comp(pooled)))


if __name__ == "__main__":
    main()
