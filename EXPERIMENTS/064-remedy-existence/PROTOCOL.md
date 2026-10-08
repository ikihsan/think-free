<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E064 — PROTOCOL

Declared 2026-10-08, session `2026-10-08-014`, VM `instance-20260717-0944`,
**before any remedy name was resolved against any registry** and before any model
was asked for this experiment's arms.

## The practical difficulty

Somebody is always about to hand you the name of a tool. An assistant names it, a
README names it, a forum answer names it, a blog post names it. The next thing you
do is `pip install` / `npm i` / `cargo add` / `go get` it, and the cost of a name
that does not exist is an afternoon; the cost of a name an attacker registered is
worse. There is no cheap, model-free, cross-ecosystem way to ask *does this exist,
where, and how do I get it* — the checks that exist are per-ecosystem search
first (`npm view`, `pip index`, `cargo search`, `repology`), and the answer an
assistant gives is not reproducible and costs a call.

## The claim under test

**E064.** On real, unprompted needs, model output names remedies at a material
rate that do not exist; and a deterministic, model-free, cross-ecosystem checker
separates non-existent names from existing ones well enough to be worth running
before an install.

## The strongest accessible alternative, named in advance

**A different free assistant, asked the same question**, with web access. It is
free, it is good, and it can read a registry page. It is beaten on only two
counts, and both are declared here rather than discovered later:

1. **Cost** — a model call per check against zero marginal cost per check.
2. **Determinism** — the same 40 names checked twice give the same 40 answers.

Those two are the entire proposed difference. **Accuracy is not part of it**, so
G4 gates on the checker not being *worse* than the assistant, and reports the
assistant's accuracy beside it rather than claiming to beat it. A checker that is
worse on accuracy, better on cost, and better on reproducibility is still a
regression against the alternative and the experiment says so.

## Arms

| arm | source | what it carries |
|---|---|---|
| **A** | the 123 model responses already recorded in [`063`](../063-own-corpus-answerability/raw/labels-pass1.tsv), column `what_a_free_assistant_supplies` | one model's real, unprompted answers to real needs; zero new model calls |
| **B** | **24 fresh needs** from three Stack Exchange sites E062 did not use (`outdoor`, `knitting`, `space`), asked of **4 models** with no tool access, blind to the other arms | independent labellers, a non-software population, and a cross-population comparison |
| **C** | **30 invented-but-plausible names** written before any registry was read, and **30 real names** read out of registries | the checker's own positive and negative control |

**Why arm A is worth a rerun rather than a rerun of the models.** It is the
mission's own recorded model output on real needs, so the base rate it yields is
already unbiased by this session's models — at the cost of one reader, which is
named as a limit and is why arm B exists.

## Gates, all declared before any name was resolved

| gate | condition | if not met |
|---|---|---|
| **G1 population** | arm B yields ≥ 20 needs with a body, and ≥ 3 answered responses each; arm C yields exactly 30 invented and 30 real names | the route is not measurable at this cost. Stop; record the ceiling |
| **G2 the base rate** | over arms A and B **separately**, with Wilson CI95, the share of named remedies that resolve in **no** registry and return nothing on the open-web check | this is the result. **A declared kill: if neither arm reaches 0.10, the problem is rare, the checker has no job, KILL** |
| **G3 checker separation** | on arm C the checker rejects ≥ 0.95 of the 30 invented and accepts ≥ 0.95 of the 30 real, using **no model and no search engine** | the checker is not better than asking. KILL |
| **G4 the alternative** | the checker's invented-name rejection rate is **not more than 0.05 below** the independent assistant's on the same 30 names | the alternative is better on the axis that matters. KILL |

**G2 is a kill gate in both directions and that is the point.** A low base rate is
the finding that most people running AI code assistants have not measured, and it
would be reported as one.

## Extraction rule, written before the rows

A response **names a remedy** when it contains a token that names an installable
or fetchable artifact: an import name, a distribution name, an executable, a
`owner/repo`, a URL, a service, or a titled work. The extractor is a
deterministic regex over the recorded text and its output is hand-checked on
every row it fires on — **an extractor with no precision control is F029's
defect**, so the extractor's own precision is reported as a number, over a
hand-marked sample, before the base rate is computed.

## Denominators and honesty rules

- Every fraction is over **names**, and every name is counted once even when it
  appears in several responses; both counts are reported.
- A name that a registry cannot answer for reasons other than absence — a rate
  limit, a 5xx, an ambiguous normalisation — is a **missing observation** (D082),
  never a zero and never a denominator.
- The labellers in arm B are free models behind one provider; they are named as
  distinct because their names are distinct and **no independence is claimed**.

## Ceiling, stated now

One day, one reader, models from one provider, needs from three Q&A sites and one
corpus, and "does this artifact exist" answered against public registries only —
which is the check a real user can run. This measures the **existence** of named
remedies. It does not measure whether an existing remedy is *good*, whether a
package with the same name is *the same thing*, or whether a non-existent name is
malicious. It does not measure adoption, and it opens no product on its own: the
build decision is the one written at the end of this file.
