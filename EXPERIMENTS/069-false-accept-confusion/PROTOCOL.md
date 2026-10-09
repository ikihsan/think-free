<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E069 — do the 24 healthy-metadata false accepts cause real confusion?

Session `2026-10-08-027-explore-the-existence-checking-false-acc`, VM `instance-20260717-0944`, declared 2026-10-08.

## The question

E064 measured that 24 false-accept package names (mutations of popular seeds that resolve to real, different packages) have healthy metadata and evade a deterministic metadata rule. The installers' own typo guards only catch non-resolving names. **Whether that gap is observed anywhere — and whether a "did you mean" warning has a population that wants it — is untested** (D080, F099).

This experiment searches for real-world evidence of confusion between each seed-mutation pair.

## Seed-mutation pairs under test (the 24 residual from E064)

| Ecosystem | Seed (intended) | Mutation (false accept) | Mutation downloads/yr |
|---|---|---|---|
| crates | clap | clap-utils | 12,614 |
| crates | clap | fast-clap | 12,557 |
| crates | regex | regex-cli | 7,979 |
| crates | regex | regex-rs | 4,087 |
| crates | regex | simple-regex | 3,015 |
| crates | tokio | tokio-go | 5,781 |
| gem | redis | async-redis | 863,051 |
| gem | rspec | async-rspec | 560,528 |
| npm | chalk | chalk-cli | 430,003 |
| npm | winston | winston-cli | (unknown) |
| pypi | typer | async-typer | 646,800 |
| pypi | boto3 | boto3-utils | (unknown) |
| pypi | click | django-click | 1,706,868 |
| pypi | rich | django-rich | (unknown) |
| pypi | typer | django-typer | 1,638,528 |
| pypi | jinja2 | jinja2-cli | 11,164,368 |
| pypi | pydantic | pydantic-cli | (unknown) |
| pypi | requests | requests-go | (unknown) |
| pypi | requests | requests-rs | (unknown) |
| pypi | requests | requests-utils | (unknown) |
| pypi | rich | rich-cli | 265,656 |
| pypi | sqlalchemy | sqlalchemy-utils | (unknown) |
| pypi | tenacity | tenacity-rs | (unknown) |
| pypi | typer | typer-cli | 485,772 |

## Claim

**At least one of these pairs causes measurable user confusion** — evidenced by GitHub issues, Stack Overflow questions, bug reports, or installer feature requests where a user intended the seed but got the mutation (or a model suggested the mutation).

## Strongest baseline

Current installer behaviour: `pip install`, `npm install`, `cargo add` — no semantic warning, only existence check.

## Kill gate (G1)

**If the total credible confusion reports across all 24 pairs is < 10, or the confusion rate (reports / seed annual downloads) is < 0.001% for every pair, the population wanting a "did you mean" warning does not exist and no prototype is built.**

Rationale: The highest-download mutation is `jinja2-cli` at 11M/yr. Even 10 reports would be < 0.0001%. A feature serving < 10 users/year across the entire ecosystem is not a population.

## Search strategy (G2)

For each pair, search:

1. **GitHub Issues** (seed repo + mutation repo): `mutation_name` in seed repo issues; `seed_name` in mutation repo issues
2. **Stack Overflow**: `"seed_name" "mutation_name"` OR `"meant to install" "mutation_name"` OR `"accidentally installed" "mutation_name"`
3. **npm/pypi/cargo issue trackers**: search for typo/confusion reports mentioning both names
4. **GitHub Code Search**: `requirements.txt` / `package.json` / `Cargo.toml` containing mutation where seed was likely intended (context clues: comments, adjacent packages)
5. **Reddit/HN/Twitter**: manual spot-check for top 5 pairs by volume

All searches use public APIs only (GitHub REST, Stack Exchange API, no auth required). Rate limits respected.

## Negative controls (G3)

- Search for confusion between each seed and a **random non-mutation package** (e.g., `requests` vs `urllib3`) — should yield similar or higher noise
- Search for `"typo"` + seed name in issues — measures baseline typo-report rate

## Thresholds

- **Credible report**: Issue/question explicitly states confusion between the two names, or shows mutation in config where seed was clearly intended (e.g., comment "# jinja2" next to `jinja2-cli`)
- **Not credible**: Feature requests for the mutation, unrelated mentions, dependency resolution errors

## Resource limits

- GitHub API: 10 req/min unauthenticated (conservative)
- Stack Exchange API: 30 req/sec, 10k/day
- Max 2 hours wall time
- Results recorded in `raw/search-results.jsonl`

## Oracle

Human review of each candidate hit. Two passes: first pass filters obvious non-hits; second pass confirms credibility. Agreement required.

## Reproduce

```bash
cd EXPERIMENTS/069-false-accept-confusion
python3 search.py      # runs all searches, writes raw/search-results.jsonl
python3 review.py      # human review, writes raw/reviewed.jsonl
python3 outcome.py     # computes G1, G2, G3 verdicts
```