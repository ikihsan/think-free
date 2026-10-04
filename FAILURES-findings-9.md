<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Failures — recorded findings, part 9 (F029)


Source: session `2026-10-04-044`. The candidate generator tested here was a live
harvest of practitioner need statements; it is refuted, and the corpus is kept
demoted. Runnable evidence: `EXPERIMENTS/012-candidate-harvest/`.

## F029 — A live corpus of unmet needs produced no candidate that survives the screens

Source: session `2026-10-04-044`, 2026-10-04, this VM. Every number is
re-runnable from `EXPERIMENTS/012-candidate-harvest/`. Nothing here is a claim
about any candidate, and no candidate moved as a result.

## The question, and why it was worth one session

F031 measured that the mission was spending its effort on its own record and
that [`STATE-next-actions.md`](STATE-next-actions.md) carried no action able to
produce a candidate. D048 gave that list an invention seat, and the seat's own
text said the next informative candidate is one "generated from live sources".
Six sealed reports had produced sixteen candidates, thirteen of them dead, and
those reports were written by one model family sharing its priors —
`RESEARCH/SYNTHESIS.md` says so itself. So: **is a different generator better?**

## What was done

`harvest_needs.py` queried Hacker News' public Algolia index for comments
containing an unmet-need phrase, restricted to comments created after
2024-01-01, dropping link dumps. **1401 need statements from 20220 scanned
comments**, each with its comment id, story title and creation date — a countable,
dated, re-harvestable corpus rather than a remembered impression.

`sample_needs.py` then drew 50 of them by a stated rule (clause of at least six
words, sorted newest first, every 21st survivor) so the sample could not be
chosen for looking promising. `screen_sample.py` gives each item a cause of
death in the same categories the record already uses for the sixteen prior
candidates.

## Observed

**Zero of 50 survived.** The causes of death:

| cause | n | share |
|---|---|---|
| `prior_art` — a tool already serves it | 19 | 38% |
| `vague` — the clause states no mechanism, so nothing can be tested | 15 | 30% |
| `not_a_software_need` — asks for a regulation, a price, a community, a document | 12 | 24% |
| `needs_hardware` — needs a device, a room, a person | 4 | 8% |

**The prior generator, on the record's own numbers: 3 of 16 live** (C2, E2, E3,
`RESEARCH/SYNTHESIS.md`), of which one stopped (F008), one's candidate died of
its own confirmed mechanism (F012), and one is time-gated. Zero validated.
**18.75% against 0%.** Switching the mission's candidate generator to live need
harvesting is refuted on this evidence.

**Why, past the tally.** A need clause is a *want*; a candidate is a *mechanism
plus a witness*. Sixty per cent of the sample never states a mechanism, so there
is nothing to falsify, and 38% is already solved — which is what a corpus of
asks actually consists of. Supplying the mechanism is the step the prior method
already performed, so harvesting substitutes the problem statement and does not
substitute the candidate.

**The corpus has no recurrence signal, and that is measurable.** Term-frequency
recurrence over 1273 clauses returns only function words — the highest-scoring
content term appears in six. `single_reporter` cannot be separated from
`shared_need` from inside a corpus of single comments.

**The constructive half, which is the reason to keep the finding.** The missing
signal *is* obtainable from a countable corpus with a different unit.
`recurrence_probe.py` searched GitHub issues for the one cluster that recurred by
eye in the harvest — coding agents making changes nobody asked for:

| query | open issues | distinct repos in first 30 |
|---|---|---|
| `"not asked for"` | 5805 | 28 |
| `"unrelated changes"` | 14510 | 29 |
| `"scope creep" agent` | 2234 | 22 |
| `"unrelated file" copilot` | 413 | 19 |

`claude-code`, `claude_skills`, `copilot-cli`, `gh-aw`, `agent-guard`,
`agent-interface` and `HumanOversightSystem` are in those sets. The unit that
carries the information is **the repository, not the request**: a thousand
issues in one project is one project's problem.

## The finding was falsified against itself

`verify_prior_art.py` re-checked 10 of the 19 `prior_art` verdicts against
population counts, because that verdict is a judgement and a wrong one would
invalidate the headline.

- **6 supported** by a populated count: `anki` 31750 stars (flashcards, 2030
  repos), `uptime-kuma` 92112 (monitoring, 10768), s3-alternative 172,
  `Vanilla-OS/ABRoot` 392, webp encoding 115, calibre tooling 13.
- **4 could not be verified** by the query chosen: selective staging (1),
  runtime instrumentation (7), model-changelog tracking (1), gdrive disk usage
  (2).

**Reversing all four unverified verdicts still yields no survivor**, and the
headline is robust to that: #42 fails Screen 3 (git add -p and `jj` exist),
#7 fails Screen 1 (needs eBPF and a fleet this VM does not have), #45 fails
Screen 3 (OpenRouter publishes changelogs), #49 is a thin niche needing an
account. That is the falsification in the useful direction: the conclusion does
not rest on the part of the measurement that is weakest.

## What it does not show, stated before anything is built on it

- **The verdicts are judgements.** Ten of nineteen were spot-checked; the other
  nine are not, and the four that failed are recorded as unverified rather than
  as gaps.
- **A thin count is not a gap.** `verify_prior_art.py` returning 1 hit for
  selective staging does not mean nothing exists — the same script returns
  10768 for monitoring, and F030 is about exactly this.
- **Issue counts are self-selected and full-text.** `"unrelated changes"` in
  14510 issues is a floor, not a population, and many hits are low-signal
  repositories. Filtering by repository signal is required before the number
  means anything.
- **One HN corpus, one and a half years, one audience.** Fifty items is a
  sample; it is enough to refute "this generator yields candidates" and not
  enough to rank generators.
- **Zero validated candidates were produced by this session either.** The
  screens did what they are for.

## What it licenses

Live harvesting is demoted from *candidate generator* to *dated, countable
problem-statement corpus*, and the pipeline's missing ingredient is named
instead: **a filtered recurrence signal from a repository-denominated issue
corpus.** D049. The next action is to build that filter and re-harvest through
it, and the cluster with the strongest measured recurrence — unrequested agent
edits — is the one to test first, with its own falsification.
