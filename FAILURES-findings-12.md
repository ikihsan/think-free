<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Failures — recorded findings, part 12 (F034)

Continues [`FAILURES-findings-11.md`](FAILURES-findings-11.md), which holds
F033. **Identifiers are stable across all findings files**: a reference to
`F034` means the same entry wherever it appears. **Renumbered on the unpushed
side:** the other VM published `F033` for the repository-signal filter's
refutation of F029's recurrence counts while this work was in flight, and
`EXPERIMENTS/014` with it.

## F034 — The prior-art screen's premise holds in mature vocabularies and largely fails in young ones

Source: session `2026-10-04-054`, T-0060. Runnable evidence:
`EXPERIMENTS/015-incumbent-serving/` (`incumbents.py`, `serving.py`,
`placebo.py`, `verdict.py`, `results.json`, `raw/`). `observed` 2026-10-04.

## What was measured, and why it was worth doing

The mission's dominant kill reason is *prior art exists*. That phrase claims a
property — **the need is served** — and no check had ever read it. F029's
check read stars; F032 then measured that stars do not predict use anywhere.
T-0059 read registry installs correctly but recorded that **its dead branch was
never executable**, because the mature arm's dominant incumbent ships as a Bazel
binary. So the mission's central screen has been validated twice against
proxies and never against the thing it names.

014 measures the premise itself, on the population the screen actually consulted:
the repositories a GitHub phrase query surfaces for each of F029's 19
`prior_art` kills, two phrasings each.

## Observed

| arm | decided | served | share |
|---|---|---|---|
| incumbents, all | 17/30 | 12 | **71%** |
| incumbents, on-topic subset | 4/9 | 4 | **100%** |
| cluster — a young vocabulary | 4/18 | 1 | **25%** |
| placebo controls (unpopular, readable) | 8/8 | 0 | **0%**, 0 false positives |

**The declared gate is `inconclusive`:** 43% of incumbents were undecided
against a declared 20% ceiling. Neither arm fires. The hypothesis — fewer than
half of named incumbents are serving — is **not supported on the readable
population, and not refuted either**, because the population is only 57% readable.

**The disagreement between the arms is the finding.** Mature vocabulary,
on-topic incumbents: 4 of 4 decided are served. Young vocabulary
(`claude code`, coding-agent guardrails): 1 of 4, with 14 of 18 unreadable.
**"A tool exists, therefore the need is served" holds where the vocabulary is
mature and largely fails where it is young** — the same young/mature split
F032 measured from the other end, now read off the screen's own population
rather than off a stars search.

## F032's dead branch is closed by measurement

`thought-machine/please` was the incumbent T-0059 declared invisible. GitHub
release assets read **87,822** downloads for it. The same channel finds
`ankitects/anki` at **39,222,570**, `gotson/komga` at 45,299,026 and
`louislam/uptime-kuma` at 188,858,375 Docker pulls — incumbents that no registry
channel sees. **Zero measured installs was never zero users; it was the
instrument's blind spot, and it is now a number.**

## Three falsifications, each changing a decision

- **The floors were challenged from below.** The *declared* placebo was five
  zero-star repositories that publish nothing to any channel. All five were
  unreadable, so **a false positive was impossible by construction and the arm
  proved nothing.** It is reported as unexercised, not as a pass — the same
  dead-branch defect F032 records, in the opposite direction. Rebuilt
  (`placebo.py`) to search for unpopular repositories that *are* readable: 8 of 8
  read, **0 false positives**, including `rustfs/mcp` and
  `uptimepage/uptimepage` in the very niches the primary arm screens. Six
  known-used self-check cases and eight known-unused controls now bracket the
  floors from both sides.
- **An instrument defect of my own, found by reading the first result.** The
  first run counted a repository publishing no release assets as a *decided
  reading of zero use*, putting 13 of 30 incumbents into the denominator with no
  evidence in them; it printed **40% served**. Excluding them gives **12 of 17,
  or 71%**. A project that ships nothing has told us about its distribution, not
  its use. This is the experiment's own subject — a proxy read as the property —
  which is why it is named in `verdict.INSTRUMENT_CORRECTION` and asserted in
  `tests/test_serving_stats.py` rather than quietly corrected.
- **The population is mostly not what the screen consulted.** **21 of 30
  incumbents are off-topic**: `flashcards anki` returns
  `donnemartin/system-design-primer` (373,170★), `hacker news api client`
  returns three same-owner spam repositories, `word game` returns an Indonesian
  book collection. F030 measured this defect on one query; here it is the
  majority of a 30-row population, and the "30 highest-starred" sample rule
  selects for it.

## What it changes

**A prior-art verdict is now a measurement with a stated vocabulary.** It may be
recorded as `served-in-a-mature-vocabulary` or `unserved-in-a-young-vocabulary`,
and neither is a novelty claim. The mission's twelve prior-art deaths are not
reversed by this, and nothing here makes any candidate worth building; what
changes is that the *reason* is no longer a proxy read as a fact.

**The install-path axis T-0059 offered is the part that survives.** In the young
vocabulary where every candidate this mission produces lives, a named incumbent
was serving 1 time in 4 — so the premise "someone already has this" is weakest
exactly where it is being used to kill.

## What it does not show

Not a novelty claim: a GitHub count can refute and cannot establish (F030), and
every figure is a download, not a user. Homebrew counts macOS and Linuxbrew
only; release-asset downloads include a project's own CI, dependabot and Docker
builds; package names are guessed, so an unnamed package reads as an absence.
Installs are not active use. The on-topic arm is n=9 and its whole-word matcher
cannot see an incumbent described in different words, so it **understates**
incumbents. The cluster arm was measured without the release channel, which
costs one GitHub core request per repository and the hourly limit was spent; 14
of its 18 rows are unreadable and its 25% rests on **four** decided rows. One
snapshot, one machine, unauthenticated public APIs.
