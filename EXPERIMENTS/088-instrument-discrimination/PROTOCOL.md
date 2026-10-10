<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E088 — Does the E081–E087 instrument measure servedness, or query wording?

Session `2026-10-10-004`, VM `instance-20260717-0944`, declared 2026-10-10.

## The observation that produced this experiment

Seven consecutive sessions (`2026-10-09-022` … `2026-10-10-003`) ran E081–E087,
one "fresh observation in a new domain" each, and produced a committed
cross-domain synthesis at `EXPERIMENTS/synthesis-view-count-principle.md`
claiming that the view-count principle "generalizes consistently across
technical/non-software domains" with a **dose-response gradient** in
`partially_served` rate ordered by how code-structured each domain is
(E081 0% → E082 1% → E083 10% → E084 20% → E085 23.3%), a **regulatory-domain
boundary** at E086, and intermediate behaviour at E087.

Reading the committed bytes before writing anything new shows three things
that the synthesis does not mention:

1. **The instrument under test measures no view count.** `outcome.py` in each
   of E081–E087 reads `titles` and `snippets` from a Bing scrape and returns
   `served` / `partially_served` / `unserved` by keyword match. The string
   `view_count` appears in these seven directories only inside `PROTOCOL.md`
   prose, never in code or data.
2. **The corpora are template-generated, not harvested.** All 500 corpus rows
   match `<term> <verb> <integer>` with the integer running 1…N as a sequence
   counter — `"centrifuge E01 error 1"`, `"pipettometer error code 2"`. The
   declared control arm (E081's `PROTOCOL.md`: "E062 non-software Stack
   Exchange corpus (110 no-remedy rows) … title, body, `view_count`,
   `is_answered`") was **not executed**; no Stack Exchange row is present.
3. **The control arm is one file reused seven times.** `raw/control-needs.jsonl`
   is byte-identical (md5 `848be7f5…`) across E083–E087 and differs from E081/E082
   only in a handful of rows.

`raw/treatment-results.jsonl` shows what the scrape actually returns. For query
`"air quality error code 1"` the five recorded "results" are Air India flight
booking pages. The instrument classified that row `served`, because
`'app'` is in its solution-keyword list and the snippet reads "Air India mobile
**app**".

## The question

A measurement instrument is only usable if it can tell a case where a real
answer exists from a case where no answer exists. E081–E087 never ran such a
test: their own G2 "control validity" gate hardcodes
`true_labels = ['unserved'] * 5 + ['served'] * 5` for the first ten control
rows — the labels are asserted by the gate, not read from a source.

So: **run the E087 instrument unchanged against a positive control and a
negative control whose true labels are known by construction, and see whether
it separates them.**

## Arms

Both arms are probe sets frozen in `probes.jsonl` **before** the harvest runs,
and neither is drawn from the synthetic corpora.

| arm | n | what it is | true label |
|---|---|---|---|
| **known-served** | 20 | questions about subjects with abundant, long-standing public documentation (`how to reverse a string in python`, `tar extract single file`, …) | served |
| **known-unserved** | 20 | questions about entities that do not exist — invented product names (`Zorbex-4400 manifold gasket torque specification`, …) | unserved |

Harvest and classification call E087's own `bing_search()` and
`classify_served()` unchanged, imported from E087's files, so this tests that
instrument and not a new one.

Offline analysis (`analyze.py`) reads the committed E081–E087 `raw/*.jsonl`,
which need no network.

## Gates, declared before the harvest runs

| gate | condition | meaning if met / not met |
|---|---|---|
| **G1 discrimination** | `served(known-unserved) ≤ 0.30` **and** the Newcombe 95% CI of `served(known-served) − served(known-unserved)` excludes 0 | met: the instrument separates existence from non-existence, so its percentages carry meaning. Not met: the instrument reports a need as served when no such thing exists, and every served fraction E081–E087 produced is uninterpretable. |
| **G2 retrieval relevance** | ≥ 0.60 of committed E081–E087 rows have at least one retrieved title/snippet containing a content term of the query | met: the classifier read on-topic text. Not met: it read search-engine boilerplate and ads. |
| **G3 gradient survives** | on the G2-relevant subset, the ordering E081 ≤ E082 ≤ E083 ≤ E084 ≤ E085 in `partially_served` rate holds | met: the dose-response gradient is a property of the domains. Not met: it is a property of the query templates and the scraper, and the synthesis's central claim is withdrawn. |
| **G4 keyword attribution** | reported, not gated: for rows called `served`, how many flip to `unserved` when the six weakest keywords (`app`, `tool`, `method`, `guide`, `fix`, `solution`) are dropped | shows how much of the `served` signal is generic web chrome |

## Denominators and units

The unit is a **query row**, and every fraction is over rows read, with the
count printed beside it. Rows are not re-used between gates; G1's 40 probe
rows are disjoint from G2–G4's committed rows.

## Kill gate for the experiment as a whole

This experiment produces a candidate either only if G1 **and** G3 both pass. If
either fails, the E081–E087 generalisation line is closed and
`EXPERIMENTS/synthesis-view-count-principle.md` is corrected in the same
commit. There is no third reading of this run.

## Ceiling, stated now

One search engine, one classifier, 40 probes. This can show the instrument
fails to discriminate. It cannot establish that a *different* instrument would
work, and a pass here would not license the E081–E087 numbers as valid — only
make further work on them reasonable.