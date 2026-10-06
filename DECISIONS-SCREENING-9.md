<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Screening decision D069 — the oracle reads what the user receives

Decisions **D069**. Split from [`DECISIONS-SCREENING-8.md`](DECISIONS-SCREENING-8.md) on
2026-10-06. `observed` from E038 and F063, session 2026-10-06-009. Completes D068: its
three questions were answered correctly, and the instruments that answered them were
capable of agreeing with a broken tool.

E038 re-ran D068's question 1 — *is the operation already possible?* — with a search
surface E037 did not have, and found two tools that take the coordinate. That is recorded
as F062 and narrows the candidate. This entry is about the two instruments that run got
wrong first, because both would have reported a good result.

## D069 — an oracle reads the artifact the user receives

**The rule.** A comparison's oracle reads **the artifact the user receives**, not a
property of the route that produced it. For a staging tool that is the file content in
the index. Reading a *derived summary* of the result — a list of hunk anchors, a count, a
return code, a hash of the route's own intermediate — is a different measurement, and it
is blind to any defect where the route produces a well-formed summary of the wrong work.

**Why, concretely.** `stg` staged a two-line insertion when asked for one line, and
E037's oracle scored it 6 of 6. `staged_anchors` returned `[4]`, which is the right
number: the hunk git printed *was* anchored at line 4. The hunk simply carried two
changes. No anchor-based oracle can see that, at any sample size, on any population.

This generalises past staging. F056 measured the calendar and asserted a direction; F025
made a failure readable and never explained it; F013 committed merge markers and every
gate passed. In each the gate read something adjacent to the property it claimed.

Three consequences, all in force:

1. **A test that pins a guess is evidence-shaped and will preserve the guess.** The test
   asserting *"there is no valid hunk for half of a two-line insertion"* carried a
   premise that was false, and would have held the bug in place permanently. A test's
   comment is a claim and has to be verified like one.
2. **A baseline must be shown able to see the problem.** E037's pty driver hardcoded one
   filename; pointed at a file it did not name it read 0 of 30, which looked like a
   devastating result for the incumbent and was an artefact of the harness. A baseline at
   zero is diagnosed before it is believed, in the same way an instrument that cannot fail
   is.
3. **An unbuildable oracle is a defect in the harness, not a result.** Fifteen of my first
   33 rows could not build a reference patch. They were scored anyway, and the routes looked
   wrong on them.

## D069b — a hand label is checked against a second reader, and a rate built on a keyword match is a measurement of the match

Two rules from the same run, because both decide whether a demand number means anything.

**A classifier's precision is measured before its output is read.** `readout.py` put 100
of 195 issues in "in-population". Against a hand-labelled sample its precision is 0.067 and
0.033 — and it missed the single strongest row in the sample, the one whose entire subject
is a line range. A keyword match over a repository-wide body search cannot tell a need from
a pull request about a CI budget. **A rate derived from it is a property of the vocabulary,
and must never be reported as prevalence.**

**Two readers, and the disagreement must be located, not averaged.** κ = 0.734 three-way and
0.889 collapsed is high, and the `yes-line` Jaccard is 0.25. Both numbers are true and they
say different things: **the readers agree where the label is easy and disagree exactly where
the claim lives** — the boundary between "the operation" and "the coordinate". Averaging the
two rates into one number would have hidden that. The reported figure is the range, and where
two readers disagree the row is reported with the sentence each one used.

**Also in force:** a sample whose rows are truncated in the instrument is read at its
truncation. Both readers found labels that turn on text past a 700-character cut, all in the
`yes-` categories. The ceiling of a hand-read arm names the truncation.

**Ceiling.** κ on 61 rows with a heavy `no` class is sensitive to prevalence, and the class
distribution is a property of GitHub issue search rather than of the need. Nothing here
measures how common the capability is — only that it is asked for, by named people, in
projects independent of this repository, and that the instrument that appeared to measure
how common it is cannot.
