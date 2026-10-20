<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E194 AMENDMENT 2 — the negative control was not negative, and `limit=200` pads

**Declared:** 2026-10-19, after panel 1 ran and before panel 2 was sent.
**No bar is moved.** G3 keeps its numeric bar and is applied to a *smaller*
window, which makes it harder to pass, not easier.

## 1. Panel 1 stands as declared

`scan.py` returned **G1 PASS, G2 FAIL, G3 FAIL, G4 PASS, G5 PASS.** G2 firing
makes every difficulty row `not_evaluated` under the protocol, so panel 1
reports **no demand finding**, and its apparent `receipt scanner` hit is not a
result. Panel 1 is not re-run and its table is not quoted as evidence.

## 2. Two defects, both in the instrument, found by reading the bytes

**D3 — the negative control was not a negative control.** The declared term was
`zzqxqv glorb tapestry`, and **`tapestry` is an English word**. The API returned
`Wool Sort: Pixel Screw Yarn`, `Tapestry Crochet`, `Threaded Color Paint By
Number`, `Yarn Jam`, `iWeaveIt` — 19 results. A match was the correct behaviour
and the control was badly chosen. A control that fails for a reason other than
the one it was built to detect is not evidence about the source.

**D4 — `limit=200` pads the tail, and a padded window measures the padding.**
The same term fetched twice at different limits:

| term | `limit=20` resultCount | `limit=200` resultCount |
|---|---|---|
| `receipt scanner` | **18** | 191 |
| `pet medication` | **20** | 188 |
| `zzqxqv glorb tapestry` | **19** | 50+ |

At `limit=20` every returned app is on-topic (`Max - Pill reminder`,
`PetDesk`, `PetMeds`… ). At `limit=200` the set grows to ~190, so the window of
the top 50 is mostly filler — games, banking, unrelated tools. **Panel 1's
`paid`, `median_paid_price` and `ratings_paid` are therefore measurements of
the padding**, and the 297,103 ratings behind its `receipt scanner` row are one
app's ratings that appeared under that window, not a measured market for receipt
archiving.

This is the F055 shape: a selection rule (how many results to ask for) silently
changed the property being measured, and the instrument reported a number
instead of saying it was measuring filler.

## 3. What panel 2 changes

| | panel 1 | panel 2 |
|---|---|---|
| fetch | `limit=200`, window = top 50 | `limit=25`, window = **whole returned set** |
| negative control | `zzqxqv glorb tapestry` | `zzqxqv glorbwump` — no dictionary word |
| relevance check | none | **G6**, per row, new |

**G6 (new, declared before the run):** at least **60%** of the apps in a
row's returned set have at least one of the term's tokens in
`trackName` + `sellerName`, case- and punctuation-folded. A row failing G6 is
`not_evaluated` — it is a row where the source did not return what was asked
for, whatever the counts say. Without G6 this scan repeats panel 1's mistake
with a smaller window.

**G1, G2, G3, G4, G5 keep their bars exactly.** G1: each positive control
yields ≥1 app priced ≥ $0.99. G2: the negative control returns `resultCount ==
0`. G3: **≥4 of 12** difficulties have **≥5 paid apps** in the returned set.
G4: **≥1** difficulty has `ratings_paid ≥ 100000` and `paid ≤ 10`. G5: two
terms fetched twice give identical `resultCount` and identical first five ids.

**G3 is now harder to pass than in panel 1**: five paid apps must appear among
~20 on-topic results rather than among 50 that included filler.

## 4. A limit on the demand proxy that panel 1 exposed

`ratings_paid` is a sum over *apps on-topic for the term's words*, and the words
attract different populations. `Fetch` (7.8M ratings) and `Ibotta` (2.0M) are
cash-back apps that match the word **receipt**; they are not competitors for
document archiving and their ratings are not demand for it. Panel 2 therefore
also reports `ratings_paid_excl_top1` and each row's top three apps by ratings,
so a reader can see **which app** the demand proxy is made of rather than a sum
that hides it. This changes no gate; it changes what a reader can check.

## 5. What panel 2 decides

Identical to panel 1: **G4 not fired kills the selection signal**, not the
difficulties, and the axis is recorded as having produced no candidate signal.

## Reproduce

```bash
tools/x -- python3 EXPERIMENTS/194-appstore-demand-scan/scan.py    # panel 1, unchanged
tools/x -- python3 EXPERIMENTS/194-appstore-demand-scan/scan2.py   # panel 2
```