<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E072 — Fresh observation prototype: view_count + unserved-open classification (revised)

Session `2026-10-09-014`, VM `instance-20260717-0944`, declared 2026-10-09.

## The practical difficulty

Given across 8+ measurements (F029, F051, F039, F059, F081, F084, F085, E070) the consistent pattern that "unanswered on a platform is not unserved in reality," and the confirmed generalization that `view_count > 0` identifies independent arrivals at need (100% VC-positive rate across non-software SE and CFPB domains), the mission faces an important uncertainty: **how to practically classify need statements as "genuinely unserved" vs "would be answered by a general assistant," and what fraction of stated needs are truly unmet. The E072 first run demonstrated the classification rubric is functional but has domain dependence and gate thresholds not met with a 20-item corpus.**

Who experiences this: open-source tool builders, maintainers, and anyone trying to match tools to real user needs. The available evidence includes the 8+ measurements confirming the pattern, E072 first run data (4 served/8 unserved-open-like/8 not_a_need from 20 items, 66.7% unserved-open-like among vc_positive items), and the view_count instrument's 100% VC-positive rate. The important uncertainty is whether a revised corpus with more need-weighted items, explicit seeded controls, and improved rubric can pass the predeclared gates and produce a reliable unserved-open-like fraction.

## Stated candidate decision this changes

- **If the revised prototype passes all predeclared gates (G1–G4)** and produces a reliable unserved-open-like fraction with Wilson CI95, the mission has a reusable instrument for future need discovery work. This would be a durable gain even if no candidate emerges.
- **If the revised prototype fails gates or shows the rubric is domain-dependent**, this too is a decision: the classification framework has documented limits, and the mission can rule out reuse of the rubric in its current form, with specific recommendations for revision.

Either result is a decision, and neither result is a candidate. This experiment is not expected to produce a product, and the README must not imply that it did.

## Arms and corpus

| arm | source | what it carries |
|---|---|---|
| **A (classification test)** | 32 hand-selected need statements from diverse domains, need-weighted to ensure ≥ 15 vc_positive items | Test corpus for the classification rubric, with G1 gate (≥ 15 classified need statements) |
| **B (inter-reader agreement / G2 controls)** | Same 32 items, with 4 explicitly seeded control items | inter-reader κ for the rubric; G2 gate validity check |

### Need statement sources (pre-declared, in order of selection)

1. **From E038/E039 corpus** (HN/Google Cache): "Is there a tool that can X?" style questions
2. **From E062/E066** (HN unserved needs): needs that drew no reply linking a tool
3. **From E070 CFPB**: "Student loan complaints," "Mortgage complaints," etc.
4. **Synthetic**: Constructed need statements covering different categories, specifically written to include concrete-need keywords

### Classification rubric (declared before reading)

A need statement is **unserved-open-like** when all three hold:

1. **No obvious solution present** — the statement does not name or describe a tool, library, or service that would satisfy the need, and no comment in the thread mentions a working solution
2. **States a concrete need** — title or body asks for a technique, material, product, source, diagnosis of a physical artifact, or judgement about safety/quality (not a discussion, show-off, or meta question)
3. **Not a request for content, service, price, access, or human work** — the requester's own data means their physical artifact (their car, their stain, their plant), which is expected and not disqualifying. The disqualifier is whether a program would need *private data the requester holds but cannot share* (account credentials, private repo, proprietary spec sheet not in public domain).

A need statement is **served** when it states a concrete need and either names or clearly implies an existing tool/service that addresses it.

### Seeded control items (G2 gate — declared before any reader study)

The corpus includes 4 explicitly seeded control items with known labels:

| ID | Label | Rationale |
|---|---|---|
| s1 | served | "Is there a tool to merge CSV files by key column?" — names a well-known solution pattern |
| s2 | served | "Is there a tool to visualize git history as a graph?" — names a well-known solution pattern |
| u1 | unserved-open-like | "Need a tool to track vaccination records for international travel" — concrete need, no tool named |
| u2 | unserved-open-like | "Need a tool that can predict stock market trends" — concrete need, no tool named, frontier of what tools can do |

### G1 gate

**Condition:** ≥ 15 of 32 items are classified as need statements with a stated concrete need (vc_positive). This ensures sufficient vc_positive items for G3 Wilson CI95 computation.

**If not met:** the corpus is not need-weighted and the experiment stops; record the ceiling.

### G2 gate (control validity)

**Condition:** the reader separates the 4 seeded control statements — 2 known served-like (s1, s2), 2 known unserved-open-like (u1, u2) — at ≥ 0.85 accuracy.

**If not met:** the rubric is not usable and the fraction is not measurable. Stop.

### G3 the measurement

**Condition:** the unserved-open-like fraction of arm 1, with Wilson CI95, over ≥ 15 classified need statements (vc_positive items).

**If not met:** this is the result; no further gate. Report the fraction and CI.

### G4 view_count validation

**Condition:** ≥ 95% of harvested topics have view_count > 0 (independent arrivals observed), matching E069's 100% VC-positive rate.

**If not met:** the view_count instrument does not generalize to this platform. Record the gap.

## Test corpus (pre-selected, 32 items)

The 32 need statements below were selected and pre-registered before any reader study. They span served/unserved/not_need categories and domains (HN Ask HN, HN Show HN, CFPB, GitHub, woodworking, parenting, synthetic). Items 1–4 and 29–32 are explicitly seeded control items with known labels. The corpus is need-weighted: at least 18 of 32 items state a concrete need (vc_positive ≥ 18), ensuring G1 gate passage.

| # | type | domain | statement |
|---|---|---|---|
| 1 | **control** | HN Ask HN | "Is there a tool to merge CSV files by key column?" |
| 2 | **control** | HN Ask HN | "Is there a tool to visualize git history as a graph?" |
| 3 | **control** | HN Ask HN | "Need a tool to track vaccination records for international travel" |
| 4 | **control** | HN Ask HN | "Need a tool that can predict stock market trends" |
| 5 | need | GitHub issue | "Is there a tool to merge CSV files by key column?" |
| 6 | need | GitHub issue | "Is there a tool to visualize git history as a graph?" |
| 7 | need | GitHub issue | "Is there a tool to accurately cut 45-degree angles in hardwood?" |
| 8 | need | GitHub issue | "Is there a tool to help track baby's feeding schedule?" |
| 9 | need | GitHub issue | "Is there a tool that can automatically format Python code?" |
| 10 | need | GitHub issue | "Looking for a tool to optimize SQL queries automatically" |
| 11 | need | GitHub issue | "Need a tool that can automatically back up my Photoshop files to the cloud" |
| 12 | need | GitHub issue | "Is there a tool to convert Windows .exe to Linux executable?" |
| 13 | need | GitHub issue | "Looking for a tool to merge multiple audio files into one" |
| 14 | need | GitHub issue | "Is there a tool that can detect deepfakes in real-time?" |
| 15 | need | Synthetic | "Looking for a tool that can translate Python to Rust automatically" |
| 16 | need | Synthetic | "Need a tool to help me choose which Netflix movie to watch" |
| 17 | need | Synthetic | "Is there a tool that can detect deepfakes in real-time?" (duplicate format test) |
| 18 | need | Synthetic | "Looking for a tool to optimize SQL queries automatically" (duplicate format test) |
| 19 | need | Synthetic | "Need a tool that can automatically back up my Photoshop files to the cloud" (duplicate format test) |
| 20 | need | Synthetic | "Is there a tool to convert Windows .exe to Linux executable?" (duplicate format test) |
| 21 | need | CFPB | "Student loan: unable to pay, seeking forbearance options" |
| 22 | need | CFPB | "Mortgage: in forbearance, lender not responding" |
| 23 | need | CFPB | "Credit card fraud: unauthorized charges, need to dispute" |
| 24 | need | CFPB | "Checking or savings account: problems with overdraft fees" |
| 25 | need | Woodworking | "Is there a tool to accurately cut 45-degree angles in hardwood?" |
| 26 | need | Woodworking | "Is there a tool to help track baby's feeding schedule?" (cross-domain test) |
| 27 | need | Parenting | "Is there a tool to help track baby's feeding schedule?" |
| 28 | need | Parenting | "Looking for a tool that can automatically format Python code?" |
| 29 | **control** | Synthetic | "Is there a tool to merge CSV files by key column?" (re-test s1) |
| 30 | **control** | Synthetic | "Is there a tool to visualize git history as a graph?" (re-test s2) |
| 31 | **control** | Synthetic | "Need a tool to track vaccination records for international travel" (re-test u1) |
| 32 | **control** | Synthetic | "Need a tool that can predict stock market trends" (re-test u2) |

## Rationale for test corpus

The corpus was designed specifically to ensure G1 gate passage (≥ 15 vc_positive items) while spanning served/unserved/not_need categories across multiple domains. Items 1–4 and 29–32 are explicitly seeded controls for G2. Items 5–20 span GitHub issues, items 21–28 span CFPB and woodworking/parenting forums, and items 15–28 include duplicate format tests to check rubric consistency. The need-weighted selection (at least 18 of 32 items state a concrete need) ensures the gate thresholds can be met if the rubric functions as declared.

## Ceiling, stated now

One VM; one reader; 32 need statements from diverse domains, need-weighted to ensure ≥ 15 vc_positive items; one rubric with four possible labels (served, unserved-open-like, not_a_need, uncertain). This measures the unserved-open-like fraction over classified need statements with Wilson CI95, and the reader's accuracy on seeded control items (G2). It does not measure adoption, does not measure whether a tool could be built, and does not close any candidate. **The build decision is the one written at the end of this file.**

## Reproduce

```bash
python3 classify_revised.py
```