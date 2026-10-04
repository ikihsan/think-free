<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0035
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0035 — Stop the credential sandbox from inheriting a CI runner's GITHUB_TOKEN

## Goal

Stop the credential sandbox from inheriting a CI runner's GITHUB_TOKEN

## Why this matters

CI runs 37174050724, 37174316639 and 37174309822 failed the Tests step, and the cause is not the code under test: tests/pushcred_fixture.py built a sandbox with a fresh HOME and a fresh git config but left GH_TOKEN and GITHUB_TOKEN in the environment. pushprobe counts an environment token as a credential mechanism (correctly - it is one), so test_no_mechanism_is_unavailable_not_broken read 'broken' where it asserted 'unavailable'. It passed on both VMs and failed only where a runner exports the token. A fixture must build the machine it claims to build.

## Preconditions

The failure is reproduced: GITHUB_TOKEN=dummy python3 -m unittest test_pushcred.VerdictTest fails, and without the variable it passes, on the same tree and the same interpreter. The verified cause is in pushprobe.any_mechanism, not in the verdict logic.

## Steps

1. Make the sandbox clear GH_TOKEN and GITHUB_TOKEN by default and restore them afterwards, with a token=True opt-in for a test that wants one. 2. Add the negative control: an environment token alone is 'broken', not 'unavailable', which is the distinction D030 is about. 3. Add a test asserting the sandbox clears a runner-injected token, so the fixture cannot regress to inheriting the environment. 4. Falsify: restore the pre-fix fixture and both new tests must fail.

## Acceptance criteria

- [ ] The credential sandbox builds a machine with no mechanism unless a test asks for one - [ ] A test says an environment token alone is 'broken', which is what makes the 'unavailable' assertion mean something - [ ] A test fails if the sandbox stops clearing a runner-injected token - [ ] The suite is green both with and without GH_TOKEN/GITHUB_TOKEN exported - [ ] The reproduced failure and its cause are recorded, and docs/operations/doctor.md says the sandbox isolates tokens - [ ] doc lint and the full suite are green

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Revert tests/pushcred_fixture.py and tests/test_pushcred.py; no production code changes, so there is nothing else to undo.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
