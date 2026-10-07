<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Decisions — screening candidates and judging experiments, part 11

Decisions **D072, D073, D074**. Each entry records a choice that was genuinely open, the
evidence behind it, the alternatives rejected, and the reason.

**Invariant:** the same as [`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md) —
every entry governs *what passes*: which candidates and experiments are screened
in or out, what a kill-gate condition may mean, and which metric a verdict is
taken on. How this repository's own gates are written and run belongs in
[`DECISIONS-GATING.md`](DECISIONS-GATING.md); recording and publishing in
[`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md). The index is
[`DECISIONS.md`](DECISIONS.md).

Split out of [`DECISIONS-SCREENING-9.md`](DECISIONS-SCREENING-9.md) on 2026-10-06,
which held D069 and D070 and had no room. All ten screening files carry the same
invariant, for the reason [`DECISIONS-SESSIONS.md`](DECISIONS-SESSIONS.md) had to
revert after T-0030: a narrower invariant is how two files' prose come to
contradict each other.

## D072 — A gate that has been failed by its own arithmetic is repaired as a rule, not as a fix

### The choice

E041 wrote `instrument.py` specifically because E040's G2 could not fire, and its
first version scored G1's ratio condition as

```python
c_ratio = rec_n0 > 0 and (rec_p / rec_n0) >= RATIO_BAR
```

On the completed run, arm **N0's recall was exactly 0.0** — not one of 77 matched
cross-repository controls reached the frozen tau of 0.05. So the guard turned "the
control arm has no instances" into **"the ratio condition failed"**, and G1 printed:

```
G1 met = False   conditions = {ratio: False, diff: False, ci: True}
paired_diff = 0.74026   ci95 = [0.636, 0.831]
```

**A paired difference of +0.74 with a CI95 of [0.64, 0.83] printed as a failure**,
and the condition that failed was the one that could not be computed. The absolute
difference was false only because it carried the same guard.

The open choice was what to do with it.

**Three options were available.** Leave the evaluation and explain the discrepancy
in prose. Recalibrate the gate on a control arm with non-zero recall. Or **treat a
zero denominator as a distinct state and repair the rule that omitted it.**

**The third was taken.**

### Why this is F067 again, and why that matters more than the bug

F067 is this repository's recorded instance of *"a zero-denominator control arm
scored as a failed bar, so a strongly positive result printed `not met`"* — one of
E040's three self-inflicted errors. **The same defect, in the same family, was
written into the code produced specifically to avoid repeating E040's mistakes.**
E041's `PROTOCOL.md` opens by naming F064 and F066 as the reason the experiment
exists, and F061's third answer is quoted in its own integrity requirements.

**That is the generalisation worth recording, and it is not about the guard.** A
defect does not stop reproducing because the run that found it has been diagnosed.
What stops it is **a rule the implementation is obliged to satisfy**, and a lesson
the implementer is expected to remember does not survive being read in a different
file by a different writer six hours later.

So the repair is a **rule**, in three parts:

1. A ratio with a zero denominator is **`not_evaluated`**, never `False`.
2. **An absolute difference carries no existence guard.** It is a subtraction of
   two measured rates and is defined whenever both rates exist. It was suppressed
   here only because the guard suppressed it.
3. A gate reports **`met_on_evaluated_conditions`** alongside `met`, so a reader
   sees which conditions were computed and which were not, rather than one boolean
   conflating "failed" with "could not be evaluated".

**Every bar is unchanged**: 1.5, 0.20, 0.50, 0.50, exactly as `PROTOCOL.md`
declared them. Only the evaluation of an undefined quantity changed.

### The rule this establishes

**A gate reports three states — `met`, `not met`, `not_evaluated` — and any
evaluation of a ratio must branch on its denominator rather than treat it as
arithmetic that always exists.** `docs/policy/gate-falsification.md` already
carries the three-state requirement for *gates in this repository*; this extends it
to **the evaluation code of an experiment's own arms**, which is where F061's third
answer keeps failing to arrive.

**Where a numeric answer is undefined, the honest reading is a third state and the
gate is reported as unevaluable alongside what *was* computable.** Not `False`, and
not a silently dropped condition.

### What it does not decide

It does not make G1 pass, and it rescues nothing. Read correctly, G1 on this
population is *"the instrument separates judged repeats from matched controls by
+0.74 [+0.64, +0.83] at the operating point where the control is silent; the ratio
form of that statement is not evaluable"* — **a positive result about the loose
control**, sitting beside **G2's failure** at 0.403 and 0.143 against a bar of 0.50.
**The verdict is `failed G2` either way.** This decision changes a label on one
sub-condition and nothing about the outcome.

## D073 — Item 0f closes on its premise's arithmetic, and the repair is not a bigger harvest

### The choice

Item 0f was this mission's **ranked top action**: build a needs index over a
**second public venue**, on the reasoning that recognition is *"thin only because
1391 rows is a small population"*, that recognition is a rate over a population, and
therefore that **whether it scales is arithmetic before it is anything else**.

E041 measured the arithmetic first, from captured bytes, with no new fetch, before
spending any of the second venue's cost. It found **`alpha = 0.971`, CI95 [0.632,
1.717]**: resolution grows at very close to **linear** rate in corpus size, and
**S2's bar (`alpha ≥ 1.0` with the CI's lower bound above 0.75) is not met**.

The open choice was what to record against item 0f.

**Three options were available.** Re-derive a second venue's harvest on the
expectation that a bigger population eventually reaches the bar of 20. Reject the
premise and leave item 0f standing pending a better instrument. Or **close the
item, on the premise's own arithmetic, and record the number that closes it.**

**The third was taken.**

### Why the arithmetic closes it rather than merely weakening it

At `alpha ≈ 1`, reaching 20 qualifying clusters from 8 needs **`n ≈ 3,500`** — a
2.5× corpus, not a second venue's worth of work. **And every stricter threshold is
worse**, not better: `alpha` falls to 0.346 at tau=0.20 and 0.111 at tau=0.25, because
higher thresholds leave 1 cluster to extrapolate from. **A stricter instrument does
not buy resolution**, which is the opposite of the intuition the item rested on.

Two further measured facts close it independently:

- **The control arm is not silent.** Arm B — the matched near-miss comments — yields
  **4 qualifying clusters at full size at tau=0.15**, against arm A's 8. The bar is
  being measured against a population where **half the headline number is matched by
  its own control**, and growing the corpus grows both.
- **The instrument cannot support the index anyway.** On 77 real practitioner-judged
  duplicate pairs, both members present in a 44,669-row corpus, the judged partner
  is the single most similar row in **0.390** of cases on titles and **0.143** with
  body text, against a bar of 0.50, and **0 of 14** when the pair's titles share no
  content term. Median partner rank is **10th of 44,669**.

### The rule this establishes

**A candidate that proposes to scale a measured quantity must be checked against the
measured growth exponent of that quantity before any of the scaling cost is
incurred, and the check is worth more than the harvest it may replace.** Item 0f
said its own scale question was *"arithmetic before it is anything else"*; it was,
it took 20 minutes and no new fetch, and it answered the question against the item.

**A linear exponent is not a rescue.** `alpha ≈ 1` means the corpus size needed grows
in proportion to the bar, and a bar that the *control* arm also approaches at a
similar rate is not reachable by corpus size at all. **Before accepting "we need more
data", measure the rate at which the data helps and the rate at which the control
helps too.**

### What it does not decide

It does not name a candidate and it does not validate one; the seat remains empty,
now for a measured reason rather than an audited one. It does not close **a needs
index built on a different instrument** — embeddings, a domain model, or human
review of a shortlist are different instruments and this run says nothing about
them. **What it closes is the item as written**: a lexical TF-IDF clustering of one
1,391-row corpus scaled by harvesting another venue.

It also does not reopen E040. E040's G4 (`8 against a bar of 20`) stands, and this
run **confirms its G1 positively for the first time** — needs separate from their
matched controls at 3.9× at tau=0.15 and 27.2× at tau=0.20. That separation is real.
**It is also much weaker than "this is the same need"**, which is what a needs index
would need, and the distance between those two is the whole of what D072's finding
measures.

### Related

D069 governs the restatement of a threshold-dependent gate when its calibration arm
is unusable, and D072 is that rule applied to E041's own gate code. D067 requires a
candidate's mechanism to be tested against its mechanism's existing source first;
D073 is the same rule applied to a candidate's *premise* — and it is the second time
in this record it has paid, after F066 closed six requests' worth of work by reading
the mechanism's availability first.

## D074 — A candidate's surviving claim must meet the caller it names, and the arm must be checked to be exercising it

`observed` 2026-10-07, session 2026-10-07-001. Evidence:
[`EXPERIMENTS/043-real-agent-staging/`](EXPERIMENTS/043-real-agent-staging/README.md);
F075.

### The choice that was open

`stg` had lost its mechanism three times over and kept a life on one claim: the
differentiation is *packaging* — a caller writes 1 line instead of ~180. E040,
E041 and E042 each measured that claim and each agreed, and none of them had run
it against a caller. E042's design document says it simulated the agent, and the
~180 figure descends from a baseline written by someone who had already read
`stg`'s selector. The choice was whether a candidate whose only surviving claim
rests on a simulated population may be called validated, or whether the caller
has to run first.

**It may not, and the caller runs first.** Six real agents on six real
repositories: 6 of 6 exact, 3 of 3 with no tool at all, 2 of 3 declining to use
`stg` when it was installed. The claim did not survive contact with the
population it was about.

### The rule, which is two rules

**First: when a candidate's justification names a caller, that caller is an arm
that runs before the candidate is called validated.** Not a route, not a script,
not a reimplementation of the mechanism — the caller. `stg` spent three
experiments being compared against artifacts this repository wrote, which is why
three experiments agreed: they shared a premise rather than testing it. The
premise was cheap to test — an afternoon and six runs — and was testable from the
first day the claim was made.

**Second, and this is the part that bit: an arm is not evidence unless it was
observed to exercise the thing under test.** The `stg` arm shipped a tool that
was not on `PATH`; all three agents reported `command not found`, the arm was a
second control arm, **and the run still scored 6 of 6 — a clean result that
would have been recorded as confirmation of the candidate.** F073 is the same
shape (an arm producing a clean table because it was not running the thing
under test) and the first time here that a control failed *open* rather than
producing a visible zero. So the harness now refuses to emit a trial unless the
tool resolves, and the general form is: **an arm that cannot fail is not a
control, and the check that it can is part of building it.**

### Why not the alternative

Keeping the simulated agent and recording its ceiling would have been cheaper and
defensible. It was rejected because **a simulated caller is a reimplementation of
the caller's reasoning, written by the party that wants the claim to hold** — the
same defect as the ~180-line baseline, one level up. Where a population is
reachable, reaching it beats modelling it; where it is not, that is a finding
about access and should be written as one.

### What it does not decide

It does not claim agents never need `stg`. Six runs, one model, one session,
synthetic Python, line numbers supplied, and `git diff` available to every agent
— the population where a line-addressed interface could still pay is an agent
that must *discover* which line changed without diff access, and that is untested.
It does not release or retire `stg`, which remains a correct tool (30/30 on E038,
byte-identical index). It does not change what this repository selects candidates
on; it changes when a candidate's last remaining claim has to be run.
