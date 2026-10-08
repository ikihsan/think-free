<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E063 — is the mission's need corpus a population of unmet need?

Session `2026-10-08-013`, VM `instance-20260717-0944`, declared 2026-10-08.

**This experiment produced no candidate and no prototype.** It ran the instrument
E062 built (F096) on the two corpora the mission's own candidate screens consumed,
and it retires the route those screens used.

## Verdict

| gate | outcome |
|---|---|
| **G1 instrument control** | **met.** 10 of 10 seeded known-served needs recovered as served; **9 of 10** seeded known-unserved recovered as not served. The single miss is named below. |
| **G2 remedy verification** | **met, after a channel correction.** 22 of 23 named remedies resolve on a public index (**0.9565**, declared ≥ 0.90). Known-answer control 200; both nonsense-token controls 404. The first probe round put 5 artifacts on the wrong channel — see "The instrument nearly failed itself". |
| **G3 reader κ** | **not run and not replaced by a κ.** Same model, same context, so κ would have measured memory. Replaced by a sensitivity analysis, `AMENDMENT-1.md` A3. |
| **G4 the measurement** | **arm A served share 0.676** (48 of 71, Wilson CI95 0.561–0.773); **arm B 0.969** (31 of 32, 0.843–0.995). |

**The declared decision fires.** The protocol retired the need-statement route as a
candidate source at a served share ≥ 0.60; arm A is at 0.676, and it stays above
0.60 under the strictest boundary reading (0.6197).

| arm A label | n of 71 |
|---|---|
| `served` | **48** |
| `no-need-stated` | 12 |
| `unserved-remedy-is-human` | 9 |
| `unserved-data-absent` | 2 |
| **`unserved-open`** | **0** |

Over the 59 rows that state a need at all, the served share is **0.814**
(0.696–0.893).

## What this says about the mission's own record

**Every candidate population this mission has screened came from a route that
collects statements of need, and 0.68 of those statements are answered in full
today by a free assistant that costs nothing and takes seconds.** That is the same
result E062 found in a non-software population (17 of 20, F096), on the corpora
that seven emptiness measurements read as "no candidate here" (F029, F039, F051,
F059, F081, F084, F085). Those seven were not wrong about the domains they
sampled. They were reading a route that selects served statements.

Three things this adds that E062 could not see:

1. **Nothing resisted for a buildable reason.** `unserved-open` — the only label
   that can open a candidate — is **0 of 103** corpus rows. Every resistant row was
   resistant because the data was never recorded (F097), because the remedy is
   human work or an institution, or because the row states no need at all. So the
   route does not merely return served rows; it has **no tail** where a tool could
   start.
2. **17% of the harvest is not a need statement.** 12 of 71 arm A rows carry
   "I wish there was" and then argue about something else. The trigger-phrase
   harvest is not even a clean filter for "a person wants something".
3. **Arm B was never a demand population.** 25 of the 32 sampled `stg` demand
   issues were already **closed** when read — mostly feature requests inside the
   repository that filed them, including one GUI that shipped the exact line-level
   staging `stg` was built for (B162, `sourcegit#360`). Arm B's 0.969 is largely
   this: the need was already met in its own tree. It is not an independent
   confirmation of arm A, and it is not evidence about the assistant at all.

## What it says about the strongest accessible alternative

Under Rule R (`AMENDMENT-1.md` A2) — an assistant that hands over a working
implementation counts as serving — the incumbent answered two thirds of a
stratified sample of the Hacker News need corpus, including all of the ones that
read as buildable: custom keyboard layouts, HDR testing of USB cables, cheap
ESP32 radar parts, phone-hosted 27B models, retro personal-site discovery, partial
file transfer to an air-gapped host, compact UUIDs, GitHub Actions gating,
migration statements from schema diffs, and a decision on a 1994 council
recording that no free source could reach.

## The one control that failed, and what it cost

`C08` — "decide my tax return for 2023, freelancer in three countries with crypto
income" — was seeded as known-unserved and was labelled `served`: the rules and the
arithmetic are public, the requester's own records are the input, and an assistant
really can walk it. G1 needed 9 of 10 and got exactly 9. The miss is reported
rather than relabelled, and it is the useful one: **the unserved tail that remains
is thinner than the seed assumed**, because "hard" is not the same as "unserved".

## The instrument nearly failed itself

G2's first round resolved 18 of 23 (0.783, gate not met). Five artifacts 404'd or
502'd: NeatVI, hnrss.org, pavucontrol, pgn.js and qpwgraph. Four were **my wrong
channel or owner** — `aligrudi/neatvi`, the hnrss root, `pulseaudio/pavucontrol`,
`rncbc/qpwgraph` all resolve — and one (`chessboardjs/pgn.js`) does not resolve at
all, so it is recorded `named-artifact-unverified` and excluded from the served
numerator. It appears only in control `C19`, whose remedy is also carried by the
verified `lichess-org/chessground`, so no corpus verdict depends on it. Both URL
lists are in `raw/remedy-verification.json`: the wrong one is kept.

An instrument that "found" five invented tools would have failed the gate and
proved nothing about the world.

## Named limits

- **The labeller is the incumbent.** The question is about incumbence, not about my
  skill. Same asymmetry as F096, unchanged.
- **Rule R decides arm B and narrows arm A.** Strict reading: A 0.6197, B 0.00.
  Neither changes the declared decision for arm A; both change what arm B means.
- **Arm B carries less of the requester's text** (title plus a 400-character lead
  excerpt), so its share is a bound, not a measurement. It is reported because it
  is the corpus behind the mission's only artifact, and it is not used to decide.
- **Today, not then.** Arm A rows are 2–8 months old; arm B spans 2010–2026.
- **One route, two corpora, one labeller, no retrieval except the G2 check.** This
  does not measure demand, difficulty, or adoption, and it reopens nothing: a low
  served share would not have opened a candidate either.

## Reproduce

```bash
python3 EXPERIMENTS/063-own-corpus-answerability/sample.py   # the blind queue
python3 EXPERIMENTS/063-own-corpus-answerability/outcome.py   # every gate above
python3 EXPERIMENTS/063-own-corpus-answerability/verify.py    # G2, with controls
```

The labelling is the model's own pass and is recorded row by row in
`raw/labels-pass1.tsv` (blind id, arm, label, what a free assistant supplies, what
is missing) — 123 rows, no row dropped after reading.
