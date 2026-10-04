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
defect 10's control failure produced, and it now has four instances: a
`STATE-defects.md` with no readable entry is a violation
(`tools/originlib/defectlist.py`), a decision record with no readable header is a
violation (`tools/originlib/decisionheader.py`), an experiment `results.json`
that cannot be parsed is a violation (`tools/originlib/resultnumbers.py`), and a
version comparison that cannot tell "we looked and it is not there" from "we
could not look" reports `record unreadable` rather than a verdict
(`tools/originlib/versions.py`). A parser that quietly stops matching is
indistinguishable from a clean tree, which is the same blind spot as a check that
has never fired.

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
**A record that says one thing once is a property a merge can break** (D043, defect
20, T-0052). Commit `eff1126` carried `STATE.md` with a byte-identical second copy of
its `Implemented (2)` dashboard row — one row from each VM, the branches concatenated
by a rebase — and every gate passed. The reload point a cold session reads first
showed two rows that are one fact, and the next session found it by reading.

The measurement is the part worth keeping, because it is what made the rule decidable
rather than merely plausible: 47 tracked documents contain a repeated table row, and
**all 47 are generated session reports**, where a row repeats because an artifact was
declared or rewritten twice and the report is telling the truth. Hand-authored
documents had zero. That is why the exemption reads the `generated-by: origin` marker
in the document rather than a path or an extension — the distinguishing property is
whether the repetition is the point, and the document already says which it is.

Falsified in both directions, and the second is the one that would have shipped a rule
nobody could run: `tools/mutate_table_rule.py` removes the rule, and `eff1126` is
reported by nothing; it removes only the generated-document exemption, and the rule
reports 47 findings on a clean tree. Too few and too many are the same mistake one
clause apart. `CommittedDefectTest` reads the duplicate out of git rather than from a
fixture written after the repair, and asserts both lines are byte-identical — the
shape is a merge artefact, not a document that repeats itself.

**A value occurring where something else is meant is the same shape, with a new
environment** (D047, defect 22, T-0056). `docs/process/experiment-protocol.md`
claimed `005-knitting-bounded-search` was exact on `113/113` checked cases while
its `results.json` says `cases_with_oracle: 115`. The tempting rule — *does this
number occur anywhere in the artifact?* — answers **yes**, because `113` also sits
at `patch_cost_sensitivity/*/cases`. So the obvious gate is green on the defect,
and shipping it would have added coverage in appearance only.

What makes this an instance of the pattern above rather than a new one: the
question a reader answers ("is 113 in this file?") is not the property being
claimed ("how many cases did this experiment check?"), and both answers are
correct. Deciding the property instead of the field is what changed the outcome:

| What the number is | What it is held to | Why that is decidable |
|---|---|---|
| fraction `N/M` | a count the artifact **declares** — an integer field naming cases/fixtures/instances, or the length of `cases` | a fraction *means* "N out of M things", so M names a population |
| decimal | any value the artifact states, however deep | two significant figures coinciding is not a realistic way to become false unnoticed |
| bare integer | nothing | a threshold, a version and a count are the same shape |

Two shape rules were written and dropped before this one. Reading *every* value in
the file is the false negative above. Reading only "headline" values — top-level
scalars — needs a case per artifact and on this tree admits either `113` (three
levels down in `patch_cost_sensitivity`) or `006`'s true `0.833` (three levels
down under its own `kill_gate`), never both: the borrowed-predicate mistake D042
records, one level up. The rule that survives reads the number, not the file.

`tests/test_result_numbers_falsified.py` asserts the *blindness* of the rejected
rule on the defect's own bytes, so the restriction cannot be dropped quietly — the
second direction, and the one that is easy to leave out.

**A rule that reads a value must read the *property*, not the file.** T-0056's
gate answers "how many cases does this record say were checked?", and the obvious
version of it answers "does the number `113` occur in `results.json`?" — which is
*yes*, because `113` also sits at `patch_cost_sensitivity/*/cases`. The obvious gate
was therefore green on the defect it was written for. Two shape rules were tried and
dropped before the one that works: reading every value in the file is the false
negative above, and reading only top-level "headline" scalars needs a case per
artefact (it admits either `113` at depth 3 or `006`'s true `0.833` at depth 3 under
its own `kill_gate`, never both). Reading the number's **shape** — a fraction's
denominator names a population, a decimal is distinctive, a bare integer is ambiguous
— is what settles it, and `tests/test_result_numbers_falsified.py` asserts the
blindness so the restriction cannot be dropped quietly.

**A rule can read nothing and look like a clean tree.** Two of T-0056's own bugs were
exactly that, and both were found by a test rather than by reading the code: a decimal
guard that rejected any following dot, so every number ending a sentence was silently
discarded; and a measurement script that excluded nested repositories by testing for
`.worktrees` in a path's parts — false for the worktree it was running in, so it
reported **zero documents**. The second is defect 19's shape again, a verdict decided
by where the checkout sits rather than by what the repository holds. Both were caught
because the count was zero or absent, which is the kind of number a reader should
never have to accept.
