<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# E037 — line-addressable partial staging, `stage-lines` / `stg`

**Status:** `mechanism` and `interface` **supported but narrower than first stated**,
`usefulness` and `adoption` **untested**. Candidate, not product. Started 2026-10-06,
session 2026-10-06-006; revised by E038 (F062–F064, D069) in session 2026-10-06-009.

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
| **KILL-Q** | Does anyone want this? | — (adoption; **not evaluated**, and not a gate this host can settle) |

**KILL-B not met** (no `file:line` in git) — but the search behind it was git's own
documentation only, and E038's search found two tools. **KILL-A not met** — the honest
baselines are E037's 133-line pty driver and `filterdiff`, at 12 of 30 each. **KILL-C not
met** — `stg` 30 of 30 across ten cases and three `diff.context` values, stable.
**KILL-P not met, narrowly**: no CLI tool takes the coordinate, splits a run correctly, and
exits non-zero when it staged something else. **KILL-S and KILL-D not met** — the capability
is asked for by named people in at least three projects, one of them an agent tool, at a
rate of **0.016–0.066** of matching GitHub issues.

Full numbers: [`EXPERIMENTS/037-line-staging/README.md`](EXPERIMENTS/037-line-staging/README.md)
and [`EXPERIMENTS/038-staging-prior-art/README.md`](EXPERIMENTS/038-staging-prior-art/README.md).

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

**KILL-Q is the whole open question and it is `not_evaluated`.** Nothing in E037 or E038 says a
person wants this; both say the interface is thin on the command line. The falsifiable form:
*given a working `stg`, a developer or an agent asked to stage one specific line will use it
rather than `git add -p`, `filterdiff`, or a hand-built patch.*

The cheapest honest test that does not need permission to contact strangers:

1. **The strongest shell baseline, which is not `filterdiff` alone.** `filterdiff` names the
   *original* file's line; `stg` names the working tree's line. A pipeline combining them, or a
   ten-line `git diff -U0` filter, is the real competitor, and it is untested. E038 measured the
   tool, not the best way to use it.
2. **Agent end-to-end, with attempts counted.** Give a coding agent "stage only the line you
   changed" against a real repository and count attempts and wrong answers. `mcp-multi-root-git#3`
   is a real requester of exactly this, so there is a population to instrument, and it is
   measurable offline.
3. **E038's unrun Pool B** — 15 pre-named Stack Exchange phrasings × 2 sites with its negative
   and denominator controls, blocked only by a quota window.
4. Only then, and only with authorisation, the named requesters cited in E038. **Contacting them
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
