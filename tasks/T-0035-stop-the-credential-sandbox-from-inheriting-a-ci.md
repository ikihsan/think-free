<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0035
status: done
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

## Outcome

`observed`, and it was not the code under test. Three CI runs failed the Tests
step (`37174050724`, `37174316639`, `37174309822`) while the suite was green on
both VMs and green locally on the same commits.

**The cause.** `tests/pushcred_fixture.py` built a sandbox with a fresh `HOME`,
a fresh `XDG_CONFIG_HOME`, a fresh git config and `GIT_CONFIG_SYSTEM=/dev/null` —
and inherited `GH_TOKEN` and `GITHUB_TOKEN` from the environment.
`pushprobe.any_mechanism` counts an environment token as a credential mechanism,
which is correct: it is one. So on a runner that exports `GITHUB_TOKEN`,
`test_no_mechanism_is_unavailable_not_broken` built a machine with a mechanism
and asserted `unavailable`, and read `broken`.

Found by reproducing it, not by reading the run: the failing step was `Tests`
with no annotations, the run log needs admin rights, and
`GITHUB_TOKEN=dummy python3 -m unittest test_pushcred.VerdictTest` fails on the
same tree and interpreter that passes without the variable. Confirmed against
the previous commit too (`4401bd2c`), so the cause predates T-0033 and was
introduced with the fixture in T-0025.

**The fix.** `Sandbox.activate` clears both token variables by default and
restores whatever it found; `token=True` opts back in for a test that wants one.

**Falsified three ways before it was trusted**, all in the session command log:
the pre-fix fixture (3 failures), a fixture that injects a token rather than
clearing one (3), and a fixture that clears the tokens but never restores them
(1). **The third was found by falsifying rather than by reading** — the first two
falsifications left the suite green, so nothing was asserting the restore. Since
unittest runs every class in one process, a token left cleared by one test
changes the verdict the next one reads, and the new
`test_the_sandbox_restores_the_tokens_it_found` says so.

**The control, which is the point.** `test_an_environment_token_alone_is_a_broken_mechanism`
asserts the opposite verdict for a machine carrying a token and no helper. The
original test only showed that *some* absence is reported; the pair shows *which*
absence, and it is D030's subject — absence and breakage are different states.

## The lesson, which cost three red runs

A fixture that inherits its environment tests the runner as much as the code, and
it fails only where the runner differs. This repository already had the lesson
recorded from the other direction (`tests/README.md`: a fixture naming
`/tmp/github-app-jwt.sh` passed on one VM and failed on another), and the same
sentence applies — "a fixture must build its own sandbox" — read as *including the
environment*, which it did not mean at the time.

380 tests green with and without `GH_TOKEN`/`GITHUB_TOKEN` exported.
