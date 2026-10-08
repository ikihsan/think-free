# E060 — Do static version badges in READMEs match the repo's latest release? (probe)

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: complete
last-verified: 2026-10-08
-->

## Question

Fresh observation (D080): are static `version` badges in READMEs a real
source of stale version claims?

## Method

- Sample: top-starred repos with >40k stars in `python`, `rust`, `javascript`
  (GitHub repo search, sort=stars, per_page=15 each, 45 repos, 2026-10-08).
- Per repo: fetch README (contents API), latest release tag.
- Instrument: regex for badge URLs containing `version` with a static
  shields-style value (`version-v?X-blue|green|...`); dynamic release badges
  are excluded by construction (they self-update).
- Kill gate (declared): if <5% of repos carry a static version badge, or
  static-badge drift share <0.05, the population does not exist → KILL.

## Results

`repos=45`, `with_static_version_badge=0`, `static_badges=0`, `drifted=0`.
Raw: `raw/rows.json`.

## Verdict

KILL — the population is absent at the top-star stratum; no static version
badges observed at all. Modern usage is dynamic release badges or no version
badge. Instrument is sound only as far as zero rows: it cannot distinguish
"no drift" from "no population" on its own, and both rows answer is *no
population*, so nothing is built. If the candidate were ever re-opened, it
needs a stratum where badges exist (e.g. random mid-star repos).
