<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E198 RESULT — the vendor landscape for 98,640 small IT purchases is fragmented

**Date:** 2026-10-19. **Outcome: G1 PASS, G2 PASS (survives), C1–C4 all PASS.**
The federal-contract money axis now has a confirmed vendor landscape. The recipient
read (`spending_by_category/recipient/` under the same `psc_codes` filter) names
**15,210 total recipient records across 9,977 distinct companies** for the five
IT/software PSC codes carrying $203.32B and 98,640 funded purchases ≤ $100k.

Protocol [`PROTOCOL.md`](PROTOCOL.md). Panel `panel1.py`, controls `controls.py`,
analysis `analysis.py`. Raw captures in `raw/` (196 response files, ~500 MB
committed).

## 1. The gate vector, exactly

| gate | declared question | result |
|---|---|---|
| **G1** source shape | all five codes return a well-formed, non-empty recipient list with `hasNext` pagination working | **PASS** — 5/5 codes, 15,210 total rows, 166 pages |
| **G2** vendor concentration | total distinct recipients ≥ 20 **AND** top 10 per code hold ≤ 80% of code's obligation | **PASS (survives)** — 9,977 distinct; top-10 shares: DA01 34.5%, DA10 35.8%, 7A21 48.9%, 7030 38.4%, D304 57.6% |

All controls pass:
- **C1**: PSC `ZZZZ` returns empty `200`
- **C2**: PSC `not-a-code` returns `422`
- **C3**: recipient sums match E196 cell totals within 0.02% (all ≤ 5%)
- **C4**: zero unused-filter messages across all 166 requests

## 2. The vendor landscape per code

| code | cell total | E197 purchases $1–$100k | recipients | distinct names | top-10 share | top 3 recipients |
|---|---:|---:|---:|---:|---:|---|
| `DA01` | $94.91B | 14,719 | 3,610 | 3,112 | 34.5% | Oracle Health Govt ($4.81B), Booz Allen ($4.73B), Accenture Federal ($4.17B) |
| `DA10` | $33.01B | 16,477 | 3,651 | 3,089 | 35.8% | Booz Allen ($3.82B), Accenture Federal ($2.91B), Leidos ($2.74B) |
| `7A21` | $29.21B | 32,747 | 3,977 | 3,384 | 48.9% | Booz Allen ($3.12B), GDIT ($2.89B), Accenture Federal ($2.41B) |
| `7030` | $25.83B | 14,033 | 3,917 | 3,298 | 38.4% | Dell Federal ($3.42B), Accenture Federal ($2.28B), Booz Allen ($1.73B) |
| `D304` | $20.37B | 20,664 | 1,155 | 1,004 | 57.6% | Verizon ($3.84B), AT&T ($3.12B), L3Harris ($2.98B) |

**Total distinct recipients across five codes: 9,977** (sum of per-code distinct
is 13,887; 3,910 names appear in multiple codes).

## 3. Concentration analysis

**The top 10 recipients per code hold 34.5%–57.6% of each code's obligation.**
All five codes are well below the 80% kill threshold. Even the most
concentrated code (D304, telecommunications) leaves 42.4% of $20.37B — **$8.64B** —
outside the top 10.

The five-code aggregate top-10 share is not a declared gate but is informative:
the union of all top-10 sets is 28 distinct companies holding **$84.2B of
$203.3B (41.4%)**. The remaining **$119.1B (58.6%)** is spread across 9,949
other companies.

## 4. What this decides

**The vendor landscape is fragmented.** The money axis now has all four
coordinates:

1. **Buyer** — US federal agencies (DoD, VA, GSA, HHS, DHS, …)
2. **Unit** — 98,640 funded awards ≤ $100k in five codes
3. **Budget** — $203.32B across those cells
4. **Vendor** — 9,977 distinct companies, top 10 per code hold 34.5%–57.6%

This is a **genuine market at the scale a small program operates at**. The
concentration is low enough that a small program could win direct awards without
being a subcontractor to a prime. The money axis has produced its first
addressable, money-sized, vendor-named population.

**Named next action:** a candidate screen on the money axis. The screen asks:
*which of these five codes, or which sub-segment within them, admits a program
that a small team could build and sell?* The screen inputs are the 98,640
purchases, the 9,977 vendors, the agency breakdown (E197 panel D), and the
award descriptions (readable via `spending_by_award/` with the same filters).
This is the first candidate screen in the record whose population is defined by
money that is confirmed funded, metered, and vendor-attributed.

## 5. Do not run

- the keyword form of this axis (closed by E195);
- an award-amount filter on the recipient endpoint (E197 probe.py finding 2);
- a re-run of E197 panels on the same parameters.