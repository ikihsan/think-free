<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0068
status: claimed
created: 2026-10-05
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
claim-agent: unknown-agent
claim-vm:
claim-session: 2026-10-05-010-test-whether-twelve-candidates-twelve-pr
-->

# T-0068 — Classify what killed each candidate, from its primary source

## Goal

Establish by count whether "twelve candidates, twelve prior-art deaths" is true of the primary records, or a figure carried by summaries

## Why this matters

The sentence is load-bearing in `STATE.md`, `HYPOTHESES.md` and
`STATE-next-actions.md`, and it is the stated premise of four experiments
(E015/F034, E016/F035, E017/F037, E021/F041) and of the top open item. If
prior art killed a minority rather than all of them, the dominant kill reason is
something else, and the two diagnoses imply opposite repairs: "the world already
has this" is not fixable by a better prior-art search, while "the claim did not
survive its own test" is. No count exists behind the claim.

## Preconditions

None. No network. The primary sources are in the repository: the six sealed
reports and the experiment records.

## Steps

1. Declaration in `EXPERIMENTS/024-kill-reason-causes/PROTOCOL.md`, written
   before any row was classified: population rule, four categories with
   precedence, both gates, and the control.
2. Take the population from the `RESEARCH/SYNTHESIS.md` inventory table plus
   `tools/origin`. Primary source only; summaries are the object under test.
3. For each row, record the verbatim deciding sentence and assign one category
   by the declared precedence.
4. Run the control: the same rule over F029's 50 already-caused rows. Exact
   match on all four categories, or H1 is `not evaluable`.
5. Report both gates from `results.json`, and name the dominant kill reason if
   H1 is killed.

## Acceptance criteria

Both gates are answered in one direction from `results.json` with the deciding
sentence present for every row, the control's verdict is recorded, and the
finding is written with the weaker claim the evidence supports.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
```

## Rollback

Removing `EXPERIMENTS/024-kill-reason-causes/` removes the measurement; the
records it produced are separate and carry the finding.

## Notes

Declared limits, before the run: one reader and no second coder, which is the
same defect E023 measured on its own labels; the categories are the record's
own vocabulary and the precedence order is a convention that can move a row
across the 50% line. This measures a cause table, not the world.