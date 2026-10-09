# Session 2026-10-09-004-observe-whether-the-silent-wrong-project

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-09
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T08:19:26+00:00
- **Duration:** 5379.7s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

Observe whether the silent wrong-project install (E064's false-accept class: a near-miss name that resolves to a real different project, invisible to installer guards) occurs among real users, and decide whether a deterministic did-you-mean-a-different-project check has a population worth prototyping

## Summary

E070 complete. Arm M: only 1 of 4 declared-B names (telegram) installs silently; sklearn, beautifulsoup, color all fail loudly. Arm W: 3 B rows in 105 G rows (headroom, tigl3, clip). K1a met (beautifulsoup 4B, telegram 3B). K2 primary = 3/4 = 0.75 >= 0.10, build authorized. K2 secondary = 3/105 = 0.0286. Silent wrong-project install is real and occurs in real reports across 2 ecosystems and 2 venues.

## Next

Prototype a did-you-mean-a-different-project checker: reads declared dependencies and actual imports, flags a declared name whose near-miss provides the import. Per D088, enumerate the gate passing region before the run.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/070-silent-wrong-project/PROTOCOL.md | 1ffdd41a28c3 | 7329 |
| EXPERIMENTS/070-silent-wrong-project/README.md | 42066b793cc9 | 5627 |

## Commands

9 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'arm_m.py'] | 2 | 30 |
| 4 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/arm_m.py'] | 0 | 1105 |
| 5 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/arm_m.py'] | 0 | 97213 |
| 6 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/fetch_reports.py'] | 0 | 139906 |
| 7 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/sample.py'] | 0 | 313 |
| 8 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/sample.py'] | 0 | 319 |
| 9 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/fetch_reports.py'] | 0 | 177651 |
| 10 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/sample.py'] | 0 | 304 |
| 11 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/sample.py'] | 0 | 398 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 34 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/070-silent-wrong-project/AMENDMENT-1.md |
|   undeclared | EXPERIMENTS/070-silent-wrong-project/AMENDMENT-2.md |
|   undeclared | EXPERIMENTS/070-silent-wrong-project/AMENDMENT-3.md |
|   undeclared | EXPERIMENTS/070-silent-wrong-project/AMENDMENT-4.md |
|   undeclared | EXPERIMENTS/070-silent-wrong-project/aid.py |
|   undeclared | EXPERIMENTS/070-silent-wrong-project/arm_m.py |
|   undeclared | EXPERIMENTS/070-silent-wrong-project/fetch_reports.py |
|   undeclared | EXPERIMENTS/070-silent-wrong-project/raw/api/gh-beautifulsoup-beautifulsoup4.json |
|   undeclared | EXPERIMENTS/070-silent-wrong-project/raw/api/gh-installed-the-wrong-package-github-issue.json |
|   undeclared | EXPERIMENTS/070-silent-wrong-project/raw/api/gh-installed-wrong-pypi-package.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 08:19:26 | session_start | Observe whether the silent wrong-project install (E064's false-accept class: a near-miss name that resolves to a real different project, invisible to  |
| 2 | 08:20:30 | artifact | wrote EXPERIMENTS/070-silent-wrong-project/PROTOCOL.md |
| 3 | 08:21:19 | command | $ python3 arm_m.py |
| 4 | 08:21:27 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/arm_m.py |
| 5 | 08:25:56 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/arm_m.py |
| 6 | 08:30:38 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/fetch_reports.py |
| 7 | 08:34:13 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/sample.py |
| 8 | 08:43:16 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/sample.py |
| 9 | 08:53:20 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/fetch_reports.py |
| 10 | 08:54:37 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/sample.py |
| 11 | 08:58:20 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/sample.py |
| 12 | 09:15:53 | milestone | arm_m complete: only telegram installs silently (exit 0); sklearn, beautifulsoup, color all fail loudly. PC classification 194/233 done. G and PL clas |
| 13 | 09:37:41 | milestone | G classification complete: 3 B rows in 105 G rows. K2 primary = 3/4 = 0.75 >= 0.10. K1a met. README written. |
| 14 | 09:37:41 | artifact | wrote EXPERIMENTS/070-silent-wrong-project/README.md |
| 15 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/AMENDMENT-1.md |
| 16 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/AMENDMENT-2.md |
| 17 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/AMENDMENT-3.md |
| 18 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/AMENDMENT-4.md |
| 19 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/aid.py |
| 20 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/arm_m.py |
| 21 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/fetch_reports.py |
| 22 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/gh-beautifulsoup-beautifulsoup4.json |
| 23 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/gh-installed-the-wrong-package-github-issue.json |
| 24 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/gh-installed-wrong-pypi-package.json |
| 25 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/gh-pip-install-succeeded-but-import-failed.json |
| 26 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/gh-pip-install-telegram.json |
| 27 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/gh-pip-install-typo-wrong-package.json |
| 28 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/gh-sklearn-scikit-learn.json |
| 29 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/manifest.json |
| 30 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-beautifulsoup-beautifulsoup4.json |
| 31 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-different-pypi-package-than-intended.json |
| 32 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-how-to-install-numpy-python.json |
| 33 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-installed-wrong-package.json |
| 34 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-pip-cache-clear.json |
| 35 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-pip-install-beautifulsoup.json |
| 36 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-pip-install-color-vs-colour.json |
| 37 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-pip-install-color.json |
| 38 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-pip-install-similar-name.json |
| 39 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-pip-install-sklearn.json |
| 40 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-pip-install-succeeded-but-import-failed.json |
| 41 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-pip-install-telegram.json |
| 42 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-pip-install-typo.json |
| 43 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-pip-install-wrong-package.json |
| 44 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-sklearn-scikit-learn.json |
| 45 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/api/se-stackoverflow-telegram-python-telegram-bot.json |
| 46 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/arm_m.json |
| 47 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/raw/arm_m_pip_versions.json |
| 48 | 09:49:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-silent-wrong-project/sample.py |
| 49 | 09:49:06 | session_end | E070 complete. Arm M: only 1 of 4 declared-B names (telegram) installs silently; sklearn, beautifulsoup, color all fail loudly. Arm W: 3 B rows in 105 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-004-observe-whether-the-silent-wrong-project/events.jsonl
```
