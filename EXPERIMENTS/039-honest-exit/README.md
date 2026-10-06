<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E039 — does `stg`'s honest-exit claim survive the boundary cases an agent workflow produces?

**Date:** 2026-10-06. **Status:** complete. **Verdict:** the claim holds on all eight
boundaries measured; it is not contradicted by any case.

## Question

E037/E038 established that `stg` answers its operation 30 of 30 against the incumbent
routes' 6–12 of 30, and that the three alternatives returned **78 wrong-but-exit-0
rows** in E038's table. The candidate's own central promise (its README: *"if it did
not stage what you asked for, it says so instead of exiting 0"*) is an **exit-code
contract**, and E038's oracle did not test one thing: what `stg` itself does at the
edges of what it can express. An agent workflow hits exactly those edges — untracked
files, binary blobs, renames, mode changes, conflict markers, and requests past the
end of the file.

## Contract under test

`stage-lines/README.md`: `0` = nothing matched, `1` = something staged, `2` = usage or
git error. (Unusual, but documented.) Honest means: the process did not exit 0/1
(“staged”) while leaving the index unchanged, and did not stage anything while
exiting non-zero in a way that claims refusal — both directions checked.

## Method

`run.py` builds eight real git repositories (no mocks), one per boundary case, runs
`stg stage` against each, and records exit code, stderr, and `git show :<path>` before
and after. The naive route (`git diff -U0 | filterdiff --lines=N | git apply
--cached --unidiff-zero`) is run on an identically-built ninth repository per case for
contrast. Raw: `raw/results.jsonl`, `raw/naive.jsonl`.

## Observed

| case | stg exit | index changed | refusal, non-zero | naive route |
|---|---|---|---|---|
| binary-file | 2 | no | `b.bin is binary` | exit 128, `unrecognized input` |
| untracked-file | 2 | no | `no stage change in new.txt` | exit 128 |
| out-of-range-line | 2 | no | `f has 3 lines; you asked for 99` | exit 128 |
| missing-path | 2 | no | `no stage change in nope.txt` | exit 128 |
| conflict-markers-in-file | 1 | yes | (content, staged as asked) | exit 0, staged |
| rename-mv | 1 | yes | (staged the edit on line 2) | exit 0, staged |
| mode-change-only | 2 | no | `no stage change matches run.sh:1` | exit 128 |
| already-partially-staged | 1 | yes | (staged only the requested line) | exit 0, staged |

**8 of 8** `stg` runs exited 2 with a named refusal when it did not stage, and exited
1 after changing the index to exactly the requested change. Zero index changes hidden
behind exit 0; zero wrong stagings hidden behind exit 1; the staged bytes were verified
against `git show :<path>`. The naive route failed with git's own 128 + `unrecognized
input` on five of the eight and silently staged on three — it cannot distinguish “the
request was invalid” from “the patch applied” by exit code alone.

Two honest limitations of `stg` surfaced, both already documented in its README and
both refusing loudly (exit 2) rather than silently: **binary files** and
**mode-change-only** requests are not stageable through it, despite a line address
existing. A rename showed no worse failure — its edit still staged by line, but the
rename record itself is git's, not `stg`'s.

## Verdict and next action

The honest-exit claim is **supported, not contradicted**, on the exact failure modes a
non-interactive caller produces; it holds where the naive route either errors opaquely
(128) or exits 0 without distinction. Combined with E038's 30/30, the candidate's
capability and its honesty at the boundary are both measured and both stand. Still
**not measured**: whether anyone wants it (KILL-Q, `not_evaluated` by five experiments
now). That remains the only open gate on this candidate, and it is not closable by a
local oracle.
