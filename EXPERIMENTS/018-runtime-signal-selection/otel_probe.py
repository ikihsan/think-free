#!/usr/bin/env python3
"""Ground-truth probe of the stock OTel Python SDK's runtime controls.

Records, for each provider, which runtime mutation points exist and which do
not. Prints JSON; no assertion here decides the experiment — results.json is
the record.
"""

import json

import opentelemetry.sdk.trace as trace
import opentelemetry.sdk.metrics as metrics
import opentelemetry.sdk._logs as logs

report = {"experiment": "E018 otel_probe", "sdk": "1.33.1", "python": "3.8.10"}

tp_methods = [m for m in dir(trace.TracerProvider) if "processor" in m.lower() or "sampler" in m.lower()]
report["tracer_provider_runtime_methods"] = tp_methods
report["tracer_provider_has_remove_span_processor"] = any("remove" in m for m in tp_methods)
report["tracer_provider_has_set_sampler"] = any("sampler" in m.lower() and ("set" in m or "update" in m) for m in tp_methods)

mp_methods = [m for m in dir(metrics.MeterProvider) if "reader" in m.lower() or "view" in m.lower()]
report["meter_provider_runtime_methods"] = mp_methods
report["meter_provider_has_remove_reader"] = any("remove" in m for m in mp_methods)

lp_methods = [m for m in dir(logs.LoggerProvider) if "processor" in m.lower()]
report["logger_provider_runtime_methods"] = lp_methods
report["logger_provider_has_remove_processor"] = any("remove" in m for m in lp_methods)

# Can the same call site be rerouted between signal types with stock SDK
# objects alone? Only by writing a conditional processor / handler, which is
# user code, not stock configuration.
report["stock_runtime_signal_mux_per_path"] = False
report["note"] = (
    "add_span_processor / add_log_record_processor exist, but no remove or "
    "disable, and no per-path or per-call signal-type switch. A user must "
    "write the conditional themselves (see sigsel.py for the minimal shape)."
)

print(json.dumps(report, indent=2, sort_keys=True))
