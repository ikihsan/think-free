<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E090 — Maven Central view-count measurement prototype

**Date:** 2026-10-11 · **Status:** active — fresh observation in a new domain per D083.

## The practical difficulty

The view-count principle has been validated on package repositories (PyPI, NPM) and non-software Q&A forums (Stack Exchange, Discourse). It measures independent arrivals at need by checking whether each row carries a positive `view_count` or equivalent arrival field. The mission's domain coverage summary confirms the principle does **not** generalize to software platforms without such metadata (GitHub issues API, web search). The next experiment per D083 must test a genuinely new domain not previously covered.

Maven Central (Java/JAR packages) is the most significant platform category not yet tested. If the principle generalizes, it would confirm platform invariance across major package repositories. If it fails, it would further delimit the principle's scope and explain why.

Who experiences this: open-source tool builders, maintainers, and anyone trying to understand whether package repository metadata can serve as a reliable arrival instrument. The available evidence includes the confirmed generalization on PyPI (E071) and NPM, and the negative results on GitHub issues and web search. The important uncertainty is whether Maven Central's metadata structure supports the same measurement.

## Stated candidate decision this changes

- **If the view-count principle passes all predeclared gates on Maven Central**, the mission has confirmed platform invariance across major package repositories. This would be a durable gain for future need discovery work, even if no candidate emerges.
- **If the principle fails gates or shows domain-specific boundaries**, this too is a decision: the mission has now mapped the principle's limits across package repositories, Q&A forums, and issue-tracking platforms, and can rule out Maven Central as a route for view-count–based need measurement.

Either result is a decision, and neither result is a candidate. This experiment is not expected to produce a product, and the README must not imply that it did.

## Arms and corpus

| arm | source | what it carries |
|---|---|---|
| **A (need-related)** | Packages whose `artifactId` or `name` suggests a concrete need (e.g., `pdf-parser`, `xml-beanutils`, `compress-utils`, `date-utils`, `math-util`, `text‑filter`) | Test class: packages that appear to address a specific programming need |
| **B (random/control)** | Randomly sampled packages from the same search results, excluding arm A items | Control class: packages with generic or nondescript names |

### Corpus construction

1. **Search query**: Use the Maven Central search API (`search.maven.org`) with a broad query term (e.g., `httpclient`) to retrieve a candidate set of packages.
2. **Sampling**: From the search results, select the top 50 unique `groupId:artifactId` pairs. Skip duplicates and scopes (e.g., test-).
3. **Classification**: 
   - **Need-related**: The `artifactId` or any token in the package name maps to a concrete programming need (parsing, compression, date manipulation, text filtering, math, etc.). Heuristic: `artifactId` contains a suffix or prefix that names a utility category (utils, parser, handler, generator, loader, saver, parser, serializer, validator, formatter).
   - **Random**: The `artifactId` is a generic name not mapping to a named utility category (e.g., `core`, `common`, `base`, `api`, `framework`, `simple`, `platform`).
4. **Fallback**: If the search API is unavailable, use a pre‑selected list of 50 `groupId:artifactId:version` tuples compiled from prior runs, with the same classification rules.

### Measurement per package

For each of the 50 sampled packages:

1. Fetch the POM from `https://repo1.maven.org/maven2/<groupId>/<artifactId>/<latest-version>/<artifactId>-<latest-version>.pom`
2. Parse the POM XML and extract:
   - `<name>` — full package name
   - `<version>` — the latest released version (exclude `-SNAPSHOT`)
   - `<downloads>` element if present (Maven Central began tracking per‑artifact download counts)
   - Number of distinct `<version>` releases visible in the POM hierarchy (parent, grandmother, etc.) as a proxy for maintenance activity
   - Presence of `<developers>` or `<contributors>` sections
3. Classify the package as **active** or **inactive**:
   - **Active** = (downloads count > 0 **or** ≥ 2 distinct historical versions visible in the POM hierarchy **or** `<developers>` section present)
   - **Inactive** = none of the above

### Classification rubric (declared before reading)

A package is **need-related** when its `artifactId` or `name` conveys a concrete programming need category:
- **Parsing**: `parser`, `parser`, `parse`, `read`, `writer`, `io`
- **Compression**: `compress`, `decompress`, `zip`, `gzip`, `unzip`
- **Date/Time**: `date`, `time`, `calendar`, `format`, `period`
- **Text/String**: `text`, `string`, `filter`, `transform`, `codec`
- **Math/Numeric**: `math`, `numeric`, `calc`, `stat`, `random`
- **File/IO**: `file`, `io`, `stream`, `resource`
- **Collection/Util**: `util`, `collection`, `core` (only if paired with a descriptive qualifier)

All other packages are **random**.

### Gates (predeclared before any result is read)

- **G1 (sufficient classified items):** ≥ 15 of 50 packages are classified (need-related + random). If not met, the corpus is under‑weighted and the experiment stops; record the ceiling.
- **G2 (reader accuracy / control validity):** If human reader is used, separate 4 seeded control items at ≥ 0.85 accuracy. For fully automated run, this gate is waived with a note.
- **G3 (activity difference):** Run a two‑sample proportion test: `p_need` = active rate for need‑related, `p_random` = active rate for random. **Pass** if Wilson CI95 lower bound for `p_need - p_random` > 0.10 (10‑percentage‑point margin, matching E071's practical significance threshold). **Fail** otherwise.
- **G4 (view_count principle validation):** ≥ 95% of sampled packages carry a positive arrivals field (downloads > 0 in POM, or ≥ 2 visible versions). If not met, the view‑count instrument does not generalize to this platform. Record the gap.

### G4 failure consequence

If G4 fails (fewer than 95% of packages have positive arrivals), the corrected statement is: *the view‑count instrument is Maven‑Central‑shaped, and every reading of it in this record is a missing observation, not a measured zero*. The four unlanded experiments that depend on this ground_truth_context inherit the correction.

### Reproduction

```bash
cd EXPERIMENTS/090-maven-view-count
python3 probe.py     # writes raw/probe.json, prints the gate table
python3 outcome.py   # re-derives results.json from raw/probe.json
```

## Strongest objection, stated before running

*"Absence of a search hit is not originality" (AGENTS.md).* The experiment does not claim Maven Central has no metadata; it claims that the **documented POM response objects** carry no arrival/view field on the observed sample, or that the activity-rate difference between need‑related and random packages is ≤ 10 pp. The claim is scoped to the public documented POM response objects, because that is the only surface any reproduction can use. A per‑package web UI download counter may exist on the Maven Central website or an undocumented endpoint, but the experiment scopes to the POM XML.

**Answer:** the claim is scoped to the **public documented POM XML response objects**, because that is the only surface the harness can fetch and parse reproducibly. The experiment does not claim Maven Central has no download information anywhere; it claims the corpora carry no arrival field in the POM, so any activity‑rate measurement must be read from the POM, not from the web UI.