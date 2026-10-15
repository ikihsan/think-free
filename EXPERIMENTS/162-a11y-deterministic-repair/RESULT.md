<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E162 — a deterministic accessibility repairer cannot close the gap, and the
# reason is not that the program is weak

**Question.** Can a small deterministic program remove a substantial share of
real axe violations **without inventing anything**, and what does a repairer
that invents things cost the page?

**Answer.** No, and the reason is structural rather than a shortfall of the
repair table. On 27 real pages, a repairer forbidden to write a string no author
wrote eliminated **0 of 125** WCAG-tagged violations against a declared 30%
gate. The same table, permitted to invent, eliminated **99 (79.2%)** — and
**104 of its 104 repairs were fabrications**. Of the 121 violation instances
whose defect *is* a missing name, **120 (99.2%) had no name available to read
anywhere in the node axe reported**: `<a id="__codelineno-0-1"
href="#__codelineno-0-1"></a>`, `<div class="md-progress" role="progressbar">`,
`<input class="md-toggle" id="__search">`. The rule table's cross-element
paths — `alt` from `title`, `figcaption` or a wrapping `<label>`, a link name
from a nested image's `alt`, a button name from `value`, `lang` from
`xml:lang`, a document title from the `h1` — had no source on these pages
either, which is what the 145 recorded abstentions say. **The scope is stated
exactly: this closes the repair table as written, which includes ten authored
text paths and four structural ones. A wider table is a different experiment,
and the class of defect it would need to beat is the class where the answer is
only knowable at runtime.**

**What this closes.** The autofix candidate line, on mechanism, by its own
predeclared kill gate. Nothing was built for release and nothing is claimed as
a product.

## 1. The population and the oracle

27 pages with status 200, from 29 declared URLs across three declared frames —
UK public sector, US public sector, independent project documentation — stored
with their sha256 in `corpus-manifest.json` before any repair was written. Two
bodies (`manchester.gov.uk`, `ed.gov`) answered **403 with a bot-challenge
page** and are excluded by the protocol's status-200 rule.

axe-core 4.14.0 in jsdom, default ruleset, page JavaScript **not** executed
(Amendment 2). jsdom performs no layout, so 27 `color-contrast` and 31
`form-field-multiple-labels` instances sit in `incomplete`, not `violations`.
**Every number below is about rules decidable from the DOM.**

216 violation instances on 21 of 27 pages; **125 of them WCAG-tagged**.

## 2. The headline contrast, and what it is made of

| | Arm A — blanket | Arm B — conservative |
|---|---|---|
| WCAG-tagged violations after repair | **26** | **125** |
| eliminated | **99 (79.2%)** | **0 (0.0%)** |
| repairs applied | 104 | **0**, and 145 abstentions each with a reason |
| of those, fabrications | **104 (100%)** | **0** — none applied |
| newly introduced | 3 | 0 |

Arm A's entire advantage is manufactured strings. Ninety of the 99 WCAG
violations it removed are **Pygments code-line anchors** on one documentation
page — arm A's `aria-label="link"` on `<a id="__codelineno-0-1">` is 90.9% of
its headline improvement, and no user ever navigates to those anchors.

**Arm B applied nothing at all.** It saw 145 repairable instances and abstained
on every one, recording why: 100 `link-name` (*no authored name for this
link*), 13 `label` and 2 `frame-title` (*no derivable value*), 4 `image-alt`,
26 `region`. In run 1 — before Amendment 4's one-line idempotence condition —
arm B did apply 11 repairs, all of them `region`, which axe tags
`best-practice` rather than WCAG; they eliminated 28 instances, **0 of them
AA-tagged**, and introduced 35. **Not one WCAG-tagged defect had a derivable
repair in either run.**

*Provenance correction, made by the session that closed the experiment: this
table's first draft carried run 1's arm-B repair count (11) beside run 2's arm-A
figures, because the canonical `results-arm*.json` were rewritten by a
backgrounded re-run at 03:40 on 2026-10-15 — after the draft was written and
after the last recorded command event. The gate table in §6 is computed from the
final bytes, the arm files were re-summarised under capture, and §5's
from-scratch re-run then reproduced both arms exactly.

## 3. Why the mechanism is unavailable, measured without any repair table

The strongest objection to §2 is that the repairer is too weak. `why-not.js`
answers it with no repairer in the loop: for every arm-0 instance it takes the
node markup axe itself reported and asks whether the node carries **any**
author-written string — text content, or `alt`/`title`/`aria-label`/
`placeholder`/`value`/`summary`/`aria-roledescription`.

| | Instances | carried a string |
|---|---|---|
| all arm-0 instances | 216 | 57 (26.4%) |
| **instances whose defect is a missing name** | **121** | **1 (0.8%)** |

Per rule, the name-defect classes:

| rule | instances | carried a readable name |
|---|---|---|
| `link-name` | 96 | 1 |
| `label` | 13 | 0 |
| `role-img-alt` | 3 | 0 |
| `aria-dialog-name` | 2 | 0 |
| `frame-title` | 2 | 0 |
| `aria-progressbar-name` | 2 | 0 |
| `image-alt`, `aria-valid-attr-value`, `aria-allowed-attr` | 1 each | 0 |

**This file's own first version got this wrong and the fix is the finding.**
With the HTML `name` attribute counted as a name, 94.8% of the 96 `link-name`
instances looked readable — because 90 of them are
`<a id="__codelineno-0-1" name="__codelineno-0-1" href="#__codelineno-0-1">`,
whose `name` is a JavaScript anchor. HTML `name` does not compute an accessible
name on `<a>`. An instrument that counts plumbing as content reports a
mechanism as available when it is not.

## 4. The oracle's denominator is mostly plumbing

`oracle-noise.js`, on the same 216 instances, two narrow buckets:

| | Instances | Share of the 125 WCAG-tagged |
|---|---|---|
| content | 124 | 33 (26.4%) |
| **generated line anchor** (a syntax highlighter's per-line anchor) | **90** | 90 (72.0%) |
| empty anchor (`<a href=""></a>`) | 2 | 2 (1.6%) |

One page carries 98 of 216 instances. So **73.6% of the WCAG-tagged violations
on these pages are aimed at anchors no user navigates to**, and the
"accessibility score" every team acts on counts them like any other. Any tool
that "fixed" them — by inventing `link` as their name — would improve the score
by 72 points of pure cosmetics.

## 5. Run 1 versus run 2, and the two repair-table defects the oracle caught

Both runs are kept. `lib/repair-run1.js` produced `results-run1-arm*.json`;
Amendment 4's one-line idempotence fix produced the canonical run.

| Arm A | run 1 | run 2 (canonical) |
|---|---|---|
| eliminated | 131 | 104 |
| introduced | **37** | **3** |
| `region` applications | 11 | 0 (abstains on every page) |

Run 1's `region` repair ran once per violation node and created a *new*
`<main>` each time: 11 applications produced 13 `landmark-unique` and 11
`landmark-no-duplicate-main` violations — **it manufactured the defects the
rules it was aliased to check for.** Amendment 3 had already caught the first
version of this (it wrapped `<header>`/`<nav>`/`<footer>`, manufacturing
`landmark-*-is-top-level`). **Rule: a repair that runs more than once on a
document must be idempotent, and the oracle is the only thing that will tell
you.**

Run 2's residual 3 introduced violations are a different and genuine finding:
arm A's `alt=""` on an image satisfies `image-alt` by declaring the image
decorative, and **creates** `role-img-alt` on the same element. Silencing one
rule and breaking another is a failure, not a win — the protocol says so and the
oracle agrees.

**Run 2 was then reproduced from scratch, and it is byte-for-byte the same
experiment.** The closing session split `lib/repair.js` (393 lines) at the
300-line cap into `lib/dom.js`, `lib/rules.js`, `lib/dispatch.js` and
`lib/repair.js`, and re-ran both arms over the whole corpus under capture. Over
all 27 pages the fresh run is **identical to the recorded one on every field,
including all 145 abstention records in arm B** — 0 differences against
`results-run2-arm*.json`. Two facts, one run: the split is behaviour-preserving,
and axe-core in jsdom over a fixed DOM is **reproducible here**, which
Amendment 2 had asserted and nothing had measured. Run 1's table is kept
replayable the same way, as `lib/rules-run1.js` + `lib/dispatch-run1.js` bound
to the same driver by `lib/repair-run1.js`.

## 6. Gate table

Computed by `analyze.js` from the recorded files against the thresholds in
`PROTOCOL.md`; nothing here was chosen after a number was seen.

| Gate | Declared | Observed | Verdict |
|---|---|---|---|
| G0 oracle validity | axe runs on ≥22 of 24 pages; ≥1 violation on ≥12 pages | axe ran on 27; 21 pages had ≥1 violation | **PASS** |
| **G1 repairable share (arm B)** | eliminates ≥ 30% of arm-0 AA-tagged instances | **0.0% (0 of 125)** | **FAIL** |
| G2 no fabrication (arm B) | fabrication rate ≤ 0.02 | **undefined — 0 repairs applied** (run 1: 0.0000 over 11) | **FAIL, vacuous** |
| G3 no regression | ≤1% newly introduced per eliminated, every frame, each arm | arm A frame B: **3 new / 7 eliminated = 42.9%** | **FAIL** |
| G4 population (arm B) | repairs on ≥8 pages, ≥3 frames | **0 pages** | **FAIL** |

G1 is the kill gate and it fails by the widest margin the protocol allows a
gate to fail. G2's mechanical verdict is worth reading precisely: `analyze.js`
scores a null rate as FAIL, and in the canonical run arm B's rate is null
because it repaired nothing — the gate is *vacuous*, not violated, and run 1
measured it at 0.0000. G3's failure is arm A's `alt=""` (§5), not arm B's.
**Nothing here is a defect in the pages, and nothing here is a defect in the
oracle: it is the class of defect that is reachable.**

## 7. What this closes, and what it does not decide

**Closed:** the deterministic, no-fabrication accessibility repairer **as
written** — ten authored-text derivation paths, four structural repairs, two
policies over one table — on mechanism, by the declared kill gate. The reason is
a property of the defects: the dominant class *is the absence of author-written
text*, which no rule can manufacture without lying — and that also explains,
rather than merely observes, why the 2026 tooling ecosystem is full of LLM
fixers ([`PRIOR-ART.md`](PRIOR-ART.md)): the one thing a model can do here is
write the sentence nobody wrote.

**Not closed, and named so the scope is not overread:** a *wider* deterministic
repair table. What is closed is the on-document derivation mechanism on this
population; a table that associates a link with the code line it sits beside, or
reads a `role="progressbar"`'s value out of the script that sets it, is a
different instrument, and the second of those is not decidable without
executing the page — which Amendment 2 ruled out for good reason.

**Not decided:** demand. Nothing here measures whether anyone would install a
repairer of either kind. **Not measured:** real-browser behaviour (jsdom runs
no CSS), and assistive-technology outcomes — `fabrication` is a mechanical
proxy for "made the page worse", not a screen-reader measurement.

**Not a prevalence claim.** 27 pages cannot estimate how broken the web is, and
§4 shows why one of those pages would badly distort such an estimate.

## 8. The single most useful next action

**Count real defects with the plumbing excluded, on a population chosen for
defect density rather than for fame.** §4 is the reproducible part: the same
27 pages yield 33 content-bearing WCAG-tagged defects instead of 125, and the
composition changes completely — no single rule holds 77% of the denominator.
Every accessibility number in circulation, including the ones that justify
buying tools, is computed on the unfiltered denominator. One honest frame — 30
to 50 pages chosen because they are *known* to violate something, excluding
generated anchors and empty links before any class is counted — would say
whether the dominant class of real WCAG defects is a name nobody wrote, or an
overwhelming share of the same plumbing E162 just measured.

**Do not fix the repair table again.** Amendment 4 declared one fix and one
re-run; that bound was kept.