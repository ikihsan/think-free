<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Reading a red CI run

How to find out which test failed on a pushed commit, without repository admin
rights. Split out of [`ci.md`](ci.md) on 2026-10-04 when that file reached 312 of
the 300 permitted lines; the stub there is the entry point, this file is the
whole method. Evidence for every number below is `FAILURES.md` F020, measured
from the public API on 2026-10-04.

## The run log is not the only way in

`GET /repos/{owner}/{repo}/actions/runs/{id}/logs` needs admin rights on a private
repository, and this repository is private. F019 spent an hour of elimination
before establishing that, and recorded the reason as "the public check-runs API
returns no annotations". **That reason does not hold.** The annotations are
public; they were simply not where the first reading looked.

## Two calls

```bash
OWNER=ikihsan; REPO=think-free

# 1. jobs, rows and check-run ids for one commit
curl -s "https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/check-runs"

# 2. the messages for one check run, one annotation per line
curl -s "https://api.github.com/repos/$OWNER/$REPO/check-runs/$ID/annotations"
```

The `Tests` step emits `::error::` lines, so a `Tests` failure annotates the
failing test's id, its file and its line — verbatim, from run `37178057818`:

```
FAIL: test_this_vms_versions_are_exercised_against_the_real_records (test_doctor_versions.RealRecordTest…)
File "/home/runner/work/think-free/think-free/tests/test_doctor_versions.py", line 69
AssertionError: 'unrecorded' != 'exercised'
```

That is F019's cause — the runner's git 2.55.0 absent from
[`../../tests/git-versions.json`](../../tests/git-versions.json) — read off the
run instead of reproduced on a VM, and the same seven rows it names were red on
run `37179073002`.

## Four answers, and only one of them is "nothing"

| What you see | What it means |
|---|---|
| Annotations, one starting `FAIL:` or `ERROR:` | The step emits. Read them. |
| Three annotations, the failure being `Process completed with exit code N` | The step emits nothing naming its violation. `Documentation lint` and `Release manifest` print no `::error::` at all, and the session step emits `::warning::` only for in-flight sessions — which is not what fails it |
| No annotations object, or `annotation_count: None` | The jobs endpoint has none. The field a check run carries is `output.annotations_count`, and on run `37178057818` it read 11 |
| HTTP 403 | The unauthenticated rate limit: 60 requests an hour per IP, and this VM has no token in its environment |

**Check `/rate_limit` before concluding anything from a 403.** A failed call and
an empty list are different answers, and treating the first as the second is how
this repository recorded a false premise for two sessions.

The general form is D030 (`[../../DECISIONS-GATING.md`](../../DECISIONS-GATING.md))
one domain out: a diagnostic must distinguish "never configured" from "stopped
working". Here it is four states, and a tool that collapses the last three into
"no annotations" is confidently wrong.

## Ceiling

The messages are the workflow's own emission, capped by the `awk` window in the
`Tests` step at 60 lines, so a run with more failures than that annotates a
prefix of them. Nothing here verifies a conclusion — it names a test, so the
conclusion can be checked on a VM, which is where F019's cause was actually
settled. And one run's rows need not agree: run `37178057818` annotates a second,
different test on its 3.11 row, which no single-cause explanation covers.