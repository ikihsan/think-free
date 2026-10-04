<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0027
status: done
created: 2026-10-03
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint && tools/origin release check && tools/origin skills verify
-->

# T-0027 — Make 'origin doctor' report the push credential mechanism it never ins

## Goal

Make 'origin doctor' report the push credential mechanism it never inspected

## Why this matters

doctor prints 'credentials none present' on a VM whose pushes are made by a GitHub App key file reached through git's credential helper, so it prints the same line on a working credential, on a broken helper, and on no credential at all. D025 requires a gate to read the property it claims; github-app.md and ROADMAP.md both list this as an unticked item, and this VM carries the live instance of it: ~/.config/github-app/git-credential-helper.sh invokes /tmp/github-app-jwt.sh, the /tmp dependency STATE.md records as having broken pushes on instance-20260717-0947.

## Preconditions

The App's own permissions stay unverified: no agent can read them. The check must never read, print, or write a credential value. doctor is not a CI gate because it probes the network, so a network probe is allowed here.

## Steps

1. Record the falsification first: three environments that must be distinguishable, and the current probe's identical output for all three. 2. Add a push_credential section to doctor that reports the configured credential.helper values, whether each filesystem helper exists and is executable, App key files by path and mode only, whether the named helper actually answers git's credential get protocol, and which absolute paths outside the user's home it depends on. 3. Give it a verdict: unavailable, broken, or configured, and say in the module that 'configured' does not mean 'authenticated'. 4. Repoint this VM's helper off /tmp onto the durable script under ~/.config, and show the reported dependency disappears only because of that change. 5. Cover it with tests including a fake helper returning a recognisable token, and assert the token never reaches doctor.json or stdout. 6. Update github-app.md, cli-reference.md, permissions-and-safety.md, ROADMAP.md, STATE.md and a decision record.

## Acceptance criteria

- [x] doctor reports the configured credential helper and whether each named helper exists and is executable
- [x] doctor reports a verdict that distinguishes no credential, a broken helper, and an intact one
- [x] the recorded instance-20260717-0947 defect (helper pointing at a path under /tmp that no longer exists) is detected, and the check fails when it should
- [x] no credential value reaches stdout, .origin/doctor.json, sessions/, or any log
- [x] this VM's helper no longer depends on a path outside ~/.config, verified by the new check and by a working push
- [x] the ceiling is stated: 'configured' is not 'authenticated', and git ls-remote cannot prove authentication because this remote is public
- [x] github-app.md's unticked checklist item is closed or restated honestly; doc lint, release check, skills verify and the full suite green

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint && tools/origin release check && tools/origin skills verify
```

## Rollback

Revert the commit. The only non-repository change is this VM's credential helper,
whose previous content is at `~/.config/github-app/git-credential-helper.sh.bak`;
the generator it now calls is `~/.config/github-app/jwt.sh`.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**The falsification was run before the fix, and it is in the command log.** Three
environments, each with its own `HOME` and its own `credential.helper`: a working
credential, the recorded `instance-20260717-0947` failure, and no credential.
`git credential fill` separated them (exit 0 vs 128, two distinct git
complaints). The old `doctor` produced **one** distinct report for all three.
After the fix the same harness produces three.

**The obvious functional probe cannot work here.** `git ls-remote <remote>` exits
0 with no credential at all: this remote is public, `GET /repos/ikihsan/think-free`
answers 200 unauthenticated. A gate built on it would have been F010 with extra
steps. That was found by trying it first, not by reasoning about it.

**The check found a live defect on the VM that wrote it.** `0944`'s helper was
intact, mode `0700`, and working, and invoked `/tmp/github-app-jwt.sh` — the
exact dependency that cost `0947` a day of pushes. Repaired by moving the
generator to `~/.config/github-app/jwt.sh` and repointing the helper, then
**deleting `/tmp/github-app-jwt.sh`**: `git credential fill` still exits 0 and the
warning is gone, so the dependency disappeared because the helper changed and not
because the check stopped looking. `~/.config/github-app/get-token.py` on this VM
returns HTTP 401 and is not the generator the helper uses; left in place, since a
broken credential artifact is worth recording rather than deleting.

**The harness's own first two cases damaged this machine** (`FAILURES.md` F014).
Two of its three sandboxes were `Path.home()`, so it overwrote the real
`~/.gitconfig` and destroyed the git identity 125 commits are authored with. The
harness now refuses any HOME outside its own directory. A related lesson: a
fixture that names a real path is a fixture the machine decides — the first
recorded-defect test named `/tmp/github-app-jwt.sh`, which exists here, so it
passed for the wrong reason. Fixtures now build every path inside a sandbox.

**A second defect surfaced while running the work** (`FAILURES.md` F015). `doc
index` rewrote 35 session reports because every generator stamped `last-verified`
with the clock, and since `doc lint` fails on a stale generated file, the
documentation gate would have failed at midnight on an unchanged repository.
Stamps are now functions of the record each file summarises, and the churn is
gone: `doc index` is idempotent and content-determined.

**Two proxies were caught by running the tests against the change itself.** The
verdict order first reported a fresh VM with no credential as `broken`; and
`_carries_secret` first tested for the substring `password=`, so a helper whose
token generator had vanished counted as healthy. Both are D024's mistake — a
clause implemented as a weaker proxy — and both were found by the harness and the
test suite rather than by reading the code.
