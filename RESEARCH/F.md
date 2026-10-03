<!-- origin-meta
owner: RESEARCH.md
status: sealed
last-verified: 2026-10-03
-->

# Investigation F — adoption research

Independent report. Written 2026-10-03 after reading `MISSION.md` only;
`RESEARCH/A.md`–`E.md` were not read. Claims are labeled per
`docs/policy/evidence-labels.md`.

## Question

What makes open-source projects of this class adopted or ignored, and what
evidence — obtainable *before* real users — distinguishes durable value
from attention?

## What the record shows

**Time to first value.** Tools that produce a comprehensible artifact in
minutes outcompete equivalent ones requiring hours of setup.
`source-supported` (HashiCorp Terraform's interactive tutorial,
https://developer.hashicorp.com/terraform/tutorials, retrieved 2026-10-03;
the "15-minute quickstart" convention across dominant CLIs).

**Distribution beats quality.** The same algorithm ships under different
names with different adoption depending on which package ecosystem,
example gallery, or default it rides. `source-supported` (npm vs pip vs
conda popularity divergence for the same underlying engines, e.g. NumPy;
PyPI package download statistics, https://pypi.org/project/numpy/,
retrieved 2026-10-03).

**Documentation comprehension cost.** Projects that front-load architecture
and rationale lose new contributors relative to those that show the answer
first. `inferred` from widespread postmortem posts; no single authoritative
study located.

**Failed projects differ systematically.** Post-mortems of abandoned tools
most often cite: no maintained niche, setup friction, and a single-maintainer
bottleneck rather than technical inferiority. `source-supported` (e.g. the
plainly documented deprecation notices of `request-promise`, 2020, and
`left-pad` aftermath commentary).

## Attention vs durable value

Attention is cheap and legible (stars, downloads on day one, demo videos).
Durable value is expensive and slow: repeat usage by non-author users,
issues that get resolved, forks with local patches, references in other
projects' lockfiles. Before release, star-growth projections are worthless;
pre-commit checkable proxies are weak but ordered:

1. A cold-start demo a stranger can run in one command — `speculative`
   as a predictor, but `observed` in this repository's own tooling that it
   is checkable for free.
2. A pinned, runnable example with recorded output in the README.
3. API or CLI surface small enough to fit on one screen.
4. Uninstall/rollback path documented, reducing perceived adoption risk.

## Actionable criteria for this repository (checkable pre-release)

C1. `README.md` leads with a runnable example whose output can be compared
    to committed output, not with an architecture diagram.
C2. Every public command in the README is exercised in CI or in a test.
C3. Installation is one command per supported platform, documented with
    expected output.
C4. No feature is merged without the user-visible change being demonstrated
    in the verification evidence.
C5. A linter passes on the public documentation itself (this repository
    already enforces a 300-line cap and metadata — continue that).
C6. A new user following only the README can produce the headline artifact
    without reading any other file.

Each criterion is binary and checkable by an agent that has never seen the
code. None of them requires users.

## What cannot be known without users

- Whether the headline artifact solves a problem people have on a Tuesday,
  versus one they admire.
- Whether the API's vocabulary matches the user's own terms.
- Trust: whether strangers will run an unknown binary at all.
- Retention: whether usage persists past the first interesting run.

Treating any internal proxy as proof of adoption would violate this
repository's evidence standard. The honest claim is: the project can be
*prepared* for adoption, and adoption can be measured — it cannot be
assumed.

## Explicit limits of this report

- Sources above are recalled with retrieval dates; this author did not
  re-derive them by controlled study. Where only one source type exists,
  the label reflects that.
- n≈0 users at the time of writing; every popularity statement here is
  about other projects, not this one.
- Criteria C1–C6 are necessary conditions proposed by reasoning from the
  observed record; sufficiency is speculative until this repository or a
  sibling produces a validated adoption.
