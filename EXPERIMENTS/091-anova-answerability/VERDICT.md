<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E091 Verdict — Hand replication of E062's answerability sub-test on Anova cooking Discourse

## Status: BLOCKED — Infrastructure limitation

**Protocol declared:** 2026-10-10 (PROTOCOL.md)
**Data collection completed:** 2026-10-10
**Assistant queries:** NOT RUN — No GPT-4o or Claude 3.5 Sonnet API access
**Human judgment:** NOT RUN — Requires assistant answers

## Summary

The experiment protocol was written and pre-registered before any population data was fetched. Population data (20 topics) and G0 discrimination probes (20 topics with ground truth) were successfully collected from Anova cooking Discourse (community.anovaculinary.com, Support category).

However, the core experimental step — querying a free general assistant (GPT-4o or Claude 3.5 Sonnet) for each topic and having a human judge whether the assistant's answer resolves the problem — **cannot be performed** in this environment due to lack of LLM API access.

## Data Collected

### Population (top 20 by view_count, filtered for problem statements)

| Rank | Topic ID | Views | Title | Problem Type |
|------|----------|-------|-------|--------------|
| 1 | 86 | 69,552 | Bluetooth PIN | Connectivity |
| 2 | 12241 | 45,955 | My Anova wont connect to my WIFI? | Connectivity |
| 3 | 1096 | 30,585 | Problem / long lasting beep | Device malfunction |
| 4 | 5021 | 23,790 | Current temp stuck at 32 degrees | Device malfunction |
| 5 | 12736 | 20,504 | Shutting Off | Device malfunction |
| 6 | 722 | 20,461 | Clamp broken | Hardware failure |
| 7 | 26273 | 19,199 | vacuum seal not sealing | Accessory malfunction |
| 8 | 717 | 17,020 | Snooze beeping when timer done | UX/annoyance |
| 9 | 4261 | 14,922 | Connecting more than one mobile device | Connectivity |
| 10 | 9020 | 14,637 | Beeping Keeps Going Off | Device malfunction |
| 11 | 6924 | 13,957 | Bluetooth Pairing PIN | Connectivity |
| 12 | 132 | 6,193 | Low Water Alarm | Device malfunction |
| 13 | 4681 | 6,120 | Eero + APC WiFi = Fail | Connectivity |
| 14 | 12987 | 6,366 | Push Notification on iOS not working | App/notification |
| 15 | 9165 | 6,290 | Straighten the impeller | Hardware repair |
| 16 | 3051 | 5,750 | Received wrong device | Shipping error |
| 17 | 8811 | 5,674 | Password reset: how? | Account/access |
| 18 | 10550 | 5,452 | Anova App Timer Resetting | App bug |
| 19 | 13044 | 5,383 | Timer Confusing or Broken? | App/device bug |
| 20 | 5115 | 5,353 | 2.5 GHz WiFi requirement | Connectivity |

Saved to `population.jsonl` with full first-post text.

### G0 Discrimination Probes (20 topics, labels known by construction)

**Known-served (10):** Topics where thread shows confirmed resolution (community fix, workaround, or vendor support)
- 1096 (beep fixed), 26273 (cleaning fixed seal), 722 (C-clamp workaround), 132 (wire fix), 4681 (community helped), 3051 (support resolved), 8811 (support manual intervention), 5115 (2.4GHz info provided), 12241 (restart worked), 717 (water level check)

**Known-unserved (10):** Topics where thread ends unresolved, with "contact support", hardware failure, or persistent bug
- 12736 (replacement also fails), 5021 (component repair only), 4261 (no multi-device solution), 9020 (asking to contact support), 12987 (vendor absent, bug persists), 9165 (no conclusion possible), 10550 (bug persists years later), 13044 (no fix notification), 659 (vendor doesn't monitor), 6924 (APK sideload only)

Saved to `probes.jsonl` with ground truth and evidence.

## Calibration Gates (Pre-declared)

| Gate | Requirement | Status |
|------|-------------|--------|
| **G0** Instrument discrimination | Human+assistant classifies ≥8/10 known-served as served, ≥8/10 known-unserved as unserved | **NOT TESTED** — requires assistant |
| **G1** Population accessibility | ≥20 topics with view_count>0, replies≥1, clear problem | **PASS** — 102 eligible, 20 selected |
| **G2** Arrival signal validity | Spearman ρ(view_count, reply_count) < 0.9 | **NOT TESTED** — computable from data |

## Kill Gates (Pre-declared)

| Gate | Requirement | Status |
|------|-------------|--------|
| **K1** Served share lower bound | Wilson CI95 lower bound ≥ 0.50 | **NOT TESTED** — requires assistant judgments |
| **K2** Difference from E062 | Cannot reject same population as E062 (17/20 = 0.85, CI95 [0.621, 0.948]) | **NOT TESTED** — requires K1 |

## Protocol Deviation

**Deviation:** The protocol specifies GPT-4o or Claude 3.5 Sonnet as the assistant. No API access to either is available in this execution environment (no API keys, no local Ollama, no OpenAI-compatible endpoint).

**Impact:** The central measurement — whether a free general assistant serves the top-arrival needs in this non-technical venue — cannot be made. The G0 discrimination test, which validates the human+assistant instrument before population measurement, cannot run.

**Mitigation attempted:** Checked for local LLM APIs (Ollama, OpenAI-compatible) — none found. Environment variables contain no API keys.

## Decision

**The experiment is blocked on infrastructure.** It cannot proceed to a verdict until run in an environment with GPT-4o or Claude 3.5 Sonnet API access.

The data collection phase is complete and the protocol+data are committed for reproducibility. The next session with API access should:
1. Run `assistant_query.py` (or equivalent) against GPT-4o/Claude API
2. Collect assistant answers for 20 population + 20 probes
3. Perform human judgment (served/unserved) on all 40
4. Compute G0, G1, G2, K1, K2
5. Produce final VERDICT.md with build decision

## Files Committed

- `PROTOCOL.md` — Pre-registered protocol with gates and reachable sets
- `population.jsonl` — 20 population topics with first-post text
- `probes.jsonl` — 20 G0 probes with ground truth from thread resolutions
- `assistant_query.py` — Placeholder script documenting the block
- `VERDICT.md` — This verdict

## Reproducibility

```bash
# Verify data collection
python3 -c "
import json
with open('population.jsonl') as f: pop = [json.loads(l) for l in f]
with open('probes.jsonl') as f: pr = [json.loads(l) for l in f]
print(f'Population: {len(pop)} topics, views range {min(t[\"views\"] for t in pop)}-{max(t[\"views\"] for t in pop)}')
print(f'Probes: {len(pr)} total, served={sum(1 for p in pr if p[\"ground_truth\"]==\"served\")}, unserved={sum(1 for p in pr if p[\"ground_truth\"]==\"unserved\")}')
"
```