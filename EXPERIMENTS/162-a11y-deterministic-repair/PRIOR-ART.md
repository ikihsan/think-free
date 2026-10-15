<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E162 — prior art, probed before the arms were run

**Retrieved 2026-10-15** by `/tmp/opencode/priorart_probe.py` writing
`/tmp/opencode/priorart.json`: 18 queries across the GitHub search API, the
npm registry search API, and PyPI's JSON API. Raw output is the probe's; the
reading is mine. Retrieval dates are separate from publication dates, and the
GitHub rows below carry each repository's own `pushed_at`.

## The claim being probed

Not "does an accessibility autofixer exist" — it obviously does, and it has for
years. The claim E162 measures is narrower and narrower on purpose:

> a deterministic (no model, no human) repairer can remove a large share of
> real axe violations **without inventing user-facing text**, and the share of
> repairs that must invent is measurable rather than argued.

So the prior-art question is three questions, not one.

## 1. Does the deterministic repair already exist?

**Yes, and it is old.** `eslint-plugin-jsx-a11y` is the incumbent: ESLint rules
with fixers, applied to JSX/TSX at author time. It is why five of the npm
searches are dominated by `eslint-plugin-*` and autofix-suppression packages
(`eslint-plugin-no-autofix`, `@morev/eslint-disable-autofix`) — the ecosystem
that grows around a fixer is mostly machinery for turning it off.

`PetriLahdelma/a11y-safe-autofix` (1 star, pushed 2026-05-19) describes itself
as "Deterministic ESLint fixes for React/TSX accessibility" — the same idea,
newer, smaller. This is prior art for the mechanism, unambiguously.

**What the incumbents do not do:** they work on **source files a developer
owns**, through a linter the developer installed, on a language they already
use. None of them addresses "fetch a URL and repair the DOM", which is the
population in this experiment.

## 2. Does the axe-shaped repair already exist?

axe-core's own answer is the important one. The npm search for `axe-core`
returns `axe-core`, `@axe-core/cli`, `cypress-axe`, `axe-playwright`,
`axe-sarif-converter`, `@axe-core/reporter-earl` — **reporting, runners and
converters, and not one fixer.** On PyPI, `axe-core-python` last uploaded
2022-09-01 at version 0.1.0; `axe-selenium-python` first uploaded 2026-04-19
at 3.0.0. Both are integration layers, not repairers.

So the gap this experiment measures is real and narrow: **axe reports and does
not fix, and the fixers that exist attach to source code, not to a fetched
page.** That is a gap in tooling, not a gap in the world.

## 3. Is the "autofix" space crowded with the thing itself?

Crowded, and mostly with models. 2026-era hits on `wcag auto fix`:

| Repository | Stars | `pushed_at` | What it is |
|---|---|---|---|
| `SocialGouv/ultra11y` | 4 | 2026-10-14 | "Zero-dependency static engine **+ agent judgment**" |
| `sclavijosuero/wick-a11y` | 64 | 2026-08-16 | Cypress plugin, reports in the Cypress log |
| `AfterRealm/curb-cut` | 1 | 2026-09-29 | audits and auto-fixes, for Claude Code |
| `iam-artificis/a11yfix` | 0 | 2026-10-01 | "writes the patch, not just the report" |
| `a11yforge/a11yforge` | 0 | 2026-08-05 | crawls a site, proposes fixes **and verifies them** |
| `gianlpz/accessibility-fixer` | 0 | 2026-03-20 | axe-core → AI explains and generates code |
| `mtalhasid/axeVision` | 1 | 2026-09-09 | axe + Gemini + dashboards |
| `dequelabs/axe-mcp-server-public` | 8 | 2026-10-13 | Deque's own MCP server: axe in your IDE |
| `nys-cdo/poc-pdf-assessor` | 5 | 2026-06-30 | PDF triage against the DOJ Title II deadline |

The pattern is consistent: an agent reads the finding and writes the fix. That
is a strong prior that **fabrication is the accepted cost** of the AI route —
and that a tool which can *measure* fabrication rather than absorb it is a
different product from the dozen above. Whether that is a product or a
measurement is not decided here.

## What this does and does not establish

- **Does establish:** the mechanism is prior art (`jsx-a11y`, 2018), the axe
  repair is not (no fixer in the axe ecosystem), and the "autofix" name is
  taken by a dozen model-driven tools, nine of them under 10 stars.
- **Does not establish:** demand. Nothing here measures whether anyone would
  install a deterministic repairer. The protocol says so, and this file does
  not change it.
- **Absence of a search hit is not originality** (AGENTS.md). The searches were
  run in the user's vocabulary ("autofix", "auto fix", "remediation", "fix
  violations") and in the ecosystem's vocabulary (axe-core, pa11y, WCAG); the
  hit counts are large and the true unknown is whether the *fetch-a-URL*
  variant exists under a name none of these 18 queries used.