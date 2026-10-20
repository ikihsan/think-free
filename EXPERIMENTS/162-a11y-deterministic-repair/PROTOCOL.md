<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E162 — protocol, declared before any page was fetched

**Question.** Real web pages carry real accessibility defects. axe-core finds
them, and it is the tool every team reaches for. axe-core **cannot fix
anything**: it reports. The available fixes are (a) a human, (b) an LLM, or
(c) a blanket mechanical edit someone scripts once. All three can make the
report go away without making the page better.

Can a small deterministic program remove a substantial share of real axe
violations **without inventing anything**, and what does a repairer that invents
things cost the page?

## Why this instrument

E122, E147, E150 and E160 all failed because synthetic fixtures made the
trivial classifier optimal (F147, and the pattern noted in `STATE.md`). This
experiment has the opposite property:

- the **oracle is an independent implementation** (axe-core 4.14.0, Deque,
  the de facto standard, 4.14.0 published 2026-10-05) run on **real pages
  nobody here wrote**;
- the positives are what axe finds in the wild, not items constructed to match
  a classifier;
- the population is fetched and hashed before any repairer is written.

## Population (declared before fetching)

Three frames, 8 pages each, 24 total. One page per site: the root URL.

| Frame | Rule | Why |
|---|---|---|
| A — UK public sector | GOV.UK and 7 local-authority/council homepages | Public Sector Bodies Accessibility Regulations 2018: a legal duty |
| B — US public sector | 6 federal/state/city homepages, plus 2 | Section 508 / Title II: a legal duty |
| C — independent OSS docs | 8 project documentation sites | No legal duty; typical developer audience |

Selection rule for B and C: any site that serves HTML to a plain `GET` with
status 200. No cherry-picking on findings — **no page is replaced after a
finding is seen.** A site that fails to fetch is replaced by the next name on
the list, declared before the run. Each page is stored with its sha256 in
`corpus-manifest.json`.

This is a **mechanism** population, not a prevalence population. 24 pages
cannot estimate "how broken the web is" and no such claim will be made.

## Oracle

`axe-core` 4.14.0 inside `jsdom` 29.1.1, **default ruleset**, run once per
page per arm. Every result's `tags` are recorded, so the WCAG-2.2-AA-tagged
subset is reported beside the full default set. Two denominators, both
predeclared, no subset chosen after the fact.

**Known oracle limit, stated now:** jsdom performs no layout, so rules that
need rendered pixels or geometry — `color-contrast` above all — cannot run.
They appear in `incomplete`, not in `violations`. Every number below is about
rules decidable from the DOM.

## Arms

- **Arm 0 — status quo.** The page as served, round-tripped through the DOM
  serializer and re-parsed, with no repair. This is the control: every arm
  below is compared to arm 0, so serialization cost is common to all arms.
- **Arm A — blanket.** A mechanical repair for every repairable class,
  including the ones that require inventing a name: `alt=""` on every image
  missing alt, `aria-label="link"` on every nameless link, `title="frame"`,
  `lang="en"`. This is what a rule-based autofixer does, and what an LLM does
  when told to make the report go away.
- **Arm B — conservative, abstain by default.** Applies a repair **only when
  the correct value is derivable from the document itself** — from text the
  author wrote, from an attribute already on the element, or from a structural
  fact the DOM already states. Otherwise it abstains and records why.

Arms A and B share one codebase and one rule table. The **only** difference is
one field per rule: `fabricates: true` or `false`. That is deliberate — it
makes the contrast an ablation of the fabrication policy, not a comparison of
two programs written by different people.

## Measures (predeclared)

1. **Violation instances** — axe nodes. Arm 0 vs each arm, per rule.
2. **Eliminated** — instances present in arm 0 and absent after repair.
3. **Newly introduced** — instances absent in arm 0 and present after repair.
   A repair that silences one rule and breaks another is a failure, not a win.
4. **Abstentions** — violations the arm deliberately left alone, by reason.
5. **Fabrication rate** — of the repairs applied, the share that put a
   user-facing string into the document which **no author wrote**: a value not
   present in the original document's text and not copied from an attribute
   already on that element. Computed mechanically, per repair, not per page.

Measure 5 is the one axe cannot see, which is the reason the experiment exists:
a page can score a perfect axe report and be worse to use than before.

## Gates (predeclared, before any page was fetched)

| Gate | Declared | Meaning if met |
|---|---|---|
| G0 oracle validity | axe runs on ≥ 22 of 24 pages; ≥ 1 violation on ≥ 12 distinct pages | the instrument works on this population |
| **G1 repairable share** | arm B eliminates ≥ **30%** of arm-0 AA-tagged violation instances | a deterministic repairer is worth building |
| **G2 no fabrication** | arm B's fabrication rate ≤ **0.02** | it can be built without inventing |
| G3 no regression | newly introduced ≤ **1%** of eliminated, in **every** frame | repairs are safe to apply to a live page |
| G4 population | repairs applied on ≥ **8 distinct pages**, ≥ 3 frames represented | the share is not one site's quirk |

**Where 30% came from, so it is not a number picked to be passed:** a third of
what a team must fix by hand is the smallest share that would change anyone's
workflow. Anything smaller is a linter, not a tool.

## Kill gate

**If G1 fails, the line closes on mechanism.** No deterministic repairer is
worth building, whatever the demand turns out to be. If G2 fails while G1
passes, the honest result is worse than nothing found: any deterministic
repairer that reaches the popular rule classes must invent accessible names,
so the axe score is being bought with the thing the score is supposed to
stand for.

## Amendment 1 — replacements, declared before the oracle ran on any page

The first fetch of the 24 declared URLs returned **21 pages with status 200**:
`manchester.gov.uk` and `ed.gov` answered **403** (bot mitigation, 5.6 KB and
11.6 KB challenge pages, not the site) and `docs.flask.palletsprojects.com`
failed to resolve. The protocol's status-200 rule excludes the two 403 bodies,
and its replacement rule covers the two fetch failures.

**No axe run had happened at the moment these four names were written down**,
and none has happened now. The replacements were declared on fetch outcome
alone, so nothing in this experiment's design was chosen after seeing a
finding.

| Frame | Replacement |
|---|---|
| A | `https://www.gov.wales/` , `https://www.reading.gov.uk/` |
| B | `https://www.dol.gov/` , `https://www.phoenix.gov/` |
| C | `https://docs.pydantic.dev/` , `https://docs.ansible.com/` |

Target stays 24 pages. If the replacement fetch again yields fewer than 24,
G0 is reported as declared, with the count actually obtained, rather than
restated against a changed threshold.

## Amendment 2 — page JavaScript is not executed

The first harness loaded each corpus page with `runScripts: "dangerously"`,
which executed the pages' own JavaScript. That is wrong on three counts and
was changed before any rule-level finding was read: it runs third-party code
from 27 fetched sites, it makes the measurement non-deterministic (two runs of
the same bytes need not agree), and the experiment is about the DOM. The
harness now uses `outside-only` and injects axe through `window.eval`.

Consequence, declared here rather than discovered later: content that only
appears after JavaScript runs is **not** in the measured DOM. These pages are
scored as a browser that never executed a script. The two partial arm-0 rows
produced under the old harness were discarded.

## Amendment 3 — one repair-table defect, found by the oracle and fixed

The first arm run produced **more newly introduced violations than eliminated
on every page it touched** (page 1: 5 new against 3 eliminated). G3 exists to
catch exactly this, and it fired on the first attempt.

The cause was in the repair table, not in the pages. Five `landmark-*` rules
were aliased to the `region` repair, which wraps body children in a `<main>`.
Applied to `landmark-unique` — "you have two `<main>` landmarks" — it added a
third. The repair manufactured the defect it was named for.

**What changed:** the `landmark-unique`, `landmark-no-duplicate-*` and
`landmark-*-is-top-level` aliases were deleted, so those rules are counted as
outside the table rather than repaired wrongly. The `region` repair was
narrowed to wrap only body children that are neither landmarks, nor
role-carrying, nor inert, and to place the new `<main>` after the last one so
document order is preserved.

**This is an implementation fix, and the first attempt's numbers are kept.** A
repairer whose own table introduces violations was never a measurement of
deterministic repair; it was a measurement of a bug. Both are recorded, and
the second run is reported as the experiment's result.

## Amendment 4 — the `region` repair is not idempotent, and the bound of the fix

The first completed run of both arms (`results-run1-armA.json`,
`results-run1-armB.json`, produced by `lib/repair-run1.js`, which is a verbatim
copy of the repair table as it stood) shows **new violations introduced by
every page where the `region` repair applied**. The rule table counts the
`region` repair as applied once per violation node, and each application
creates a *new* `<main>`: 11 applications on 12 pages produced 13
`landmark-unique` and 11 `landmark-no-duplicate-main` violations. Amendment 3
narrowed *which children* get wrapped; it did not make the repair apply at most
once.

G3 is a gate about the page, not about the repair table. A gate that fails
because the instrument is not idempotent is not a measurement.

**What changed, one condition:** `region` now abstains, with a recorded reason,
when the document already states where main content is — `main` or `[role=main]`
already present. With that one condition the repair is applicable at most once
per document and can never sit beside an existing `<main>`.

**The bound, declared before the re-run so it cannot become a loop:** this is
**one** repair-table fix and **one** re-run. Whatever the second run reports is
reported as the experiment's result. Run 1's numbers stay in the repository
next to it and are not deleted, and no third attempt is made, because the
gates that decide the mechanism (G1, G2, G4) are functions of the **rule
composition of real pages** — 96 of the 125 AA-tagged arm-0 instances are
`link-name`, which no idempotence change can reach — and only G3 depends on the
table being right.

## What this experiment cannot decide

- **Demand.** Nothing here measures whether anyone would install a repairer.
  Prior art was probed separately and recorded in `PRIOR-ART.md`.
- **Real-browser behaviour.** jsdom runs no CSS and no layout. A repair that
  passes here can still fail in Chrome.
- **Assistive-technology outcomes.** The harm measure is *fabrication* — a
  proxy for "made the page worse", not a measurement that a screen-reader user
  did worse.