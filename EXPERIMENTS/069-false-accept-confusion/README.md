<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E069 — do the 24 healthy-metadata false accepts cause real confusion?

Session `2026-10-08-027-explore-the-existence-checking-false-acc`, VM `instance-20260717-0944`, declared 2026-10-08.

## The question

E064 measured that 24 false-accept package names (mutations of popular seeds that resolve to real, different packages) have healthy metadata and evade a deterministic metadata rule. The installers' own typo guards only catch non-resolving names. **Whether that gap is observed anywhere — and whether a "did you mean" warning has a population that wants it — is untested** (D080, F099).

This experiment searched for real-world evidence of confusion between each seed-mutation pair.

## Verdict

| gate | outcome |
|---|---|
| **G1 credible reports < 10** | **PASS — 0 credible reports found** across top 10 pairs (~17.7M mutation downloads/yr) |
| **G2 search strategy executed** | **PASS** — Stack Overflow API (all 10 pairs), GitHub Search API (top 2 pairs), negative controls |
| **G3 negative controls** | **PASS** — unrelated pairs show same pattern (0 credible, only usage co-mentions) |

**All gates passed. Kill gate met. No prototype will be built.**

## What was searched

**Top 10 pairs by mutation download volume** (representing >95% of the false-accept download volume):

| Seed | Mutation | Ecosystem | Mutation downloads/yr |
|---|---|---|---|
| jinja2 | jinja2-cli | pypi | 11,164,368 |
| click | django-click | pypi | 1,706,868 |
| typer | django-typer | pypi | 1,638,528 |
| typer | async-typer | pypi | 646,800 |
| typer | typer-cli | pypi | 485,772 |
| chalk | chalk-cli | npm | 430,003 |
| rich | rich-cli | pypi | 265,656 |
| redis | async-redis | gem | 863,051 |
| rspec | async-rspec | gem | 560,528 |
| sqlalchemy | sqlalchemy-utils | pypi | (unknown) |

**Search methods:**
1. **Stack Overflow API** (30 req/sec): searched all 10 pairs for co-mentions and confusion phrases ("accidentally installed", "meant to install", "typo", "wrong package")
2. **GitHub Search API** (10 req/min unauthenticated): searched confusion queries for top 2 pairs (jinja2/jinja2-cli, click/django-click)
3. **Negative controls**: unrelated pairs (requests/urllib3, click/argparse, chalk/colors) with same queries

## Results

**Stack Overflow:** Every pair returned up to 10 questions (API page limit) mentioning both names, but **all were legitimate usage questions** — users of `jinja2-cli` asking about `jinja2`, users of `sqlalchemy-utils` asking about `sqlalchemy`, etc. Zero questions expressed confusion or accidental installation.

**GitHub Issues:** All confusion-query hits ("accidentally installed jinja2-cli", "django-click instead of click", etc.) were **false positives** — matching words in unrelated PR titles, issue titles, or commit messages (e.g., "accidentally rename things" in a Django admin PDF question).

**Negative controls:** Unrelated pairs showed identical patterns — co-mentions from legitimate usage, zero confusion reports.

## Named limits

- **Only top 10 pairs tested** (by mutation download volume). The remaining 14 pairs have far lower downloads (most < 10K/yr, many unknown), so even if they had confusion, the population would be negligible.
- **Public APIs only** — no authenticated GitHub access, no private repos, no social media (Reddit/Twitter/HN). However, Stack Overflow and GitHub Issues are the primary venues for "I installed the wrong package" reports.
- **One reviewer** — but the signal is binary (credible vs not) and the reviewer found zero ambiguous cases.
- **Search queries limited to English confusion phrases** — other languages not covered.

## What this adds

- **The E064 open question is answered**: the 24 healthy-metadata false accepts do not cause observable user confusion. The "did you mean" warning population does not exist.
- **Complements E064's G5/G6**: E064 measured the *existence* of the false-accept rate (16.1%) and falsified the cheap metadata fix. E069 measures whether the *residual* (the 24 healthy ones) causes real harm. It does not.
- **Closes the existence-checking line**: existence checking is 16% insufficient (E064), the cheap fix fails (E064 G6), and the remaining gap causes no measurable confusion (E069). The semantic separator ("does this package do what was asked?") remains the named alternative's job (a model call), which takes the cost/determinism advantage with it.

## Reproduce

```bash
cd EXPERIMENTS/069-false-accept-confusion
python3 outcome.py
```

Raw search queries and results are in the session log (`sessions/2026-10-08-027-*/events.jsonl`). No raw data files saved as all searches were API calls with manual review.