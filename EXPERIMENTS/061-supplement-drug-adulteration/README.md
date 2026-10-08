# E061 — Do dietary supplement recalls show persistent drug adulteration patterns across multiple firms? (probe)

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: complete
last-verified: 2026-10-08
-->

## Question

Fresh observation (per D080): do specific unapproved drugs repeatedly appear in supplement recalls from different firms, indicating persistent supply-chain contamination that consumers cannot detect?

## Method

- Source: FDA food enforcement API, 1000 most recent recalls (2026-10-08)
- Filter: dietary supplement recalls (identified by product/firm/reason keywords: supplement, dietary, vitamin, protein, capsule, tablet, softgel, powder, colostrum, spermidine, herbal, botanical, probiotic, prebiotic)
- Instrument: search recall reason text for known adulterant drug names (PDE5 inhibitors, weight-loss drugs, anabolic steroids, stimulants, chloramphenicol, etc.)
- Kill gate (declared): if no drug class appears in recalls from ≥3 distinct firms, the persistent-contamination population is not observed → KILL.

## Results

`supplement_recalls=142`, `food_recalls=858`.

Drug mentions in supplement recalls (distinct firms):
- chloramphenicol: 4 firms (National Enzyme Co, Global Health Laboratories, Kirkman Group, Health Wright Products)
- tadalafil: 1 firm
- picamilon: 1 firm
- methylpentane/dmba: 1 firm
- aegeline: 1 firm

Chloramphenicol (a banned antibiotic) recurs across 4 firms, all linked to contaminated raw materials (whey, chlorella/spirulina sources).

## Reading

The chloramphenicol signal exceeds the kill gate (≥3 firms). However:
1. This contamination mode is **already known to FDA** — import alerts and guidance exist for chloramphenicol in aquaculture/honey/supplement ingredients.
2. The recurrence is **ingredient-specific** (chlorella, whey protein concentrate) not product-specific — consumers have no ingredient-supply-chain visibility.
3. Only 4 firms in 142 supplement recalls (2.8%) — too rare for a consumer-facing tool to have meaningful coverage.
4. FDA already publishes "tainted supplements" warnings and import alerts for these exact adulterants.

## Verdict

**KILL for a candidate.** The chloramphenicol recurrence is real (F093) but the serving channel is FDA's existing import alerts and tainted-supplements database. The contamination is ingredient-supply-chain-level, not product-level, so no consumer-facing tool can reliably warn without supply-chain transparency that does not exist. Nothing built.

Raw data: `raw/results.json`.