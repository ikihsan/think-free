<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E041 — AMENDMENT-1: the repository set is selected by a rule, not by name

**Written after the mechanism yield was read and before any similarity between
two rows was computed.** The only numbers read before this file existed are the
two below, and both are properties of *what the source can serve* — the question
D067 says to ask before measuring a population, not the question this experiment
answers.

## What the yield reading was, and what it is not

`pallets/click`, captured completely and reconciled against the API's own
`total_count`: **1809 issues, 16 labelled `state_reason: "duplicate"` — a share
of 0.0088** — and of those 16, **1** had a parseable `#N` naming another issue
**inside the same captured repository**. Fourteen named no issue at all; they
reference pull requests, documentation URLs, or other projects. One named an
issue outside the capture.

So the declared repository list yields **1 positive pair per 1809 issues**. At
that rate, G1's paired-difference interval and G2's top-1 accuracy cannot
resolve anything: the arm would be about five rows long.

**This is a yield finding about repository choice, not a result.** No similarity
was computed, no gate was evaluated, and nothing about whether the instrument
finds repeats has been touched. It says one thing only: *triage volume and
duplicate-closure rate are different properties of a repository, and a list of
famous libraries is a list of the wrong one.*

## The choice

The protocol fixed a list of ten repositories by name and said they would not be
replaced by better yield. The opening was real: **which repositories can supply a
positive control at all**, and a by-name list of famous libraries is a
demonstrably poor choice for that. Three options were available. Capture more
repositories from the same by-name list and accept a five-row arm. Abandon the
control. Or **select repositories by the property the control needs, by a rule
fixed in advance**.

**The third was taken.**

## The rule, fixed now

**Screening, ten requests.** `GET /search/issues?q=is:issue+reason:duplicate+"duplicate+of+#"`,
ten pages of 100. Every returned row's body is parsed with the **same six
declared reference patterns**, and the count of rows that name a parseable target
is recorded **per repository**. This is the platform telling me which
repositories duplicate-close, at a cost of ten requests and no capture at all.

**Selection.** Repositories are appended in **descending order of that
parseable-reference count**, ties broken by repository name ascending, and the
first **six** are captured completely. Six, not ten: the yield per repository
measured on the screening sample is 0.18 parseable references per returned row,
so six repositories chosen *for* references should yield a usable arm at a
fraction of the requests the by-name list needed.

**The exclusion rule is unchanged and still fires first.** A repository whose
duplicate-labelled share exceeds **0.20** in its own capture is excluded as
automated, with the share recorded. Screening on `reason:duplicate` makes this
check more important, not less, because it is now selecting for the very label
that rule polices.

**One screening constraint, declared now for the same reason — and then withdrawn
by the correction below.** `stars:>500`, on the reasoning that a repository which
mass-closes issues as duplicates is the automation case.

## The original list is kept, not discarded

**The declared ten remain in the corpus and are reported as a separate arm**,
`P-by-name`, alongside the extended arm `P-screened`. Every gate is evaluated on
each. This is deliberate and it is the F044 discipline: the by-name selection was
a real choice made on real reasoning, it turned out to have a 0.9% yield, and
deleting it would leave a reader unable to see that the choice was made and what
it cost. **The pooled verdict is taken on the arm with the larger positive
population, and both verdicts are printed.**

## CORRECTION — `stars:>500` is withdrawn, and the reason is a finding

The screening query was run once with `stars:>500` in it and returned **89 rows
in total**. That is not a plausible population, so the qualifier itself was
measured rather than trusted, before any similarity was computed:

| query | `total_count` |
|---|---|
| `is:issue reason:duplicate` | **358,471** |
| `is:issue reason:duplicate "duplicate of"` | 96,971 |
| `is:issue reason:duplicate "duplicate of #"` | 96,971 |
| `is:issue reason:duplicate stars:>500` | **107** |
| `is:issue reason:duplicate stars:>500 "duplicate of #"` | 89 |
| `is:issue reason:duplicate in:body "duplicate of #" stars:>100` | **0** |

**A repository-scoped qualifier takes this population down by a factor of 3350
and, combined with an `in:body` restriction, to zero.** Whatever the cause, the
consequence for this experiment is the same: **`stars:` cannot be used to
restrict this query**, and a screening rule that looked like a free precision
filter was in fact discarding the population.

**This is the tenth instance of the shape F055, F058 and F059 record, and the
first caught before the measurement rather than after it.** The qualifier is a
property of the *instrument's selection*, and reading it before using it cost
seven requests and changed the design. Had it been left in, the run would have
reported "89 issues, 3 repositories, 1 pair" and the honest-looking conclusion
would have been that no reachable repository supplies pairs — a conclusion about
**the query** presented as a conclusion about **the world**, which is exactly the
error those three findings are about.

**Withdrawn:** `stars:>500`. **Replaced by:** nothing. The automation guard is
the 0.20 duplicate-share exclusion, which is computed on the capture itself and
needs no qualifier. **Not replaced by a heuristic:** no new filter is invented to
occupy the space, because a substitute would carry the same unverifiable
assumption the withdrawn one carried.

## What this amendment does not decide

- It does not make the two populations interchangeable. Repositories selected
  *for* duplicate closure differ from repositories selected *for* being famous,
  in their moderation culture, their user base, and their text. A gate met on
  `P-screened` is evidence about the instrument on **screened repositories**,
  and the ceiling travels with it.
- It does not change the bars. 1.5, 0.20, 0.50 and 0.50 are as declared.
- It does not touch the two text units, the grid, the metric, or the gates.
- **A 422 from the search API is a hard failure, not a retry.** `tiangolo/typer`
  returns 422 because the repository was renamed, and the first capture spent two
  minutes in a retry loop on it. Non-retryable statuses are recorded and the
  repository is skipped, which is what the protocol's "reported as unreconciled
  and excluded" clause already required.
