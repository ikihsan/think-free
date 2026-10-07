<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# Findings F076-F080 (E046, `EXPERIMENTS/046-real-changes/`)

Split out of [`FAILURES.md`](FAILURES.md) as part 29. One finding per section:
what happened, what it rules out, and the ceiling of the evidence. **Identifiers
are stable across all findings files.**

**Three are defects in the `stg` artifact, found on real repository changes and
fixed; one is a defect in this session's own referee, found three times in three
different shapes.** The first four are the third, fourth and fifth time the same
move has found real bugs the synthetic corpus could not see (E038's two, then
these four), and the fifth is the reason a reader should not believe the first
four without reading how they were measured.

## F076 — No line of any new file could be staged, in any repository

**What happened.** E046 replayed **114 real file changes** drawn from real commits
in three real repositories and staged every address one at a time. In the 15 cases
drawn from real file-creation commits, **435 of 435 addresses refused**: `stg
stage f:12` on a new file exited 2 with `git apply refused the patch: error f:
already exists in index`. With `git add -N` run first — the documented way to make
a new file addressable — the same refusal, because `git diff -U0` then names
`/dev/null` as the old side and `git apply --cached` will not create a path the
index already holds.

**What it rules out.** It rules out the artifact's own ceiling claim. E037–E042
each declared in the same words that untracked files were untested; ten synthetic
cases had no case that created a file, so nothing in the record constrained the
code path. `git` has no such limit — the same patch naming the path on both sides
is accepted and leaves the index holding exactly the addressed lines — so this was
never a git limitation, and "the gap is on the interface, not the capability" was
true of the *interface stg offered* and false of what was reachable through it.

**Fixed, and the fix had a second half.** Naming the path on both sides makes a
new file's patch an edit of the intent-to-add entry. More than one change in one
patch then needs **one** hunk, not several: each carries `-0,0 +N,1` and applied
together they land in reverse, so `split --all` on a three-line new file staged
`three two one`. Both were measured before being fixed. Five tests added; the
suite is 34 → then 36 as the other two findings added theirs.

**Ceiling.** New files whose content is not UTF-8, and new files in a repository
with `core.autocrlf` set, are not covered by the corpus. The corpus itself
excluded non-UTF-8 files by rule.

## F077 — One address could name two changes, and staging it staged both

**What happened.** A real commit in this repository (`7c7ef912`,
`STATE-next-actions.md`). A deletion is addressed by the line whose content moved
up, because a deleted line has no line of its own. When an insertion lands on
exactly that line, **two different changes answer to one coordinate**. `stg stage
STATE-next-actions.md:80` removed eight lines **and** added one, printed the
coordinate twice, and exited 1. `stg list` printed `STATE-next-actions.md:80`
twice with nothing in either row to tell them apart. 8 address rows over 4 cases.

**What it rules out.** It rules out E039's honest-exit result as a general property
and narrows it to the failure modes E039 enumerated. "Exited 1 after the index
matched the request" was true on eight real failure modes; a request that matches
nothing was never among them, and the tool reported a two-change staging as one
success. This is the E038 bug class again — a tool that stages something the
caller did not name — which makes two independent confirmations of the same shape
on real input, against two different oracles.

**Fixed** by giving the file the assignment rather than the change: a change that
occupies a line claims it, a deletion keeps its documented address unless that
line is taken, and a single-line request returns at most one change. `stg list`
and `stg stage` read the same assignment — an earlier version of the fix made
`select` honest while leaving the listing printing a coordinate that no longer
selected its change, which is a worse defect than the one it repaired and was
caught by a test written for the original behaviour.

**Ceiling.** Where every candidate line near a deletion is claimed by another
change the deletion is still displaced upward, and the coordinate it prints is
then one line away from the gap rather than beside it. That is a naming choice,
not a correctness property, and no test asserts which line is chosen.

## F078 — An address that could not change anything reported success

**What happened.** One real jq commit (`a19efdd4`, `src/lexer.c`, a generated
table rewritten wholesale). **9 of that file's 190 addresses** were a pair that
removed a line and added the identical line back: `git diff -U0` pairs removes
with adds positionally, and in a large rewrite the pairing lands a line against
itself. `stg stage src/lexer.c:597` exited 1 and printed `stage src/lexer.c:597`
while leaving `.git/index` **byte-identical to HEAD**.

**What it rules out.** It rules out the honest-exit claim as a property of the
tool and, with F077, explains why the E039 result did not generalise: E039 tested
eight *invalid* requests, and this is a *valid* request that does nothing. A
caller reading "exit 1, staged src/lexer.c:597" and then finding nothing in the
index has no signal that anything went wrong, because none was reported.

**Fixed** in `_split_run`: a pair that replaces a line with itself is not a
change, and is no longer listed or staged.

**Ceiling.** The no-op test compares the removed and added line of a *pair*. A
surplus run of deletions whose content also happens to be present elsewhere is not
tested, and `git apply` accepting a redundant patch is not a property E046 measured.

## F080 — Two lines silently merged into one, reported as staged

**What happened.** A real commit in `psf/requests` (`e9b1217c`,
`src/requests/packages.py`), a file whose last line has **no newline**. Two lines
were inserted immediately above that unterminated line. `stg
stage src/requests/packages.py:28` — the *second* of the two — exited 1 and
printed `stage src/requests/packages.py:28`, and the index came back with

```
-# Kinda cool, though, right?
+# Kinda cool, though, right?        sys.modules[f"requests.packages.{target}"] = sys.modules[mod]
```

Two logical lines merged into one, in the index, reported as success. The
addressable neighbour one line up staged correctly, and `split --all` staged the
file correctly; only the *split* of that one insertion was wrong.

**Why it happens.** `git apply --cached --unidiff-zero` cannot express "a
terminated line before an unterminated one". Given `@@ -26,0 +28,1 @@` for a file
the index holds 27 lines of, it places the line at the end rather than at
position 28 — exit 0, wrong file. Reproduced by hand with the patch alone, so it
is git's behaviour and not `stg`'s arithmetic: `LASTLINENEW2` in the index.

**What it rules out.** It is the only finding here that **corrupts** rather than
mis-selects, and it rules out "the artifact is safe on real input" as a claim
that survives one corpus. It also bounds F076–F078: all three are wrong answers
at exit 1, and this one is a wrong *file*.

**Fixed by refusing, not by answering.** There is no patch shape that inserts a
terminated line before an unterminated one, so `stg` now names the case and
points at the command that works (`git add` the file). Two tests, one asserting
the refusal and one asserting it does **not** fire on a file that ends with a
newline, because a guard that cannot tell those two files apart would refuse most
of a normal day's work.

**Ceiling.** A new file whose last line has no newline stages with a trailing
newline the working tree does not have: the index entry is written whole and
cannot end mid-line. That is a fidelity loss, not a corruption, and it is not
tested.

## F079 — A referee written from the tool's own output grades the tool, three times

**What happened.** E046's judge was rebuilt three times before it produced a
verdict anyone should believe, and each earlier version produced confident,
wrong, *directional* numbers on real data:

1. **Header equality.** The first judge required git's own `diff --cached` hunk
   header to equal the coordinate `stg list --json` declared. git anchors the old
   side of an insertion inside a run of adjacent changes wherever the arithmetic
   lands, so header equality is a placement convention, not a property of content:
   **55 rows of a byte-exact result read as `mis_staged`.**
2. **Reading the wrong state.** The second version read the index blob after the
   harness reset, measuring the pre-image it had just put back. Every row of the
   positive control failed: **0 of 30**, all of them correct.
3. **CRLF.** The third applied the residual patch and compared bytes, in text
   mode. Python's universal-newline translation rewrote every `\r\n` to `\n` on
   read, so **23 rows of a real requests commit read as `mis_staged`**.

Each was found only because a control was in the way, and the negative control
took three more versions: it first asked `stg` for a wrong line and called the
refusal a failure (punishing correct behaviour); then asked for a line no change
answers to, so `stg` refused all twelve and the judge was never consulted; only
the third built the wrong index state with `git apply` and checked the judge
rejected it.

**What it rules out.** It rules out any E046 number read without its controls.
The positive control's 30/30 and the negative control's 17/17 are what make the
real-change table mean anything, and both were earned after three failures each.

**The transferable part, and it is the same sentence F049 already earned.** A
judge must be built from something the tool does not produce. Here that is git's
own patch text on both sides of the request — what git reported unstaged before,
and what it reports staged after — rather than any coordinate the tool printed.
An equality between the tool's output and the tool's output is a tautology with a
number attached, and it fails in whichever direction the tool's convention happens
to differ from the referee's.

**Ceiling.** The judge does not test *which* change was staged when two changes
have identical removed and added line content, and it accepts a residual apply
that reproduces the working tree as sufficient evidence of position. Both were
adequate here; neither is established as sufficient in general.