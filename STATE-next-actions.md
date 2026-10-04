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
2. **The two gaps in that pattern, both found by hitting them.** (a) Doc lint
   rule 7 reads findings definitions, findings index rows and decision spans. It
   does not read the numbered list in [`STATE-defects.md`](STATE-defects.md), so
   T-0034 and T-0035 — written on two VMs in the same hour — both took **defect
   7** and nothing reported it. The unpushed side renumbered to 8 and 9; the
   numbers are unique and the list is not in ascending order, and until the rule
   is extended that file is the one document here whose identifiers are checked
   by reading it. (b) A red CI run names a **step and a version**, not a test:
   the run log needs admin rights and the public check-runs API returns no
   annotations, which is why F019 took an hour to find. The fix is one check per
   test file — the suite is 40-odd files and the slowest is the fleet harness, so
   it is affordable — and it is the only diagnostic that needs no rights.
   **Ceiling:** neither closes the general problem; they narrow where a
   hand-maintained identifier list and an unreadable log can hide a defect.
2. **Identifier allocation: the allocation half is done (T-0031), the detector
   half is T-0030** (defect 5 in [`STATE-defects.md`](STATE-defects.md)).
   `tools/originlib/idalloc.py` allocates F, D and T numbers from
   `origin/<base>` plus this working tree, and every command that hands out a
   number prints the record it read. Twelve collisions between two VMs in two
   days; a stale tree no longer collides with the base, and a withdrawn task's
   number is not recycled.
   **Ceiling:** two VMs allocating between their own fetches still collide, and
   an unpushed number reserves nothing. Rule and states:
   [`docs/reference/identifier-allocation.md`](docs/reference/identifier-allocation.md).
3. **Fleet bookkeeping is now end to end** (T-0018, T-0032, T-0033). The records
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
4. **Done in T-0025: the pushed CI run is read and recorded** (run `37165413909`,
   commit `9e865a4`, all six steps green, `observed`), which closes the standing
   "CI is not claimed green" caveat for that commit. A run says nothing about a
   second runner image or a rebase conflict.
5. **E3's line is closed** (F010 census, F012 attribution, T-0017). Timestamps
   are the only byte-level cause for the one builder available here, and
   `SOURCE_DATE_EPOCH` removes all of it. **Do not re-run either half.** Still
   open is the census's per-package heterogeneity, which this run does not
   explain. **Ceiling:** one builder, pure-Python sources, Linux.
6. **Do not extend the knitting line.** Stage A is settled (T-0010, T-0011) and
   the prior-art condition is settled (T-0015): the algorithmic advantage is
   prior art (F009) and no tool supplies an intervention sequence for an
   existing hand-knit structure. Stage B needs an experienced knitter and
   authorization. **Ceiling:** nothing software-side remains; the only live
   question is usefulness, which this repository cannot measure.
7. **Do not run E1** (retry jitter). It is the cheapest experiment in the
   repository and the least informative: jitter is already in every modern
   client library, so a pass changes no build decision. D020, Screen 3.
8. **E2 stays scheduled, side A snapshotted (T-0019, VM 0947).** The informative
   comparison is two snapshots weeks apart, and two resolver runs on one day
   measure nothing — so side A
   (`EXPERIMENTS/009-lockfile-drift-snapshot/snapshot-a.json`, 8 artifacts:
   requests/six/packaging/pyparsing plus 4 pulled deps, pip 20.0.2) is banked with
   no verdict. Take side B no earlier than days later and diff the closures; fast
   drift shows as a version or hash change.
9. **Do not build a product.** Nothing is selected, and the base rate for
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