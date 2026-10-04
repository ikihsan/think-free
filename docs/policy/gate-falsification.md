<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# What a fix costs to believe

Split out of `STATE-defects.md` on 2026-10-04 (T-0042), when adding a defect
entry took that file past the 300-line cap. It is the method the entries in that
list are held to, not another entry in it, so the list stays a list.

**Every entry marked solved was falsified against its own defect first:** the new
tests were run against the unfixed code and had to fail. One of those
falsifications (T-0024's second attempt) mutated a code path the callers never
reach and passed anyway — the failure of the falsification, not of the gate — so
it was redone by reverting the generators instead. See D025 in
[`DECISIONS-GATING.md`](../../DECISIONS-GATING.md).

**A falsification has two directions and the second is the one that is easy to
leave out.** A rule that fires on the defect proves it can fail; only a rule that
stays silent on the repair proves it can be satisfied. Both are asserted here:

| Direction | What it rules out | Where it is asserted |
|---|---|---|
| Fires on the defect's own bytes | A rule that cannot detect the thing | `test_conflicts.py` (three regions of `fd7b4a1`), `test_identifiers.py` (`e6eb992`), `test_defectlist.py` (`e53ca23`, `e701ad8`), `test_decision_header.py` (`d451169`) |
| Silent on the repair and on the tip | A rule nobody can satisfy, which is a gate nobody runs | the same files, plus a sweep over every commit that touches the record |

**Two of the three lessons are written up where they are used rather than here**,
because both now live in [`tests/README.md`](../../tests/README.md) next to the
tests they describe, and a rule copied into two places is a rule that will drift:
how a gate is falsified and what each failure taught — the T-0030 control that
caught a decision-index regex matching no row in any of 174 commits, and a stale
generated file arriving four times because each repair fixed the layer that
happened to be running (the task commands, then the CLI, then — at last — the
appenders and the merge). Read that file for the mechanism; the entries in
`STATE-defects.md` carry the dates and the commits.

**A gate whose input it cannot read has to say so.** This is the obligation
defect 10's control failure produced, and it now has three instances: a
`STATE-defects.md` with no readable entry is a violation
(`tools/originlib/defectlist.py`), a decision record with no readable header is a
violation (`tools/originlib/decisionheader.py`), and a version comparison that
cannot tell "we looked and it is not there" from "we could not look" reports
`record unreadable` rather than a verdict (`tools/originlib/versions.py`). A
parser that quietly stops matching is indistinguishable from a clean tree, which
is the same blind spot as a check that has never fired.

**A gate's verdict must be a function of the repository alone** (D041, defect 19,
T-0051). The fourth instance of the form the entries above keep meeting, and the
first whose environment is the filesystem *outside* the checkout, which no record
of the tree can pin. `doc lint` rule 3 resolved each candidate with `exists()`,
so a link written `../../docs/x.md` from `tasks/` was judged by whether the
checkout's parent directory held `docs/x.md`: measured on one probe document at
two checkout locations, no finding in one and `broken link` in the other. T-0047
had already recorded the symptom — a green lint in the worktree it built in, a
red one after landing, identical bytes — and could not reproduce which run
decided it. The answer is that the run was never the variable.

Three things make the repair checkable rather than merely different:

- **The defect is reproduced by the test, not described by it.**
  `tests/test_link_escape.py` builds both checkouts, so the disagreement is
  observed. The previous rule is written out in that test as a witness, because
  after the repair the production code can no longer demonstrate its own defect.
- **One mutation falsifies both directions,** since removing the containment
  filter *is* the previous rule: the escape goes unreported and the
  parent-dependence returns. `tools/mutate_link_rule.py` counts its own pattern
  before writing, after T-0047's first mutation matched nothing and a green run
  read as a control.
- **The control that cannot fire is stated.** No tracked link in this repository
  leaves it, so the rule adds a verdict and no violation;
  `NoRegressionTest` counts the links it read (577 on 2026-10-04, and it fails
  below 100 so that assertion cannot pass by reading almost nothing) and also
  asserts the rule still reports the links it always reported.

**Ceiling.** Inline links only. A reference link, a bare autolink, and a link that
resolves inside the repository to the wrong document are unexamined, and rule 3
still takes its file list from git, so an untracked document is invisible to it
as to every other rule.