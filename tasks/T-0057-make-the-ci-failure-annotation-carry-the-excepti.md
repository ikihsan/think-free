<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0057
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-043-t-0057-claim-the-task-and-verify-it
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_ci_failure_annotation -q && tools/origin preflight
-->

# T-0057 — Make the CI failure annotation carry the exception line its window dropped

## Goal

Make the CI failure annotation carry the exception line its window dropped

## Why this matters

The tip was red and nothing could explain it. Runs `37219755262` and `37220040091` failed on **identical bytes** with three different tests failing between them — the shape of an environmental fault, not a defect in the code — and every public annotation ended one frame short of the answer. The `Tests` step printed one `::error` per line, twelve from the `FAIL:` header, and **the exception is the last line of a traceback**. So the mechanism that exists to make a red run explicable was the thing dropping the explanation.

## Preconditions

Nothing in flight on either VM; the previous session's work landed and `session verify` clean.

## Steps

Read the awk out of the workflow and run it on a log shaped like a real one, rather than asserting on a copy that can drift
Anchor the window on the *end* of the block: one command per failure, the header plus the last thirteen lines, joined with `%0A`
Falsify against the defect's own bytes by keeping the previous program in the test and running it on the same log
Renumber to defect 23 and F025 — the other VM took 22 and F024 in the same hour, for an unrelated defect

## Acceptance criteria

- [x] The exception line survives a traceback longer than the window
- [x] Each failure is one command, and a percent is escaped before the join
- [x] The gate reads the awk out of the workflow rather than a copy of it
- [x] The previous program is held dropping the exception, as the direction of the falsification
- [x] The full suite, doc lint and preflight pass

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_ci_failure_annotation -q && tools/origin preflight
```

## Rollback

Revert the awk in `.github/workflows/ci.yml` and `tests/test_ci_failure_annotation.py`; the annotations fall back to one command per line.

## Notes

**The second work collision in a day, and again the numbers that collided were not the work.** This VM's T-0054 duplicated T-0055 (a claim that could not be published); this task's *numbers* collided with T-0056 (a mission record restating an experiment number), while the *defects* were unrelated: theirs is a false number in a document, mine is a window that drops the exception. The `idcheck` detector refused the land and named both, which is the standing rule working — this side renumbered.

**Two bugs the falsification found in the repair, both of the same kind**, and neither would have been caught by a test that only asserted the exception appeared:

1. `printf "...%s\\n"` prints a literal backslash-n, not a newline, so two failures came out as one command with a second `::error` embedded in its message.
2. Escaping `%` **after** inserting `%0A` — the order that looks obviously right — turned the newline escape into `%250A`, collapsing every frame onto one line.

Both are the shape of the repository's own F013, where the awk doubled a percent, and neither was caught by the existing `test_the_tests_step_escapes_a_percent_as_the_toolkit_does`, which asserts on the *presence* of `%25` rather than on what surrounds it.

**What this does not do.** It does not explain `37219755262`. Three tests failed on identical bytes; the whole suite was run repeatedly on this VM without reproducing it, and the exception that would have said why was the part being dropped. The cause is `untested`, and the fixture is the suspect: `make_fleet` copies the whole tooling tree into a fresh bare remote plus two clones **per test class**, which on a 2-CPU runner is the only thing here that scales with the number of tests. Recording it as untested is the honest half; the next run of that tree will now say what it is.