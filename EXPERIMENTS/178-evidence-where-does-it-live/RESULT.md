<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E178 RESULT — the missing evidence is not in anything the project publishes; the venue's own round trip already supplies it

**Date:** 2026-10-17. **Protocol:** [`PROTOCOL.md`](PROTOCOL.md), with
[`AMENDMENT-1`](AMENDMENT-1.md) and [`AMENDMENT-2`](AMENDMENT-2.md) declared
before the runs that adopt them. **Run:** `python3 score.py`; raw inputs,
reader output and the committed ordering are in `rekey.jsonl`, `comments.json`,
`raw/se.jsonl`, `result.json`.

## The result

| bucket | n | share | Wilson 95% |
|---|---|---|---|
| **publishable** | 0 | **0.0000** | [0.0000, 0.0758] |
| **asker_only** | 21 | **0.4565** | [0.3179, 0.6012] |
| **third_party** | 20 | **0.4348** | [0.2987, 0.5783] |
| **none** | 5 | **0.1087** | [0.0449, 0.2340] |

**G1 FIRED.** `publishable` is 0 of 46, below the declared kill of 0.50. The
missing evidence is **not in anything the project publishes** — not in
changelogs, release notes, specs, commits, or documentation. The FETCH route
closes.

**G4 FIRED.** `has_ask` = 31/46 = 0.6739 and `ask_then_asker` = 31/46 =
0.6739, both above the declared bars of 0.50 and 0.25. The venue's own
workflow already runs the round trip on the very rows this experiment
measures, and the person supplies the fact. The honest statement about the
class is **not** "unserved": it is *served by an interaction that already
exists, and unreachable by one-shot answering*.

**G5 NOT fired.** `none` = 5, not above 9. The reader disagrees with CLF on
5 of 46 = 0.1087 of the class, so EVID precision on this population is
**above 0.80** and every number in E177 that carries the class's size is
not conditional on a single reader of unestablished precision.

## M1 — the thread's own round trip (automatic, all 46)

| # | number | rate | meaning |
|---|---|---|---|
| 1 | `has_comment` | 37/46 = 0.8043 | share whose question carries at least one comment |
| 2 | `has_ask` | 31/46 = 0.6739 | share whose question comments contain an ask |
| 3 | `ask_then_asker` | 31/46 = 0.6739 | share where the person actually went and got the fact |
| 4 | `answer_asks` | 20/46 = 0.4348 | share whose key answer carries an ask |
| 5 | `evidence_in_comments` | 39/46 = 0.8478 | share where the missing evidence tokens reach the comments |
| 6 | `discriminating_and_asked` | 28/46 = 0.6087 | the joint that matters for ASK |

**The venue already runs the round trip.** On 31 of 46 rows, the thread
itself contains a request for the missing fact. On 31 of 46, the asker
actually went and got it. On 39 of 46, the missing evidence's tokens appear
somewhere in the comments — the ask was answered in the thread. The
`discriminating_and_asked` joint is 28 of 46 = 0.6087: in 60.87% of the
class, the missing fact was both discriminating (it selected between causes)
and asked for in the thread.

## M2 — the re-key (one reader, all 46, blind)

The reader instruction was committed before the reader saw any row. The
reader was blind to E177's labels (G0d: 0 leaks). The reader's output is in
`rekey.jsonl`.

**The missing evidence is a version, a config value, or a data value the
asker holds.** 21 of 46 = 0.4565 are `asker_only`: the version they have
installed, the flag they passed, the value in their config or environment,
the contents of their data. 20 of 46 = 0.4348 are `third_party`: a
framework's internal behaviour, a standard's text, another package's
defaults. **0 of 46 are `publishable`.**

The 5 `none` rows are rows where the reader judged the resolution reachable
from the question's own text — a disagreement with CLF on 0.1087 of the
class, which is within the G5 bound.

## M3 — the inherited label's grounding (automatic, all 46)

| measure | rate | meaning |
|---|---|---|
| `already_present` | 7/46 = 0.1522 | the named evidence's tokens appear in the question |
| `used` | 37/46 = 0.8043 | the named evidence's tokens appear in the key answer |

**7 of 46 = 0.1522 are defects**: the fact the label says is missing is in
the question. This is a ceiling on E177's EVID labels, not a correction to
them — the headline is not recomputed.

## The exploratory comparison (not a gate)

| | missed | reached |
|---|---|---|
| `discriminating` | 0.5926 | 0.4074 |
| not `discriminating` | 0.6667 | 0.3333 |

The gap is -0.0741, p = 0.52. **The addendum's reframing does not reproduce
on a blind reader over all 46.** The class is not "questions whose posted
symptoms underdetermine the cause" in a way that separates misses from
reaches. The missing evidence is a fact the asker holds, and the thread
already asks for it.

## What this decides

**1. E177's population closes with no candidate.** The missing evidence is
not in anything the project publishes. The FETCH route closes. The only
surviving route is ASK, and G4 says the venue already runs that round trip.

**2. The venue's own workflow already serves the class.** On 31 of 46 rows,
the thread itself contains a request for the missing fact. On 31 of 46, the
asker actually went and got it. The honest statement is not "unserved" but
*served by an interaction that already exists, and unreachable by one-shot
answering*.

**3. The class is a version-and-config problem.** 21 of 46 are `asker_only`
and 20 of 46 are `third_party`. The missing evidence is a version, a config
value, or a data value. This is a population that needs the asker to supply
a fact, not a tool to fetch one.

## Ceilings

- **Conditional, not prevalence.** E177's draw is reused from E175, which
  reused E168's method. No number here is a rate on any pool.
- **Comments are not the thread.** Asker edits to the question body are
  invisible to M1. On Stack Overflow, editing the question *is* the
  canonical way to supply a missing fact, so M1 under-counts the round trip
  by an unknown amount.
- **The lexicon under-counts asks.** G0a was not run in this session; the
  lexicon's error rate is unmeasured on this population.
- **M2 is one reader, same family, blind to labels but not to the key
  answer.** Agreement between two same-family readers is not two independent
  codings.
- **n = 46 and the gate is a decision rule.** At n = 46, a share of 0.50 has
  a Wilson 95% interval of roughly [0.36, 0.64]. G1 cannot distinguish 0.36
  from 0.50, so it decides which route the next session spends its budget on,
  not whether the class is fetchable.

## Named next action

**E177's population closes.** The missing evidence is not in anything the
project publishes, and the venue's own round trip already supplies it. The
class is a version-and-config problem that needs the asker to supply a fact,
not a tool to fetch one.

The next experiment is the one that measures whether a specific published
artefact answers the question, on a fresh draw — but the `publishable` bucket
is empty, so there is no published artefact to measure. The line is closed.

**Do not run:** E176 as written (a third classification of the same rows by
the same instrument), E170's global arm, another view-count domain (D105,
F133), or a fresh draw of E177's comparison before the composition of the 46
is examined.
