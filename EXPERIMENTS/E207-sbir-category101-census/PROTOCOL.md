<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# E207 protocol: does the NIH SBIR category-101 accessibility finding survive a complete census?

**Date:** 2026-10-21. **Author:** opencode session 2026-10-21-001.

## The concrete difficulty this tests

E204 and E206 (2026-10-20) are marked `completed` in `STATE.md` — the reload
point — and report specific numbers: NIH SBIR spending category **101** holds
**147 grants across 134 distinct organizations with top-5 vendor share 11.6%**,
called "the most fragmented market measured in this repository." A committed
prototype (`tools/nih_accessibility_prototype.py`, T-0095) encodes the derived
IC consensus (NIAID, NCI, NHLB, NIA) as recommendations.

Three observed facts make those numbers unverifiable as recorded, each checked
before this protocol was written:

1. **`EXPERIMENTS/E204-sbir-spending-category-screen/` and
   `EXPERIMENTS/E206-sbir-subsegment-category101/` contain only a `RESULT.md`.
   No script, no raw data.** The numbers cannot be recomputed from the repo.
   (This is the F142/D121 pattern: a claim at the reload point with nothing
   behind it.)
2. **The committed prototype's `fetch_grants()` has no `activity_codes`
   filter.** It fetches from all **85,133** FY2023 projects, capped at 2000 in
   default order, then the caller filters the 2000-row sample for a category
   string. It cannot have produced a population of 368, and a 2000-row
   default-order slice of 85,133 is not a census of anything.
3. **The API does report exactly 368 for FY2023 `R41`/`R42`** (verified this
   session, `api.reporter.nih.gov` `/v2/projects/search` with
   `activity_codes:['R41','R42']`), so a *correct* census is reachable — the
   question is whether E204's per-category numbers match it.

This is a mechanism/replication question, not a product question. It decides
whether a number sitting at the reload point and baked into a committed
prototype is real.

## Question (predeclared)

**Does a complete, `R41`/`R42`-filtered census of FY2023 NIH RePORTER projects
reproduce E204's category-101 headline — 147 grants, 134 distinct orgs, top-5
vendor share 11.6% — within a declared tolerance?**

## Instrument

`census.py`. Fetches **all** FY2023 projects with `activity_codes:['R41','R42']`
using the API's own `meta.total` as the stopping condition (no row cap), no
`include_fields` (the default response already carries every field). Records
every row to `raw/census.json`. Deterministic: one pass, no sampling, no seed
needed because there is no random component.

## Gates (declared before the census is run)

Let `G` = grants whose `spending_categories` contains `101`, `O` = distinct
`organization.org_name` among them, `A` = sum of `award_amount` among them, and
`top5` = share of `A` held by the 5 largest-award orgs.

- **G1 (population).** The fetched census size equals the API's reported
  `meta.total` for `R41`/`R42` FY2023 (368 at probe time). Fail = the fetch is
  incomplete or the API moved.
- **G2 (category-101 count).** `G` is within **±10%** of E204's claimed 147
  (i.e. 132–162). Outside that band = E204's count does not reproduce.
- **G3 (distinct orgs).** `O` is within **±10%** of E204's claimed 134
  (121–147). Outside = does not reproduce.
- **G4 (top-5 concentration).** `top5` is within **±5 percentage points** of
  E204's claimed 11.6% (6.6%–16.6%). Outside = does not reproduce, and this is
  the gate that decides whether "most fragmented market" survives.
- **G5 (rank ordering).** The top-5 categories by grant count in the census
  include `101`, `108`, `525`, `701`, `176` (E204's claimed top 5). Absence of
  `101` from the census top 5 = the headline category is not even top-5.

## Kill condition / what each outcome decides

- **All G1–G5 pass:** E204's numbers reproduce from a real census; the finding
  stands as source-supported (though E204's *record* is still defective for
  carrying no script/raw data — that is a documentation fix, not a science
  fix). The committed prototype's *sampling method* remains wrong and is a
  separate defect to note.
- **G2, G3, or G4 fails:** E204's headline does not reproduce from the
  population it names. The claim is withdrawn from the reload point, the
  prototype's IC consensus is marked unverified, and the reason is recorded in
  `FAILURES.md`. The accessibility *pattern* may still hold on the true census
  numbers — this is reported either way, not buried.
- **G1 fails:** the instrument is defective or the API moved; no conclusion
  about E204 either way, and the defect is declared.

## Bound

One census, one comparison. No re-run on unchanged parameters. This does not
test whether NIH SBIR is a good target for a product, whether small programs win
grants, or adoption — only whether the recorded number reproduces.
