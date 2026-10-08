<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Session history, part 3

What each older session changed, newest first. Continues
[`STATE-history-2.md`](STATE-history-2.md) and
[`STATE-history.md`](STATE-history.md), all three split off `STATE.md` at its
300-line cap — this one on 2026-10-06 (T-0081), when the reload point reached
322 lines after E039. Identifiers here are the same ones `STATE.md` uses.

**Why a third file rather than a fourth entry in the second:** the split is by
invariant — `STATE.md` is the reload point, these are the per-session accounts it
must not carry — and the cap has now been hit by `STATE.md` **eight** times,
each repair moving material to the file whose invariant owns it. The sessions
below are the ones that left `STATE.md`'s "What changed recently" on 2026-10-06;
they are not new, only relocated, and nothing in them was edited.

## Moved here on 2026-10-06 (T-0081), from the reload point

- **Session 053, VM 0944 (T-0063, F039, D051).** E019 counted the people in
  E012's need corpus: 1401 Hacker News comments carry **1250 distinct authors**,
  median one each, so F029's narrow-audience explanation is disproved and **no
  need-level recurrence is detectable inside the corpus**. F029 is not reversed —
  those 50 rows are dead either way. **What the corpus holds is 1250 named people
  who each wrote down what was missing**, a demand-side population this mission has
  never used. Full detail in
  [`EXPERIMENTS/019-corpus-person-diversity`](EXPERIMENTS/019-corpus-person-diversity/README.md).

- **Session 003, VM 0947 (T-0065, F040).** Asked whether the copy F037 inferred
  leaves a repository stale, which is the first question in five experiments about
  the world rather than about this repository's own instruments. **It does not
  copy: copying is documented in 687 places and duplicated in 4.7% of distinct
  file contents, with no cross-author overlap.** Drift is `inconclusive` rather
  than zero, and two of this session's own instruments were falsified against
  their own bytes. Details are in the In-flight entry in [`STATE.md`](STATE.md).

- **Sessions 050-051, VM 0944 (F029, F030, D049, E012).** The invention seat was
  **tested rather than filled**: 1401 harvested need statements, 50 drawn by a
  stated rule, **0 survived the screens** (38% prior art, 30% no mechanism, 24% not
  software, 8% needing hardware) against the prior generator's own 3-of-16. A need
  corpus cannot supply recurrence — term recurrence returns only function words —
  while an issue corpus counted **by repository** does (5805 issues, 28
  repositories). F030: one search query decides a prior-art verdict wrongly in both
  directions. Two costs recorded: a concurrent instance closed session 044's stream
  mid-session, so those commits predate its record; and a renumbering applied to a
  README while the rebase that renamed the directory was discarded left two indexed
  copies of one experiment that no gate could see, consolidated in `c38f1b4`.

- **Session 047, VM 0947 (T-0058, F028).** The flat adoption tail is vocabulary
  age, not niche: `build provenance` / `supply chain audit` carry long-lived or
  vendor-official outliers, so a stars-based "plausible adoption path" criterion
  is uninformative for a vocabulary younger than a few years — which is where
  every candidate lives. Census in
  [`EXPERIMENTS/011-niche-adoption-census`](EXPERIMENTS/011-niche-adoption-census/README.md).
  **Which axis replaces the criterion is an owner decision**, and is recorded as such.

- **Session 047, VM 0947 (T-0059). Twelve prior-art deaths are not twelve
  pieces of evidence.** Measuring installs rather than stars in five niches:
  three young vocabularies have 88–100% of their leading implementations with
  no measurable monthly install, and stars do not predict installs in any niche,
  mature included — which retracts the reading F028 was offered as support for.
  A crowded niche is the normal state of every niche. Two instrument defects
  were found by pre-flight and would each have flattered the hypothesis: an npm
  endpoint that answers in two different shapes, and an HTTP 200 that means
  *rate limited*. A third — a package name matching a repository it does not
  belong to, 25% of the time — would have under-counted the mature arm's leader
  by three orders of magnitude. F032.

## Moved here on 2026-10-08 (session 2026-10-08-013), from the reload point

- **Session 2026-10-08-003, VM 0944: fresh observation, docs-drift
  probe closed (E056, F087).** First falsifiable pass at a
  docs-drift audit candidate: five popular PyPI CLI packages
  (black, cookiecutter, httpie, mypy, pre-commit), `--help` over
  every subcommand versus `--flags` in the docs. Embedded help
  blocks match `--help` exactly (0 of 3 drift); every prose flag
  "missing" from `--help` was another tool's flag in an example.
  No candidate opened; E2's registry thread stayed closed.
- **Session 2026-10-08-001, VM 0947: registry thread closed; a day of
  uncommitted work landed.** E054 tested E2's registry premise on bytes:
  a deterministic 543-of-3800 stride sample of the artifact URLs E049's
  old uv.lock snapshots recorded all hashed today to their
  lockfile-recorded sha256 (0 mismatches, 0 fetch failures), so the
  retraction mechanism E050 found dead at the version level is dead at
  the byte level too (`no-artifact-drift`). T-0086 completed (E050
  verified, `no-registry-breakage`). Sessions 2026-10-07-016/017's
  uncommitted work landed: E051 (kill gates pass on 8/8 synthetic
  contradictions; 0 of 38 real abstracts — domain bound), E052, E053
  (synthetic-only; no public matched statement/ledger data exists),
  plus the F086 row, the D080 header repair, the SESSION-SUMMARY
  meta block. `doc lint` exits 0.
