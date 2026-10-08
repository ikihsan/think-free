<!-- origin-meta
owner: FAILURES.md
status: active
last-verified: 2026-10-08
-->

# Findings 34 — independent confirmation of the need-harvest route retirement

`observed` 2026-10-08, session 2026-10-08-021, VM `instance-20260717-0944`.
Evidence: [`EXPERIMENTS/066-need-answerability/`](EXPERIMENTS/066-need-answerability/README.md).

Split out of [`FAILURES-findings-33.md`](FAILURES-findings-33.md) on 2026-10-08.
**Identifiers are stable across all findings files.**

## F100 — E066 confirms E063: the need-harvest route is closed at the population level

**What happened.** E066 ran an independent classification of the two corpora every
candidate screen in this repository consumed: E038's 189 GitHub issues (the
corpus behind the `stg` candidate) and E012's 1401 Hacker News "is there a tool
that" comments (the corpus behind the 0-of-50 harvest). This was a separate
session from E063, using a different classifier (this model's direct judgment
rather than E062's instrument with controls), to confirm the primary result.

**The measurement.**

| corpus | total | actually about target | served | not-software | notes |
|---|---|---|---|---|---|
| GitHub (E038) | 189 | 34 (18%) | 34 (100% of real) | — | 155 false positives on CI/CD/build/pipeline stages |
| HN (E012, sampled) | 100 | 45 | 39 (86.7%) | 55 | top 5 triggers by frequency, 20 each |

**GitHub corpus:** Only 34 of 189 issues are actually about git line/hunk
staging. The other 155 are false positives from the search queries matching
"stage" in CI/CD contexts (GitHub Actions stages, build pipeline stages,
deployment stages, Docker multi-stage builds, etc.). All 34 real issues request
capabilities that already exist in the ecosystem: `git add -p`, lazygit, magit,
VS Code's `git.stageSelectedRanges`, neogit, tig, git-hunk, gah, filterdiff.
Two shipped tools (`gah`, `git-hunk`) take the exact coordinate `stg` uses and
name the agent population in their READMEs. This replicates E045's finding that
the classifier had 0.372 precision / 0.552 recall and the "population" was
largely noise.

**HN corpus:** The top 5 trigger phrases by frequency capture predominantly
non-software content:
- "i wish there was" (749): personal wishes, political commentary, philosophy
- "is there a way to" (154): mixed technical and non-technical
- "any tool that" (97): often political/philosophical statements
- "looking for a way to" (70): mixed
- "is there anything that" (54): mostly political/philosophical

55% of sampled needs are not software needs at all. Of the 45 software-related
needs, 39 (86.7%) are resolved-from-knowledge — tools, libraries, frameworks,
or patterns already exist. 4 are unresolved-no-public-data (private contact,
undocumented firmware), 2 resolved-needs-external-data (proprietary
subscriptions).

**What it buys.** E063's finding (F098) is independently confirmed: seven
emptiness measurements in this repository (F029, F039, F051, F059, F081, F084,
F085) were not wrong about the domains they sampled; they were reading a route
that selects **served statements**. The trigger-phrase harvest over HN/GitHub
has no tail where a tool could start (`unserved-open` = 0). The route is
retired as a candidate source. Per D083, any successor session starts from
fresh observation in a new domain with a runnable falsification experiment
(stdlib-only, synthetic fixtures, predeclared kill gates).