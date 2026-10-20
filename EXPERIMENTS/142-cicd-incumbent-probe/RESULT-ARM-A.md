<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-15
-->

# E142 Stage 1 result — Arm A incumbent survey (E140's G5, cheap probe)

Session `2026-10-15-002`, VM `instance-20260717-0947`, measured 2026-10-15.
Protocol declared before any search: [`PROTOCOL.md`](PROTOCOL.md).

## Headline

**G5-tool-strict = 0 of 14. G5-tool-claimed = 0 full + 2 partials. The kill
does not fire** (it required ≥7 strict). The single most on-point incumbent
found — the top marketplace hit for "fix failed build" — **explicitly
disclaims the fix half** in its own FAQ. Per the protocol's second kill
condition, P1 has no sourced support after the attempt made here, so **the
E140 harvest is declined and the mission returns to fresh exploration**.
E140 itself is not killed by this probe; it is shelved as unrun.

## Method (as declared)

Arm A over the 14-category superset (E140 `ERROR_CATALOG.md` + `ERROR_CATALOG-2.md`).
Strict rule: a free existing tool counts only if a fetched source shows it
**taking a failing run and producing an applied fix** (applied change,
rewritten file, merged/auto-merged PR, automatic reconfiguration).
"Explains what to change", "reproduces locally", and vendor marketing do not
count. Search was unavailable, so the sweep used: GitHub Marketplace search
(fetched), GitHub repo code search via API (observed), and direct fetches of
the named incumbents. All retrieval dates 2026-10-15.

## Market-absence evidence (C3, the negative direction)

- Marketplace search "fix failed build" returns **2 results total** (fetched
  2026-10-15): `Badgr Pipeline Check` and `Java Dependency Upgrade Fixer`.
- GitHub repo search `self-healing ci fix github actions failure` returns
  **6 repos, all 0 stars**, last pushed 2026-03 to 2026-06, each describing a
  bring-your-own-key LLM demo ("diagnoses via Claude", "using Anthropic
  Claude", "OpenAI (GPT-4o-mini)") — observed via API, commands in
  `sessions/2026-10-15-002-*/commands.log`. No shown applied fix; not
  free-standing free tools. Per C4 they are one incumbent class (LLM wrapper),
  and it fails the "free" criterion.
- Paid incumbents (Copilot, BuildPulse-class) are out of scope by G5's "free"
  criterion regardless of capability (recall-only on pricing; supports only an
  exclusion, counts toward nothing).

## The two real incumbents, both fetched

**Badgr Pipeline Check** (`https://github.com/marketplace/actions/badgr-pipeline-check`,
retrieved 2026-10-15) — diagnosis YES, fix NO, by its own words:

- "Diagnose failed CI builds with likely cause, evidence, and **a suggested
  fix**. Local checks first, AI only when needed"
- FAQ: "**Does Badgr auto-fix code? No.** Badgr reports findings and suggested
  fixes. It does not modify code, rerun pipelines, or merge PRs."
- Its AI-fix-PR option "opens a PR with proposed fix instructions — **not a
  code patch**. Never auto-merges."
- Rule-based failure check is "pattern-matched against **14+ known error
  types**" (missing dependencies, test failures, Docker errors, TypeScript
  errors, package conflicts, timeouts, auth failures, deployment issues) —
  a vendor's implicit frequency claim that mixes both ownership halves; it is
  not a distribution and supports neither P1 nor its negation.

**Java Dependency Upgrade Fixer / JAIPilot** (`https://github.com/marketplace/jaipilot`,
retrieved 2026-10-15) — the only asserted auto-repair found:

- "repairs failed Dependabot and Renovate updates in public Maven and Gradle
  repositories… and opens a **draft** repair PR… **never auto-merges**."
- "**3 installs**." Free plan covers public repos only.
- Scope: a sub-case of category 1 (Java/Maven/Gradle **bot PRs**, not failing
  runs generally); output is a draft PR, not an applied change. Strict NO;
  counted as the single claimed partial.

**pre-commit.ci** (`https://pre-commit.ci`, retrieved 2026-10-15) — the
strongest adjacent incumbent (category 13, lint):

- "if tools make changes to files during a pull request, pre-commit.ci will
  **automatically fix the pull request**." Free for open source.
- Divergence from the strict rule, recorded not laundered: its input is a PR
  with an adopted `.pre-commit-config.yaml`, not a failing Actions run; it
  fixes only what its configured hooks rewrite. Strict NO; second claimed
  partial.

**actionlint** (`https://github.com/rhysd/actionlint`, retrieved 2026-10-15)
— category 6 diagnosis only: "Static checker for GitHub Actions workflow
files" (syntax, expressions, action usage, shellcheck/pyflakes integration);
no auto-fix capability in the feature list. Strict NO.

## Per-category verdicts (strict)

| # | Category | Strongest incumbent | Verdict |
|---|---|---|---|
| 1 | Dependency resolution | JAIPilot (Java bot-PRs, draft only, 3 installs); Dependabot/Renovate proactive, read no failing run (recall-only) | NO (claimed partial) |
| 2 | Test failure | none; fix is code intent | NO |
| 3 | Permission/auth | GitHub annotations diagnose; secrets cannot be auto-minted | NO |
| 4 | Timeout | Badgr flags missing timeouts; bump-vs-hang needs judgment | NO |
| 5 | Resource exhaustion | retry / paid larger runners only | NO |
| 6 | Config/syntax | actionlint diagnoses, never fixes | NO |
| 7 | Missing secret/env | unfixable by construction for secrets | NO |
| 8 | Cache/artifact | re-run, not fix | NO |
| 9 | Build/compile | `cargo fix`-class tools are human-invoked, read no run | NO |
| 10 | Network | transient; retry, not fix | NO |
| 11 | Container/Docker | Renovate updates tags proactively; no reactive fixer | NO |
| 12 | Deploy/release | human-gated by design (environment rules) | NO |
| 13 | Lint | pre-commit.ci auto-fixes PRs (input is PR, not run) | NO (claimed partial) |
| 14 | Flaky/intermittent | rerun/quarantine ≠ fix | NO |

Counts: **strict 0/14; claimed 0 full categories + 2 partials** (cat-1
Java-only sub-case, cat-13 hook-covered sub-case). Kill gate (≥7 strict)
does not fire. The weaker original-G5 reading (asserted capability) reaches
at most 2 partials — also no kill.

## P1/P2 assessment (standing evidence + one sourcing attempt)

- P1 (project-code half dominates frequency): **no sourced support this
  session.** One attempt made: TravisTorrent site fetch failed (transport
  error). Badgr's "14+ known error types" list mixes both halves and states
  no distribution. P1 remains `untested`, exactly as declared.
- P2 (assistant closes the config-half gap): standing evidence only — E092
  measured 30/37 = 0.8108 on appliance-diagnosis text; CI logs untested.
  G5-alt is **untested**, not supported.
- Protocol kill condition 2 fires as written: G5-tool passes (no kill) but P1
  is unsourced → **do not run the ~7,500-request harvest; return to fresh
  exploration.** Stage 2 (`ARM-B.md`) is therefore **not written**: its row
  sample would come from the declined harvest.

## Defects in this session's own work

1. Web search was unavailable (integration cancelled all queries); the sweep
   ran on marketplace search + API repo search + direct fetches instead. The
   instrument change is recorded here, before measurement, not after.
2. The strict rule's "applied change" examples never contemplated draft PRs;
   JAIPilot forced the reading. Decision: a draft PR is a proposal, not an
   applied change — strict NO, claimed partial. A future protocol should name
   the draft-PR case explicitly.

## Decision and continuation

- **Decided:** E140's harvest is declined (cost ~7,500 API requests + hours
  against an unsourced P1 and an untested G5-alt). E140 stays declared/unrun;
  nothing about the CI domain is closed.
- **Single most useful next action:** fresh observation in a new domain
  (E140's protocol stands reusable if P1 ever gains sourced support; a small
  hand-sample Arm B on real failed-run logs is the deferred alternative that
  could still kill E140 via G5-alt, but the protocol routes there only after
  fresh exploration, not before).
