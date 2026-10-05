# E029 reader rubric

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

Written 2026-10-05, before either reader saw a pair. Both readers get this file
verbatim.

## What you are shown

Exactly two things, and nothing else:

```
NEED
<the person's own words, verbatim, as they posted it>

SHIPPED
<title: <Show HN title>>
<url: <url if the index had one>>
```

You are **not** shown the person's name, the story the need was posted in, the
thread, any reply, or any other need. Several pairs come from different people and
different threads. **Nothing tells you which of two kinds of pair you are looking
at**, and you are not to try to work that out.

## What to decide

One label for the pair. Choose exactly one.

### `addresses`

The shipped item plausibly **does the thing the need says is missing.**

Test it by naming the capability and the artifact. Write:

- the **capability** the need asks for, in a few words, and
- the **what the shipped item is**, in a few words, and
- whether those are **the same job**.

They are the same job if a person who wanted this need would plausibly point at
this shipped item as the answer, or would find it on the list of things to look at.

### `unrelated`

The shipped item's subject **is not** the need's subject. Different job, different
domain, or a different problem entirely.

### `unclear`

You cannot call it. Use it when:

- the need is too thin — it says something is missing without saying what;
- the shipped title is too thin to tell what the thing is;
- the two are adjacent but you cannot tell whether they are the same job;
- the shipped item is generic infrastructure (a library, a language, a framework, a
  database, a web server) **and** the need does not name a specific use of it.

That last clause matters. Most `Show HN` items are generic infrastructure. "A
Postgres driver" is not the answer to "I need something to reconcile two CSV files
where the columns are in different orders".

## What not to do

- **Do not judge quality.** A terrible implementation that does the job is
  `addresses`. You cannot see the code and are not asked to.
- **Do not judge popularity.** Points, comment counts and stars are not shown, and
  would not matter if they were.
- **Do not require the need to be phrased as a request.** Many of these are a
  complaint, a question, or a description of a workaround. Read for **what is
  missing**, not for the grammatical mood.
- **Do not infer that a related-looking pair is the point of the experiment.** Some
  pairs are unrelated on purpose.

## Worked examples

**Need:** "Is there a Python library that uses Markdown or another lightweight
markup language for TUIs?"
**Shipped:** `Show HN: Rich – A Python library for rich text and beautiful
formatting in the terminal`
→ **`addresses`.** The need asks for markup-formatted terminal UI; Rich is a
terminal formatting library. Same job.

**Need:** "does anyone know a tool that lets you do a partial commit in git without
staging each hunk?"
**Shipped:** `Show HN: A Git client for Android`
→ **`unrelated`.** Git is shared vocabulary; the jobs are not.

**Need:** "nobody has built a thing that does X, I'd pay for it"
**Shipped:** `Show HN: A faster JSON parser in Rust`
→ **`unclear`.** "X" is not recoverable from the text, so you cannot compare.

## Output

One line per row, `row_id<TAB>label<TAB>capability<TAB>what_it_is`, in the row order
given. `row_id` is copied from the input and nothing else is changed.

Label distribution matters less than the individual calls. Two readers will disagree;
that is measured (gate A3) rather than reconciled away. Do not try to guess the other
reader's answer.
