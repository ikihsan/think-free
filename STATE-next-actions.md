<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# Next actions

> **READ FIRST (2026-10-12).** The view-count domain sweep is **STOPPED**
> (E113, F116, D105). E113's matched-harvest control of E107 showed the
> effect is a harvest artifact (δ 0.826 → 0.075, stratified p=0.183) and the
> shared classifier labels only 28% of a representative pool. Every
> "ALL GATES PASS" below that came from this line is **`untested` on a matched
> harvest, not confirmed**. Do not run another registry sweep. See
> [`EXPERIMENTS/113-viewcount-matched-harvest/`](EXPERIMENTS/113-viewcount-matched-harvest/README.md).

## E182 completed (2026-10-18) — the fourth explanation of F136's gap is gone, and the ground truth has a measured ceiling

**What was tested.** E181 left one explanation standing: is the EVID gap a
disagreement with the community's chosen resolution? **The question had to be
corrected before it could be asked.** E177's draw is of questions that were
*unanswered*, so `accepted_answer_id` is non-null on **3 of 181** rows, **1 of
145** key rows, and **0 of the 60 scored rows** — the key answer is the
**top-voted** one, which E177 had already disclosed in its own RESULT and in a
pre-declared AMENDMENT-2. Three documents carried the superseded wording into the
next session, so *is the **accepted** answer the best answer, or merely the
**accepted** one?* named a field the population does not contain (F141).
Corrected to **top-voted**, with an instrument built for it.

**Two instruments, and the first had to be destroyed.** Vote margin looked like a
cheap non-judgemental proxy and was **4 of 10 against hand-read labels** — wrong
in both directions at similar rates, so not a noisy proxy but no proxy:
implementation competition reads as disagreement (`zip_transform` against a `zip`
loop), and flat contradictions sit under wide margins (`qid 79556333`: "you
can't, closed Shadow Root" against "you can add CSS, see the docs", runner-up at
44%). **Its earlier null was therefore withdrawn rather than reported.** Raw
prescriptive-token overlap was then **rejected at 0.6500 balanced accuracy
against a bar of 0.80 declared before either ran**, with specificity at
**0.5000 — chance**. The rejection is what identified the defect: shared
*problem* vocabulary counted as shared *prescription*. **Residualised against the
question's own tokens it reached 0.8000 balanced accuracy at specificity 1.0000**,
and the gate ran on it. Neither the bar nor τ moved after a result was seen.

| arm | rows | `divergent` |
|---|---|---|
| EVID missed | 9 | 4 |
| EVID hit | 6 | 3 |
| SELF hit (reference) | 12 | 4 |

**G2′ did not fire: Fisher exact p = 1.0, OR 0.80, diff −0.0556.** A post-hoc
exact permutation test on the continuous statistic, same instrument, same rows:
median residual overlap **0.054 against 0.083**, **U exactly at `n₁n₂/2`,
p = 1.0000** — not a near-null.

**Coverage is the real ceiling and is stated rather than smoothed.** Of 60 rows,
16 are `single_answer`, 2 have a runner-up scoring ≤ 0, and 5 more are conceptual
rows with no prescription to compare. **37 of 60 rows are labelled and 21 of the
30 EVID rows**; the remaining 9 EVID rows are `untested`. The accepted detector
has sensitivity 0.6000, and the bound it implies straddles both arms.

**What this decides.** With E178 (`publishable` 0/46, `has_ask` 0.6739), F137 /
F138 (0.9000 on money SE) and E181 (every paired arm null), **all four
explanations of F136's gap are closed and the EVID line closes as a capability
limit** — the assistant reasons worse on questions whose resolution needs a fact
the question omits, which no context pipeline closes (D120). This is the first
closure in the line with its last explanation measured rather than unexamined.

**And a ceiling on this record's own headline numbers.** The ground truth behind
every service rate here is **contested on 21.7%** of rows (a runner-up within a
factor of two of the top-voted answer) and **uncorroborated on 26.7%** (one
answer, nothing to disagree with) — **48.3%**. E177's scorer asks whether the
assistant states the same resolution as the **top-voted** answer, so on those
rows it measures agreement with a resolution that is disputed or uncorroborated.
That weakens hit and missed rows alike, so it explains **none** of the SELF/EVID
*gap* and bounds every absolute *level* here, **0.8667 and 0.4000 included**.

**Do not run:** any re-test of resolution divergence on this population; vote
margin as a disagreement proxy; a third overlap instrument.

**Named next action: `prior-art-check` the ground-truth-quality axis before
writing product code.** A public corpus consumed as training and evaluation data
has **48.3%** of its high-arrival resolutions contested or unattested, and a
three-signal filter — vote margin, corroboration count, residualised prescriptive
divergence — now has a **calibrated** discrimination estimate (0.8000 /
specificity 1.0000) and a **measured** prevalence. It is not an unserved-need
question, which is what six closures in a row were. Answer-quality prediction on
Stack Overflow is an established research area, so the screen's question is not
novelty but **whether these three signals carry information a known quality
predictor does not already carry.** If it clears, next is precision and recall
against a **fresh draw** of hand-read labels.
[`EXPERIMENTS/182-ground-truth-contest/RESULT.md`](EXPERIMENTS/182-ground-truth-contest/RESULT.md).

## E181 completed (2026-10-18) — supplying the missing fact moves nothing, and neither does pasting the thread

**What was tested.** E177 measured the assistant at 0.4000 on questions whose
resolution needs a fact they never state. The obvious product is: identify the
fact, ask for it, close the gap. E181 ran that as four paired arms on one
population, all answered and scored in one session, with no arm label in any
input file and a leak assertion on every input.

| arm | added context | reached | Wilson 95% |
|---|---|---|---|
| question only | — | 7/14 = 0.5000 | [0.2680, 0.7320] |
| **+ the one extracted missing fact** | 15.5 median tokens | 8/14 = 0.5714 | [0.3259, 0.7862] |
| **+ every comment on the thread, verbatim** | 232.5 median tokens | 9/14 = 0.6429 | [0.3876, 0.8366] |
| + a fact from a different row (placebo) | 14.5 median tokens | 4/10 = 0.4000 | [0.1682, 0.6873] |

**Every paired comparison is null.** Treatment vs floor: exact McNemar
**p = 1.0**. Treatment vs whole thread: **p = 1.0**. Floor vs whole thread:
**0 rows for, 2 against, p = 0.5** — *pasting the entire discussion never once
beat answering the question alone.*

**Two numbers survive.** An extracted fact is **6.7%** of the tokens of the
thread it came from, so targeted elicitation would have been fifteen times
cheaper than pasting; it simply is not the mechanism. And on all 30 of E177's
EVID rows the comments name the deciding fact on **14/30 = 0.4667**, with **10 of
the 16 nulls carrying the remedy itself** and 6 carrying another reporter's
observation. **So F137 and F138 need one clause: the round trip runs to the
solution, not to the fact, and on more than half of these rows the solution is
what it delivers.**

**Two findings about this record rather than about the world.**
**G4 FIRED**: the same reader re-scoring E177's own answers one day later
disagreed on **4 of 10** against a declared tolerance of 3, so a one-reader
reach rate here is not stable at ±0.4, and **no absolute level in E181 may be
compared with E177's 0.4000 or 0.8667** — only its within-session paired
comparisons survive. **K1 fired** (14 rows carry a fact, declared floor 16), so
G1–G3 and G5 are `not evaluable`, G5's blind re-read was partially executed,
and every arm is labelled exploratory rather than a gate result.

**What this decides.** The elicitation route for the EVID class closes. F136's
population gap stands and is now *unexplained* rather than *under-supplied*.
**Do not re-run:** a larger elicitation study on this population, or a
"paste-the-thread" arm on it, or a placebo arm on it — all three were measured.

**Named next action.** Read the rows every arm missed and ask whether the
accepted answer is the **best** answer or merely the **accepted** one. One
reader, no new fetch, and it is the only explanation this population has left:
if the missed rows are rows where the community's chosen resolution is
contestable, then the EVID gap is a disagreement about answers and no context
pipeline of any kind will close it.

> **RUN as E182 (2026-10-18) — and the wording named a field this population
> does not contain.** `accepted_answer_id` is non-null on **0 of the 60 scored
> rows**: the draw is of questions that were unanswered, and the key answer is
> the **top-voted** one (F141). Corrected to *is the **top-voted** answer the
> best answer, or merely the top-voted one?* and run with an instrument built
> for it, because vote margin is not a proxy for resolution divergence (**4 of
> 10** against hand-read labels) and raw prescriptive overlap confuses shared
> problem vocabulary with shared prescription (**0.6500** balanced accuracy,
> specificity at chance). **Residualised against the question, the instrument
> reached its declared bar at 0.8000 / specificity 1.0000, and the gate did not
> fire**: Fisher **p = 1.0**, and an exact continuous test on the same rows gave
> **p = 1.0000**. **Do not re-run this line in any form.** The EVID class closes
> as a capability limit, and with it the fourth and last explanation of F136's
> gap.
> [`EXPERIMENTS/182-ground-truth-contest/`](EXPERIMENTS/182-ground-truth-contest/RESULT.md).

## Money SE fresh observation (2026-10-17) — the round trip is even stronger when missing facts are personal

A fresh observation on Personal Finance SE (`money.stackexchange.com`) tested F137's conclusion on a second venue. **Hypothesis (declared before the run):** on money SE, missing facts are more personal (income, debt, jurisdiction, age) and harder to elicit, so the round trip should fail *more* than on SO. **Result: the opposite.** On the 30 highest-arrival questions with answers, **9/30 = 0.3000 lack a specific personal fact** (income/age/jurisdiction/amount — the money-SE analog of E177's EVID class), and **27/30 = 0.9000 carry a round-trip ask** (someone comments asking for the missing fact), against SO's 31/46 = 0.6739. The round trip is **stronger** on money SE, not weaker: the venue asks *more* readily when the missing fact is personal, not less. **F177's conclusion is confirmed on a second venue** — the EVID class is served by the venue's own round trip, and the genuinely unserved residue is tiny and eventually answered. The "unserved need" hypothesis is dead for money SE too. Raw data: `/tmp/opencode/money_analysis.json` (per-question facts, comments, asks). **Next action:** the EVID line is closed on two venues. The mission returns to fresh exploration.

## E178 completed (2026-10-17) — the missing evidence is not in anything the project publishes; the venue's own round trip already supplies it

**The gap E177's own measurement opened.** E177 found a class of **46 of the
100 highest-arrival rows that carry a key answer** whose resolution depends on a
fact or artefact the question does not contain, and on that class a free general
assistant reaches **12/30 = 0.4000** against **26/30 = 0.8667** on the
self-contained half of the same pool (gap +0.4667, Fisher p = 0.000368; F136,
D118). The class is real and large and the rate on it is the lowest this mission
has measured. **None of that says the population is buildable**, which is what
this experiment asks.

**The result.** Blind re-key of all 46: **publishable 0/46 = 0.0000, asker_only
21/46 = 0.4565, third_party 20/46 = 0.4348, none 5/46 = 0.1087**. **G1 FIRED**
(publishable < 0.50): the FETCH route closes. **G4 FIRED** (has_ask 31/46 =
0.6739 >= 0.50, ask_then_asker 31/46 = 0.6739 >= 0.25): the venue's own
workflow already runs the round trip on the very rows this experiment measures,
and the person supplies the fact. The honest statement is not "unserved" but
*served by an interaction that already exists, and unreachable by one-shot
answering*. **G5 NOT fired** (none = 5, not > 9): EVID precision is above 0.80.
M1: has_comment 37/46 = 0.8043, has_ask 31/46 = 0.6739, ask_then_asker 31/46 =
0.6739, answer_asks 20/46 = 0.4348, evidence_in_comments 39/46 = 0.8478,
discriminating_and_asked 28/46 = 0.6087. M3: already_present 7/46 = 0.1522 (a
ceiling on E177's labels), used 37/46 = 0.8043. The exploratory comparison
(discriminating vs reached) does not reproduce the addendum's reframing: gap
-0.0741, p = 0.52. **E177's population closes with no candidate.**

**What this decides.** The missing evidence is a version, a config value, or a
data value the asker holds. The venue's own round trip already supplies it. The
class is not "unserved" but *served by an interaction that already exists*. The
next step is fresh exploration.

**Do not run:** E176 as written (a third classification of the same rows by the
same instrument), E170's global arm, another view-count domain (D105, F133), or
a fresh draw of E177's comparison.

