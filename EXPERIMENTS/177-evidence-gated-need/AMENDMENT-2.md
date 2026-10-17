<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E177 AMENDMENT 2 — the key is the top-voted answer, and the answer fetch was truncated

**Declared before the re-run that adopts both.** Two defects, both found by the
first two runs and neither visible from the protocol.

## 1. There is almost no accepted answer in this pool

The protocol says the key is "the accepted answer". `accepted_answer_id` is
present on **3 of 181** returned questions and `is_accepted` is true on **6 of
700** fetched answers. This is not a filter problem — a control fetch of
question 79327621 returns `accepted_answer_id: null` under **both** the default
filter and `withbody`, on a question with four answers. The pool came from
E126's screening of questions with *at least one answer*, not of questions with
an *accepted* answer.

An accepted answer would key **6 rows**. The protocol's G1 needs 30 per arm.

**Repaired:** the key is **the highest-scoring answer; ties broken by the
earliest `creation_date`, then the lowest `answer_id`.** It is available on every
one of the 145 answered rows, it is a fixed function of bytes, and it is what
E175's `gold_from = "top_voted"` branch was already using for all but a handful
of its rows — so every number here stays comparable to E175's 0.1448 and
E175's F135.

**Ceiling this adds, declared:** the top-voted answer is not always what resolved
the asker's problem — an answer can be most-endorsed and still be "what I would
do", not "what fixed it". So the key is *the community's best answer*, and the
claim is about reaching that, not about resolving the question. Recorded as a
ceiling in RESULT.md, not repaired, because the alternative keys available here
(6 accepted answers) cannot carry the declared n.

## 2. The answer fetch was truncated by paging

`questions/{ids}/answers?pagesize=100` returns up to **100 answers across all
the ids in the request**, so the 25-id chunks silently dropped answers for
questions with many answers, and `has_more` was recorded but never read. The
first two runs therefore fetched 700 answers with an unknown shortfall.

**Repaired:** page until `has_more` is false, and log every page. Chunked at 20
ids. Questions with `answer_count == 0` are skipped, which is where most of the
saving is.

`raw/se.jsonl` is truncated and rewritten so the file on disk is one clean run
rather than three overlapping ones. The two earlier runs' response bodies are
discarded, not curated: they were only ever counted, never read.