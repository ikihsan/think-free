# E2 lockfile closure drift — snapshot side A

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

Side A of the comparison `RESEARCH/E.md` mechanism E2 calls for: the sorted
closure of (name, version, artifact hash) for a small fixed package set,
resolved against PyPI on 2026-10-03 (T-0019).

- Requested: `requests`, `six`, `packaging`, `pyparsing`; the resolver pulled
  `idna`, `urllib3`, `certifi`, `charset-normalizer` with them — 8 artifacts.
- Record: [`snapshot-a.json`](snapshot-a.json) (schema
  `origin.lockfile-snapshot/1`), each artifact with file, name, version,
  sha256, and byte size, plus tool versions and the UTC date.
- Method: `pip3 download -d <tmp> requests six packaging pyparsing`
  (pip 20.0.2, Python 3.8.10, `https://pypi.org/simple`); hashes computed
  over the downloaded files. Nothing installed.

**No verdict.** E2 is time-gated: the informative comparison diffs this file
against a side B taken days-to-weeks later. Fast drift would show as a
version or hash change in the closure; slow drift (yanks over weeks) is the
interesting regime and needs patience, not a bigger snapshot. Do not conclude
anything from side A alone.
