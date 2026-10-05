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