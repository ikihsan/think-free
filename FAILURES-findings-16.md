<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Failures — recorded findings, part 16 (F040)

Continues [`FAILURES-findings-15.md`](FAILURES-findings-15.md), which holds F039,
and [`FAILURES-findings-14.md`](FAILURES-findings-14.md), which holds F037
and F038. **Identifiers are stable across all findings files**: a reference to
`F040` means the same entry wherever it appears.

Source: session `2026-10-05-004`, task T-0064. Runnable evidence:
`EXPERIMENTS/020-copied-artifact-serving/` — `PROTOCOL.md` (the declaration),
`copycount.py`, `coverage.py`, `forkstatus.py`, `tally.py`, `results.json`, and
82 raw captures under `raw/`. Tests: `tests/test_copy_channel.py` (30).

## F040 — the prior-art screen's young-vocabulary failure is the world, not a channel it failed to look at

**Observed, 2026-10-05.** F037 left the prior-art premise's split — 4 of 4
on-topic incumbents served in mature vocabularies, 1 of 4 in a young one — with
one escape route standing: the artifact a coding-agent user puts in their
repository is a **directory they copy**, not a package they install, so every
channel the mission owns was reading the wrong thing. `STATE-next-actions.md`
item 0 named the testable form and said the honest proxy was a repository count
that **no public API serves**.

**A public unauthenticated API does serve it.** Sourcegraph's streaming search
endpoint returns repository-level counts for a path pattern, with no token. That
alone is a correction to the record: it removes the blocker item 0 was written
around.

**And the channel turns out to be the smaller one.**

| | figure |
|---|---|
| indexed repositories containing a `.claude/hooks/` directory | **1,026** (a floor) |
| young arm's total monthly installs, all four channels | **8,676** |
| ratio | **0.118** |

The declared gate needed **≥ 20×** to survive and **≤ 5×** to be dead, the
interval chosen so that "the channel we counted is not the channel the field
uses" would not be arguable. At 0.118 the copy channel is an **order of
magnitude smaller** than the install channel.

**So F037's reading does not hold.** *1 of 18 incumbents clears an install floor
while 14 of 18 have no readable channel* is not "a field that is used and
invisible to the instrument". It is a field whose visible use is thin. **The
screen was reading the dominant channel.** The young side of F034's original
split is now the world rather than the instrument, and the last escape route
F037 left open is closed by measurement rather than by argument.

### Two things the same run established

**The record's instrument premise was wrong, and the correction is not the
finding.** Having a copy channel at all does not make it the right one; what
makes it the wrong one is the 0.118.

**A direct count is not a benchmark.** A mature-vocabulary hook script is copied
into **more** repositories (1,770) than a young one (1,026), and a mature
pre-commit config into **18,989** — both saturated floors. Copying is what
configuration files do generally. It is not a coding-agent specialty, and the
C3 control is what says so; without it the 1,026 could be read as a young-vocab
signal when it is a configuration signal.

### What this rules out

- **It rules out the escape hatch, not the screen.** "Prior art exists" and "the
  need is served" are still different claims, and only the first has been in
  question. Nothing here reopens any of the twelve prior-art deaths.
- **It does not validate the install channels.** H1 compares two imperfect
  measures. It shows copying is not *more* important than installing; it does not
  show installing is measured well.
- **It is not attribution.** Whether any counted repository copied *this*
  artifact or independently wrote a similar one is not decidable from a path
  count. H1 is about a channel's volume.

### The second finding: this instrument is blind exactly where the candidates are

C2, the coverage control, is the one that could have refused the experiment. It
did not for the young arm — **17 of 18** young repositories are in the index — so
the 1,026 is a count on the population rather than on a blind spot.

**The placebo arm is 0 of 13.** 015 built those thirteen deliberately unpopular
repositories so that a figure there would announce an instrument defect, and this
instrument **cannot see a single one of them**. So it is not merely biased toward
popular projects: it is blind below whatever threshold GitHub stars cross, which
is precisely the region every candidate in this mission lives in. Any future use
of it inherits that blind spot, and it is a *different* blind spot from the
registry channels F037 ruled out.

### The six instrument defects this run found on itself

1. **A retry loop overwrote five good captures with refusals** — counts of 1, 1,
   1, 1 and 2, unrecoverable, and it cost the experiment half of H2. A capture
   holding an answer is now never overwritten; a refusal is written beside it.
2. **A substring match on overlapping path patterns** put
   `^\.claude/hooks/README\.md$`'s count of 42 on the broader
   `^\.claude/hooks/`. Matching is now on the recovered term, by equality.
3. **Two independent copies of one naming rule.** The consumer re-derived the raw
   filename; when the query header was added, all 22 configurations became
   `no_origin`. Naming is now one exported function.
4. **`copycount.json` was clobbered by every run**, silently discarding nine
   counts on a partial re-fetch. It merges now, and `--rebuild` re-derives the
   whole index from `raw/`.
5. **A capture could not be traced to its query** — the slug cannot distinguish
   `^\.claude/hooks/README\.md$` from `^\.claude/hooks/`. Every capture now
   carries a `# query:` line. Nine predate it and are recovered by slug, marked
   as such.
6. **Falsifying a test destroyed the evidence it was checking.** Restoring the
   overwrite defect and executing it overwrote the H1 capture itself. This is
   the sharpest instance of the class: **the repair for a defect was untested
   against the defect, and testing it destroyed a measurement.** `COPYCOUNT_PROTECT`
   now refuses to touch a capture holding a value other than the one the run was
   asked to reproduce. The H1 figure survived in this session's command log and
   in `forkstatus.json`; **the raw bytes did not**, and `results.json` says so.

**The pattern underneath all six is worth more than any of them.** The rate limit
is *positional*: it armed after ~30 requests from one host and every query after
it returned **HTTP 200 with an HTML challenge page** — F036's shape, in a
different instrument. The first coverage pass issued 61 queries unpaced and
**33 rows — every young row and every placebo row — came back as HTML.** That
reads as "the index does not contain the young arm", which is a clean, confident,
wrong finding about the world. It was caught only because C2 was declared to be
able to refuse the experiment and the refusal was recorded as a refusal.

Ceiling: one young vocabulary, one index, one afternoon. H2 needs a host the
endpoint will answer; its low band is a declared mechanical slice, so a rerun
needs no new decisions, only an unblocked endpoint.