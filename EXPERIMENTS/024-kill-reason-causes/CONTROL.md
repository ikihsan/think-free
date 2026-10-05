<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# 024 — the control, run first, and what it found

`observed` 2026-10-05, T-0068. Run **before** any row of the treatment
population was classified. The clause under test is in `PROTOCOL.md`; the
replacement control and the disclosure that bounds it are below.

## The clause as declared

[`PROTOCOL.md`](PROTOCOL.md) named one control: run the same rule over
`EXPERIMENTS/012-candidate-harvest/raw/screened.jsonl`, whose 50 rows carry
F029's own cause table, and pass only on an exact four-category match.

## It fails, for a reason that is not the rule's fault

| F029's cause | rows | a home among the declared categories? |
|---|---|---|
| `prior_art` | 19 | yes |
| `vague` — states no mechanism | 15 | **no** |
| `not_a_software_need` | 12 | **no** |
| `needs_hardware` | 4 | **no** |

**31 of 50 rows cannot be assigned at all**, so an exact four-way match is not
merely unmet, it is unreachable.

The reason is that the two populations sit at different pipeline stages. E029
screened 50 harvested *sentences* for *"is this a buildable software need at
all?"* — a quarter were not software needs, and those never became candidates,
so no kill reason was ever attributed to them. The treatment population is
*candidates that were promoted*, each already past that question. **The declared
control tested the rule on rows it was never written to classify**, and 31 of 50
fail for a reason unrelated to its judgement.

This is a control with no way to express a negative result — the same defect
class as E021's unusable H2 band and F039's controls that returned 0 for
everything. Here it fails in the opposite direction: the control had no way to
express rows that are not kills.

**A first repair was attempted and rejected.** Mapping F029's four causes onto
the rule's categories (`vague`/`not_a_software_need`/`needs_hardware` →
`never_a_candidate`) makes the comparison well posed and yields a **perfect
19/19 agreement with zero errors** — and a control that cannot fail is not a
control. It was discarded. The mapping and the mapped rows were not kept.

## The control that replaces it

**`EXPERIMENTS/016-prior-art-adjudication/raw/attributions.jsonl`** — E016's
per-item verdicts, from a *different instrument at a different time*, one row
per prior-art clause with the deciding text recorded. Its `verdict` field is
exactly the binary the rule claims to make: `prior_art` versus
`no_prior_art_found`.

The 13 adjudicable judgement kills carry:

| E016's verdict | rows |
|---|---|
| `served` (prior art found) | 8 |
| `contested_counted_as_served` | 1 |
| `no_prior_art_found` | 3 |
| `unadjudicable_for_clause_served_for_reason` | 1 — excluded, as E016 did |

Every one of the 13 was `prior_art`-killed by F029, so this population is a
**hard** test: if the rule simply reads a cause column, all 13 come out
`prior_art` and it scores 9 of 12 correct with **three false positives** — the
exact error F035 documented. If it reads the primary evidence, it can recover
the three.

This is the control the protocol should have named: same population, same label
semantics, **independently produced**, and with known errors in the reference
labels, so a pass means something.

## Disclosure, because the rule's author has seen the answers

This reader ran the control **after** reading `EXPERIMENTS/016`'s README and
results, which report 3 of 12. **The three items (7, 12, 16) and their verdicts
were known before the rule was applied to them.**

That weakens the control as evidence of independence and it is stated here
rather than buried. What survives the disclosure:

- The three false positives are **named in advance** by the reference labels, so
  the control's *outcome* is not a discovery — only whether this rule reproduces
  a known, already-published error pattern.
- It remains falsifiable in the useful direction: the rule is free to score
  **worse** than 9 of 12, and a rule that scored worse would show the hand-built
  categories do not track the evidence.
- It does **not** license any claim that the rule's judgements on the treatment
  population are independent. They are one reader, with the reference answers in
  context.

## Ceiling

Agreement with E016 is not correctness either. E016's own arm-1 control passed
6 of 6 and its arm-2 gate **landed exactly on its threshold with one row
deciding it**; F035 records that item 16's strict reading reverses to `served`
under the stricter-counting alternative. A rule that matches E016 exactly is
reproducing judgements made at a declared knife-edge, not recovering truth.

**And the decisive limit is the one E023 already measured on this mission's
labels: one reader, no second coder.** This experiment's control bounds whether
the rule tracks an external label set. It does not bound whether this reader's
judgements on the twenty treatment rows are right.