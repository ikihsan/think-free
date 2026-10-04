<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0040
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0040 — Make a red doc lint, release check or skills gate step annotate the fi

## Goal

Make a red doc lint, release check or skills gate step annotate the file it rejected

## Why this matters

FAILURES.md F020 measured it from the public API: the Tests step emits ::error:: lines and its annotations are public, but Documentation lint and Release manifest print no ::error:: at all, and the session step emits ::warning:: only for in-flight sessions, which is not what fails it. So a red doc lint on a pushed commit names a step and nothing else - run 37180487906 (a stale session report) and the four runs of defect 4 (37163434868 and later) were all diagnosed by elimination or by rebuilding a tree on a VM, not by reading the run. docs/operations/ci-diagnosis.md gives the four answers the endpoint can give and says the general form is D030: a diagnostic must distinguish never-configured from stopped-working. Here three of the five gate steps answer nothing at all, and the workflow's own emission is what would have answered.

## Preconditions

origin/research/origin has defect 11 open (T-0039, claimed on instance-20260717-0947): task new keeps only the last --steps and --acceptance, so this task passes each exactly once, as one multi-line string, and says so here.

## Steps

The claim, in one sentence with its scope: for every violation the five file-reading gates report, tools/origin annotate emits one GitHub workflow command naming the violating file, and emits none at all on a tree every gate accepts. Baseline, named: the awk window in the workflow's own Tests step, which is the strongest existing implementation of the same idea in this repository and is proven on a real run (37178057818 carried 11 annotations). It escapes percent and strips CR, and it has no file or line property; the renderer must match it on escaping and add the location, without changing what the Tests step does.

## Acceptance criteria

Kill gate, fixed before observing: on the real tree of commit e53ca23 - the duplicate defect 7 that reached the shared base and that T-0036 already extracted - the renderer must emit at least one ::error naming STATE-defects.md. If it emits none, or emits one without file=, the mechanism is dead and the task is cancelled rather than reworked. Second half of the same gate: the CI step's present command, tools/origin doc lint, run on that same tree must emit zero ::error:: lines, measured and kept, because the whole claim is that it emits none today.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Ceiling, declared now rather than discovered: annotations are the workflow's own emission and GitHub renders them, so nothing here proves a conclusion - it names a file. The Tests step keeps its awk. The cap is the 60 lines the awk already uses; the platform's own limit was not measured.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
