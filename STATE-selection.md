<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# What the mission selects candidates on

Split out of [`STATE-next-actions.md`](STATE-next-actions.md) on 2026-10-06
(T-0081), where item 0 had reached **168 of that file's 300 permitted lines**.
The split is by invariant, not by size: that file ranks *work to be done*, and
item 0 is not work — it is an **owner decision** that no experiment in this
repository can settle, so keeping it in a ranked work list invited it to be
worked on. It is preserved here verbatim, including its reasoning, with E039's
result added where E039 answered part of it.

Nothing here is a defect to repair and nothing here is blocked on tooling.

## The decision, stated

**What does this mission select candidates on, now that novelty cannot be the
filter — and the premise behind the old filter is now measured?**

**Renumbered on 2026-10-06.** This file was written as `STATE-next-actions.md`
item 0 with D053 and E021, and moved here with the numbering the other VM's
publication forced (F060, D068, E039). The reasoning is unchanged.

## Why it is not novelty, and why that took four measurements

Twelve candidates, twelve prior-art deaths, the twelfth being `tools/origin`
itself (`RESEARCH/PRIOR-ART-ORIGIN.md`, F026, F027). Each measurement below
attacks the screen's own premise:

| finding | axis | what it measured | which way it came out |
|---|---|---|---|
| F034 | soundness | 4 of 4 on-topic incumbents in mature vocabularies are served, **1 of 4** in a young one | against the screen |
| F035 | coverage | 3 of 12 adjudicable kills have no prior art on any of three corpora; 4 were reachable only on the open web | against the screen |
| F037 | composition | the young arm is **14 of 18 executable code**, not prose | against the "it's just documents" rescue |
| F041 (other VM) | distribution | the copy channel holds **1,026** repositories against **8,676** monthly installs, ratio **0.118** | **against** the "used and invisible" reading |
| F060 (this VM) | demand side | the need corpus's own threads answered 57% of its statements, drew a link for 5.5%, and named anything new in **0 of 1391** | against the corpus as an artifact signal |

The screen is therefore sound where it is least load-bearing and unsound precisely
where this mission's candidates live — which is neither a reason to keep it nor a
reason to drop it, but a reason to state the axis in terms of the vocabulary a
candidate sits in. **Every channel that could have carried the choice has now been
measured, and five measurements agree that supply-side counts do not carry it.**

**This is an owner decision:** which axis replaces it (usefulness without users,
distribution, domain knowledge, or something not yet named), and whether
publishing the tooling as-is is ever on the table.

## Ceilings on the four measurements

F034's own gate is `inconclusive` — 43% of incumbents were undecided against a
declared 20% ceiling — and its young arm rests on four decided rows. F027's sample
is small and self-selected, and 0 stars is a weak proxy with known false negatives
(`ripgrep`, `jq`). F037's undecidable fraction is partly an artefact of which
channels were consulted. F060 is one site, one audience, 466 days, over a
population of threads chosen because a need comment happened to be in them.

## What is left, and it is one question

Everything measured about **supply** says supply is uninformative about demand
(F028, F032, F037), and the demand-side corpus is now measured and cannot answer
it either. **But that corpus is 1250 named, publicly identified people who each
wrote down, in public and unprompted, what was missing from their work.** It is
the only demand-side asset here that is not a supply count.

The axis it suggested was not "does anyone want this" — unmeasurable without
publishing — but "**is there a specific person who already told us exactly what
they want, and did they use the thing?**".

**E039 has now measured the second half of that question and answered it.** The
public record of responding to a need contains no outcome signal at all: **1 of
794** requesters whose need drew a reply replied again, and **0 of the 77** whose
need drew a link. So the outcome of a need is not recorded anywhere in the thread
it was asked in, and an axis of that shape needs a channel this repository does not
have. That is a build-or-buy question and therefore the owner's.

**Ceiling on the whole suggestion:** contacting anyone needs authorization, its
denominator is 1250 people who happened to post on one site, and one satisfied
requester proves nothing about a market.

## The reasoning as recorded before E039

Preserved because it is the reasoning the owner reads, and because E039 changed
part of it rather than all of it.

F035, F037 and F039 took the three measurements that bear on this, and F039
removed the last remaining source. F035 measured **coverage**; F037 measured
**composition**; F039 measured the **need corpus the survivors came from** and
found it is **1250 distinct individuals**, median one comment each over 466 days,
with **no need-level recurrence detectable inside it**. A yield measured on it was
never interpretable (D051), so E016's two surviving leads (12 and 16) are closed
*as sources*: the premise that anyone shares the request was never measured. The
instrument question is answered too — **four of six positive controls with
demonstrated adoption returned 0 or 1 distinct author**, so no recurrence verdict
could be drawn and the kill gate is recorded *not evaluable*. A lexical count
cannot carry a claim about demand.

That session also falsified its own headline: a shared content *word* is a weak
test, and two stricter measures added afterwards disagree with the 79.25% they were
meant to test. What survives is narrower than this item first said: not what to
search, and not what the screen found, but what a fact about supply is supposed
to tell us about demand — the young arm's median row is a 60-star tool, 14 of 18
rows have no readable use channel, and the most-starred tool there is installed
363 times a month.

The third reading was taken too (F040, `EXPERIMENTS/020`): copying is widely
*instructed* — `cp -r .claude` in **687** Sourcegraph content matches against a
nonsense control of **0** — and barely *duplicated*: **92 of 1950** distinct
configuration file contents (4.7%) are byte-identical across repositories, and
**no two repositories from different authors overlap by half**. The near-zero
install readings are not explained by an invisible distribution channel. Drift
itself is `inconclusive`, not zero. **The last open channel — forks and dependents
— was VM 0944's T-0064 and has since been answered on the base.** Its result (F041
in that VM's numbering, `EXPERIMENTS/021-copied-artifact-serving`) is the opposite
of the reading above and it is the important one: the copy channel holds **1,026**
indexed repositories against the young arm's **8,676** monthly installs, a ratio of
**0.118** against a declared dead-gate of ≤5×. **So the artifact really is
installed and lightly counted, and F037's "used and invisible" reading does not
stand** — the fourth measurement of this screen, and it is the one that finally
closes the young-vocabulary question.

## Related work this decision is not

- **Item 0b**, the CI flake, is deferred on purpose: CI is green and nothing is
  blocked on it.
- **Item 0c**, the undecidable-fraction question, is mostly closed by F037 — and
  **E039 supplied the falsifier it was waiting for.** Its falsifier was "a
  population where the unmeasurable fraction is near zero". The need corpus's own
  threads are exactly that, and in them the *reading* fraction is high (99.3% of
  needs recovered) while the *serving* fraction is 0 of 1391. **A channel can read
  an artifact perfectly well and still say nothing about whether it serves the
  clause** — which is the sharper form of 0c's worry, now measured rather than
  argued. What remains open is narrower: whether an *unreadable* row predicts
  anything, which needs a stated channel set or it measures the instrument.
- **Item 0d**, the invention seat, holds no queue: both generators under it are
  closed for measured reasons (F029, F033, F039), and lead 7's mechanism answer
  was a feature gap (F038). E2's lockfile claim is the only live mechanism there.
- **Item 12**, "do not build a product", stands: nothing is selected.