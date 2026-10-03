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
| `test_doc_gaps.py` | Documentation-gap implications: `any` and `all` record groups |
| `test_tasks.py` | Task creation, claim conflicts, verification, index |
| `test_doclint.py` | Line cap, metadata, links, orphans, stale generated files |
| `test_skillsync.py` | Skill naming, cross-agent mirrors, vendored integrity |
| `test_fleet.py` | Two-clone fleet: remote-truth claims, takeovers, worktrees |
| `test_sync.py` | Pull, push, land, rebase, divergence reporting; the rebase continue must stay non-interactive |
| `test_session_flow.py` | Session start and finish across two clones: stale trees, uncommitted work |
| `test_cli.py` | Exit codes, index generation, doctor, preflight, in-flight tolerance |

Exit codes are part of the contract and are tested: `0` success, `1` usage,
`2` lint, `3` verification failed, `4` integrity.

**The git version is part of the suite's environment.** The land tests failed on
git 2.56 and passed on git 2.25 until `FAILURES.md` F010 was fixed, because
`git rebase --continue` opens an editor from git 2.26. Run the suite against the
git your fleet actually uses — this repository's own VMs disagree (`EXPERIMENTS/000-capabilities/`
recorded 2.55.0, one VM has 2.25.1).
