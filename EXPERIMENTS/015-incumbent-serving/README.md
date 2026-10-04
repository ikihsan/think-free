# 015 — does "prior art exists" mean the need is served?

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

**Date:** 2026-10-04. **T-0060.** The hypothesis, the sample rule and the floors
below were written **before any figure was read**. The only network access before
this file existed was the instrument's self-check, which asserts that six
certainly-used tools read as used.

**Verdict: the declared gate is `inconclusive`** — 43% of incumbents were
undecided against a declared 20% ceiling — but the premise behind the mission's
dominant kill reason has now been measured directly, and it **holds in mature
vocabularies and largely fails in young ones** (4/4 versus 1/4). F034.

## The question

The mission's dominant kill reason is "prior art exists". It killed 19 of 50
harvested needs (F029) and all twelve candidates the six sealed reports
produced. That verdict claims a property — **the need is served** — and it has
never been measured:

| check | property actually read | result |
|---|---|---|
| `verify_prior_art.py` (F029) | GitHub stars ≥ 100 | stars do not predict use in any niche, `\|rho\| ≤ 0.35` (F032) |
| `usage.py` (T-0059) | npm, PyPI, crates downloads | correct, but **its dead branch was never executable**: `thought-machine/please` ships as a Bazel binary |

So the verdict has been validated twice against proxies, and the one
instrument that read the property itself could not see the incumbent it was
built to judge. **H:** in the population of tools a prior-art screen names, fewer
than half show serving evidence.

This is the shape `docs/policy/gate-falsification.md` names — a check that
reads a proxy for the property it claims to read — arriving at the level of the
screen rather than the level of a gate. MISSION.md already says absence of a hit
is not originality. What is at stake here is stronger than novelty: it decides
whether the mission has been discarding needs that nobody is actually served on.

## Kill gate, declared before the run

- **K** — H is dead if **≥50%** of incumbents with a decided outcome show serving
  evidence at the declared floors.
- **S** — H survives if **<50%** do.
- **Inconclusive**, and the gate refuses to round up to either side, if:
  (a) more than 20% of incumbents have a `REFUSED` channel and no decided
  outcome — an instrument that declined is not a fact about the world; or
  (b) **any placebo repository shows serving evidence** at a rate floor. The
  placebo is the lowest-starred repositories five of the same queries return in
  reverse order; nobody uses them, so a figure there is an instrument defect.

Floors, declared: **rate** channels (npm, PyPI, crates, Homebrew 30-day installs)
≥ 1,000/month; **cumulative** channels (GitHub release-asset downloads ≥ 10,000;
Docker Hub pulls ≥ 100,000). The classes are reported separately and never
merged, because a cumulative count cannot decay and a monthly rate can.

**A second arm, declared after the population was built and before any figure
was read.** `incumbents.py` ran first, and its output shows the population
construction carrying F030's own defect: `flashcards anki` returns
`donnemartin/system-design-primer` at 373,170 stars, `word game` returns an
Indonesian book collection, and `hacker news api client` returns three
same-owner spam repositories. **The instrument that told the screen "prior art
exists" returned repositories that have nothing to do with the need**, and the
high-starred end of these queries is exactly where that happens.

So the declared gate above is answered on the population *as the screen
consulted it*, and a second, separately-reported arm answers it on the
*on-topic* subset: a repository is on-topic when a content term of the need's
phrasing appears in its name or description, matched mechanically with no
judgement. **Both are reported whatever they say, and neither is chosen after
the fact.** A gate that only reads the on-topic arm would silently repair the
population with taste after seeing which repair flatters the answer.

### Known limit of that second arm

Whole-word matching on a two-word phrase cannot see an incumbent described in
different words, so the on-topic arm **understates** incumbents and is biased
against H surviving. It is a bound, not a substitute.

## Method

| step | script | what it fixes |
|---|---|---|
| population | `incumbents.py` | two phrasings per killed need, `in:name,description` only, top 3 by stars, deduplicated; placebo arm |
| instrument | `serving.py` | rate and cumulative channels, each attribution verified to name the measured repository; a self-check of six known answers |
| verdict | `verdict.py` | the tally and the gate, in both directions |

**Two channels are new and they close T-0059's dead branch.** Homebrew's own
analytics answer `brew install` counts for CLI tools, which is the dominant
install path for the class of tool this screen kills. GitHub release-asset
`download_count` answers downloads for tools that ship a binary and publish
nothing to a registry — `thought-machine/please` reads **87,822** there, against
the zero every registry instrument reports for it.

**A name is not an identity.** Every registry and Homebrew figure counts only if
the package's own metadata names the repository being measured. The case F032
names is refused by construction and asserted in `tests/test_serving_stats.py`.

## Limits, stated before the numbers are read

- **Homebrew counts macOS and Linuxbrew only.** A tool nobody installs that way
  reads as unused, which is the direction that flatters H.
- **Release-asset downloads include a project's own CI, dependabot and Docker
  builds.** This is why the placebo arm exists.
- **Package names are guessed** from repository names (`serving.guesses`), so an
  unnamed package reads as an absence. Recorded per row in `guessed`.
- **The sample is the 30 highest-starred incumbents**, which is the sample most
  likely to be serving. A "not served" result from it is not rescued by picking
  less popular tools; a "served" result is not rescued by that direction either.
- **The population is what a phrase query surfaces**, which F030 measured as
  wrong in both directions from one query. Two phrasings reduce that; they do not
  eliminate it, and nothing here is a novelty claim.
- **Installs are not users**, and Docker pulls are not installs.
- One snapshot, one machine, unauthenticated public APIs.

## Result (`observed` 2026-10-04, `results.json`)

**The declared gate is `inconclusive`: 43% of incumbents were undecided, above
the declared 20% ceiling.** Neither arm fires and neither is reported as
passing. What the run did establish is narrower and more useful than the
hypothesis asked for.

| arm | decided | served | share |
|---|---|---|---|
| incumbents, all | 17/30 | 12 | **71%** |
| incumbents, on-topic subset | 4/9 | 4 | **100%** |
| cluster — the young vocabulary | 4/18 | 1 | **25%** |
| placebo controls (unpopular, readable) | 8/8 | 0 | **0%**, 0 false positives |

### 1. The instrument's dead branch is now executable

`thought-machine/please` was the incumbent T-0059 declared invisible, because it
ships as a Bazel binary and no registry carries it. GitHub release assets read
**87,822** downloads for it. The same channel finds `ankitects/anki` at
**39,222,570** and `gotson/komga` at 45,299,026 — incumbents no registry channel
sees. F032's ceiling is closed by measurement, not by argument.

### 2. The floors survive their own falsification

The declared placebo was five zero-star repositories that publish nothing to any
channel: **all five unreadable, so a false positive was impossible by
construction.** That arm proved nothing and is reported as unexercised. It was
rebuilt (`placebo.py`) to search for unpopular repositories that *are* readable:
**8 of 8 read, 0 false positives**, including `rustfs/mcp` and `uptimepage/uptimepage`,
which sit in exactly the niches the primary arm screens. The self-check's six
known-used cases and these eight known-unused ones bracket the floors from both
sides.

### 3. The arms disagree, and the disagreement is the finding

Mature vocabulary, on-topic incumbents: **4 of 4 decided are served.** Young
vocabulary (`claude code`, coding-agent guardrails): **1 of 4**, and 14 of 18
unreadable. The prior-art verdict's premise — *a tool exists, therefore the need
is served* — **holds where the vocabulary is mature and largely fails where it is
young.** That is the first measurement of the premise itself rather than of a
proxy for it, and it is the same shape as F032's young-versus-mature split seen
from the other end.

### 4. The population carries the instrument's own defect

Of the 30 incumbents the screen consulted, **21 are off-topic**: the query
`flashcards anki` returns `donnemartin/system-design-primer` (373,170★) and
`hacker news api client` returns three same-owner spam repositories. The
high-starred end of a phrase query is where this happens, and the sample rule
(30 highest-starred) selects for it. F030 measured this on one query; here it is
the majority of a 30-row population.

### An instrument correction, recorded rather than quietly applied

The first run counted a repository publishing no release assets as a **decided
reading of zero use**. That put 13 of 30 incumbents into the denominator with no
evidence in them and printed **40% served**; excluding them gives **12 of 17, or
71%**. The error is the same shape as the one the experiment exists to name — a
proxy (a published artifact) read as the property (use) — which is why it is in
`verdict.INSTRUMENT_CORRECTION`, asserted in `tests/test_serving_stats.py`, and
reported as a number the gate first printed.