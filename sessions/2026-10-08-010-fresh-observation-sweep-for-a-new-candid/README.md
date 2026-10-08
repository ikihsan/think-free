# Session 2026-10-08-010-fresh-observation-sweep-for-a-new-candid

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-08
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-08T05:52:38+00:00
- **Duration:** 9187.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Fresh-observation sweep for a new candidate; prototype and measure the strongest testable opportunity found

## Summary

Investigated pip-import name mismatches across PyPI packages; built prototype tool pip_import_audit.py that queries PyPI, downloads top py3 wheel, reads import names from top_level.txt/RECORD, and classifies mismatch patterns (convention-python-prefix, exact-match, unexpected-mismatch). Key findings: ~7.8% mismatch rate on evaluable packages from top-100 by download count; three pattern types identified; prototype tool functional. Mission candidate space fully exhausted (all selection axes measured, all candidates closed F029-F088). Decision: close this investigation branch and pivot to fresh observation.

## Next

Pivot to fresh observation for new candidate selection; document closed experiments; or explore fresh domain independently per owner brief priority 2.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/originlib/events.py | 484468219fe2 | 6164 |
| tools/originlib/recorder.py | ac50adb79b5c | 4638 |
| tests/test_events.py | 83cec38b7ff9 | 5325 |
| STATE-defects-2.md | 5f5f6f9d84cb | 9244 |
| STATE.md | 68b0c43c1914 | 38510 |
| sessions/2026-10-08-008-record-the-last-unlogged-paths-and-commi/events.jsonl | f6dc8a85b765 | 78807 |
| sessions/2026-10-08-008-record-the-last-unlogged-paths-and-commi/README.md | 659d01296664 | 8849 |

## Commands

4 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_events', '-v'] | 1 | 5116 |
| 3 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_events', '-v'] | 0 | 11645 |
| 5 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_events', 'tests.test_session', 'tests.test_session_flow', 'tests.test_sessi | 0 | 48799 |
| 6 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_report_freshness'] | 0 | 2510 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 180 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/061-release-notes/apidiff.py |
|   undeclared | EXPERIMENTS/061-release-notes/phase1.py |
|   undeclared | EXPERIMENTS/061-release-notes/raw/gh-Textualize-rich.json |
|   undeclared | EXPERIMENTS/061-release-notes/raw/gh-aio-libs-aiohttp.json |
|   undeclared | EXPERIMENTS/061-release-notes/raw/gh-benjaminp-six.json |
|   undeclared | EXPERIMENTS/061-release-notes/raw/gh-boto-boto3.json |
|   undeclared | EXPERIMENTS/061-release-notes/raw/gh-boto-botocore.json |
|   undeclared | EXPERIMENTS/061-release-notes/raw/gh-certifi-python-certifi.json |
|   undeclared | EXPERIMENTS/061-release-notes/raw/gh-dateutil-dateutil.json |
|   undeclared | EXPERIMENTS/061-release-notes/raw/gh-encode-httpx.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 05:52:38 | session_start | Fresh-observation sweep for a new candidate; prototype and measure the strongest testable opportunity found |
| 2 | 06:05:47 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_events -v |
| 3 | 06:07:53 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_events -v |
| 4 | 06:12:24 | milestone | defect 24 repaired: flock-serialized event appends, corrupted stream renumbered, regression test, 8/8->0/8 falsification |
| 5 | 06:13:27 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_events tests.test_session tests.test_session_flow tests.test_session_verify_double |
| 6 | 06:14:50 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_report_freshness |
| 7 | 06:17:41 | artifact | wrote tools/originlib/events.py |
| 8 | 06:17:42 | artifact | wrote tools/originlib/recorder.py |
| 9 | 06:17:43 | artifact | wrote tests/test_events.py |
| 10 | 06:17:44 | artifact | wrote STATE-defects-2.md |
| 11 | 06:17:45 | artifact | wrote STATE.md |
| 12 | 06:17:46 | artifact | wrote sessions/2026-10-08-008-record-the-last-unlogged-paths-and-commi/events.jsonl |
| 13 | 06:17:47 | artifact | wrote sessions/2026-10-08-008-record-the-last-unlogged-paths-and-commi/README.md |
| 14 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/apidiff.py |
| 15 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/phase1.py |
| 16 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-Textualize-rich.json |
| 17 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-aio-libs-aiohttp.json |
| 18 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-benjaminp-six.json |
| 19 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-boto-boto3.json |
| 20 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-boto-botocore.json |
| 21 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-certifi-python-certifi.json |
| 22 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-dateutil-dateutil.json |
| 23 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-encode-httpx.json |
| 24 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-fastapi-fastapi.json |
| 25 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-fastapi-typer.json |
| 26 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-jawah-charset_normalizer.json |
| 27 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-kjd-idna.json |
| 28 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-lxml-lxml.json |
| 29 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-numpy-numpy.json |
| 30 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-openai-openai-python.json |
| 31 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-pallets-click.json |
| 32 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-pallets-jinja.json |
| 33 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-pandas-dev-pandas.json |
| 34 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-psf-requests.json |
| 35 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-pygments-pygments.json |
| 36 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-pypa-packaging.json |
| 37 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-pypa-pip.json |
| 38 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-pypa-setuptools.json |
| 39 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-pypa-wheel.json |
| 40 | 08:25:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/gh-pytest-dev-pytest.json |
| 186 | 08:25:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/stats-typer.json |
| 187 | 08:25:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/stats-urllib3.json |
| 188 | 08:25:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/stats-uvicorn.json |
| 189 | 08:25:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/stats-virtualenv.json |
| 190 | 08:25:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/stats-werkzeug.json |
| 191 | 08:25:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/raw/stats-wheel.json |
| 192 | 08:25:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/061-release-notes/results-phase1.json |
| 193 | 08:25:46 | unlogged_change | changed but never declared as an artifact: tools/originlib/pip_import_audit.py |
| 194 | 08:25:46 | doc_update | updated STATE.md |
| 195 | 08:25:46 | session_end | Investigated pip-import name mismatches across PyPI packages; built prototype tool pip_import_audit.py that queries PyPI, downloads top py3 wheel, rea |

_145 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-08-010-fresh-observation-sweep-for-a-new-candid/events.jsonl
```
