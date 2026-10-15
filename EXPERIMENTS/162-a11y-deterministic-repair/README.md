<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E162 — can a deterministic repairer fix real accessibility defects without making the page worse?

Method, files and how to re-run. The numbers and the verdict are in
[`RESULT.md`](RESULT.md); the gates were declared, in order, in
[`PROTOCOL.md`](PROTOCOL.md) before any page was fetched; what already exists
is in [`PRIOR-ART.md`](PRIOR-ART.md).

## The one-sentence version

axe-core 4.14.0 finds 216 real violations on 27 real pages. One repair table,
two arms, differing only in whether a rule may invent a user-facing string.
The arm that may not invent is measured against the arm that may, on the same
denominator, on the same bytes.

## Files

| File | What it is |
|---|---|
| `PROTOCOL.md` | question, population, oracle, arms, five predeclared gates, the kill gate, and the four amendments written as they were needed |
| `PRIOR-ART.md` | 18-query probe of GitHub, npm and PyPI, retrieved 2026-10-15 |
| `fetch.js` | the 29 declared URLs; keeps every body with its sha256, including the two 403 bodies the protocol excludes |
| `corpus-manifest.json` | every page: url, status, bytes, sha256, frame, which rule admitted it |
| `frames.txt` | the frame rules in the order they were declared |
| `lib/harness.js` | jsdom + axe, page scripts **not** executed, `incomplete` recorded separately |
| `lib/dom.js` | the three node readers the rules use |
| `lib/rules.js` | the single repair table |
| `lib/dispatch.js` | defect id → repair, and `permitted(policy, rule)`, which is the whole difference between arms |
| `lib/repair.js` | the driver that applies one arm to one document |
| `lib/rules-run1.js`, `lib/dispatch-run1.js`, `lib/repair-run1.js` | run 1's table and lookup, bound to the same driver, so run 1 stays replayable |
| `run-arm0.js` | control run: the page as served, round-tripped, no repair |
| `run-arms.js` | arms A and B on the same DOM, resumable from its own output file |
| `analyze.js` | the gate table, computed from the recorded run files with the declared thresholds |
| `tests/test-repair.js` | 14 tests on the protocol's declared behaviours, not on current output |
| `results-arm0.json` / `results-armA.json` / `results-armB.json` | raw per-page rows, canonical run |
| `results-run1-arm*.json`, `results-run2-arm*.json` | the superseded run 1 and the run 2 the canonical files were re-derived from |
| `results-arms.json`, `gates.json` | per-arm summaries and the gate table |

**The corpus itself is not tracked.** `corpus/*.html` is 2.7 MB of third-party
pages; `corpus-manifest.json` records every url, status, byte count and sha256,
and `fetch.js` re-fetches them. `node_modules/` likewise: `package.json` and
`package-lock.json` pin axe-core 4.14.0 and jsdom 29.1.1.

## Re-running

```bash
cd EXPERIMENTS/162-a11y-deterministic-repair
npm ci                       # axe-core 4.14.0, jsdom 29.1.1
node tests/test-repair.js    # 14/14
node run-arm0.js             # ~30 min, control
node run-arms.js             # ~15 min, both arms; resumable
node analyze.js              # writes gates.json, prints the gate table
```

`run-arms.js` rewrites its output file after every page and skips ids already
present, so an interrupted run resumes without re-running a page. **Run only
one instance at a time** — the resume check is a read of the file at startup,
so two concurrent instances will both claim the same page.

## Reading the corpus

Page ids carry their fetch index: `A0`–`A7` are frame A's first eight names,
`A23`/`A24` the two replacements declared in Amendment 1, and so on. Two
bodies are stored but never measured (`A4` manchester.gov.uk, `B9` ed.gov):
both answered **403 with a bot-challenge page**, which is the mitigator's
document, not the site.