# E137 — View-Count Classifier Prototype v3.1

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

## Experiment Summary

**Status**: prototype — evidence-gathering, not product validation.

**The question**: Can the view-count principle's core classifier be operationalized as a
standalone, domain-adaptable instrument that classifies text as `need-related`,
`generic`, or `unlabelled` using word-boundary-aware patterns with the
AMENDMENT-3 masking rule? This prototype is not expected to produce a candidate
or a product. It is an evidence-gathering prototype that tests whether the
classifier methodology can be separated from platform-specific API concerns.

**If successful**: It provides a reusable instrument for future fresh observations
per D083 across any domain with text data.

**If unsuccessful**: It documents the technical gap and confirms that the
classifier requires refinement before cross-domain reuse.

## The Practical Difficulty

Researchers measuring unmet needs across domains cannot reliably classify text as
need-related or generic because existing classifiers either:
- Use unanchored substring matching that fires on `ai` inside `email` and `base`
  inside `database` (E113: labels only ~28% of a representative pool)
- Lack word-boundary awareness, producing false positives from morphological
  overlaps
- Are coupled to platform-specific APIs, limiting reuse across domains

**Who experiences this**: Mission researchers conducting fresh observations
across domains per D083, and any practitioner trying to measure unmet needs from
text data.

**Available evidence**: The mission has 11+ experiments using classifiers across
package descriptions, forum titles, code repositories, and regulatory documents.
The E113/F116 matched-harvest control showed that the original design's effect
collapsed when using proper harvest design and anchored classification. The
classifier coverage problem (196/700 rows labelled, 458 matching neither
vocabulary) is the binding constraint.

**What the next action could establish**: Whether a standalone, domain-adaptable
classifier with word-boundary patterns and AMENDMENT-3 masking can reliably
classify text across domains, with known false-positive/false-negative rates, and
produce reproducible gate computations.

## Design

The prototype consists of three modules:

### 1. Classification Vocabulary (`classify_core.py`)

**Need indicators** (technology/noun phrases signaling a genuine need):
- web framework, http server, http client, api client, rest api
- database, orm, sql, postgresql, mysql, redis, mongodb
- cache, caching, queue, messaging, rabbitmq, kafka
- authentication, authorization, oauth, jwt, session, security
- logging, monitoring, observability, testing, test framework
- deployment, ci/cd, continuous integration, continuous deployment
- kubernetes, docker, container, microservices, service mesh
- graphql, grpc, websocket, real-time, pub/sub, message broker
- serialization, json, xml, yaml, protobuf, avro
- validation, schema, configuration, config, secrets management
- search, elasticsearch, fulltext, machine learning, ml, ai
- data processing, etl, streaming, data pipeline
- load balancing, rate limiting, circuit breaker, retry, timeout
- router, routing, middleware, dependency injection, cli
- command line, argument parsing, template engine, rendering
- migration, seeding, factory, active record
- data, analysis, mining, processing

**Generic terms** (common words signaling pervasiveness, not a specific need):
- utils, common, core, library, package, tool, util, helper
- base, standard, stdlib, internal, private, experimental
- template, boilerplate, scaffold, starter, example, demo
- tutorial, learning, practice, playground, sandbox, toy
- sample, proof of concept, poc, prototype, experiment

### 2. Word-Boundary Patterns

All patterns use `\b` word boundaries. Longest term first ordering.
AMENDMENT-3: need phrases are masked before generic scan, preventing
'learning' from cancelling 'machine learning' and 'ai' from not firing inside
'email'.

### 3. G0 Planted Positive Recovery

Planted need texts explicitly containing technology nouns (database, cache, auth,
orm, etc.) — must label `need` at ≥ 9/10.
Planted generic texts — must label `generic` at ≥ 9/10.

## Gates, Declared Before Any Row Is Fetched or Read

| Gate | Condition | If Not Met |
|------|-----------|------------|
| **G0** | Planted need recovered ≥ 9/10 AND planted generic recovered ≥ 9/10 | Kill gate — labeler cannot be trusted; stop, record the ceiling. |
| **G1** | ≥ 30 items per arm with classifiable text (not unlabelled) | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2** | Seeded control items classified at ≥ 0.85 accuracy against true labels | the rubric is not usable and the fraction is not measurable. Stop. |
| **G3** | the fraction of active packages (API success) in the need arm, with Wilson CI95, over ≥ 30 rows; and the same fraction over the control arm's rows | this is the result; no gate |
| **G4** | 17 of 20 top-arrival need packages classified as `need` or `generic` (i.e., labelled, not `unlabelled`) | the answerability gap generalizes; the view_count principle does not serve the top-arrival need population |

**Denominators**. Every fraction is over rows read, and rows not read are reported
as rows not read. Per D082, an arm that produced no observation is a missing
observation, never a zero and never a denominator.

**G0 kill gate (predeclared, must pass first)**: The labeler must recover
independent real positives: seeded on 20 packages with descriptions explicitly
containing a technology noun (`database`, `cache`, `auth`, `orm`, etc.) it must
label `need` at ≥ 9/10 and on 20 packages matching only generic vocabulary at
`generic` ≥ 9/10. Kill: G0 below threshold stops the experiment — a labeler
that cannot find planted positives cannot be trusted to find natural ones.

## Ceiling, Stated Now

One platform-agnostic classifier with word-boundary-aware classification using
both description and keywords, and one corpus of classifiable text. This measures
the operationalizability of the view-count classification methodology, with
gates confirming instrument validity. It does not measure demand, does not
measure adoption, and does not close any candidate.

## Reproduce

```bash
python3 EXPERIMENTS/137-viewcount-classifier-prototype/classify_core.py
python3 EXPERIMENTS/137-viewcount-classifier-prototype/harvest_demo.py
```

Needs Python 3.8+ with no external dependencies (stdlib only).

## Evidence Labels

All metrics: **observed** (directly measured from harvested/classified data)
Classifier design: **specified** (declared before measurement, not tuned post-hoc)
Gate results: **observed** (computed from committed data)
Domain adaptability claim: **speculative** — requires cross-domain validation