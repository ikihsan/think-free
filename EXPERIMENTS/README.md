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
| `016-prior-art-adjudication` | Do E012's 19 prior-art kills survive re-adjudication? | 3 of 12 adjudicable kills have no prior art on any corpus (F035) |
| `017-incumbent-artifact-type` | Is the screen's young-vocabulary population mostly documents? | **no**; 14 of 18 are executable code, by hand 13 of 18 (F037) |
| `018-runtime-signal-selection` | Can one annotation select metric/log/trace at runtime per path? | mechanism real, stock-OTel friction real, **feature gap, not a candidate** (F038) |
| `019-corpus-person-diversity` | How many people are in the need corpus, and can a shared need appear in it? | 1250 individuals; 79% of clauses share no content word; the recurrence instrument failed its own controls (F039, D051) |
| `020-copied-config-drift` | Does agent-configuration copied into a repository go stale? | **inconclusive** (0 attributable pairs); copying is instructed 687× and duplicated in 4.7% of content, which corrects F037's "it is copied" (F040) |
| `021-copied-artifact-serving` | Is copying a larger serving channel than installing? | **no**, 0.118×; the copy channel is the smaller one (F041) |
| `022-need-outcomes` | What becomes of a publicly stated unmet need? | 1401 statements, 812 answered (0.5796), 0 of 24 built it themselves; `served` later withdrawn (F042, F043) |
| `023-served-baseline` | Is E022's 38.5% `served` above ordinary comments in the same threads? | **no**, 0.395 vs 0.368; reader agreement κ = 0.923, so it is the population (F043) |
