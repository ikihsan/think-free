# Experiments

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-03
-->

Each experiment must include a hypothesis and falsification criterion, implementation, explicit baselines, deterministic reproduction command where possible, raw results, environment details, and limits. Synthetic cases must be labeled synthetic. Failed experiments are retained.

## Inventory

| # | Question | Verdict |
|---|---|---|
| `000-capabilities` | What can this machine do? | recorded, re-probed per VM by `origin doctor` |
| `001-photo-baseline` | Does the photo-migration motivating example reproduce? | **kill gate met** (F001) |
| `002-a1-masking` | Does A1's advantage survive a fieldwork-cost budget? | **gate met with caveats** (F006) |
| `003-information-sufficiency` | Is the input set sufficient for the claimed mechanisms? | W1/W3 survive, W2 does not (F007) |
| `004-knitting-stage-a` | Is the local knitting planner valid? | valid 9/9, suboptimal on 1 case |
| `005-knitting-bounded-search` | Is whole-neighbourhood search exact? | exact 115/115 (F024) |
| `006-ventilation-measurement-design` | Does adaptive selection beat a prescribed protocol? | **kill gate not met** (F008) |
| `007-build-timestamps` | How many wheels carry non-normalised timestamps? | 0.965, but the gate was vacuous (F010) |
| `008-build-timestamp-attribution` | Are timestamps the whole cause? | `SOURCE_DATE_EPOCH` gives bit-identical builds (F012) |
| `009-lockfile-drift-snapshot` | Are lockfiles weak witnesses over time? | side A banked; **zero drift at ~21h**, a fast-drift null only |
| `010-annotation-rendering` | Does GitHub file an annotation on the emitted `file=`? | yes, `observed` (F021 corrected it) |
| `011-niche-adoption-census` | Is the flat adoption tail vocabulary age or niche? | vocabulary age, on stars (F028) |
| `012-candidate-harvest` | Does a live need corpus yield a surviving candidate? | 1401 harvested, **0 of 50** survived (F029) |
| `013-prior-art-predicts-adoption` | Does a crowded niche mean a solved one? | **no**; stars do not predict installs (F032) |
| `014-repository-signal-filter` | Does E012's strongest cluster survive the filter it was promised? | **no**; every query collapses >100x (F033) |
| `015-incumbent-serving` | Does "prior art exists" mean the need is served? | **inconclusive**; the premise holds in mature vocabularies and fails in young ones (F034) |
| `016-prior-art-adjudication` | Is "a tool already serves this" a screen that can be shown to work? | **yes, and it is the weakest verdict the mission owns**: 6/6 controls recovered, 3 of 12 kills have no prior art, and the open web carries a third of what code indices miss (F035, F036, D050) |
