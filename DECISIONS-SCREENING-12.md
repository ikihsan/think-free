<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# Decisions — screening candidates and judging experiments, part 12

Decisions **D075, D076, D077**. Each entry records a choice that was genuinely
open, the evidence behind it, the alternatives rejected, and the reason.

**Renumbered on landing, 2026-10-07.** These were D074 and D075 on the side that
had not been pushed; VM 0944 landed **D074** — *a candidate whose surviving claim
names a caller runs that caller as an arm, with the arm checked to have actually
exercised the tool* — while this session's rebase was stopped on the same files.
The unpushed side moves, per
[`docs/process/multi-vm-coordination.md`](docs/process/multi-vm-coordination.md).

**D074 and D075 are not independent of each other**, and a reader should hold them
together. D074 makes the *arm* a real caller rather than a simulation, and D076
makes the *referee* read something the tool did not produce. D074's own failing
case was a simulated arm, and a simulated arm is precisely the thing whose verdict
is a function of the thing under test.

**Invariant:** the same as [`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md) —
a decision belongs to the file whose subject it is, the number is allocated with
`origin id next D` against the base, and the heading, this table's row and the
file's own `Decisions **…**` header all move together
([`docs/process/multi-vm-coordination.md`](docs/process/multi-vm-coordination.md)).

## D075 — A candidate's declared ceiling is a measurement plan, not a disclaimer

**The choice.** E046's protocol was written before its run. Six experiments on
the same candidate — E037, E038, E039, E040, E041, E042 — had each closed with
the same sentence in its own limitations section, in nearly the same words:
*"does not test renames, mode changes, `--intent-to-add`, binary files, untracked
files, or multi-file scenarios."* Six times that sentence was treated as
disclosure rather than as a work list. The candidate was described as a tool
whose only untested property was its interaction with input nobody had used.

**The evidence.** E046 drew 114 real file changes out of real commits in three
real repositories, stratified by the shapes that sentence names, and staged every
address one at a time against a referee built from git's own patches. **Three
defects, all in shapes the sentence had already listed:**

- no line of any new file could be staged — 435 of 435 addresses across 15 real
  file-creation commits (F076);
- one address could name two changes and staged both — a real commit in this
  repository, `stg STATE-next-actions.md:80` removing eight lines and adding one
  while printing the coordinate twice and exiting 1 (F077);
- an address that could not change anything reported success — 9 of one real jq
  file's 190 addresses replaced a line with itself and left the index
  byte-identical (F078).

All three are now fixed and the corpus re-runs clean. None is reachable from a
single-file synthetic case, and the corpus is not exotic: it is this repository,
`psf/requests` and `jqlang/jq`, newest 800 commits each.

**Decision.** A candidate's own limitations section is a **measurement plan**. It
is executed as a run over real input, with the same referee the supported claims
were measured with, before the candidate is called release-ready — not before it
is called a candidate, which costs nothing and has a ceiling of its own. The gate
is per-shape and named before the run: a shape the tool cannot address at all is
a gap with the caller's manual route recorded beside it, and a shape it addresses
wrongly is a defect with a reproducer.

**Rejected: executing the ceiling as a release gate.** It would have blocked
every candidate that has ever existed here on input nobody had yet tried, which is
the same failure as D050's screens: killing a candidate for a property of the
experiment rather than of the candidate. The candidate is still a candidate; what
changes is that the untested list stops being a disclaimer.

**Rejected: extending the synthetic corpus instead.** Ten more cases of the same
shape would have found none of the three, which is the point: the failure mode is
a property of *where* the input came from, not of how many cases there were.
E038 already showed the same move paying once — a stronger oracle on the same
ten synthetic cases found two real bugs — and this is the second time, with the
oracle held fixed and the *input* varied instead.

**Ceiling.** E046's corpus is UTF-8-decodable files only, newest-first, three
repositories. Completeness is checked only where the replay is faithful — where
`git add` on the replayed path itself reproduces the post-image — which is 81 of
114 cases; the other 33 are pure renames and deletions, with no line-addressable
change at all. A shape E046 does not name is not covered by having named these.

## D076 — A referee is built from something the tool does not produce

**The choice.** E046 had to judge `stg`'s staging without asking `stg` whether
the staging was right. Its judge was rebuilt three times before it produced a
verdict worth reading, and each earlier version produced confident, directional
wrong numbers on real data (F079):

- requiring git's `diff --cached` hunk header to equal the coordinate the tool
  printed read **55 byte-exact rows** as `mis_staged`, because git anchors the old
  side of an insertion inside a run of adjacent changes wherever the arithmetic
  lands;
- reading the index blob after the harness reset measured the pre-image it had
  just put back, so the positive control scored **0 of 30** on results that were
  correct;
- comparing bytes in text mode let Python's universal-newline translation rewrite
  every `\r\n`, so **23 rows of a real `requests` commit** read `mis_staged`.

**Decision.** A referee reads **something the tool did not produce**. Here that
is git's own patch text on both sides of the request: what git reported unstaged
before, and what it reports staged after, plus a residual `git apply` that must
reproduce the working tree. Equality between a tool's output and a value derived
from that same output is a tautology with a number attached, and it fails in
whichever direction the tool's convention happens to differ from the referee's.

Two controls are part of the instrument, not of the result: a positive control
that must reproduce a known-correct answer the referee has never seen (E038's
30-row matrix, 30/30), and a negative control that must reject a **known-wrong
index state built with `git apply` rather than with the tool** (17 of 17; one
injection skipped for reproducing the correct answer). Asking the tool for a wrong
input measures the tool, and asking for an input no change answers to produces a
refusal the referee never sees.

**Rejected: asserting on coordinates.** It is cheaper to read and it is the
mistake above. Rejected: asserting only on the staged *diff*, which is what
E037's oracle did and which scored a two-line over-staging as correct; the bytes
in the index are what the user receives.

**Relation to F049.** F049's sentence — establish a reference *before* measuring
agreement against it — is the same rule one level up. There, a repair was checked
against a reference that had not been established; here, a verdict was read off a
reference that was a function of the thing under test.

**Ceiling.** The judge does not distinguish two changes with identical removed and
added line content, and treats a residual apply that reproduces the working tree
as sufficient evidence of position. Both were adequate for E046's rows; neither is
established as sufficient in general.
---

## D077 — A candidate's demand evidence is read, in full, before its population is used

**Decided 2026-10-07, VM 0947.** Evidence: E045 (T-0083), F081, F082.

**The choice.** F081 killed the only population the mission's ranked top action
had left, and F082 killed the differentiator. Both kills were available in
evidence this repository had been holding since E038 and had read only at the
level of titles and of a classifier's precision. So: when a candidate's demand
claim names a population, that evidence is read row by row — requester, and the
specific thing the requester says it lacks — **before** any experiment is built
to measure that population, and before any next action is ranked against it.

**Why this is a rule and not a one-off reading.** F082's shape is D067 already:
test a candidate against its mechanism's existing source first. The new part is
*which* source. A harvested corpus is not a sample of needs; it is a sample of
**one retrieval route's ranking**, and the bodies of those rows name every
incumbent that route could see. Here the corpus named 26 implementations where
the web search returned 2, and the two it missed were the only command-line ones
— the two that matched the candidate's interface. Running a search against the
open web is not a substitute for reading the corpus already on disk, and in this
case it was strictly worse, because the search could not rank by
"implements the thing" while the corpus could name it in the issue title.

**Rejected: read the corpus before building the next experiment, but keep ranking
first.** The ranking is what makes the claim load-bearing. Item 0a was ranked
top, described as "cheap and decides a live build question", and would have
consumed a session establishing that its population is a construction of the
proposing harness. A rank is an assertion about evidence that has been read, and
this one had not been.

**Rejected: treat "the corpus contains the kill" as a reason to distrust all
harvested corpora.** The application here is real — 29 issues, 26 repositories,
three shipped tools — and two of those rows name a difficulty none of the three
tools addresses. A corpus that fails to support a candidate is not a corpus with
nothing in it; it is a corpus that has to be read rather than counted.

**Relation to D069 and D075.** D069 made a classifier's precision be measured
before its output is read; E045 measured it (0.372) and found the reading still
unnecessary, because the count that mattered came from the reader. D075 made a
candidate's limitations section a measurement plan; F081 is what that plan would
have found had it been aimed at *the population* rather than at the artifact's
inputs.

**Ceiling.** This rule costs one reading of one corpus per candidate, which for
a corpus of 189 rows was an afternoon and is not affordable at the scale of a
harvest. It is affordable at the scale of a candidate with a named population,
which is the only time it is required.
