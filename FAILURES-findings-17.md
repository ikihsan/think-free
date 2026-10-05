<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Failures — recorded findings, part 17 (F042)

Continues [`FAILURES-findings-16.md`](FAILURES-findings-16.md), which holds F041,
and [`FAILURES-findings-15.md`](FAILURES-findings-15.md), which holds F039.
**Identifiers are stable across all findings files**: a reference to `F042` means
the same entry wherever it appears.

Source: session `2026-10-05-008`, task T-0066. Runnable evidence:
`EXPERIMENTS/022-need-outcomes/` — `PROTOCOL.md` (declared before any outcome
was read), `run.py`, `need_depth.py`, `need_depth_walk.py`, `lift_stratified.py`,
`serve_sample.py`, `author_build.py`, `combine.py`, `results.json`, and 11 raw
captures under `raw/`. Tests: `tests/test_need_depth_gate.py` (14).

## F042 — a repair instrument that reported "nothing to fetch" 29 times, resolved nothing, and exited 0

**Observed, 2026-10-05.** E022's own gate was red for its whole run:
`need_depth.py --verify` reported **434 of 1401 need comments with
`depth: null`**. `need_depth_walk.py` was written to resolve them. It fetched 432
ancestors, every one with status `ok`, and **resolved none of the 434**. It
printed `round N: 434 chains, no new ancestors` for 29 rounds and returned
**exit code 0**.

**The defect.** The loop advanced each chain by re-appending the chain's
*current* node with a larger hop count:

```python
nxt.append([node, sid, hops + 1, waiting])   # node is never replaced
```

`node == sid` is the only condition that resolves a chain, so a chain longer
than one hop could never close. Three sampled chains resolve live at **4, 2 and
3 hops**. After the repair **1401 of 1401 depths resolve**, with a tail to depth
20.

**Three properties make this more than a missing 434 rows.**

1. **The first diagnosis was wrong, and confidently wrong.** The walk's own
   docstring read the residue as "unreadable but fetchable" and attributed it to
   advancing "one hop per round", giving up when a round had no *new* ancestors.
   Every one of those 432 ancestors was already in `parent`, so **"no new
   ancestors" was correct** — the loop was asking for nodes it already had,
   because it was asking about the wrong node. A wrong diagnosis written into a
   docstring is inherited by the next session as though it were a finding; it is
   corrected in place.
2. **The error's direction was the convenient one, twice over.** The unresolved
   rows were exactly the *deeply nested* ones. Excluding them reweights the
   population toward depth 0, which is the stratum with the **highest** reply
   rate. The bug also **erased the deep tail from the stratum table entirely** —
   the reader could not see that 442 comments had no depth-matched control,
   because those comments had no depth at all.
3. **The gate that could have caught it was the one the walk did not run.** The
   walk exits 0 on the bug it just had. Only reading the committed capture shows
   the residue, which is why `tests/test_need_depth_gate.py` asserts against
   `raw/need_depth.jsonl` and holds the defective loop shape as an explicit
   failing assertion.

**What the bug did not change: the reported result.** The Mantel-Haenszel odds
ratio was **0.701** over the defective capture and **0.703** after the repair,
because the two strata the arm actually uses (depths 0 and 1) were never
affected. **A repaired instrument that returns the same number is a fact worth
recording, not a reason to distrust the number** — but it could only be known
after the repair, and before it the record said 434 comments were unreadable when
none were.

**Two of this session's own measurements were falsified before the record was
complete**, and the pattern is the one this mission has now hit repeatedly: *an
instrument's own docstring was more confident than the instrument.*
`author_build.py`'s predecessor in `run.py` read `h.get("type") == "story"`,
which Algolia's `search_by_date` route never populates — it returned zero rows
for every author and the arm reported "nobody built anything", F002's shape
exactly. It is left in `run.py` as a function that raises, naming the live file.

Ceiling: one repair, one experiment. The generalisable rule is narrow and is
already D025's: **a walk that terminates on a round with nothing new to do has
not converged, it has stalled, and the two look identical in a log.**
## F043 — the number that carried E022's conclusion is the ordinary base rate of a Hacker News conversation

Source: session `2026-10-05-009`, T-0067. Raw results:
[`EXPERIMENTS/023-served-baseline/results.json`](EXPERIMENTS/023-served-baseline/results.json).
Labels, one note per row: [`EXPERIMENTS/023-served-baseline/raw/labels.tsv`](EXPERIMENTS/023-served-baseline/raw/labels.tsv).
Instrument `observed` 2026-10-05.

**The claim withdrawn.** E022 measured that a need statement is answered 58.0% of
the time, and that when a reply exists something serving it is named in **38.5%**
of a hand-labelled sample (15/39). From those two the record concluded the corpus
is "a population of needs the world **absorbed conversationally** rather than one
awaiting a builder", and `STATE-next-actions.md` item 0 was narrowed on it.

**The measurement was inadequate, not the approach.** No control was ever run on
the `served` cell. E022's C1 and C2 both measure `answered` — whether a reply
exists — while its own protocol states "`answered` is not `served`". The cell
carrying the conclusion was the only cell with no counterfactual.

**Measured, `observed`.** Control arm: ordinary comments in the **same stories**,
matching none of the 23 trigger phrases, **restricted to answered** so both arms
share the "a reply exists" condition.

| arm | served | rate | Wilson CI95 |
|---|---|---|---|
| need statements | 15/38 | 0.395 | [0.256, 0.553] |
| **ordinary comments, same stories** | 14/38 | **0.368** | [0.234, 0.527] |

Difference **0.026**, intervals overlapping across nearly their whole width. The
protocol declared that overlap reads `not informative`, and it does.

**The rubric is not why.** Two readers labelled the **identical 39 rows** — this
one blind to E022's labels before writing its own — and agree at **κ = 0.9226**
(raw agreement 0.9487, two disagreements, both `partial` versus `not_served`).
Gate B3 passed, so the null is about the population and not about a reader who
cannot tell the categories apart. E022's recorded limit, "40 labels from one
reader with no second coder", is now a measured magnitude rather than a caveat.

**What this does not touch.** E022's two other numbers stand, and one of them is
the sharpest thing the corpus has produced: **58.0% of 1401 stated needs drew a
reply**, and **0 of 24 requesters whose need went unserved built it themselves**.
Nothing here reopens them, the 589 unanswered statements, the prior-art screen,
or any of the twelve deaths.

**What it does change is the inference.** A reply naming an artifact is a pointer,
and on this population it is **not distinguishable from what an ordinary comment
in the same thread receives**. So the 0.385 was never a rate *about needs*; it
was a rate about Hacker News that the record read as a rate about needs. The
corpus is still a population the world mostly absorbed in thread — that
conclusion now rests on `answered` and on the build arm, which are the two cells
that were measured — but the sentence that made it sound like a demand-side
discovery is withdrawn.

**The pattern, which is the transferable part.** Two neighbouring cells now say
the same thing: a comment matching a need trigger is answered at lift **0.703**
(E022's gate A2, declared floor 1.0) and is served at **0.026 above ordinary
conversation** (this experiment). A trigger vocabulary can find people who state
needs and be **invisible to what happens to those needs next**. That is the
generalisable claim, and it bounds every outcome measured from a
trigger-harvested corpus — this one included.

**Ceiling.** One community, one observation day, 38 rows per arm; a difference
below roughly 0.2 is unresolvable at this sample size, so the honest reading is
that a small need effect is not excluded. The control arm is defined by *not
matching the trigger vocabulary*, which may still catch a need phrased
unusually, making 0.026 a lower bound rather than an estimate. `served` is
labelled, not measured, and both arms carry that equally.

**One instrument fact, and a control that failed for the wrong reason.**
Firebase answers **HTTP 200 with the literal body `null`** for an absent comment
id; Algolia answers 404. The first falsification run asserted a 404 and returned
exit 3 on a healthy reader — a control that fails on a status code the API never
uses would have rejected a working instrument. Repaired to assert **no reply
tree**, which is the property C3 exists to test. E022 had already named this
shape `null_body`; it was re-derived here rather than read.

