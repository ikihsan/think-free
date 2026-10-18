<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# E181 AMENDMENT 1 — two corrections to the protocol, before any reader saw a row

**Written:** 2026-10-18, after `prep.py` ran and after `population.json` and the
twenty `ext/` files were written, and **before `facts.jsonl` exists** — before
any reader has looked at a question, a comment, or an accepted answer in this
experiment. Both changes make the population and the treatment's input larger
and better specified. Neither changes a gate, an arm, or a threshold.

## 1. The selection order is a seeded shuffle, not descending view count

The protocol said the twenty rows are "the first 20 in E177's
`score/index.json` order. That order is CLF's emission order, which is the draw
order, which is descending `view_count`." **The last clause is wrong.**

`EXPERIMENTS/177-evidence-gated-need/arms.py:62` does sort each arm by
`-view_count`, so E177's 30 EVID rows are the 30 highest-arrival EVID rows of
its pool. But `score_inputs.py:45` then shuffles the graded set with
`random.Random(17720261018)` before writing `score/index.json`, and the reader
is handed that shuffled order. **The index order is therefore a seeded random
permutation of the 30**, which the observed `view_count` values confirm
(6,340 / 9,816 / 7,926 / 12,078 / 13,728 / 3,247 …).

**This makes the property stronger, not weaker, and nothing else changes.** The
twenty rows are still the first twenty of a fixed order nobody chose while
reading anything, and that order is now *independent of arrival as well* — so
they are not the twenty highest-arrival rows either. `population.json` now
records the true rule and the seed.

## 2. `EXT`'s input includes the question's comments, not only the accepted answer's

The protocol named "the comments on its accepted answer". That was written
before checking where the round trip actually is on these rows, and it is too
narrow: **240 of the 303 comment spans on these twenty rows are on the
question**, not on the answer (63), and five of the twenty rows have *no*
comment on the accepted answer at all while carrying 3–30 on the question.

Two reasons this matters, one of them an integrity point.

**The integrity point.** E178's `where` labels (`asker_only` / `third_party` /
`none`) were written by a reader whose input files contain the question and the
key answer and **no comments at all** — visible in
`EXPERIMENTS/178-evidence-where-does-it-live/reader/b0/*.txt`. So `where`
records **an inference about where such a fact must live**, not an observation
that anybody wrote it down. Taking the accepted answer's comments as *the*
round trip would have treated an inference as a measurement, which is F133's
shape. `EXT` now sees both comment sets, each in creation order.

**The power point.** Under the original wording, five rows would have had no
eligible source at all and K1 (< 16 rows carrying an A1 fact) would have fired
on a definitional accident rather than on a fact about the world.

## 3. The eligibility rule, declared and checked

A row is eligible when at least one comment on the question or on its accepted
answer is on disk. **All 30 of E177's scored EVID rows are eligible**, so the
rule excluded nothing and the population carries no eligibility bias. It is
recorded because it was checked, and because a reader comparing this population
with E177's 30 needs to know the two are the same 30.

## Cost, recorded

`prep.py` re-fetched 8 answer-comment sets E178 had not captured (the other 22
reuse E178's committed bytes) and recovered 240 question comments from E178's
own `raw/se.jsonl` rather than re-fetching them. Every response is in
`raw/se.jsonl` with its URL, item count, paging flag and quota counter.

## The leak assertion, passed

`prep.py` re-reads all twenty `ext/` files after writing them and refuses to
continue if any key-answer id, or the first 120 characters of any accepted
answer, appears in one. It did not. The accepted answer is absent from every
file `EXT` will see.