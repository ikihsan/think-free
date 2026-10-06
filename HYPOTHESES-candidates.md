<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# E037 — line-addressable partial staging, `stage-lines` / `stg`

**Status:** `mechanism` and `interface` **supported**, `usefulness` and `adoption`
**untested**. Candidate, not product. Started 2026-10-06, session 2026-10-06-006.

## Claim

A person who wants to commit part of a file, and who is not a person at a terminal — a
script, a CI job, an editor keybinding, an AI coding agent — cannot name the change they
want, because **no interface addresses it by the coordinate they already hold**, which is
the line number in the file they are reading. Supplying that coordinate is a small tool, and
it is not prior art as an interface.

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
| **KILL-Q** | Does anyone want this? | — (adoption; **not evaluated**, and not a gate this host can settle) |

**KILL-B not met** (no `file:line` in git; the documented workaround needs a hand-typed
header and `--unidiff-zero`). **KILL-A not met** — the honest baseline is a 133-line pty
driver reaching 4 of 6. **KILL-C not met** — `stg` 6 of 6, stable at `diff.context` 1 and 3.
Full numbers: `EXPERIMENTS/037-line-staging/README.md`.

## What would falsify the useful claim

**KILL-Q is the whole open question and it is `not_evaluated`.** Nothing in E037 says a
person wants this; it says the interface does not exist. The falsifiable form is: *given a
working `stg`, a developer or an agent asked to stage one specific line will use it rather
than `git add -p` or a hand-built patch.*

The cheapest honest test that does not need permission to contact strangers:

1. **Extend the case set** to renames, mode changes, `--intent-to-add`, untracked files,
   `diff.algorithm`, and `interactive.diffFilter`. Six synthetic cases on one git version is
   the run's clearest ceiling.
2. **Agent end-to-end, with attempts counted.** Give a coding agent "stage only the line you
   changed" against a real repository and count attempts and wrong-answers. This is the
   instrument the mission has never had, and it is measurable offline.
3. Only then, and only with authorisation, the 557 named requesters in F061 who wrote these
   unprompted. **Contacting them is outside current permissions** and is not proposed here.

## Mechanism, stated separately from usefulness

`stg` parses `git diff -U0` into the smallest hunks `git apply --unidiff-zero` accepts, cut
at the point where removed and added counts pair up — the same rule `git add -p`'s `s` uses,
except `s` cannot apply it inside a run of adjacent changes. Each change is addressed by its
first line in the file as it reads now; a deletion is addressed by the line whose content
moved up, so every addressable change names a line that exists. Correctness is checked
against git itself: on a real file in this repository the resulting `.git/index` is
**byte-identical** to the one a hand-built patch leaves.

## Ceiling

One platform, one tool, one git version, six synthetic cases. The comparison is against
routes written by this mission, not against what the ecosystem contains — **web search was
unavailable on this host**, so "no prior art" rests on git's documentation and behaviour. The
gap is on the interface, not the capability, and an interface gap is the kind that closes
quietly: if a future git takes `file:line`, this is dead, and the check is one command.
