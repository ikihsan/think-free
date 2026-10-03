<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0017
status: done
created: 2026-10-03
claim-agent: opencode
claim-session: 2026-10-03-030-run-t-0017-attribute-every-differing-byt
claim-vm: instance-20260717-0944
verify: test -d EXPERIMENTS/008-build-timestamp-attribution && python3 -c "import json;d=json.load(open('EXPERIMENTS/008-build-timestamp-attribution/results.json'));s=d['sources'];assert len(s)>=4;assert all(r['built_ok'] for r in s);assert all(len(r['builds'])==7 for r in s);c=[r['comparisons']['arm_n_different_mtime'] for r in s];assert all('patch_identical' in x and 'differing_bytes_in_timestamp_fields' in x for x in c);assert all(x['half_controls']['local_header_only_reaches_identity'] is False and x['half_controls']['central_directory_only_reaches_identity'] is False for x in c);p=[r['comparisons']['planted_content_defect'] for r in s];assert all(any(k['kind']=='content-differs' for k in x['residual_causes_after_patch']) for x in p);assert d['gate']['verdict'] in ('timestamps-first','timestamps-not-first','inconclusive')" && grep -q '008-build-timestamp-attribution' HYPOTHESES.md && grep -q 'F012' FAILURES.md && tools/origin doc lint
-->

# T-0017 — Build one source twice under different SOURCE_DATE_EPOCH values and at

## Goal

Build one source twice under different SOURCE_DATE_EPOCH values and attribute the byte difference per cause, to test whether build timestamps are worth fixing first

## Why this matters

RESEARCH/E.md's E3 falsifying experiment has two halves. T-0013 ran the prevalence half over 200 PyPI wheels and passed its predeclared 5% gate at 0.965, but the metric it names is near-vacuous: it counts wheels whose DOS epoch is not pinned to 1980, which 193 of 200 wheels fail, so it cannot say whether timestamps are the dominant cause of a reproducibility failure. The load-bearing claim ('worth fixing first') needs the other half, which E.md states in the mechanism section and which is runnable on this machine. Prevalence without attribution is not a decision input, and this is the cheapest experiment in the repository that could change E3's standing.

## Preconditions

setuptools 45.2.0 and wheel 0.34.2 present on this machine; Python 3.8.10; a small pure-Python source tree that builds with bdist_wheel

## Steps

1. Pick a source tree that builds with 'python3 setup.py bdist_wheel' and pin the builder. 2. Build it N>=6 times under distinct SOURCE_DATE_EPOCH values with no other change, recording the sha256 of each artifact. 3. Compare byte-for-byte pairs, then attribute each differing byte region to a cause: zip entry date fields, RECORD/METADATA content, file ordering, compression level, or genuinely different file content. 4. Build again twice with the SAME SOURCE_DATE_EPOCH on a clean tree to establish the noise floor: how many runs are bit-identical when nothing changes? 5. Report, per cause, the fraction of differing bytes and the fraction of artifacts that are bit-reproducible, and state what an all-causes-fixed comparison would look like. 6. Apply a predeclared gate before looking at the numbers.

## Acceptance criteria

A predeclared kill gate written before the run; >=6 builds under distinct epochs plus a same-epoch noise floor; every differing byte attributed to a named cause; the answer to whether timestamps alone account for the difference is explicit and quantitative

## Verification

```bash
test -d EXPERIMENTS/008-build-timestamp-attribution && python3 -c "import json;d=json.load(open('EXPERIMENTS/008-build-timestamp-attribution/results.json'));s=d['sources'];assert len(s)>=4;assert all(r['built_ok'] for r in s);assert all(len(r['builds'])==7 for r in s);c=[r['comparisons']['arm_n_different_mtime'] for r in s];assert all('patch_identical' in x and 'differing_bytes_in_timestamp_fields' in x for x in c);assert all(x['half_controls']['local_header_only_reaches_identity'] is False and x['half_controls']['central_directory_only_reaches_identity'] is False for x in c);p=[r['comparisons']['planted_content_defect'] for r in s];assert all(any(k['kind']=='content-differs' for k in x['residual_causes_after_patch']) for x in p);assert d['gate']['verdict'] in ('timestamps-first','timestamps-not-first','inconclusive')" && grep -q '008-build-timestamp-attribution' HYPOTHESES.md && grep -q 'F012' FAILURES.md && tools/origin doc lint
```

## Rollback

Delete EXPERIMENTS/008-build-timestamp-attribution/ and the HYPOTHESES.md row. Nothing else consumes a build-attribution table, and no published wheel is involved.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**Numbering.** Created as T-0016 at 21:21:57. Session 029 on
`instance-20260717-0947` created its own T-0016 at 21:28:52 and pushed it first,
so this task is T-0017. Its finding is F012, not F011: F009 (knitting prior art), F010 (E3's
census, session 026) and F011 (`sync land` on git >= 2.26, session 032) were all
taken by the time this result was recorded, the last one by the other VM in the
same hour. `task new` allocates from the local
tree, which two VMs cannot share; the renumber has to happen before the push.

**The verify string was rewritten.** As created it asserted `d['builds']` and
`d['attribution']`, keys this task guessed before any run. The schema that
`results.json` actually holds is `sources[].comparisons` and `sources[].builds`,
so the original string could never have passed. It now checks what the acceptance
criteria actually require: five sources built with seven builds each, per-pair
attribution present, **both half-controls false on every source**, a
`content-differs` residual on every planted source, a legal verdict, and the two
record updates. A verify command that cannot run is worse than none.
