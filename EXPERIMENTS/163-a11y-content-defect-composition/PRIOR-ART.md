<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E163 — prior art, probed before any build decision

**Retrieved 2026-10-15** by `/tmp/opencode/priorart163_probe.py` writing
`/tmp/opencode/priorart163.json`: 16 queries across the GitHub search API and 5
across the npm registry search API, plus a PyPI name probe on seven candidate
spellings. Raw output is the probe's; the reading is mine. Retrieval dates are
separate from publication dates, and GitHub rows below carry each repository's
own `pushed_at`. E162 probed the autofix class (18 queries,
[`162-a11y-deterministic-repair/PRIOR-ART.md`](../162-a11y-deterministic-repair/PRIOR-ART.md));
this file probes the **triage and prioritization** class, which is the class a
G3 build would compete in.

## The claim being probed

Not "does an accessibility checker exist" — it obviously does. The claim a G3
pass would build on is narrower:

> a deterministic tool that ranks real WCAG defects for a team, separating
> machine-generated plumbing (syntax-highlighter line anchors, empty anchors)
> from content-bearing defects, and derives candidate accessible names from
> authored text elsewhere in the document — answering "which defects should we
> fix first, and which of those can be fixed without inventing text".

So the prior-art question is four questions, not one.

## 1. Does axe-shaped triage/prioritization exist?

**Reporting yes; triage barely.** The populated niche is *reporting scanner
output*: `axe-html-reporter` (npm, "create HTML Report from raw accessibility
aXe result objects"), `jest-axe`, `@axe-core/playwright`, and the W3C's own
`wai-wcag-em-report-tool` (96★) and `wcag-em-report-tool` (79★). The W3C tools
are **manual-evaluation reporting** — a human fills in findings against WCAG-EM
methodology; they do not consume an axe report and rank it.

Triage-named repositories are few and tiny:

| Repository | Stars | `pushed_at` | What it is |
|---|---|---|---|
| `liip/TheA11yMachine` | 643 | 2019-12-17 | crawler + tester (audit, not triage) |
| `sumanbasuli/lime` | 28 | 2026-05-14 | audit platform, scan tracking, screenshots |
| `hmmhmmhm/ax-grep` | 13 | 2026-10-06 | CLI for static inspection, "search triage", browser handoff |
| `LaserTrajectory/easyalliance-a11y-triage` | 0 | 2026-10-11 | "confidence-routed accessibility bug triage" — prototype |
| `manjunathnp/A11yLens` | 0 | 2026-09-22 | local audit workspace, "issue triage", element evidence |
| `basira-accessibility-radar` | 2 | 2026-08-25 | local-first triage radar (Arabic/English) |

The pattern: audit platforms exist at low adoption; tools whose *named
purpose* is triage are 2026-era prototypes with single-digit stars. "axe
prioritize" returns 12 repositories, none of which is a triage tool over axe
output. Nothing found ranks real-world scan results by what is worth fixing.

## 2. Does anything filter machine-generated or false-positive-prone findings?

**Essentially nothing.** "wcag false positive" returns 3 repositories:
`Elizabeth1979/accessibility-validator` (0★, self-described "no false positives")
and `cogniumhq/a11y-benchmark` (0★, a fixture corpus for measuring scanner
recall/precision — the closest thing to E163's own instrument, as a benchmark
for scanners rather than a triage tool). No tool addresses the specific
population E162/E163 measured: defects on elements **a machine generated**
(line anchors, empty anchors) that a scanner reports as if they were author
defects. Five further queries that would bear directly on this question —
"a11y false positive filter", "axe false positive", "accessibility report
generator", "a11y defects dashboard", "axe violations dashboard" — **hit the
GitHub rate limit (403) and returned no totals**; the vocabulary is recorded
here as unprobed, not as empty.

## 3. Does anything derive accessible names from authored text elsewhere in the document?

axe-core itself computes accessible names per the spec (aria-labelledby,
associated label, figcaption, value, …) — that is name *computation* from the
DOM, and D1–D6 in E163's probe re-derive it. What no probed tool does is use
that computation **as a triage signal**: "this defect's correct value is
already written somewhere in this document by a person, so it is fixable
without invention." No hit in any query. The 2026 autofix tools E162 probed
(`a11yforge`, `curb-cut`, `ultra11y`) generate text with models instead.

## 4. Is the space crowded, and how adopted is what exists?

Crowded at the **check** layer (eslint-plugin-jsx-a11y, axe-core, Lighthouse,
WAVE, pa11y — all established), nearly empty at the **triage-of-real-scans**
layer. The largest triage-adjacent tool found is 643 stars and last pushed
2019; the triage-named tools are 0–13 stars and months old. npm totals on
broad terms ("a11y audit" 43,755; "wcag report" 61,389) are keyword matches
over unrelated packages and are not adoption evidence.

## What this does and does not establish

- **Does establish:** deterministic triage/prioritization of real WCAG scan
  output is not a populated niche. Reporting is; triage is prototypes. No
  measured tool filters machine-generated plumbing, and none uses
  name-derivation as a fixability signal.
- **Does not establish:** demand (nothing here measures whether anyone would
  install such a tool — the protocol says so and this file does not change it),
  and five rate-limited queries mean part of the triage vocabulary is unprobed.
- **Absence of a search hit is not originality** (AGENTS.md). The searches
  were run in the user's vocabulary ("triage", "prioritization", "false
  positive", "ranking", "report") and the ecosystem's (axe-core, wcag); the
  true unknown is whether a real-world triage tool exists under a name none of
  these 21 queries used.
