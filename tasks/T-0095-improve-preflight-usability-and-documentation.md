<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-13
-->

# T-0095 — improve preflight usability and documentation

<!-- task-meta
id: T-0095
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