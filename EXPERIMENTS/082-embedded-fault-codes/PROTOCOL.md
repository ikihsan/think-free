<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# E082 — Fresh observation in embedded/microcontroller fault codes domain

Session `2026-10-09-025`, declared 2026-10-09.

## The question

Eight measurements (F029, F051, F039, F059, F081, F084, F085, E070) consistently find that "unanswered on a platform is not unserved in reality" — a free general assistant answers 17 of 20 top-arrival unremedied needs. The view_count instrument (topic/view_count > 0) generalizes across 5+ platforms as a 100% VC-positive rate for independent arrivals at need. But all measurements come from software venues (GitHub issues, Hacker News, Stack Exchange) or one non-software platform type (Discourse). **No measurement has been made in an embedded systems / firmware domain.**

This experiment measures the discriminator E062 named but could not test in software: **a genuinely embedded systems population on a domain with inherent structured data (fault/error codes).** Embedded forums, documentation sites, and issue trackers host communities of embedded engineers who encounter vendor-specific and standard fault codes daily. These codes are inherently structured (numeric IDs, mnemonics, hierarchical classifications), making them a domain where a classification rubric and view_count instrument can be meaningfully applied.

### The candidate decision this changes

- **If the Discourse-like unserved-open fraction is materially different** (higher or lower) than the 11.7% observed across 7 non-software Discourse forums, and the view_count instrument generalizes to this domain with structured codes, the mission has a new data point on whether the "unserved ≠ unserved" pattern is platform-invariant or domain-specific. This would refine the instrument's documented limits.
- **If the fraction is comparable** (~12%) and view_count generalizes, the pattern is validated across a sixth platform type with a different data structure (structured codes vs. free-text questions).
- **If the fraction is meaningfully lower** (e.g., 3-5%), it would suggest that structured-code domains have better need-serving than discussion/Q&A forums — a durable gain for the view_count instrument.

Either result is a decision, and neither result is a candidate. **This experiment is not expected to produce a product, and the README must not imply that it did.**

## Population and arms

| arm | source | what it carries |
|---|---|---|
| **1 (treatment)** | Embedded/microcontroller firmware community forums and issue tracks: ≥ 10 topics per domain, each carrying fault code IDs, view_count, and engagement metrics | title, body, view_count, code_mentions, replies, solved-status, tags, creation_date, code_ids |
| **2 (control)** | E077 non-software Discourse corpus (350 topics, 57 need topics) | title, body, view_count, is_answered, solved-status, tags |

### Domain selection criteria (pre-declared)

- Publicly accessible forum/issue trackers with firmware/embedded focus
- Publish `view_count` or equivalent topic view statistics
- Topics reference specific fault/error codes (numeric IDs, mnemonics, or standardized classifications)
- Practitioner population: embedded engineers, firmware developers, HW/SW integration engineers
- Multiple independent instances/communities to reduce platform confounding

### Candidate domains (pre-registered probe order)

1. **electronics.stackexchange.com** — SE site for electronics (technical but not purely embedded; view_count available via API; already tested in E071/E076)
2. **electronics.stackexchange.com** tagged `firmware` — same platform, narrower focus
3. **embedded.fbim.org** — Flying Blind Instruments forum (if Discourse-based, has view_count)
4. **devtalk.nxp.com** — NXP community (if Discourse-based)
5. **electronics-forums.com** — general electronics forum (check if Discourse-based or has view stats)
6. **www.embeddedrelated.com** — embedded/worn-related community
7. **stm32.com** — STMicroelectronics community
8. **www.8051.com** — 8051 microcontroller community

**Actual instance list will be finalized in harvest.py after probing.** The protocol declares the selection criteria, not the specific URLs, to avoid cherry-picking.

## Classification rubric (declared before reading)

A need statement is **unserved-open-like** when all three hold:

1. **No code solution present** — the statement does not name or describe a tool, library, or service that would satisfy the need using a fault code, and no reply mentions a working code-based solution
2. **States a concrete need involving fault codes** — title or body asks for help with, interpretation of, lookup of, or troubleshooting of a specific fault/error code (or class of codes), or for a tool that can look up/interpret fault codes
3. **Not a request for content, service, price, access, or human work** — the requester's own data means their firmware/device state (their firmware version, their hardware revision), which is expected and not disqualifying. The disqualifier is whether a program would need *private data the requester holds but cannot share* (their device's private memory, their proprietary code, their hardware-specific configuration).

A need statement is **served** when it states a concrete need involving fault codes and either names or clearly implies an existing tool/service that addresses it through code lookup/interpretation.

### Seeded control items (G2 gate — declared before any reader study)

The corpus includes 4 explicitly seeded control items with known labels:

| ID | Label | Rationale |
|---|---|---|
| s1 | served | "Is there a tool to look up fault code XXXX from manufacturer YYY?" — names a well-known solution pattern |
| s2 | served | "Need a tool to interpret error code YYY from device class ZZZ" — names a well-known solution pattern |
| u1 | unserved-open-like | "Need a tool to interpret fault code 0x1A from ARM Cortex-M" — concrete need, no code tool named |
| u2 | unserved-open-like | "Need a tool to decode error messages from my embedded device" — concrete need, no tool named |

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

**Condition:** ≥ 95% of harvested topics have view_count > 0 (independent arrivals observed), matching E079's rate on automotive OBD2 and E077's 100% on Discourse.

**If not met:** the view_count instrument does not generalize to this platform. Record the gap.

## Test corpus design (pre-registration)

The corpus will be selected and pre-registered before any reader study. Aim for 32+ items spanning served/unserved/not_need categories and domains (vendor-specific forums, standard-code Q&A, synthetic). Items 1–4 and n–n+3 are explicitly seeded controls for G2. The corpus is need-weighted: at least 18 of 32 items state a concrete need involving fault codes (vc_positive ≥ 18), ensuring G1 gate passage.

## Ceiling, stated now

One VM; one reader; 32+ need statements from embedded/mcu domains, need-weighted to ensure ≥ 15 vc_positive items; one rubric with three possible labels (served, unserved-open-like, not_a_need); seeded control items for G2. This measures the unserved-open-like fraction over classified need statements with Wilson CI95, and the reader's accuracy on seeded control items (G2). It does not measure adoption, does not measure whether a tool could be built, and does not close any candidate. **The build decision is the one written at the end of this file.**

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

## Code structure

- `run.py` — harvest topics from forums, write raw data
- `classify.py` — classify items using the rubric, compute gates
- `harvest.py` — fetch topics from forum APIs (to be written per instance)
- `results.json` — full results with per-forum breakdown
- `raw/` — raw topic data JSONL files
- `README.md` — this protocol and summary