<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Failures — recorded findings, part 13 (F035, F036)

Continues [`FAILURES-findings-12.md`](FAILURES-findings-12.md), which holds
F034. **Identifiers are stable across all findings files**: a reference to `F035`
means the same entry wherever it appears.

Source: session `2026-10-04-056`, task T-0061. E016's two gate arms, adjudicated
on three corpora with six positive controls. Runnable evidence:
`EXPERIMENTS/016-prior-art-adjudication/` (`stats.py`, `results.json`,
`raw/attributions.jsonl`, `raw/web_log.jsonl`). Both arms were declared, with
their phrasings and stopping rule, in `phrasings.json` before the first fetch.

## F035 — "a tool already serves this" is the mission's least reliable verdict, and a third of what it can find lives in a corpus it never read

### What happened

E012 killed 19 of 50 harvested needs with one verdict. That verdict also killed
all twelve candidates from the six sealed reports, so no candidate has ever
survived it here. E016 re-adjudicated those 19 kills from scratch: phrasings
written from the clause text, three corpora, six positive controls run first,
attribution per item with the deciding text recorded, and a stopping rule that
forbids "none found" on a single query.

| arm | declared gate | result |
|---|---|---|
| 1, instrument validity | ≥ 5 of 6 positive controls re-adjudicated **served** | **6 of 6** |
| 2, the answer | ≥ 3 of the 13 judgement kills **no prior art found** on all three corpora | **3 of 12**, threshold met exactly |

### The observation

**The category is real but its basis was not, and the corpus that carries a
third of it had never been read by any prior-art probe in this repository.**

Of the thirteen kills with no populated count behind them:

- **9 served**, and the recoveries are strong rather than nominal:
  `akitaonrails/ai-memory` (8819 stars) describes "handoff between different
  agent vendors", which is item 5's clause verbatim; `dingdugan/model.tracker`
  is item 45; `git add -p` itself is item 42, one prompt in which `s` splits a
  hunk and `y` stages it.
- **3 found no prior art** on two GitHub phrasings, three registry keywords and
  two open-web phrasings each: item 7 (annotate once, choose the signal per code
  path at runtime), item 12 (tag HN posts and authors inside an HN client),
  item 16 (a daily word game that shows the solution order so a player can give
  up).
- **1 was never adjudicable**: item 0's clause asks for a game in which bots are
  allowed, while E012's reason — and therefore the phrasings — asked about
  Hacker News clients. The verdict was decided against the reason. That is a
  defect in the screen, not in the item, and it is recorded rather than
  repaired.

**Corpus carriage is the part that generalises.** GitHub's repository index
carried every verdict the code corpora carried (11 items). The registries
carried **none** on their own: PyPI's search endpoint answers a bot challenge,
so that leg became the complete 905,521-name index with no descriptions, and
npm and crates.io substring search is noise (`hn` → 1186 PyPI names, 588 npm
packages; `immutable os` → 46,733 npm packages). The open-web corpus carried
**4 of the served verdicts that two code corpora returned nothing for**, by name:

- **url-popularity** — two code corpora, 1 and 9 GitHub hits, nothing
  attributable. The open web returned twelve hosted services that take a URL and
  return a score or rank: `sitestackup.com`, `webanalyzer.dev`,
  `domainanalyzer.com`, `ahrefs.com/traffic-checker`, `similarweb.com/website/`,
  `domainrank.app/url-rating`, `toolszu.com`, `seoreviewtools.com`,
  `organicvisit.com`, `trafficchecker.net`, `backlinko.com`, `neilpatel.com`.
- **cpp-subset-linter** — Vector's PC-lint Plus, whose own page says static
  analysis "applies that enforcement automatically to MISRA C and C++, AUTOSAR,
  CERT-C, and CWE", which is what a restricted subset of C++ enforced by a linter
  is. Plus `cpp-linter`, MSVC's C26475 old-style-cast rule.
- **selective-stage** — `git add -p` and lazygit, neither of which either code
  corpus named.
- **interest-field** — contested, and counted as served to favour prior art:
  Tinder's Interests, Instagram's suggestion behaviour and LinkedIn's Interests
  section are all single-platform declared-interest fields; nothing named serves
  the cross-platform half.

### Where it sits on the threshold, stated rather than rounded

**Arm 2 landed on 3 with a threshold of 3, and one row decides it.** Item 16's
open-web results are ten lists of clones and ten answer-aggregator sites that
reveal solutions *outside* the game. A looser attribution rule that counted
those as serving the clause moves the count to 2 and reverses the declared
direction. The stricter rule is used, because the clause asks for a capability
and an answer site does not have it, and `results.json` carries both numbers so
a reader can move the row. The honest reading is therefore: **the declared
direction fires, but it fires on a margin of one row.**

### What changed

F029's cause table is restated. "38% already served" was the right number for
the wrong reason: the verdict was right on 9 of 12 adjudicable items and
unsound on 3, and the instrument that produced it was blind to a third of the
population it was judging. **Prior-art survival is not merely unreachable for
this mission's candidates (F026, F027); the verdict itself is the least
trustworthy instrument the mission owns, and it is the only instrument that has
killed every candidate.**

### A neighbouring finding, and what separates the two

The other VM's `F034`, landed 2026-10-05 while this ran, reads "the prior-art
screen's premise holds in mature vocabularies and largely fails in young ones"
(`EXPERIMENTS/015-incumbent-serving`; this file's findings are F035 and F036
after the collision, renumbered on the unpushed side). The two are complementary
rather than competing, and the difference is the axis: F034 asks whether a
screen's *premise* holds across vocabularies, and this one measures whether a
screen's *instrument* can see the population it judges. A screen can have a
sound premise and still be blind, and E016's four open-web-carried verdicts are
what that blindness looks like when the premise is fine.

### What it does not show

None of the three is a gap, a candidate, or useful. Item 16 sits beside 7658
wordle clones and item 12 beside 892 HN clients; an absence of a hit on three
corpora is the absence of a hit. Two of the three controls and both attributed
recoveries also show the mission's standing pattern from the other side —
`dingdugan/model.tracker` and all five of item 49's artifacts have 0 to 2 stars,
so **served and unused are the same state**, and this experiment measures
existence and never adoption.

## F036 — a web capture can answer HTTP 200 with results that have nothing to do with the query

### What happened

The third corpus was refused three times before one instrument worked, and the
first two failures had opposite shapes. DuckDuckGo's HTML and Lite endpoints
answered **202 with an image challenge** to every scripted query (19 of 19).
Startpage answered 200 with a **proof-of-work challenge**, `searx.be` a
**browser-verification page**, Mojeek 403, Brave 429 through the harness's
fetch tool, and the harness's own search tool returned `cancelled`.

Bing answered **HTTP 200 with ten well-formed organic results for each of all 38
declared queries** — and the results were unrelated to the queries. An immutable
Linux distribution query returned YouTube Music help pages; a lazygit query
returned Gmail sign-in pages and Zhihu answers. It did this with the malformed
User-Agent that was declared, and again with a corrected Firefox string.

### The observation

**Nothing inside the capture distinguishes a poisoned answer from a real one.**
38 queries, 380 results, every status field green, zero of them about the
question. A pipeline that recorded counts — as this one did, before the
attribution step existed — would have reported a complete, successful read of
the corpus. This is F032's class with a worse shape: there an HTTP 200 meant
*rate limited*; here it means *a different query was answered*.

The one instrument that worked, DuckDuckGo Lite through the harness's fetch tool,
was accepted only after a **known-answer control**: the query "lazygit terminal
UI stage hunk split hunk" returned nine of ten results about lazygit. That
control is also why item 42 names lazygit at all — neither declared phrasing
returned it.

### The rule, and the defect this session committed against it

An open-web probe carries three things or its output is not evidence: a
known-answer control, a nonsense-token control, and per-query result titles in
the record. A refusal is recorded as `refused` and never counted as an absence.

**Defect, in this session's own record-keeping:** `raw/web_log.jsonl` was
overwritten at its own path, breaking the append-only rule the experiment
protocol states. The 22 rows lost were all Brave 429 refusals whose bodies
survive as `raw/brave/*.log`, and the refusal is summarised in the row that
replaced them, so no decision here rests on what was lost — but the overwrite
happened and is recorded here rather than repaired quietly. This is the class of
F003 and F004, and it is the third time.