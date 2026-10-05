# E030 — Amendment 8

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Dated 2026-10-05, after the pair-level run and after reading the mutual groups,
and before the permutation control was run.** It withdraws B1's verdict and adds
the one gate that could have caught this.

## 1. B1 "fired" on an instrument that does not read the property

The pair-level run, from `raw/recurrence.json`:

| arm | pairs | accounts with a partner | `R_pair` | CI95 |
|---|---|---|---|---|
| treatment (declared) | 449 | 321 / 919 | **0.3493** | [0.3192, 0.3807] |
| control | 451 | 579 / 2 687 | **0.2155** | [0.2003, 0.2314] |
| treatment (matched rule) | 466 | 339 / 919 | 0.3689 | [0.3383, 0.4006] |

difference **0.1338, CI95 [0.0997, 0.1687]** — over the declared 0.10, excluding
zero, no overlap, 33 multi-artifact mutual groups of ≥ 3. **Every declared
condition for B1 was met.** And the mutual groups the statistic produced are
printed in `raw/mutual_treatment.jsonl`, and they are not clauses:

```
size=4  shared tokens: abandon absolute attempt automatically aware awkward bank
  ragequittah | Opnsense | I'll never understand this attitude. Recently I set up a full network...
  jasode     | IBM      | but a pure Linux mainframe is surprisingly competitive not just in compute...
  shevy-java | PHP      | So I had to take a look around to remind myself what Ruby and Ruby on Rails...
  sethammons | Go       | Having been at a several places that have gone from framework-makes-us-fast...
```

Four unrelated comments, one about a firewall, one about mainframes, one about
Ruby, one about Go frameworks. They share `absolute`, `aware`, `attempt`,
`abandon`. A second group links a Ruby comment, an Angular comment, a SQLite
comment and a C comment through `abandon`, `absolute`, `allocation`, `apis`,
`aside`.

**These are ordinary English words of length ≥ 4 that happen to occur in ≤ 5
accounts of a 919-account arm.** With ~8 500 rare tokens spread over 919 long
comments, two unrelated comments sharing two of them is the expected event, not a
shared clause. The statistic is measuring **coincidence**, and its arms differ
partly because the treatment arm's comments are **longer** (median 90 words against
74) and its common-token cutoff is `2% of 919 = 18` against `2% of 2 687 = 54`, so
it keeps proportionally more rare tokens per account.

## 2. B1's verdict is withdrawn

`R_pair` **does not measure clause recurrence**, so a difference in it is not a
difference in recurrence. H1's status is **`not_evaluated`**: not *"the clauses do
not recur"* — nothing here can say that — and not *"they do"*.

This is `docs/policy/gate-falsification.md` applied to a gate that passed: a gate
is trusted when it reads the property it claims to check, and this one was
falsified against its own bytes by printing its own output. No B verdict from this
experiment stands.

## 3. A9, the gate that would have caught it, declared now and run once

**A9 — is `R_pair` above chance at all?** The identical pipeline, run on
**signatures permuted across accounts within the same arm**: each account keeps
its signature's *size* and every token's *arm-level frequency*, but the token no
longer belongs to the account that wrote it. Everything the statistic depends on
except the token-to-account association is held fixed. **50 permutations, seed
3008.** The matched variant runs on the control arm too.

**Gate: the observed `R_pair`'s CI95 lower bound exceeds the permutation mean's
CI95 upper bound, in the treatment arm.**

- **A9 fires** → the statistic carries signal, B1 may be read, and the experiment
  continues.
- **A9 fails** → the statistic is at or below chance, the verdict is
  `not_evaluated` for the third and final time, and the finding is about the
  instrument rather than about the world.

**Declared after the diagnostic, which is the only honest ordering available**, and
that is exactly why it is a *null* control rather than another threshold: a null
cannot be tuned towards a result, and its failure is the informative outcome.
`AMENDMENT-7`'s "the linking tokens are printed so the linkage can be read rather
than trusted" is the instruction that found this; the printout *is* the falsifier,
and A9 is the version of it that runs without a reader.

## 4. Also reported, feeding no gate

- **A length-matched subsample.** The treatment and control arms are re-sampled to
  the same text-length distribution (deciles of stripped word count, seeded) and
  `R_pair` recomputed. If the difference shrinks toward nothing when length is
  held fixed, the between-arm difference was length.
- **The mean rare-signature size per account in each arm**, which is the mechanism
  the length account predicts.
