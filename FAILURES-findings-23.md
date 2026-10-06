<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Failures — recorded finding F057

Split out of [`FAILURES-findings-22.md`](FAILURES-findings-22.md), which held
F053–F056 at 288 of 300 lines. See [`FAILURES.md`](FAILURES.md) for the index.
**Identifiers are stable across all findings files.**

## F057 — the per-tag spread is real, reproducible, and not attributable: two of E034's three declared claims did not survive its own run

**Status: a design that produced the numbers and could not read them.** `EXPERIMENTS/034-reask-tail/`,
T-0078, 2026-10-06. What fired: the pooled gradient on all four variants, the per-tag
kill gate A4, and AMENDMENT-1's replication of both extremes. What failed: **D6**, the
attribution of the spread, and **B1**, the mechanism the proposed application rests on.
A third declared claim — the a-priori stratum hypothesis — is falsified outright.

### What the run measured, and what is safe to keep

Three matched arms of the same tag on one route, 2124 rows over eight tags, labelled by
Stack Exchange's own `closed_reason == "Duplicate"`. Pooled duplicate-closure rate:
**tail 0.1352 [0.1122, 0.1620]**, score head **0.0371**, **`Active` tab 0.0303
[0.0201, 0.0455]**. **4.5× against the ordering a person actually reads**, on equal
denominators too. This replicates F055's whole-site gradient on an independent,
tag-stratified population, and **F055 stands**.

### Failure 1 — the spread cannot be apportioned between tag and site (D6)

Per-tag tail rates run **0.0000 to 0.4300**, with 12 disjoint interval pairs among the
seven tags clearing n ≥ 50, and both extremes reproducing on the next four pages
(`customs` 0.430→0.495, `excel-formula` 0.000→0.000). That part is solid.

It is not attributable, because **duplicate closure is a moderator act**. A community's
closing practice is a first-class explanation of a rate this instrument cannot observe,
and the declared population had **one `travel` tag and three `math` tags against five
`stackoverflow` ones**, so the highest cell was the only cell from its site. AMENDMENT-1
added one more tag on each of the two sites that produced an extreme —
`travel`/`baggage` 0.1979 and `math`/`calculus` 0.1020 — and the unambiguous statistic
answers **4/10 within-site disjoint pairs against 14/26 cross-site**.

**Site carries a real part of the variance and tag carries a real part, and three to
five tags per site cannot say how much of each.** The per-tag reading — the entire
differentiating output of the proposed tool — is therefore **not established**, even
though the kill gate it was gated on fired.

**The declared R2 gate was also ill-formed, and it was ill-formed before the fetch.**
It read "`baggage`'s CI95 is disjoint from **both** math tags", and the data gave
`baggage` disjoint from `probability` and `linear-algebra` but overlapping `calculus`, so
both declared branches could fire at once. A binary gate over a pair-relation needs an
exclusive partition; the fix was a statistic (D6's density) rather than a threshold, and
it should have been declared that way. This is D062's shape one level up: the linkage
rule here was not the candidate-pair rule but the **decision rule applied to a relation
between candidates**, and nothing tested whether it could return two answers.

### Failure 2 — the mechanism the application claims is not measurable here (B1)

The proposed reading of a duplicate closure is *"the answer existed and was not found."*
B1 tested the observable half: among duplicates, the share with no accepted answer.
Tail **0.8163**, `Active` tab **0.7273**, difference **CI95 [−0.0774, +0.3075]** —
spans zero. **This run cannot separate "people re-asked it" from "moderators closed it",
nor "nobody answered it" from "closure hides the answer".** E033 had already recorded the
second half of that error (AMENDMENT-3 §2) and E034 walked into it anyway, because the
label is *about* closing and nothing in the protocol asked whether closing could produce
the difference by itself.

What is established is **where the repeats sit, not what happened to them** — which is a
narrower result than the one the run was declared to produce, and it is the first
demand-side instrument in this record that returned positives at all.

### Failure 3 — the a-priori stratum hypothesis is backwards

`PROTOCOL.md` §3 declared two tags per stratum on the reasoning that *a tag with one
obvious canonical answer should be findable*. The prediction is inverted on this
population: **`excel-formula`, the situational exemplar, has the lowest tail rate of all
ten tags at 0 of 100**, while the "one canonical answer" tags sit at 0.12–0.19. The
hypothesis was declared before the fetch and it is dead, with nothing replacing it. It is
recorded because a stratum rule that was declared, could have failed, and did, is the only
kind worth reading — and because it means §3's stratum column is decoration in every
number above.

### Two instrument facts that outlive this run

- **The canonical edge is unreachable from this host.** Nine named channels: four
  vectorised `{ids}` routes (E033), the question page and `stackoverflow.com` with a
  browser User-Agent (Cloudflare 403), both StackPrinter hosts (1213-byte "server too
  busy", four attempts), SEDE (403), the question's own **comments** (no system comment
  naming a canonical), the answer's **`closed_details`** (field absent), and the
  `closed_details` filter itself (`400 invalid filter`). **A duplicate closure is a
  reliable label and an unreachable edge**, and any future instrument here is built on the
  label alone. This closes E033's open question "what to measure recurrence on" on its
  other half.
- **The label is a set of literals, not one.** `closed_reason` is absent on all 1790 open
  rows and present on every one of the 724 closed rows — **no row is closed without
  stating a reason**, so absence means "not closed" and nothing is imputed. But ten
  literals occur, and **`exact duplicate` (9 rows) is the legacy spelling of `Duplicate`
  (222)**. The primary label is the exact literal, which is conservative: including the
  legacy spelling raises the pooled tail rate from 0.1352 to 0.1462. **E033's published
  0.0540 is a floor for the same reason**, and so is every rate derived from it.

### Ceiling

One platform, one label, and a label that means *a moderator judged these two the same*.
Nothing here separates that from findability. The tail arm is the most-downvoted
questions and four pages of `order=asc` never reach score ≥ +1, so the comparison is
{score ≤ 0} against {score ≥ 30} with an unsampled gap; within the tail, score −2..0 runs
0.4933 against 0.0938 at score ≤ −3, which argues against "closure earns the downvotes"
but does not rule out that both happen. Three to five tags per site cannot apportion site
from tag. And **whether anyone acts on a per-tag reading is entirely unmeasured** — that
is the adoption question, and no gate here touches it.

---

## F058 — the population is not one that was overlooked, and its ordering is offered by no surface

**Status: an experiment's motivating frame falsified by its own successor's free reads, and
the mission's top-ranked next action re-scoped for the cost of a re-read.** `EXPERIMENTS/035-unanswered-surface/`,
session 2026-10-06-004, `observed` 2026-10-06. Four results over E034's committed bytes, at
zero quota cost; full numbers and digests in
[`EXPERIMENTS/035-unanswered-surface/README.md`](EXPERIMENTS/035-unanswered-surface/README.md).

**What E034 §1 assumed, and what the bytes say.** Its protocol motivates the whole
candidate on the claim that the questions worth surfacing are "the ones the ranked feed is
worst at showing", with the implication that people are failing to find answers that
exist. Within E034's own tail arm the duplicate-closed rows have a **higher** median view
count than their non-duplicate neighbours — **251 against 193**, means 1612 against 906 —
and the arm's median age is **8.49 years** against the `Active` tab's 5.53. These questions
have been read about 200 times each and the duplicates slightly more than their neighbours.
**The findability framing is falsified.** What exists is an eight-year-old backlog with a
measured duplicate rate, which is a different product with a different user; `STATE.md`'s
framing of this line as a *rescue* should not survive into a build.

**The `Active` tab is not a thinner copy of the population — for two of eight tags the two
sets do not intersect.** `stackoverflow`/`python`: tail −34…−11 against `Active` −9…304.
`math`/`probability`: tail −9…−4 against `Active` −2…159. A "4.5× gradient" reads very
differently as a statement about *membership* than as a statement about density, and the
stronger statement is the one the bytes support.

**And no rendered Stack Overflow tag page offers the ordering at all.** With
`stackoverflow.com` behind a Cloudflare challenge from this host on every path, a
2026-09-26 Wayback snapshot of a real tag page was read: **409,639 bytes of first-party
rendered HTML**, whose tab bar offers `Newest · Active · Votes · Frequent · Trending ·
Bounties · Unanswered` scoped by `Week`/`Month`, and which contains **0 occurrences** of
`oldest`, `order=asc`, `sort=votes&order=asc`, `lowest.vote` or `ascending`.
`not_measured`: the *direction* of `tab=Votes`, because the archive refused that snapshot.

**Correction (F059, E036, 2026-10-06).** This was a correct reading of a tag page and was
used as a statement about the platform. It is not one: `/search/advanced` accepts
`sort=votes&order=asc&tagged=…` and returned **81 of E034's 100 `git` tail ids** in one
unauthenticated request, ascending, with the closure label already in the response. The
sentence above is now scoped to **rendered tag pages** and the platform-wide reading is
withdrawn (**D066**). The evidence is unaffected; the claim it was asked to support is not.

**The declared remedy for D6 was aimed at the wrong constraint.** Item 0e ranked "three to
four more tags on each of the three sites, about 30 requests" the mission's top action.
Between-tag excess variance on the arcsine scale reads **+0.0417** pooled and **+0.0420
within `stackoverflow` alone** — the four `stackoverflow` tags run 0.000 / 0.130 / 0.150 /
0.210, a clean ladder, and their spread inside one site *equals* the whole spread. Tag
variance is already reproducible without a site, so the binding constraint was never
per-tag resolution. The residual question is only whether `travel`'s two tags are high
*because of travel*. Separately, the objection that a rank-selected tail is a
non-comparable stratum is **unsupported**: r(tag mean tail score, tag rate) = +0.2485,
t = 0.725, df = 8, `not_established`.

### The rule, and the reading it licenses

**Before spending a declared remedy on a population, check on the committed bytes whether
the premise it addresses is still the binding one.** Four questions here — is the
population reachable, are the compared arms one population, is the declared remedy aimed at
the constraint, and does the obvious objection survive — cost zero requests and reordered
the mission's top item. The reverse is the standing risk: three consecutive sessions have
now spent Stack Exchange quota, and this one spent 19 of a shared 300 mostly discovering
that the label is unreadable on the one route that mattered.

### Ceiling

This is a re-reading of one population of 1125 tail rows on three sites, plus one archive
snapshot of one tag page on one site. `travel`/`customs` at 0.4650 and
`stackoverflow`/`excel-formula` at 0.0000 both remain single cells, and R3-style variance
components on 4/2/3 tags per site are not sufficient to apportion tag against site.
**Nothing here measures whether anyone wants the backlog surfaced**, which is the whole
adoption question, and the run that followed it left its own density gate `not_evaluated`.
