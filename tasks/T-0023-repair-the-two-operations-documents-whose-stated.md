<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0023
status: open
created: 2026-10-03
claim-agent:
claim-session:
claim-vm:
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

- [ ] No document in docs/ claims no GitHub App exists
- [ ] The App's status separates what is observed from what is unverified
- [ ] No document requires a Python version the suite has not been verified on
- [ ] The Python statement points at the machine-readable record
- [ ] doc lint, release check, and the full suite green

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint && tools/origin release check
```

## Rollback

Revert the commit; both files are prose and nothing reads them at runtime.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
