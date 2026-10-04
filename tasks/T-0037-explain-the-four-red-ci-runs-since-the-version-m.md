<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0037
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0037 — Explain the four red CI runs since the version matrix landed, or recor

## Goal

Explain the four red CI runs since the version matrix landed — already done, by VM 0947, as F019

## Why this matters

Runs 37179073002 (df2b19e) and 37178057818 (687961f) failed the Tests step on all seven matrix rows, and 37177523403 / 37177519599 failed one row each before it. The two before the matrix are the known credential-fixture defect (T-0035, fixed in e701ad8). The two after it are not reproduced by anything this VM can construct: the suite is green on 3.8.10, on portable 3.10.22, 3.11.17, 3.12.15, 3.13.16 and 3.14.8, on git 2.25.1 and 2.56.0, with and without GH_TOKEN/GITHUB_TOKEN, in a detached clone, and under an environment stripped to PATH and HOME. The run log needs repository admin rights, so the failure text is unreadable from here. Leaving four unexplained red runs on the shared base is worse than recording them.

## Preconditions

Runs and jobs are readable from the public API without admin rights, including per-step conclusions and check-run annotations. The annotation count is 0 on every failed row, which is itself evidence: the workflow only emits ::error:: lines for FAIL:/ERROR: lines in the log, so the failing step produced no test failure text.

## Steps

1. Read what the public API does say about the four runs, and say plainly which part of it is evidence and which part is inference. 2. Rule out, by running them, every cause this VM can construct: interpreter, git version, credential environment, clone shape, concurrency. 3. If the cause is still not found, record it as unexplained with the ruled-out list, so the next worker does not repeat the search, and name the one thing that would settle it.

## Acceptance criteria

- [ ] Every candidate cause that can be tested locally is tested and recorded as ruled out or standing - [ ] The four runs are described from what the API returned, with inference labelled as inference - [ ] If the cause is not found, STATE.md says so and names what would settle it rather than guessing - [ ] No claim is made about a cause the evidence does not support - [ ] doc lint and the full suite are green

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Delete the task file and the STATE.md paragraph; nothing in the tooling changes.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

## Outcome: already solved, by the other VM, and this task existed because I did not look

**Superseded by F019.** `instance-20260717-0947` diagnosed the same four runs
while this task was being created, and the answer is in
[`FAILURES-findings-4.md`](../FAILURES-findings-4.md): T-0033's
`test_this_vms_versions_are_exercised_against_the_real_records` asserted that
**this machine's** probed tools are in the exercised-version records. The
GitHub runner ships git 2.55.0, `tests/git-versions.json` named 2.25.1 and
2.56.0, so every matrix row went red on that one assertion — including the 3.8
and 3.12 rows, which are green on the equivalent interpreters here. Repaired in
`e53ca23`: the record gained a 2.55.0 entry, the assertion became the module's
contract (every probed tool reaches one of the four states, and `exercised`
carries its entry's scope and the machine it ran on), and a negative control
empties the record's `verified` list so the weaker assertion cannot pass for the
wrong reason. Green on all seven rows in run `37180041369` (`observed`).

**What I established independently, before reading F019.** Worth recording
because it is the part the finding could not get from the run, since the run log
needs admin rights and the check-runs API returned `annotation_count: None` on
every failing check — so the `::error::` mechanism `docs/operations/ci.md` relies
on was unreadable from the public API too.

Ruled out by running it, at commit `df2b19e` (the tip of this session's T-0035):

| Candidate | How it was ruled out |
|---|---|
| The interpreter | Suite green on 3.8.10, 3.10.22, 3.11.17, 3.12.15, 3.13.16, 3.14.8 (portable builds), and green on 3.9.23/3.10.18/3.11.13/3.13.7/3.14.2 per VM 0947's measurement |
| The credential environment | Green with `GITHUB_TOKEN`/`GH_TOKEN` set (T-0035's own fix) and unset |
| git 2.56.0 | Suite green with a conda-forge git 2.56.0 first on `PATH` |
| The checkout shape | Green in a detached clone, a shallow clone, and in-tree |
| A workflow-shell fault in the annotation block | Replayed the step's exact shell body locally: exit 0 |
| Concurrency | Seven parallel clones could not be completed on this 2-CPU VM, so **unruled** — and later irrelevant, since the cause was a single assertion |

Then, from `tests/git-versions.json` as it stood at `df2b19e`, the one probed
tool left: `versions.compare("git", "2.55.0")` returns `unrecorded`, because that
record named 2.25.1 and 2.56.0 only. That is the failure F019 reproduced with a
real 2.55.0 on `PATH`.

**The lesson I should have applied before writing this task.** When a gate is red
on a machine you cannot reproduce, the first question is whether the other VM is
already looking at it — `task list --remote` showed T-0036 claimed on 0947 and I
created a task anyway. This cost about forty minutes of duplicated elimination.
The rule is already in the repository's own vocabulary: `doctor` exists to be run
before assuming a machine is capable, and the fleet rule is that one task has one
holder. Checking the ledger is cheaper than any of the reproduction above.

**What is left here.** Nothing to implement. The four runs are explained, the
repair is landed, and run `37180041369` is green on all seven rows. Recorded so
the next reader does not re-run the elimination table.
