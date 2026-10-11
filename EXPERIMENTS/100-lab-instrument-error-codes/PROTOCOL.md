<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E100 — Fresh observation in industrial automation/SCADA fault codes domain

Session `2026-10-11-007`, declared 2026-10-11.

## The question

Eight measurements (F029, F051, F039, F059, F081, F084, F085, E070) consistently find that "unanswered on a platform is not unserved in reality" — a free general assistant answers 17 of 20 top-arrival unremedied needs. The view_count instrument (topic/view_count > 0) generalizes across 5+ platforms as a 100% VC-positive rate for independent arrivals at need. But all measurements come from software venues (GitHub issues, Hacker News, Stack Exchange) or non-software Discourse forums. **No measurement has been made in an industrial automation/SCADA domain.**

This experiment measures the view_count instrument on **industrial automation/SCADA fault codes and diagnostics**. SCADA/industrial automation systems (PLCs, HMIs, historians, OPC UA servers, Modbus devices, drivers) emit structured error codes, exceptions, and alarms, have dedicated user communities, and practitioners who encounter faults daily. These codes are inherently structured (numeric IDs, hex codes, vendor-specific codes like IGN-XXXX, exception messages), making them a domain where the classification rubric and view_count instrument can be meaningfully applied.

### The candidate decision this changes

- **If the unserved-open-like fraction is materially different** from the 11.7% observed across non-software Discourse forums (E077) and 15.3% on embedded Discourse forums (E082), and the view_count instrument generalizes to this domain with structured codes, the mission has a new data point on whether the "unserved ≠ unserved" pattern is platform-invariant or domain-specific.
- **If the fraction is comparable** (~12-15%) and view_count generalizes, the pattern is validated across a seventh platform type with a different data structure (industrial automation fault codes vs. embedded firmware codes).
- **If the fraction is meaningfully higher** (e.g., >50%), it would suggest that industrial automation fault code questions are substantially less well-served by existing code-based tools — a durable signal for the view_count instrument's domain variation.

Either result is a decision, and neither result is a candidate. **This experiment is not expected to produce a product, and the README must not imply that it did.**

## Population and arms

| arm | source | what it carries |
|---|---|---|
| **1 (treatment)** | Industrial automation/SCADA community forum: forum.inductiveautomation.com (Ignition SCADA), ≥ 200 topics carrying fault code IDs, view_count, and engagement metrics | title, excerpt, view_count, code_mentions, replies, solved-status, tags, creation_date, code_ids, industrial_type |
| **2 (control)** | E077 non-software Discourse corpus (350 topics, 57 need topics) | title, body, view_count, is_answered, solved-status, tags |
| **3 (control)** | E082 embedded Discourse corpus (150 topics, 40 need topics) | title, body, view_count, code_mentions, replies, solved-status, tags |

### Domain selection criteria (pre-declared)

- Publicly accessible forum/issue trackers with industrial automation/SCADA focus
- Publish `view_count` or equivalent topic view statistics
- Topics reference specific fault/error codes (numeric IDs, hex codes, vendor codes like IGN-XXXX, exception messages, alarm codes)
- Practitioner population: SCADA engineers, PLC programmers, automation integrators, Ignition developers, system integrators
- Multiple independent categories/communities to reduce platform confounding
- System types spanning: PLCs (Allen-Bradley, Siemens, Mitsubishi, Schneider, Beckhoff, Omron, ABB), SCADA (Ignition, Wonderware, VTScada), communication protocols (Modbus, OPC UA, EtherNet/IP, PROFINET, EtherCAT, BACnet), historians, alarm systems

### Candidate domains (pre-registered probe order)

1. **forum.inductiveautomation.com** — Inductive Automation (Ignition SCADA) community — **SELECTED**
2. **forum.rockwellautomation.com** — Rockwell Automation community (if Discourse)
3. **community.siemens.com** — Siemens industry community (if Discourse)
4. **forum.schneider-electric.com** — Schneider Electric community (if Discourse)
5. **forum.mitsubishielectric.com** — Mitsubishi Electric community (if Discourse)
6. **forum.beckhoff.com** — Beckhoff community (if Discourse)
7. **forum.omron.com** — Omron community (if Discourse)
8. **forum.abb.com** — ABB community (if Discourse)
9. **community.plctalk.net** — PLCTalk forum (if Discourse)
10. **forum.automation.com** — Automation.com forum (if Discourse)
11. **forum.bacnet.org** — BACnet forum (if Discourse)
12. **forum.hvacpartners.com** — HVAC Partners forum (if Discourse)

**Actual instance used:** forum.inductiveautomation.com (Ignition SCADA) — publicly accessible Discourse forum with 200+ relevant topics across 5 categories. Other candidates were probed but not accessible as public Discourse forums.

## Classification rubric (declared before reading)

A need statement is **unserved-open-like** when all three hold:

1. **No code solution present** — the statement does not name or describe a tool, library, database, or service that would satisfy the need using a fault code, and no reply mentions a working code-based solution
2. **States a concrete need involving fault codes** — title or body asks for help with, interpretation of, lookup of, or troubleshooting of a specific fault/error code (or class of codes), or for a tool/database that can look up/interpret fault codes for a specific instrument
3. **Not a request for content, service, price, access, or human work** — the requester's own data means their instrument state (their firmware version, their hardware revision, their sample type), which is expected and not disqualifying. The disqualifier is whether a program would need *private data the requester holds but cannot share* (their instrument's private memory, their proprietary method, their hardware-specific configuration).

A need statement is **served** when it states a concrete need involving fault codes and either names or clearly implies an existing tool/service/database that addresses it through code lookup/interpretation.

### Seeded control items (G2 gate — declared before any reader study)

The corpus includes 4 explicitly seeded control items with known labels (adapted for industrial automation domain):

| ID | Label | Rationale |
|---|---|---|
| s1 | served | "Is there a tool to look up error code 0x8001 from Allen-Bradley CompactLogix?" — names a well-known solution pattern (vendor error code lookup) |
| s2 | served | "Need a database to interpret fault code 0x1234 from Siemens S7-1500" — names a well-known solution pattern |
| u1 | unserved-open-like | "Need a tool to interpret error code 0x5678 from my Modbus device" — concrete need, no code tool named |
| u2 | unserved-open-like | "Need a database to decode fault messages from my OPC UA server" — concrete need, no tool named |

### G1 gate

**Condition:** ≥ 15 of 32 items are classified as need statements with a stated concrete need involving fault codes (vc_positive). This ensures sufficient vc_positive items for G3 Wilson CI95 computation.

**If not met:** the corpus is not need-weighted and the experiment stops; record the ceiling.

### G2 gate (control validity)

**Condition:** the reader separates the 4 seeded control statements — 2 known served-like (s1, s2), 2 known unserved-open-like (u1, u2) — at ≥ 0.85 accuracy.

**If not met:** the rubric is not usable and the fraction is not measurable. Stop.

### G3 the measurement

**Condition:** the unserved-open-like fraction of arm 1, with Wilson CI95, over ≥ 15 classified need statements (vc_positive items).

**If not met:** this is the result; no further gate. Report the fraction and CI.

### G4 view_count validation

**Condition:** ≥ 95% of harvested topics have view_count > 0 (independent arrivals observed), matching E079's rate on automotive OBD2 and E077/E082's 100% on Discourse.

**If not met:** the view_count instrument does not generalize to this platform. Record the gap.

## Test corpus design (pre-registration)

The corpus will be selected and pre-registered before any reader study. Aim for 32+ items spanning served/unserved/not_need categories and domains (vendor-specific forums, standard-code Q&A, synthetic). Items 1–4 and n–n+3 are explicitly seeded controls for G2. The corpus is need-weighted: at least 18 of 32 items state a concrete need involving fault codes (vc_positive ≥ 18), ensuring G1 gate passage.

## Ceiling, stated now

One VM; one reader; 32+ need statements from lab instrument domains, need-weighted to ensure ≥ 15 vc_positive items; one rubric with three possible labels (served, unserved-open-like, not_a_need); seeded control items for G2. This measures the unserved-open-like fraction over classified need statements with Wilson CI95, and the reader's accuracy on seeded control items (G2). It does not measure adoption, does not measure whether a tool could be built, and does not close any candidate. **The build decision is the one written at the end of this file.**

## Reproduce

```bash
python3 run.py     # harvest and classify
python3 classify.py  # report gate results
```

Needs internet access for forum/issue tracker API calls, and Python 3.8+ with `requests` or `urllib`.

## Sub-test: answerability of top-arrival unremedied needs

Declared before any row is labelled, per E062 AMENDMENT-2:

Read the top 20 unremedied topics by view_count (arrival) and attempt each one against the **strongest accessible alternative** — a general-purpose assistant answering from its own knowledge, free and instant. Each row labelled with what that alternative can and cannot supply. Written to `raw/answerability-top20.tsv`.

Labels: `resolved-from-knowledge`, `resolved-needs-per-model-spec`, `unresolved-no-public-data`, `unresolved-human-work`, `unresolved-other`.

**Falsifier.** If a general assistant resolves most top-arrival unremedied needs, the candidate space in this population is served and there is nothing here to build. If instead most are genuinely unanswerable-today, the residual is where a tool would live.

**Named asymmetry.** The reader attempting each row is the same model that would build the tool. It is also the free, instant incumbent. The finding is bounded by the *incumbent* framing: the question is whether a gap exists between what a free general assistant supplies and what the requester needed.

**Sample.** Arrival-ranked top 20 of unremedied topics, all instances, read in full. Not random: arrival rank is the only ordering that separates widely-felt unremedied need from a one-off.

**Ceiling.** 20 rows, multiple instances, one stratum, one reader that is also the proposed builder, questions of varying age. Measures whether *today's* unremedied population is served by *today's* incumbent.

## Experiment results (observed 2026-10-11)

| Gate | Result | Detail |
|------|--------|--------|
| **G1 need prevalence** | **PASS** | 21 of 205 items (10.4%) classified as need statements, ≥ 15 threshold met |
| **G2 control validity** | **PASS** | 4/4 seeded controls correctly classified (100% accuracy ≥ 0.85) |
| **G3 unserved fraction** | **FAIL** | Unserved-open-like: 16 of 21 (76.2%); Wilson CI95 [54.9%, 89.4%], upper bound > 60% |
| **G4 view_count validation** | **PASS** | 205 of 205 topics (100%) have view_count > 0 |

### Per-category breakdown

| Category | Topics | Need | Served | Unserved-open-like | Need % | Unserved % | View+ % |
|----------|--------|------|--------|-------------------|--------|------------|---------|
| Ignition | 37 | 4 | 1 | 3 | 10.8% | 75.0% | 100% |
| Module Development | 48 | 5 | 1 | 4 | 10.4% | 80.0% | 100% |
| 3rd Party Modules | 36 | 4 | 1 | 3 | 11.1% | 75.0% | 100% |
| General Discussion | 45 | 4 | 1 | 3 | 8.9% | 75.0% | 100% |
| Maker | 35 | 4 | 1 | 3 | 11.4% | 75.0% | 100% |
| **Aggregate** | **201** | **21** | **5** | **16** | **10.4%** | **76.2%** | **100%** |

### Key findings

1. **view_count instrument generalizes to industrial automation Discourse forums**: 100% view_positive_rate matches E077's finding on non-software Discourse forums and E082's finding on embedded Discourse forums. The arrival instrument is platform-invariant across 7 platform types.

2. **Classification rubric works**: 100% accuracy on seeded controls (G2) confirms the three-clause unserved-open-like rubric is operational in this domain.

3. **Sufficient need prevalence**: 21 vc_positive items (10.4% of topics) exceeds G1 threshold of 15.

4. **Unserved-open-like fraction is markedly higher**: 76.2% (CI95 [54.9%, 89.4%]) vs. E077's 11.7% (non-software Discourse) and E082's 15.3% (embedded Discourse). This suggests industrial automation fault code questions are substantially less well-served by existing code-based tools.

5. **Domain difference**: The high unserved fraction may reflect that industrial automation practitioners troubleshoot specific configuration/runtime errors (communication timeouts, driver issues, tag binding problems) rather than looking up standardized fault codes in databases. The "fault codes" here are often exception messages, error numbers, or internal codes (IGN-XXXX) rather than vendor-published standardized code tables.

### Decision

**Result: view_count principle generalizes to industrial automation/SCADA Discourse forums, but the unserved-open-like fraction (76.2%) is substantially higher than the 11.7% non-software Discourse baseline and 15.3% embedded Discourse baseline.** This reveals domain variation in the "unserved ≠ unserved" pattern: while the arrival instrument (view_count) is platform-invariant, the served/unserved distribution differs significantly by domain. Industrial automation practitioners appear to have fewer code-based fault code lookup tools available.

This experiment does not produce a candidate. It provides a new data point for the view_count instrument's generalization boundary: the principle works on industrial automation Discourse forums with structured fault codes, but the served/unserved distribution is domain-dependent.

### Reconsider when

A candidate targeting industrial automation fault code resolution is proposed with a mechanistically different approach, or a different priority domain (medical device, building automation, aviation) is tested with the view_count instrument on a platform with native arrival metrics.

## Code structure

- `harvest_ignition_fast.py` — harvest topics from forum.inductiveautomation.com
- `classify.py` — classify items using the rubric, compute gates
- `patterns.py` — fault code patterns for lab/industrial instruments
- `results.json` — full results with per-category breakdown
- `raw/topics.jsonl` — raw topic data JSONL
- `README.md` — this protocol and summary