# EXPERIMENTS/018 — runtime signal selection over one annotation

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Date:** 2026-10-05. E016's lead 7 (`runtime-instrumentation`) reduced to its
mechanism question (D050): *is there an interposition point that sees the code
path and can select a signal per path, or is the choice always made at
instrumentation time?* This experiment answers that question twice: against
the stock OpenTelemetry SDK, and against a minimal prototype of what the need
asks for.

## Hypothesis and kill gate

- H1: the stock OTel Python SDK cannot, at runtime and per path, switch what an
  annotated call emits between metric, log and trace. Prediction: only
  instrumentation-time choices exist (sampler, processor list, provider
  wiring), and there is no remove/disable for a span processor.
- H2: the need's exact semantics — one annotation, per-call runtime choice of
  emitted signal — is implementable in a few dozen lines around a decorator,
  with the choice variable read on every call.
- Kill gate for the *candidate* reading: if H1 fails (stock OTel runtime does
  it), the need is served and lead 7 dies. If H2 fails (not implementable as
  stated), the need is speculative. Utility is **not** measured here.

## Environment

- Python 3.8.10, pip 20.0.2.
- `pip3 install --target /tmp/opencode/otelpkg opentelemetry-sdk opentelemetry-api`
  → `opentelemetry_sdk-1.33.1-py3-none-any.whl` (observed wheel download
  2026-10-05). The target directory is volatile; the command reproduces it.

## Run

    PYTHONPATH=/tmp/opencode/otelpkg tools/x -- python3 EXPERIMENTS/018-runtime-signal-selection/otel_probe.py
    tools/x -- python3 EXPERIMENTS/018-runtime-signal-selection/sigsel.py

## Raw results

See [`results.json`](results.json) for the probe record and the prototype's
pass/fail. `sigsel.py --run` prints the observed emission sequence; the
assertions in the same file fail loudly on any mismatch.

## Limits

- One SDK language version (Python 1.33.1); other languages may differ.
- The collector tail-sampling README was read from GitHub `main` on
  2026-10-05: it keeps/drops whole traces by policy; it does not choose
  metric-vs-log-vs-trace per path. `source-supported`, one revision.
- Nothing here measures usefulness, adoption, or overhead.
