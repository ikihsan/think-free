<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# Findings — failures and negative results, part 47

Local lineage (pre-merge F125–F129) renumbered on the 2026-10-20 merge, which
adopted upstream's F125–F143 for the same identifiers: this file holds **F147, F148**. Split out of
`FAILURES-findings-41.md`–`43.md` as they stood on `3bae5f6a`.
See [`FAILURES.md`](FAILURES.md) for the index. **Identifiers are stable across
all findings files.**
Continued from [`FAILURES-findings-46.md`](FAILURES-findings-46.md) (F144–F146).

---

## F147 — PostgreSQL deadlock classification: keyword baseline perfect on synthetic fixtures, structural classifier adds no value

**Observed 2026-10-14**, session `2026-10-14-031-run-t-0093-test-discriminating-observati`, experiment `E147` (`EXPERIMENTS/147-postgres-deadlock-classification/`).

**The claim:** A structural classifier using parsed lock modes, relation pairs, and query patterns beats a keyword-only baseline by ≥15pp on PostgreSQL deadlock report root cause classification (accuracy ≥80%).

**The result:** Claim falsified. On 27 synthetic fixtures (5 per category: fk_lock_contention, index_lock_contention, tuple_lock_contention, advisory_lock_contention, explicit_lock_contention + 2 G4 info-sufficiency pair):

| Classifier | Accuracy |
|------------|----------|
| Keyword-only baseline | **100.0%** (27/27) |
| Structural classifier | **74.1%** (20/27) |
| Random | 14.8% |
| Majority | 22.2% |

**Kill gates:**
- G1 (fixture validity): PASS — all fixtures labelled by construction
- G2 (Δ≥15pp vs keyword): **FAIL** — structural 74.1% vs keyword 100.0%, Δ = -25.9pp
- G3 (accuracy ≥80%): **FAIL** — 74.1% < 80%
- G4 (info-sufficiency witness): PASS — G4 pair correctly distinguished
- G5 (abstention ≤20%): **FAIL** — 22.2% (6/27) abstained

**Root cause:** Synthetic fixtures have non-overlapping keyword signatures by construction (each category has unique canonical keywords: `ShareLock` for FK, `duplicate key` for index, `tuple`/`ctid` for tuple, `advisory`/`pg_advisory` for advisory, `LOCK TABLE` for explicit). Keyword matching is therefore sufficient and optimal on these fixtures. The structural classifier's parser is too conservative, failing on 5/6 FK fixtures and 2/5 index fixtures.

**Negative controls violated:** Keyword-only baseline beats structural classifier, so the experiment cannot distinguish signal from noise.

**Classification:** The approach does not work on this fixture design. Do not rebuild this classifier. The finding is that synthetic fixture design critically determines whether keyword or structural classification wins — fixtures must force structural reasoning (overlapping keywords, ambiguity) to test structural classifiers meaningfully.

**Artifacts:** `EXPERIMENTS/147-postgres-deadlock-classification/{PROTOCOL.md,fixtures.jsonl,classifier.py,run.py,results.json,RESULT.md}`

---


## F148 — the deterministic accessibility repairer: the dominant class of real WCAG defects is an author-written string that is not on the page, so every repair of it is a fabrication

**Observed 2026-10-15**, session `2026-10-15-002-measure-whether-real-accessibility-defec`, experiment `E162` (`EXPERIMENTS/162-a11y-deterministic-repair/`).

**The claim:** a small deterministic program can eliminate ≥ 30% of real axe
AA-tagged violations **without inventing anything** — declared before any page
was fetched, with the 30% argued from the point where a third of by-hand work
stops being a linter and becomes a tool.

**The result:** claim falsified on mechanism, by its own kill gate. **0 of 125**
AA-tagged instances eliminated (0.0%). The same rule table permitted to invent
eliminated **99 (79.2%)** — and **104 of its 104 repairs were fabrications**
(every one put a user-facing string into the document that no author wrote).
27 real pages from three declared frames, fetched and sha256-pinned before any
repairer was written; axe-core 4.14.0 in jsdom as an independent oracle.

**The mechanism, measured with no repairer in the loop** (`why-not.js`, over the
216 arm-0 instances axe reported): of the **121** instances whose defect *is* a
missing name, **120 (99.2%) carry no author-written string anywhere on the node
axe itself reported** — 1 of 96 `link-name`, 0 of 13 `label`, 0 of 3
`role-img-alt`, 0 of 2 each `aria-dialog-name`, `frame-title`,
`aria-progressbar-name`. The information the rule asks for is not on the page.

**And the denominator most accessibility numbers use is mostly plumbing**
(`oracle-noise.js`): of the 125 WCAG-tagged instances, **92 (73.6%) are aimed at
anchors no user navigates to** — 90 of them a syntax highlighter's per-line
anchor on one documentation page, which alone carries 98 of 216 instances. A
tool that "fixed" those by inventing `link` as their name would improve the
score by 72 points of cosmetics.

**Three instrument defects the oracle caught, all kept:**

- `region` was not idempotent: 11 applications produced 13 `landmark-unique`
  and 11 `landmark-no-duplicate-main` violations — it manufactured the defects
  the rules it was aliased to check for. One declared condition fixed it.
- arm A's `alt=""` satisfies `image-alt` by declaring an image decorative and
  **creates** `role-img-alt` on the same element (3 introduced). Silencing one
  rule and breaking another is a failure.
- the first version of `why-not.js` counted the HTML `name` attribute as an
  accessible name, which made **94.8%** of `link-name` instances look readable —
  because 90 of them are `<a id="__codelineno-0-1" name="__codelineno-0-1">`,
  whose `name` is a JavaScript anchor. **HTML `name` does not compute an
  accessible name on `<a>`**, and an instrument that counts plumbing as content
  reports a mechanism as available when it is not.

**Classification:** the approach does not work; do not rebuild the deterministic
repairer **as written**. The table carried ten authored-text derivation paths
(`alt` from `title`/`figcaption`/wrapping `<label>`, link name from a nested
image's `alt`, button name from `value`, `lang` from `xml:lang`, document title
from the `h1`) and four structural repairs, and still eliminated nothing: the
class it would have to beat is the class whose answer is only knowable at
runtime. The line closes on mechanism whatever the demand turns out to be,
which is what the predeclared kill gate said would happen. This also explains,
rather than merely observes, why the 2026 tooling ecosystem is full of LLM
autofixers: the one thing a language model can do here is write the sentence
nobody wrote.

**Not closed, and named so the scope is not overread:** a wider repair table.
What is closed is on-document derivation on this population. Associating a link
with the code line beside it, or reading a `role="progressbar"`'s value out of
the script that sets it, is a different instrument — and the second is not
decidable without executing the page, which Amendment 2 ruled out.

**Ceiling — what this finding does not decide.** `fabrication` is a mechanical
proxy for "made the page worse", not a screen-reader measurement; jsdom performs
no layout, so `color-contrast` sits in `incomplete` and every number is about
DOM-decidable rules; 27 pages cannot estimate how broken the web is, and §4
shows why one of them would badly distort such an estimate. Demand was never
measured. **Not a prevalence claim.**

**Corroborates** F147 and the four experiments before it (a fixture that is
built for the classifier makes the classifier look unnecessary) — E162's
instrument is the opposite construction, an independent oracle on pages nobody
here wrote, and it still closed. **Consumes** the preflight and view-count lines'
shared pattern: the instrument is the deliverable that outlives the candidate.

**Artifacts:** `EXPERIMENTS/162-a11y-deterministic-repair/{PROTOCOL.md,PRIOR-ART.md,RESULT.md,analyze.js,gates.json,results-*.json,lib/,tests/}`
