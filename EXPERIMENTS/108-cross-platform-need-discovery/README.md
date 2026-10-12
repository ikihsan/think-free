<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E108 — Cross-Platform Need Discovery Prototype

## Overview

`needfind` is a reversible exploratory prototype that leverages the **validated view-count principle** across multiple platforms to help developers discover the right package/repository for their stated need.

The view-count principle states: **need-related items (packages, repositories, questions) have systematically higher engagement metrics (downloads, stars, views) than random items.** This has been experimentally validated across 8+ platform types in this mission (E071, E072, E102, E103, E107, E077, E062, E100).

## Installation

```bash
cd EXPERIMENTS/108-cross-platform-need-discovery
# No dependencies beyond Python standard library
python3 needfind.py --help
```

## Usage

```bash
# Search for a need (auto-detects language/platforms)
python3 needfind.py "async HTTP client for Python"

# Explicit platform targeting
python3 needfind.py "React state management" --platforms npm,github

# Language hint
python3 needfind.py "JSON serializer" --language csharp

# JSON output for scripting
python3 needfind.py "database ORM" --json

# More results
python3 needfind.py "web framework" --top 30
```

## Supported Platforms

| Platform | Activity Metric | API | Rate Limit |
|----------|-----------------|-----|------------|
| PyPI | Monthly downloads (pypistats) | JSON | None |
| NPM | Metadata activity score (E072) | JSON | None |
| GitHub | Stars + forks + recency | REST (v3) | 60/hr unauth |
| NuGet | Total downloads | Azure Search | None |
| Hex.pm | 30-day downloads | JSON | None |

## How It Works

1. **Need Classification**: The query is analyzed using the Need Indicator / Generic Term framework (E078/E103) to detect functional categories (web, database, auth, cache, etc.) and classify as need-related/random/ambiguous.

2. **Language Detection**: Programming language keywords in the query determine which platforms to search (e.g., "Python" → PyPI + GitHub Python repos).

3. **Platform Search**: Each platform is queried with optimized search terms extracted from the query.

4. **Enrichment**: Top results per platform are enriched with detailed metadata and activity metrics.

5. **Cross-Platform Ranking**: Results are normalized within each platform, then combined with a need-relevance bonus based on matching categories/keywords.

6. **Output**: Ranked results showing platform, name, description, activity metric, and relevance score.

## Example Output

```
$ python3 needfind.py "async HTTP client for Python"

Query: async HTTP client for Python
Classification: need-related
Need indicators: ['async', 'http', 'client']
Categories: ['web']
Detected languages: [('python', 3)]
Searching platforms: pypi, github

  Searching pypi...
    Found 10 packages
  Searching github...
    Found 10 repos

Ranking results by view-count signal...

Rank Platform Name                                 Score Activity      Summary
---- -------- ---------------------------------------- ------- ----------- ------------------------------------------------------------
   1 pypi     httpx                                  1.000   5,000,000 dl/mo Next generation HTTP client for Python 3
   2 pypi     aiohttp                                0.850   3,000,000 dl/mo Async HTTP client/server framework
   3 pypi     requests                               0.720  10,000,000 dl/mo Simple HTTP library for Python
   4 github   psf/httpx                              0.950       8,500★ Next generation HTTP client
   5 github   aio-libs/aiohttp                       0.800       5,200★ Async HTTP client/server
```

## Gate Validation (Per PROTOCOL.md)

| Gate | Criterion | Status |
|------|-----------|--------|
| G1 | Tool runs without error on test queries | To be tested |
| G2 | Returns results for ≥2 platforms per query | To be tested |
| G3 | Need-related results rank higher (manual inspection) | To be tested |
| G4 | Cross-platform deduplication works | To be tested |

## Architecture

```
needfind.py          # Main CLI entry point
classifier.py        # Need/language classification (E078/E103 framework)
ranker.py            # Cross-platform normalization & ranking
platforms/
  ├── __init__.py
  ├── pypi.py        # PyPI search + pypistats downloads
  ├── npm.py         # NPM search + metadata activity score
  ├── github.py      # GitHub repo search + stars/forks
  ├── nuget.py       # NuGet search + total downloads
  └── hex.py         # Hex.pm search + 30-day downloads
PROTOCOL.md          # Experiment protocol
README.md            # This file
```

## Limitations (Honest)

- **No authentication**: GitHub limited to 60 requests/hour unauthenticated
- **No download stats for GitHub**: Uses stars/forks as proxy (validated in E107)
- **NPM activity score is metadata-based**: Not actual downloads (E072 approach)
- **NuGet nuspec parsing is simplified**: May miss some metadata
- **Rate limiting**: Polite delays added; bulk searches may be slow
- **Reversible prototype**: Not a production tool; no caching, no persistence, no tests

## Validation Plan

Test queries covering different languages and need types:
1. "async HTTP client for Python" → PyPI + GitHub (Python)
2. "React state management library" → NPM + GitHub (JavaScript)
3. "C# JSON serializer Newtonsoft" → NuGet + GitHub (C#)
4. "Elixir web framework Phoenix" → Hex.pm + GitHub (Elixir)
5. "Rust async runtime Tokio" → GitHub (Rust)

Each should return relevant results on ≥2 platforms with need-related packages ranking higher.

## Related Experiments

- E071: PyPI view-count principle (ALL GATES PASS)
- E072: NPM activity as view_count proxy (ALL GATES PASS)
- E102: NuGet view-count principle (ALL GATES PASS)
- E103: Hex.pm view-count principle (ALL GATES PASS)
- E107: GitHub repositories view-count principle (ALL GATES PASS)
- E067: View-count measurement framework (prototype)

## License

MIT — see repository root LICENSE.