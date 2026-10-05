<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Failures — recorded findings, part 14 (F037)

Continues [`FAILURES-findings-13.md`](FAILURES-findings-13.md), which holds
F035 and F036. **Identifiers are stable across all findings files**: a reference
to `F037` means the same entry wherever it appears.

Source: session `2026-10-04-056`, task T-0061. Runnable evidence:
`EXPERIMENTS/017-incumbent-artifact-type/` (`rootlisting.py`, `classification.py`,
`servingjoin.py`, `tally.py`, `reviewed.json`, `results.json`, `raw/`). The
declaration is `PROTOCOL.md` and the reload point is that directory's `README.md`,
both committed before any artifact type in this population was classified.
`observed` 2026-10-05, unauthenticated public APIs, one snapshot.

## F037 — The screen's young-vocabulary population is real code, so the premise's failure is not a population artefact

### What was tested

F034 measured the prior-art screen's own premise — *a tool exists, therefore the
need is served* — and found it holds 4 of 4 in mature vocabularies and 1 of 4 in
a young one. It could not say whether that was the world or the instrument, and
one alternative explanation had never been tested at all: **that in a young
vocabulary the highest-starred matches for a need's words are documents rather
than software**, so "prior art exists" is satisfied by prose and the screen is
measuring the existence of writing.

**H:** in the young vocabulary, `document` is more than half the readable
population the screen consulted. Dead at ≤50%, or if document rows clear a
declared serving floor at the same rate executable rows do.

### Observed

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

**H is dead.** The young arm is 14 of 18 executable; `document` is 22% of the
readable young arm against a declared 50% threshold. **The verdict does not
depend on the classification rule's errors.** Every young-arm root listing was
read by hand into `reviewed.json` and the arm is **13 executable and 5
document** (28%) — one disagreement, and it runs *against* the hypothesis.
Across all three arms there are three disagreements in both directions, and the
gate is computed on the mechanical class because that is the class it was declared
on; `tests/test_artifact_tally.py` asserts `tally.h1` never reads the review.

**So the alternative explanation for F034 is excluded.** The premise's failure in
a young vocabulary is not explained by the screen's population being documents.

### What the young arm looks like instead

| | median stars |
|---|---|
| young arm, executable rows | **566** |
| young arm, document rows | **6,072** |
| mature arm, executable rows | 7,032 |

An order of magnitude, and it runs the other way from the hypothesis: the young
arm's *median* row is a 60★ tool, its top four by stars are a Go tool
(`alibaba/open-code-review`, 43,700★), a prompt collection (12,829★), a showcase
(10,035★) and a guide-with-an-MCP-server (6,101★), and its documents are not
where the stars are. Meanwhile **14 of 18 young rows have no serving reading at
all and 13 of those are tools.** The four rows that could be read are the whole
of what is known about use in this vocabulary, and one of them clears a floor:

| repository | stars | best reading | floor |
|---|---|---|---|
| `clay-good/OpenLore` | 318 | 7,761 npm/month | clears |
| `alibaba/open-code-review` | 43,700 | 363 brew/30d | does not |
| `kaplanelad/shellfirm` | 934 | 492 crates/month | does not |
| `YoanWai/agent-manager` | 566 | 60 brew/30d | does not |

**Supply is plentiful, measured use is scarce, and they are not the same
population.** A prior-art screen counts the first and reports it as the second.

### What it changes, and what it does not

It **narrows F035 rather than repeating it.** The other VM's E016 re-adjudicated
E012's 19 prior-art kills and found **3 of 12 adjudicable kills had no prior art
on any of three corpora**. That is a *coverage* failure. This is a *composition*
measurement, and it comes out the other way: the population the screen consulted
is mostly genuine software. **Two independent measurements now put the prior-art
screen's problem in what it can reach, not in what it found** — which is a
different repair from anything in `STATE-next-actions.md`, and it is the first
time two measurements taken independently on 2026-10-05 agree on a cause.

It **does not rescue any candidate.** Twelve prior-art deaths are not reversed, no
candidate is validated, and the deferred owner decision on the selection axis is
untouched. What is stronger now is narrower: in a young vocabulary, "a repository
exists for this need" is a fact about **supply**, and the screen has been reading
it as a fact about **demand**. That gap is F034's 1-of-4 with its cause removed
as an artefact.

### Three instrument defects, each found by this experiment running on itself

- **A budget refusal cached as a reading.** The core limit is 60 an hour and the
  run needed two requests for each of 30 rows, so two rows were answered `403`
  and stored. A later run skipped them as already asked. That is F032's dead
  branch again — *I could not ask today* becoming *this repository could not be
  read* — and it was invisible because both rows classified as `unreadable`,
  which looks like a finding. `rootlisting._complete` now refuses a half-answered
  row.
- **Two vocabularies for "refused".** The fetcher declared `"refused"` and the
  classifier compared against `"refused:upstream"`, so a genuinely refused listing
  matched no branch and reached the `unexpected_shape` fallback: the right class
  for the wrong reason, and one edit away from the wrong count. Found by holding
  the *committed* cache to the property rather than a fixture. Both now take the
  constant from `attribution`.
- **A gate that answered about a population nobody read.** H2's declared
  thresholds are counts, and 0 hits is ≤ 2, so the first run printed `dead` for an
  empty read. It has a third answer now — `not_evaluated` — added after seeing the
  defect and before seeing any read.

### What this does not show

- **Not a novelty claim.** A GitHub count can refute and cannot establish (F030),
  and 015 measured 21 of 30 mature rows to be off-topic.
- **Three rows were never read**: the core budget ran out twice, so
  `dariusk/express-activitypub` and `landy22granatt/Kumpulan-Script-Termux`
  (mature) and `Notifuse/selfhost_s3` (placebo) are absent from the table and
  named in `results.json`. Two are mature and one is placebo, so the young arm's
  counts — the ones the gate uses — are complete.
- **H2 was not evaluated.** Its declared population is the 10 highest-starred
  young-arm `document` rows. There are 4. `tally.py` reports `population_short`
  with `n = 4`, which is a quarter of what the thresholds were written for, and
  the read of those 4 rows is not in this finding because it cannot carry a gate.
- **One young vocabulary**, chosen by 015 because its cluster recurred.
- **Classification is about what a repository contains.** A `Makefile` for
  checking links is a build file and the repository is an awesome list; a prompt
  collection tagged 100 times is executable by the declared rule and is not. Both
  are named in `reviewed.json` with the direction of each error.
- **A release count is a tag count**, so the `executable` signal is weaker than it
  looks, and that error direction grows `executable`.
- Installs are not users. Homebrew counts macOS and Linuxbrew only. Release-asset
  downloads include a project's own CI. 14 of 18 young rows were unreadable, and
  the 25% rests on four decided rows.