<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# E020 — Does agent-configuration copied into a repository go stale?

**Date:** 2026-10-05. **Status: designed, no figure read yet.**

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