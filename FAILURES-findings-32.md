<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-08
-->

# Failure findings 32

Split from `FAILURES-findings-31.md` at its 300-line cap.

## F090 — The token-cluster instrument's G1 passes on the remaining 38 Stack
Exchange sites are all topics, never a single step; the channel-level null
now covers the whole population (E058)

E058 ran E057's exact protocol on the 38 survivors E057 skipped
(`kept[12:]`): same stratum (open, no accepted answer, 36 months), same
two votes arms (ascending tail, descending head), same instrument, same
manual read of each G1 cluster as one step or one topic. 38 sites, 76 arms,
11092 rows, 7022 distinct requesters.

**G1 as a step count never fired.** The nominal cluster count was large
— 23 tail / 19 head concepts at `edge=4, minusers=8` — but the same
hand-read that E057 applied to its three G1 clusters yields no step:
`visa → Expatriates/Travel`, `solana wallet transaction`, `Craft CMS
fields`, `monero wallet gui`, `window file drive install`, `lens camera
flash`, `wood finish` are all topics the requester can be about, not one
step with one success condition. The three E057 G1 clusters (identify an
unlabelled object/part) remain the only step-level fires in the whole
50-site survivor set, and both died at G2.

**What this strengthens:** E057's null was "this channel does not show one
in the 12-site slice". After E058 it is "this channel shows exactly one
class of recurring step (unlabelled-object identification) in all 50
survivors, and that class is served". G2/G3 therefore no longer need to be
re-run on a wider slice of the same channel.

**What it does not close:** the channel itself (Stack Exchange: formulable
needs, question-is-a-step framing, English, self-selected). The primitive
remains the G2 correction E057 recorded: in this channel the requesters
name the incumbents. The score-tail rule does not transfer here either
(E058's nominal G1 counts were indistinguishable across arms, 23 vs 19).

**Evidence:** [`EXPERIMENTS/058-se-remaining-sites/README.md`](EXPERIMENTS/058-se-remaining-sites/README.md),
`PROTOCOL.md` (gates declared before the fetch), `raw/` (76 arms, index),
`cluster.py` (same instrument as E057).
