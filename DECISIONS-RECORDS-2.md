<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# Decisions — records (continued)

Decisions **D110, D112**. Each entry records a choice that was genuinely open, the
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
