<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Failures — recorded finding F051

Split out of [`FAILURES-findings-20.md`](FAILURES-findings-20.md), which held
F048–F050. See [`FAILURES.md`](FAILURES.md) for the index. **Identifiers are
stable across all findings files.**

## F051 — the unfilled departure requirement is not a property of the population, and no requirement in it recurs

**Date:** 2026-10-05. `EXPERIMENTS/031-unfilled-requirement/`, task T-0075.
Protocol declared before any account was read, amended four times. No network
fetch: the corpus is E030's captures.

### What was asked

E030 established that the departure-framing population is real (held-out
separation 0.64 vs 0.036) and falsified its recurrence ruler (F050). It never
read that population **for what it says about the gap rather than the move**.
E031 read it, with one reader question — *does this comment state a capability
something the author relies on cannot do?* — asked in identical bytes across
three arms of 72 comments each, and measured two things: whether accounts seeking
an alternative state a missing requirement more often than ordinary same-story
comments (H1), and whether any such requirement **recurs across independent
authors and independent departing artifacts** (H2).

### What was observed

**Departure accounts state a missing capability at nearly twice the base rate of
ordinary comments, and the seek stratum is indistinguishable from the move
stratum.**

| arm | n | yes | rate | CI95 |
|---|---|---|---|---|
| seek (names no successor) | 72 | 25 | **0.347** | [0.248, 0.462] |
| move (names a successor) | 72 | 25 | **0.347** | [0.248, 0.462] |
| ordinary (no framing) | 72 | 13 | **0.181** | [0.109, 0.285] |

B1's declared margin was 0.20; the observed seek − ordinary difference is
**0.1667** CI95 [0.0224, 0.3024] — real, interval excluding zero, and **below
the margin, so H1 does not survive**.

**The finding that decides the hypothesis the experiment was built on is the
seek-vs-move contrast, which was declared secondary and was not a gate: 0.347
against 0.347, difference exactly 0.0000 CI95 [−0.1523, 0.1523].** Accounts that
named a successor state a missing capability exactly as often as accounts that
did not. **"Unfilled" is not a property this population has.** The seek/move
split is a difference in framing phrase, not in whether anything was left
unfilled — which retires the premise E031 was built on, and does so by
measurement rather than by prior art or by a screen.

**And nothing recurs.** 100 candidate clause pairs — sharing ≥ 1 rare content
token, different authors, different departing artifacts, different stories —
gave **0 `same`** and 5 `unclear`. 100 length-matched random pairs from the same
arms gave **0 `same`** and 0 `unclear`. Difference **0.0000** CI95
[−0.0370, 0.0370].

**Length was checked, because E030's failure was length (F050).** Reweighting
the ordinary arm to seek's length distribution moves the difference from 0.1667
to **0.1698**. The difference is **not** a length artifact — the opposite of
F050's account of its own statistic.

### Why the zeroes are evidence, not a broken instrument

Four gates were declared and run specifically so that a `0` could be read as a
result rather than a failure:

| gate | rule | result |
|---|---|---|
| A3 | reader κ ≥ 0.6 on 96 double-read rows | **passes**, **κ = 0.7189**, raw agreement 0.875 |
| A4 | q1 `yes` ≤ 0.25 on 24 token-shuffled rows | **passes**, **0/24** both readers |
| A5 | successor question separates move from seek by ≥ 0.20 | **passes**, **0.486** (0.583 vs 0.097) |
| A6 | pair adjudicator: ≥ 16/20 synthetic positives `same`, ≤ 0.20 matched negatives | **passes**, **20/20** and **0/10** |

A6's ceiling is declared and stands (AMENDMENT-4 §2): its positive pairs are a
transform of the source clause sharing nearly all its content words, so A6 shows
the instrument can return a positive and rejects matched negatives — it does
**not** validate semantic paraphrase discrimination. The instrument's ability to
separate genuine recurrence from lexical resemblance is the very thing the
zeroes put in question, and a passing A6 does not settle it.

### What it rules out

The hypothesis E031 existed to test: that accounts seeking an alternative state a
requirement the departed artifact failed, **in a form that recurs across
independent authors and independent departing artifacts**. **A fourth
demand-side generator closes**, and this one closes on a **measured failure of
its own premise** rather than on prior art, on a screen, or on the trigger
vocabulary F043 showed is blind to outcomes.

It is also the sharpest evidence yet for the reading that has been assembling
since F033 and F039: the demand-side absence of task-level recurrence is a
**property of public accounts**, not an artefact of a harvest vocabulary. Two
structurally different populations — 1250 people each asking once (F039), and 919
departure accounts from people who had depended on the thing — both contain
missing capabilities at a measurable rate, and **neither contains a recurring
one**.

### Ceilings

- **63 clauses across three arms.** Two people needing the same capability twice
  would both have to land in a 25-clause arm sample. AMENDMENT-4 §"ceiling"
  declares this before the adjudication; nothing in the run removes it.
- **Reader independence is contextual, not prior.** Both readers were sub-agent
  contexts of one model family (AMENDMENT-1 §1). κ = 0.7189 is evidence the
  question is answerable from the text, not evidence two people would agree.
- **One corpus and one channel set.** GitHub issues, Reddit, support forums and
  the open web were declared unread by E030 and remain unread.
- **The 0.347 figure is a rate about what people say**, from a self-selected
  population of public technical argument, at 216 rows.
- **The move arm's q3 rate of 0.583** means the A5 separation is partly the
  stratum definition restated; it validates that the reader can read the
  distinction, not that the framing phrases perfectly partition it.

### The instrument defects this run found, and their relation to F050

1. **A declared linkage rule that could not fire** (AMENDMENT-3). Requiring two
   independent clauses to share ≥ 2 rare content tokens yields **4 candidate
   pairs against a chance expectation of 4.9** — unreachable whatever the world
   contained. This is the mirror image of F010 (a gate that could not fail) and
   the same family as F050 (a statistic that fired on coincidence): **a third
   distinct way a recurrence instrument is wrong about recurrence.**
2. **The unit change that fixed F050 broke C1.** Reader clauses are short — median
   11 words, range 5 to 26 — so a linkage rule tuned for 90-word comments does
   not transfer. Fixing the coincidence problem created the power problem.
3. **The replacement control is the one F043 showed this record had been
   missing**: not a permutation of the candidate set, which holds the selection
   fixed and therefore cannot say what the reader would answer about pairs
   nobody selected, but **100 reader-adjudicated random pairs** from the same arms
   through the same filters.
4. **Two checker defects on their first run**, both found by running the gate
   before trusting it: the byte-identity check included the per-row `ID:` line,
   which differs by arm by construction (AMENDMENT-1 §3), and the verbatim check
   rejected two correctly-copied clauses for a curly apostrophe and a double
   space (AMENDMENT-2, which declares the fold and records the **2 rows in 456**
   it rescued).
5. **An amendment of my own carried a wrong number.** AMENDMENT-3's first table
   counted pairs *within* arms (53 at ≥ 1, 2 at ≥ 2) while the generator pools
   them (100 at ≥ 1, 4 at ≥ 2). Corrected in place before any pair was
   adjudicated, with the correction visible in the file.

**Nothing in this run revives a candidate.** A closed lead that names a clause is
not a product, and F051's own ceilings are stated with the finding.
---

## F052 — the gate written to catch machinery dominating the work passed on machinery dominating the work, 4.8 times over

**Date:** 2026-10-06. `tests/test_allocation_measurement.py`,
`tools/measure_allocation.py`. Found while running the suite after F051, not by a
red CI run.

### What was asked

F031 measured this mission's allocation and recorded its complaint as a ratio:
**18,699 lines in `tools/` + `tests/` against 3,910 in `EXPERIMENTS/`**, a
proportion of **4.8 : 1**. The gate that carries F031's line finding into the
test suite asserted:

```python
ratio = data["lines"]["ratio_machinery_to_experiment"]
self.assertGreater(ratio, 1.0, "machinery should outweigh experiment code")
```

**At F031's own measured 4.8 : 1 this assertion passes.** The gate written to
detect machinery dominating the work was satisfied *by* machinery dominating the
work, nearly five times over. `test_the_original_assertion_would_have_passed_f031`
now asserts exactly that (`4.8 > 1.0`), so the blindness is recorded rather than
merely repaired.

### Why it stayed green through a fortnight

The floor at 1.0 is close to the live value, so the gate survived by being nearly
satisfied. It then turned red on 2026-10-06 **by this session doing the work the
mission exists to do**: E031 added **1,535 lines of experiment code and 4 lines
of machinery**, taking the ratio from 1.06 to **0.99**. So the gate punished an
experiment, and the punishment arrived as a red row on a suite whose subject is
allocation.

This is the third instance of a shape the same module already records twice above
it (F018, F019): **a gate that reads a property of the record rather than of the
artefact.** The per-day assertions in the same test were repaired for exactly
this reason — a finding about two named days made to depend on how much history
existed when re-derived — and the ratio assertion was left holding a global,
undated quantity.

### The repair, and its falsification

**A ceiling, not a floor, because F031's claim is about machinery dominating.**
F031 measured 4.8 : 1 and called it a complaint, so the ceiling is set to
**3.0 : 1** — below the measured complaint, so the gate fires *before* the
repository returns to the proportion F031 recorded. Direction is now the
mission's: **an experiment that adds code is not a regression**, which is the
opposite of what the old floor asserted.

`RatioCeilingTest` falsifies it in both directions: it fires at F031's own 4.8,
it passes on the 0.99 this session produced, and it asserts the old rule's
blindness. Six tests in the module, all green.

### What this rules out

**The claim that this repository's test suite has been monitoring its own
allocation is withdrawn as far as the line ratio is concerned.** F031's *finding*
stands — the proportion moved sharply and no artefact reported it — but the
artefact that claimed to hold it was satisfied by the condition it was written to
detect. A **passing gate here is not evidence about allocation**, and the
per-day commit shares in the same module remain the readable measurement.

**Ceilings.** The ratio counts **lines of Python in two directory trees**, which
F031 already stated is not a measure of value. It says nothing about
documentation, data, or whether the machinery is load-bearing — F031's own text
says the machinery is genuinely load-bearing and 22 defects were found by running
the record on itself. This finding repairs a gate that was measuring the wrong
thing in the wrong direction; it is **not** an argument that the machinery should
shrink, and the ceiling of 3.0 is a threshold chosen to sit below a recorded
complaint, not a target.

### The method point, which is D062's sibling

F051 found a declared linkage rule that **could not fire**. This is the mirror:
a declared gate that **could not fail**. Three distinct ways an instrument is
wrong about the thing it measures — F010 (cannot fail), F050 (fires on
coincidence), F051's rule (cannot fire) — and now a fourth (passes on the
condition it detects). All four were found by **running the gate or counting its
inputs before trusting its verdict**, which is the one practice this finding
recommends and the one the repository has now had to learn four times.
