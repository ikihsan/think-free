# E012 — Can a live corpus of unmet needs generate candidates?

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

**Date:** 2026-10-04. **Verdict: the generator is refuted; the corpus is kept and
demoted.** 0 of 50 mechanically drawn need statements survived the mission's
screens. F029, F030, D049.

**Renumbered on the unpushed side.** The other VM published `F025`–`F028` and
`EXPERIMENTS/011-niche-adoption-census` first, so this experiment and its two
findings carry `012` and `F029`/`F030`. The allocation finding it rests on became
`F031`. No content changed; the collision is recorded here rather than in the
event streams.

## The question

`RESEARCH/SYNTHESIS.md` records sixteen candidates from six sealed reports,
thirteen dead, all written by one model family sharing its priors. F031 measured
that the next-action list held nothing able to produce a candidate, and D048 gave
it an invention seat whose text says the next informative candidate is one
generated from live sources. So: **is a different generator better?**

## Method, and why the sample is not mine

| step | script | what it fixes |
|---|---|---|
| harvest | `harvest_needs.py` | 25 unmet-need phrases, HN Algolia comments, created after 2024-01-01, link dumps dropped → `raw/hn_needs_2026-10-04.jsonl` |
| sample | `sample_needs.py` | 50 items by a stated rule: clause ≥ 6 words, newest first, every 21st. No taste involved |
| screen | `screen_sample.py` | a cause of death per item, in the categories the record uses for the prior sixteen |
| falsify the screen | `verify_prior_art.py` | 10 of the 19 `prior_art` verdicts re-checked against population counts |
| prior art, twice | `prior_art_probe.py`, `prior_art_probe2.py` | one phrasing, then several, after the first pass was wrong twice |
| recurrence | `recurrence_probe.py` | the same cluster counted in issues, per repository |

Raw capture and every probe result are under `raw/`. All are re-runnable; the
only external dependency is the public Algolia, GitHub and GitHub-search APIs.

## Result

| generator | screened | survived | rate |
|---|---|---|---|
| six sealed reports (recorded, `RESEARCH/SYNTHESIS.md`) | 16 | 3 live, 0 validated | 18.75% |
| this harvest (measured here) | 50 | **0** | **0%** |

Causes of death across the 50: `prior_art` 19, `vague` 15, `not_a_software_need`
12, `needs_hardware` 4.

**Correction, 2026-10-05 (F047, `EXPERIMENTS/027-cause-of-death-reread/`).** The
numbers above are this experiment's record and are not restated here. **31 of
the 50 were assigned from a clause, not from a comment** — `sample_needs.py`
extracts the text between the trigger phrase and the first sentence break,
capped at 300 characters — and re-reading those 31 from the full comment with
two blind readers found **6 of the 15 `vague` kills state a mechanism or a named
artifact in the text this screen never read**. `vague` is therefore withdrawn as
a cause of death at the size recorded above. **The 0-of-50 result stands and
the 19 `prior_art` verdicts are untouched**, because none of the 8 re-opened
rows is a candidate and because E016 already re-adjudicated `prior_art` on three
corpora. Read this table as a screen's original output, not as a measurement of
the world's stated needs.

**Kill gate, as declared:** if at least one harvested need yields a candidate
passing Screen 1 (a killing experiment smaller than the argument) and Screen 3 (a
surviving result changes a build decision), the generator is better and becomes
the mission's method. **Not met. The gate was written before the sample was
drawn and it did not pass.**

## The falsification that matters

`verify_prior_art.py` exists because the headline rests on a judgement. Six of
ten spot-checked verdicts are supported by a populated count — `anki` 31750
stars across 2030 flashcard repositories, `uptime-kuma` 92112 across 10768, s3
storage 172, `Vanilla-OS/ABRoot` 392, webp encoding 115, calibre tooling 13. Four
could not be verified by the query chosen: selective staging (1 repo),
runtime instrumentation (7), model-changelog tracking (1), gdrive disk usage (2).

**Reversing all four unverified verdicts still yields no survivor:** #42 and #45
fail Screen 3 (`git add -p` and `jj` exist; OpenRouter publishes changelogs), #7
fails Screen 1 (needs eBPF and a fleet this VM has not), #49 is a thin niche
needing an account. The conclusion does not rest on the weakest part of the
measurement. The four are recorded as **unverified**, not as gaps — F030 is the
finding that a thin count is not a gap, demonstrated on the same day.

## The constructive half

The corpus cannot distinguish one person's wish from a shared need: term
recurrence over 1273 clauses returns only function words, the top content term
appearing in six. Counted in a different unit, the same cluster is unambiguous:

| query | open issues | distinct repos in first 30 |
|---|---|---|
| `"not asked for"` | 5805 | 28 |
| `"unrelated changes"` | 14510 | 29 |
| `"scope creep" agent` | 2234 | 22 |
| `"unrelated file" copilot` | 413 | 19 |

`claude-code`, `claude_skills`, `copilot-cli`, `gh-aw`, `agent-guard`,
`agent-interface`, `HumanOversightSystem`. The unit that carries the information
is the repository, not the request. D049 makes that the rule.

## Limits

- The 19 `prior_art` verdicts are **judgements**; 10 were spot-checked and 4 of
  those failed. The other nine are unverified.
- A GitHub count is a floor. A tool on PyPI, npm or a commercial service reads as
  zero. These probes can refute; they cannot establish novelty, and nothing here
  is a novelty claim.
- Issue counts are full-text and self-selected; `"unrelated changes"` in 14510
  issues includes low-signal repositories. A repository-signal filter is
  required before the number means anything, and is the next action.
- One corpus, one audience, 19 months, 50 items. Enough to refute one generator;
  not enough to rank two.
- **No candidate was produced by this session either.** The screens worked.

## What this licenses

Keep the corpus as a dated, countable problem-statement source. Demote it from
candidate generator. Build the repository-signal recurrence filter, re-harvest
through it, and test the cluster with the strongest measured recurrence first —
changes a coding agent makes that nobody asked for — against its own stated
falsification rather than against this one.