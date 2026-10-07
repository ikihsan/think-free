<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# In flight, part 5 — E043/E044, the candidate's last two claims against real agents — **closed**

Split out of [`STATE.md`](STATE.md) on 2026-10-07 at its 300-line cap, by invariant:
this is one candidate's complete reading and its successor's correction, which is
what `STATE-in-flight-3.md` holds for E034. **Identifiers are stable across the
parts.** Read a finding number and go to the file it is defined in — F075 is in
[`FAILURES-findings-29.md`](FAILURES-findings-29.md), D074 in
[`DECISIONS-SCREENING-11.md`](DECISIONS-SCREENING-11.md), and the full
protocol in [`EXPERIMENTS/043-real-agent-staging/`](EXPERIMENTS/043-real-agent-staging/README.md).

## The packaging advantage was priced against a simulation (E043, F075, D074)

`observed` 2026-10-07, session 2026-10-07-001, VM `instance-20260717-0944`, git
2.25.1, Python 3.8.10. Six real agent runs.

**What the candidate was resting on.** `stg` lost its mechanism three times over
(F062 prior art, E041 parity, E038's stronger oracle finding two real bugs) and
kept a life on one claim: the differentiator is *packaging* — a caller writes 1
line instead of ~180. E040, E041 and E042 each measured that claim. None of them
ran a caller. E042's design document, line 38: *"Since we can't run a real coding
agent, we simulate the agent's decision process."* And the ~180 figure descends
from `shell_baseline.py`, a baseline written by someone who had already read
`stg`'s selector and reimplemented it.

**What was run.** Six real agents, six real repositories, one committed `app.py`
with a real dirty working tree, and the instruction *"stage ONLY the change on
line N; leave every other change unstaged. Do not commit."* Two arms: no tool
offered, and `stg` genuinely on `PATH` and named in the prompt as available and
not required. Three scenarios — two adjacent modified lines (ask for the second),
two adjacent inserted lines (ask for the first), and one edit among three
scattered (ask for it).

**The oracle is independent and was checked before any agent ran.** The expected
index content is written by hand in `build.py` from each scenario's description,
hoisted outside every trial directory so no agent can diff against it, and the
scorer was validated on four routes × three scenarios: `stage-all` → `wrong`,
`stage-none` → `wrong`, a hand-rolled `diff-filter` → `wrong` on both adjacent
cases and `exact` on the easy one, `stg` → `exact` on all three.

### Observed

| arm | exact | used `stg` |
|---|---|---|
| no tool offered | **3/3** | n/a |
| `stg` on `PATH` | **3/3** | **1 of 3** |

**6 of 6 exact.** No trial committed, none left a stray file, all left the other
changes unstaged. Every `nostg` agent independently converged on the same route
without being told: `git diff`, hand-write a minimal patch, `git apply --cached`.
One call each, no code written. Three of six dry-ran first; two of the three
that wrote a patch file hit patch-malformedness and were caught by their own
check. Two agents independently flagged that `git apply` is all-or-nothing, so a
bad hunk header is a hard error rather than a silent partial stage.

### What this closes

**The packaging advantage is not observed in the population the demand evidence
names.** `mcp-multi-root-git#3` asks for "no way to stage lines 1-50
separately"; that caller had a non-interactive route available and used it, 3 of
3. **"1 line instead of 180" is true and worth nothing here: 180 lines is the
cost of building a *general* selector, and these agents did not need one** — they
needed one patch, and `git diff` told them what it was. Three consecutive
experiments agreed with each other because they shared a premise, not because
the premise held.

**`stg` is no longer a candidate for release on the strength of agent
usability.** It remains a working, correct tool — 30 of 30 on E038, index
byte-identical to a hand-built patch, honest exits at all eight boundaries E039
measured — and that is the whole of its claim now.

### What survives open, and it is named

An agent that must **discover which line changed**, without diff access and
without a line number being supplied. That is the population where a
line-addressed interface could still pay, it is untested, and it is a two-arm
rerun of this harness rather than a new line of work. The negative result closes
the claim and the population actually tested — not the tool, not the domain, and
not the discovery route.

### The arm that was not exercising the tool

`stg` was written into an untracked `.bin/` inside the fixture. All three agents
in that arm reported `stg: command not found`, so the arm was a second `nostg`
arm — **and the run still scored 6 of 6, which would have been recorded as
confirmation of the candidate.** F073's shape, and the first control here to fail
*open* rather than producing a visible zero. The harness now refuses to emit a
trial unless `stg --help` resolves.

A second defect, in the scorer rather than the arm: `git show :app.py` succeeds
and returns `HEAD`'s content when nothing is staged, so "staged nothing" and
"staged the wrong thing" collapsed into one verdict. Three untouched
repositories scored `wrong`, which would have reported a 3-of-6 failure that
never happened. Found by scoring fixtures no agent had touched and asking why an
untouched repository scored as a wrong answer.

A third, caught by the agents' own honesty: in the first pass the oracle file sat
inside the trial directory, and one agent verified its work by diffing against
it. That run scored `exact` and was not evidence; it was discarded.

### Ceiling

Three scenarios, six runs, one agent model, one session, synthetic Python, line
numbers supplied in the prompt, and `git diff` available to every agent. Agent
heterogeneity — weaker models, or harnesses that forbid shell heredocs — is
untested and is the most plausible place `stg` still wins. An agent with only an
edit tool and no diff access is a different population and is untested. The
oracle was verified to discriminate on four routes but not against a second
independent reader.

## The discovery population doesn't need it either (E044, F083, D078)

`observed` 2026-10-07, session 2026-10-07-002, same VM. Six real agent runs.
Protocol: [`EXPERIMENTS/044-discover-staging/`](EXPERIMENTS/044-discover-staging/README.md).

The population named above was run: byte-identical fixtures, but the prompt
describes the change semantically and never names a line, and a logging policy
shim on `PATH` refuses `git diff` (passing `stg`'s own plumbing — the
candidate's exemption from the agent's restriction is the hypothesis under
test). Kill gate declared before the runs: `nostg` ≥ 2 of 3 exact kills the
claim. The oracle was checked first on four routes × three scenarios,
including a no-diff difflib route proving every fixture solvable from file
contents alone.

| arm | exact | used `stg` |
|---|---|---|
| no tool, no line number, no diff | **3/3** | n/a |
| `stg` on `PATH`, same constraint | **3/3** | 3 of 3 |

**6 of 6 exact — and every agent in both arms did the discovery by hand
first**: `git show HEAD:app.py` against `cat -n app.py`, compared by eye,
correct line on the first attempt in all six. In the `stg` arm all three
agents used the tool this time, and all three reports describe `stg list` as
*confirming* a line they had already identified — the coordinate listing
answered a question they had already answered. The `nostg` arm added a route
no experiment here had seen: `git hash-object -w` +
`git update-index --cacheinfo`, staging the intended blob with no patch at
all.

**The candidate is closed.** Every population the demand evidence or any
experiment's ceiling named is tested and negative: not agents told a line
(E043), not agents who must discover it without diff, at this scale (E044).
`stg` is a correct tool — 30/30 on E038, exact whenever used in both real
harnesses — with no observed population that needs it. The untested cells
(weaker models, no-shell harnesses, files too large for discovery-by-eye)
have no named requester in F064's demand evidence.

**The instrument point that generalises (D078).** The shim log shows one
agent-facing `git diff --cached --stat`, refused, in one trial — and that
attempt appears in **no agent's self-report**, though all six reports were
otherwise accurate command-by-command. When a constraint is part of the
treatment, compliance is measured at the enforcement point; the subject's
account of its own compliance is not evidence of it.

## Where the other VM's task files are linked from

[T-0073](tasks/T-0073-test-whether-the-need-staters-who-publicly-shipp.md) and
[T-0083](tasks/T-0083-e045-read-the-demand-evidence-the-candidate.md) were
committed without a hand-authored document naming them, and `doc lint`'s orphan
rule does not count the generated `tasks/INDEX.md` as a link, so this file names
them. Nothing about either task is asserted here; a task file that records its
own goal and verify command does not need a second mention to be findable.
