<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0050
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-034-separate-the-line-cap-exemption-from-rec
claim-vm: instance-20260717-0947
verify: python3 -m unittest discover -s tests && tools/origin preflight
-->

# T-0050 — Separate the line-cap exemption from reconciliation, so a json/jsonl/l

## Goal

Separate the line-cap exemption from reconciliation, so a json/jsonl/log edit cannot pass undeclared

## Why this matters

Item 2(d) of STATE-next-actions.md, and the false negative defect 12's entry says it never measured: reconcile._is_vendored reuses doclint.is_exempt, which returns True for DATA_SUFFIXES because those files are exempt from the 300-line cap. Content the cap ignores is treated as content no session can change silently, so tests/python-versions.json, tests/git-versions.json and tasks/CLAIMS.jsonl can be edited with nothing declared and nothing reported - the opposite of the defect T-0047 closed, which fixed the false positives. A version record that decides whether this VM can run the work is exactly the kind of file that must not be editable undeclared.

## Preconditions

Measure the change's cost before making it: sweep every closed session's window for data-suffix paths that are not declared, so the new reports are a list rather than a surprise.

## Steps

1. Sweep every closed session: the data-suffix paths its commits touched that no artifact event declared, with the generated mark and the session's own directory excluded. Record the counts.
2. Split doclint.is_exempt into the two questions it was answering - a data suffix, which only the cap cares about, and a declared exempt: glob, which both do - and make reconcile._is_vendored read only the declared globs.
3. Declare the claim ledger the way the task file is declared: the appender records the path and the bytes it wrote, so task commands' own appends are silent and any later edit is reported.
4. Falsify both ways: remove the new clause and watch the new tests fail; run the rule over the sweep's own commits and over the tip.
5. Record the measurement, the ceiling and the sweep as a test, and close defect 12's stated residual.

## Acceptance criteria

The sweep is committed as a runnable script and its numbers are in the record, with the sessions and paths named - not a promise that the sweep would be clean.
The new tests fail against the unrepaired code: a .json and a .jsonl and a .log changed without declaring are reported, and the pre-repair rule reports none of the three.
tasks/CLAIMS.jsonl is declared by its appender with the digests of the bytes it wrote, silent while they match and reported after any later edit - the property defect 12 refused to trade away.
No data-suffix path is exempt from reconciliation because of its suffix: every remaining exemption is declared, hash-verified (vendored), generated, or the session's own directory.
preflight green and the sweep silent on the tip.

## Verification

```bash
python3 -m unittest discover -s tests && tools/origin preflight
```

## Rollback

Revert the doclint/reconcile split and the ledger declaration; nothing outside tools/ and tests/ depends on it.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
