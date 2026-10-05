# E029 — protocol amendment 2

<!-- owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05 -->

**Declared 2026-10-05, after reader r2 reported and before any reader rate was
computed or any gate was read.** No gate has been evaluated, no arm has been
compared, and the separation C1 tests has not been calculated. The thresholds in
[`PROTOCOL.md`](PROTOCOL.md) are unchanged.

## The defect

The mismatched arm draws its partner from the whole 241-author population, but the
*items shown* are the partner's own `show_hn` items **that postdate the partner's own
need**. Only 74 of the 241 have any such item, so **45 of the 74 mismatched rows
rendered an empty SHIPPED section** — the literal text
`"(this person has not posted a Show HN item since)"`.

A reader cannot label such a row anything but `unrelated`. The mismatched arm was
therefore **depressed by construction**, and both C1 and B1 would have read an
artifact of the view builder as a finding about the world. 45 of 74 rows is not a
bias to be footnoted; it is most of the arm.

This was found by a test, not by reading a rate: the test for "every reader row has
a build that postdates the need" was written over all three arms and fired on `X00`.
The first version of that test iterated only the matched arm and passed. The
population of the test was the population that could hide the defect.

## The repair

**The mismatched arm's partner pool is restricted to the 74 authors who have a build
postdating their own need.** All three arms then have the same structure: a non-empty
SHIPPED section, and a NEED text that differs only in whose it is. The matched arm is
a subset of the same pool, so the arms are drawn from one population and differ in
exactly one thing.

Sattolo's derangement is re-run over 74 elements rather than 241, still with
`random.Random(2901)` and still asserted to have no fixed point.

## What is *not* re-read, and why that is not a convenience

Only the **matched** and **story-title** arms are affected by the defect's *opposite*:
those two arms already had a non-empty SHIPPED section on all 74 rows. Their content
is **byte-identical** under the repaired builder, because the matched arm is the same
74 authors sorted the same way and the story-title arm is the same author plus the
same story.

So the 148 already-produced `M` and `T` labels from each reader **carry over**, and
only the 74 `X` rows are re-read. `test_claims.py` asserts the byte-identity of the
`M` and `T` sections across the two builds, so "they are unaffected" is checked
rather than asserted.

**The cost of this path is stated rather than hidden:** the two readers label the `X`
arm in a later pass than the `M` and `T` arms, so any drift within a reader biases
the agreement figure slightly *downward*. That is the conservative direction for a
gate whose threshold is a floor.

## What reader r2's labels were, and are not used for

Recorded here so the record does not have to be reconstructed: r2 labelled all 222
rows of the **first** view, giving `unrelated` 156, `unclear` 58, `addresses` 8 —
of which **4 matched, 3 story-title, 1 mismatched**. Those eight `addresses` labels
are not evidence of anything: one in three of them sits in the arm that was
depressed by construction, and the arm-level rates were never computed.

r2 also reported, unprompted, that it resolved two borderline rows toward `unclear`
per the rubric's "adjacent but you cannot tell" clause (a web-typesetting need
against a site that typesets the Federalist Papers, and an OCR benchmark against an
OCR model benchmark). That is the rubric working as written, and it is a reminder
that `unclear` is a real category here and not a rounding error.
