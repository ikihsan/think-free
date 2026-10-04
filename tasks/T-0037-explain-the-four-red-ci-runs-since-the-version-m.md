<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0037
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0037 — Explain the four red CI runs since the version matrix landed, or recor

## Goal

Explain the four red CI runs since the version matrix landed, or record them as unexplained

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
