<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

# E028 — protocol amendment 2

Written 2026-10-05, **before either reader ran and before any label exists**.
Amendment 1 made the instrument runnable; this one bounds what a reader is
shown, because a full bundle is larger than a reader context and an unbounded
bundle would silently become whichever artifacts the reader happened to open.
Both bounds are therefore declared here rather than discovered during the run.

## 4. A reader sees at most four artifacts per row, and 1,800 characters of each

**Artifact cap: the first four artifacts in the order the screen recorded
them**, per row. E016's `artifacts` arrays are in the order its own probe
returned them, so the cap takes the four the screen listed first rather than an
arbitrary four chosen after the fact.

**Character cap: the first 1,800 characters of each stored capture**, and the
reader is told that the full capture is on disk with the path, and is permitted
to grep the full capture for the attribute's terms and to quote from anywhere in
it — recording the quote with the path so a later reader can find it.

**What the cap costs, declared.** The row label `serves` therefore means *at
least one of the four artifacts the screen listed first does what the attribute
asks*. An artifact the screen listed fifth could serve the clause and the row
would still read `does_not_serve`. This is a real weakening and it is a ceiling,
not a finding. The full set of 90 named artifacts and each one's fetch status is
published in `results.json`, so a reader can see exactly what was not shown.

## 5. Reader isolation, mechanically

Each reader is a separate context and is given, in this order and nothing else:

1. `RUBRIC.md` (this directory).
2. `raw/requirements.jsonl` for Step A — which contains the requirement text,
   the story title, the date and the trigger phrase, and **no verdict, no kill
   reason, no incumbent name, and no other reader's output**.
3. For Step B: its **own** Step A output, the fetch log, and the stored
   captures for its own bundles.

Neither reader is given `raw/record_facts.json`, `screened.jsonl`,
`attributions.jsonl`, or the other reader's file. The two readers are the same
model family, which MISSION.md records as **not independent human validation**;
κ measures their consistency with each other and nothing more.

## 6. Step A runs as its own pass for both readers, before either sees a document

The base protocol ordered Step A before Step B but did not say the passes were
separate. They are: **Step A is run for both readers, both files are committed,
and only then is Step B run.** The barrier is what makes "derived from the
requirement text alone" checkable from the repository rather than asserted — a
Step A file written after a reader has opened a README is indistinguishable from
one written before, unless the barrier is in the record.

## 7. The controls are run in the same passes, not after them

The mismatched pairings (amendment 1 §4) and the positive control row are
labelled by both readers inside their own Step B pass, from their own view
files, so no control is adjudicated by an instrument the real rows were not.

The positive control is `H03` (`webp-encode`), which E016 recorded as *"Served
beyond argument, on install counts as well as on existence"* — `sharp` at
436,835,441 downloads per month. It is a **control on the instrument**, and it is
drawn from the same population as the rows it controls, so a reader who cannot
recover it is measuring something else. Declared threshold, unchanged from the
base protocol: both readers must label it `serves`.

## Nothing else changes

Population, gates, falsifications and the decision map are as declared in
`PROTOCOL.md`. No gate is added, moved or relaxed here.