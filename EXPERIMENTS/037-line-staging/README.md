<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E037 — can a program select one change by line number, and what does it cost?

`observed` 2026-10-06, session 2026-10-06-006, VM `instance-20260717-0944`, git 2.25.1,
Python 3.8.10. **No network.** Raw results: [`raw/compare.jsonl`](raw/compare.jsonl) (one
JSON object per line). Reproduce: `python3 EXPERIMENTS/037-line-staging/compare.py`.
Verdict: **the mechanism is not already public as a first-class interface, and the
prototype is 6 of 6 where the incumbent needs a program and gets 4 of 6.**

This is the first experiment in this record whose subject is a **candidate being built**,
not a population being measured. The prototype is [`stage-lines/`](../../stage-lines/); its
own tests are 28 cases against real repositories, `python3 stage-lines/test_stg.py`.

## The question, and what would have killed it

`git add -p` selects part of a file. It has no non-interactive equivalent. **Is that a gap
in git, or is it a gap only for people who cannot type at a terminal?** If a program can
drive `git add -p` correctly, the candidate is prior art and nothing is built.

**Declared kill conditions, fixed before the run.** Kill if any of:

- **KILL-A** a program can drive `git add -p` to select a named line with no more code than
  the call itself;
- **KILL-B** git or a mainstream tool already takes `file:line` for staging;
- **KILL-C** the prototype loses a case the incumbent wins.

KILL-B was checked first, in about four commands, because **D067** requires a
mechanism-bearing candidate to be tested against that mechanism's existing source before any
population is measured for it.

## KILL-B, checked against the mechanism's own source

`git add --help` on this host lists `--interactive` and `--patch` and nothing that takes a
line number. Three routes were tried on a concrete file (`g.txt`, four edits, want the
third):

| Route | Result |
|---|---|
| `git add -p` with keys on a pipe | **not** ignored, contrary to this record's first reading. It applied what it could and stopped at EOF, staging **0** of 4 and **exiting 0**. |
| `git add --patch` under a pty | works, but git presents all four edits as **one** hunk at its default `diff.context`, so `y` takes all four. |
| `git add g.txt:2` | `fatal: pathspec 'g.txt:2' did not match any files` |
| `git apply --cached` on a sliced patch | needs the `diff --git` header re-typed by hand, and a `-U0` hunk is rejected without `--unidiff-zero` (verified: `error: patch failed: nl.txt:1`). |

**KILL-B not met.** The interface does not exist. The earlier "piped keys are ignored"
reading is corrected here: the keys were read, the run ended early, and **the exit status
was 0**. That is the finding, and it is worse than being ignored.

## The comparison

Six cases, each asked for the same thing: stage the change on a given working-tree line and
no other. Three routes:

- **`stg`** — `stg stage f:N`. The line number and nothing else.
- **`pty_driver`** — `git add -p` driven through a real terminal by a program written
  specifically to overcome what makes the interface awkward. Held in
  [`driver.py`](driver.py) **on its own so its size can be counted: 133 lines.** This is the
  strongest form of the incumbent, not a strawman.
- **`naive`** — the keys a first-try script writes: count the hunks at `-U0`, answer each.
  Derived once at git's default context and replayed, because that is the only way a script
  can use them.

Every route was run at `diff.context` 1 and 3 as well as unset.

## The result

| Case | asked for | `stg` | `pty_driver` | `naive` |
|---|---|---|---|---|
| modify one of three | line 4 | **[4]** | [4], 4 steps 1 split | **[]** |
| deletion among edits | line 3 | **[3]** | **[]**, 3 steps | **[3, 5]** |
| insertion among edits | line 5 | **[5]** | [5], 1 step | [5] |
| adjacent edits | line 2 | **[2]** | **[]**, 3 steps | **[]** |
| append at eof | line 4 | **[4]** | [4], 1 step | [4] |
| adjacent inserts | line 4 | **[4]** | [4], 1 step | [4] |

**`stg` 6 of 6, identical at every `diff.context`. `pty_driver` 4 of 6 for 133 lines of
caller code. `naive` 3 of 6.**

**KILL-C not met.** KILL-A not met, and the two failures name the reason.

## Why the incumbent's route fails, precisely

Both `pty_driver` failures have one cause, and it is not the driver's cleverness:

**`git add -p`'s `s` splits only at context boundaries.** For two adjacent modified lines
git emits a single change pair, `@@ -1,2 +1,2 @@` over `-a -b +A +B`, and `s` leaves it
intact — the driver's own log records the run count falling from 2 to 1 with the hunk still
spanning lines 1–2. **Line 2 is not reachable through the interactive prompt at all** except
through the `e` editor, which opens a patch in `$EDITOR`. `stg f:2` stages it directly:
`@@ -2 +2 @@ -b +B`.

**So the numbers git prints are not the numbers the caller has.** For the adjacent pair the
header says line 1, the reader says line 2, and the difference is inside one hunk.

## The failure mode that matters most

`naive`'s three failures split into two kinds, and the second is the reason to care:

1. `adjacent-edits`: `wanted_index` came back `None` — the header's anchor is line 1, so
   line 2 is not derivable from the output at all.
2. `modify-one-of-three` and `deletion-among-edits`: **the wrong thing was staged.** The
   first staged nothing where one change was wanted; the second staged **two** changes
   where one was wanted. Both with `git add -p` **exit status 0**.

A caller that checks the exit status sees success. `stg` exits 2 and names what it could not
find (`no stage change matches f:2`), and exits 1 only when it actually staged something.

## Correctness evidence independent of the comparison

The prototype's correctness does not rest on the table above. On a real file in this
repository, `stg stage STATE-constraints.md:3` and a hand-built patch applied with
`git apply --cached --unidiff-zero` leave a **byte-identical `.git/index`** (verified with
`cmp`). The parser is therefore checked against git's own arithmetic, not against a
model of it.

## What this does not establish

- **Not an adoption result.** Nothing here says anyone wants this. `KILL-Q`, the question
  F059 left `not_evaluated`, is still `not_evaluated` here.
- **The pty route is not shown to be impossible.** It is shown to need **133 lines** of
  caller code and, written that way, to reach 4 of 6. A better driver might reach 6 of 6,
  and would still have to solve the two problems named above. That is a claim about
  machinery, not about capability, and it is the whole of the difference.
- **Six synthetic cases**, one file, one platform, git 2.25.1. `diff.context` was varied
  because it is the obvious way the hunk count moves; `diff.algorithm`,
  `interactive.diffFilter`, renames, and mode changes were not varied.
- **Web search was unavailable on this host**, so "no prior art" rests on git's own
  documentation and behaviour, not on a search. That is a real gap in KILL-B.

## The next action this produces

Not a decision to ship. The question this leaves is the one no amount of local measurement
can answer: **is the 133 lines the whole cost, or is it the first 133 lines of a much larger
problem?** The concrete next step is a second class of case — renames, mode changes,
`--intent-to-add`, untracked files — and then an agent-run end-to-end: give a coding agent
"stage only the line you changed" and count how many attempts it needs.
