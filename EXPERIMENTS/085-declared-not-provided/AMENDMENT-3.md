<!-- origin-meta
owner: EXPERIMENTS/085-declared-not-provided/PROTOCOL.md
status: active
last-verified: 2026-10-10
-->

# E085 — Amendment 3 (declared before arm A was scanned)

## The problem this closes

The protocol's ceilings section ended with: *"`wrong-distribution` requires
finding a real provider, and PyPI has no reverse module index. The candidate
provider set is therefore the name-canonicalised module name plus its PEP 503
normalised variants."*

That set recovers nothing. PEP 503 normalisation of `sklearn` is `sklearn`,
`cv2` is `cv2`, `yaml` is `yaml` — the module name normalises to itself, so
every silent wrong-project row would fall through to `unprovided`, and G3's
target class would be empty by construction. **That is the E069 failure mode
(D088): a gate whose passing region cannot be reached.** Declared here rather
than discovered on the results.

## The route, and why it is the right population

The reverse index used is **the set of distributions declared across the arm A
corpus itself** — every distribution named in any of the 24 repositories'
requirement files or `setup.py`.

This is not a workaround, it is the question the population actually poses:

> You declared `sklearn` and imported `sklearn`. **Is the distribution that
> provides `sklearn` already in your project's dependency universe?**

That is the decision a developer faces. A provider nobody in the project
declares is not a dependency this project can adopt by renaming one line, and
counting it would inflate the class with rows no tool can act on.

The index is built from the corpus's own declared files **before** any
classification, and every distribution in it is resolved by the same
instrument, with the same missing-observation rule.

## What this changes, stated in advance

- The `wrong-distribution` class becomes reachable. Rows where the provider is
  in the corpus index are decidable; rows where it is not are reported as
  `unprovided` with the reason `no-candidate-provider-in-corpus`, and are
  **counted separately, never silently folded into either class**.
- The rate `S` is reported **three ways**, so a reader can apply their own
  denominator:
  1. `S_strict` — `wrong-distribution` / computable pairs. The declared G3
     gate is judged on this. It is the **lower bound**: it can only be
     understated, never overstated.
  2. `S_upper` — (`wrong-distribution` + `unprovided`) / computable pairs.
     Every `resolves-wrong-project` row is in one or the other, so this is the
     **upper bound** on the silent class.
  3. `S_all_declared` — `wrong-distribution` / **all declared distributions**
     resolved. The most conservative reading: a wrong declaration per project
     rather than per declaration.
- G3 is judged on `S_strict`. Because `S_strict` is a lower bound, a KILL on
  `S_strict` closes the line only if it is also below the threshold; a KILL
  that rests on the gap between `S_strict` and `S_upper` is reported as a
  measurement limit, not as a closed direction.

## One correction to a declared prediction

Amendment 2 predicted `skimage` would land in `no-such-project`. It landed in
`sdist-only-undecidable`: PyPI has a `scikit-image` project with no wheel.
The observed status is authoritative; the prediction in Amendment 2 was wrong
and the table there should be read with this correction. No gate depended on
it — both classes are classified, not scored against each other.

## Ceiling this adds

The corpus index is drawn from 24 deep-learning repositories. For an ordinary
web project the index would be differently shaped, and a provider outside it
would be missed. The two-sided reporting above is what keeps that from
becoming a silent understatement.