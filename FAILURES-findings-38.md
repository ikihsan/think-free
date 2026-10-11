<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# Findings, part 38

Split out of [`FAILURES-findings-37.md`](FAILURES-findings-37.md)
at the 300-line cap: F115, the E092 result, is the
newest finding and the only one in this file.

## F115 — Appliance-fault diagnosis is a real, reachable population, and a free general assistant already serves the answerable class at 0.81: the diagnosis line closes (E092)

**The test E091 named.** E091 (F114, D103) left one
class open — diagnosis of a specific device from a
described symptom — and D103's reopening condition
required a venue whose ownership mix is reported, whose
answerable-class unserved share clears the gate, and whose
population contains a program-shaped remedy. E092 ran that
test on Home Improvement Stack Exchange (`diy`, tag
`appliances`), a multi-vendor venue exposing `view_count`
through the same API E062 and E079 used.

**The population is real.** 707 unanswered `appliances`
questions were fetched; of the 150 highest-arrival, **66
(44.0%)** are diagnosis-shaped (a specific device, a
symptom, an unknown cause), and of those 66, **61 are
answerable-class (92.4%)**, 2 repair, 3 vendor — against
E091's Anova forum at 7/20 answerable (35%). The
composition difference is decisive: Fisher one-tailed
p = 4.7e-07. G0 discrimination passed first (10/10
answerable probes answered, 10/10 unanswerable declined,
labels known by construction); attempts were committed
before any thread content was read.

**The answerable class is served.** A free general
assistant served 30 of 37 answerable rows = **0.8108**,
Wilson CI95 [0.6580, 0.9052] — the declared K1 lower
bound (0.50) is cleared, and the share is statistically
indistinguishable from E062's 17/20 on non-software
Stack Exchange (p = 0.764) and from E091's Anova
answerable class, 4/7 (p = 0.182). The overall shares
differ (32/40 vs 5/20, p = 0.000055) because the
compositions differ — D103's thesis, now measured
directly in a second venue with the same instrument.

**Arm A is 0 of 40.** Not one sampled resolution is a
self-contained program: they are parts, wiring, cleaning
cycles, pressure tests, and service calls. The residue
is a wrong-first-hypothesis rate (7 of 37 answerable
rows missed — e.g. chloramine attacking the molded
reservoir, defrost heaters stuck on, a de-rated breaker,
a frozen coil from low refrigerant), not an unserved
population.

**Decision: the line closes for good** (D104), per the
protocol's own K1 branch. The need is real, large, and
reachable; the strongest accessible alternative serves
it; no program-shaped remedy exists in the population.

**Record correction carried in this finding.** E091's
`RESULT.md` §3 and F114 describe E062's 17/20 population
as "Steam". That is false: E062's `AMENDMENT-1.md`
retired the Steam arm before any row was fetched (Valve's
per-game feature-request boards no longer exist; the probe
is `EXPERIMENTS/062-nonsw-need-shape/raw/steam-probe.json`),
and the 17/20 was measured on six non-software Stack
Exchange sites — the top-20 by view_count being 12 `diy`,
4 `woodworking`, 2 `cooking`, 1 `gardening`, 1 `bicycles`
(`raw/answerability-top20.tsv`). The 0.85 is a number
about a mostly-physical-domain **knowledge** population,
not a software population. E091's own composition finding
stands on its own 20 rows; the contrast it drew is
corrected in place in F114 and E091's `RESULT.md`.

**Instrumentation.** The pool's first fetch crashed on a
variable-name bug after 8 requests (its log was lost with
it; the second run's 8 requests are the committed
`fetch-log.jsonl`); the thread fetch's first run truncated
40 of 140 answers on one 100-item page, repaired by
pagination and reconciled against the API's own
`answer_count` (140 of 140, 0 mismatches). Fisher exact
is the exact hypergeometric tail in integer arithmetic,
cross-checked against exhaustive enumeration on 155 random
small tables (F114's defect class).

Evidence: `EXPERIMENTS/092-appliance-diagnosis/`
(`RESULT.md`, `PROTOCOL.md`, `screening.tsv`, `g0_probes.py`,
`attempts.py`, `grades.py`, `score.py`, `results.json`).
