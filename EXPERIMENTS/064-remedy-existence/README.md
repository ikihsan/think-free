<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E064 — does a named remedy exist, and is "it exists" enough?

Session `2026-10-08-014`, VM `instance-20260717-0944`, declared
2026-10-08 in `PROTOCOL.md`, re-aimed the same day in `AMENDMENT-1.md`
(G2/G3 withdrawn as prior art — arXiv:2501.19012 already publishes the
hallucinated-name rate and the resolve-against-the-registry check).

**This experiment produced no candidate and no prototype.** It measured
the one quantity in that paper's neighbourhood the literature does not
report, and it falsified the one cheap deterministic fix this protocol
fixed in advance.

## The question

Every existence check anyone can run — the registry, `pip index`,
`npm view`, the installer itself — returns one bit: *exists* or *not*.
The prior art measures how often models name things that do **not**
exist. This experiment measures the complementary failure: how often a
plausible near-miss name **resolves to a real, different artifact**, so
the check returns *exists* and the install succeeds and is wrong.

Ground truth is definitional, so no labeller is involved and no label
can be argued with: mutate a real package name the way a model does
when it half-remembers one (suffix `-cli`/`-utils`/`-py`/`-rs`/`-js`/
`-x`/`-go`, prefix `py-`/`django-`/`fastapi-`/`node-`, synonym
`async-`/`lite-`/`fast-`/`simple-`/`mini-`), and the *intended*
artifact of every mutated name is the original. Any mutation that
resolves is a **false accept by construction**.

## Verdict

| gate | outcome |
|---|---|
| **G1 population** | **met.** 37 of 37 seeds resolve in all 5 ecosystems; 576 mutations generated (gate: ≥ 20 seeds in ≥ 4 ecosystems, ≥ 100 mutations). |
| **G5 the false-accept rate** | **fired — the problem is real and material.** 93 of 576 mutations resolve: **0.1615, Wilson CI95 [0.1337, 0.1937]**, against a kill line of 0.05. |
| **G6 discriminability** | **failed on the recall arm.** The declared rule flags 69 of 93 false accepts (**0.742**, gate ≥ 0.90) and leaves 29 of 30 real packages alone (**0.967**, gate ≥ 0.90). |

**The declared build decision stands: nothing is built.** G5 says
existence-checking is materially insufficient; G6 says the fixed
metadata rule cannot repair it, because the false accepts it misses are
healthy, popular, actively maintained projects.

## G5, the measurement

Per ecosystem (the namespaces differ in flatness and size, and the
rate tracks both):

| ecosystem | false accepts | rate | Wilson CI95 |
|---|---|---|---|
| npm | 40/144 | **0.278** | [0.211, 0.356] |
| PyPI | 32/192 | **0.167** | [0.121, 0.226] |
| crates.io | 15/96 | **0.156** | [0.097, 0.242] |
| RubyGems | 6/96 | **0.063** | [0.029, 0.130] |
| Packagist | 0/48 | **0.000** | [0.000, 0.074] |

Per mutation family: suffix 46/259 = 0.178, synonym 30/185 = 0.162,
prefix 17/132 = 0.129. All three families contribute; the rate is not
an artifact of one shape.

Packagist's zero is structural, not luck: its names are `vendor/pkg`,
so a near-miss of `monolog/monolog` resolves only if the *same vendor*
published the mutated name. Flat namespaces (npm, PyPI) collide most.

Zero mutations returned `unknown` — no missing observations sit in
G5's denominator.

## G6, and the 24 that make it fail

The rule (fixed before any mutation was generated) flags a resolve when
any of: downloads < 1 000; description empty or badge/badge-URL-shaped;
newest release older than 3 years; no repository URL. A clause whose
field the registry does not carry is dropped for that row, never read
as a low count (D082): PyPI downloads come from pypistats, which
429s a burst, and Packagist and Homebrew carry no download count at all.

The specificity arm passed — 29 of 30 real registry-listing names are
left alone; the one flag is `zero-fill`, a real npm package whose
newest release is 2020. The recall arm failed, and its residual is the
finding:

**24 of the 93 false accepts carry healthy metadata.** `jinja2-cli`
(11.2 M downloads/year), `sqlalchemy-utils`, `django-click` (1.7 M),
`django-typer` (1.6 M), the gem `async-redis` (863 K), `async-typer`
(647 K), `chalk-cli`, `typer-cli`, `rich-cli`, `tenacity-rs`,
`requests-rs`, `requests-go`, `winston-cli` … These are not junk
squats; they are real, popular, actively maintained projects that are
**a different artifact than the one intended**. On every signal the
declared rule uses, they are indistinguishable from the real class.
Some are the de-facto companion libraries of their seeds — which is
exactly why the failure is silent: the install succeeds, and the
package does something adjacent.

So the classes overlap on coarse registry metadata. The separator that
remains is semantic — *does this package do what was asked* — and that
is the named alternative's job (a model call), which takes the cost and
determinism advantage that justified a checker with it.

**A drafting slip in `AMENDMENT-1.md`'s gate table, recorded:** the
table says the rule must "flag ≥ 0.90 of true accepts" while the prose
below it says it must "leave 0.90 of real packages alone". The two
readings disagree; the prose is the operative intent (a rule that flags
both classes at 0.90 discriminates at nothing). The verdict is the same
under either reading — the rule flags 0.033 of true accepts and leaves
0.967 alone — so G6 fails on the recall arm regardless.

## What this adds

- **The false-accept rate of existence-checking, measured.** The prior
  art (arXiv:2501.19012, ICML 2025) measures the non-existent-name
  rate at 0.22 %–46.15 % per ecosystem and names the squatted-name
  failure with n = 2 RubyGems anecdotes. This is the same failure's
  complement, at 16.1 % (CI95 13.4–19.4) over 576 definitional
  ground-truth names in five ecosystems, with no labeller in the loop.
- **The cheap fix is falsified for the declared rule.** A deterministic,
  model-free, cross-ecosystem pre-install checker — the candidate E064
  originally proposed — would have *confirmed* 16 % of the wrong
  names it was asked about. Its success case is the failure case.
- **The instrument.** `registry.py` is a model-free existence check
  over 13 ecosystems (PyPI, npm, crates, RubyGems, Maven Central,
  NuGet, Packagist, Go, Hex, GitHub, GitLab, Homebrew, Launchpad),
  returning `exists` / `absent` / `unknown` with D082 handling;
  `meta.py` fetches the metadata the rule needs with the same
  discipline; `control.py` is their CLI. All three are stdlib-only
  and reusable.

## The instrument nearly failed itself

The metadata run at 12:21 returned `unknown` for **all six NuGet and
all six Homebrew** real-class rows — a transient registry failure under
the burst, since both endpoints answered normally minutes later. Per
D082 those rows were excluded, not zeroed; they were re-fetched
(`raw/refetch-real-12.tsv` → `raw/refetch-real-12.json`) and merged
into `raw/metadata-real.json`, which is what `outcome.py` reads. With
them recovered, specificity is 29/30; without them it would have been
computed over 18 rows. The failure and the recovery are both in the
tree.

## Named limits

- **One author's idea of "plausible mutation"**, three families, 37
  seeds chosen as packages an assistant would plausibly reach for. The
  real near-miss distribution of model output is a different sample;
  measuring it was the withdrawn G2, and the published rate covers the
  non-existent tail, not this one.
- **The real class is not uniformly mid-tail**, despite the amendment's
  claim: the crates and NuGet control arms were read download-sorted,
  the Packagist and Homebrew arms alphabetically, the npm arm by
  keyword search. Decomposed, the alphabetical arms pass 12/12 and the
  download-sorted arms 12/12, so the specificity result does not rest
  on fame alone — but it was measured against a mixed class.
- **Existence and coarse metadata only.** Nothing here measures whether
  a resolved package is *semantically* the right one (that is the
  residual), whether any impostor is malicious, or whether any human
  would run such a check. `pip install` is free and already answers the
  existence bit; the proposed difference was always only the false-
  accept bit, and that bit is now measured in both directions.
- **One day, one reader, five ecosystems, 2026-10-08.** Registries
  change; a re-run is one `outcome.py` away from a new number.

## Reproduce

```bash
cd EXPERIMENTS/064-remedy-existence
python3 control.py --self-test      # both instruments can say yes and no
python3 mutate.py                   # rebuilds raw/mutations.json
python3 outcome.py                  # every number above, from raw bytes
```

`outcome.py` exits 1 if any recomputed value disagrees with the
recorded one. The per-ecosystem verdicts are in `raw/verdicts-*.json`
(the original arm-C controls, 30 invented and 30 real, are in the same
files under `arm` — 2 of the 30 invented resolved, which is why hand-
invented names cannot serve as this experiment's negative control).
