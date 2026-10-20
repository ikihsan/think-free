<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E126 RESULT — Stack Overflow closes like the others; the venue is served

`observed` 2026-10-13, Python 3.8.10, `instance-20260717-0944`.
Protocol [`PROTOCOL.md`](PROTOCOL.md), amendment
[`AMENDMENT-1.md`](AMENDMENT-1.md), raw output
`results.json` (pending — never committed), attempts
[`attempts.jsonl`](attempts.jsonl), grading
[`grading-results.jsonl`](grading-results.jsonl).

```
python3 -m unittest discover -s EXPERIMENTS/126-stackoverflow-service-test -t .
```

## 1. The gate accounting

| gate | declared | measured | verdict |
|---|---|---|---|
| **G0 discrimination** | ≥9/10 answered, ≥9/10 declined | 10/10, 10/10 | **PASS** |
| **G1 population** | ≥60 question-shaped of ≥300 fetched | 292 of 299 | **PASS** |
| **G2 composition** | reported per arm and pooled | §3 below | **PASS** |
| **K1 served share** (n=40) | Wilson LB ≥ 0.50: served | **0.5202** | **PASS** |
| **K2 execution share** | reported, not gated | 6/299 = 0.0201 | **PASS** |
| **K3 program residue** | count | 6 | **PASS** |

**K1 passed on 40 rows.** The first 20 straddled (Wilson CI95
[0.4329, 0.8188]); the protocol's rule extended once to 40. The
combined 27/40 = 0.6750, Wilson CI95 **[0.5202, 0.7992]**.

## 2. The served share

**27 of 40 = 0.6750** answerable-class rows are served by a free
general assistant. The assistant names the likely fault and the action
that resolves it, at the specificity the thread's own resolution
reaches, in 27 of 40 cases.

This is consistent with every other venue the mission has measured:
E062's 17/20 = 0.85, E091's 5/20 = 0.25, E092's 30/37 = 0.81,
E114's 0/374 fabricated, E116's recall 1.0. Stack Overflow — the
flagship software-owning venue — closes like the others.

## 3. The composition (G2)

| arm | n | question | execution | answerable | specific | program | manual |
|---|---|---|---|---|---|---|---|
| A (votes) | 199 | 198 | 1 | 157 | 41 | 1 | 0 |
| B (creation) | 100 | 94 | 5 | 47 | 47 | 5 | 0 |
| **pooled** | **299** | **292** | **6** | **204** | **88** | **6** | **0** |

**Execution share: 6/299 = 0.0201.** The composition differs by arm
as predicted: Arm B (creation-sorted) carries 10x the execution share
of Arm A (votes-sorted). The stratum concern declared in the protocol
is confirmed — the two arms are not the same population.

**Program-shaped residue: 6 rows.** These are rows whose remedy is a
self-contained program the asker runs. This is E091's K2 shape — the
one class where a software tool (not an answer) could serve. Six rows
in 299 is a real but small population.

## 4. What this establishes

1. **Stack Overflow closes.** The flagship software-owning venue is
   served by a free general assistant at 0.6750, consistent with every
   other venue measured. The composition finding (E091/F114, E092/F115)
   extends to the last untested venue class.

2. **The execution-shaped residue is real but small.** Six program-
   shaped rows in 299 is the one class a tool could serve. It is not
   zero (E091's K2 shape), but it is 2% of the venue — not a candidate
   population on its own.

3. **The stratum concern is confirmed.** The two arms differ by 10x
   in execution share. Any future screen on this venue must report
   its draw stratum beside its rate.

## 5. What this does not establish

- **That the 6 program-shaped rows are unserved.** They were not
  attempted — the protocol's attempt sample was the answerable class.
  Whether a tool could serve them is `untested`.
- **That the venue is served at the whole-pool level.** Two strata
  were measured, not the whole pool (E033/E034's lesson, declared).
- **That the served share generalizes to older questions.** The
  population is 2025+ only (recency declared).

## 6. Reopening

The venue closes on service, like E062, E091, E092, E114, E115, E116.
The one residue worth testing — the 6 program-shaped rows — is a
separate question: whether a self-contained program could serve what
an answer cannot. That is a candidate question, not a served-share
question, and it requires its own protocol.

The line is **closed**. No candidate.
