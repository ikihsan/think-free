# E016 — Is "a tool already serves this" a screen that can be shown to work?

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

**Date:** 2026-10-04. **Declared before any count was read**, in the order the
question, the gate, the phrasings and then the fetches.

## The question

E012 screened 50 harvested need statements and killed 19 with one verdict:
*"a tool already serves this"*. That verdict is load-bearing twice over. It was
the largest cause of death in the harvest (F029), and the same verdict killed
all twelve candidates that came out of the six sealed reports, so no candidate
has ever survived a prior-art screen in this mission.

Its own record says the verdict is not reliable. F030 demonstrated, on the same
day, that a single search query decides a prior-art verdict wrongly in **both**
directions — 502 hits that were not prior art, and 0 hits that were not a gap.
`EXPERIMENTS/012-candidate-harvest/README.md` puts the exposure in numbers: of
the 19 kills, **6 have a populated count behind them, 4 were checked and could
not be verified, and 9 were never checked at all.** Thirteen of nineteen rest on
judgement, made by one agent, with the instrument its own record calls
unreliable.

So: **is F029's largest cause of death sound?** Not "is there a better
generator" — that question was answered. This asks whether a specific
adjudication procedure, applied to needs that are already on the table, finds
prior art where the judgement found it.

## Why a third corpus

Two corpora have been read so far: GitHub's repository index and package
registries. Both are code indices, and both miss the same population — a hosted
service, a commercial product, a vendor feature, a paper, a forum answer. F030
states the blindness in one line: *"a tool on PyPI, npm or a commercial service
reads as zero."* The blind spot is symmetric: a commercial tool reads as zero
on GitHub too.

The **open web** is the corpus where that population is visible, and no
prior-art probe in this repository has ever read it. It is also the corpus a
practitioner would actually use before building: what would I type into a
search engine to find out whether this already exists.

| corpus | what it sees | what it cannot see |
|---|---|---|
| GitHub repositories (`in:name,description`) | open source, by stars | commercial, hosted, configuration, a feature inside a bigger product |
| package registries (PyPI, npm, crates.io) | installable libraries and CLIs | anything not packaged, anything needing an account |
| open web | hosted and commercial tools, docs, comparisons | anything not indexed by a search engine, anything recent |

`in:name,description` and not `in:readme`: F030 showed `in:readme` matched the
README of `awesome-go` (186917 stars), a self-hosting guide and a Discord bot.

## Design

**Positive controls first.** Six of the nineteen kills are already supported by
a populated count: `anki` 31750 stars across 2030 flashcard repositories,
`uptime-kuma` 92112 across 10768, s3 storage 172, `Vanilla-OS/ABRoot` 392, webp
encoding 115, calibre tooling 13. A procedure that cannot recover those six is
not measuring this question, and everything it says about the other thirteen is
void. The controls are run first, in that order, so a broken procedure is
caught before it produces an answer.

**Attribution, never a count.** A hit counts only when an artifact is named that
plausibly serves the clause, and the deciding text is recorded. This is F030's
rule applied to the population that produced F030.

**Stopping rule, fixed in advance.** An item is *served* as soon as one corpus
returns one attributed artifact. An item is *no prior art found* only after
**at least two phrasings on every corpus have returned nothing attributable** —
never on the strength of a single query, which is the exact error F030 names.
A refused or rate-limited answer is recorded as `refused` and is never an
absence.

**Phrasings are written down before the first fetch**, in
[`phrasings.json`](phrasings.json), derived from the clause text and not from
the original screen's reason. Where the original reason answered a different
question than the clause asked, that is recorded as a defect in the screen and
not repaired silently.

**Known limit, declared here.** The adjudicator is the same model that drew the
sample and wrote the original reasons. It cannot be blind to them. The positive
controls are the only instrument check available, and they bound the
instruments' error from one side only — they can show the procedure is too
weak, never that it is too strong.

## The gate

Two arms, both declared before any count was read.

**Arm 1, instrument validity.** At least **5 of the 6 positive controls** must
be re-adjudicated *served*. Fewer than 5 and the answer to the real question is
void; the finding becomes a statement about the instrument.

**Arm 2, the answer.** Of the 13 kills with no populated count behind them, how
many are *no prior art found* on all three corpora.

- **≥ 3** — `prior_art` is materially overstated as a cause of death, F029's
  cause table is restated, and those items become the mission's first leads not
  derived from its own reports. They go to a mechanism step; F029's generator
  verdict is **narrowed, not reversed**, because Screen 1 and Screen 3 still
  apply to a need with no solution found.
- **≤ 2** — the category is confirmed, `EXPERIMENTS/012` closes for good, and
  need-harvesting is not a generator.

Either direction is a decision this mission has never been able to make about
this verdict.

## Method

| step | script | what it fixes |
|---|---|---|
| adjudicate | `adjudicate.py` | runs the declared phrasings over the three corpora, appends every raw response |
| attribute | attributed by the agent, recorded in `raw/attributions.jsonl` | a count is never a verdict |
| report | `results.json`, `stats.py` | the two arms, from the record rather than from memory |

Raw captures are append-only under `raw/`. The open-web corpus is searched by
the agent and transcribed query-for-query into `raw/web_log.jsonl`, because the
search tool has no API this script can call; the transcription is the evidence
and its limits are stated with it.

## Limits, declared before the run

- Absence of a hit on three corpora is not novelty and is not a gap. It is the
  absence of a hit, which is the only thing any of these instruments can
  produce.
- 19 items, one model, one day, and the controls are drawn from the same 19.
- A need statement is not a candidate. Even an un-served item has no mechanism,
  no differentiation and no adoption path, and this experiment supplies none of
  those three.

## What the run found, 2026-10-05

Both arms are answered from the record by `stats.py`, which writes
`results.json`; nothing below is typed from memory.

| arm | declared gate | result |
|---|---|---|
| 1, instrument validity | ≥ 5 of 6 positive controls re-adjudicated **served** | **6 of 6** |
| 2, the answer | ≥ 3 of the 13 judgement kills **no prior art found** on all three corpora | **3 of 12**, threshold met exactly |

**Arm 2 landed on the threshold, and one row decides it.** The three are items
7 (annotate once, choose metric/log/trace per code path at runtime), 12 (tag HN
posts and authors inside an HN client) and 16 (a daily word game that shows the
solution order so a player can give up). Item 16's open-web results include ten
answer-aggregator sites that reveal solutions *outside* the game; counting those
as serving the clause gives 2 and reverses the declared direction. The stricter
rule is used and `results.json` carries both numbers. A thirteenth item is
**unadjudicable**: its clause asks for a game in which bots are allowed while
E012's reason — and therefore the phrasings — asked about Hacker News clients.

**Corpus carriage is the transferable part.** GitHub's repository index carried
every verdict the code corpora carried (11 items). The registries carried none
on their own: PyPI's search answers a bot challenge, so that leg became the
complete 905,521-name index with no descriptions, and npm/crates substring
search is noise. **The open web carried 4 served verdicts that two code corpora
returned nothing for** — url-popularity (twelve named hosted services),
cpp-subset-linter (PC-lint enforcing MISRA), selective-stage (`git add -p`
itself), interest-field (contested, counted as served to favour prior art).

**Two instrument facts changed how this could have been run.** Bing answered
HTTP 200 with ten well-formed organic results for all 38 declared queries and
every one of them was unrelated to its query, with and without a corrected
browser User-Agent; and `raw/brave/*.log` records a Brave route that returned
429 partway through. Only DuckDuckGo Lite through the harness's fetch tool
passed a **known-answer control** ("lazygit stage hunk split hunk" → 9 of 10
results about lazygit), and that control is why item 42 names lazygit when
neither declared phrasing did. F035 and F036 are the findings; D050 is the
decision.

**Ceilings, unchanged by the result.** Arm 1's controls were selected for having
a populated count, so recovery shows the instrument finds a *category*, not that
it finds an *attribute*. The adjudicator is the same model that drew the sample
and wrote the original reasons. Absence of a hit on three corpora is the absence
of a hit: item 16 sits beside 7658 wordle clones and item 12 beside 892 HN
clients, and neither is a gap, a candidate, or useful.

**Raw layout.** `raw/` holds `github_search.jsonl`, `registry_search.jsonl`,
`pypi-simple-meta.json`, `web_log.jsonl` (transcribed open-web results, with the
instrument checks in its first three rows), `attributions.jsonl` (the
attributed judgement, per item, with the deciding text) and `brave/*.log` plus
`openweb-one-capture.log`, the two refused routes kept verbatim. The PyPI name
index itself is untracked under the `.gitignore` clause for downloaded
third-party inputs pinned by hash; its url, status, byte count, sha256 and name
count are in `pypi-simple-meta.json`.
