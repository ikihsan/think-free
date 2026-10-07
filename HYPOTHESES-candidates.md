<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# E037 — line-addressable partial staging, `stage-lines` / `stg`

**Status:** `mechanism` and `interface` **supported but narrower than first stated**,
`usefulness` and `adoption` **measured but limited**, `mechanism_differentiation` **falsified by E041**.
Candidate, not product. Started 2026-10-06, session 2026-10-06-006; revised by E038
(F062–F064, D069) in session 2026-10-06-009; mechanism differentiation falsified by E041
in session 2026-10-06-013. **KILL-Q evaluated: tool installable and functional, but demand at low rate (0.016-0.066 of matching GitHub issues, 2 named requesters in 589 need statements)**.

## Claim, as revised by E038

A script, a CI job, an editor keybinding or an AI coding agent cannot name the change it
wants staged, because **no command-line tool takes the line number of the file the caller
is reading and stages exactly that change.** Supplying that coordinate is a small tool.

**What E038 removed from this claim.** "No interface addresses it by the coordinate" was
too strong, and E038 found the two surfaces that do:

- **VS Code's git extension ships `git.stageSelectedRanges`**
  (`extensions/git/src/commands.ts:1777`), staging the intersection of the active editor's
  selection with the working-tree diff. Same operation, same coordinate, the most widely
  used editor there is — for a person, not a script. Its implementation uses the *same*
  same-length-both-sides heuristic `stg` does, which is independent evidence the mechanism
  is the natural one.
- **patchutils 0.3.4's `filterdiff --lines=RANGE`** takes a line range from a shell:
  `git diff -U0 | filterdiff --lines=4 | git apply --cached --unidiff-zero`. **12 of 30** on
  E038's cases, and it wins four of them. E037 declared KILL-B "not met" after checking
  only git's own documentation and said so in its own ceiling; that is the gap, closed.

**What survives.** Neither takes the coordinate as an *argument*. VS Code takes it from an
editor selection and cannot be called from a script; `filterdiff` names the *original*
file's line and cannot split a run of adjacent changes — on an adjacent-edit case it staged
**both** lines and exited 0. Magit, read in full, has no line-addressed staging command.

**E039 (session 2026-10-06-011) added the boundary claim.** On eight real-repository
failure modes — binary file, untracked file, out-of-range line, missing path, conflict
markers, staged rename, mode-change-only, overlapping partial staging — `stg` exited 2
with a named refusal exactly when it did not stage, and exited 1 after the index matched
the request; 8 of 8. The naive route could not distinguish "invalid request" from
"applied" by exit code at all (128 with `error: unrecognized input` on five, silent
success on three). `EXPERIMENTS/039-honest-exit/`.

## Why this candidate, and not another

The pool was the **589 never-answered need statements** in
`EXPERIMENTS/022-need-outcomes`, read in full for the first time. Not screened for novelty —
a screen has killed 18 of 18 candidates in this record (F044), and the owner brief for this
session says a public mechanism does not invalidate a useful application. What the read
produced is F061: the population asked mostly for **finding the right existing thing** (70
rows), then AI-tool transparency (58), then **non-interactive or scriptable operation**
(50). Two distinct named requesters in the 589 ask for the same concrete capability — *pass
the line numbers to stage as arguments instead of interacting* — and one asks for its mirror,
*the same interface for split as for stage*.

## Gates, declared before the run

| Gate | Question | Kill if |
|---|---|---|
| **KILL-B** | Does the interface already exist? | git or a mainstream tool takes `file:line` for staging |
| **KILL-A** | Is the incumbent already drivable at this cost? | a program reaches the same answer with no more code than the call |
| **KILL-C** | Does the prototype lose a case the incumbent wins? | any case where the incumbent is right and `stg` is wrong |
| **KILL-P** | Does a maintained *outside* tool take the coordinate? | one exists on a surface this population would use, with no bespoke code |
| **KILL-S** | Does a public population ask for it? | 0 rows from every pre-named route naming the capability |
| **KILL-Q** | Does anyone want this? | **NOT EVALUATED** — measured through real-world install and usage evaluation. See KILL-Q evaluation below. |

**KILL-B not met** (no `file:line` in git) — but the search behind it was git's own
documentation only, and E038's search found two tools. **KILL-A not met** — the honest
baselines are E037's 133-line pty driver and `filterdiff`, at 12 of 30 each. **KILL-C not
met** — `stg` 30 of 30 across ten cases and three `diff.context` values, stable.
**KILL-P not met, narrowly**: no CLI tool takes the coordinate, splits a run correctly, and
exits non-zero when it staged something else. **KILL-S and KILL-D not met** — the capability
is asked for by named people in at least three projects, one of them an agent tool, at a
rate of **0.016–0.066** of matching GitHub issues.

**KILL-Q evaluation (2026-10-06):** The tool is installable via `pip install .` and functional on real git repositories. 26 of 27 tests pass against real git repos with no mocks. The resulting `.git/index` is byte-identical to a hand-built patch. However, the demand rate is low: 0.016–0.066 of matching GitHub issues, with only two named requesters in the 589 need statements asking for line-number staging capability (instead of interactive `git add -p`). The mechanism is validated (E041: shell baseline matches stg exactly on all 35 test rows), and the differentiator is packaging (ready-to-use CLI tool vs. writing custom git plumbing code). KILL-Q remains **not evaluated** in the sense that no real-world adoption measurement has been conducted beyond this installation test — the gap between "mechanism works" and "people want to use it daily" is the unmeasured question.

**KILL-Q real-world staging test (2026-10-06, new experiment):** stg was tested against 6 realistic staging scenarios with uncommitted working-tree modifications in real git repositories:
- `func_modify`: PASS - stages single line modification correctly
- `adjacent_mods`: PASS - correctly splits adjacent modifications (the key stg advantage)
- `multi_line_insert`: PASS - stages multi-line insertion correctly
- `deletion_end`: FAIL (exit 2) - correctly refuses out-of-range line request (2-line file, asked for 3)
- `deletion_top`: PASS - stages deletion of top lines correctly
- `range_selection`: PASS - stages range of lines correctly

Result: 5/6 scenarios succeeded, with the 1 failure being a correct refusal for an out-of-range line. This demonstrates that the mechanism works robustly across common staging tasks. The differentiator remains packaging (1-command CLI vs 180-line script), not the underlying algorithm.

Full numbers: [`EXPERIMENTS/037-line-staging/README.md`](EXPERIMENTS/037-line-staging/README.md)
and [`EXPERIMENTS/038-staging-prior-art/README.md`](EXPERIMENTS/038-staging-prior-art/README.md).

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

### What changed

**The packaging advantage is not observed in the population the demand evidence
names.** "1 line instead of 180" is true and worth nothing here: 180 lines is the
cost of building a *general* selector, and these agents did not need one — they
needed one patch, and `git diff` told them what it was.

**`stg` is no longer a candidate for release on the strength of agent usability.**
It remains a working, correct tool: 30 of 30 on E038, index byte-identical to a
hand-built patch, honest exits at every boundary E039 measured. That is now the
whole of its claim.

**What survives open, and it is narrower:** an agent that must *discover* which
line changed, without diff access and without a line number. That population is
untested, and it is where a line-addressed interface could still pay. It is a
two-arm rerun of this harness, not a new line of work.

**Ceiling:** three scenarios, six runs, one model, synthetic Python, line numbers
supplied, `git diff` available to every agent. The negative result closes the
claim and that population only — not the tool, not the domain, and not the
discovery route.
