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
| mature | executable | 26 | 17 | 12 | **71%** |
| mature | document | 4 | 0 | — | — |
| young | executable | **14** | 4 | 1 | **25%** |
| young | document | **4** | 0 | — | — |
| placebo | executable | 9 | 7 | 0 | 0% |
| placebo | document | 4 | 1 | 0 | 0% |

All 61 rows were read; `results.json` carries `population.complete: true`. The
first run reached 58 and named the three it could not — they were this
instrument's core budget, not the repositories, and two of them classify as tools.

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
all, and 10 of those 14 are tools.** The four rows that could be read are the whole
of what is known about use in this vocabulary, and one of them clears a floor:

| repository | stars | best reading | floor |
|---|---|---|---|
| `clay-good/OpenLore` | 318 | 7,761 npm/month | clears |
| `alibaba/open-code-review` | 43,700 | 363 brew/30d | does not |
| `kaplanelad/shellfirm` | 934 | 492 crates/month | does not |
| `YoanWai/agent-manager` | 566 | 60 brew/30d | does not |

**Supply is plentiful, measured use is scarce, and they are not the same
population.** A prior-art screen counts the first and reports it as the second.

### What the four documents turned out to be, and it is the useful part

H2 is dead, and its control could not run, so this is a four-row observation
rather than a gate. It is recorded because the *reason* it is dead is not the
reason the hypothesis expected.

| repository | ★ | what the reader is told to do | repeated? | class |
|---|---|---|---|---|
| `diet103/claude-code-infrastructure-showcase` | 10,035 | "This is NOT a working application — it's a reference library. Copy what you need into your own projects." Then `git clone` + `npx tsx setup.ts ~/my-project`, or copy `.claude/` and install hook dependencies. README: "Time to integrate: 15-30 minutes" | no — once per project | tutorial |
| `ChrisWiles/claude-code-showcase` | 6,072 | "1. Create the `.claude` directory 2. Add a `CLAUDE.md` file 3. Add `settings.json` with hooks 4. Add your first skill", against a `your-project/.claude/{agents,commands,hooks,skills}` tree | no — once per project | tutorial |
| `Cloudgeni-ai/infrastructure-agents-guide` | 206 | thirteen chapters of architectural decisions, then "if you want to see these patterns implemented in a real product, see OpenGeni" | no — nothing to perform | tutorial |
| `Aryia-Behroziuan/References` | 70 | 37,405 bytes under one heading, `References` | no | teaches_only |

**None of them is a manual workaround.** The hypothesis was that the field's
best-known documents would show a repeated procedure that nothing runs. They show
the opposite: the reader copies a **directory of files into their own repository
once**, and after that the hooks the document installed are what run, on every
prompt and every edit.

**That is the observation with a consequence.** In this vocabulary the artifact
that gets used is not a package — it is a `.claude/` directory, delivered by clone
or by copy. **Every serving channel this repository has is blind to it:** npm,
PyPI, crates, Homebrew, Docker Hub and GitHub release assets all count
installations, and a directory committed into somebody's repository is none of
those. So the number F034 and this experiment both read — *1 of 18 young-arm
incumbents clears a serving floor, 14 of 18 have no readable channel at all* — is
consistent with a field that is **used and invisible to the instrument**, and
F037 has now removed the two explanations that were available before
(population-is-documents, and population-is-not-what-was-read).

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
- **H2 is four rows.** The declared control did not run, and no amount of
  reading fixes that: the placebo documents in this population are
  `CalibreWeb-Ebook-Server/.github` and three repositories whose roots are
  documents incidentally. A control built on that population cannot discriminate,
  which is a defect in the population rule and not in the read.
- **The four-row read is one annotator's judgement** of `repeated`. Every quote
  is in `reads.json` so the disagreement can be had with the judgement rather
  than with the number.
- **H2 was read and is `dead` at 0 of 4.** Its declared population is the 10
  highest-starred young-arm `document` rows. There are 4, so `population_short` is
  true and the verdict rests on four observations whatever it says. It says: all
  four are `tutorial` by the mechanical fields, and **none of the four teaches a
  repeated procedure**. The declared control could not run — one of the four
  placebo documents was readable and it is a 119-byte stub — so it is reported
  `unexercised`, not as a pass.
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
## F038 — Lead 7's mechanism question is answered, and the answer is a feature gap, not a candidate

### What happened

E016's third arm put three need statements no artifact on three corpora serves
(F035, D050). The first went to its mechanism question the same day
(`EXPERIMENTS/018`): *is there an interposition point that sees the code path
and can select a signal per path, or is the choice always made at
instrumentation time?*

### The two probe results

- Against the stock OTel Python SDK 1.33.1 (`otel_probe.py`): the only
  runtime mutation points are `add_span_processor` and
  `add_log_record_processor`. No remove, no disable, no runtime sampler swap,
  and no per-call signal switch. The nearest built-in prior art, the collector's
  tail-sampling processor, keeps or drops whole traces by static policy — it
  never chooses metric-vs-log-vs-trace for a path.
- Against the need itself (`sigsel.py`): one annotation per path, a mode
  variable read on every call, and the same call site emitted `metric`, `log`,
  then `trace` across four calls — asserted, not eyeballed. ~70 lines.

### What it rules out

- It does **not** rule lead 7 back out. "No prior art found on three corpora"
  is still the state of the world, and the stock-SDK friction the HN clause
  complains about is now demonstrated, not assumed.
- It does rule lead 7 out as a project. The missing piece is a thin built-in
  conditional in an observability SDK — a feature request, not an invention,
  until a use case with users is named. Utility is unmeasured and no user has
  been quoted beyond the original HN comment.

Ceiling: one SDK version, one language, one collector README read once on
2026-10-05.
