<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# Failures — recorded finding F127

Continues [`FAILURES-findings-42.md`](FAILURES-findings-42.md), which held
F126. See [`FAILURES.md`](FAILURES.md) for the index. **Identifiers are
stable across all findings files.**

## F127 — a renumbering that resolved one collision created another, and an overwrite that recorded a decision deleted the decision before it

**Observed 2026-10-14**, session `2026-10-14-002`, while repairing a suite
that was already red when this session started. Both defects were inherited;
neither was caused by E141, and both were reproduced on the parent commit
before anything was changed.

### (1) D044 was overwritten, not edited

`f65940c4` ("Record D046: release preflight as public prototype with adapter
interface") is `10 insertions(+), 40 deletions(-)` on
`DECISIONS-PUBLISHING.md`. The 40 deleted lines are **D044 in full** — *"The
session's own record is not uncommitted work, and the claim says so"*, T-0055,
defect 21, F023. The file's own header and `DECISIONS.md`'s row both still
named `D044–D046`, and the section boundary that recovered D044 is
`old.index("## D045 —")` — which sits **before** D044 in that file, so a naive
"from D044 to D045" extraction returns nothing at all and the overwrite is
invisible to the obvious repair.

Three independent gates each caught a different half of it and none of them
caught the whole: `doc lint` said the header named an id the file does not
define, `test_decision_header` said the same, and
`test_identifier_enforcement` said `DECISIONS.md` lists `D044` and nothing
defines it. D044's body is recovered verbatim from `f65940c4^` and re-appended.

**An overwrite of a section header destroys the section.** The pattern that
caught it is the one already in the repository's own rules — the index, the
file header and the heading must all move together (D110's invariant) — and it
fired correctly. What the rules could not say is *where* the destroyed section
used to be.

### (2) The D046 → D048 renumbering resolved one collision by creating another

`1cc83e2a` ("Resolve D046 identifier collision: renumber DECISIONS-RECORDS D046
to D048") moved `DECISIONS-RECORDS.md`'s D046 to **D048**, which was already
defined in `DECISIONS-SCREENING-2.md` since 2026-10-05. It also left
`DECISIONS.md`'s row for `DECISIONS-RECORDS.md` naming the old id `D046`, and
left a **stale `D048` in that file's own header** — a leftover from T-0063,
when D048–D050 moved *verbatim* to `DECISIONS-SCREENING-2.md` and numbering was
deliberately preserved. So `D048` was in `DECISIONS-RECORDS.md` three times over
and the identifier check, which reads every source, reported the collision
correctly.

Repaired by the standing rule — **the later allocation yields.** `SCREENING-2`'s
D048 is from 2026-10-05 and is referenced from **ten** places across the record
(`FAILURES-findings-8.md`, `-9.md`, `STATE-next-actions-closed.md`,
`DECISIONS-SCREENING.md`, `DECISIONS-SCREENING-3.md`, `DECISIONS.md`'s row,
`EXPERIMENTS/012-candidate-harvest/README.md` and session summaries).
`DECISIONS-RECORDS.md`'s is from 2026-10-13, was a mechanical renumbering of an
existing id, and is referenced only inside its own file. It yields:
`DECISIONS-RECORDS.md`'s D048 is now **D113**, its header's stale `D048` is
gone, and `DECISIONS.md`'s row reads `D029, D032, D035, D041, D043, D047,
D113`.

**The rule this adds.** A renumbering is not finished when the two colliding
headings differ: it is finished when **every** source of the identifier agrees —
the index row, the file's own header, and every reference elsewhere. `1cc83e2a`
updated two of five and checked the free list rather than the used one.

### What was left red, and why

Adding two new `DECISIONS-SCREENING-*.md` files is itself a four-place edit, and
the suite names all four: `paths.MISSION_RECORDS` (the list a session obligation
reaches), `reconcile.IMPLICATIONS["decision"]` (the list that satisfies a
`decision` event), and the same two names in `tests/test_decision_files.py`,
which pins each against the other. **All four were updated here**, and the
repair is worth one sentence for the next session that splits a file: a new
`DECISIONS-` file is not one index row, it is two source lists in
`tools/originlib/` and the same two names again in the test that holds them to
each other.

Two failures remain, and **neither was caused by this session.** Both were
reproduced on the parent commit before anything was changed.

`test_no_tracked_link_leaves_the_repository` fails on **21 links in
`EXPERIMENTS/125-third-party-harness-preflight/readmes/`** — E125's captured
third-party READMEs, whose `/owner/repo/path` links are meaningful in *their*
tree and meaningless here. The same 21 files are the source of ~400 of the 427
remaining `doc lint` violations. Scoping a link gate away from vendored
third-party prose is defensible, but it is a change to what a gate enforces, it
was not this session's work, and **it is not done here on a red suite by a
session that did not own the debt.** It is named instead, with the exact
repair: a declared `exempt:` glob in `vendor/MANIFEST.md` for captured
`readmes/*.md`, honoured by `doclint.check_links` and by
`test_link_escape`, with a negative control that a link in an *authored*
document still fails.

`test_ci_annotations.test_the_tip_reports_nothing_and_annotates_nothing`
fails in the full discover run and passes when its module is run alone — a
test-ordering dependency, present at baseline, cause `untested`.

**Corroborates** F117 (two uncoordinated runs writing one identifier and
returning opposite results — the same failure at file scope rather than
experiment scope), F121 (a key that could not match what it was compared
against), F003/F004 (this repository's own record-keeping). **Consumes** the
`doc lint` and `test_identifier_enforcement` failures as named, dated
failures. **Ceiling:** the repair restored the gates, it did not explain why
`f65940c4` overwrote a section rather than appending one, and that cause is
`untested`.

---

## F128 — PostgreSQL deadlock classification: keyword baseline perfect on synthetic fixtures, structural classifier adds no value

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
