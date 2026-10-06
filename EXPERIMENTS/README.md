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
| `024-kill-reason-causes` | What actually killed the candidates? | prior art is 10 of 18 eligible rows, a one-row margin over a population of 20, and 7 died of something else (F044) |
| `025-need-staters-builderhood` | Did the 0-of-24 build arm hide a disclosure channel? | **no** — rate 0.2224 of need-staters have shipped something, against 0.278 for ordinary commenters (F045) |
| `026-unserved-need-structure` | Is the corpus's 589-statement unserved tail structured? | **no**; diffuse in length (0.948) and trigger (p ≈ 0.06), and B2's firing rests on 9 rows (F046) |
| `027-cause-of-death-reread` | Were F029's 31 clause-based kills measured on a regex rather than a comment? | 6 of 15 `vague` kills are not vague, read by two blind readers; the six-label kappa fails but F029's 0-of-50 stands anyway (F047) |
| `028-incumbent-fit` | Does the incumbent a prior-art screen named do what the clause asked? | **`not_evaluated`** — the declared positive control failed, and use is not fit (F048) |
| `029-need-build-match` | Do the people who stated a need go on to ship that need? | 167 of 241 shipped **before** the need; the reader arm's verdict is in [`029-need-build-match/README.md`](029-need-build-match/README.md) (F049) |
| `030-departure-recurrence` | Do departure accounts supply a recurring unmet clause? | the population is real (0.64 vs 0.036) and the ruler was falsified: the statistic read length and coincidence (F050) |
| `031-unfilled-requirement` | Do accounts seeking an alternative state an unfilled requirement, and does it recur across independent authors? | **no, twice** — 0.347 vs 0.181 against ordinary comments but below the declared margin, the seek and move strata are **identical at 0.347**, and 0 of 100 clause pairs recur with every instrument gate passing (F051) |
| `032-venue-recurrence` | Is the recurrence zero a fact about public conversation or about Hacker News? | the zero **is not Hacker News's** length, unit, population or vocabulary selection; 0 of 32 candidate pairs and 0 of 60 control pairs, κ = 0.8344 — a venue-agnostic **bound of 0.0223** pooled with E031 (F053, F054) |
| `033-question-recurrence` | Is that 0.0223 bound a fact about the world or a fact about the draw? | **the bound is refuted: 0.0540 CI95 [0.0416, 0.0698]** over 1000 questions, read from Stack Exchange's own duplicate closure. The zeros were a **stratum effect** — `sort=votes` draws the tertile where recurrence is **4.5× rarer**, and the top 60 by score contains 0. The run's second claim — that repeats go unanswered — was **withdrawn as mechanical** (zero of 54 has an accepted answer). The edge arm failed (6 of 24), so the canonical is treated as unreadable (F055) |
| `037-line-staging` | Can a program select one change by line number, and what does it cost? | **interface gap confirmed** — mechanism available, interface absent; `stg` 6/6 vs the incumbent's 4/6 (F060, D068) |
| `021-need-statement-response` | What happened to the 1401 public need statements — did their own threads answer them? | **kill gate fired** (1.235× vs a bar of 1.5); 0 of 1391 drew a novel-host link, 1 of 794 requesters returned (F060-F063, D068) |
| `042-stg-end-to-end` | Does stg give an agent a practical advantage over the strongest baselines? | **stg 6/6 correct, 0 silent; shell baseline matches; filterdiff 2/6; naive 2/6; mechanism not differentiator** |
