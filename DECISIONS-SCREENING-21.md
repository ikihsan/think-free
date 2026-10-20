<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# Screening decisions, part 21

Split out of [`DECISIONS-SCREENING-20.md`](DECISIONS-SCREENING-20.md), which held
D107-D109. This part holds the decision taken when the scoring pass of an
already-predeclared run returns a number that is wrong twice before it is right.

Decisions **D124**. Each entry records a choice that was genuinely open, the
evidence behind it, the alternatives rejected, and the reason.

**Invariant:** the same as [`DECISIONS-SCREENING-12.md`](DECISIONS-SCREENING-12.md)
- a decision belongs to the file whose subject it is, the number is allocated
with `origin id next D` against the base, and the heading, `DECISIONS.md`'s row
and this file's own `Decisions **...**` header all move together.


**Identifier note (2026-10-20 lineage merge):** `E140` and `E141` in this file mean
`EXPERIMENTS/140-judge-form-invariance/` and `EXPERIMENTS/141-valueset-second-genre/`.
The upstream lineage carried two further directories under those numbers, so an
unqualified `E140`/`E141` is disambiguated by directory name from here on.

---

## D124 — a detection rate counts the items where the defect was actually introduced, and it is measured by pairing

**Decided 2026-10-14**, on E140's own scoring pass, which got both halves wrong
before it got them right. Evidence:
[`EXPERIMENTS/140-judge-form-invariance/`](EXPERIMENTS/140-judge-form-invariance/RESULT.md),
AMENDMENT-4 §1, `gates.json`, F144.

**Rule 1 — the denominator of a detection rate is the arm items in which the
builder actually introduced the defect.** An item where introduction was
impossible is `not_evaluated`, never a miss. K1 was declared on the *value* and
first scored on the *item*, dividing by 15 and returning 0.7333 — a fail. Four
of the fifteen corrupted rows carry no extractable value, so the corrupter had
nothing to replace, `C = V`, and there was no corruption to detect. On the
declared unit: **11/11 = 1.0000**.

**Rule 2 — the exclusion must be checkable from the arm file before any
instrument runs.** This is the part that keeps Rule 1 from being a licence. The
four items are identifiable from `arms.jsonl` alone, and `build_arms.py` had
already recorded them in its own drop report at arm-construction time. If the
session had not inspected the result afterwards, the same denominator would have
been correct — what changed is that this session looked, not what the gate
wanted. **A denominator repaired after measurement is reported as two numbers
and both are published.** `gates.json` carries `observed` and
`observed_if_degenerate_items_counted`.

### Alternatives rejected

- **Keep 0.7333 and report the line as failing.** Rejected: the gate was
  declared on the value, and four rows where the defect cannot exist measure a
  population the gate was never written about. This is D072's rule — a ratio
  over a population that cannot carry the event is `not_evaluated`, not `False`
  — applied one level up, from a zero denominator to a *degenerate* item.
- **Add an eighth corrupted item to restore a previously written denominator.**
  Rejected: choosing which extra item, and wanting an extra item at all, would
  both be decided after seeing a shortfall and before seeing any outcome. A
  weaker gate is better than a gate tuned to hit a number written before the
  subset rule was run.

### Rule 3 — an instrument's detection rate is measured by pairing each flag to
the defect that was introduced, never by differencing aggregate counts

M1's aggregate `ungrounded_value` counts differ by 6 between the corrupted and
verbatim arms; the paired question — *was the swapped value itself the flagged
one?* — gives **9 of 11**. The aggregate difference is a bound on the wrong
quantity and would have been published as this experiment's headline detection
number had the pair test not been run. The pairing is cheap and the aggregate is
available first, which is exactly why the rule has to be written down.

**Ceiling.** This rule governs *rates produced by this repository's own
instruments on this repository's own arms*. It says nothing about a third-party
instrument whose internals expose no per-instance verdict, where pairing is not
available and the aggregate remains the only number available — such a rate is
then reported as a bound, and named as one.

**Bears on** F123 (a rate belongs to an arm), F118 (a control must include the
case where the subject is right and the form is different), D072 (zero
denominator), and the next action on E140's candidate artifact, whose gate
denominators will be set on a second genre.
