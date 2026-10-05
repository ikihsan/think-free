<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

# E028 — reader rubric

Given to both readers, unchanged, before either ran. The labels are the whole
measurement, so their definitions are here rather than in either reader's head.

## What you are doing

You will read short statements in which a person wrote down something they
wanted, and decide **whether an existing product already does the part that
mattered**. You are not deciding whether the want was reasonable, whether a new
product would be a good idea, or whether the person should have solved it
differently. Those judgements are not the measurement and mixing them in makes
the number mean nothing.

## Step A — from the requirement text alone

For each row, write four fields. **Do this before looking at any product.**

| field | what to write |
|---|---|
| `category` | one noun phrase: what *kind of thing* is being asked for |
| `attribute` | one sentence: the property this particular want has that an ordinary product of that category would **not** have |
| `attribute_stated` | `yes` if the requirement says so itself; `inferred` if you had to read it off what it complains about; `none` if there is no such property |
| `attribute_note` | the words in the requirement that carry the attribute, quoted |

**The test for `attribute`:** someone could hold up two products of the same
`category` and ask which one this person was asking for. If both would do, there
is no distinguishing attribute — write `attribute` as `no_distinguishing_attribute`
and set `attribute_stated` to `none`. That is a real and reportable answer, not a
failure to answer.

**Write no products, no brand names and no guesses about what exists.** Step A is
about what was *asked for*. If you name a product here you have contaminated the
pass, and the reader who follows you will read the requirement through it.

## Step B — with the products' own documentation

For each row you are shown the requirement, your own Step A attribute, and for
each product its **own published documentation**, quoted from the file named
beside it. Decide one label for the row.

| label | meaning |
|---|---|
| `serves` | at least one product's own documentation says it does what the attribute asks |
| `partial` | a product does part of the attribute and the part it does is less than the attribute |
| `does_not_serve` | no product in the bundle does the attribute |
| `unreadable` | no product in the bundle has documentation you were given |

**`does_not_serve` is the interesting answer and the easy one to give wrongly.**
A product being in the right category is not `serves`. A product's
documentation describing its category, its feature *list*, its marketing, or its
general capability is **not** evidence for the attribute. If the documentation
never mentions the attribute or the thing the attribute is about, the answer is
`does_not_serve` — the documentation is the evidence, and its silence is the
evidence.

If the requirement's attribute is `no_distinguishing_attribute`, the row cannot
be fit-tested: label it `no_distinguishing_attribute` instead of the four
labels above, and say so in `note`.

### Fields you must also return

| field | what to write |
|---|---|
| `evidence` | one or more quotes, each `path :: quoted text`, copied from the file you were shown |
| `evidence_path` | the file you took the deciding quote from |
| `note` | one sentence, and it must distinguish *"the documentation is silent on the attribute"* from *"the documentation says the opposite"* |

**`note` must not be a paraphrase of your label.** Its job is to record what the
documentation did, so a later reader can disagree with your label for a stated
reason instead of re-doing the reading.

## Mismatched pairings

Some rows in your file carry a `mismatched_with` field. The product
documentation shown belongs to a **different** row's requirement. Judge it by the
same rubric and answer honestly. `does_not_serve` is almost always right, and
that is the point: a procedure that calls these `serves` is not measuring fit.
If a mismatched pairing genuinely does look served, label it as it looks and say
in `note` why — a real confusion is information, and hiding it destroys the
control.

## Output format

One JSON object per line, no commentary outside the JSON. Keys:

```
row, category, attribute, attribute_stated, attribute_note,   # Step A
row, label, evidence, evidence_path, note                     # Step B
```

`row` is the id you were given. Do not invent rows. Do not skip a row: if you
cannot judge one, return it with `label` of `unreadable` and a `note` saying
what stopped you.