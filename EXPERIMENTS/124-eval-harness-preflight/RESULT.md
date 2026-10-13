<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E124 RESULT — the rate is withheld on four of six committed harnesses, and one declared gate failed

Run 2026-10-13 on `instance-20260717-0947`, Python 3.8.10. Protocol
[`PROTOCOL.md`](PROTOCOL.md), amendment [`AMENDMENT-1.md`](AMENDMENT-1.md),
raw output [`results.json`](results.json), instrument in [`preflight/`](preflight),
tests [`test_preflight.py`](test_preflight.py) — **16 tests, all passing**, every one of
which tries to make the tool say `OK` when it should not.

```
python3 run.py                      # the six cases below
python3 -m unittest test_preflight  # 16 tests
```

## What was built

`preflight` — 4 modules, standard library only, no model calls, no domain
knowledge. It measures three properties of an evaluation harness and withholds
the headline rate when one of them fails (exit 3, reason printed):

| check | measures | verdict that withholds |
|---|---|---|
| C1 concordance | whether the key's ids and the output's ids are the same entities | `SILENT_NO_MATCH`, `NO_DISCRIMINATING_PAIRING` |
| C2 alternate-form FP | the rate at which a flagger condemns items known to be right, per arm | `ALTERNATE_FORM_FP` |
| C3 control arm | whether a declared negative arm is negative, by evidence the key does not use | `CONTROL_NOT_EMPTY` |

The caller supplies rows, labels and predicates. A rate is obtainable only via
`--anyway`, which prints it *and says the instrument checks failed*.

## What the run found, on committed harnesses

| case | harness | verdict | measurement |
|---|---|---|---|
| A | E116 scorer, committed integer key ids | **fires** `SILENT_NO_MATCH` | 0/80, Wilson [0.0000, 0.0458]; shared field `account_id` is `int` on one side, `str` on the other |
| B | same key, composed ids (`score.py`'s repair) | silent | 80/80 |
| C | E114 verifier, verbatim values in a bare sentence | **fires** — *declared silent* | **100/107 = 0.9346**, Wilson lower 0.8711 |
| C' | E114 verifier, the reader's own values in the reader's own prose | fires | **65/330 = 0.1970**, Wilson lower 0.1577 |
| D | E114 verifier, the 24 hand-verified-present values, bare sentence | fires | **16/24 = 0.6667**, Wilson lower 0.4671 |
| E | E116 `G0_C_precision` control arm | fires `CONTROL_NOT_EMPTY` | **4/20 = 0.2000**, Wilson [0.0807, 0.4160] |

**Baseline, side by side.** On all four firing cases the harness's own declared
gates were green or printed a clean-looking number: E114 reported
`instruments_valid: true` with `KG-C1` recall 1.0000 and `KG-C2` 0.0069; E116
printed TP/FP/FN per account and `recall 1.0000`. Every one of them was wrong
about its own instrument, and every one of them is now caught by a command that
reads files the harness already had.

## The declared gate accounting, including the failure

| gate | declared | observed | verdict |
|---|---|---|---|
| K1 sensitivity | ≥ 4 of 5 declared verdicts | A, B, D, E as declared; **C not** | **PASS 4/5** |
| K2 discrimination | C silent **and** D's FP ≥ C's + 0.40 | C fires; D 0.6667 < 0.9346 + 0.40 | **FAIL as declared** |
| K3 generality | 4 injected defects caught on a sound fixture, fixture clean | 4/4 caught, fixture clean, exit 3 on each | **PASS** |
| K4 the refusal | exit 3 on A, C, D, E; exit 0 on B | as declared | **PASS** |

K2 failed because its premise was wrong, not because the instrument failed to
discriminate. K2 assumed the easy arm would measure ≈0.02 and the alternate-form
arm ≈0.9. The easy arm measured 0.9346. **The gate is recorded as failed**; the
substitute reading is stated below and is weaker than the one the protocol
wanted: nothing in this run establishes an arm on which *this* verifier is
demonstrably sound.

## The finding: a false-positive rate belongs to an arm, not to an instrument

One verifier, four arms, one instrument:

| arm | host text | false-positive rate |
|---|---|---|
| E114's own `KG-C2` control | the reader's prose, value in situ | **0.0069** (1/145) |
| C' | the reader's prose, value in situ, label by string search | **0.1970** (65/330) |
| D | a bare sentence naming the value | **0.6667** (16/24) |
| D, in situ | the reader's own prose (committed verdicts) | **1.0000** (24/24) |
| C | a bare sentence naming a value copied from the document | **0.9346** (100/107) |

Two things follow, and the second is the one that matters for anyone building a
verifier:

1. **F118's rule is necessary and not sufficient.** "Include the case where the
   subject is right and the form is different" caught the alternate-surface-form
   case. C found a further axis: `judge()` scores *context-word overlap*, so a
   value presented in a sentence with no content words in common with the
   document scores near zero **whether or not it is present**, and is condemned
   as `ungrounded_claim` — 100 of 107 in case C, none of them `ungrounded_value`.
2. **A quoted false-positive rate does not transfer.** E114's 0.0069 is a true
   measurement and does not qualify this verifier for any arm but its own. The
   rule that follows: *an instrument's false-positive rate is a property of the
   pair (instrument, arm); quote it with the arm, or quote nothing.*

This is the same shape as F114 — "unserved share is a property of what a
community owns" — and as F116: a comparison across unlike arms is not a
measurement of either.

## The candidate question, and the prior-art answer

[`PRIOR-ART.md`](PRIOR-ART.md) searched for all three checks in the users'
vocabulary, the academic term and the infrastructure term. Verdict:
**`partially-covered`**. No tool performs all three, none automates C3, and the
most relevant practitioner document — Anthropic's "Demystifying evals for AI
agents" — already tells practitioners to author a reference solution that passes
every grader (C2) and to build balanced problem sets (C3), in prose, by hand,
with no measurement and no gate. `dblect` has a static join-key-type rule for
SQL; `gameonc/eval-harness` refuses to report on a sample-size gate; JudgeBench
measures judges on its own published labels.

So the claim available is narrow and it is the one that matters: **the three
checks are known advice; measuring them, bounding them with an interval, and
failing closed on them in one stdlib-only command is not something this search
found in use.** Two honest caveats: the search tooling degraded badly (rate
limits, CAPTCHAs), and two plausible artifacts — Meta's EvalEval toolkit and
Inspect AI's `metac_eval` — could not be located or refuted, which is a search
failure, not evidence of absence.

## Two corrections this run makes to the record, and one thing it does not

- **C' does not contradict F118's "0 of 374 fabricated".** Its independent label
  is a plain string search of the document, which found 330/374; the remaining 44
  are normalisation gaps in *my* search (a date written `Oct. 9` against a label
  of `October 9, 2026`), not fabrications. The verifier condemned only 6 of those
  44 — it is less trigger-happy than a naive substring search, which is the
  expected direction. The headline claim is untouched.
- **E is a re-derivation, not a discovery.** 4 of 20 C accounts carry a
  `"monthly ... identical amount"` pattern in the reader's own prose while the key
  calls them negative — the count F122 reported, arrived at from committed files
  by a declared regex. It confirms the finding is reproducible from the artifacts
  alone, which is all it is evidence of.
- **Not established:** that any of this generalises past two harnesses in one
  repository, and not that the tool is useful to anyone outside it. See
  [`PRIOR-ART.md`](PRIOR-ART.md).

## What this changes as a build decision

The mission's own screening instruments are the only population measured here,
and they failed silently three times in three days (F118, F121, F122). The
change: **before this repository reports a rate over generated output again, the
harness is expected to answer the same three questions**, and a result whose
instrument did not is `withheld`, not `served`. That is a process obligation with
a tool behind it, and it is the smallest thing that would have prevented all
three losses.

Whether the tool is a *candidate* — something a person outside this repository
would install — is not decided by any gate above. K1 through K4 only say it works
on five cases from one repository and on fixtures designed to break it.