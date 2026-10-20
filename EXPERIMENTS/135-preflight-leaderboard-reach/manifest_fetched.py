#!/usr/bin/env python3
"""E135: manifest of the fetched third-party bytes, by sha256.

The repository rule (D091/D092) is that third-party bulk input is
recorded by hash and never committed. This manifest lets anyone
re-fetch the same URLs and verify the bytes the recomputation read.
"""
import hashlib
import json
import os

FILES = {
    "helm_scenario_state": (
        "scenario_state.json",
        "https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/runs/v1.0.0/"
        "mmlu:subject=abstract_algebra,method=multiple_choice_joint,model=01-ai_yi-34b/scenario_state.json",
    ),
    "helm_stats": (
        "stats.json",
        "https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/runs/v1.0.0/"
        "mmlu:subject=abstract_algebra,method=multiple_choice_joint,model=01-ai_yi-34b/stats.json",
    ),
    "helm_per_instance_stats": (
        "per_instance_stats.json",
        "https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/runs/v1.0.0/"
        "mmlu:subject=abstract_algebra,method=multiple_choice_joint,model=01-ai_yi-34b/per_instance_stats.json",
    ),
    "helm_run_spec": (
        "run_spec.json",
        "https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/runs/v1.0.0/"
        "mmlu:subject=abstract_algebra,method=multiple_choice_joint,model=01-ai_yi-34b/run_spec.json",
    ),
    "helm.js": (
        "helm.js (HELM site bundle, evidence the site renders from the same GCS bytes)",
        "https://crfm.stanford.edu/helm/helm.js",
    ),
}

manifest = []
for local, (label, url) in FILES.items():
    path = os.path.join("/tmp/opencode", local)
    if not os.path.exists(path):
        manifest.append({"local": local, "url": url, "status": "missing"})
        continue
    blob = open(path, "rb").read()
    manifest.append({
        "local": local,
        "label": label,
        "url": url,
        "bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
        "fetched": "2026-10-14",
    })

print(json.dumps(manifest, indent=1))
with open("/home/ubuntu/think-free/EXPERIMENTS/135-preflight-leaderboard-reach/"
          "fetched-manifest.json", "w") as fh:
    json.dump(manifest, fh, indent=1)
    fh.write("\n")
