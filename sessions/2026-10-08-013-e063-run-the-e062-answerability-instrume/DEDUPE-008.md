<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# The repair of session 008's stream, and what it cost

Session `2026-10-08-013`, VM `instance-20260717-0944`, 2026-10-08. Defect 24.

`tools/origin session verify` failed on
`sessions/2026-10-08-008-record-the-last-unlogged-paths-and-commi/events.jsonl`
with `sequence is not 1..n contiguous`, and would not stop failing for any later
commit. The file held **181 lines carrying 162 sequence numbers**: 19 numbers
appeared twice.

## What happened

Two `origin session finish` runs for session 008 overlapped on the same VM. Each
allocated sequence numbers by reading the file's tail and adding one, so both
allocated from the same snapshot, and both appended. The result is two complete
reconciliations — 84 `unlogged_change` events for the **same 84 paths** — over
one stream, with the `session_end` written twice.

`finish`'s own guard against this, added for session 014, is a read of the stream
for an existing `session_end` followed by the append. Two finishes that both read
before either wrote both see no `session_end` and both proceed.

## The repair, in two parts

1. **`tools/originlib/events.py`** — `hold_stream()` takes an exclusive
   `flock` on the stream, allocates the next number inside it, and writes before
   releasing. `append()` goes through it; `next_seq()` remains as a
   read-without-the-lock preview and says so. `recorder.record` holds the lock
   across both its command-log block and its event, because the log header and
   the event must carry the same number.
2. **`tools/originlib/session.py`** — `_single_finish()` holds a
   `.finish.lock` beside the session's stream for the whole of `finish`, so the
   second of two overlapping runs exits 1 with `another 'session finish' is
   already running` instead of writing.

`tests/test_event_stream_concurrency.py` runs four processes appending to one
stream and asserts the numbers come back `1..n` contiguous, and that the second
of two concurrent `finish` calls is refused.

## The record repair, and what it does not restore

19 duplicate lines were dropped, keeping the first occurrence of each number.
This is a deletion from an append-only log, so it is recorded here rather than
done silently.

**Nothing is lost except duplication.** Checked row by row before deleting:

| check | result |
|---|---|
| distinct `unlogged_change` paths before | 84 |
| distinct `unlogged_change` paths after | 84 |
| paths present before and absent after | **0** |
| sequence numbers after | `1..162`, contiguous |
| last event | `session_end`, outcome `worked` |

The two sweeps named the same paths because both swept the same tree, so
deduplication removes a duplicate record and no record.

**One thing is not recoverable and is not claimed to be:** the second
`session_end`'s `duration_s`, `next`, and `unlogged_changes` counts were computed
by the run that lost the race. The retained end is the one at seq 162. The
duplicate count is now visible as a gate note rather than as a failure — the
`session_end appears N times` branch — which is the shape the verifier already
distinguishes.

**`verify` still reports the double end as a note, and that is intended.** The
note is the evidence that the repair fired.

## Reproduce

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_event_stream_concurrency -v
tools/origin session verify
```
