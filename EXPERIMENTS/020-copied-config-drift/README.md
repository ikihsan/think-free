<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# E020 — Does agent-configuration copied into a repository go stale?

**Date:** 2026-10-05. **Verdict: `inconclusive`, and two figures retracted.**

The drift rate is not measured: **0 attributable copy/upstream pairs** exist in
the measurable population, so the declared no-drift gate fires. That is an
unanswerable question, not evidence that drift is low, and `results.json` carries
`drift_rate: null` rather than `0`.

Two things *were* established, and one of them corrects F037. Copying is widely
**instructed** — `cp -r .claude` appears in **687** Sourcegraph content matches
against a nonsense control of **0** — and barely **duplicated**: of 1950 distinct
configuration file contents across 31 repositories, **92 (4.7%)** are
byte-identical across repositories, and **no two repositories from different
authors overlap by half**. So F037's "the reader copies the directory" is an
instruction people are given; what they do is adapt it.

See [`FAILURES-findings-25.md`](../../FAILURES-findings-25.md) F040.

## Why this experiment and not another instrument measurement

E014 through E018 all measured *this repository's own instruments*: how well a
repository filter counts (F033), whether incumbents are serving (F034), whether a
prior-art verdict's coverage holds (F035), what a screen's population is made of
(F037), and whether a runtime signal can be selected per path (F038). Five
experiments in a row about the quality of the mission's own judgement, while the
mission's actual subject — software in the world — went unobserved.

This one is different in kind. It asks a question about the world that follows
from F037's most consequential observation, and the answer is *not* about us.

## The observation that opens it

F037 read the four high-star rows of the screen's young-vocabulary arm by hand
and found that none of them is a manual workaround. The reader **copies a
`.claude/` directory into their own repository once, and the hooks run themselves
thereafter.** The artifact in use is not a package.

That has a consequence nobody has drawn. Every serving channel this repository
owns — a registry install, a Homebrew tap, a release-asset download — counts a
*package*. So the near-zero reads in F037 and F059 are consistent with a field
that is heavily used and entirely invisible to measurement.

But an artifact that is copied rather than installed has no update channel. The
copy does not know the upstream exists, does not know it changed, and does not
learn about it. So the same finding predicts a specific, checkable pathology:
**copied configuration drifts silently from the upstream it was copied from.**

## The claim, stated as a test assertion

Not "agent configuration is hard to keep current" — that is a complaint. The claim
is:

> For repositories that contain an agent-configuration directory copied from an
> identifiable upstream, the copy diverges from current upstream in at least one
> behaviour-bearing field, and the repository carries no record of the version it
> was copied from.

Both halves must hold. The first is drift; the second is the part that makes
drift *unactionable* rather than merely present.

## Population rule, declared before the first fetch

1. **Entry:** repositories returned by GitHub repository search, unauthenticated,
   over the term set declared in `population.py`, capped at `N` per term in the
   order the API returns them. No hand-picking, no curation after seeing content.
2. **Containment:** a repository is in the population if
   `raw.githubusercontent.com/{repo}/HEAD/.claude/settings.json` returns **200**.
   A 404 is an absence and excludes; a non-200/non-404 is an *undecidable* and is
   counted separately and never as an absence. (F036's lesson: an HTTP 200 means
   nothing without knowing what answered it.)
3. **Attribution:** a copied directory is *attributable* when the repository's own
   README names the upstream it was copied from, by the matching rule in
   `attribution.py`. An unattributable `.claude/` is counted separately and is
   **not** scored as clean. An unattributable copy is the normal case and its
   frequency is itself a finding.
4. **Version record:** a repository *records its version* if it contains a field
   naming the upstream version — a commit-pinned copy, a version comment, a
   submodule pointer, or an `installed_plugins` entry naming a version. Absent is
   the expected case.

## Arms and controls

| arm | what it is | what must happen |
|---|---|---|
| **A1 drift** | attributable copied configs, compared field-by-field against upstream `HEAD` | the measured divergence rate, with the undecidable count beside it |
| **A2 no-drift** | repositories whose `.claude/` is **first-party** — the upstream's own repository | drift must be **near zero by construction**. A non-zero rate here means the comparator is reading noise and A1 is void |
| **A3 instrument falsification** | a deliberately stale synthetic copy of a real config | the comparator must **detect** it. A comparator that passes the stale copy cannot be trusted to fail a fresh one |
| **A4 version record** | the same attributable population | the share recording the version they copied, against the share that has drifted |

A2 and A3 are the two ways this experiment can lie to us, and they are the only
reasons A1's number means anything.

## Gates, declared before the first fetch

**Drift gate.** If at least 40% of attributable copies differ from current
upstream in at least one behaviour-bearing field, the drift claim is supported.
Drift at or below 10% refutes it: copied configuration tracks upstream closely,
which would mean the concern is unfounded and copies are cheap after all.

**No-drift gate.** If fewer than 20 rows are attributable, the question cannot be
answered and the arm reports **inconclusive** rather than "no drift". This is
stated now because an empty answer and a negative answer look identical in
`results.json` unless they are different keys (defect: `017`'s H2 thresholds were
satisfied by an empty read, and the first run printed a verdict no evidence
supported).

**Comparator gate.** A1 is void unless A3 detects the planted stale copy *and*
A2's rate is at or below 5%.

## Amendment 1, declared after the first fetch and before the second

**What was seen when this was written:** population rule 3 (attribution from the
README) yields **0 of 31**. Twenty-three repositories contain attribution
*language*, and reading each match by hand shows almost all of it is `source code`,
`source ~/.bashrc`, or "data source". The two genuine attributions
(`coleam00/claude-memory-compiler` → a Karpathy gist, `fcakyon/claude-codex-settings`
→ `livekit/agent-skills`) attribute an *idea*, not a copied `.claude/` directory.

**Why the rule was wrong, and this is the finding rather than a workaround.** A
copied config file is anonymous by construction: the thing being copied is
configuration, not source, and nobody credits a config. Rule 3 therefore could not
have worked for the phenomenon it was written to detect. Recorded as a **limitation
of the instrument**, not repaired after the fact.

**Two channels added, both declared here, before either is run:**

- **A5 structural attribution.** Two repositories are copies of a common template
  when their `.claude/settings.json` is byte-identical after whitespace and
  key-order normalisation. This attributes a copy with no credit given, which is
  how copying actually manifests.
- **A6 field validity.** A configuration that names a field the tool does not
  recognise is a configuration that does not do what it says. The check is
  against the field set observed in the population's own most-common schemas and
  against `$schema` declarations, and an unrecognised field is reported as
  `unverified` unless the repo's own `$schema` contradicts it.

**The gate is unchanged in form and threshold.** Fewer than 20 attributable rows
still means **inconclusive**. Adding a second way to *find* a copy raises
coverage; it does not lower the bar. If A5 also comes back near zero, the correct
reading is that configuration is *recreated* from documentation rather than copied
— a different fact with a different implication, and the drift question is then
about reconstruction accuracy rather than copy staleness.

## Amendment 2, declared after A5 and before the control runs

**What was seen:** A5 over authoritative trees (`git clone --depth 1`, which
replaced a marker-file probe that `validate_probe.py` falsified against the
contents API on 8 of 8 repos) finds **92 of 1950 distinct file contents shared by
two or more repositories — 4.7%** — and the only repositories whose `.claude/` is
≥50% one other repository are **one author's own two repositories**.

**The doubt this raises, stated before answering it.** Population rule 1 selected
repositories by searching for *claude-config terms*. That selects repositories
that **advertise** their agent configuration: showcases, guides, tools. A
repository that quietly copied a `.claude/` directory into itself never mentions
claude in its description and would not be returned. So A5's near-zero may be a
fact about configuration, or it may be a fact about my sampling rule — and the
two have opposite implications for F037's copy-not-install reading.

**Control declared now, before it is run (`control.py`).** Repositories drawn by
the same mechanism — GitHub repository search, capped, read in the API's order —
from a term set with **no agent terms in it**. If the control's `.claude/`
containment rate is materially above zero, the population rule was selecting the
publishers and a large invisible population exists, so A5's near-zero is an
artefact of sampling. If it is near zero, adoption is concentrated in
self-advertising repositories and A5's near-zero is a fact about the ecosystem's
top layer. **Either answer is informative and both are reportable; neither is
post-hoc.**

**Kill gate for the copy claim.** The claim "a `.claude/` directory is copied
wholesale between repositories" is supported only if a wholesale bundle (≥50% of
one repository's `.claude/` byte-identical to a *different author's* repository)
exists. The single pair found is one author's two repositories, which is
authorship, not copying, and is excluded by that wording. If no cross-author
bundle exists, the claim is **refuted for the population measurable here** — which
is a statement about this population and not about every repository on GitHub.

## What would make this a candidate, and what would not

A drift rate of 60% with a 0% version-record rate is **not** a candidate. It is
one observation about one ecosystem's current practice, and the obvious repair —
a version marker — is a feature request, not a project. What would license further
work is narrower: drift that is **expensive rather than merely present**, i.e. a
field whose divergence changes what the agent *does* rather than what it prints.
The experiment reports both counts separately so the distinction is available
before anyone writes the argument.

## Raw results

`raw/` — one file per fetch, `results.json` — the tallies with `undecidable`
carried beside every rate.

## What the arms returned

| arm | result |
|---|---|
| **A1 drift** | **`inconclusive`** — 0 attributable pairs. `drift_rate: null`, never `0` |
| **A2 no-drift** | 0/31 self-reported drift — the comparator is sound |
| **A3 falsification** | the planted stale copy **is** detected |
| **A4 version record** | **retracted** — 17/31 matched, and every match pins a *CLI* version, not a copied config |
| **A5 structural** | 92 of 1950 distinct contents (4.7%) shared by 2+ repos; widest 3; **0 cross-author bundles** |
| **A6 field validity** | **not run** — needs the tool's schema, which is not published where this could read it |
| marker probe | **falsified** — 8 of 8 disagreements against the contents API; replaced by shallow clone |

## Population-scale context, and one figure that must not be misread

Sourcegraph's unauthenticated index reports **4,540** repositories carrying a
`.claude/settings.json` path. A 150-repository control drawn from non-agent search
terms found **1** `.claude/` directory — and **that rate is not a prevalence**,
because repository search returns repositories ranked by relevance and popularity.
It bounds the top of each topic and nothing else; the 4540 supersedes it. The
confound is recorded in `results.json` and asserted by a test.

## Reproduction

```bash
python3 EXPERIMENTS/020-copied-config-drift/population.py   # 175 repos, 3-state
python3 EXPERIMENTS/020-copied-config-drift/bodies.py       # per-path captures
python3 EXPERIMENTS/020-copied-config-drift/surface.py      # marker probe (falsified)
python3 EXPERIMENTS/020-copied-config-drift/validate_probe.py  # its falsification
python3 EXPERIMENTS/020-copied-config-drift/trees.py        # authoritative clones
python3 EXPERIMENTS/020-copied-config-drift/a5_structural.py
python3 EXPERIMENTS/020-copied-config-drift/control.py
python3 EXPERIMENTS/020-copied-config-drift/analyse.py      # A1-A4 tallies
```

`trees.py` clones into `/tmp/opencode/e020-clones`; the committed evidence is
`raw/trees.json`, so a re-run does not need the clones.

The `probe--*` files that `surface.py` once wrote are **deleted, not kept**: they
were captured by the probe `validate_probe.py` falsified, and every path they
cover is already hashed in `raw/trees.json`. `raw/captured_bodies.json` holds the
README and `settings.json` bodies verbatim as JSON, because raw captures are data
rather than documents this repository maintains — storing them as `.md` made
`doc lint` check a third party's links as if they were ours.