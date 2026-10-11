<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E092 result — appliance-fault diagnosis is a real population, and the general assistant already serves it

Session `2026-10-11-004`. Protocol `PROTOCOL.md`;
screening record `screening.tsv`; G0 gate `g0_probes.py`
(`g0_probes.json`); attempts `attempts.py`
(`attempts.jsonl`, all `attempt_first=true`); grades
`grades.py` (`grades.jsonl`); arithmetic `score.py`
(`results.json`).

This is the test E091 (`../091-anova-answerability/`,
F114, D103) named in its §6: is appliance-fault
diagnosis a general need outside one vendor's own
forum, with an unserved answerable-class population a
program could serve?

## 1. Gates

| gate | result |
|---|---|
| **G0 discrimination** | **PASS** — 10/10 construction-labelled answerable probes answered, 10/10 unanswerable declined (per-model specs, vendor records, physical inspections), labels known by construction |
| **A1 population** | **PASS** — 707 unanswered `appliances` questions fetched (8 requests, all HTTP 200, reconciled against the API's own `answer_count` for the thread fetch: 140 of 140) |
| **G1 population** | **PASS** — 66 of the top 150 by `view_count` are diagnosis-shaped (44.0%, Wilson CI95 [36.0%, 52.3%]) against a declared ≥ 40 |
| **K1 served share** (answerable class) | **PASS (line closes)** — 30/37 = 0.8108, Wilson CI95 [0.6580, 0.9052]; the lower bound 0.6580 clears the declared 0.50 |
| **K2 Arm A** | **0 of 40** remedies is a self-contained program |

## 2. What the population is

Of the 150 highest-arrival unanswered appliance
questions on a multi-vendor knowledge venue:

- **66 (44.0%)** are diagnosis-shaped — a specific
  device exhibits a symptom whose cause the asker does
  not know. The rest are installation, wiring, purchase,
  code, and repair-how-to questions with known causes.
- Of the 66, **61 are answerable-class (92.4%), 2
  repair, 3 vendor** — against E091's Anova forum at
  7/20 answerable (35%). The composition difference is
  itself decisive: Fisher one-tailed **p = 4.7e-07**.
- The sample (40 highest-view diagnosis rows) holds 37
  answerable, 2 vendor, 1 repair.

## 3. The measurement

The general assistant served **32 of 40 = 0.8000**
overall (Wilson CI95 [0.6524, 0.8950]) and **30 of 37
= 0.8108** of the answerable class. Against the record:

| contrast | table | one-tailed p |
|---|---|---|
| E092 served share vs E091 Anova served share | 32/40 vs 5/20 | 0.000055 |
| E092 answerable class vs E091 Anova answerable class | 30/37 vs 4/7 | 0.1819 |
| E092 answerable class vs E062's 17/20 (non-software Stack Exchange, F096) | 30/37 vs 17/20 | 0.7644 |

The overall shares differ by 0.55; the answerable-class
shares do not differ significantly in either comparison.
**The venue difference is composition, not community** —
which is D103's thesis, now measured directly in a
second venue with the same instrument: where a venue's
curation keeps vendor-bound rows out (92% answerable
here), the served share rises to the 0.81 that E062
measured on knowledge venues; where it does not (Anova,
35% answerable), the overall share falls to 0.25.

## 4. The eight misses

Seven answerable-class rows were missed, and the miss
shape matters: in every one the attempt named a
textbook cause and the thread's resolution was a
less-common one — chloramine attacking the molded
reservoir (not sediment); defrost heaters stuck on (not
condenser coils); a de-rated breaker (not the
compressor circuit); a frozen coil from low refrigerant
(not the start relay); a control-board fault (not
crossed wiring); deteriorated element insulation
shorting when hot (not the breaker); water under the
drum being normal with a rubber-lining smell (not a
drain failure). These are wrong-first-hypothesis
misses, not refusals — the same shape as E091's two
answerable-class failures. One vendor row was missed
(vaporization/pressure, the thread's central mechanism
that the attempt's minority causes did not cover).

## 5. Instrumentation notes

- The pool's first fetch run crashed on a variable-name
  bug after 8 requests, losing its log; the second run
  re-fetched the pool and its 8 requests are the ones
  in `fetch-log.jsonl`. The wasted 8 requests are
  recorded here rather than in the log, because the log
  itself was the casualty.
- The thread fetch's first run took one 100-item page
  and truncated 40 of 140 answers; the paginated re-run
  fetched all 140 and reconciled them against the
  declared `answer_count` (0 mismatches). Both runs'
  requests are in `thread-fetch-log.jsonl`.
- Fisher exact is computed as the exact hypergeometric
  tail in integer arithmetic (`math.comb`), cross-checked
  against exhaustive enumeration on 155 random small
  tables (F114's defect class: E091's first Fisher tail
  summed from the wrong term). The live tables (60 and
  86 cells) are past enumeration's reach; the check is
  on the implementation, not the live numbers.
- One reader, one grader, one model family for both
  attempt and grade — the E062/E091 shape. Attempts were
  committed before any thread content was read; the
  screening classified shape and remedy class before any
  answer was read.

## 6. Decision

**The appliance-fault-diagnosis line closes for good,
per the protocol's own K1 branch.** The population is
real, large, and reachable — 44% of the highest-arrival
unanswered appliance questions on a multi-vendor venue
are diagnosis-shaped, 92% of those are answerable-class,
and the arrival instrument (`view_count`) works on the
venue — but the strongest accessible alternative, a free
general assistant, serves the answerable class at 0.81
(lower CI95 bound 0.66), statistically indistinguishable
from E062's 0.85 on knowledge venues, and **not one of
the 40 sampled resolutions is a self-contained
program**. The residue is a wrong-first-hypothesis rate
(7 of 37), not an unserved population, and no program
in the population could do what the assistant does not.

D103's reopening condition is therefore answered in the
negative on both of its limbs: the answerable-class
unserved share does not clear the gate, and the
population contains no program-shaped remedy. The
four-venue closure of fault-code tooling (E079, E082,
E083, E084) and the two-venue closure of diagnosis
itself (E091, E092) now rest on the same finding: the
need is real, the general assistant serves it, and the
composition of the venue — not the community — decides
what share of its arrivals any tool could add to.

**What this does not establish.** One venue, one reader,
40 rows; the attempt arm is the same model family as the
grader; the 0.19 miss rate on the answerable class is a
real limitation (the misses are wrong-first-hypothesis,
and a second reader might grade some of the 32 served
rows differently); and the composition contrast, while
decisive (p = 4.7e-07), is one reader's classification
in both venues.
