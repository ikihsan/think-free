<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E058 — The remaining Stack Exchange survivors: does a recurring unserved
# step appear there?

`observed` 2026-10-08, session 2026-10-08-006. Protocol declared before
the fetch: [`PROTOCOL.md`](PROTOCOL.md). Same instrument as E057
(`EXPERIMENTS/057-unserved-step/`), same gates, same arms.

## Verdict

**`KILL`. G1 never fires at step level on any of the 38 sites, so the
decision rule builds nothing.**

| gate | result |
|---|---|
| **G1 (as one step)** | **FAIL.** 23 tail / 19 head nominal clusters at `edge=4, minusers=8`, and every one reads as a *topic*, not a step, under the same hand-read E057 used. No step cluster in this slice. |
| **G2** | Not reached; G2 kills a step cluster, and none survived G1's reading. |
| **G3** | Not reached. |

## What was run

`observed`. 365 sites enumerated from the API's own site list; 50 survive
E057's published exclusion list; E057 ran the 12 alphabetically first;
**E058 ran the remaining 38**, same stratum: open, no accepted answer, 36
months from 2023-10-24, `pagesize=100`, two votes arms (ascending tail,
descending head = control B1), two pages per arm. **76 arms, 11092 rows, 7022 distinct requesters.**
Raw rows in `raw/`, unedited.

## The G1 clusters and why none is a step

`observed`. At `edge=4, minusers=8` the nominal clusters split as:
Solana/Anchor wallet errors (57 tail / 79 head users), Craft CMS fields
(46/37), Expatriates/Travel visas (42/66), Tridion publishing (30/30),
Monero wallet GUI (25/25), GenAI model errors (12/22), Tor connectivity
(21/21), Cross Validated regression (12/13), Pets/cats (18 users), and
similar — all of these name a *topic*, never one step with one
success condition. The three G1 step clusters E057 found — identify an
LEGO brick (Bricks, 49+39 users), identify a bicycle (16), identify a
specimen (Biology, 8+22) — remain the only step-level fires in the whole
50-site survivor set, and E057's G2 killed two of the three and G3 the
third.

## What E058 changes

E057's null covered 12 sites. E058 extends it over every site left after
the same exclusion list: **the channel shows exactly one class of
recurring step, and that class is served**. G2 does not need to be re-run
on a wider slice. The primitive E057 recorded — G1 is free in a corpus of
thousands of requesters — held again: 23 nominal clusters at the same
threshold that produced 3 step-level reads on a third of the sites.

## Ceilings

Same as E057: one channel (Stack Exchange), English, formulable needs,
a question is a framing not a practice, title-level clustering reads
framing, nothing contacted or published. Cross-site step recurrence
(≥5 users across ≥2 sites) was pre-declared in G1's alternative and did
not appear either.

## Reproduction

```
python3 EXPERIMENTS/058-se-remaining-sites/fetch.py    # raw/sites index + 76 arms
python3 EXPERIMENTS/058-se-remaining-sites/cluster.py  # raw/clusters.json
```

One raw file, `raw/mechanics-tail.json`, carries the repo-standard
exemption header on line 1 (`# origin-allow-secret-patterns: openai-key`):
the scanner's `openai-key` pattern fires on the URL slug
`sk-rapid-u0416…-link-beween-trouble-codes` inside a question title. Stripping
line 1 restores the original fetched bytes; the file predates the header and
the header is declared here so the exemption is not silent.
