<!-- origin-meta
owner: EXPERIMENTS/085-declared-not-provided/PROTOCOL.md
status: active
last-verified: 2026-10-10
-->

# E085 — Amendment 1 (declared 2026-10-10, after the first control run, before any repository scan)

## What was observed

The first run of the instrument over the declared arms returned **G2 positive
0 of 10** and **G2 negative 0 of 10 false flags**. Read literally, that is a
failed gate. Read carefully, the positive arm was measuring the wrong thing,
and the run also exposed one genuine defect in the instrument.

`control-results.json` before this amendment is not retained; the values above
are the run's `gates` block and are quoted here so the amendment is judged
against the run it corrects.

## The defect (instrument, real)

`top_level_modules` was returning wheel *filenames* as module names: `attr`
reported `['attr.py', 'dry_attr.py']`, `matplotlib` reported `'pylab.py'`,
`pytest` reported `'py.py'`. The `src=` prefix of `.data/purelib` was also
ignored. **Repaired** in `provides.py` before any repository was scanned; the
repair changes arm C's output and nothing else, and arm C re-runs clean
(10 of 10) after it.

## Why the positive arm was mis-posed

As declared, arm B asked the resolver to *name the provider* of a written
module name. That is the **reverse** direction, and PyPI publishes no reverse
module index, which the ceilings section already said. Asking for it scored the
instrument against a direction it was never declared to support.

What the tool actually does is the **forward** direction: given the name a
developer wrote, ask PyPI whether a real project by that name exists and
whether it provides the module. The observed statuses already show why that
matters, and they split the arm into two populations the protocol had merged:

| written name | PyPI status | what it means for the user |
|---|---|---|
| `sklearn` | **sdist-only, no wheel** | a real project occupies the name; E070 measured `pip install sklearn` exiting 1 with the project's own "use scikit-learn instead" |
| `Crypto` | resolves to wheel `crypto-1.4.1`, which provides `crypto` | **silent wrong project** — install succeeds, `import Crypto` cannot work |
| `attr` | resolves to wheel `attr-0.3.2`, which provides `attr` (a module, not the `attrs` package) | **silent wrong project** |

## The amendment

Arm B becomes three sub-tests, each with its own denominator and its own
non-vacuous failing region. The three failures are *different* failures and
the gate now distinguishes them:

| sub-test | condition | failing means |
|---|---|---|
| **B1 detection** | of the arm B rows whose written name resolves on PyPI to a project that does **not** provide that module, the detector fires on **all** | the instrument cannot recognise the silent class it was built for |
| **B2 classification** | of the arm B rows whose written name has **no** PyPI record, the detector classifies them `no-pypi-record` and **not** as a silent finding | the instrument cannot tell the loud class from the silent one, which is the distinction E064 exists |
| **B3 provider recovery** | for **all 10** rows, resolving the true provider's distribution yields a module set containing the written module | the tool's value-add over deptry does not work |

B3 is the half that earns the tool its place: deptry names the module that is
unprovided and does not name the distribution that provides it.

**Both regions remain reachable for every sub-test.** Each of the 10 rows has
a determinate correct answer in all three directions, so every sub-test can
fail. G2 is met only when B1 is 100%, B2 is 100%, and B3 is at least 8 of 10.

The population split is declared here rather than discovered later: the number
of rows landing in B1 versus B2 is itself reported, because it is the first
denominator-correct read of how often this corpus's shadow names resolve to
real projects rather than to nothing.