#!/usr/bin/env python3
"""build_arms.py — construct E140's five arms from E114's committed answers.

V  verbatim            the real answer, unchanged
P  paraphrase          deterministic surface transforms only
P2 paraphrase, written  a fresh writer rewords it (job file; the rewrite lands
                        in p2.jsonl and is merged by finalize_p2.py)
C  corrupted           one value replaced, reusing E114's own seeded corrupter
K  truncated           one list item deleted, the rest intact

Writes arms.jsonl (every arm, for the deterministic instruments), the blinded
judge batches, and the P2 rewrite job. K4 is checked here and an item that
fails it is dropped and counted, because an invalid arm is not evidence.
"""
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
E114 = os.path.join(HERE, "..", "114-value-grounding")
sys.path.insert(0, HERE)
sys.path.insert(0, E114)

import controls as e114_controls  # noqa: E402  (seeded, documented corrupter)
import ground  # noqa: E402  (E114's extractor, imported unchanged)
import valueset  # noqa: E402

SEED = 20261014
JUDGE_SEED = SEED + 1     # AMENDMENT-2 §3: reshuffled after the orchestrator read the key
N_JUDGE = 10
N_P2 = 5
BATCH = 5


def _protect(text):
    """Replace every extracted value span with a private-use placeholder.

    Done on offsets, not by substring search, so a value that occurs twice is
    protected twice and the restoration is exact. After this the transforms
    below cannot reach a digit, which makes the P arm's value preservation
    structural rather than incidental."""
    spans, offset, out, last = [], 0, [], 0
    kept = []
    for kind, raw in ground.extract(text):
        i = text.index(raw, offset)
        spans.append((i, i + len(raw), raw))
        offset = i + len(raw)
    tokens = []
    for n, (s, e, raw) in enumerate(spans):
        token = "\ue000" + chr(ord("A") + n // 26) + chr(ord("a") + n % 26) + "\ue001"
        tokens.append((token, raw))
        out.append(text[last:s])
        out.append(token)
        last = e
    out.append(text[last:])
    return "".join(out), tokens


def surface_paraphrase(text, rng):
    """Surface-form changes only. Nothing here may alter which values appear,
    only how they are written or where in a list they sit.

    Every value span is lifted out first, so these transforms operate on the
    connective text between values. Two earlier versions did not protect, and
    K4 caught both: the first broke ground.extract's longest-match grouping of a
    citation run, so digits inside one code match became separate num matches;
    the second protected citations only, and a docket/FR pair re-split and
    contributed two values the verbatim arm did not have. See AMENDMENT-1.md
    sections 1 and 5."""
    out, tokens = _protect(text)

    out = re.sub(r"\bper hour\b", rng.choice(["each hour", "an hour"]),
                 out, flags=re.I)
    out = re.sub(r"\bpercent\b", lambda m: rng.choice(["%", "per cent"]),
                 out, flags=re.I)
    # punctuation and spacing, which the rubric's own text says to ignore
    out = re.sub(r";\s*", rng.choice([". ", "; "]), out)
    out = re.sub(r"  +", "  ", out)
    # reorder the item list: the value set survives, the order does not, and
    # this is the move that breaks M1's proximity check
    parts = [p for p in re.split(r"(?<=[.;])\s+", out) if p.strip()]
    if len(parts) > 3:
        head, items = parts[0], parts[1:]
        rng.shuffle(items)
        parts = [head] + items
    out = " ".join(parts)

    for token, raw in tokens:
        out = out.replace(token, raw)
    return out


def truncate(text):
    """Delete the last complete list item. Everything remaining is correct, so
    the arm tests sensitivity to omission rather than to a wrong value."""
    parts = [p for p in re.split(r"(?<=[.;])\s+", text) if p.strip()]
    if len(parts) < 3:
        return None
    return " ".join(parts[:-1])


def load_items():
    path = os.path.join(E114, "answers.jsonl")
    rows = [json.loads(l) for l in open(path) if l.strip()]
    rows = [r for r in rows if r["arm"] == "A"]
    rows.sort(key=lambda r: (r["document_number"], r["question"]))
    return rows


def judge_subset(rows):
    """Ten of the fifteen ANSWERS, not ten documents: the corpus is 15 answers
    over 5 documents, so the first version of this rule sampled from a
    five-element list and admitted all fifteen. One answer per document is drawn
    first and the rest are then spread across documents, so a single document
    cannot drop out. See AMENDMENT-1.md §3."""
    rng = random.Random(SEED)
    chosen, remaining_per_doc = [], {}
    for doc_num in sorted({r["document_number"] for r in rows}):
        candidates = [r for r in rows if r["document_number"] == doc_num]
        chosen.append(candidates[rng.randrange(len(candidates))])
        remaining_per_doc[doc_num] = len(candidates) - 1
    pool = [r for r in rows if r not in chosen]
    rng.shuffle(pool)
    for r in pool:
        if len(chosen) >= N_JUDGE:
            break
        if remaining_per_doc[r["document_number"]] > 0:
            remaining_per_doc[r["document_number"]] -= 1
            chosen.append(r)
    return chosen


def main():
    rows = load_items()
    docs = {}
    for r in rows:
        num = r["document_number"]
        if num not in docs:
            docs[num] = e114_controls.load(os.path.join(E114, "raw"), num)

    judge_rows = judge_subset(rows)
    judge_set = {(r["document_number"], r["question"]) for r in judge_rows}

    out, dropped = [], []
    for r in rows:
        num, ans = r["document_number"], r["answer"]
        ref_num = valueset.numeric_multiset(ans)

        rec, mode = None, None
        for mode in ("B1_from_document", "B2_absent"):
            rec = e114_controls.corrupt(ans, docs[num],
                                        random.Random(SEED + int(num[-3:])), mode)
            if rec is not None:
                break
        corrupted = rec is not None
        if not corrupted:
            # The three "this document states no dollar amounts" answers carry no
            # extractable value, so there is nothing to replace and C == V. AMENDMENT-2
            # §3 excludes them from the judge arm: they are duplicates of a V row, not
            # a third state, and a judge cannot grade them I without being wrong.
            dropped.append({"document_number": num, "arm": "C",
                            "reason": "no extractable value to corrupt; C == V"})
            corrupt, corrupt_mode, orig_v, repl_v = ans, None, None, None
        else:
            kind, original, repl, corrupt_mode = rec
            i = ans.find(original)
            corrupt = ans[:i] + repl + ans[i + len(original):]
            orig_v, repl_v = original, repl
        p_text = surface_paraphrase(ans, random.Random(SEED + int(num[-3:])))

        # K4: the arm must carry the same numeric multiset as the verbatim arm.
        # For C this is not the right test and never was: a corruption that does not
        # change the multiset has not corrupted anything. C is checked by "exactly one
        # reference value replaced", which is stated here so the drop report cannot be
        # read as a defect count it does not mean (AMENDMENT-2 §2).
        if valueset.numeric_multiset(p_text) != ref_num:
            dropped.append({"document_number": num, "arm": "P",
                            "reason": "numeric multiset differs from V"})
        if corrupted:
            # full canonical multiset, not numeric_multiset: the corrupter also
            # replaces citations and dates, which numeric_multiset does not carry
            rv, rc = (Counter(map(repr, valueset.canonical(t)))
                      for t in (ans, corrupt))
            n_changed = sum(((rc - rv) + (rv - rc)).values())
            if n_changed != 2:
                dropped.append({"document_number": num, "arm": "C",
                                "reason": "corruption changed %d values, expected 1"
                                          % (n_changed // 2)})

        base = {"document_number": num, "question": r["question"],
                "in_judge_subset": (num, r["question"]) in judge_set}
        out.append(dict(base, arm="V", answer=ans))
        out.append(dict(base, arm="P", answer=p_text))
        out.append(dict(base, arm="C", answer=corrupt, corrupted=corrupted,
                        corruption_mode=corrupt_mode,
                        original_value=orig_v, corrupted_value=repl_v))
        k_text = truncate(ans)
        if k_text:
            out.append(dict(base, arm="K", answer=k_text))

    with open(os.path.join(HERE, "arms.jsonl"), "w") as fh:
        for row in out:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

    # P2 job: the five judge items carrying the most values. AMENDMENT-2 §5
    # replaced the protocol's "shortest answer" rule, which selected the three
    # no-dollar-amount answers and so put P2 where there was nothing to reword.
    # No length cap: a cap would re-introduce the same defect.
    judge_items = sorted(
        [r for r in out if r["in_judge_subset"] and r["arm"] == "V"],
        key=lambda r: (-len(valueset.numeric_multiset(r["answer"])),
                       len(r["answer"])))[:N_P2]
    with open(os.path.join(HERE, "p2_job.json"), "w") as fh:
        json.dump({"items": [{"document_number": r["document_number"],
                              "question": r["question"],
                              "answer": r["answer"]}
                             for r in judge_items]}, fh, indent=1,
                  sort_keys=True)

    # blinded judge batches: no arm label in the text the judge will read, and no
    # un-corrupted C row, because that row repeats a V row verbatim (AMENDMENT-2 §4)
    judge_rows_out = [r for r in out
                      if r["in_judge_subset"] and r["arm"] in ("V", "P", "C")
                      and r.get("corrupted", True)]
    batches = []
    items = list(judge_rows_out)
    rng = random.Random(JUDGE_SEED)
    rng.shuffle(items)
    for i in range(0, len(items), BATCH):
        chunk = items[i:i + BATCH]
        key = [{"document_number": c["document_number"], "arm": c["arm"],
                "question": c["question"]} for c in chunk]
        batches.append({"batch": i // BATCH, "items": chunk, "_key": key})
    with open(os.path.join(HERE, "judge_batches.json"), "w") as fh:
        json.dump(batches, fh, indent=1, sort_keys=True)

    print(json.dumps({
        "items": len(rows), "judge_subset": sorted(judge_set),
        "arms_written": len(out), "judge_items": len(judge_rows_out),
        "batches": len(batches), "p2_items": len(judge_items),
        "k4_dropped": dropped}, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
