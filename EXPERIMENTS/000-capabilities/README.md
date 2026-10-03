# Capability probe

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: sealed
last-verified: 2026-10-03
-->

The initial probe compiles and executes trivial C and Rust programs in a temporary directory, executes Node, records tool versions, checks memory and disk, and issues read-only HTTPS requests to public sources. Raw results: `results.json`.

This verifies basic execution and public HTTP access only. It does not demonstrate GPU availability, cloud provisioning, authenticated GitHub writes, Docker daemon permissions, long-running unattended inference, or unlimited compute.

Authentication checks inspect only whether GH_TOKEN/GITHUB_TOKEN environment variables exist, not their contents. Other credential methods are untested. Missing CLI or environment tokens do not establish that all GitHub authentication is unavailable.
