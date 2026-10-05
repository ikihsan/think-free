# 020 — is the young vocabulary served by copies rather than installs?

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

**Date:** declared and run 2026-10-05. **T-0064.** The declaration is in
[`PROTOCOL.md`](PROTOCOL.md), written before any count on the population was
read. **H1 is `dead`; H2 is `not evaluable`.** F040.

## The two results

**H1 is dead, and it is dead in the direction that kills F037's escape hatch.**
The declared gate asked whether copying is a larger channel than installing,
needing ≥ 20× the young arm's install readings. **The copy channel is 0.12× —
an order of magnitude smaller, not larger.**

| | figure |
|---|---|
| indexed repositories containing a `.claude/hooks/` directory | **1,026** (a floor) |
| young arm's total monthly installs, all four channels | **8,676** |
| ratio | **0.118** |

The gate fires dead at ≤ 5×. F037 reasoned that *1 of 18 incumbents clears an
install floor while 14 of 18 have no readable channel* is "consistent with a
field that is **used and invisible to the instrument**". **That reading is now
measured and it does not hold.** A direct count of the artifact class those four
documents tell the reader to copy finds **a thousand repositories against nearly
nine thousand monthly installs** — the channel the screen already read was the
bigger one, not the smaller one.

So the young vocabulary's thin measured use is **not** an artefact of looking in
the wrong place. That is a genuine negative result, and it closes the last
escape route F037 left open. What remains unexplained is F034's original split —
4 of 4 on-topic incumbents served in mature vocabularies against 1 of 4 in a
young one — and this result says the young side of that split is **the world,
not the instrument**.

**H2 could not be answered, and the reason is this session's own doing.** The
gate asks whether forks and templates separate heavily-copied configurations from
barely-copied ones. Nine configurations cleared the high band (165 to 4,000
copies) and **none of their origin repositories is a fork or a template** — which
is the direction that would have supported the stand-in. But the low band is
empty, because the instrument began refusing queries partway through that half
and the retry loop overwrote the five answers it had already obtained. A rate
over one band is not the rate the gate declares, so it is reported
`not_evaluated`. **The nine high-band rows are recorded and the missing half is a
named cost, not a silent gap.**

## What the instrument premise in the record was, and is

`STATE-next-actions.md` item 0 states the cheapest honest proxy for "was this
copied" is a repository count that **"no public API serves"**, and that the first
move is therefore to decide whether forks, dependents or templates are an
adequate stand-in. **A public, unauthenticated API does serve it** — Sourcegraph's
streaming search endpoint returns repository-level counts for a path pattern.
This is `observed` on 2026-10-05, and it removes the blocker item 0 was written
around. It does not settle which signal is right, and the run below shows the
copy signal is the *weaker* of the two.

Its three ceilings are declared in the protocol and hold every number here:

- **a floor, not a census** — the index is a subset of GitHub;
- **forks and archived repositories are excluded by default**;
- **the `file:` pattern is a path glob, so a repository counts once** however many
  of its files match. A field with one copied directory and a field with fifty are
  the same row.

## Controls

| control | result | what it establishes |
|---|---|---|
| **C1 calibration** | `.github/workflows/ci.yml` 4,000 (saturated), `.pre-commit-config.yaml` 18,989 (saturated), `.githooks/pre-commit` 1,770, `.claude/hooks/` 1,026, **two absent paths 0 and 0** | the instrument distinguishes none from few from many, saturates where it should, and **a zero is a zero** — the control that F032's defect class required, run in both an anchored and a directory-shaped pattern |
| **C2 index coverage** | mature **30/30**, young **17/18**, placebo **0/13** | **the load-bearing control, and it did not refuse the experiment.** The young arm is in the index at 94%, so a count on it is a count on the population rather than on the instrument's blind spot |
| **C3 mature arm** | CI configuration 4,000+, pre-commit config 18,989, hook script 1,770 | **the young count is not remarkable.** A mature-vocabulary hook script is copied into *more* repositories (1,770) than a young one (1,026), and a mature config file into an order of magnitude more. Copying is what configurations do generally; it is not a coding-agent specialty |
| **C4 absent path** | 0, in two shapes | folded into C1 |

**C2's placebo arm is 0 of 13, and that is the second finding in this
experiment.** 015 built those thirteen deliberately unpopular repositories so
that a figure there would announce an instrument defect. The copy-count
instrument **cannot see a single one of them.** So this instrument is not merely
biased toward popular projects — it is blind below whatever threshold GitHub
stars cross, which is exactly the region every candidate in this mission lives
in. Any future use of it inherits that blind spot, and it is a different blind
spot from the registry channels F037 ruled out.

## Five instrument defects, all found by this run executing on itself

1. **A retry loop overwrote five good captures with refusals.** `fetch()` wrote
   every attempt to the same filename, so once the anti-bot challenge armed, each
   retry replaced a measured answer with an HTML page. The five lost figures were
   counts of 1, 1, 1, 1 and 2 — and nothing else recorded them, so H2's low band
   is gone. **A capture holding an answer is now never overwritten**; a refusal
   is written beside it as `.refused`. This cost the experiment half of H2, which
   is the honest price of writing the fetcher before the retry loop.
2. **A substring match on overlapping path patterns.** `^\.claude/hooks/` is a
   substring of `^\.claude/hooks/README\.md$`, so the broad hooks pattern took
   the narrow one's count of 42 and two configurations were misreported. Matching
   is now on the recovered `file:` term, by equality.
3. **Two independent copies of one naming rule.** The consumer re-derived the raw
   filename instead of calling the writer's function; when the query header was
   added to the capture, all 22 configurations became `no_origin`. Naming is now
   one exported function, `copycount.capture_name`, and anything that needs to
   find a capture calls it.
4. **`copycount.json` was clobbered by every run**, so re-fetching three patterns
   to add a hook path silently discarded nine counts. It is now merged, and
   `--rebuild` re-derives the whole index from `raw/` — which is how the ten lost
   counts came back.
5. **A raw capture could not be traced to its query.** The file recorded only its
   own slug, and the slug cannot distinguish `^\.claude/hooks/README\.md$` from
   `^\.claude/hooks/`. Every capture now carries a `# query:` first line. Nine
   captures predate it; they are recovered through the slug and marked
   `attributed_by: slug` rather than being treated as attributed.

**A sixth, which is the pattern rather than the instance.** The rate limit is
positional: it armed after ~30 requests from one host, and every query after it
returned HTTP 200 with an HTML challenge page — **F036's shape, again, in a
different instrument.** `copycount.detect_challenge` names the marker so a
challenge is a *named* refusal rather than a mysterious parse failure, and
`coverage.py` retries only what is unanswered and backs off on a streak. The
first coverage pass issued 61 queries unpaced and **33 rows — every young row and
every placebo row — came back as HTML**, which read as "the index does not contain
the young arm" until C2 was rerun with pacing and returned 17 of 18. **Had that
first pass been reported, it would have been a clean, confident, wrong finding
about the world.**

## What this does not settle

- **Attribution.** Whether any counted repository copied *this* artifact or wrote
  something similar is not decidable from a path count. H1 is about a channel's
  volume. Reading `dead` as "these incumbents are not serving" would overreach in
  the other direction, and it is equally unsupported.
- **One vocabulary, one index, one afternoon.**
- **Nothing here reopens a prior-art death.** F035 already established that "no
  prior art found" means the absence of a hit. What changed is narrower: the
  screen's young-vocabulary premise is now supported rather than merely
  undefended, because the alternative explanation has been measured and is small.
- **The install channels are not thereby validated.** H1 compares two imperfect
  measures. It shows copying is not *more* important than installing; it does not
  show that installing is measured well.

## The decision this changes

`STATE-next-actions.md` item 0 asked whether the serving signal for a young
vocabulary is forks and dependents rather than installs, and named the copy count
as the honest proxy. **Both halves are now answered in the negative**: the copy
channel is 0.12× the install channel, and the configurations that do get copied
en masse are mature ones (18,989 for a pre-commit config against 1,026 for
coding-agent hooks).

So the selection axis item 0 defers to the owner cannot be "find the channel the
instrument was missing" — there is no such channel here, and F028, F032 and F037
already established that supply-side counts do not speak for demand. What is left
is the narrower question the item already named, with F040 removing the escape
hatch it was holding open: **the prior-art screen is not obviously wrong in young
vocabularies, which means the twelve deaths stand unless something other than the
screen is wrong.** That is an uncomfortable result and it is the measured one.

## Method

| step | script | what it fixes |
|---|---|---|
| format | `captureformat.py` | what a capture on disk **means**: its `# query:` header, challenge detection, the saturation ceiling, and `rebuild_index()`, which re-derives the index from `raw/` |
| lookup | `captureindex.py` | which capture answers a given path pattern — equality on the recovered term, escaping canonicalised, largest count across ceiling variants, slug fallback marked as such |
| fetch | `copycount.py` | one paced query per pattern, capture written before parsing, a challenge named as a refusal, an answer never overwritten |
| coverage | `coverage.py` | C2, from 017's committed artifacts; retries only unanswered rows and backs off on a refusal streak |
| forks | `forkstatus.py` | H2: copy count per configuration, then `fork` and `is_template` from GitHub's core API for the repository shipping the path |
| verdict | `tally.py` | both gates, all four controls, H1's recovery from the records that still hold it, and every refusal recorded rather than dropped |

`captureformat`, `captureindex`, `coverage` and `forkstatus` were one file until the
300-line cap; they are split by invariant, and each split is a fault line — the
lookups, the fetcher and the verdict each had their own defect, and none of the
three defects was visible from the other two.

Tests: `tests/test_copy_channel.py` (the capture format) and
`tests/test_copy_channel_gates.py` (both gates and all four controls), which hold
each defect above against the committed captures rather than against a fixture.

## Limits on the ceiling

- H2 needs re-running from a host the index will answer. The high band's nine
  rows are on disk and the low band's twelve patterns are declared by a
  mechanical slice (`low_band_paths`, every 400th hook path the index returned),
  so a rerun needs no new decisions — only an unblocked endpoint.
- The instrument cannot see the 13 placebo repositories, so **it cannot be used
  to argue anything about unpopular work**, which is where this mission's
  candidates are. Any follow-up needs a second corpus the instrument does cover.