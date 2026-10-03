<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Tests

Standard-library `unittest` suite. No third-party runner, so it works on a
fresh VM with nothing installed.

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests
```

Each test builds a throwaway git repository in a temporary directory, copies the
tooling into it, and points `ORIGIN_ROOT` at it. Tests therefore exercise the
same code path as the CLI, including real `git` reconciliation, and cannot
interfere with the working repository.

| File | Covers |
|---|---|
| `harness.py` | Repository fixture and in-process CLI runner |
| `test_events.py` | Event ordering, schema validation, malformed-line handling |
| `test_secrets.py` | Secret detection, redaction, artifact refusal |
| `test_session.py` | Lifecycle, reconciliation, command capture, reports |
| `test_tasks.py` | Task creation, claim conflicts, verification, index |
| `test_doclint.py` | Line cap, metadata, links, orphans, stale generated files |
| `test_skillsync.py` | Skill naming, cross-agent mirrors, vendored integrity |
| `test_cli.py` | Exit codes, index generation, doctor, preflight |

Exit codes are part of the contract and are tested: `0` success, `1` usage,
`2` lint, `3` verification failed, `4` integrity.
