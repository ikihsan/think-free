<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E195 RESULT — the spend axis is open, and a keyword's money belongs to a different industry than the word suggests

**Date:** 2026-10-19. **Outcome: panel 1 G2 FAIL (my request, not the source);
panel 2 G1 PASS, G2 PASS, G3 FAIL, G4 PASS. The axis is usable and the keyword
form is not, on the evidence of two terms.**

Protocol [`PROTOCOL.md`](PROTOCOL.md), correction
[`AMENDMENT-1.md`](AMENDMENT-1.md). Panels: `probe.py` (1), `probe2.py` (2).
Raw: [`raw/probe.json`](raw/probe.json), [`raw/probe2.json`](raw/probe2.json).

## 1. What this establishes

D122 routes the mission's money axis through **spend** because price is
unreachable from this host. This probe asks the only question that matters
before any screen is built on it: **does a spend source answer here, and does it
return rows carrying an amount?**

**Yes, and yes.** `api.usaspending.gov` answers from this host with no key. Its
reference vocabulary returned 52,950 bytes of agencies in panel 1, and in panel 2
a plain-English keyword returned award rows carrying **numeric amounts and free-text
descriptions**.

| row | status | rows | rows with an amount | total |
|---|---|---|---|---|
| `usaspending_agencies` | 200 | reference vocabulary | — | 52,950 bytes |
| `usaspending_laundry` | 200 | 5 | **5** | **$112,839.14** |
| `usaspending_knitting` | 200 | 5 | **5** | **$3,582,719.36** |

**G2 PASS. The spend axis exists on this host.** That is the first time in this
record that an organisation's actual money has been readable, and it is the
precondition D121 requires for the next candidate screen.

## 2. The result that matters: the money is attached to a different industry

**G3 FAILED**, and the way it failed is the finding. The declared bar expected
`laundry` to exceed `knitting` by 2× — intuitively right, since the federal
government buys laundry *services* and does not buy knitting. **The ratio is
0.031: knitting carries 32× more money than laundry.** Reading the descriptions
says why:

- `laundry` → *"LAUNDRY SERVICE FOR THEIR OCS TRAINING"*, *"TY 22 OCS LAUNDRY
  SERVICE FOR 225 PAX"* — base-level service contracts, small.
- `knitting` → *"FIRE RESISTANT ENVIRONMENTAL ENSEMBLES AND OTHER CAMOUFLAGE
  COMBAT UNIFORM CLOTHING ITEMS"*, *"RRB ARMY PHYSICAL FITNESS UNIFORMS"*,
  *"RECRUIT SUSTAINMENT PROGRAM (RSP) ENHANCEMENT ITEMS"* — **military clothing
  procurement, $3.58M.**

**A keyword scan of spend measures procurement vocabulary, not markets.** The word
"knitting" bought combat uniforms, and a screen that summed amounts would have
reported a healthy textile market that is not the one any candidate in this record
was ever about. **This is E194's `TurboScan` defect in a second form and a second
source**: there, a PDF scanner matched *receipt*; here, combat uniforms matched
*knitting*. In both cases the number was confident, plausible, and about something
else.

**The rule this earns: a spend screen must read the descriptions on the rows it
sums, and report the industry distribution beside the total.** A total without a
description audit is not a market measurement.

## 3. Instrument defects found, both mine

**D6 — the 422 was my request.** `spending_by_award` rejected the first attempt
with `"Missing value: 'filters|award_type_codes' is a required field"`. A 4xx
that names the missing field is the endpoint working correctly and the caller
getting it wrong — the same shape as E193's D2. Reachability was never in
question; the 52,950-byte reference response in the same run said so.

**D7 — my G3 could not fail, and it fired on 0 ÷ 0.** The declared condition was
`ratio >= 2.0` **or** one arm non-zero and the other zero. With `amount_total = 0`
on both arms the ratio is `inf`, `inf >= 2.0` is true, and the gate **passed
having observed nothing**, because both requests had failed. This is E017's `H2`
(0 hits satisfying "dead at ≤ 2" on an unread population) and F061's share over
a growing denominator: **a gate whose pass condition is satisfied by an empty
denominator.** Panel 2 adds **G4** — *both* arms must return at least one row
carrying a numeric amount — and G3 is reported `not evaluable` without it. G4 is
in the script, not only in the amendment, so the defect cannot recur silently.

## 4. Limits, declared before the run and not revised after it

1. **Two keywords.** `laundry` and `knitting` were chosen before any result was
   seen and they cannot estimate anything about any domain. The finding is about
   the *shape of the instrument*, not about either market.
2. **Five rows per keyword**, `limit=5`, relevance-ordered, 2020–2023. A screen
   would need a stratified draw, and `G4` only proves the shape carries amounts.
3. **US federal spend only.** It is a real budget with real money, and it is not
   a sample of what any industry pays.
4. **Descriptions are unfiltered free text.** Whether they can be classified
   reliably at scale is untested, and E181's lesson — the same reader disagreed
   with itself on **4 of 10** — applies to any reader over them.

## 5. What this decides

**The money axis named by D122 is open, and the instrument requirement is now
known.** A candidate screen built on spend must (a) read descriptions, not only
amounts; (b) report the industry distribution beside every total; and (c) treat a
keyword's hit count as a property of procurement vocabulary.

**G3 not fired kills the keyword form of this axis**, as declared: federal spend
is also addressable by product and service code (PSC/NAICS), which is a different
vocabulary and a different experiment. That is the named next action, not a retry
with the same words.

[`E193`](EXPERIMENTS/193-source-capability-probe/RESULT.md) measured that this is
the only reachable money source besides the app store, and
[`E194`](EXPERIMENTS/194-appstore-demand-scan/RESULT.md) is the app-store scan
whose `TurboScan` row this instrument defect now explains.