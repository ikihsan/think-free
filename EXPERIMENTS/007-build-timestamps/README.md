<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-03
-->

# 007-build-timestamps

E3's build-timestamp census: `RESEARCH/E.md`'s smallest falsifying experiment
for the claim that embedded build timestamps are the dominant, cheap-to-count
determinism violation in Python packaging. Task T-0013. Real artifacts, real
network, no synthetic data.

## Claim under test

Many PyPI wheels embed wall-clock times in their zip entry headers. If the
fraction of recent wheels carrying a non-normalised timestamp is at or above 5%,
E3 is worth broadening; below 5%, E3 is a weak lead and the experiment ends.

The claim E3 actually wants to support is stronger: that timestamps are worth
fixing *first*. This experiment measures the first half and cannot settle the
second. See "What this does not establish".

## Kill gate (predeclared in `RESEARCH/E.md` before any run)

- **Gate metric:** the fraction of sampled wheels with any zip entry date other
  than 1980-01-01. Threshold 5%.
- **Below 5%:** E3 ends as a weak lead.
- **At or above 5%:** the lead survives and E3 is worth broadening.

The verdict is taken on this metric because it is the one E.md names. Two
stricter fractions are reported beside it and neither can overrule it: both are
lower bounds on the gate metric by construction.

## Method

- **Sample:** 200 wheels, one per release, from ten packages. Selection is in
  `sampling.py`, kept apart from measurement because a selection rule that
  silently changes the population would invalidate the whole result while an
  inspection bug would affect one artifact.
- **Selection rule:** the 20 most recently uploaded wheel releases per package
  by the release's own upload time, smallest wheel per release when a release
  ships several, distinct release versions enforced. `six` has only 19 wheel
  releases in its whole history, so the shortfall of one goes to `requests`
  (21), which keeps the sample at 200 releases drawn from the same ten packages
  rather than adding an eleventh.
- **Honest weakness:** the ten packages are a declared list, not a popularity
  ranking. PyPI download counts are not served by the public JSON API from this
  machine, so "popular" here is asserted, not measured.
- **Measurement:** every value comes from the artifact. For each wheel the zip
  is opened and every `ZipInfo.date_time` is read; `METADATA` and `RECORD` are
  scanned for ten-digit integers in the unix-epoch range. Nothing is inferred
  from the index's metadata.
- **Failure handling:** one pass, no retries. A download or parse failure is
  recorded in `results.json` and counted in the denominator report. This run had
  zero failures over 205,305,241 bytes.

## Results (`results.json`, 2026-10-03)

| Quantity | Value | 95% CI (normal approx.) |
|---|---|---|
| Releases inspected | 200 wheels / 200 releases / 10 packages | — |
| **Non-1980 fraction (gate metric)** | **0.965** | 0.940–0.990 |
| Mixed-date fraction (>=2 distinct entry dates) | 0.670 | 0.605–0.735 |
| Spread >= 1 hour ("carried mtime") | 0.145 | 0.096–0.194 |
| Spread >= 1 minute | 0.535 | — |
| Wheels with epoch-like integers in METADATA/RECORD | 0 of 200 | — |

Entry-date spread, all 200 wheels: 66 wheels have a single date across every
entry, 27 span under a minute, 78 span minutes to an hour, 4 span hours, 25 span
a day or more. The widest is `requests-2.26.0-py2.py3-none-any.whl`: 23 entries
spanning 789 days, with one entry dated 2019-05-16 in a wheel uploaded in 2021.

**Gate verdict: `lead-survives`.** The gate metric is 19x the threshold, which is
itself the finding rather than a reassurance: a metric that almost nothing can
fail is not a measurement of the mechanism. Recorded as `FAILURES.md` F010.

### Where the signal is, per package

| package | releases | mixed | single date | all 1980 | spread >= 1 min | spread >= 1 h |
|---|---|---|---|---|---|---|
| `boto3` | 20 | 20 | 0 | 0 | 20 | 0 |
| `click` | 20 | 4 | 16 | 0 | 4 | 4 |
| `cryptography` | 20 | 0 | 13 | 7 | 0 | 0 |
| `jinja2` | 20 | 16 | 4 | 0 | 16 | 16 |
| `numpy` | 20 | 20 | 0 | 0 | 20 | 0 |
| `pyyaml` | 20 | 20 | 0 | 0 | 19 | 0 |
| `requests` | 21 | 15 | 6 | 0 | 15 | 7 |
| `setuptools` | 20 | 20 | 0 | 0 | 2 | 2 |
| `six` | 19 | 19 | 0 | 0 | 11 | 0 |
| `urllib3` | 20 | 0 | 20 | 0 | 0 | 0 |

The heterogeneity is the real finding, and it cuts against a single ecosystem
rate. Only `cryptography` ships 1980-normalised wheels (7 of 20, all `win_amd64`
platform wheels; the 13 `abi3`/pure wheels are not), and it is also the only
package with zero spread. `urllib3` stamps every entry of a wheel with one
instant — the wall clock at build time — which is a *different* violation from
`jinja2`'s, whose entries carry the modification times of the checkout.

## What this does not establish

1. **The gate metric is weak, and passing it is close to trivial.** 1980-01-01
   is what you get only when the zip DOS epoch is pinned to that date. A builder
   that honours `SOURCE_DATE_EPOCH` with a real commit time still produces
   non-1980 dates, so 0.965 mostly says "nobody pins the DOS epoch", not "96.5%
   of wheels are irreproducible because of timestamps". The load-bearing numbers
   are the stricter ones: 0.535 of wheels carry entries spanning at least a
   minute and 0.145 span at least an hour, and those cannot be a single build's
   wall clock.
2. **Prevalence is not attribution.** Nothing here says timestamps are the
   *first-order* cause of a byte-level reproducibility failure, because nothing
   here rebuilds anything. Reproducible-builds tooling (`diffoscope`, `reprotest`)
   already attributes diffs per cause; this census does not.
3. **The embedded-string half of the assumption failed.** Zero wheels carried a
   unix-epoch integer in `METADATA` or `RECORD`. On PyPI wheels the timestamps
   live only in the zip headers.
4. **Population.** Ten hand-picked packages, mostly pure-Python or
   source-heavy, sampled from release history rather than downloads. It bounds
   nothing about npm, conda, Maven, or about how a user-weighted sample would
   look.
5. **Zip dates have 2-second resolution.** The 27 wheels spanning under a minute
   include spreads a real build could produce, so 0.535 is read as a floor and
   the under-a-minute bucket is not claimed as evidence either way.

## Threats to validity checked

- The same run repeated with an earlier version of the selection code (which
  picked the first-listed wheel per release and allowed a duplicate release
  through the top-up path) returned 0.975 / 0.69 / 0.245 against 0.965 / 0.67 /
  0.145. The verdict is not an artefact of the selection rule.
- Both stricter metrics are computed from the same per-wheel rows in
  `results.json`, so the gate metric cannot be inflated by counting a wheel
  twice.

## Reproduce

```bash
cd EXPERIMENTS/007-build-timestamps && python3 census.py
```

Standard library only, Python 3.8.10 on Linux, ~205 MB downloaded, about two
minutes. The run rewrites `results.json`; the sample is re-derived from the PyPI
index each time, so a later run sees newer releases and different numbers.

## Defects found while reviewing the interrupted run

The session that wrote this experiment was interrupted after two runs. Review
found three claims in its code that the code did not implement, all fixed here
before the committed `results.json` was produced:

1. `census.py` rebound `failures` after `build_sample()` reported missing
   packages, silently discarding them. Harmless in this run (zero failures), but
   it would have hidden a hole in the sample. The first repair appended a second
   row per absent package, which counted one hole as two failed wheels; a package
   that yields no wheels is now reported as its own `sample.packages_absent`
   list, distinct from the wheels that failed to download or parse.
2. `sampling.py` documented "the smallest wheel per release" but took whichever
   wheel the JSON index listed first, making the sample a function of key order.
3. The top-up path that fills a shortfall compared wheel URLs but not release
   versions, so a release already sampled could contribute a second platform
   variant. Fixed; the sample is now 200 distinct releases.

`census.py` also names the gate metric explicitly, so the verdict is taken on
the metric E.md states rather than on a stricter one the code happened to
compute first.

## Follow-up this names

E3's own falsifying experiment has a second half that this run did not perform:
build the same source twice under different `SOURCE_DATE_EPOCH` values and
attribute the byte difference. `RESEARCH/E.md` states that measurement in the
mechanism section and E.md's stated strongest objection is aimed at it — that the
counting exercise reports a solved problem. Prevalence without attribution is not
a decision input, so this half is what would move E3 off `untested` and it is
runnable on this machine (`setuptools` 45.2.0 and `wheel` 0.34.2 are present).
Recorded as **T-0017**,
`EXPERIMENTS/008-build-timestamp-attribution/`.
