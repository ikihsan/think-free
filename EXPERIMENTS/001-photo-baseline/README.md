# E001 — Can a simple baseline already explain the photo-migration opportunity?

Status at design: experiment not yet executed. Date: 2026-10-03.

## Question and predeclared decision

Research B proposed an independent photo-migration verifier after finding an import that reports zero errors despite losing originals/edits. Before implementing a semantic auditor, test whether a simple source/destination checksum set difference detects the motivating failure.

**Claim under test:** the published four-image example requires a relationship-aware invention to reveal its missing media.

**Falsifier:** checksum identity alone finds all missing media described in the published trace, without original/edit inference. If so, the example establishes a failure of importer reporting, but does not demonstrate an advantage for a new semantic auditor. Seek a separate real case where all bytes survive and important relationships do not, or park this candidate.

## Evidence and limits

- Primary report: https://github.com/simulot/immich-go/issues/1422
- Fixture/trace branch: https://github.com/gthb/immich-go/tree/issue-repro/edited-pair-files
- Pin the branch commit before execution and record source hashes.
- Read the four generated JPEGs and two metadata sidecars from the public ZIP in memory. Do not open personal archives, extract untrusted paths, or modify an Immich instance.
- Parse successful asset creation and accepted deletion operations in the published trace. This reconstructs an **accepted-operation model**, not the actual asynchronous server state. Compare it with the reporter's final-state description; do not claim independent live reproduction.
- SHA-1 is used only to match the checksum field of the published API trace. It is not proposed as an adversarial integrity primitive. SHA-256 records downloaded artifact integrity.
- Importer logs and traces remain third-party evidence. The only new measurement is the baseline applied to those artifacts.

## Controls

1. Full four-identity destination: no missing identities.
2. Identical bytes with changed filenames: no missing identities; names are not identities.
3. Missing original/edit contents as represented by accepted operations: report the exact missing filenames.
4. Synthetic relationship-only damage with all identities retained: checksum baseline cannot detect it. This limits the baseline; it does not establish prevalence or prove a new checker valuable.

## Execution plan

Implement a bounded standard-library Python runner, download only the pinned small public artifacts, retain result JSON with source URLs/hashes and checks. Network errors and invalid fixture structure must fail, never produce a positive result. No timing benchmark or product usability claim is relevant.

Run from this directory: `python3 run.py`. The experiment will write `results.json`; later independent review should inspect the model assumption and baseline fairness.
