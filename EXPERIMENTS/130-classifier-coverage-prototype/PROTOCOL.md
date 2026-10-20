<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->
# E130 — Classifier coverage prototype for view-count measurements

## Objective

Test whether an improved word-boundary anchored classifier achieves a declared coverage floor ≥60% of a representative pool, enabling the view-count principle's reopening condition #1: "A classifier that covers its population."

## Background

E113/F116 reclassified the view-count domain sweep as `untested` on a matched harvest,
finding that E107's large effect (δ=0.826) collapsed to δ=+0.075 (p=0.183) under matched harvest,
and the shared classifier labelled only 196 of 700 rows (28%), with 458 matching *neither*
vocabulary. The two defects were:

1. **Asymmetric harvest**: need arm and random arm drawn from different topics, both sorted
   by the outcome metric (need-8.6× random compared most-starred web frameworks against
   most-starred utility libraries).
2. **Unanchored substring classifier**: labels only ~28% of a representative population, with
   458 of 700 rows matching *neither* vocabulary because it matches unanchored substrings
   (`ai` inside `email`, `base` inside `database`). No experiment on this line had a
   declared coverage gate — a 28% screen was reported as a 100% measurement.

D083 identifies three conditions that would justify reopening the line, in order:
1. **A classifier that covers its population** — described as "a buildable engineering
   problem, not a research one."
2. **A coverage gate declared before the run** — the fraction of the population the
   labeler assigns at all, with a floor.
3. **A matched harvest as the default design**, not a control added after a positive.

This experiment addresses condition #1.

## Classification Rules

### Need patterns (word-boundary anchored)

| Pattern | Purpose |
|---|---|
| `\bhow\b` | How-do-I questions |
| `\bwhat\b` | What-is/what-should-I questions |
| `\bwhy\b` | Why-questions |
| `\bhow (do|can|should|would|is|are)\b` | how-do-I / how-can-I questions |
| `\bwhat (is|are|should|would|causes?|makes?)\b` | what-is questions |
| `\bwhy (is|are|do|does|did|can|won)\b` | why-questions |
| `\bhelp\b` | Help requests |
| `\bissue\b` | Issue reports |
| `\bproblem\b` | Problem reports |
| `\berror\b` | Error reports |
| `\bfailure\b` | Failure reports |
| `\bnot working\b` | Not working reports |
| `\bbroken\b` | Broken reports |
| `\brecommend\b` | Recommendation requests |
| `\bsuggestion\b` | Suggestion requests |
| `\badvice\b` | Advice requests |
| `\bwhich\b` | Which questions |
| `\bwhere\b` | Where questions |
| `\bstuck\b` | Stuck reports |
| `\blost\b` | Lost reports |
| `\bwondering\b` | Wondering |
| `\bshould I\b` | Should-I questions |

### Non-need patterns (word-boundary anchored)

| Pattern | Purpose |
|---|---|
| `\bIC\b` | Integrated Circuit references |
| `show.*(off|me)` | Show-off content |
| `my (new|first|latest) (setup|build|project|purchase)` | New project sharing |
| `just (got|bought|picked up|received)` | Purchase announcements |
| `welcome to` | Welcome messages |
| `thank(s| you)` | Thank-you messages |
| `image(s)?\s*(only|thread)` | Image-only threads |
| `picture(s)?\s*(only|thread|uno)` | Picture-only threads |
| `introductions?` | User introductions |
| ````` | Code block fences |
| `code block` | Code block references |
| `announcement` | Announcements |
| `release note` | Release notes |

## Gates

| Gate | Criterion | Pass condition |
|---|---|---|
| G1 | Classification validity | Single-rater, well-defined rules (satisfied by design) |
| G2 | Need prevalence | ≥5% of sampled threads are need topics |
| G3 | Coverage floor | Classified fraction ≥ declared floor (default: ≥60%) |
| G4 | Cross-platform signal | ≥2 of 3 sampled threads classified as need have tool-named replies |

### Falsification

The experiment fails if:
- G2: need prevalence < 5%
- G3: classified fraction < coverage floor (60%)
- G4: 0 of 3 sampled need threads have replies naming a tool/artifact

## Deliverables

- `raw/thread_data.jsonl` — sampled thread data (need + random arms from matched harvest)
- `results.json` — aggregated results with gate assessment and coverage measurement
- `README.md` — experiment summary, coverage rate, and gate outcomes
- `coverage_report.txt` — detailed coverage analysis

## Reopening the view-count line

If G3 passes (coverage ≥ 60% floor), the view-count line can potentially be reopened
with condition #2 (declared coverage gate) and condition #3 (matched harvest design).
If G3 fails, the classifier coverage constraint is confirmed and a different fresh
observation must be pursued.