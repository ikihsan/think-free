<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# 013 — does a crowded niche mean a solved one? (E, T-0059)

F027 and F028 counted **stars**. This counts **installs**, because "does prior
art exist" only means "is this problem solved" if existing mechanisms are
actually used, and that link had never been measured. Verdict: **H survives** —
in three young vocabularies 88–100% of the leading implementations have no
measurable monthly install. Full entry F032 in
[`FAILURES-findings-6.md`](../../FAILURES-findings-6.md).

## Hypothesis, declared before the run

H: inside a niche, star rank does not predict which implementation people use.
- **K** — H is dead if ≥3 of 5 niches put the most-used implementation first by
  stars, with ≥1,000 installs/month behind it.
- **S** — H survives if ≥3 of 5 do not, and ≥half of every young niche's
  implementations have no measurable install.
- Otherwise the record says **inconclusive**, which the gate tests directly.

## Result (`observed` 2026-10-04, `results.json`)

| Niche | Age | any install | max installs/mo | leader by stars | its installs | ρ(stars, installs) |
|---|---|---|---|---|---|---|
| `agent session log` | young | 2/25 | 1,864 | `PostHog/posthog` 40,135★ | 0 | −0.157 |
| `lockfile drift` | young | 3/25 | 3,100 | `mcptrust/mcptrust` 6★ | 0 | 0.350 |
| `knitting chart` | young | **0/25** | 0 | `knitscape/knitscape` 64★ | 0 | undefined |
| `reproducible build` | mature | 4/25 | 4,519 | `thought-machine/please` 2,616★ | 0 | 0.030 |
| `exif metadata` | mature | 7/25 | 16,599,464 | `remove-ai-watermarks` 5,757★ | 8,100 | 0.070 |

1. **Stars do not predict installs in any niche**, mature included. So F028's
   heavy star tail is not evidence of adoption and its flat tail is not evidence
   against it: the two measures are decoupled here.
2. **Vocabulary age does not rescue a niche.** Four of five are flat, including
   the mature one. Only `exif metadata` has volume, and it is the niche whose
   artifact is a small library with an unambiguous install path.

## The instrument was the hard part, and it failed twice before it worked

Both failures pushed measurements towards zero, the direction that flatters the
hypothesis. Both are held by `tests/test_census_stats.py`.

- **Pre-flight self-check.** Nine packages that are certainly installed must
  read as installed. It caught that npm's single-package endpoint answers flat
  (`{"downloads":N}`) while its bulk endpoint keys by name
  (`{"vite":{"downloads":N}}`), so `vite` read as unused.
- **A throttle is not an absence.** shields.io answers a rate-limited request
  with **HTTP 200** and `{"message":"rate limited by upstream service"}`, which
  parses as a package with no downloads. Three outcomes are now kept apart — a
  number, `None` for genuinely unpublished, `REFUSED` for declined — and refusals
  are counted per niche.
- **A name match is not an identity.** 31 of 125 projects (25%) matched a
  package whose metadata named a *different* owner. Unverified, this credited
  39,000,000 installs/month to `PostHog/posthog` and gave `thought-machine/please`
  47 via an unrelated `npm:please` owned by `mrdrozdov/please`. Attribution now
  requires the package's declared repository to be the project measured, checked
  in both directions before any result is reported.
- **Spearman is the wrong primary statistic.** With 24 of 25 rows tied at zero
  it separates "the used project is #1" from "it is #3" by 0.340 against 0.283.
  The gate uses the star rank of the most-used project instead, which separates
  those as 1 against 3.

## Limits

- **Registry installs are not users.** `thought-machine/please` is a real
  2,616-star build system with real users and is invisible here: it ships as a
  Bazel binary, not a package. **Zero measured installs is not zero users.**
- Consequently the gate's **dead branch was not fully executable** — the mature
  arm's dominant incumbent is precisely what this instrument cannot see. H
  surviving is weaker here than it would be on a measurable arm.
- Installs are not active use; a package pulled by a CI default counts per job.
- Package names are guessed from repository names; renamed repos, monorepos and
  packages declaring no repository are dropped, which biases **downwards**.
- One snapshot, one endpoint family, one 2-CPU machine, search over names and
  descriptions. No measurement of usefulness is made or implied.

## Files

`census.py` (run), `usage.py` (instrument), `stats.py` (rank statistics),
`results.json` (raw), `run.log` (stdout). Tests: `tests/test_census_stats.py`,
18 cases including the gate in both directions and the split-verdict refusal.