# 016 — what does the prior-art screen's population actually contain?

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

**Date:** 2026-10-04. **T-0061.** The classification rules, both gates and the
control's interpretation rule below were written **before any artifact type was
read**. No network request was made for this experiment before this file existed.

**The hypothesis was not formed blind, and the leak is named.** I read the 48
repository *names* inside `EXPERIMENTS/015-incumbent-serving/results.json`
before writing this, and four of them are named `…-guide`, `…-showcase`,
`…-system-prompts` and `…-references`. That is reconnaissance from an artifact
this repository already holds, and it is the only thing I looked at: no artifact
type, file listing, release count or serving figure for this population was read
before the gates below were fixed.

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

## Population — reused, not re-searched

Every row `EXPERIMENTS/015-incumbent-serving/results.json` holds: 30
`incumbents` (mature vocabularies, from F029's 19 prior-art kills), 18 `cluster`
(young vocabulary: `claude code`, agent guardrails), and 015's 5 declared
placebos plus its 8 rebuilt placebo controls. **61 rows**, not the 56 this file
first said — the 5 declared placebos are included as well, and they are worth
including precisely because 015 could read none of them.

Reusing the population is deliberate. It costs comparability nothing and search
quota everything — GitHub's unauthenticated search budget is 10 requests per
minute and its core budget 60 per hour, so a second population would have been
smaller and uncomparable rather than larger and clean.

Three arms are reported separately and **all whatever they say**:

| arm | rows | what it is |
|---|---|---|
| mature | 30 | the population the screen consulted for F029's kills |
| young | 18 | one young vocabulary: coding-agent guardrails |
| placebo | 13 | 5 repositories 015 declared unexercised + 8 unpopular ones its instrument *could* read |

## Classification — primary evidence, no taste

A row is classified from **the repository's own root file listing** and **whether
it has published a release**. Nothing is inferred from the repository's name,
description or topic list, because those are the fields the phrase query matched
on and reading them back would be the experiment's own subject.

**`executable`** — the root listing contains at least one of
`package.json`, `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements.txt`,
`Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`,
`Dockerfile`, `docker-compose.yml`, `Makefile`, `CMakeLists.txt`, `install.sh`,
`bin/`, or a file named `cli.*`, `main.*`, `index.*`, `app.*`, `server.*`,
**or** the repository has published at least one GitHub release.

**`document`** — the root listing was readable and none of the above holds.

**`unreadable`** — the root listing could not be read. A third class, never
folded into the other two and never silently dropped. 015's own instrument
correction is the reason: a repository that publishes nothing has told us about
its distribution, not its use, and that error must not be repeated by counting an
unreadable row as a document.

Root listing and release existence are **both** read for every row, and the
contents-only classification is reported alongside, because "ships a binary and
keeps no manifest" is a real class (F032's `thought-machine/please` is one).

### Declared correction, made before any row was classified

The entry-name patterns were first declared as `cli.*`, `main.*`, `index.*`,
`app.*`, `server.*` on **any** suffix. That rule calls `index.html` an executable
artifact, and the error direction is the one that shrinks the class this
experiment needs to be large in. The correction — match those stems only against
**source** suffixes — was written after the self-check and **before any row of
the population was classified**; its motivation was the self-check's own
`index.html` case, not a row. It is recorded as
`classification.DECLARED_CORRECTION`, the classifier as first declared is kept
runnable as `classify_as_first_declared`, and a test asserts the two disagree on
exactly that case and on nothing else.

### Every row is also reviewed by hand

`reviewed.json` carries a `reviewed_class` and a one-line reason for every row,
and `tally.audit` reports agreement per arm. **The gate is computed on the
mechanical classification, because that is the classification the gate was
declared on** — a test asserts `tally.h1` never reads the review. The review
exists so the mechanical rule's error rate is visible and its *direction* is
known, which a gate on the mechanical class alone cannot show.

## H1 — the population is mostly documents in the young vocabulary

**Declared gate.** H1 is **dead** if `document` is **≤50%** of the readable young
arm, **or** if `document` rows clear a declared floor at the **same rate** as
`executable` rows do (within 10 percentage points). It **survives** otherwise.
Both conditions are reported separately and one firing condition is enough, so a
run in which documents are 70% of the arm *and* serve no better than tools is
**dead on the second condition alone** — which is the informative reading, because
the descriptive half of H1 then holds while the differentiating half does not.

If parity cannot be computed — one class has no decided row — that condition is
**not counted as firing**, the gate is decided on the share alone, and the reason
is printed. An uncomputed condition is not silently treated as a pass.

Floors are 015's, unchanged and imported rather than restated: rate channels
≥ 1,000/month; release-asset downloads ≥ 10,000; Docker pulls ≥ 100,000. A second
copy of "clears a declared floor" in this repository is how a comparison ends up
measuring two definitions, and 015's own `INSTRUMENT_CORRECTION` is the record of
that having already happened once.

## H2 — a high-star document teaches a repeated procedure nothing runs

This is the half that could produce candidates rather than only calibrate a
screen, so it is read by hand and its per-row evidence is recorded.

**Population:** the 10 highest-starred young-arm rows classified `document`, or
all of them if fewer than 10 are readable and classified so.

**Read protocol**, recorded per row:

| field | how it is decided |
|---|---|
| `procedure` | what the README tells the reader to **do**, quoted |
| `repeated` | whether it is naturally performed more than once — per project, per day, per commit — judged from the quoted text |
| `install_line` | mechanical: the README contains an install-shaped command (`pip install`, `npm i`, `brew install`, `uvx`, `npx`, `curl … \| sh`, `go install`, `cargo install`) |
| `foreign_link` | mechanical: the README links a GitHub repository or product URL other than itself |
| `class` | `tutorial` if `install_line` or `foreign_link`, else `teaches_only` |

**Declared gate.** H2 **survives** if **≥4 of the 10** rows are `repeated` **and**
`teaches_only`. It is **dead** at **≤2**. Three is `inconclusive`, and the gate
will not round up.

**The control, and its interpretation rule declared in advance.** The same
protocol is applied to the **8 placebo repositories** — unpopular ones, in the
same niches, which 015 built precisely so that a figure there would be an
instrument defect. If the placebo rows are *also* predominantly
`repeated and teaches_only`, then H2's **generative** reading — *a high-star
document is a witness of an unmet need* — is **dead**, even though the descriptive
claim ("these documents teach procedures") survives. That is the reading that
would produce candidates, so it is the reading the control is aimed at.

## Limits, stated before the numbers are read

- **One annotator.** H2 is `observed` from primary-source reading by one model
  with a prior the record already names as a shared weakness
  (`RESEARCH.md`, and `SYNTHESIS.md` §4). Every quote is recorded so a reader can
  disagree with the `repeated` judgement specifically.
- **`repeated` is a judgement; the other four fields are mechanical.** The
  deliberate split is which side of it the claim rests on.
- **The population is 48 rows chosen by phrase search and by stars**, and 015
  measured 21 of 30 mature rows to be off-topic. Nothing here is a novelty claim:
  a GitHub count can refute and cannot establish (F030).
- **The young arm is one vocabulary.** `claude code` and coding-agent guardrails,
  chosen by 015 because its own cluster recurred. Every candidate this mission
  produces is in a young vocabulary, but not necessarily *this* one.
- **Classification is about what a repository contains, not about whether it
  works.** A tool with a manifest can be a shell script that prints "hello".
- **Neither H1 nor H2 validates a candidate.** H2 at best produces a list of
  procedures. A procedure is not a project.

## Method

| step | script | what it fixes |
|---|---|---|
| fetch | `fetch.py` | root listings and release counts, cached on disk so the 60/hour core budget is spent once |
| classify | `classify.py` | the three classes from the declared marker list, and the self-check against known-answer rows |
| join | `join.py` | classification joined to 015's serving figures, tallied by arm and class |
| read | `read.py` | the mechanical README fields; the judgement fields are written by hand into `reads.json` and `read.py` only checks the row shape |
| verdict | `tally.py` | both gates, the control's interpretation, and the candidate seeds |

Module names are unique across the repository: a sibling experiment owns
`stats.py` and `verdict.py` each, and two modules of one name in an interpreter
means the second import is silently shadowed — defect 24.