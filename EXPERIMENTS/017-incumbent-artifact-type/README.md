# 017 — what does the prior-art screen's population actually contain?

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

**Date:** declared 2026-10-04, run 2026-10-05. **T-0061.** The classification
rules, both gates and the control's interpretation rule were written **before any
artifact type was read**, and the declaration survives in full in
[`PROTOCOL.md`](PROTOCOL.md). No network request was made for this experiment
before that file existed.

**Verdict: H1 is `dead`.** In the young vocabulary the prior-art screen's
population is **14 of 18 working code, not documents** — the hypothesis this
experiment was built to test is disproved, and by hand rather than by the rule's
own margins. F037.

**The hypothesis was not formed blind, and the leak is named.** I read the 48
repository *names* inside `EXPERIMENTS/015-incumbent-serving/results.json`
before writing the declaration, and four of them are named `…-guide`,
`…-showcase`, `…-system-prompts` and `…-references`. That is reconnaissance from
an artifact this repository already holds, and it is the only thing I looked at:
no artifact type, file listing, release count or serving figure for this
population was read before the gates were fixed.

## The question

F034 measured the prior-art screen's own premise — *a tool exists, therefore the
need is served* — and found it **holds 4 of 4 in mature vocabularies and 1 of 4
in a young one**. That result is consistent with two explanations the mission has
never separated:

- **(i)** young-vocabulary needs really are unserved, so the screen has been
  killing live candidates; or
- **(ii)** the screen's instruments cannot see young-vocabulary tools at all, so
  the 1-of-4 is the instrument talking rather than the world.

Neither is testable by measuring serving harder — F034 already found that in the
young arm **14 of 18 rows had no readable channel**, so more channels of the same
kind is what produced the ambiguity.

**A third possibility is visible in the population F034 already collected and has
never been tested.** A GitHub *phrase search* returns whatever matches the words,
and in a young vocabulary the things that match a need's words best are frequently
not software. `Piebald-AI/claude-code-system-prompts` (12,829★),
`diet103/claude-code-infrastructure-showcase` (10,035★),
`ChrisWiles/claude-code-showcase` (6,072★) and
`Cloudgeni-ai/infrastructure-agents-guide` (206★) are documents. If the
highest-starred match for a need is a **document**, then "prior art exists" is
satisfied by prose, the need is real and acknowledged at scale, and the screen is
not measuring competition — it is measuring the existence of writing.

This has a consequence the mission needs either way. The deferred owner decision
is *what to select candidates on*. One candidate answer is measurable without
users and is not a proxy: **is the procedure the field's best-known documents
teach still being done by hand, because nothing runs it?**

**The declaration is in [`PROTOCOL.md`](PROTOCOL.md)**, written 2026-10-04 before
any artifact type in this population was classified. In one paragraph: the
population is all **61 rows** of `EXPERIMENTS/015-incumbent-serving/results.json`
(30 mature, 18 young, 13 placebo), reused rather than re-searched so the two
experiments measure the same repositories; a row is `executable`, `document` or
`unreadable` **from its own root file listing and whether it has published a
release**, never from its name, description or topics, because those are the
fields the phrase query matched on; every row is also reviewed by hand into
`reviewed.json` so the rule's error rate and direction are visible; and the
declared gates are

* **H1** dead if `document` is ≤50% of the readable young arm, **or** if document
  rows clear a declared floor at the same rate executable rows do (within 10
  points). One firing condition is enough. An uncomputed condition does not fire.
* **H2** survives at ≥4 of the 10 highest-starred young-arm `document` rows being
  `repeated and teaches_only`, dead at ≤2, **inconclusive** at 3. The gate does not
  round up.
* **the control** — if the placebo documents behave the same way, H2's *generative*
  reading is dead even if its descriptive claim survives. That rule was fixed
  before the read.

**The declaration — population rule, classification rules, both gates, the
control's interpretation rule, the limits and the method — is in
[`PROTOCOL.md`](PROTOCOL.md), written before any artifact type in this
population was classified. This file carries the result.

## Result (`observed` 2026-10-05, `results.json`)

### **H1 is dead.** The hypothesis was wrong and the field is stocked with code.

| arm | class | n | decided | served | share |
|---|---|---|---|---|---|
| mature | executable | 25 | 17 | 12 | **71%** |
| mature | document | 4 | 0 | — | — |
| mature | unreadable | 1 | 0 | — | — |
| young | executable | **14** | 4 | 1 | **25%** |
| young | document | **4** | 0 | — | — |
| placebo | executable | 8 | 6 | 0 | 0% |
| placebo | document | 4 | 1 | 0 | 0% |
| placebo | unreadable | 1 | 1 | 0 | 0% |

**The young arm is 14 of 18 executable. `document` is 22% of the readable young
arm, against a declared 50% threshold, so the share condition fires and H1 is
dead.** The rate-parity condition could not be computed — no young document has a
decided row at all — and is reported as uncomputed rather than as a pass.

**The verdict does not depend on the classification disputes.** Reading every
young-arm root listing by hand gives **13 executable and 5 document**, one
disagreement (`Piebald-AI/claude-code-system-prompts`: 12,829★, 100 GitHub
releases, no manifest and no entry point — a prompt collection tagged a hundred
times), and 28% is still below 50%. `reviewed.json` carries the review; a test
asserts the gate never reads it.

**So the alternative explanation for F034 is excluded.** F034 found that *a tool
exists, therefore the need is served* holds 4/4 in mature vocabularies and 1/4 in
a young one, and it could not say whether that was the world or the instrument.
One candidate answer was that the screen is counting prose — that in a young
vocabulary the things that match a need's words best are guides and prompt
collections rather than software. **They are not.** Four of eighteen. The
premise's failure in a young vocabulary is not explained by the population being
documents.

### What the young arm looks like instead

The arm is real code that the instrument can barely see, and the attention is not
where the code is.

| | median stars |
|---|---|
| young arm, executable rows | **566** |
| young arm, document rows | **6,072** |
| mature arm, executable rows | 7,032 |

An order of magnitude. The young arm's top four rows by stars are a Go tool
(`alibaba/open-code-review`, 43,700★), a prompt collection (12,829★), a showcase
(10,035★) and a guide-with-an-MCP-server (6,101★); its **median** row is a 60★
tool. Meanwhile **14 of 18 young rows have no serving reading at all**, and 13 of
those 14 are tools.

Four rows could be read, and they are the whole of what is known about use in this
vocabulary:

| repository | stars | best reading | floor |
|---|---|---|---|
| `clay-good/OpenLore` | 318 | 7,761 npm/month | clears |
| `alibaba/open-code-review` | 43,700 | 363 brew/30d | does not |
| `kaplanelad/shellfirm` | 934 | 492 crates/month | does not |
| `YoanWai/agent-manager` | 566 | 60 brew/30d | does not |

**The most-starred tool in the young vocabulary is installed a few hundred times a
month.** Against the mature arm's 12 of 17, the young arm is 1 of 4 — and 1 of 18
of the arm as a whole. That is F034's split again, now with the population's
composition established: supply is plentiful, measured use is scarce, and **the two
are not the same population.** A prior-art screen counts the first and reads it as
the second.

### H2 could not be evaluated on the population it was declared for

The declared H2 population is the 10 highest-starred young-arm rows classified
`document`. **There are 4.** The gate is reported as `population_short` with
`n = 4`, which is a quarter of what the thresholds were written for: whatever H2
says, it rests on four observations and cannot be more than that. The gate also
has a third answer it did not have when declared — `not_evaluated` for an empty
read — added after the first run printed `dead` for a population nobody had read.

### An instrument defect of my own, found by reading the cache

The first fetch run **cached two budget refusals as readings**: the core limit is
60 an hour and the run needed two requests for each of 30 rows, so
`dariusk/express-activitypub` and `landy22granatt/Kumpulan-Script-Termux` were
answered `403` and stored. A later run would have skipped them as already asked.
That is F032's dead branch again — *I could not ask today* becoming *this
repository could not be read* — in a new place, and it was invisible because the
rows still classified as `unreadable`, which looks like a finding. `rootlisting._complete`
now refuses a half-answered row and the refused half is re-asked;
`tests/test_artifact_tally.py::FetchCacheTest` holds the difference in both
directions.