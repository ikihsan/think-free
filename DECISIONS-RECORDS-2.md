<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# Decisions — records (continued)

Decisions **D110, D112, D113, D114**. Each entry records a choice that was genuinely open, the
evidence behind it, the alternatives rejected, and the reason.

The second half of [`DECISIONS-RECORDS.md`](DECISIONS-RECORDS.md), split on
2026-10-14 when that file reached 308 of the 300 permitted lines. Same
invariant, same shape, one more decision: **what this repository's own
records must be**.

## D110 — A list split across files is read by a reader that reads all of them

> **Renumbered from D046 on 2026-10-14.** Two VMs allocated D046 from the
> same base against two unrelated decisions and both landed in `48b7e1f8`:
> this one, and "A prototype tool with a working adapter interface is
> released when the adapter pattern is confirmed" in
> [`DECISIONS-PUBLISHING.md`](DECISIONS-PUBLISHING.md). The publishing one
> keeps D046 because four documents cite it, two of them sealed session
> records. The allocation rule (T-0030) refuses a collision before
> publication; the land merged two that had each been allocated
> separately, so the repair lands on the side with no dependants.

Evidence: T-0056, session `2026-10-04-042`. Defect 22 in
[`STATE-defects.md`](STATE-defects.md).

**The choice.** `STATE-defects.md` was split at its 300-line cap, and
`defectlist.py` reads **every file of the list** rather than the first. The parent
file's own record had said the split could not be made without exactly this change
— "it cannot be done inside its own numbered list without `defectlist.py` reading
more than one file" — and it was done here rather than by trimming an entry to make
room, the cut falling at the `## Open` heading the document already states as a
boundary.

The alternative was to leave the reader pointed at the parent and note in prose that
the other half is unchecked. That is the defect the rule exists to catch: **the
reason `defectlist.py` reads this list at all is defect 10**, where two VMs took
defect 7 in the same hour, each tree internally consistent, and only a human reading
the file reported it. A duplicate spanning the two halves is invisible to a reader of
either half, so it is exactly the case the rule must catch and exactly the one a
single-file reader cannot.

Rejected: **trim entries instead of splitting** — what the cap has been met with five
times already, each time repaired by moving material to the file whose invariant owns
it. Rejected: **making the split generate both files**, which would make a numbered
list a derived artefact and lose the property that an entry is written once, by the
session that found it.

**Ceiling.** A **gap** in the numbering is still unreported, and after a split a gap
can straddle the two files as easily as sit inside one — so this fixes the reader, not
the coverage. Both halves are checked in `tests/test_defectlist.py`, including a
control asserting that reading only the parent would have missed the collision the
split makes possible.

## D112 — A rule for this repository is not applied to a document this repository did not write (2026-10-14)

Observed: E125 committed 30 READMEs and 17 `git ls-tree` listings fetched
verbatim from other people's repositories, and `doc lint` reported 402 violations
on them — broken links and links that "leave the repository" — with no edit to an
authored file able to clear any of them (F127).

**The choice.** `doclint.check_meta` and the link rule now skip files
`vendor/MANIFEST.md` declares exempt, exactly as the line cap, the orphan rule
and the metadata rule already did. The exemptions are declared by glob with the
reason written beside them, not by a path prefix in the rule.

**Why the rule cannot be made to hold them instead.** A README's `docs/`,
`examples/` and `/owner/repo/...` links name the repository it was fetched from.
Making them resolve here would mean either creating a second copy of that
repository's tree inside this one, or editing upstream bytes — and the second is
the one thing an evidence copy is for. E125 committed those files to record what
22 candidate harnesses' own documentation says about them, and 402 lint
violations are not a reason to stop recording that.

**Why this is not the weakening it looks like.** The link rule is unchanged for
every authored document, the exemption covers one declared class, the rule
itself names the reason in its own docstring, and the control in
`tests/test_link_escape.py` — which asserts that *no* tracked link leaves the
repository — is read through the same `is_exempt` decision the rule uses, so
widening the exemption shows up there as a widening of what the control
examines. The five other `doc lint` causes E134 repaired (two E130 stubs, five
`RESULT.md` files naming three files that were never written, and the D046
collision two VMs allocated from the same base) were repaired, not exempted.

Rejected: **rewriting the fetched links** to absolute URLs, which turns evidence
into a document this repository asserts. Rejected: **dropping the fetched files**,
which loses the population E125 drew from. Rejected: **teaching the link rule to
resolve a third party's tree**, which is harness-specific knowledge in a
repository-wide rule — the adapter tax D046 and F124 both record.

**Ceiling.** `is_exempt` is now consulted by three rules that previously were not,
so the exemption list has more reach than it did when it governed one rule. Every
entry is a class with a reason and a count; a future entry that is a single file
is the shape to refuse.

## D113 — a service screen must stratify on version-dependence, not report one pool rate

**Decision.** Any screen that measures whether the strongest accessible
alternative serves a population must classify each row as **version-pinned**
or not, and report the alternative's served share **per stratum**. A single
pool-level rate is not an admissible result. E168 is the template for the
classification; [`EXPERIMENTS/168-version-pinned-need/PROTOCOL.md`](EXPERIMENTS/168-version-pinned-need/PROTOCOL.md)
is the rubric.

**Why.** Seven service closures in this record (E062, E077, E082, E091,
E092, E126, E143) ended with the same sentence — the free general assistant
serves it, 0.25 to 1.00 — and that sentence was read as "no population here
is unserved". It was never tested per stratum, because every one of those
screens drew from **public questions**, which are the most-served class of
human information need that exists. E168 read the 13 failures E126 graded
`unserved` and never characterised, and found all eight of its software rows
fail for one reason: the answer depends on what is true in a specific version
of a specific component. Stratified on that, the same pool gives
**85 of 299 = 0.2843** version-pinned (Wilson [0.2361, 0.3379]) against a
2.0% program-shaped residue, and the assistant's served share on the
high-arrival end of that class is **11 of 24 = 0.4583** against E126's own
pool-level 0.6750 on the same rows with the same instrument.

**The evidence is one experiment and it is thin.** Fisher p = 0.1168 on the
stratum comparison; four of the 24 grades are near misses and the served share
moves between 0.3750 and 0.5417 with their treatment. This decision costs a
classifier, not a new instrument, and the classifier is cheap. What it is *not*
is a licence to build: E168's mechanism gate (does grounding on the
component's published version history recover the failures?) is **unrun**,
because the session that ran G1 and G2 had already read every thread.

Rejected: **re-running the seven venues with the new classifier.** The
decision is about the next screen, not about re-reading closed populations;
E126's pool is re-analysed in place instead. Rejected: **treating
version-pinnedness as the only unserved class**, which F096 and E091 both
warn against — E091's vendor-bound composition is a different mechanism and
E168 does not speak to it. Rejected: **a `version_pinned` requirement as a
condition on candidates**, which would be the mirror-image error: it would
exclude the vendor-bound and private-code classes that are genuinely
unserved for other reasons. Rejected: **using E168's 0.4583 as a venue
serving rate**, which is 24 rows of the high-arrival end of one class on one
day.

**Ceiling.** The classifier's precision is measured on the 13 rows the
headline rests on (13/13) and unmeasured over the other 72 `vp = 1` rows.
The Jaccard of 0.4417 against E126's independent `answerable`/`specific`
labels says the two screens see different rows at both edges; which edge is
right is not established.

## D114 — "the strongest accessible alternative" must state whether it can retrieve, and an instrument-limited rate is not a rate

**Date:** 2026-10-16. Evidence: F130, and E169's instrument findings.

**What this is about.** Thirteen service closures in this record read
"the strongest accessible alternative serves it". The alternative in every one
of them was a free general assistant **with no retrieval** — a fact stated once,
in E091, and then carried silently through twelve venues, a classifier redesign
and a candidate seat. E168's addendum named the problem on its own rows: 20 of
24 threads point at an external fix, and the resolution is sitting in a
searchable issue tracker.

**The decision.** A service screen declares, in its protocol, three things
before any population is read:

1. **whether the alternative may retrieve**, and if so from what index;
2. **the instrument that will be used to check whether the alternative reaches
   the fix**, and its own positive control;
3. **what the number is not**, when the index is narrower than the class.

A pool-level rate from a narrower instrument is reported as a bound on that
instrument, never as the class's serving rate. Two rates from different
instruments are not compared, and a closure that rests on one is re-opened
rather than generalised.

**Why this is a decision and not a note.** The gates this repository already
has did not catch it. A gate that reads its own environment checks the
environment it recorded (F018, F019). E169 declared a reachability gate whose
instrument could not fire, and **the instrument's own positive control is what
proved it** — 3 of 13, then 13 of 13 — after the treatment arm had already
produced a clean-looking 1 of 13. The general rule this adds: **a screen's
baseline must be validated by feeding it a case the screen would be expected to
find, and a control that cannot fail is a control that has not run.** E169's
G1 is the degenerate version of the same thing — both columns were 1 on all 20
rows, so its agreement statistic was 20 of 20 whatever the extractor did.

**Rejected: re-running the twelve closures with a retrieval-enabled arm.**
This host has no general web search (F130), so the re-run cannot happen here and
a closure re-opened without a reachable instrument produces a number with no
denominator. Rejected: **treating containment as a substitute for the
search-enabled baseline.** Containment is the necessary condition for a match
and says nothing about ranking, and it is recorded as an obstruction screen, not
as a service rate. Rejected: **a standing "this host has no web search" rule.**
The boundary is a property of the measurement's question, not of the machine;
a protocol that needs search must say so and stop, and one that needs a single
resource must fetch the resource.

**Ceiling.** This decision constrains future screens and revokes the wording of
thirteen closures; it does not re-open any of them, because no reachable
instrument here could re-open them. What it does buy is that the next screen
that *can* run will say which alternative it beat.
