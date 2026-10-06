<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# E040 — stg's interface claim, tested in an agent-style loop

E037 measured the interface cost of `git add -p` (a 133-line pty driver, 4 of 6);
E038 measured correctness against the index (stg 30 of 30); E039 measured
honesty at the failure edges (8 of 8). None of them ran the operation the way
the candidate's demand evidence points at: **a stateless caller that reads a
request, issues tool calls, and must know from the output alone whether the
staging it asked for happened.** `mcp-multi-root-git#3` states exactly that
case. E040 runs it.

## Method

`run.py` builds five real repositories (case table embedded; no mocks), runs
each request through three routes, and scores the result against a literal
expected staged blob — not against a re-derivation of the selector:

| route | what the caller does |
|---|---|
| stg | one call: `stg stage f:L` |
| plumbing | `git diff -U0`, keep hunks whose new-side span covers L, `git apply --cached --unidiff-zero` |
| filterdiff | `git diff -U0 \| filterdiff --lines=L \| git apply --cached --unidiff-zero` |

Requests: adjacent modified lines (ask for 2 of 2), a two-line insertion (ask
for 1), a single-line insertion, a last-line edit, and a line that did not
change. Per (case, route): exit code, tool calls, bytes read by the caller,
exactness, honesty, silent over-staging.

## Observed

| case | route | exit | calls | bytes | exact | honest | silent wrong |
|---|---|---|---|---|---|---|---|
| adjacent-modifications | stg | 1 | 1 | 10 | yes | yes | no |
| adjacent-modifications | plumbing | 0 | 2 | 10 | **no** | **no** | **yes** |
| adjacent-modifications | filterdiff | 0 | 3 | 93 | **no** | **no** | **yes** |
| two-line-insertion | stg | 1 | 1 | 10 | yes | yes | no |
| two-line-insertion | plumbing | 0 | 2 | 10 | **no** | **no** | **yes** |
| two-line-insertion | filterdiff | 128 | 3 | 26 | no | no | n/a (opaque) |
| single-line-insertion | stg | 1 | 1 | 10 | yes | yes | no |
| single-line-insertion | plumbing | 0 | 2 | 10 | yes | yes | no |
| single-line-insertion | filterdiff | 128 | 3 | 26 | no | no | n/a (opaque) |
| tail-modification | stg | 1 | 1 | 10 | yes | yes | no |
| tail-modification | plumbing | 0 | 2 | 10 | yes | yes | no |
| tail-modification | filterdiff | 0 | 3 | 85 | yes | yes | no |
| unchanged-line | stg | 2 | 1 | 33 | yes | yes | no |
| unchanged-line | plumbing | 2 | 1 | 22 | yes | yes | no |
| unchanged-line | filterdiff | 128 | 3 | 26 | yes | yes | no |

Totals: **stg exact and honest 5 of 5, one call, 10–33 bytes**. Plumbing
exact 3 of 5 — and both failures are *silent* (exit 0, wrong staged content).
filterdiff exact 2 of 5, opaque 128 on 2 of 3 insertion requests, silent
over-stage on 1.

## Why the plumbing route cannot win

On adjacent modifications, git itself reports **one** hunk
(`@@ -1,2 +1,2 @@`). A caller slicing `git diff` recovers no split from it —
the information is gone before the caller sees it. The plumbing route staged
both lines in 2 of 5 cases while exiting 0. stg's library splits the hunk
into per-line pairs that `git apply` accepts; that split is the mechanism the
caller would otherwise have to implement itself.

## A finding about the artifact, not the routes

`stage-lines/README.md` claims a half of a two-line append "is not a thing
`stg` will pretend to stage." Observed: current `stg` stages exactly the
asked-for line of a two-line insertion and exits 1 (the E038 fix behavior).
The README was stale; corrected in the same change.

## Verdict and next action

The interface claim **survives in the agent setting, narrowed as F062 says**:
no other command-line route takes `file:line`, splits adjacent changes, and
fails loudly — here measured as 5 of 5 against 3 of 5 (with both misses
silent) and 2 of 5 (with opaque and silent misses). **KILL-Q remains
`not_evaluated`.** Five experiments now; no local oracle closes it.
Raw: `raw/results.jsonl`.
