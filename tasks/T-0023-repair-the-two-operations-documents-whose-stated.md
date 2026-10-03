<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0023
status: done
created: 2026-10-03
claim-agent: opencode
claim-session: 2026-10-03-039-repair-two-operations-documents-that-sta
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint && tools/origin release check
-->

# T-0023 — Repair the two operations documents whose stated requirements the repo

## Goal

Repair the two operations documents whose stated requirements the repository has already falsified

## Why this matters

Both are public documents (docs/ is public by RELEASE-MANIFEST.md), and both tell a VM something untrue. docs/operations/vm-execution.md requires 'Python 3.11 or newer'; instance-20260717-0944 runs 3.8.10 and the 232-test suite is green there, so a fresh VM reading that line would refuse to work on a machine the tooling supports. docs/operations/github-app.md opens with 'Status: design, not implemented. No GitHub App exists yet', while every push for the last 21 hours has been made by a GitHub App: 121 of 131 commits are authored by 'Ihsan Ai Server Bot <ihsan-ai-server-bot[bot]@...>' and D018 records the durable credential arrangement.

## Preconditions

Claim only what can be observed. The App's permissions, installation scope, and workflow triggers cannot be read from this repository, so they must stay marked unverified rather than be guessed. Neither document is claimed by the other VM: T-0020 touches session verification, not docs/operations.

## Steps

1. Record what is observable about the App: the bot author on 121 commits, the App id recorded in D018, the durable helper under ~/.config, and CI reading the remote. 2. Rewrite the status block to separate observed from unverified, and tick only the checklist items that are demonstrably done. 3. Replace the Python requirement with the versions the suite is actually verified on, pointing at the machine-readable record rather than restating it. 4. Check the other operations documents for the same two claims and fix any that are false.

## Acceptance criteria

- [x] No document in `docs/` claims no GitHub App exists
- [x] The App's status separates what is observed from what is unverified, and
      the least-privilege table is marked as a design to check against rather
      than a reading of the real settings
- [x] No document requires a Python version the suite has not been verified on
- [x] The Python statement points at the machine-readable record for the git
      equivalent and names the missing Python equivalent as a gap
- [x] `doc lint`, `release check`, and the full suite (232 tests) green

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint && tools/origin release check
```

## Rollback

Revert the commit; both files are prose and nothing reads them at runtime.

## Notes

**Four documents were wrong, not two.** `bootstrap.md` carried the same Python
floor and the same "a GitHub App private key, until github-app.md is
implemented" rule, and `ci.md` listed five gates, missed the sixth, and claimed
`preflight` covers "the first four" when it covers three. All four are repaired.

**The key-handling check was run rather than assumed.** It is the check the
document had been waiting on: 111 files under `sessions/` and
`.origin/doctor.json` carry no secret shape. Doing it turned up a key at mode
`0644` in a `0700` directory, repaired to `0600` on this VM.

**What stays open, deliberately.** The App's real permissions and installation
scope are unobservable from this repository, so `github-app.md` now says so in
three places rather than implying the design table describes reality. And
`doctor` checks four credential environment variables while the App uses a key
file, so a VM with a broken helper reports healthy — recorded in `STATE.md` and
the ROADMAP rather than fixed here, since it changes `doctor`'s output shape.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
