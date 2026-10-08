<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E064 AMENDMENT-1 — G2 and G3 are prior art; the surviving question is the false accept

Declared 2026-10-08, session `2026-10-08-014`, VM `instance-20260717-0944`,
**after** arm C had been run and read (2 of 30 hand-invented control names
resolved to real packages) and **before** any mutation name was generated and
before any metadata other than those two names was fetched.

## Why the declared gates are withdrawn

The protocol's G2 asks for the base rate of model-named remedies that do not
exist, with a declared kill below 0.10. That number is published:

- **Krishna, Galinkin, Derczynski, Martin, *Importing Phantoms: Measuring LLM
  Package Hallucination Vulnerabilities*, arXiv:2501.19012, ICML 2025**
  (`source-supported`, read in full on 2026-10-08). Eleven models, three
  ecosystems, 9 900 prompts. Package Hallucination Rate 0.22 %–46.15 %, with
  means JavaScript 14.73 %, Python 23.14 %, Rust 24.74 %. Their definition
  already excludes anything registered before the model's cutoff.
- Spracklen et al., *We Have a Package for You!*, arXiv:2406.10279, is the
  5 %–20 % figure the same paper cites (`source-supported`, as cited by
  2501.19012 §2).

Re-measuring a published rate in this repository would produce a number nobody
could use and a session the record cannot spend twice. G2 is withdrawn as
**prior art**, not as failed.

G3 asks whether a deterministic checker separates invented from real names. The
same paper describes exactly that mechanism — resolve the name against the
registry, compare against a pre-training-cutoff list (§4.6) — and reports it
working. G3 is withdrawn for the same reason.

**The build decision this changes.** E064 as declared could not have opened a
candidate even if both gates had fired, because the mechanism and its result
are on the record in the literature. It is re-aimed below at the one quantity
in that paper's neighbourhood that it does not report.

## What the paper does not report, and what arm C stumbled into

2501.19012 §2 states the consequence in one sentence and supports it with two
RubyGems examples: it is useful to identify names *missing* from the catalogue
**and** "squatted packages in the registry that have reasonable sounding names" —
`rubygems.org/gems/langchain` when the real project is `langchainrb`, and the
pre-emptively registered `arangodb` gem.

Those are **n = 2, anecdotal, one ecosystem.** No rate is given anywhere in the
sources read. So the open quantity is:

> **Every existence check available — the registry, `pip index`, `npm view`,
> the installer itself, an IDE squiggle — returns one bit: exists or not. That
> bit is necessary and, if it has a material false-accept rate, insufficient.**
> The failure it lets through is silent: the install succeeds.

Arm C produced two instances of that failure on its own negative control, and
in both the checker's verdict was **correct** and the control's label was wrong:

| invented control name | verdict | what is actually there |
|---|---|---|
| `pypi/asyncpg-migrate` | exists | real, version 0.0.7, 6 releases, first upload 2019-07-19, summary is a broken Dependabot badge |
| `nuget/Nito.AsyncEx.Coordination` | exists | real and huge — 162 024 792 downloads, 5.1.2, "Asynchronous coordination primitives" |

Hand-invented names cannot be used to measure this: 2 of 30 mislabelled means
the negative control is unsound. A ground truth that does not need a labeler is
required.

## The replacement claim

**E064-A1.** Plausible software-artifact names collide with real,
different artifacts at a material rate; and that rate is measurable with
registry metadata alone — no model, no search engine, no human labeler.

Ground truth is **definitional, by construction**, so no labeller is involved
and no label can be argued with:

- **Negative class.** Take a real package an assistant would plausibly name,
  and form the mutations an assistant actually produces when it half-remembers
  a name: task suffixes (`-cli`, `-utils`, `-py`, `-rs`, `-x`), framework
  re-prefixes (`py-`, `django-`, `fastapi-`, `node-`), and head-noun synonym
  swaps (`async`, `lite`, `fast`, `simple`, `mini`). The **intended** artifact
  of every mutated name is known — it is the original. Any mutation that
  resolves is therefore a **false accept by definition**.
- **Positive class.** Real packages drawn from the registries' own listings at
  the same sort order, never cherry-picked for fame, so both classes are
  mid-tail by construction and the task is not trivially separable by downloads.

## Gates, declared before any mutation name was generated

| gate | condition | if not met |
|---|---|---|
| **G1 population** | ≥ 20 seeds resolve in ≥ 4 of 5 ecosystems, and ≥ 100 mutations are generated | route not measurable at this cost. Stop, record the ceiling |
| **G5 the false-accept rate** | over mutations, Wilson CI95, the share that **resolve** — each resolved mutation is a false accept by construction. **Kill if the point estimate is below 0.05**: existence-checking is then sufficient and there is no job | |
| **G6 discriminability** | one fixed, declared, model-free rule flags ≥ 0.90 of false accepts **and** ≥ 0.90 of true accepts | registry metadata does not discriminate; **no deterministic check is possible and nothing is built** |

**The rule, fixed now, with no peeking at the data.** Flag a resolve when *any*
of:

1. total downloads < 1 000 (about a month of a moderately used package);
2. description empty, or contains `img.shields`, `badge`, `dependabot`, or a bare URL;
3. newest release older than 3 years;
4. no repository URL on the registry record.

The precision arm of G6 is the load-bearing half. A rule that flags everything
scores recall 1.0 on false accepts and is worthless; it must also leave 0.90 of
real packages alone.

## Ceiling, stated now

One day, one reader, five ecosystems, mutations of one author's idea of
plausible mutation, one fixed rule. It measures **existence and coarse
metadata**. It does not measure whether the resolved package is *semantically*
the right one, whether a malicious impostor is present, adoption, or whether
any human would run such a check — `pip install` is free and already answers
the existence bit, so the proposed difference is **entirely** the false-accept
bit and nothing else. It opens no product on its own.
