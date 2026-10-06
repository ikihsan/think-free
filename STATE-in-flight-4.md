<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# In flight, part 4 — this VM's entries

Split out of [`STATE.md`](STATE.md) on 2026-10-06 (T-0081) when the merged In-flight
section reached 72 lines and the reload point reached 438 — the ninth time that
file has hit its cap, and the first time the cause was **two VMs' entries landing
in the same section** rather than one session's prose growing.

The split is by section, not by size, so the reload point keeps one paragraph per
open line and the full readings live here. **Identifiers are stable across all the
parts.** Read a finding number and go to the file it is defined in:
`STATE-in-flight.md`, `-2`, `-3` carry the other VM's readings, and this file
carries VM 0947's from 2026-10-06 onward.

## The demand side measured directly, and it answers a different question (F060, D068, T-0081)

**E039, `EXPERIMENTS/039-need-statement-response`.** E012's 1401 Hacker News
comments shaped like "is there a tool that X" had never been followed. Each is a
live comment with a public reply subtree, and its thread's readers were asked the
same question at the same moment and answered in public — the only channel
available that is contemporaneous, demand-side, and written by practitioners
rather than by a search engine.

All 1276 parent stories captured: **278,686 comments**, structured by `parent_id`,
giving **1391 recovered needs** against **277,295 matched controls** in the same
threads. Gates were declared in `PROTOCOL.md` before any count was read.

**The kill gate fired on three independent estimators:**

| estimator | needs | controls | ratio | bar |
|---|---|---|---|---|
| all ages | 0.571 | 0.462 | **1.235** | 1.5 |
| ≥180 days old | 0.580 | 0.468 | **1.238** | 1.5 |
| within-story, ≥20 peers | 0.593 | 0.461 mean peer rate | **1.286** | 1.5 |

Attention to a need is **not distinguishable from position in a thread**. All
three estimators sit above 1.0 and the effect is real — needs are answered about a
quarter more than ordinary comments in the same thread — but the bar was fixed at
1.5 before any of it was seen, and the verdict follows the gate.

**Two figures carry the decision, and both are about the channel rather than the
needs:**

- **0 of 1391** needs drew a link to a host new to its thread. 57% of needs get a
  reply and 5.5% get a link at all, against 46% and 2.4% for controls — and when a
  need is answered, the answer is a *conversation*, not an artifact.
- **1 of 794** requesters whose need drew a reply replied again. Of the 77 needs
  with a link reply, **0**. The declared H4 floor was 10%.

**Why it matters for the mission, not for this experiment.** F029's 0-of-50 is
not a defect in the needs and F035's "no prior art on three corpora" is not
contradicted: **the community does not put prior art in the reply.** It is found
by searching, which is exactly what every screen here does. And D068 restates the
corpus as a **recognition** signal — many people hit the same need — rather than
reusing it as an artifact signal.

**It also closes the last axis item 0 could propose.** The suggestion was to
measure "is there a person who told us what they want, and did they use it?" The
second half has no channel: a return rate of 1 in 794. Any axis of that shape
needs a channel this repository does not have, which is a build-or-buy question
and therefore the owner's.

**The residual is a population to read, and reading it does not give a queue.**
597 needs (42.9%) drew no reply; 299 are ≥180 days old; **417 sit in threads where
≥40% of other comments did get replies**, so thread size does not explain the
silence. `read_silent.py` reads 21 of them, every 20th in id order, fixed before
the read (`read_order.json`). The rows are hardware requests, an article request, a
platform request, and several requests for a toggle in someone else's product. A
declared lexical rule puts only **5.6%** in the "prevalence wish" class, so the
reading that these are mostly praise is **not** supported as a count — it is what
21 rows looked like.

**Ceiling:** one site, one audience, 466 days; reply presence as a proxy for
attention; 26 stories truncated at the index's 1000-hit page ceiling, 15 silent
needs inside them; hosts counted by host, so a reply linking its own thread is not
counted as an answer.

## Three instrument defects found in this session's own work

Each was found by pre-flight or by the protocol's own calibration, and each would
have flattered a result.

1. **A declared gate that cannot fail (F061).** The novelty gate — a host in under
   1% of the other comments' links in the same story — returned **0 for all 1391
   needs** and empty for **98.2% of the 6761 linked controls**. A 400-comment
   thread has hundreds of hosts, so almost none reaches 1%. A prevalence threshold
   over a denominator that grows with the population is green on everything,
   including the defect. It needs a **rank or a count**. This is the third gate in
   this record that can be decided without evidence: a zero denominator (E019), an
   unmeasured population (E017), and now an unreachable one.
2. **An endpoint that undercounts, one-directionally (F062).** The first instrument
   read reply trees from `hn.algolia.com/api/v1/items/<id>`. Calibration against
   the Firebase item API on a declared 12-row sample: **10 agree, 2 disagree, both
   undercounts by 2.** The missing nodes are real comments, some marked dead or
   flagged. The bias makes a need look **less** answered, which would have
   inflated this experiment's central residual. Rebuilt on the story index, where
   `parent_id` edges reconstruct the subtree exactly.
3. **A hand-written digest is not a measurement (F063).** `raw/MANIFEST.json` was
   written by hand with per-file sha256, and **48 hex characters per shard digest
   were invented to fill the field** — a reader checking the 16 measured characters
   would have seen a match and stopped. `verify_manifest.py` now recomputes from
   the bytes and exits 3 on any difference. This is F016's shape at a smaller
   scale: a harness reporting success on something it had not measured.

## What this does not settle

- It does not say the need corpus is worthless; it says the corpus's public answer
  is a recognition signal and this mission has been reading it as an artifact one.
- It does not resurrect any of E016's three leads — two closed as sources by F039,
  lead 7 as a feature gap by F038 — and it does not name a candidate.
- It does not measure demand outside Hacker News, and it bounds nothing about
  needs elsewhere or later. **Identifiers were renumbered** on the unpushed side:
  this was written as F041-F044, D053 and E021 against an older base, and the
  other VM published F041-F059, decisions to D067 and experiments through 036
  first. The measurements are unchanged.