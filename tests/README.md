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
| `test_conflicts.py` | Unresolved merge-conflict markers: every shape git writes, the shapes that must stay silent, the declared waiver |
| `test_release.py` | `RELEASE-MANIFEST.md` enforcement: one seeded defect per clause, and a fixture that passes |
| `test_skillsync.py` | Skill naming, cross-agent mirrors, vendored integrity |
| `test_fleet.py` | Two-clone fleet: remote-truth claims, takeovers, worktrees |
| `test_sync.py` | Pull, push, land, rebase, divergence reporting; the rebase continue must stay non-interactive |
| `test_session_flow.py` | Session start and finish across two clones: stale trees, uncommitted work |
| `test_cli.py` | Exit codes, index generation, doctor, preflight, in-flight tolerance |
| `test_inflight_session.py` | In-flight versus abandoned: one falsifiable clause per rule of `inflight.classify`, plus the `--strict` and `--lease-hours` gate |
| `test_landed_work.py` | Attribution when another VM's commits land mid-session: replayed against session 029's nine false reports, with the negative controls that must keep reporting |
| `test_task_index_freshness.py` | A created task is linked by the generated indexes: `task new` then `doc lint` must pass with no manual regeneration, and a file nobody created must still be an orphan |
| `test_gitversions.py` | Schema of `git-versions.json` and that the docs point at it |
| `git-versions.json` | Machine-readable record of the git versions the suite and the sync flow are verified against (schema `origin.git-versions/1`) |

Exit codes are part of the contract and are tested: `0` success, `1` usage,
`2` lint, `3` verification failed, `4` integrity.

**A test that cannot fail is worse than no test.** Every clause of the in-flight
predicate was checked by deleting the clause and re-running: each produced a
failing test. Do the same before believing a new gate is covered — F011, F013,
F014 and F015 all sat in code paths whose tests could only have passed.

**Falsifying a new gate.** A gate added for a defect is run against that
defect's own bytes before it is trusted. `test_conflicts.py` carries the three
committed regions of `fd7b4a1` as literal text with the line numbers the rule
must report, which is how its first implementation was caught reporting only
malformed blocks and missing three of four committed defects.
`test_release.py` seeds one defect per clause of `release check` into a
throwaway repository, plus a fixture that passes — because a check that only
ever fails is not a check either.
`test_landed_work.py` was written before the fix it covers and run against the
unfixed code first: 4 failures and 1 error naming session 029's mis-attributed
paths. Reverting the exclusion failed 3 of its 6 tests while the 3 negative
controls stayed green, which is the shape a falsifiable control should have.

**The git version is part of the suite's environment.** The land tests failed on
git 2.56 and passed on git 2.25 until `FAILURES.md` F011 was fixed, because
`git rebase --continue` opens an editor from git 2.26. The machine-readable
authority is [`git-versions.json`](git-versions.json): every version there has
carried the full suite green. This repository's VMs disagree
(`EXPERIMENTS/000-capabilities/` recorded 2.55.0, one VM has 2.25.1), so run
the suite against the git your fleet actually uses — and when a new version
goes green, record it in `git-versions.json` rather than in prose alone.
