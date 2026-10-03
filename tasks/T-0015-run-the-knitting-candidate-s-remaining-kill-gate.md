<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0015
status: claimed
created: 2026-10-03
claim-agent: opencode
claim-session: 2026-10-03-028-run-the-knitting-candidate-s-remaining-k
claim-vm: instance-20260717-0947
verify: test -f RESEARCH/PRIOR-ART-KNITTING.md && for f in origin-meta 'Prior art' Inspected Difference 'Why it matters' 'Surviving risk' Confidence 'Query log' Verdict; do grep -q "$f" RESEARCH/PRIOR-ART-KNITTING.md || exit 1; done && grep -q 'PRIOR-ART-KNITTING.md' HYPOTHESES.md && grep -q 'PRIOR-ART-KNITTING.md' STATE.md && tools/origin doc lint
-->

# T-0015 — Run the knitting candidate's remaining kill-gate prior-art check: does

## Goal

Run the knitting candidate's remaining kill-gate prior-art check: does existing tooling already supply equivalent intervention sequences?

## Why this matters

HYPOTHESES.md's knitting kill gate has one untested condition: 'Abandon the algorithmic-advantage claim if existing graph tooling already supplies equivalent intervention sequences'. Stage A is settled (T-0010, T-0011), so this literature question is the only remaining cheap test. STATE.md ranks it first and forbids a third synthetic planner experiment. C.md searched only user-facing and hobby vocabularies and recorded that no patents were searched, so the adjacent industrial-knitting and graph-rewriting vocabularies are genuinely unqueried.

## Preconditions

RESEARCH/C.md, HYPOTHESES.md, EXPERIMENTS/005-knitting-bounded-search/README.md read; prior-art-check skill loaded; network reachable (doctor probes github_api and arxiv 200).

## Steps

1. Search the user's vocabulary (fix a knitting mistake without unraveling, repair a cable that crossed wrong, frogging). 2. Search the academic term (knit fabric repair planning, stitch graph repair, weft knitting defect repair, unravelling ladder model, industrial mending of knitted fabric). 3. Search the infrastructure term (graph rewriting minimal repair sequence, minimum-cost edit plan over a dependency graph, repair planning in graph transformation). 4. Open what is found, including limitations, known-issues pages, abandoned attempts and one patent search. 5. For each prior-art item record Source, Date, What it does, Evidence actually read, Status, Gap only if verified. 6. State the difference in one sentence and answer why a user would switch. 7. Judge the kill-gate condition and record it: abandon or narrow.

## Acceptance criteria

- [ ] Report written with all six prior-art-check fields (Prior art, Inspected, Difference, Why it matters, Surviving risk, Confidence) and a query log naming databases, languages and what was NOT searched.

## Verification

```bash
test -f RESEARCH/PRIOR-ART-KNITTING.md && for f in origin-meta 'Prior art' Inspected Difference 'Why it matters' 'Surviving risk' Confidence 'Query log' Verdict; do grep -q "$f" RESEARCH/PRIOR-ART-KNITTING.md || exit 1; done && grep -q 'PRIOR-ART-KNITTING.md' HYPOTHESES.md && grep -q 'PRIOR-ART-KNITTING.md' STATE.md && tools/origin doc lint
```

## Rollback

Delete RESEARCH/PRIOR-ART-KNITTING.md and revert the HYPOTHESES.md/STATE.md rows; no code or product depends on a prior-art report.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
