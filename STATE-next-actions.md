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
   against the defect's own bytes before it is trusted** (D025, from F013). Five
   gates now work that way: the conflict-marker rule, `release check`, the
   landed-work attribution and generated-stamp rules (both falsified in T-0024,
   one after a first attempt that falsified nothing), the identifier allocation
   of T-0031, whose first falsification run also exposed two defects in the
   implementation it was testing, and the CI-matrix gate of T-0034. The pattern
   is in `tools/originlib/conflicts.py`.
   **Ceiling:** each rule detects only the shape it was written against.
2. **The two gaps in that pattern, both found by hitting them.** (a) **Closed in
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
   (b) A red CI run names a **step and a version**, not a test: the run log needs
   admin rights, which is why F019 took an hour to find. The fix proposed here is
   one check per test file — the suite is 40-odd files and the slowest is the fleet
   harness, so it is affordable. **The premise under this half is now itself in
   question; see item 3.**
   **Ceiling:** neither closes the general problem; they narrow where a
   hand-maintained identifier list and an unreadable log can hide a defect.
   A third, cheaper observation belongs here: a commit published while a session
   with **no task and no claim** is open is red on the session step, twice in an
   hour on 2026-10-04 (runs `37174316639`, `37181374433`), each green on the next
   commit. D027's predicate can only prove a session alive from a claim, so a
   taskless session has nothing to point at. `docs/operations/ci.md` now says how
   to recognise this case from the run alone, which is the cheap half; the other
   half is whether a taskless session should publish code commits at all.
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
   **Ceiling:** the annotations are the workflow's own emission, capped at 60
   lines, and the endpoint gives four answers of which three look like "none" — the
   wrong endpoint, the wrong sub-resource, and a 403 from the 60-requests-an-hour
   unauthenticated limit. What survives of 2(b) is the half that is real: three
   gate steps emit no annotations at all, so a red `Documentation lint` still names
   a step and nothing more.
4. **Identifier allocation: the allocation half is done (T-0031), the detector
   half is T-0030** (defect 5 in [`STATE-defects.md`](STATE-defects.md)).
   `tools/originlib/idalloc.py` allocates F, D and T numbers from
   `origin/<base>` plus this working tree, and every command that hands out a
   number prints the record it read. Twelve collisions between two VMs in two
   days; a stale tree no longer collides with the base, and a withdrawn task's
   number is not recycled.
   **Ceiling:** two VMs allocating between their own fetches still collide, and
   an unpushed number reserves nothing. Rule and states:
   [`docs/reference/identifier-allocation.md`](docs/reference/identifier-allocation.md).
5. **Fleet bookkeeping is now end to end** (T-0018, T-0032, T-0033). The records
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
6. **Done in T-0025: the pushed CI run is read and recorded** (run `37165413909`,
   commit `9e865a4`, all six steps green, `observed`), which closes the standing
   "CI is not claimed green" caveat for that commit. A run says nothing about a
   second runner image or a rebase conflict.
7. **E3's line is closed** (F010 census, F012 attribution, T-0017). Timestamps
   are the only byte-level cause for the one builder available here, and
   `SOURCE_DATE_EPOCH` removes all of it. **Do not re-run either half.** Still
   open is the census's per-package heterogeneity, which this run does not
   explain. **Ceiling:** one builder, pure-Python sources, Linux.
8. **Do not extend the knitting line.** Stage A is settled (T-0010, T-0011) and
   the prior-art condition is settled (T-0015): the algorithmic advantage is
   prior art (F009) and no tool supplies an intervention sequence for an
   existing hand-knit structure. Stage B needs an experienced knitter and
   authorization. **Ceiling:** nothing software-side remains; the only live
   question is usefulness, which this repository cannot measure.
9. **Do not run E1** (retry jitter). It is the cheapest experiment in the
   repository and the least informative: jitter is already in every modern
   client library, so a pass changes no build decision. D020, Screen 3.
10. **E2 stays scheduled, side A snapshotted (T-0019, VM 0947).** The informative
   comparison is two snapshots weeks apart, and two resolver runs on one day
   measure nothing — so side A
   (`EXPERIMENTS/009-lockfile-drift-snapshot/snapshot-a.json`, 8 artifacts:
   requests/six/packaging/pyparsing plus 4 pulled deps, pip 20.0.2) is banked with
   no verdict. Take side B no earlier than days later and diff the closures; fast
   drift shows as a version or hash change.
11. **Do not build a product.** Nothing is selected, and the base rate for
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
- A conflict in `tasks/CLAIMS.jsonl` is resolved by keeping both lines. The
  ledger is a sequence of events, so the union is correct; only the order is in
  question. `sync land` deliberately stops for it. Run `doc lint` afterwards
  rather than only before committing — `observed`, and written up in
  [`docs/process/multi-vm-coordination.md`](docs/process/multi-vm-coordination.md).
- `DECISIONS-GATING.md` is at **297 of 300** lines, and its own header records a
  split that was attempted and reversed on 2026-10-04 (T-0030). So the next gating
  decision cannot simply be appended: it needs that file split by invariant on a
  quiet base, or its cap deliberately changed. A decision does **not** go into
  whichever decision file happens to have room — that is the mistake the reversed
  split was made of. `tools/originlib/doclint.py` is at 299 of 300 for the same
  reason, and the next check added to it has to split it.