<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E177 AMENDMENT 4 — one file per row, hard-wrapped, after the reader lost 18 questions to line length

**Declared before the re-run that adopts it.** CLF batch `a` ran and reported
its own defect, which is why the reader was given the shape it was given.

`clf/a.jsonl` and `clf/b.jsonl` are one JSON object per line. The reading
tool caps a line at 2000 characters, and a Stack Overflow `key_answer` that
carries a code block runs past that. **On 18 of batch a's 50 rows CLF never saw
the question at all** — it labelled them from the key answer plus title and
tags, which is exactly the half of the row the label is a function of both of.
The reader said so, named all 18 qids, and named the six it would not defend.

**Those 18 labels are discarded, not merged.** `clf/labels-a.jsonl` is deleted.
They are not averaged, not repaired, and not reported.

**Repair.** `roles.py` now writes **one text file per row**,
`clf/<batch>/<qid>.txt`, with fixed labelled sections and every line hard-wrapped
at 90 columns. No line can exceed the cap whatever the answer contains. The
population, the batch split and the ordering are unchanged, and
`clf_population.json`'s digests are unchanged, so the run is comparable to the
one it replaces.

This is the second instrument defect in this experiment's first three runs
(`AMENDMENT-1` the tag shape, `AMENDMENT-2` the key and the paging), and it is
the third in this repository's history that came from a *format* rather than a
*judgement*. Recorded as a finding candidate for the FORMAT section of the
record rather than left in this file alone.