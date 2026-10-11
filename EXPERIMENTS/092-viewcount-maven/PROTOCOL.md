# E092 — View-count principle on Maven Central Java packages

<!-- origin-meta
owner: EXPERIMENTS/092-viewcount-maven
status: active
last-verified: 2026-10-11
-->

## Question

Can the view-count principle generalize to a third package repository ecosystem (Java/Maven Central), beyond PyPI and NPM? Specifically: are "need-related" Java packages systematically more "active" (have significant metadata indicating adoption/usage) than random packages?

## Population

**Denominator**: A sample of Java packages from Maven Central, selected via unauthenticated Solr search.

**Numerator**: Packages classified as "need-related" — those whose description or keywords indicate a specific problem/domain where a library would be sought.

## Instrument

### Data Fetch

Query Maven Central Solr API for a random sample of packages:

```
https://search.maven.org/solrsearch/select?q=&rows=100&wt=json
```

Fetch at minimum 100 packages (G2 gate). Each package record includes:
- `g` (group/coordinates)
- `a` (artifact/name)
- `v` (latest version)
- `p` (path)
- `desc` (description)
- `keywords` (keywords list)

### Classification Rule

A package is `need-related` iff its description or keywords contain at least one term from a predefined set of problem-domain indicators, AND the package does not trivially self-describe (e.g., "utils", "common", "api").

Predefined term sets (to be defined before fetch):

**Problem-domain indicators** (examples):
- `api`, `client`, `server`, `framework`, `engine`, `core`, `utility`, `helper`
- Domain-specific: `web`, `rest`, `mvc`, `orm`, `sql`, `json`, `xml`, `http`
- Functional: `parser`, `lexer`, `encoder`, `decoder`, `converter`, `transform`
- Application type: `gui`, `cli`, `webapp`, `framework`, `library`, `tool`

**Excluded terms** (too generic, always classified as `random`):
- `utils`, `common`, `api` (when alone), `core`, `library`, `framework` (when alone), `jar`, `dependencies`

A package is `random` if it does not meet the `need-related` criteria.

### Metric

**Active rate**: proportion of packages that have:
- A non-null, non-empty description
- Version metadata present (v field is not null/latest version exists)
- Keywords list with at least 1 entry

G4 (sample-size): at least 50 packages classified for the rate to be meaningful.

## Kill Gates

**G1**: If the active rate of `need-related` packages is under **55%** of the active rate of `random` packages, **close the line**. Need-related packages are not systematically more active, and the view-count principle does not generalize to Maven Central.

**G2**: Must sample at least **100** packages total for the rate to be meaningful.

**G3**: Each of at least **2** distinct Solr query batches must contribute classified packages to avoid batch bias.

**G4**: At least **50** packages must be classified total.

## Reproduction

```bash
cd EXPERIMENTS/092-viewcount-maven
python3 run.py --gate
```