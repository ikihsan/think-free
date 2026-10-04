<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Failures — recorded findings, part 3 (F013 onwards)

Continues [`FAILURES-findings-2.md`](FAILURES-findings-2.md), which holds
F009–F012 and reached the 300-line cap at F013. **Identifiers are stable across
all three files**: a reference to `F012` means the same entry wherever it
appears. New findings are appended here.

**The invariant is unchanged by the split.** Findings are separated from
`FAILURES.md`'s live list because a reader must be able to tell a disproved
claim from a still-open question. The files split by line cap, not by subject:
part 1 holds F001–F008, part 2 F009–F012, part 3 the rest. F014 and F015 were
written on a second VM while this file was being written on the first, and were
renumbered into place when both branches landed; `STATE.md` records the collision
and what it cost.

## F013 — Three mission records were committed with conflict markers, and every gate passed

Source: T-0021, commit `fd7b4a1`, repaired in `FAILURES.md`, `FAILURES-findings-2.md`,
and `DECISIONS-GATING.md`. Rule: `tools/originlib/conflicts.py`, doc lint rule 6.

**What happened.** The third identifier collision of 2026-10-03 was renumbered by
hand while a rebase was in progress, and the commit went out with `<<<<<<< HEAD`
still in three mission records. `FAILURES.md` and `FAILURES-findings-2.md` each
held a complete block; `DECISIONS-GATING.md` held one block plus a terminator
left behind with nothing open. F011 and F012 were ambiguous exactly where the
markers sat: the renumber had deleted an F011 that had meanwhile become a
different VM's finding, so the "empty" side of the conflict was wrong and the
records were unreadable in the region that decides what is disproved.

**Why every gate passed.** `doc lint` checked line counts, metadata, links,
orphans, and generated-file drift — never whether the *text* was a resolved file.
`session verify` checks the event stream. `skills verify` checks vendored
hashes. Reconciliation compares trees, not content. A marker is a content defect
in files that every existing rule reads for a different reason.

**Fix and its falsification.** The repair keeps both sides of all three regions,
because both sides carried distinct claims (F011 and F012 are different
findings). The gate is `doc lint` rule 6: exactly seven `<`, `|` or `>` at
column 0 opens or closes a block, a seven-character `=` divider belongs to a
block only when one is open, and a block is reported once at its opening line. A
file may declare `origin-allow-conflict-markers`, reported as `info` so a waiver
is never silent.

**The rule was wrong before it was right.** The first implementation reported
only *malformed* blocks. Run against the three historical files it found one
defect out of four, because a well-formed `<<<<<<< / ======= / >>>>>>>` triple
is exactly what a committed unresolved conflict looks like. The kill gate — scan
the pre-fix bytes, require a finding per defect — is what caught it. Same clause
shape as D024: the gate clause was implemented as a weaker proxy.

**Classification.** Record-keeping defect, found by reading the base branch
rather than by a gate. Fourth collision of the evening, and the first one whose
damage outlived the session that caused it.

**Lesson kept.** A gate that checks structure cannot catch a structural mistake
in content, and a repair performed by hand during a rebase is the highest-risk
edit in the repository. What made this survivable was that the markers were
still text: nothing had been lost, only made ambiguous.

## F014 — The documented VM sequence was impossible, and refusals printed tracebacks

**What failed.** `docs/operations/vm-execution.md` §3 tells a VM to
`task claim` and then `worktree add`. Observed 2026-10-03: the second command
refused, because `worktree.add` rejected *any* claim, including the one the same
VM had just published. The isolation step of the whole fleet flow could not be
reached by following the document that specifies it.

**Second defect, same command.** `worktree.WorktreeError` and `sync.SyncError`
were not in `cli.main`'s handlers, so the refusal escaped as a Python traceback.
The exit status was `1` by accident of an uncaught exception rather than by the
documented contract, and a caller could not distinguish a refusal from a crash.

**Consequence.** Two agents following the documentation on one VM: one keeps
working in the shared tree (the isolation the docs call "the thing that removes
the collision at the filesystem level" never happens), the other is deterred.
Nothing detected either state; the refusal is an exit code and a stack trace,
which is exactly the output nobody pastes into a bug report.

**Fix.** `worktree.add` refuses only a claim held by a *different* VM. The VM is
the right unit of isolation: two agents on one machine already share a working
tree, a git index, and one `sessions/active.json`, which is the collision
`worktree` exists to remove. A claim with no recorded VM is still refused, since
an unattributable claim cannot be shown to be ours. `cli.main` now maps both
errors to exit `1` with one stderr line. Tests in `tests/test_fleet.py`: a claim
from another VM is still refused, a claim from this VM is accepted, and the CLI
returns `1` with no traceback.

**Classification.** Documentation and implementation disagreed, and the
implementation's error path was unhandled. Both found by following the
documented sequence rather than by reading it.

**Lesson kept.** A procedure nobody has executed end to end is a description,
not a contract. `worktree add` had been exercised in the fleet tests only
*before* a claim existed, so the two features had never met.

## F015 — The local and remote views of a task's holder disagreed after every takeover

**What failed.** `tasks.active_claims()` opened a claim only for the ledger
action `claim`, while `taskremote.remote_active()` opened it for `claim` **or**
`takeover`. A takeover is how this fleet legally takes a dead VM's work, and
after one the local view reported no holder while the remote view reported the
new holder.

**Consequence.** Two views of the same file disagreeing is worse than one wrong
view: `tasks/INDEX.md` and `task list` printed a holder that a fetched
`task list --remote` contradicted, so a reader could not tell which was true. It
also matters mechanically — the in-flight classification added by T-0020 reads the
ledger to decide whether an unfinished session is still being worked on, and an
ignored takeover would have made a legitimately re-claimed task look abandoned.

**Fix.** `active_claims()` honours `takeover`, matching the remote view, and the
behaviour is pinned by a test that appends `release` then `takeover` and asserts
the claim is still in force locally.

**Classification.** Implementation defect, duplicated logic in two places with
no shared definition. The two functions had drifted because nothing compared
them.

**Lesson kept.** When two modules answer the same question from the same file,
one of them must call the other.
## F016 — A falsification harness overwrote this VM's real `~/.gitconfig`

Source: T-0025, session `2026-10-03-040`, 2026-10-04. Guard:
`tests/pushcred_fixture.py` and `tests/test_pushcred_safety.py`.

**What happened.** The falsification harness for the push-credential probe ran
three environments, each meant to get a throwaway `HOME` and its own
`credential.helper` config. Two of the three cases passed `Path.home()` as that
sandbox. The harness then wrote its own `.gitconfig` into it, which overwrote
`/home/ubuntu/.gitconfig`: `user.name`, `user.email`, and the real
`credential.helper` were replaced by a helper line pointing at a file that does
not exist. `git commit` stopped working on the machine with *"Please tell me who
you are"*.

Repaired in the same session from values read earlier in it — the bot identity
was confirmed against the 125 committed commits that carry it — and verified by
`git credential fill` returning exit 0 with four fields. No secret was lost: the
key file and helper live under `~/.config/github-app/` and were untouched.

**Why it is a finding and not a note.** The damage was to machine state outside
the repository, in a file no gate watches, from a tool whose whole purpose was
to be safe. It is the same shape as F004, where a directory sweep declared build
output as artifacts: an operation that writes somewhere it was not pointed. The
difference is severity — F004 polluted a record, F016 broke the machine — and the
correction is the same. **A sweep must be unable to address anything outside its
own sandbox, and that has to be enforced rather than remembered.**

**What it also falsified.** My first reading of an unrelated error — git
reporting `invalid credential line: eyJ…` from `git credential fill` — was that
the App's credential helper was incompatible with git's protocol. That was
wrong. The corrupted gitconfig had pointed `credential.helper` at
`/tmp/github-app-jwt.sh`, a JWT *generator*, not a credential helper, which is
exactly what produced the warning. A diagnosis made in a broken environment is
not evidence about the code.

**Lesson kept.** The harness now refuses to run if any case's HOME resolves
outside its own directory, and every test fixture builds its paths inside a
sandbox. A related fixture defect surfaced the same morning: a test naming
`/tmp/github-app-jwt.sh` passed on this VM for the wrong reason, because that
file happens to exist here. **A fixture that names a real path is a fixture whose
result the machine decides.**

## F017 — A generated file's date came from the clock, so the docs gate failed at midnight

Source: T-0025, session `2026-10-03-040`, 2026-10-04. Repair:
`tools/originlib/report.py`, `tools/originlib/docindex.py`,
`tools/originlib/tasks.py`; tests in `tests/test_cli.py` (`GeneratedStampTest`).

**What happened.** Running `doc index` on 2026-10-04 rewrote **thirty-five**
session reports, every one for the same single reason: their `last-verified` had
advanced from `2026-10-03` to `2026-10-04`. `report._meta`, `docindex.render`,
and `tasks.render_tasks_index` all stamped `events.now_iso()[:10]`.

**Why that is a defect and not cosmetics.** `doc lint` fails when a committed
generated file differs from what the generator produces now — that check is the
point of the rule. A clock-derived stamp therefore means the documentation gate
fails at 00:05 on a repository nobody has changed, in CI, for a reason with no
connection to the commit under test. The green CI run this repository can point
to (`37157528596`) happened to execute on the same day its commit was made, so
nothing had caught it. It is the same shape as F010: a gate whose outcome is
decided by something other than what it claims to measure.

**Repair.** Every stamp is now a function of the record it summarises:
`report.session_date` uses the session's own last event, `docindex._stamp` uses
the newest `last-verified` among the documents being indexed (excluding itself,
so the index cannot date itself from its own previous output), and
`tasks._stamp` uses the newest date in the task files or the claim ledger. Each
keeps the clock only as a fallback for an empty repository, where there is
nothing to derive from.

**Lesson kept.** A generated file's metadata must be a function of its inputs.
Where it is a function of the clock, the staleness check stops measuring staleness
and starts measuring the time of day — and it does so silently, because the file
looks updated. The corollary is worth stating for any future generator: a test
must be able to render the same inputs on two different days and get the same
bytes. `GeneratedStampTest` does exactly that, with a session dated three days
before the run.

## F018 — A gate in the suite asserted a fact about the record, so the suite failed on every interpreter nobody had run

Source: T-0034, session `2026-10-04-012`, 2026-10-04. Repair:
`tests/test_doctor_versions.py`; the coupling it was missing is now enforced by
`tests/test_ci_matrix.py`.

**What happened, `observed`.** The suite was run on five CPython builds that no
VM here has installed — 3.9.23, 3.10.18, 3.11.13, 3.13.7 and 3.14.2, portable
builds unpacked outside the repository. On **all five** it failed, with exactly
one failure and no errors: `RealRecordTest.test_the_reported_scope_names_this_suites_size`
in `test_doctor_versions.py`, a file written hours earlier in T-0033. On 3.8.10
(this VM) and on CI's 3.12 the same suite is green.

**Why that is a defect and not a version incompatibility.** The assertion was

```python
match = versions.compare("python3", versions.extract_version(platform.python_version()))
self.assertRegex(match.scope, r"\d+ tests")
```

which requires *this* interpreter to appear in `tests/python-versions.json`. The
record's own `not_exercised` clause named 3.9 to 3.11 as versions nobody had run.
So the suite was red on precisely the versions it had never been run on, and
green only where the record already pointed. No line of `tools/originlib` is
involved: the failure is entirely about the record, and `3.14.2` — newer than
anything this repository has ever named — failed exactly as `3.9.23` did.

**The half that was nearly missed.** The sibling test
`test_this_vms_versions_are_exercised_against_the_real_records` asserts the same
"this interpreter is recorded" claim from a *different* source: `doctor.collect`
probes `python3` from `PATH`. Two tests, one question, two sources, agreeing only
because this VM's `PATH` `python3` is 3.8.10 — the one recorded version available
locally. Running the suite under a downloaded interpreter, where `PATH` and
`sys.executable` disagree, is what separated them.

**Why it was not found sooner, and what it would have caused.** CI pinned one
version, so the question never arose; and that same pin is the entire stated
reason 3.9 to 3.11 were never exercised (`not_exercised[0].why`, verbatim:
*"CI pins a single version"*). Adding a matrix without this repair would have
made five of seven rows red for a reason about the record, and the two available
responses — weaken the assertion, or drop the rows — both reduce measurement. A
gap that rewards the agent for not measuring it is worse than an honest red row.

**The other VM found the same assertion from the other end, an hour later.** Its
CI run `37174050724` was red on this test too, for the mirror-image reason: on a
CI row the interpreter is 3.12, the matched entry is CI's own, and that entry's
scope names a *run id* rather than a test count — so an assertion that had been
green on every VM was red on the only interpreter this repository had evidence
about. Its fix asserted that the reported scope is the matched entry's own text
unchanged, which is a different property from the one it replaced. Both findings
are kept, in `tests/test_doctor_versions.py`, because neither clause catches the
other's failure: the merged test requires every entry to say how much it ran
*and* hands back that text unaltered *and* tolerates an interpreter the record
does not name. Neither VM could have seen the other's failure, which is the
clearest statement yet of the D025 rule this finding is about — a gate that reads
one machine's wording is a gate about one machine.

**Repair.** The test now states the disjunction it can actually support: every
`verified` entry's `scope` names a test count, the comparison returns that
entry's text unchanged, and *this* interpreter either matches an entry or is
reported `unrecorded` with its version named. The record's `3.12` CI entry was
given a count as well as its run id, since the missing count was a real gap in
it. The other coupling — every matrix row is recorded, and nothing a row runs is
still listed as never exercised — is enforced on the two artefacts in
`tests/test_ci_matrix.py`, which is where that property lives.

**Lesson, and it generalises past this repository.** A test that asserts a fact
about a *record* rather than about the *code* is green only on the versions that
record happens to cover. The falsification for such a test is not a mutation of
the code: it is running it on an input the record does not name. That needs no
new tooling — it needs an interpreter, and `python-build-standalone` publishes
one for every minor version at a stable URL.
