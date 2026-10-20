<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E177 RESULT — the assistant is at 0.867 on self-contained questions and 0.400 on evidence-gated ones, and every closure in this record measured a mixture

**Date:** 2026-10-17. **Protocol:** [`PROTOCOL.md`](PROTOCOL.md), with
[`AMENDMENT-1`](AMENDMENT-1.md) through
[`AMENDMENT-6`](AMENDMENT-6.md) declared and committed before the runs that
adopt them. **Run:** `python3 score.py`; raw inputs, readers' outputs and the
committed ordering are in `labels.json`, `arms.json`, `ans/`,
`score/verdicts.jsonl`, `census.json`, `result.json`.

## The result

| | n | reached | rate | Wilson 95% |
|---|---|---|---|---|
| **SELF** — resolution reachable from the question's own text | 30 | 26 | **0.8667** | [0.7032, 0.9469] |
| **EVID** — resolution needs a fact or artefact the question does not contain | 30 | 12 | **0.4000** | [0.2459, 0.5768] |

**gap +0.4667, Fisher exact two-sided p = 0.000368.** G3's declared bar was
`gap >= 0.25` **and** `p < 0.05`. **G3 fired.**

Controls, all on the same run: **G0a** 60 of 60 substantive answers, 0 refusals
in either arm · **G0b** 5 of 5 real positives recovered · **G0c** 0 of 5 real
non-equivalents accepted · **G0d** arms disjoint, 0 overlap.

## What it decides

**1. D107's standing constraint is supported, on this population.** The
constraint said a candidate must target a task whose answer is not computable
from the text plus the facts, because the missing input is *evidence*. That
constraint had governed candidate selection for five days on an inference and
never been measured. It now has a number: the same assistant, the same key, the
same venue, differing only in whether the question carried its own evidence,
**0.8667 against 0.4000**.

**2. The six service closures measured a mixture, and every one of them reported
the mixture.**

| experiment | population | reported share | what the mixture was |
|---|---|---|---|
| E062 | non-software SE needs | 17/20 = 0.85 | not stratified |
| E091 | Anova | 5/20 = 0.25 | stratified by answerability, not evidence |
| E092 | Home Improvement SE | 30/37 = 0.81 | not stratified |
| E126 | SO program-shaped residue | 0.6750 | stratified by question shape |
| E143 | Cross Validated | 20/20 = 1.0 | not stratified |
| E115 | CFR applicability | 14/14 | by construction decidable |

**0.4000 is the lowest rate a free general assistant has scored on a real
question population in this record**, and the SELF arm's 0.8667 sits inside the
0.6750–1.0 band all six closures reported. Both numbers are consistent with
them: a pool that is mostly SELF lands high, and the low tail was always there,
unmeasured, inside every one of those pools.

**3. The class is large.** CLF labelled the **100 highest-`view_count` rows that
carry a key answer**, out of 145 in E175's committed 200-row draw:
**SELF 52, EVID 46, UNCLEAR 2.** So **0.46 of high-arrival answered questions
have a resolution the question itself does not contain**, and on that class the
assistant reaches 0.40. Composition of the 46:

| kind | n | meaning |
|---|---|---|
| `upstream_source` | 19 | the resolution is in a changelog, release note, spec or upstream thread |
| `other` | 8 | a fact from another product, a framework's internal behaviour |
| `version` | 7 | a version number or what changed between versions |
| `configuration` | 6 | a config value, a build flag, a code path |
| `data_value` | 4 | a value from a system the asker had and did not report |
| `platform` | 2 | OS, libc, runtime |

Within the 30 EVID rows, reached rows are spread across kinds in proportion
(`upstream_source` 6, `other` 3, `version` 2, `configuration` 1) — **no single
kind carries the failure.** So there is no mechanical checker inside EVID to
build, which is E115's K4 finding in a second population.

**4. The failure is confident, not cautious.** **0 of 30 EVID questions got a
refusal or a stub, against 0 of 30 SELF** — identical. The assistant does not
notice that the evidence is missing; it answers anyway and is wrong more than
half the time. AMENDMENT-3 declared abstention-by-arm to be reported rather
than gated; this is the report, and it is the more useful half. A population
where the assistant is confidently wrong 60% of the time is a *worse* place to
send a person than one where it abstains, and it is the population this record
has never once measured.

## The census (automatic, all 145 keyed rows)

**Evidence gain** — the share of the key answer's content tokens absent from the
question: **median 0.7959**, and **137 of 145 = 0.9448, CI95 [0.8949, 0.9718]**
at or above 0.50.

This is descriptive and **is not the arm definition**; a reasoning answer can
legitimately use new vocabulary. It is reported because it costs no reader time
and because it is the same shape as E169's containment result: the answer's
vocabulary is largely not the question's. Where E177 goes past it is the
`SELF`/`EVID` split, which is a reader's judgement about the resolution rather
than a token count — and the census is the check on that judgement, which is why
it is reported whether or not G3 fires.

## What this does not say

- **n = 30 per arm, chosen for the gap.** Each arm's own rate carries roughly
  ±0.15. **No claim may be made about either arm's absolute level from this
  run.** The SELF arm's 0.8667 is consistent with six prior rates in the
  0.6750–1.0 band; it is not a new measurement of that level.
- **One venue, one question shape, one platform.** High-arrival *answered*
  Stack Overflow questions, and nothing else.
- **The draw is reused from E175**, so every rate here is **conditional**, not a
  prevalence estimate on a fresh pool. A fresh draw is required for a prevalence
  claim and is the named next action.
- **The key is the top-voted answer, not the accepted answer** (AMENDMENT-2:
  this pool carries an accepted answer on 6 rows). So the claim is about
  reaching *the community's best answer*, not about resolving the question. A
  top-voted answer can be "what I would do" rather than "what fixed it".
- **All three readers are the same model family.** Three blinded passes remove
  the *ordering* bias that contaminated E170 and E174's arms; they do not make
  three independent readers, and MISSION.md already says agents are not
  independent human validation.
- **CLF is one reader with no second coder.** It named 8 rows in batch `a` and 6
  in batch `b` that it would not defend without a second reader. No control
  except G0d would notice a systematic mislabel, and G0d only checks disjointness.

## Instrument defects this run found, in the order they happened

Four before any measurement, one during:

1. `filter=withbody` returns tags as strings, the default filter as objects
   (AMENDMENT-1).
2. `questions/{ids}/answers` caps at 100 answers **across the whole request**,
   so 25-id chunks silently truncated; and this pool has an accepted answer on
   6 of 145 rows, so the key was redefined to the top-voted answer (AMENDMENT-2).
3. One JSON object per line loses the question to a 2,000-character line cap
   whenever the answer carries a code block — **18 of 50 rows in CLF batch `a`**,
   whose labels were discarded, not merged (AMENDMENT-4).
4. One unescaped quote in 60 treatment answers (AMENDMENT-5).
5. **The Fisher tail summed ratios instead of probabilities** and returned 1.0
   for every table, against a gap of 0.4667 (AMENDMENT-6).

Defects 3 and 5 are the same shape as E091/F114 and F063: **a pipeline whose
only job was to move bytes or arithmetic, failing at the byte or the sum.** The
Fisher one is the record's third hand-written tail found wrong and the second
found only by disbelieving its own output — because **every declared control in
this protocol passed while the p-value was wrong by a factor of 2,700.**

## Named next action

**E178 — what is the missing evidence, and can it be fetched before the person
asks?** This result names a population (0.46 of high-arrival answered
questions), a rate (0.4000), and a composition. It does not name a tool, and
PROTOCOL.md's G5 says so in advance.

The question E178 has to answer is whether the missing evidence is *obtainable
from something the asker already has*. The kinds split that: `version`,
`upstream_source` and `configuration` (32 of 46) are recoverable from the
project's own published history, and E169–E175 spent four experiments on exactly
that with a population of 7% and a reachable share of 0. `data_value` and
`platform` (6 of 46) are recoverable only from the asker's own environment.

**Do not run:** E176 as originally written (a classification of the same rows by
the same instrument — the third such in a row, and it cannot decide anything the
arms have now decided), a replication of E170's global arm, another view-count
domain, or a fresh draw of the same comparison before the composition of the 46
is examined (the reused draw means the 46's composition, not its rate, is the
number a fresh draw would add).
---

## Addendum (post-hoc, exploratory — not a finding and not a gate)

Run **after** `score.py` and after all verdicts existed, on committed data, with a
reader that could see both the labels and the verdicts. Everything here is
`speculative`, is contaminated by that ordering, and **must not be read as a
measurement**. It is recorded because it changed what the next experiment should
ask, and because it found defects in this experiment's own labelling.

**What it says about E178's framing.** E178's declared buckets are
`publishable` / `asker_only` / `third_party`. On this reader's guesses over the
30 EVID rows, **`publishable` drew 0 of 30** — not one resolution needed a fact
the project already publishes. Misses skewed `asker_only` (11 of 18) against
reaches (4 of 12); reaches skewed `third_party` (8 of 12).

If that holds, it says the missing evidence is **not in changelogs and release
notes at all**, which would remove the last route the version-pinned line had
available and would leave the class as *values the asker holds and did not
report*. That is a materially different candidate from "a published artefact the
tool can fetch", and it is the reason E178's framing is worth keeping. **It is
one reader's guess on 30 rows, made knowing which rows were missed. It is a lead,
not a count.**

**What it says about CLF.** The same pass flagged **7 of the 30 EVID rows** as
labels this reader would not defend:

| qid | the objection |
|---|---|
| 79686551 | the treatment contradicted the question rather than lacking evidence — a wrong answer, not an absent-evidence failure |
| 79385315 | the resolution is "open upstream issue, no fix yet" — no fact exists to withhold, so the gate is untestable on it |
| 79600161 | `missing_evidence` is a mirror URL — resource-finding, not evidence-gating |
| 79791886 | the label names a plausible but wrong fact (`RAND_MAX` cannot establish modulo bias; glibc's Mersenne `RAND_MAX` makes it impossible) |
| 79818015, 79335513, 79843062 | the label may have picked a symptom-compatible cause rather than the load-bearing one |
| 79665976 | labelled EVID and reached; agreement appears to contradict the label |

So **CLF's precision on this population is somewhere around 0.77–0.87 by an
audit that saw the answers, not 1.0.** The headline is **not** recomputed with
those rows removed: choosing which labels to drop *after* seeing which arms
scored is the fitting this record has been burned by twice, and it is the same
move as declaring a kill's scope after the arms. **This is a ceiling on G3, not
a correction to it** — and it is a ceiling on the *arms*, so the honest statement
is that the comparison is between two classes defined by a single reader whose
precision on 30 rows is not established.

**What it says about mechanism.** One pattern accounts for the whole split: in
**18 of 18 misses the missing fact was load-bearing** — it selected among several
causes compatible with the symptoms the asker posted, so the treatment's
alternative was equally consistent with the text. In **8 of 12 reaches the fix is
the same with or without the missing fact.** If that is the mechanism, then the
class is not "questions missing a fact" but **questions whose posted symptoms
underdetermine the cause**, and the missing evidence is the thing that
*discriminates* between hypotheses. That is a sharper target than E178's three
buckets, and it is what the next experiment should be written against.

**One more defect, in the gate rather than in the experiment.** Two `origin doc
lint` runs overlapped once while this file's addendum was being written. The
second run reported **21 violations on files it had not changed** — 18
`README.md` files from the view-count sweep whose timestamps were days old, four
`.py` files at 301–380 lines, and `DECISIONS-PYTESTIVE-SUMMARY.md` as missing an
`origin-meta` block **while that block was the first line of the file**. A single
run on the same bytes reported `doc lint: OK`.

`observed`: the concurrent run reported the violations; the clean run did not.
`inferred`, not confirmed: two processes of the same gate reading and writing
shared classification state. **Not reproduced and not diagnosed here** — it was
found because the clean run disagreed with the noisy one and the reported files
were days old, which is the same instinct that caught `AMENDMENT-6`.

Recorded because the next session will run this gate, and because the correct
response to a red `doc lint` whose named files are days old is to look for a
concurrent run before editing any of them.
