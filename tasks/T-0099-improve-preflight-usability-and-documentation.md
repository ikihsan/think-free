<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-13
-->

# T-0099 — improve preflight usability and documentation


<!-- renumber
On 2026-10-20 the lineage merge found `T-0095` allocated by both lineages from the
same base. The unpushed side yields, so this task is now `T-0099`; its sealed session
streams still name `T-0095` and were not rewritten.
-->

<!-- task-meta
id: T-0099
status: open
created: 2026-10-13
claim-agent: opencode
claim-session: 2026-10-13-001-t-0095-improve-preflight-usability
claim-vm: instance-20260717-0944
verify: tools/origin doc lint && python3 -c "
import json, sys
catalog = json.load(open('EXPERIMENTS/adapters_catalog.json'))
assert catalog['total_harnesses'] == 8, f'Expected 8 harnesses, got {catalog[\"total_harnesses\"]}'
for h in catalog['adapter_measurement']['harness_structure']:
    assert h['under 50-line ceiling'] == True, f'{h[\"harness structure\"]} exceeds 50 lines'
print('All', catalog['total_harnesses'], 'adapters under 50-line ceiling, catalog complete')
sys.exit(0)
"