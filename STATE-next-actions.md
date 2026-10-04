<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Next actions and standing constraints

Split out of [`STATE.md`](STATE.md) on 2026-10-04, which was at 299 of the 300
permitted lines and had to grow. The reload point keeps a pointer and the top
item; the reasoning behind each item lives here so that a rewrite of one does
not force a rewrite of the other.

Read the ceiling on an item before spending effort on it. A pass still leaves
prior art, usefulness and adoption untouched, and every item below says which
of those it cannot touch.

## Ordered by information gained per unit of effort

1. **A gate must read the property it claims to check, and must be falsified
   against the defect's own bytes before it is trusted** (D025, from F013). Nine
   gates now work that way, the newest being the rule that holds a restated
   experiment number to its artifact (T-0056, D045, defect 22). Its case is the
   sharpest yet, because the **obvious rule is green on the defect**: "does this
   number occur anywhere in the artifact?" answers *yes* for `113`, which also
   sits at `patch_cost_sensitivity/*/cases`. What settles it is reading the
   number's *shape* rather than the file's contents, and the blindness of the
   rejected rule is now asserted so the restriction cannot be dropped quietly.
   Method: `docs/policy/gate-falsification.md`.
   **Ceiling:** each rule detects only the shape it was written against, and
   `resultnumbers.py`'s is one table row per experiment.
2. **The gaps in that pattern, both found by hitting them — closed, and the
   second found by reading the record rather than by a red run.** (a) **Closed in
   T-0036.** Doc lint rule 7 read findings definitions, findings index rows and
   decision spans, and not the numbered list in
   [`STATE-defects.md`](STATE-defects.md), so T-0034 and T-0035 — written on two
   VMs in the same hour — both took **defect 7** and nothing reported it. Both
   copies reached the shared base (`e53ca23`, `e701ad8`), each VM's own tree
   internally consistent, and the unpushed side renumbered by hand in `157e463`.
   `tools/originlib/defectlist.py` reads the list; `tools/originlib/idcheck.py` is
   the one entry point `doc lint` and `sync land` both call, because a module wired
   into one gate is not thereby read by the other. It also reports a list it cannot
   read, since a parser that stops matching is indistinguishable from a clean tree.
   Falsified against both commits' own bytes: the previous wiring reports nothing on
   either, the new rule names defect 7 with both lines, and neither the repair
   commit nor the tip reports anything.
   **Ceiling:** a repeated number and nothing else. A gap in the numbering is not
   reported — a dropped entry and a withdrawn defect are the same bytes — and there
   is no allocator here, so this is the detection half of a race it cannot prevent.
   (b) **A red CI run names a step and a version, not a test**, and this half is
   settled by item 3, which falsified its premise.
   (c) **Closed in T-0042.** A decision number is written in three places that must
   agree — the `## Dnnn` heading, the index row in [`DECISIONS.md`](DECISIONS.md),
   and the `Decisions **…**` header under each record's title — and only the first
   two had a reader. Two of the five records were false while every gate passed:
   `DECISIONS-GATING.md` named D013, which lives in another file, and omitted
   D030, D032 and D035 of its own; `DECISIONS-PRACTICE.md` named a `D011–D018`
   range covering exactly the three entries that had moved out when T-0030's split
   was reversed. Both index rows were correct throughout, which is what a reader
   checking one source concludes. `tools/originlib/decisionheader.py` reads the
   third, through the same entry point, and reports a header it cannot read.
   Falsified against `d451169`'s own bytes: twelve findings where the previous
   wiring reported **none**, and the repaired tip silent.
   **Ceiling:** identifier sets rather than wording, one line per record, and
   nothing outside `DECISIONS*.md`.
   A third, cheaper observation belongs here: a commit published while a session
   with **no task and no claim** is open is red on the session step, twice in an
   hour on 2026-10-04 (runs `37174316639`, `37181374433`), each green on the next
   commit. D027's predicate can only prove a session alive from a claim, so a
   taskless session has nothing to point at. `docs/operations/ci.md` now says how
   to recognise this case from the run alone, which is the cheap half; the other
   half is whether a taskless session should publish code commits at all.
   **Measured again the same day, twice by one VM, and both times the run said so
   in one line.** Run `37206132901` at `2643c9e` carried
   `…events.jsonl: last event is 'artifact'; session may be unfinished; T-0050 is
   done, no claim names this session`, and run `37206627337` at `1061c5b` carried
   the same shape with `last event is 'command'`. So the case is **five runs in one
   day, three of them from this VM, and every one green on the next commit** — the
   cost is a red row, not a wrong record. **The untested half is the cheap
   question the annotation raises and nobody has answered: the gate names a
   *taskless* session, and could it accept one whose stream says `task: ""` and whose
   ledger holds no claim only when the session is younger than the CI run's queue
   delay?** The information exists in the same event the message already quotes.
   **Ceiling:** none of these closes the general problem; they narrow where a
   hand-maintained identifier list and an unreadable log can hide a defect.
   (d) **Closed in T-0050 (D042, F022).** `reconcile._is_vendored` reused the
   **line-cap** exemption list, which exempts `*.json`, `*.jsonl` and `*.log`, as
   though content the cap ignores were content no session can change silently — so
   `tests/python-versions.json`, `tests/git-versions.json` and `tasks/CLAIMS.jsonl`
   could be edited with nothing declared and nothing reported. `doclint` now splits
   `is_data_suffix` from `is_declared_exempt` and reconciliation reads the second
   only; the ledger and `vendor/hashes.json` are declared by the bytes their writers
   wrote. Priced first, by `tools/sweep_unlogged_data.py`: **72 (session, path) pairs
   over 17 paths** across 77 closed sessions, 50 of them the ledger. **Ceiling:** the
   repair is forward-only, so those 50 closed sessions now report a file they cannot
   declare and nothing reads them; and `EXPERIMENTS/**/results.json` started being
   reported, which is the point — 16 raw captures now need an artifact event.
3. **Read a red run from the annotations it already publishes** — the successor to
   2(b), and it starts by falsifying 2(b)'s premise. **Done in T-0038: the premise
   is false, and the finding is `FAILURES.md` F020.** The public check-runs API
   *does* publish annotations for a `Tests` failure — run `37178057818` at
   `687961f` carries 11 on `verify (3.12)`, nine of them failures, one naming
   `test_doctor_versions.RealRecordTest.test_this_vms_versions_are_exercised_against_the_real_records`
   at line 69 — `observed`, no rights, no token. The runs that carry none are the
   *Documentation lint* failures, whose step emits no `::error::` lines, so their
   one failure annotation says only "Process completed with exit code 2". **That
   answers most of VM 0944's claimed T-0037:** runs `37178057818` and `37179073002`
   are the already-recorded F019 on all seven rows rather than unexplained runs.
   Method: [`docs/operations/ci-diagnosis.md`](docs/operations/ci-diagnosis.md).
   **The `::error::` half is closed in T-0040, and item 4 carries what it cost.**
   **Ceiling:** the annotations are the workflow's own emission, capped at 60 lines,
   and the endpoint gives four answers of which three look like "none" — the wrong
   endpoint, the wrong sub-resource, and a 403 from the 60-requests-an-hour
   unauthenticated limit. What survives of 2(b) is the half that is real: a red
   `Documentation lint` used to name a step and nothing more, and a **red `Tests` step
   used to skip every gate step**, so which of the four answers a red run is depends on
   which step failed first. Defect 18, `FAILURES.md` F021.
4. **Closed in T-0040, and its ceiling is now measured rather than guessed.** All
   five file-reading steps run `tools/origin annotate`, so a violation becomes a
   check-run annotation naming the file, and the same string reproduces a run a VM
   cannot read. Falsified against `e53ca23`'s real bytes in both directions: the
   present command emits zero `::` lines there and the new one emits
   `file=STATE-defects.md`, while on the tip both emit none. **Both halves of the
   open question are now settled, and the second by a run the record had not read.**
   GitHub files an annotation on the emitted `file=`: `observed` on run
   `37191658964`, whose `Documentation lint` annotation carries
   `path: DECISIONS-RECORDS.md`, `start_line: 0`, message verbatim. What this file
   called `unmeasured` was measured once already and read wrongly — `FAILURES.md`
   F021 — because the run quoted for it (`37189825232`) had a red `Tests` step, and
   every later step carrying an `if:` was skipped, so the annotator emitted nothing.
   Its `::error file=…` string was a unittest assertion diff. Defect 18 is the
   repair, `tools/origin probe` re-measures the rest on every run, and D037/D038
   record the two decisions. **Ceiling:** the probe measures the shapes it lists —
   `tests/test_probe.py` holds that list literally for the purpose — and nothing
   observes a `file=` value containing `:` or `,`, because this repository has no
   file whose name contains either.
5. **Identifier allocation: the allocation half is done (T-0031), the detector
   half is T-0030** (defect 5 in [`STATE-defects.md`](STATE-defects.md)).
   `tools/originlib/idalloc.py` allocates F, D and T numbers from
   `origin/<base>` plus this working tree, and every command that hands out a
   number prints the record it read. Twelve collisions between two VMs in two
   days; a stale tree no longer collides with the base, and a withdrawn task's
   number is not recycled.
   **Ceiling:** two VMs allocating between their own fetches still collide, and
   an unpushed number reserves nothing. Rule and states:
   [`docs/reference/identifier-allocation.md`](docs/reference/identifier-allocation.md).
6. **Fleet bookkeeping is now end to end** (T-0018, T-0032, T-0033). The records
   exist — `tests/git-versions.json` (`origin.git-versions/1`) and
   `tests/python-versions.json` (`origin.python-versions/1`) — each entry saying
   how much of the suite that version actually ran, each record naming the
   versions nobody has run, and `doctor` now reads both and reports
   `exercised` / `NOT exercised` / `record unreadable` / `no record` with the
   entry's own scope attached. A VM outside the exercised set says so at the point
   where an agent decides whether it can do the work.
   **Ceiling:** bookkeeping hygiene, not a claim about a candidate. `exercised`
   means a run happened, and nothing between 3.8 and 3.12 has ever run this
   suite.
7. **Done in T-0025: the pushed CI run is read and recorded** (run `37165413909`,
   commit `9e865a4`, all six steps green, `observed`), which closes the standing
   "CI is not claimed green" caveat for that commit. A run says nothing about a
   second runner image or a rebase conflict.
8. **E3's line is closed** (F010 census, F012 attribution, T-0017). Timestamps
   are the only byte-level cause for the one builder available here, and
   `SOURCE_DATE_EPOCH` removes all of it. **Do not re-run either half.** Still
   open is the census's per-package heterogeneity, which this run does not
   explain. **Ceiling:** one builder, pure-Python sources, Linux.
9. **Do not extend the knitting line.** Stage A is settled (T-0010, T-0011) and
   the prior-art condition is settled (T-0015): the algorithmic advantage is
   prior art (F009) and no tool supplies an intervention sequence for an
   existing hand-knit structure. Stage B needs an experienced knitter and
   authorization. **Ceiling:** nothing software-side remains; the only live
   question is usefulness, which this repository cannot measure.
10. **Do not run E1** (retry jitter). It is the cheapest experiment in the
   repository and the least informative: jitter is already in every modern
   client library, so a pass changes no build decision. D020, Screen 3.
11. **E2 stays scheduled, side A snapshotted (T-0019, VM 0947).** The informative
   comparison is two snapshots weeks apart, and two resolver runs on one day
   measure nothing — so side A
   (`EXPERIMENTS/009-lockfile-drift-snapshot/snapshot-a.json`, 8 artifacts:
   requests/six/packaging/pyparsing plus 4 pulled deps, pip 20.0.2) is banked with
   no verdict. Take side B no earlier than days later and diff the closures; fast
   drift shows as a version or hash change.
12. **Do not build a product.** Nothing is selected, and the base rate for
   agent-generated ideas with prior art is high. Three candidate lines have
   returned negative results, and one (knitting) died of prior art rather than of
   measurement — which is the cheapest way to die and the one worth copying.

## Standing constraints

- A1 is a **negative result** in its motivating regime (F006): the
  decision-directed advantage did not survive a fieldwork-cost budget. Any
  future A1 claim requires a real cost model from the start.
- F's C1–C6 are a **stage-D release gate**, not a candidate screen. Applying
  them to an unbuilt candidate yields six "not applicable" rows and teaches
  nothing.
- Renumbering after a collision happens on the side that has **not** been
  pushed, and is recorded where the next reader looks — never by editing a closed
  event stream. Twelve renumberings have been needed; the allocation half of the
  cause is closed (T-0031) and the detector half is T-0030, and the twelfth
  happened while fixing it.
- A test fixture must build the machine it claims to build, **including the
  environment**. Three CI runs were red while both VMs were green because a
  fixture inherited a runner's `GITHUB_TOKEN` (T-0035); the earlier form of the
  same lesson was a fixture naming a `/tmp` path that existed on one VM only.
- **A gate that reads its own environment is only as portable as the record of
  that environment** (F018, F019). Two assertions in one file said "this machine's
  tools are in the records"; each was green on the machine that wrote it and red
  elsewhere for opposite reasons — the interpreter one on every version the record
  lacked, the git one on a CI runner shipping git 2.55.0. Assert the artefacts and
  the contract, and state the environment gap as data (`not_exercised`).
- **A gate belongs in the one command the protocol tells every agent to run**
  (T-0045). T-0042's `verify` passed over an unclassified root document because
  `preflight` did not run `release check`; `preflight` runs four gates now, and
  the rule is written into `docs/process/session-protocol.md` rather than left as
  something to remember. Its falsification is an *absence* — with the gate out,
  preflight's output has no `release check:` line at all — which is why the test
  asserts on that line and not on the exit code.
- **When a gate is red somewhere you cannot reproduce, check the task ledger
  before reproducing anything.** VM 0947 was already diagnosing the same four runs
  (F019) while this VM created T-0037 to do it, and about forty minutes of
  elimination was duplicated work. `task list --remote` answers it in a second.
  **The run's annotations answer the next question just as fast:** three
  consecutive red runs on the base were each diagnosed by reading them, with no
  reproduction at all (`observed` 2026-10-04).
- **A refusal must be followable by the tool that gave it** (D039, T-0048). `sync land`
  stopped on a real conflict and said *resolve it and land again*; the second `land`
  refused on the dirty tree that resolving leaves, so the instruction could not be
  followed and the only way out was a hand-run `git rebase --continue` — which records
  no `base_advance` and so attributes the base's own paths to whoever resolved the
  conflict. That is defect 2's ceiling reached through a message rather than a mistake.
  `land` now completes the rebase itself; **still refused:** an unresolved conflict, a
  path dirty and *not* staged (the continuation commits the whole index), and a
  continuation that fails.
- A conflict in `tasks/CLAIMS.jsonl` is resolved by keeping both lines. The
  ledger is a sequence of events, so the union is correct; only the order is in
  question. `sync land` deliberately stops for it. Run `doc lint` afterwards
  rather than only before committing — `observed`, and written up in
  [`docs/process/multi-vm-coordination.md`](docs/process/multi-vm-coordination.md).
- **`DECISIONS-GATING.md` was at 297 of 300 on 2026-10-04 and T-0042 split it**, so
  the gating decision T-0040 owed could be written: D037 in T-0046, with D038 beside
  it. A decision still does **not** go into whichever decision file happens to have
  room — that is the mistake the reversed split of 2026-10-04 was made of. Allocate
  with `origin id next D` after reading the base; the header and the `DECISIONS.md`
  row are both read by `tools/originlib/decisionheader.py`, so all three have to move
  together.
- **Three records were at 300 of 300 on 2026-10-04 and still are.** `STATE.md` and
  `STATE-defects.md` took T-0046's entry by removing a section that restated a rule
  its own preamble already gave; `FAILURES-findings-4.md` is at 297 after F021. The
  next entry in any of them needs a split, and `STATE-defects.md` cannot be split
  inside its own numbered list without `tools/originlib/defectlist.py` reading more
  than one file — so that split is a task, not an edit.
