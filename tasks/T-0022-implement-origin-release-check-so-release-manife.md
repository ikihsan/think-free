<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0022
status: open
created: 2026-10-03
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin release check && tools/origin doc lint
-->

# T-0022 — Implement 'origin release check' so RELEASE-MANIFEST.md is enforced by

## Goal

Implement 'origin release check' so RELEASE-MANIFEST.md is enforced by a machine rather than by review

## Why this matters

ROADMAP lists it twice as outstanding. RELEASE-MANIFEST.md says three times that nothing enforces it, so 'a path listed as public here is a human claim rather than a machine guarantee'. D004 made the manifest the authority on the public split and the coverage check it implies fails today: seven top-level tracked entries (RELEASE-MANIFEST.md, STATE-history.md, FAILURES-findings*.md, HYPOTHESES-results.md, .github/, .gitignore) are classified by neither table, and three declared-public paths (LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md) do not exist with no way to say they are expected to be absent.

## Preconditions

The manifest tables must be machine-parseable without losing their prose. Each check needs a seeded defect, or it may be vacuous - the same lesson as D024 and D025. Do not edit .github/workflows/ci.yml next to the Session record integrity step: instance-20260717-0947 holds T-0020 and is adding annotations there, so insert the new step earlier in the file to keep the rebase clean.

## Steps

1. Parse the two tables into path sets with a pending marker, in tools/originlib/release.py. 2. Check no wildcards, exactly-one classification of every top-level tracked entry, declared-public paths exist unless pending (and pending ones must not exist), and no public path sits inside an internal directory. 3. Scan every classified path for credential shapes, since manifest rule 3 covers internal as well as public. 4. Add the front-door state marker: the manifest declares a release state and README must declare the same one, which makes manifest rule 4 decidable as agreement rather than truth. 5. Classify the seven unclassified entries and mark the three absent paths pending, in the same commit. 6. Falsify every check by seeding each defect into a throwaway repository and asserting a non-zero exit. 7. Wire it into the CLI and into CI, after the Documentation lint step so the rebase stays clean. 8. Document what the check does not decide, because a check that reads as broader than it is worse than none.

## Acceptance criteria

- [ ] `tools/origin release check` exits 0 on this tree and exits non-zero on a seeded defect of each kind
- [ ] Every top-level tracked entry is classified by exactly one table
- [ ] A path declared public and absent is marked pending, and removing the pending mark fails the check
- [ ] The manifest and README must agree on the release state, and disagreeing fails
- [ ] Credential-shaped text in a classified path fails
- [ ] CI runs it, and the failure output names the file and line
- [ ] The check's limits are stated in both the manifest and the CLI reference
- [ ] Full test suite and doc lint green

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin release check && tools/origin doc lint
```

## Rollback

Revert the module, the CLI wiring, the CI step, and the manifest edits. Nothing is stored outside the manifest itself, so reverting the commit restores the previous, unenforced state.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
