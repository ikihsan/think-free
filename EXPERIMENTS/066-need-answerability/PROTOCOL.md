<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E066 — Answerability of the mission's own need corpora

**Question.** The mission's two corpora — E038's 189 GitHub issues (about line/hunk staging)
and E012's 1401 Hacker News "is there a tool that" comments — have been screened
for candidates and found empty. E058 showed that in a non-software population,
**17 of 20** arrival-ranked unremedied needs are answered in full by a free general
assistant today. The mission has been measuring *statements* of need and reading
them as *service levels*. This experiment asks: **does the same hold for the
mission's own corpora?**

**Population.** Two corpora already on disk, no network fetch required:

1. **GitHub issues** (`EXPERIMENTS/038-staging-prior-art/raw/requests.jsonl` →
   `EXPERIMENTS/066-need-answerability/raw/github_issues.jsonl`): 189 unique
   issues harvested from 10 GitHub issue search queries about line/hunk staging,
   sorted by reactions. These are the issues E038 and E045 read.

2. **Hacker News needs** (`EXPERIMENTS/012-candidate-harvest/raw/hn_needs_2026-10-04.jsonl`
   → `EXPERIMENTS/066-need-answerability/raw/hn_needs.jsonl`): 1401 comments
   matching 25 "unmet need" trigger phrases on HN stories after 2024-01-01,
   newest first. These are the needs E012 screened (0 of 50 survived).

**Instrument.** The reader (this model) attempts each need against its own
knowledge — the strongest accessible free alternative — and classifies the
outcome. This is the same instrument E058 used: the model that would build the
tool is simultaneously the free instant incumbent.

**Classification (adapted from E058).**

| Label | Meaning |
|---|---|
| `resolved-from-knowledge` | The need is fully answerable from general knowledge available to a free assistant today. No external data, no proprietary spec, no private repository required. |
| `resolved-needs-external-data` | The *method* is known, but the specific value requires data not in general knowledge (e.g., a manufacturer spec sheet, a serial number registry, a private API key). |
| `unresolved-no-public-data` | No free public source the assistant can reach provides the answer. The data was never recorded, or is behind a paywall/rate-limit/registration the assistant cannot satisfy. |
| `not-a-software-need` | The need is not about software or a tool a program could provide (e.g., "is there a tool that makes my boss listen to me"). |

**Sampling.** Testing all 1590 rows is impractical in one session. We sample:

- **GitHub**: All 189 issues (the corpus is small enough). Each issue is read and
  classified.
- **Hacker News**: A stratified sample of 100 needs — 20 from each of the 5
  most frequent trigger phrases, taken from the newest items (matching the
  harvest's "newest first" order). This mirrors E058's "top 20 by arrival".

**Gates.**

| Gate | Condition |
|---|---|
| G1: GitHub served share | ≥50% of GitHub issues classified as `resolved-from-knowledge` or `resolved-needs-external-data` → the corpus is predominantly served. |
| G2: HN served share | ≥50% of sampled HN needs classified as `resolved-from-knowledge` or `resolved-needs-external-data` → the corpus is predominantly served. |
| G3: Software-need purity | ≤20% of sampled HN needs classified as `not-a-software-need` → the trigger phrases do capture software needs. |
| G4: Comparison to E058 | The served share in both corpora is ≥ the 85% (17/20) observed in E058's non-software population. |

**Kill condition.** If **both** G1 and G2 are met (≥50% served in both corpora),
the mission's need-harvest route is **not a route to unmet need** — it has been
selecting statements that are already served. The generator is refuted at the
population level, not just the candidate level.

**Output.** `raw/classification.tsv` with columns: `corpus`, `id`, `title_or_trigger`, `text_excerpt`, `classification`, `notes`. Summary counts in `README.md`.

**Ceiling.** One reader (this model), no second coder. The classification is
subjective but the instrument is the same one E058 used and the finding there
was decisive (17/20). A single reader's verdict on 189 + 100 rows is sufficient
to move the decision; κ is not required when the effect size is this large.