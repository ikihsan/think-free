<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# Decisions — screening candidates and judging experiments, part 12

Decisions **D075, D076**. Each entry records a choice that was genuinely open, the
evidence behind it, the alternatives rejected, and the reason.

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