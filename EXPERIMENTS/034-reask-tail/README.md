# E034 — the questions people re-ask are in the score tail, and every surface a person reads shows them last

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

**Date:** declared, run and reported 2026-10-06. Task T-0078. Protocol in
[`PROTOCOL.md`](PROTOCOL.md) before any fetch of the declared population, amended once:
**AMENDMENT-1** (§7) added the out-of-sample replication and the site/tag confound test,
and it is disclosed as added after the run rather than folded into the declaration;
**AMENDMENT-2** (§7a), written after the run, records that AMENDMENT-1's own R2 gate was
**ill-formed before the fetch** and leaves §7 as declared rather than rewriting it.
**F057** records the two declared claims that failed. Fetches in
[`raw/pages.jsonl`](raw/pages.jsonl) — 101 requests, every response body committed
beside its sha256 — and the population in
[`raw/harvest.jsonl`](raw/harvest.jsonl), [`raw/r1.jsonl`](raw/r1.jsonl),
[`raw/r2.jsonl`](raw/r2.jsonl).

Reproduce: `python3 EXPERIMENTS/034-reask-tail/tally.py --check` (integrity, exits 0),
`--gates` (gate outcomes, exits 3 while D6 and B1 fail, which is the result), and
`python3 check.py` (45 behavioural checks plus 17 mutations of `reask.py` and
`measures.py` that must all be caught). `reask.py report` prints the per-sample table;
`reask.py harvest` and `reask.py replicate` dispatch to `harvest.py`, so `report` does not
import an HTTP client. `measures.py` holds the statistics with no gate attached and
`tally.py` the gate table, split the same way as E033's `descriptive.py`.

**One gap in the record, stated rather than papered over.** `session finish` reported the
five files under `raw/` as changed-but-undeclared: they were fetched by the reader after
the artifact declarations were made, and a closed session accepts nothing further. They
are committed and `tally.py --check` re-hashes every one of the 101 logged response
bodies against the `sha256` beside it, so a reader can verify them — but they are not in
the session's declared artifact set, and this line is the only place that says so.

**One defect was introduced and caught in this session's own refactor, and the harness
now holds it.** `reask.load()` returns every sample, so a gate table built from it
double-counted the two tags R1 re-reads at a later page and reported the *replication*
back as the result — pooled tail 0.1582 instead of 0.1352, every interval still
plausible, every gate still in the same direction. `measures.build()` now reads the
declared sample explicitly, asserts no amendment row is present, and `falsify.py`'s
seventeenth mutation puts the bug back to prove a check catches it.

## Verdict

**The pooled gradient fires on every variant, the per-tag spread fires and replicates,
and the two claims that would make this a diagnostic both fail.** A4, the declared kill
gate, fires — so this is not a methodological note — but D6 says the spread cannot be
apportioned between tag and site, and B1 says nothing distinguishes these repeats from
the ones the Active tab already shows.

| gate | rule | result |
|---|---|---|
| **A1a** | every logged request 200 | **passes** — 101 of 101 || **A1b** | no row is closed without stating a reason | **passes** — 0 of 2514 (substitution for the declared key rule, see below) |
| **A1c/A1d** | declared disclosures | 1790 rows carry no `closed_reason` key; **9 carry `exact duplicate`**, which the primary label excludes |
| **A2** | ≥3 of 8 tags have a tail duplicate | **passes** — 7 of 8 |
| **A3a** | pooled tail CI95 lower > pooled **Active tab** CI95 upper | **fires** — 0.1122 > 0.0455 |
| **A3b** | pooled tail CI95 lower > pooled head CI95 upper | **fires** — 0.1122 > 0.0542 |
| **A3b/A3a matched-n** | same on equal denominators | **fires** — 0.1208 > 0.0542 and > 0.0436 |
| **A4** | two tags with tail n≥50 have disjoint tail CI95s — **KILL GATE** | **fires** — 7 tags eligible, **12 disjoint pairs** |
| **R1** | AMENDMENT-1: the two tags that decide A4 reproduce on the next pages | **passes** — `customs` 0.430→0.495, `excel-formula` 0.000→0.000 |
| **D6** | within-site tag pairs separate as often as cross-site pairs | **FAILS** — 4/10 = 0.40 against 14/26 = 0.54 |
| **B1** | tail−default share of duplicates with no accepted answer, CI95 excludes 0 | **FAILS** — [−0.0774, +0.3075] |
| **D7** | declared disclosure: the gradient inside the tail | score ≤ −3: 61/650 = 0.0938; score −2..0: **37/75 = 0.4933**; **scores ≥ +1: none fetched** |

Denominators throughout are the **fetched row count after removing overlap** between the
declared population and the two amendment samples, which is why 2124 declared + 200 R1 +
200 R2 reads as **2514** rather than 2524: the paginated ordering is not perfectly stable
across a page boundary, so 4 R1 rows and 6 R2 rows were already declared. `tally.py`
removes them and reports each count rather than calling either sample disjoint.

## The number that holds

Three matched arms, same route, same filter, same page budget, 2124 rows over eight tags:

| arm | what it is | n | duplicates | rate | CI95 | score range |
|---|---|---|---|---|---|---|
| `tail` | `sort=votes&order=asc` | 725 | 98 | **0.1352** | [0.1122, 0.1620] | −85 … 0 |
| `head` | `sort=votes&order=desc` — what E032's `sort=votes` drew | 674 | 25 | 0.0371 | [0.0252, 0.0542] | 30 … 27242 |
| `default` | `sort=activity&order=desc` — **the `Active` tab** | 725 | 22 | **0.0303** | [0.0201, 0.0455] | −11 … 5855 |

**4.5× against the feed a person actually reads**, and the Active-tab arm is the
strongest alternative available rather than a deliberately weak one: it is the platform's
own default ordering of the same tag, on the same rows, with the same label. Equal
denominators (674 per arm) move the tail to 0.1454 and change nothing.

This replicates F055's whole-site 4.5× gradient on an independent, tag-stratified
population with a platform-owned label. **F055 stands, and is now measured twice, in two
different designs.**

## The number that is new

Nothing in this record had measured the rate *per tag*. It spans **0.000 to 0.493**:

| tag | site | tail | CI95 | Active tab |
|---|---|---|---|---|
| `excel-formula` | stackoverflow | **0.0000** | [0.0000, 0.0370] | 0.0300 |
| `probability` | math | 0.0200 | [0.0055, 0.0700] | 0.0100 |
| `linear-algebra` | math | 0.0500 | [0.0215, 0.1118] | 0.0400 |
| `docker` | stackoverflow | 0.0800 | [0.0222, 0.2497] | 0.0400 |
| `git` | stackoverflow | 0.1200 | [0.0700, 0.1981] | 0.0200 |
| `python` | stackoverflow | 0.1500 | [0.0931, 0.2328] | 0.0400 |
| `regex` | stackoverflow | 0.1900 | [0.1251, 0.2778] | 0.0500 |
| `customs` | travel | **0.4300** | [0.3373, 0.5278] | 0.0200 |

Seven tags clear the n ≥ 50 floor and **12 of their pairs are disjoint**. AMENDMENT-1's
R1 arm re-read the next four pages of the two tags that decide A4: `customs` **0.4948**
[0.3975, 0.5926] against the declared 0.4300, and `excel-formula` **0.0000** against
0.0000. Both extremes are out-of-sample facts, not page-window artefacts. The
`customs` closures are **43 distinct askers over 28 distinct months from 2013 to 2025**,
so this is a standing property of that tag and not a moderator's one afternoon.

**The Active tab shows none of this.** It reads 0.02 where the tail reads 0.43 for
`customs`, and it reads 0.03 where the tail reads 0.00 for `excel-formula`. A reader
watching the feed would conclude those two tags are the same, and would be wrong in
opposite directions.

## Two declared claims that failed

**The a-priori stratum hypothesis is falsified.** §3 predicted that tags whose questions
are specific to a situation would have the *worst* findability, on the reasoning that one
obvious canonical answer makes a tag findable. The prediction is backwards on this
population: `excel-formula` — the situational exemplar — has the **lowest** tail rate of
all ten tags at 0/100, and the "one canonical answer exists" tags (`git`, `regex`,
`python`) sit at 0.12–0.19. The hypothesis was declared before the fetch and it is dead;
nothing in this run explains what replaces it.

**The spread is not apportioned between tag and site.** `customs` was the only `travel`
tag in the declared population, so tag and site were confounded, and duplicate closure is
a **moderator act** — a community's closing practice is a first-class explanation of a
rate E034 cannot see. AMENDMENT-1 added one more tag on each of the two sites that
produced an extreme: `travel`/`baggage` **0.1979** [0.1305, 0.2886] and
`math`/`calculus` **0.1020** [0.0564, 0.1777]. The declared R2 gate was written as
"disjoint from both math tags", and it is **ill-formed**: `baggage` overlaps `calculus`
while being disjoint from `probability` and `linear-algebra`, so both of its branches
could fire. The unambiguous statistic is **D6** — how often two tags on the *same* site
separate at all — and it answers 4/10 within-site against 14/26 cross-site.

**So site carries a real part of the variance and tag carries a real part, and this
design cannot say how much of each.** The per-tag reading is therefore **not
established**, which is the thing a diagnostic product would be for.

## The mechanism claim fails, and it is the load-bearing one

The proposed application says a duplicate closure records *"the answer existed and was
not found."* B1 tested the observable half of that: among rows closed as duplicates,
the share carrying no accepted answer. Tail **0.8163** [0.7282, 0.8805], Active tab
**0.7273** [0.5185, 0.8685], difference **CI95 [−0.0774, +0.3075]** — spans zero. E033
already recorded the shape of this error (AMENDMENT-3 §2): closing a question as a
duplicate does not answer it, so most of the gap is *what closure does*, not what askers
needed. **This run cannot tell "people re-asked it" from "moderators closed it", and it
cannot tell "nobody answered" from "the platform's closure hides the answer".**

What is established is narrower and still worth something: **where the repeats sit, not
what happened to them.**

## Two instrument facts other work should not have to re-derive

**The canonical edge is unreachable.** E033 left this open with four vectorised `{ids}`
routes, the question page and StackPrinter all failing. This session added the question's
**comments** (the system "already has an answer here" banner is not among them), the
**answer's `closed_details`**, a browser User-Agent on two hosts, both StackPrinter hosts,
and the **SEDE archive**. All six fail: Cloudflare 403 on the question page,
`stackoverflow.com` and SEDE; StackPrinter's 1213-byte "server too busy" page on four
requests; no system comment; no `closed_details`. Nine channels in all
([`measures.py`](measures.py) `CHANNELS`). **E033's live question "what to measure
recurrence on" is answered on its other half: the label is available and the edge is not,
so any instrument here is built on the label alone.**

**The label is a set of literals, not one.** `closed_reason` was absent on all 1790 open
rows and present on every one of the 724 closed rows — no row is closed without stating
a reason, so absence means "not closed" and nothing is imputed. But the field carries
**ten** distinct literals, and `exact duplicate` (9 rows) is the legacy spelling of
the same moderation act as `Duplicate` (222). The declared label is the exact literal,
which is conservative and raises the pooled tail rate from 0.1352 to 0.1462 if the legacy
spelling is included. **E033's 0.0540 is a floor for the same reason.**

## Reverse causation, partly answered

The tail arm is the *most downvoted* questions, and a question closed as a duplicate may
earn downvotes *because* it was closed — which would make the whole gradient an artefact
of the outcome. D7 splits the tail arm by score: **score ≤ −3 is 0.0938, score −2..0 is
0.4933.** If closure drove downvotes, the most-downvoted band would be the densest, and
it is the *least* dense; the peak sits at score 0. That is evidence against the reverse
path and it is not proof, because **the tail arm contains no row with score ≥ +1** — four
pages of `order=asc` stops at 0 — so the comparison is {score ≤ 0} against {score ≥ 30}
with a gap E034 never sampled.

## What this does and does not settle

**It settles:** F055's gradient, twice; a per-domain rate this record had never measured,
reproducing out of sample at both extremes; where the repeats sit relative to the feed a
person reads; and the unreachability of the canonical.

**It does not settle:** whether the per-tag spread is a property of the tag or of the
site's moderation practice (D6 failed); what happened to the repeats (B1 failed); whether
anyone acts on the reading (unmeasured, and the whole adoption question); and the
declared stratum hypothesis, which is falsified with no replacement.

**It is not a product.** `reask.py` is a reader that costs 85 requests for eight tags and
prints a table. Its value so far is that one generation of measurement in this record is
now reproducible from committed bytes by someone who did not run it, which four earlier
demand-side generators could not claim. Nothing here is a prior-art screen, a novelty
claim, or evidence of usefulness to anyone outside it.

**The single next action** is the one D6 names: **more tags per site**, three to four
more on each of the three sites, `tail` arm only, 4 pages each — about 30 requests against
tomorrow's 300. That is the only measurement standing between this population and the
per-tag reading, and it is cheap enough to be worth doing before anything is built on
top of it.
