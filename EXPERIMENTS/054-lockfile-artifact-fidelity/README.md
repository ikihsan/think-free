# E054 — Lockfile-pinned artifact fidelity over ~10 months

<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-08
-->

Follow-up to E050. E050 established that 0 of 421 pinned
(name, version) pairs were yanked or absent and all 3800
recorded artifact URLs still resolve. Both are
existence checks: a rewritten URL, or a URL whose bytes
changed under the same version string, answers "found".
E054 closes that gap.

## Question, declared before the run

For the artifacts E049's old uv.lock snapshots pinned with
a URL and sha256 (September–December 2025), do the bytes at
that URL today hash to the recorded sha256?

## Method

Extracted every `url = "...", hash = "sha256:..."` pair
from the six E049 old-snapshot uv.lock files
(encode_starlette, encode_uvicorn, pallets_flask,
pallets_werkzeug, samuelcolvin_pydantic,
urllib3_urllib3): 3800 unique URLs. Deterministic stride
sample of every 7th sorted URL (seedless: stride over the
sorted set, recorded in results.json). Each sampled URL was
fetched today and its sha256 compared to the recorded one.

## Result

- Sample: 543 of 3800. **Byte mismatches: 0. Fetch failures: 0.**
- Every one of the 543 fetched artifacts hashed exactly to
  the six-to-ten-months-old recorded hash.

## Verdict

`no-artifact-drift`. The registry-retraction mechanism is
now dead at this population on both prongs: no pinned
version is yanked or absent (E050), and no live artifact's
bytes differ from the bytes the lockfiles recorded (E054).
E2's registry claim survives only as the time-gated Part B
re-run of E049, not as something a candidate could promise
to fix today.

Ceiling: one registry (PyPI), one artifact ecosystem, one
snapshot population of ten projects, one sampling stride.
Recorded via `tools/x`; raw counts in results.json.
