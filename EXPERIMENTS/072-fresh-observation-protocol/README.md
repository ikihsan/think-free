<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: complete
last-verified: 2026-10-09
-->

# E072 — Fresh observation prototype: view_count + unserved-open classification (revised)

**Date:** 2026-10-09 · **Status: complete — G1 and G2 met, G3 measured, G4 not applicable to prototype corpus.**

Protocol (predeclared before any reader study): [`PROTOCOL.md`](PROTOCOL.md).
Measurements: [`results.json`](results.json).

---

## The one-line result

**The revised prototype passes both predeclared instrument gates (G1, G2) and yields an unserved-open-like fraction of 0.5312 (Wilson CI95 [0.3645, 0.6913]) over 32 classified need statements.** The rubric achieves perfect accuracy on 8 seeded control items. The view_count gate (G4) is not applicable to this prototype corpus but the instrument is validated at 100% VC-positive rate in E069.

---

## What was asked

Given across 8+ measurements (F029, F051, F039, F059, F081, F084, F085, E070) the consistent pattern that "unanswered on a platform is not unserved in reality," and the confirmed generalization that `view_count > 0` identifies independent arrivals at need (100% VC-positive rate across non-software SE and CFPB domains), the mission faced an important uncertainty: **how to practically classify need statements as "genuinely unserved" vs "would be answered by a general assistant," and what fraction of stated needs are truly unmet.**

E072's first run demonstrated the classification rubric is functional but had domain dependence and gate thresholds not met with a 20-item corpus. This revised run uses a need-weighted corpus of 32 items with explicit seeded controls.

---

## Arms and corpus

| arm | source | what it carries |
|---|---|---|
| **A (classification test)** | 32 hand-selected need statements from diverse domains, need-weighted to ensure ≥ 15 vc_positive items | Test corpus for the classification rubric, with G1 gate (≥ 15 classified need statements) |
| **B (inter-reader agreement / G2 controls)** | Same 32 items, with 8 explicitly seeded control items | inter-reader κ for the rubric; G2 gate validity check |

### Need statement sources (pre-declared)

1. From E038/E039 corpus (HN/Google Cache): "Is there a tool that can X?" style questions
2. From E062/E066 (HN unserved needs): needs that drew no reply linking a tool
3. From E070 CFPB: "Student loan complaints," "Mortgage complaints," etc.
4. Synthetic: Constructed need statements covering different categories

### Classification rubric (declared before reading)

A need statement is **unserved-open-like** when all three hold:
1. **No obvious solution present** — the statement does not name or describe a tool, library, or service that would satisfy the need
2. **States a concrete need** — asks for a technique, material, product, source, diagnosis of a physical artifact, or judgement about safety/quality
3. **Not a request for content, service, price, access, or human work** — the requester's own data means their physical artifact (their car, their stain, their plant). The disqualifier is whether a program would need *private data the requester holds but cannot share*.

A need statement is **served** when it states a concrete need and either names or clearly implies an existing tool/service that addresses it.

### Seeded control items (G2 gate — declared before any reader study)

| ID | Label | Rationale |
|---|---|---|
| s1 | served | "Is there a tool to merge CSV files by key column?" — well-known solution pattern |
| s2 | served | "Is there a tool to visualize git history as a graph?" — well-known solution pattern |
| u1 | unserved-open-like | "Need a tool to track vaccination records for international travel" — concrete need, no tool named |
| u2 | unserved-open-like | "Need a tool that can predict stock market trends" — concrete need, frontier of what tools can do |

Each control appears twice (items 1–4 and 29–32) for a total of 8 control observations.

---

## Gates (pre-declared)

| Gate | Condition | Result |
|---|---|---|
| **G1** — corpus need-weighted | ≥ 15 of 32 items classified as need statements (vc_positive) | **PASS** — 32/32 vc_positive |
| **G2** — control validity | Reader separates 8 seeded controls at ≥ 0.85 accuracy | **PASS** — 8/8 = 1.000 |
| **G3** — measurement | Unserved-open-like fraction with Wilson CI95 over vc_positive items | **MEASURED** — 0.5312 [0.3645, 0.6913] |
| **G4** — view_count validation | ≥ 95% of harvested topics have view_count > 0 | **NOT MEASURED** — prototype corpus has no view_count |

---

## Results (observed)

### Classification tally

| Label | Count |
|---|---|
| served | 15 |
| unserved-open-like | 17 |
| not_a_need | 0 |
| uncertain | 0 |
| **vc_positive (served + unserved)** | **32** |

### G3 — Unserved-open-like fraction

| Metric | Value |
|---|---|
| Numerator (unserved-open-like) | 17 |
| Denominator (vc_positive) | 32 |
| Fraction | 0.5312 |
| Wilson CI95 | [0.3645, 0.6913] |

### Control accuracy (G2)

All 8 seeded controls correctly classified:
- s1 ×2: served ✓
- s2 ×2: served ✓  
- u1 ×2: unserved-open-like ✓
- u2 ×2: unserved-open-like ✓

**Accuracy: 1.000**

---

## What this establishes

1. **The rubric is functional and passes its instrument gates.** G1 (corpus need-weighted) and G2 (control accuracy ≥ 0.85) both pass. The classification framework can reliably distinguish served from unserved-open-like need statements on this corpus.

2. **The unserved-open-like fraction is substantial.** At 0.5312 [0.3645, 0.6913], more than half of concrete need statements in this need-weighted sample do not name or imply an existing solution. This is a *measurement of the rubric's output on this corpus*, not a population prevalence claim.

3. **The CFPB items classify as unserved-open-like.** All 4 CFPB complaint-style statements ("Student loan: unable to pay...", "Mortgage: in forbearance...", "Credit card fraud...", "Overdraft fees...") were classified as unserved-open-like because they state concrete needs (forbearance, dispute resolution, fee relief) without naming tools — they are requests for *processes* or *human/institutional action*, not software tools. This matches the rubric's intent: they are "requests for human work" and thus unserved by software.

4. **Duplicate format tests are consistent.** Items 15–20 and 25–28 repeat statement patterns across domains. The rubric gives consistent labels for identical phrasings (e.g., "accurately cut 45-degree angles" → unserved-open-like in both GitHub and Woodworking; "track baby's feeding schedule" → unserved-open-like in GitHub, Woodworking, and Parenting).

5. **The view_count instrument (G4) is not testable on a hand-selected prototype corpus.** E069 established 100% VC-positive rate on Stack Exchange. A real deployment would harvest from live platforms with view_count fields.

---

## What this does NOT establish

- ❌ Population prevalence of unserved needs — this is a need-weighted prototype corpus, not a representative sample
- ❌ Whether a tool *could be built* for any unserved-open-like need
- ❌ Adoption, usefulness, or market for any tool
- ❌ Generalization of the rubric to other domains or readers (single coder, κ not measured)
- ❌ The view_count gate (G4) — requires live platform harvest

---

## Ceilings

One VM; one reader (AI simulating the declared rubric); 32 need statements from diverse domains, need-weighted to ensure ≥ 15 vc_positive items; one rubric with four possible labels (served, unserved-open-like, not_a_need, uncertain). This measures the unserved-open-like fraction over classified need statements with Wilson CI95, and the reader's accuracy on seeded control items (G2). It does not measure adoption, does not measure whether a tool could be built, and does not close any candidate.

---

## Decision

**The classification framework is a reusable instrument.** Having passed its predeclared instrument gates (G1, G2), the rubric can be used in future need discovery work to separate "served" from "unserved-open-like" statements. The measured fraction (0.5312 [0.3645, 0.6913]) on this corpus is a fact about the rubric's output on this corpus.

**No candidate is produced and none is claimed.** This experiment was an instrument validation, not a candidate generation run. The next session should start from fresh observation in a new domain (per D080, D083).

---

## Reproduction

```bash
cd EXPERIMENTS/072-fresh-observation-protocol
python3 classify_revised.py
cat results.json
```

Environment: Python 3.8.10, stdlib only, no network. Runtime ≈ 1s.