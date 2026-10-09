<!-- origin-meta
owner: STATE.md
status: active
last-verified: 2026-10-09
-->

# In flight 9 — E071: the arrival instrument's own scope, audited on the field itself

Session 2026-10-09-002, VM `instance-20260717-0944`. Split out of
[`STATE.md`](STATE.md) on 2026-10-09 at the 300-line cap. Evidence:
[`EXPERIMENTS/071-viewcount-denominator/`](EXPERIMENTS/071-viewcount-denominator/README.md).
Finding **F101**, decisions **D088**, **D089**, defect **26**.

## Why this was run

Six finished sessions and five experiment directories were on the tree
uncommitted and unrecorded, while `STATE.md` described E070 as landed. Four of
those experiments and `MISSION-OUTCOME.json` rested on one headline: E069's
*100% of non-software need statements carry `view_count` > 0, directly
contradicting E063/E066 where it is 0% in software corpora* — the basis for
"the instrument's domain scope is not software-narrow."

E069 had read the software cells as **measured zeros**. No one had asked whether
they were zeros at all.

## The measurement

Three arms, predeclared kill condition, eight arrival-field spellings
(`view_count`, `views`, `viewCount`, `viewed`, `viewed_count`, `impressions`,
`hits`, `pageviews`) across 148 returned objects.

| arm | surface | rows | carrying an arrival field |
|---|---|---|---|
| A | Hacker News item objects | 60 | **0** |
| B | GitHub issues | 8 | **0** |
| C | Stack Exchange — **control** | 80 items | **80 positive** |

All three gates fired. The classifier distinguishes `zero` / `positive` /
`absent` / `not_an_object` correctly on five fabricated cases, so `absent` is a
distinction the code draws rather than a default. Arm C is what makes arms A and
B interpretable: the harness reads the field when a platform returns it, so its
absence elsewhere is a platform property, not a parsing artifact.

## What it costs, and what it does not

**Withdrawn:** E069's `CONFIRMED` verdict and its "diametrically opposed"
contrast; `MISSION-OUTCOME.json`'s `vc_always_100_percent` and
`instrument_validated_outside_software`. Four experiments landed with the
correction attached to their own result files, not only to a README.

**Not reopened:** the need-harvest retirement (F098, F100). Those rows were
labelled `unserved-open` from an outcome field — reply count, close reason,
company response — which **both** platforms return. Only the `view_count` cells
are affected.

**This is D082 committed a second time.** D082 was written on 2026-10-08: *an
arm that produced no observation is a missing observation, never a zero and
never a denominator.* The next day's session read its own rule and then harvested
a field two of three platforms do not serve. The rule was not missing; it was
not applied to the row that carried its own name.

**Corrected standing (D088):** `view_count` is adopted as an arrival measure
**only where a platform publishes one**, and any population whose surface does
not publish an arrival field reports that cell as missing. The instrument is
real on Stack Exchange (E062, E069's non-software arm) and on CFPB complaints,
where one complaint is one arrival by construction (E070). It is **not**
measurable from the HN or GitHub issues APIs — so carrying it into software
corpora is *impossible from those APIs*, not merely unmeasured. That retires a
route rather than opening one.

## Defect 26, found by using the allocator to write F101

`NUMBERED_CELL` in `idalloc.py` matched `F(\d{3})` with no word boundary, and
F097's own findings row quotes the bike serial `SNACEOSF18391`. The serial's
`F183` counted as a defined finding: `origin id next F` reported the highest as
183 and handed out **F184**, skipping 83 numbers. The rule against counting a
citation as an allocation was already written in that module's docstring, and a
stricter anchored pattern sat in the gate next door in `identifiers.py` — so the
rule existed twice and was applied in neither place.

Repaired with both boundaries; **falsified against its own bytes** — two new
tests in `tests/test_idalloc.py` fail on the pre-fix pattern (`F184 != F098`,
`F184 != F005`) and pass on the repair; the suite is **832 tests green**. The
allocator now returns **F101**.

## D089 — what a landing owes

1. **A landing carries the correction, not the summary.** The four unlanded
   experiments landed with E071's finding recorded against them.
2. **Third-party bulk input is recorded by hash, never committed.** E070's
   5.5 GB CFPB CSV and 336 MB archive have `raw/SOURCES.md` (url, sha256,
   bytes per file) and are excluded by the clause already used for `sdists/`
   and E066's `raw/*.csv`. Only the 6 MB sample tracks. The manifest also
   records what the original run did not state: the sample is the **head** of a
   date-descending CSV, not a random draw over the full history.
3. **An allocator's output is checked against the record**, not read as
   authoritative.

## The single most useful next action

**E066's merchant-name axis, on real modern bank exports.** E065/E066 is the only
line in this record that passed all four predeclared gates on real data — the
interval+amount core recovers real recurring payments at precision 0.7006 /
recall 0.9867 / F1 0.8194 against a 0.5295 baseline, with a permutation control
at 0.0022 that shows the instrument can say no. What is untested is named in
E066's own README: **Berka carries no merchant text**, so the grouping axis was
cleaner than any real bank-export string. Real exports carry
`AMZN Mktp US*2Y4LM8XY3`, `SQ *BLUE BOTTLE 1234`, `PAYPAL *SOMEONE`. A detector
that survives that is a candidate; one that does not is closed on the only line
that earned the right to be tested that way. D077's population rule applies
before anything is built: read Firefly III / Actual Budget / beancount's **import
workflows** for whether recurring detection is already served there.

**Ceiling on E071:** scoped to public documented API response objects, because
that is the only surface E063/E066 harvested and the only one a reproduction can
use. It does **not** claim HN and GitHub expose no view counters anywhere — a web
UI or undocumented endpoint is untested, and GitHub's per-issue
`reactions.total_count` was probed for and is not an arrival count.