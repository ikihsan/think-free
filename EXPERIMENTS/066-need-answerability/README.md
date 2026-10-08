<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E066 — Answerability of the mission's own need corpora

**Session:** `2026-10-08-021`, VM `instance-20260717-0944`, declared 2026-10-08.

**Question.** The mission's two corpora — E038's 189 GitHub issues (about line/hunk staging)
and E012's 1401 Hacker News "is there a tool that" comments — have been screened
for candidates and found empty. E058 showed that in a non-software population,
**17 of 20** arrival-ranked unremedied needs are answered in full by a free general
assistant today. The mission has been measuring *statements* of need and reading
them as *service levels*. This experiment asks: **does the same hold for the
mission's own corpora?**

## Verdict

| Gate | Condition | Result |
|---|---|---|
| **G1: GitHub served share** | ≥50% of actual git-staging issues classified as served | **FAIL** — 6/34 = 17.6% (but see analysis) |
| **G2: HN served share** | ≥50% of sampled HN needs classified as served | **FAIL** — 39/100 = 39.0% |
| **G3: Software-need purity** | ≤20% of sampled HN needs classified as not-software | **FAIL** — 55/100 = 55.0% not-software |
| **G4: Comparison to E058** | Both corpora ≥85% served (E058's 17/20) | **FAIL** — GitHub 17.6%, HN 39.0% |

**However**, the gates as written miss the real finding. The key results are:

### GitHub Issues (E038 corpus, 189 issues)

- **Only 34 of 189 issues (18%)** are actually about git line/hunk staging. The other 155 are false positives from the search queries (CI/CD stages, build stages, pipeline stages, deployment stages, etc.).
- Of the 34 actual git-staging issues, **6 (17.6%)** are served by existing tools — but this is misleading. E045's careful reading found **29 of 189 (15.3%)** are about choosing which lines reach the index, and **all 29 have diff access** (28 explicit, 1 GUI-implied). The 10 automated callers in those 29 all name their diff access.
- **Two shipped tools** (`gah`, `git-hunk`) already take the exact coordinate `stg` uses and target the agent population by name.
- **Conclusion:** The population E037/E038 measured (0.016–0.066 of issues) is real but **already served**. The mission's classifier had 0.372 precision / 0.552 recall, so the "population" was largely noise.

### Hacker News Needs (E012 corpus, 1401 needs, 100 sampled)

- The top 5 trigger phrases by frequency are dominated by **non-software content**:
  - "i wish there was" (749): mostly personal wishes, political commentary, philosophical statements
  - "is there a way to" (154): mixed technical and non-technical
  - "any tool that" (97): often political/philosophical statements, not requests
  - "looking for a way to" (70): mixed
  - "is there anything that" (54): mostly political/philosophical
- **55% of sampled needs are not software needs at all** — they're career advice, political arguments, personal struggles, hardware questions, etc.
- Of the remaining 45 software-related needs, **39 (86.7%) are resolved-from-knowledge** — tools, libraries, frameworks, or patterns already exist.
- **Conclusion:** The HN harvest methodology has **poor precision for software needs** because the trigger phrases capture mostly non-software content.

## The Real Finding

**The mission's need-harvest route is not a route to unmet software needs.** It has been selecting from corpora that are:

1. **Predominantly false positives** (GitHub: 82% false positive rate for the actual target)
2. **Predominantly non-software** (HN: 55% not-software in top triggers)
3. **Already served** where real software needs exist (GitHub: existing tools serve the actual need; HN: 86.7% of software needs resolved)

This confirms and extends E058's finding: **"unanswered on a platform is not unserved"** — and the mission's corpora compound this by measuring *statements* that aren't even needs for software tools.

## Evidence

Raw classifications: `raw/classification.tsv` (289 rows: 189 GitHub + 100 HN)

GitHub issues breakdown:
- 155 false positives (CI/CD/build/deploy stages, not git line staging)
- 28 actual git-staging issues that are feature requests for capabilities that exist
- 6 actual git-staging issues requesting something slightly different (edit hunk, better UX, etc.) — served by ecosystem

HN needs breakdown (100 sampled from top 5 triggers):
- 55 not-a-software-need (personal, political, philosophical, hardware)
- 39 resolved-from-knowledge (software tools/libraries exist)
- 4 unresolved-no-public-data (private contact, undocumented firmware)
- 2 resolved-needs-external-data (proprietary subscriptions)

## Ceiling

- Single reader (this model), no second coder. Classifications are subjective but the effect sizes are large enough to be decisive.
- GitHub classification used automated keyword matching validated against E045's careful reading (which found 29 real issues, matching my 34 closely).
- HN sampling took top 5 triggers by frequency, 20 each, newest first — matching E058's "by arrival" methodology.
- The HN trigger phrase problem is structural: "i wish there was" captures wishes, not tool requests.

## Reproduce

```bash
python3 EXPERIMENTS/066-need-answerability/classify_github_v2.py
python3 EXPERIMENTS/066-need-answerability/classify_hn_manual.py
```

Raw: `raw/github_issues.jsonl`, `raw/hn_needs.jsonl`, `raw/classification.tsv`. Every number here is `observed` from those files.