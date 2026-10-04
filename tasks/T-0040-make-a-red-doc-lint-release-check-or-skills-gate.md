<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0040
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-020-give-the-file-reading-ci-gate-steps-a-ch
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0040 — Make a red doc lint, release check or skills gate step annotate the file it rejected

## Goal

Make a red doc lint, release check or skills gate step annotate the file it rejected

## Why this matters

`FAILURES.md` F020 measured it from the public API: the `Tests` step emits
`::error::` lines and its annotations are public, but `Documentation lint` and
`Release manifest` printed no `::error::` at all, and the session step emitted
`::warning::` only for in-flight sessions, which is not what fails it. So a red doc
lint on a pushed commit named a step and nothing else — run `37180487906` (a stale
session report) and the four runs of defect 4 (`37163434868` and later) were all
diagnosed by elimination or by rebuilding a tree on a VM, not by reading the run.
`docs/operations/ci-diagnosis.md` gives the four answers the endpoint can give and
says the general form is D030: a diagnostic must distinguish "never configured" from
"stopped working". Three of the five gate steps answered nothing at all, and the
workflow's own emission is what would have answered.

## Preconditions

At the time this task was created, `origin/research/origin` had defect 11 open
(T-0039, claimed on `instance-20260717-0947`): `task new` kept only the last
`--steps` and `--acceptance`. Each flag is therefore passed exactly once, as one
multi-line string. **It bit anyway** — see Notes.

## Steps

1. Measure the baseline first: extract the real tree of `e53ca23` as a git
   worktree and run the present CI command over it.
2. Give a violation the location its own rule knows, as a `str` subclass so every
   existing assertion keeps testing what it was written to test.
3. Render it as a workflow command with the toolkit's escaping, and publish
   `file=`/`line=` only when true.
4. Wire the five gate steps through one command, and fix the awk's escaping.
5. Split `doclint.py` by what a rule may read, because the conversions had nowhere
   to go at 299 of 300 lines.
6. Falsify against the defect's own bytes in both directions, then plant a tree
   with one violation of each shape and run the real command over it.

## Acceptance criteria

- [x] Defect 14 in [`STATE-defects.md`](../STATE-defects.md) is closed with its
      ceiling, and 15 and 16 with theirs — all three found by running the code.
- [x] On `e53ca23`'s real tree the new command emits one `::error` naming
      `STATE-defects.md`, where the present command emits **zero**. On this tip
      both emit none.
- [x] All five file-reading steps run `tools/origin annotate -- <gate>`, and each
      gate keeps its own exit code.
- [x] `tests/test_annotate.py` and `tests/test_ci_annotations.py` hold the
      controls: structured path beats the message, a directory or absent path and
      a line past the end of a file are dropped, `%` is `%25`, a newline cannot
      inject a second command, the cap is announced, a clean tree emits nothing,
      an unread gate or flag is refused with exit 1.
- [x] `docs/operations/ci-diagnosis.md` no longer says a gate step emits nothing,
      and the method, the escaping and the ceiling are in one place.
- [x] The suite is green and `doc lint` exits 0. **Unrun and stated as such:** no
      pushed commit has exercised the annotator, so how GitHub renders one is
      `unmeasured`.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Revert `tools/originlib/annotate.py`, `finding.py`, `doclint_tree.py`, `usage.py`
and the `Finding` conversions together with the five `ci.yml` steps. Reverting one
side alone is the defect: a step that runs a wrapper the wrapper's own gate does not
cover is a red run that names only a step.

## Notes

**The kill gate failed first, which is what it is for.** On `e53ca23`'s tree the
first run emitted `::error::identifier collision: …` with **no** `file=`, because
`check_identifiers` wrapped each line from `idcheck` in a prefix and dropped the
structured path it was carrying. The gate's second half — "or emits one without
`file=`, the mechanism is dead" — is what said so.

**Measured, in this order, all from `commands.log`:**

| Run | Input | Result |
|---|---|---|
| Baseline | `e53ca23`'s tree, the present `doc lint` | 1 violation, exit 2, **0** `::` lines |
| After | the same tree, `annotate -- doc lint` | 1 violation, exit 2, `::error file=STATE-defects.md::…` |
| Tip | this repository | 0 violations, **0** `::` lines |
| Planted | a broken link, a 328-line file, an orphan, a stale index, a conflict marker | six commands; `file=` on all five that name a real file, `line=4` and `line=9` where the rule knows one, `file=docs/INDEX.md` for the whole-file verdict |
| Planted | a `.claude/skills` mirror that is a real directory | `::error::…` with **no** `file=` |
| Planted | a missing generated index | `::error::sessions/INDEX.md: …` with no `file=`, because the file is not there to point at |

**Two more defects came out of running it rather than reading it.** `Finding` is a
`str` subclass, and a three-argument call raised `TypeError` until `__init__` was
defined as well as `__new__` — found by the planted conflict marker. And
`conflicts.py` already had a `Finding` of its own, which shadowed the import by two
lines of file order.

**This task file was truncated on creation, by the defect it names.** The fields
were passed as a shell array built with `mapfile -t`, which splits on **lines**, not
on blank lines, so seven of the twelve paragraphs passed to `task new` were dropped
and the sections landed one field early. The acceptance criteria above were written
afterwards. The repair is the file you are reading; the lesson is the one defect 11
already carries, and it was cheaper here only because this task was about making a
record say what it means.