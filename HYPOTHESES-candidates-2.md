<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# Candidate record — readings that revised E037

Split out of [`HYPOTHESES-candidates.md`](HYPOTHESES-candidates.md) on
2026-10-07 at the 300-line cap, and by invariant. That file holds the
candidate's *current* claim, its gates and its standing; this one holds the
per-experiment readings that claim was revised against, in the order they
happened, so that revising the claim does not require rewriting the history.

## E041 — strongest shell baseline falsifies mechanism differentiation

E037 hypothesized that "a ten-line `git diff -U0` filter" could be the real competitor to
`stg`. E040 compared `stg` against a naive approach and found a practical difference.
E038 compared against `filterdiff` and `git add -p` via pty and found `stg` superior.
But neither tested the **strongest achievable shell baseline** — a script that correctly
implements the line-pairing split logic.

E041 builds `shell_baseline.py` (~180 lines of Python) implementing the same algorithm
as `stg`: parse `git diff -U0`, pair removes with adds line-for-line, split surplus adds
per-line, select the hunk covering the requested working-tree line, apply via
`git apply --cached --unidiff-zero`, return honest exit codes.

**Result: the shell baseline matches `stg` exactly and honestly on all tests.**

| Test suite | stg | shell_baseline |
|------------|-----|----------------|
| E040 agent-style (5 cases) | 5/5 exact, 5/5 honest | 5/5 exact, 5/5 honest |
| E038 full matrix (10 cases × 3 diff.context = 30 rows) | 30/30 correct | 30/30 correct |

**Kill gate met:** a well-implemented script achieves parity with `stg` on correctness
and honesty. The mechanism is not the differentiator — the differentiator is packaging
(a ready-to-use, tested, documented CLI tool vs. writing/maintaining your own script).

Full numbers: [`EXPERIMENTS/041-strongest-baseline/README.md`](EXPERIMENTS/041-strongest-baseline/README.md).

## Two bugs E038 found in `stg`, and why E037's 6 of 6 missed them

E037's oracle read `staged_anchors` — the line numbers of the hunks now in the index. A hunk
carrying two changes when one was asked for still prints one clean hunk at the right anchor,
so it scored as correct. E038's oracle reads the index **content**.

- **Adjacent insertions were staged whole.** `stg f:4` on a two-line insertion staged both and
  exited 0. E037's test asserted this as intended, in a comment: *"there is no valid hunk for
  half of a two-line insertion"* — **a premise that was wrong**, since git apply takes
  `@@ -3,0 +4,1 @@` then `@@ -3,0 +5,1 @@` over the same `@@ -3,0 +4,2 @@`. Fixed, and the
  test now asserts the corrected behaviour.
- **A coordinate offset bug in the fix** — the surplus adds start at content index
  `nrem + pairs`, not `nrem`, because the removes come first and then the already-paired adds.
  Caught by the new test, not by inspection.
- **Deletions stay whole, deliberately**: consecutive deletions share one address, so splitting
  them would add length to `stg list` and no reach. I tried it, reverted it, and wrote down why.

30 tests, all against real git repositories, no mocks.

## What would falsify the useful claim

**KILL-Q is the whole open question and it is `not_evaluated`.** Nothing in E037–E041 says a
person wants this; all say the interface is thin on the command line. The falsifiable form:
*given a working `stg`, a developer or an agent asked to stage one specific line will use it
rather than `git add -p`, `filterdiff`, or a hand-built patch.*

**E041 tested the strongest shell baseline (item 1 above) and the kill gate for mechanism
differentiation is met.** A ~180-line Python script implementing the same splitting logic
matches `stg` on all 35 test rows (5 E040 + 30 E038). The practical advantage E040 measured
was against a naive baseline, not the strongest achievable one.

Remaining honest tests that do not need permission to contact strangers:

1. **Agent end-to-end, with attempts counted.** Give a coding agent "stage only the line you
   changed" against a real repository and count attempts and wrong answers. Compare `stg` vs
   the agent writing its own script vs. `filterdiff` vs. naive `git add -p`. `mcp-multi-root-git#3`
   is a real requester of exactly this, so there is a population to instrument, and it is
   measurable offline.
2. **E038's unrun Pool B** — 15 pre-named Stack Exchange phrasings × 2 sites with its negative
   and denominator controls, blocked only by a quota window.
3. Only then, and only with authorisation, the named requesters cited in E038. **Contacting them
   is outside current permissions** and is not proposed here.

## E046 — the packaging claim, measured on real changes, did not hold

Full reading: [`HYPOTHESES-results-3.md`](HYPOTHESES-results-3.md).

## Mechanism, stated separately from usefulness

`stg` parses `git diff -U0` into the smallest hunks `git apply --unidiff-zero` accepts. Removed
and added lines pair up line for line — the rule VS Code's own implementation uses, and which
`git add -p`'s `s` cannot apply inside a run of adjacent changes. A run of consecutive
insertions splits one line at a time, because each is its own line in the file as it reads now.
Each change is addressed by its first line in the file as it reads now; a deletion is addressed
by the line whose content moved up, so every addressable change names a line that exists.
Correctness is checked against git itself: on a real file in this repository the resulting
`.git/index` is **byte-identical** to the one a hand-built patch leaves.

## Ceiling

Two platforms (git 2.25.1, patchutils 0.3.4), ten synthetic cases, one file per case, one
`diff.context` sweep. No renames, mode changes, untracked files, `--intent-to-add` or
`diff.algorithm`. Prior art was found through three primary sources and two code indexes;
**GitHub code search answered 401, grep.app 429, codesearch.debian.net 403, and the web search
tool was unavailable on this host**, so "no prior art" is narrowed, not established — and
E038's own finding of `filterdiff` and VS Code is the proof of that. The
gap is on the interface, not the capability, and an interface gap is the kind that closes
quietly: if a future git takes `file:line`, this is dead, and the check is one command.

**E041 ceiling:** The shell baseline is Python, not pure shell (awk/sed). A pure shell
implementation would be significantly harder and more fragile. The baseline implements
`stg`'s exact algorithm — it's not an independent alternative. The "independent
implementation arriving at the same mechanism" (VS Code's `git.stageSelectedRanges`, F062)
is evidence the mechanism is natural, not that it's trivial to reimplement. Only tested on
git 2.25.1. Git 2.55.0 (CI runner) may behave differently. Does not test renames, mode
changes, `--intent-to-add`, `diff.algorithm`, binary files, untracked files, or conflicted
merges — same ceiling as E038. KILL-Q remains `not_evaluated` for the fifth experiment.

## E042 — agent end-to-end test confirms packaging advantage

**E042 tested the remaining honest test from E041 (item 1): agent end-to-end with attempts
counted.** Eight realistic staging scenarios run against four approaches:

| Approach | Success | Silent Failure | Agent Code Lines |
|----------|---------|----------------|------------------|
| **stg** | **1.00** | 0.00 | **1** |
| **shell_baseline** | **1.00** | 0.00 | 180 |
| filterdiff | 0.00 (unavailable) | 0.00 | 1 |
| naive_git_add_p | 0.62 | **0.38** | 50 |

**Key findings:**

1. **Mechanism parity confirmed**: shell baseline matches stg exactly (100% both), confirming
   E041. The mechanism is not the differentiator.

2. **Packaging is the differentiator**: stg requires **1 line** of agent code vs **180 lines**
   for the shell baseline — a **180× reduction** in code the agent must write, maintain, and
   debug.

3. **Naive approach is unsafe**: 38% silent failure rate (stages wrong lines, exits 0),
   matching E038's finding that the naive route "exited 128 on five, silent success on three".

4. **Failure modes**: naive approach fails precisely where line-level splitting matters:
   adjacent modifications, multi-line insertions, multiple scattered changes.

**KILL-Q update for agent usability**: For a coding agent, stg provides a significant
practical advantage — 100% vs 62% success, 0% vs 38% silent failures, 1 vs 180/50 code lines.
The mechanism works; the differentiator is packaging. KILL-Q remains `not_evaluated` for
*daily human adoption* but is **strongly supported for agent usability**.

Full numbers: [`EXPERIMENTS/042-agent-staging-e2e/README.md`](EXPERIMENTS/042-agent-staging-e2e/README.md)
and [`EXPERIMENTS/042-agent-staging-e2e/results.json`](EXPERIMENTS/042-agent-staging-e2e/results.json).

**E042 ceiling:** Eight scenarios, one VM, simulated agent (not a real coding agent).
The naive approach model may not match what a real agent would write. filterdiff unavailable
on this host. Only git 2.25.1 tested. The 180x code reduction assumes the agent would
otherwise write the shell baseline from scratch — a real agent might copy-paste or import.

---

## E043 — the agent-usability claim, run against real agents (F075)

`observed` 2026-10-07, session 2026-10-07-001. Evidence:
[`EXPERIMENTS/043-real-agent-staging/README.md`](EXPERIMENTS/043-real-agent-staging/README.md).

E042's own ceiling said "simulated agent (not a real coding agent)". E043 ran six
real agents on six real repositories — one committed file, a real dirty working
tree, the instruction *"stage ONLY the change on line N; leave every other change
unstaged"* — scored against a hand-written oracle that no agent could read.

| arm | verdict | used `stg` |
|---|---|---|
| no tool offered (3 scenarios) | **3/3 exact** | n/a |
| `stg` on `PATH`, named as available (3) | **3/3 exact** | **1 of 3** |

**6 of 6 exact. Every `nostg` agent independently converged on `git diff` →
hand-write a minimal patch → `git apply --cached`, one call each, no code
written.** 2 of the 3 that had `stg` installed declined to use it.
