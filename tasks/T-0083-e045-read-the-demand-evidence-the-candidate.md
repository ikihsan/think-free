<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-07
-->

<!-- task-meta
id: T-0083
status: done
created: 2026-10-07
verify: python3 EXPERIMENTS/045-demand-evidence/read.py
claim-agent:
claim-vm:
claim-session: 
-->

# T-0083 — E045: read the demand evidence the candidate rests on, and ask who the requester is

## Goal

Read, in full, the primary demand evidence behind the only candidate this
mission has produced — F064's 195 harvested GitHub issues and the four of them
the record names — and answer the two questions it never asked: **who** is making
the request, and **which interface does the requester lack**. Then state, from
that evidence, whether the population the in-flight E044 experiment measures is
a real population or an artefact of its own harness.

## Why this matters

The record's demand claim rests on a rate of `0.016-0.066` of matching issues
and on **four named issue threads**. Three of the four are requests filed by
people at an editor GUI. The record then carries a claim about "an agent that
must discover which line changed, with no diff and no line number" — and that
population was produced by the experiment's own harness, not found in the
demand evidence. If the evidence contains no such requester, then a clean or
dirty E044 result is a statement about a population the record invented, and the
candidate's remaining population is the with-diff one that E043 already measured
at 3 of 3 correct with no tool present.

This is not a re-audit of a selection method. It is the reading of primary
evidence the record cites but has not read, and it names the decision it
changes: **which population the candidate is allowed to be evaluated against.**

## Preconditions

The corpus is cached in `EXPERIMENTS/038-staging-prior-art/raw/requests.jsonl`
(65 search-API responses, the `need` arm carrying the harvested issues). No
network is needed for the corpus itself; thread bodies may need a fetch, and if
the fetch is unavailable the missing half is recorded rather than guessed.

## Steps

1. Extract every issue in the cached corpus with its title, body and repository,
   and record the total as the denominator the record's rate is a fraction of.
2. Locate the four issues the record names (`sublime_merge#976`,
   `vim-gitgutter#446`, `sublime_merge#465`, `mcp-multi-root-git#3`) and read
   each in full, verbatim, not from the record's summary of it.
3. For each, record: what operation is requested; who the requester is (a person
   at a GUI, a script, a CI job, a coding agent); what the requester says they
   can and cannot do; and whether the request names any interface the requester
   lacks.
4. Classify the whole corpus against the same two questions, so the four named
   rows are a sample of a counted population rather than a selected list.
5. Record the result, the finding, and the decision.

## Acceptance criteria

A table over the corpus with the requester class and the "interface the
requester lacks" class per issue; the four named issues quoted in full; a stated
count of how many corpus issues describe a requester **without diff access**;
and a conclusion that either supports or refutes the population E044 measures.
The count must be a count over a declared denominator, not a rate across readers.

## Verification

```bash
python3 EXPERIMENTS/045-demand-evidence/read.py
```

## Rollback

Read-only over cached evidence. All output under `EXPERIMENTS/045-demand-evidence/`.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.