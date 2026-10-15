<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# Experiment 151: VS Code Marketplace (Open VSX) View-Count Principle Test

## Claim
On the VS Code extension marketplace (via Open VSX Registry), need-related extensions (language support, debuggers, framework tools, cloud tools, database tools) show systematically higher download counts than general/foundation extensions (themes, icon themes, keymaps, generic snippets).

## Scope
- **Platform**: Open VSX Registry (open-source VS Code extension marketplace)
- **Population**: Extensions accessible via public search API
- **Metric**: downloadCount
- **Classification**: Need-related vs. General/Foundation extensions based on categories, tags, and name/description keywords

## Selection Rule (Stated Before Data Collection)
This domain is chosen by the stated rule: "largest untouched extension marketplace with exposable per-item install-count metadata" from the VIEW-COUNT-SUMMARY.md next-step options (Option A). The Open VSX Registry has 19,679 extensions with downloadCount universally available.

## Classification Rule (Pre-declared, Before Seeing Results)

### Need-Related Extensions (Treatment)
An extension is classified as **need-related** if ANY of these conditions are met:

1. **Category-based**: Category is one of:
   - `Programming Languages`
   - `Debuggers`
   - `Linters`
   - `Formatters`
   - `Language Packs` (localization for specific languages)
   - `Cloud` (AWS, Azure, GCP, etc.)
   - `Databases`
   - `Testing`
   - `CI/CD`
   - `Containers` (Docker, Kubernetes)
   - `Machine Learning` / `AI`
   - `Data Science`
   - `Mobile Development`
   - `Game Development`
   - `IoT` / `Embedded`

2. **Tag-based**: Any tag indicates a specific language/framework/tool:
   - Language tags: `python`, `javascript`, `typescript`, `java`, `go`, `rust`, `cpp`, `csharp`, `php`, `ruby`, `swift`, `kotlin`, `scala`, `r`, `matlab`, `julia`, `dart`, `lua`, `perl`, `haskell`, `clojure`, `elixir`, `erlang`, `fsharp`, `ocaml`, `vbnet`, `powershell`, `bash`, `shell`
   - Framework tags: `react`, `vue`, `angular`, `django`, `flask`, `spring`, `express`, `nextjs`, `nuxt`, `svelte`, `laravel`, `rails`, `aspnet`, `dotnet`
   - Cloud tags: `aws`, `azure`, `gcp`, `google-cloud`, `kubernetes`, `k8s`, `docker`, `terraform`, `ansible`
   - Database tags: `sql`, `postgresql`, `mysql`, `mongodb`, `redis`, `sqlite`, `dynamodb`, `cassandra`
   - Tool tags: `debugger`, `linter`, `formatter`, `test`, `testing`, `ci`, `cd`, `github`, `gitlab`, `bitbucket`

3. **Name/Description keyword-based** (case-insensitive):
   - Language names: `python`, `javascript`, `typescript`, `java`, `golang`, `rust`, `c++`, `c#`, `php`, `ruby`, `swift`, `kotlin`, `scala`, `r language`, `matlab`, `julia`, `dart`, `lua`, `perl`, `haskell`, `clojure`, `elixir`, `erlang`, `f#`, `ocaml`, `vb.net`, `powershell`
   - Framework names: `react`, `vue`, `angular`, `django`, `flask`, `spring`, `express`, `next.js`, `nuxt`, `svelte`, `laravel`, `rails`, `.net`, `asp.net`
   - Cloud/provider: `aws`, `azure`, `gcp`, `kubernetes`, `docker`, `terraform`
   - Database: `postgres`, `mysql`, `mongo`, `redis`, `sqlite`, `dynamodb`
   - Tool purpose: `debugger`, `debug`, `lint`, `format`, `test`, `language server`, `intellisense`, `completion`, `refactor`, `profiler`

### General/Foundation Extensions (Control)
An extension is classified as **general** if:
- It has NO need-related tags from above
- Its category is one of: `Themes`, `Icon Themes`, `Keymaps`, `Snippets` (generic), `Other` (without need-related tags)
- Its tags/name/description suggest purely cosmetic or generic utility:
  - Theme indicators: `theme`, `color theme`, `dark`, `light`, `color scheme`
  - Icon theme indicators: `icon theme`, `icons`, `file icons`, `folder icons`
  - Keymap indicators: `keymap`, `keybinding`, `vim`, `emacs`, `sublime`
  - Generic snippets: `snippet`, `boilerplate`, `template` (without language/framework specificity)

### Excluded (Neither)
- Extensions that don't clearly fit either category
- Deprecated extensions
- Extensions with downloadCount = 0 or missing

## Sampling Strategy
1. **Stratified sampling by download count** to avoid selection bias:
   - Fetch top 100 by download count (`sort=downloads`, page=1, size=100)
   - Fetch middle tier: page=50, size=100 (approx rank 5000-5100)
   - Fetch lower tier: page=150, size=100 (approx rank 15000-15100)
   - Fetch random-ish: search with empty query, page=10, size=100
   - Fetch random-ish: search with empty query, page=100, size=100
2. Total target: ~500 extensions, deduplicated by `namespace.name`
3. Filter out excluded extensions

## Statistical Test
- **Primary**: Cliff's delta (effect size) between need-related and general groups for downloadCount
- **Secondary**: Mann-Whitney U test (non-parametric), p-value
- **Thresholds** (pre-declared):
  - Cliff's delta ≥ 0.33 (medium effect) → **PASS** (systematic advantage)
  - Cliff's delta ≥ 0.147 (small effect) → **WEAK** (suggestive but not decisive)
  - Cliff's delta < 0.147 → **FAIL** (no meaningful advantage)
  - Kill gate: If Cliff's delta < 0.147, claim is rejected

## Baseline
Strongest available: Random sampling from same platform without need-filtering (the control group IS the baseline).

## Negative Controls
1. **Shuffle control**: Randomly shuffle labels 1000x, recompute Cliff's delta. True effect must exceed 95th percentile of null distribution.
2. **Category-only control**: Verify the classification isn't just picking up category imbalances by checking effect size using only category-based classification.

## Resource Limits
- API requests: ≤ 50 (5 pages × 100, plus individual lookups if needed)
- Time: ≤ 10 minutes
- Storage: ≤ 10 MB JSON

## Falsification Conditions (Kill Gates)
1. **Primary kill gate**: Cliff's delta < 0.147 between need-related and general groups.
2. **Direction kill gate**: General extensions systematically OUTPERFORM need-related extensions (Cliff's delta < -0.147).
3. **Population kill gate**: Fewer than 30 extensions in either group after classification (insufficient power).
4. **Confound kill gate**: The effect disappears when controlling for extension age (timestamp) or publisher type (verified vs unverified).

## Context
This experiment extends the view-count principle investigation summarized in [`docs/reference/VIEW-COUNT-SUMMARY.md`](../../docs/reference/VIEW-COUNT-SUMMARY.md), which documents the principle's boundaries across 15+ domains. This is a fresh observation in a domain this mission has not touched (VS Code extension marketplace), chosen by the stated rule in the named next action.

## Outputs
- `RAW_DATA.jsonl` - All fetched extensions with raw categories, tags, and metrics
- `CLASSIFIED.jsonl` - Extensions with classification labels
- `RESULT.md` - Statistical results, effect sizes, decision
- `CLASSIFIER.md` - Documented classification rules with examples

## Pre-registration
This protocol is written BEFORE any data analysis. Classification rules are fixed. Thresholds are fixed. Kill gates are fixed.