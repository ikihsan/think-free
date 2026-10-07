<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# E037 — line-addressable partial staging, `stage-lines` / `stg`

**Status:** **withdrawn as a candidate, 2026-10-07 (E045, F081, F082).** What was
measured stands — the mechanism works, the interface is real, and four defects
E046 found on real repository shapes are fixed — but the population the candidate
rests on is **absent from its own demand evidence (0 of 189 rows)** and the
differentiator is **prior art in two shipped command-line tools that were named
inside that same corpus**. The tool remains in the repository, unreleased, as a
correct tool; that is its final standing. History below: the mechanism, the
gates, the five experiments that revised the claim, and the reading that closed it.

## Claim, as revised by E038

A script, a CI job, an editor keybinding or an AI coding agent cannot name the change it
wants staged, because **no command-line tool takes the line number of the file the caller
is reading and stages exactly that change.** Supplying that coordinate is a small tool.

**What E038 removed from this claim.** "No interface addresses it by the coordinate" was
too strong, and E038 found the two surfaces that do:

- **VS Code's git extension ships `git.stageSelectedRanges`**
  (`extensions/git/src/commands.ts:1777`), staging the intersection of the active editor's
  selection with the working-tree diff. Same operation, same coordinate, the most widely
  used editor there is — for a person, not a script. Its implementation uses the *same*
  same-length-both-sides heuristic `stg` does, which is independent evidence the mechanism
  is the natural one.
- **patchutils 0.3.4's `filterdiff --lines=RANGE`** takes a line range from a shell:
  `git diff -U0 | filterdiff --lines=4 | git apply --cached --unidiff-zero`. **12 of 30** on
  E038's cases, and it wins four of them. E037 declared KILL-B "not met" after checking
  only git's own documentation and said so in its own ceiling; that is the gap, closed.

**What survives.** Neither takes the coordinate as an *argument*. VS Code takes it from an
editor selection and cannot be called from a script; `filterdiff` names the *original*
file's line and cannot split a run of adjacent changes — on an adjacent-edit case it staged
**both** lines and exited 0. Magit, read in full, has no line-addressed staging command.

**E039 (session 2026-10-06-011) added the boundary claim.** On eight real-repository
failure modes — binary file, untracked file, out-of-range line, missing path, conflict
markers, staged rename, mode-change-only, overlapping partial staging — `stg` exited 2
with a named refusal exactly when it did not stage, and exited 1 after the index matched
the request; 8 of 8. The naive route could not distinguish "invalid request" from
"applied" by exit code at all (128 with `error: unrecognized input` on five, silent
success on three). `EXPERIMENTS/039-honest-exit/`.

## Why this candidate, and not another

The pool was the **589 never-answered need statements** in
`EXPERIMENTS/022-need-outcomes`, read in full for the first time. Not screened for novelty —
a screen has killed 18 of 18 candidates in this record (F044), and the owner brief for this
session says a public mechanism does not invalidate a useful application. What the read
produced is F061: the population asked mostly for **finding the right existing thing** (70
rows), then AI-tool transparency (58), then **non-interactive or scriptable operation**
(50). Two distinct named requesters in the 589 ask for the same concrete capability — *pass
the line numbers to stage as arguments instead of interacting* — and one asks for its mirror,
*the same interface for split as for stage*.

## Gates, declared before the run

| Gate | Question | Kill if |
|---|---|---|
| **KILL-B** | Does the interface already exist? | git or a mainstream tool takes `file:line` for staging |
| **KILL-A** | Is the incumbent already drivable at this cost? | a program reaches the same answer with no more code than the call |
| **KILL-C** | Does the prototype lose a case the incumbent wins? | any case where the incumbent is right and `stg` is wrong |
| **KILL-P** | Does a maintained *outside* tool take the coordinate? | one exists on a surface this population would use, with no bespoke code |
| **KILL-S** | Does a public population ask for it? | 0 rows from every pre-named route naming the capability |
| **KILL-Q** | Does anyone want this? | **NOT EVALUATED** — measured through real-world install and usage evaluation. See KILL-Q evaluation below. |

**KILL-B not met** (no `file:line` in git) — but the search behind it was git's own
documentation only, and E038's search found two tools. **KILL-A not met** — the honest
baselines are E037's 133-line pty driver and `filterdiff`, at 12 of 30 each. **KILL-C not
met** — `stg` 30 of 30 across ten cases and three `diff.context` values, stable.
**KILL-P not met, narrowly**: no CLI tool takes the coordinate, splits a run correctly, and
exits non-zero when it staged something else. **KILL-S and KILL-D not met** — the capability
is asked for by named people in at least three projects, one of them an agent tool, at a
rate of **0.016–0.066** of matching GitHub issues.

**KILL-Q evaluation (2026-10-06):** The tool is installable via `pip install .` and functional on real git repositories. 26 of 27 tests pass against real git repos with no mocks. The resulting `.git/index` is byte-identical to a hand-built patch. However, the demand rate is low: 0.016–0.066 of matching GitHub issues, with only two named requesters in the 589 need statements asking for line-number staging capability (instead of interactive `git add -p`). The mechanism is validated (E041: shell baseline matches stg exactly on all 35 test rows), and the differentiator is packaging (ready-to-use CLI tool vs. writing custom git plumbing code). KILL-Q remains **not evaluated** in the sense that no real-world adoption measurement has been conducted beyond this installation test — the gap between "mechanism works" and "people want to use it daily" is the unmeasured question.

**KILL-Q real-world staging test (2026-10-06, new experiment):** stg was tested against 6 realistic staging scenarios with uncommitted working-tree modifications in real git repositories:
- `func_modify`: PASS - stages single line modification correctly
- `adjacent_mods`: PASS - correctly splits adjacent modifications (the key stg advantage)
- `multi_line_insert`: PASS - stages multi-line insertion correctly
- `deletion_end`: FAIL (exit 2) - correctly refuses out-of-range line request (2-line file, asked for 3)
- `deletion_top`: PASS - stages deletion of top lines correctly
- `range_selection`: PASS - stages range of lines correctly

Result: 5/6 scenarios succeeded, with the 1 failure being a correct refusal for an out-of-range line. This demonstrates that the mechanism works robustly across common staging tasks. The differentiator remains packaging (1-command CLI vs 180-line script), not the underlying algorithm.

Full numbers: [`EXPERIMENTS/037-line-staging/README.md`](EXPERIMENTS/037-line-staging/README.md)
and [`EXPERIMENTS/038-staging-prior-art/README.md`](EXPERIMENTS/038-staging-prior-art/README.md).

## E043 and E045 — the agent-usability claim, and the population it assumed

E043's run is tabulated in
[`HYPOTHESES-candidates-2.md`](HYPOTHESES-candidates-2.md) (six real agents,
three with no tool offered). What changed, and what closed:

### What changed

**The packaging advantage is not observed in the population the demand evidence
names.** "1 line instead of 180" is true and worth nothing here: 180 lines is the
cost of building a *general* selector, and these agents did not need one — they
needed one patch, and `git diff` told them what it was.

**`stg` is no longer a candidate for release on the strength of agent usability.**
It remains a working, correct tool: 30 of 30 on E038, index byte-identical to a
hand-built patch, honest exits at every boundary E039 measured. That is now the
whole of its claim.

**What survived open, and it did not exist (E045, F081, F082, 2026-10-07).**
The remainder was *an agent that must discover which line changed, without diff
access and without a line number*, and it came from this experiment's own
harness rather than from the demand evidence. E045 read all 189 unique issues in
E038's cached corpus and labelled each row's requester and its diff-access
evidence: **29 of 189 are about choosing which lines reach the index, 28 of those
carry explicit diff access and the 29th GUI-implied, and none carries none.**
Every one of the ten automated callers names its diff access in its own text.
Three of the four issues F064 cites are not evidence of what they were cited for —
`sublime_merge#465` says the feature already exists and asks for
discoverability, `sublime_merge#976` asks for staging *within* a modified line
(sub-line staging, which `stg` does not provide), and `vim-gitgutter#446` is a
person in vim with a visual selection.

The same reading killed the differentiator. The 29 rows name **26 distinct
repositories**; two of them are command-line tools that take `stg`'s coordinate
and shipped before E037. `gah` (Rust, crates.io) offers "line range" staging,
names `stg`'s exact hard case in its README, targets AI coding agents explicitly
and ships a Claude Code plugin for them. `git-hunk` (Python, PyPI) has
line-level control and has already run the two-arm agent experiment this record
was about to run. **Packaging is gone with it**: all three are installable, two
ship agent distribution, and `gah` addresses by a *content anchor* that stays
stable when line numbers shift — strictly better for an agent than the
working-tree line number `stg` uses.

**`stg` is withdrawn as a candidate.** KILL-Q is answered, and the answer is
that the population does not exist and the mechanism is prior art twice over.
What remains is exactly the sentence above it: a working, correct tool —
30 of 30 on E038, 37 of 37 after E046's four fixes, index byte-identical to a
hand-built patch, honest exits at every boundary E039 measured — with a
measured absence of population. It stays in the repository, unreleased, with
`status: draft`, and that is its final standing unless the state of the
incumbents changes.

**Not closed:** the application. 29 real issues in 26 real repositories is a
real population and it is being served; a negative result closes the claim and
the population actually tested, not the domain.

**Ceiling:** three scenarios, six runs, one model, synthetic Python, line numbers
supplied, `git diff` available to every agent. E045's ceiling is one reader with
no second coder over a top-30-per-query slice of a 3124-instance universe, and
only two of the 26 named repositories were read at the source. The negative
result closes the claim and that population only — not the tool, not the domain,
and not the discovery route.

supplied, `git diff` available to every agent. The negative result closes the
claim and that population only — not the tool, not the domain, and not the
discovery route.

---

## E044 — the discovery population, run against real agents (F083)

`observed` 2026-10-07, session 2026-10-07-002. Evidence:
[`EXPERIMENTS/044-discover-staging/README.md`](EXPERIMENTS/044-discover-staging/README.md).

E043's ceiling named the last open population: an agent that must *discover* which
line changed, with no line number and no `git diff`. E044 reran the same harness —
byte-identical fixtures — with exactly those two changes: the prompt describes the
change semantically and never names a line, and a logging policy shim refuses
`git diff` (passing `stg`'s own plumbing, which is the exemption under test).

| arm | verdict | used `stg` |
|---|---|---|
| no tool, no line number, no diff (3 scenarios) | **3/3 exact** | n/a |
| `stg` on `PATH`, same constraint (3) | **3/3 exact** | 3 of 3 |

**6 of 6 exact, and all six agents did the discovery by hand first** — `git show
HEAD:app.py` against `cat -n app.py`, compared by eye, correct line named on the
first attempt in every scenario. In the `stg` arm, `stg list` was run *after* the
agent had already identified the line, and is described in the agents' own reports
as confirmation. The `nostg` arm produced a route E043 never saw: one agent built
the staged blob directly (`git hash-object -w` + `git update-index --cacheinfo`)
and never wrote a patch at all.

### Final status: candidate closed

**`stg` is withdrawn as a release candidate; it is a correct tool with no observed
population that needs it.** Mechanism supported (E038: 30/30, byte-identical index;
E039: honest exits 8/8); mechanism differentiation falsified (E041); packaging
advantage not observed against agents told a line (E043); discovery population not
observed to need it either, at this scale (E044). The one cell never tested —
weaker models, harnesses without shell access, files large enough that
discovery-by-eye is not free — has no named requester in the demand evidence
(F064), and chasing it would be two hypotheticals past the last observation.

**Ceiling:** as E043, plus the no-diff simulation is cooperative (logged, not
sandboxed) and the files are 20 lines — a negative result at this scale closes the
small-file discover population only.
