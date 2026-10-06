# E031 reader rubric

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

Declared 2026-10-05, written before any reader saw a row. Identical for every
arm and every reader; `verify_labels.py` checks the question block is
byte-identical across the three arm views.

## What you are looking at

One comment from a public technical discussion. You are told nothing about
where it came from, who wrote it, what it is about, or which group it is in.

## q1 — the missing-capability question

> **Does this comment state a capability that something the author relies on
> cannot do?**

Answer **yes** only when the comment says a thing lacks a capability, or says the
author could not do something with a thing they use or used. The capability is
named or paraphrased in the comment itself.

| answer | when |
|---|---|
| `yes` | a named or clearly described thing cannot do something, or the author hit a limit of it |
| `no` | the comment reports a fact, an opinion, a preference, a workaround, or a capability without asserting something lacks it |
| `unclear` | the text is truncated, garbled, or genuinely admits both readings |

Do **not** answer `yes` for a preference ("I prefer X over Y"), a pure
announcement, a workaround that already works, or a capability that exists.

## q2 — the clause, copied verbatim

Only when q1 is `yes`. Copy the **shortest phrase inside the comment** that
states the missing capability. Copy it exactly, including its original casing and
punctuation. Do not paraphrase, summarise, or repair the grammar. Do not include
the tool's name unless the name is inside the phrase you copy.

If q1 is `no` or `unclear`, write `-`.

## q3 — the successor question (planted separation check)

> **Does this comment name the thing the author moved to?**

`yes` when the comment names a specific other tool, service or artifact that the
author moved on to. `no` when it names nothing. `unclear` when the thing named is
not identifiable as an artifact.

## q4 — pair adjudication (recurrence stage only)

Two clauses are shown with their row ids and nothing else — no arm, no author, no
story, no artifact name.

> Do these two clauses state **the same missing capability**?

`same` when a builder reading both would be working on one task. `different` when
they are distinct tasks that happen to share vocabulary. `unclear` when you
cannot tell from the two phrases.

## Label file format

Tab-separated, three columns, **one row per view id, in the view's order**:

```
<id>	<q1>	<q2>
```

- `id` — exactly as printed in the view's `ID:` line, including its arm prefix.
- `q1` — `1`, `0`, or `u`.
- `q2` — the verbatim clause, or `-`.

The pair stage writes `raw/e031_pairs_labels.tsv`, tab-separated
`<pair_id>	<verdict>` where verdict is `same`, `different` or `u`.

A q2 phrase that is not a verbatim substring of its own row's text is rejected
before any rate is computed. This is the check that makes a printed clause
evidence rather than a paraphrase.