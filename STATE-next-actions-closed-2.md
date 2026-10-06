<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Next actions, closed items, part 2

Split out of [`STATE-next-actions-closed.md`](STATE-next-actions-closed.md) on
2026-10-06 (T-0081) at the 300-line cap, by invariant: that file now holds the
**prose** about why closed work was moved and the one standing deferral (item 0b),
while this file holds **the numbered items themselves**. Nothing was shortened in
either direction.

Identifiers are the same ones `STATE-next-actions.md` and `STATE.md` use. Read a
finding number and go to the file it is defined in.

1. **A gate must read the property it claims to check, and must be falsified
   against the defect's own bytes before it is trusted** (D025, from F013). Nine
   gates now work that way, the newest being the rule that holds a restated
   experiment number to its artifact (T-0056, D047, defect 22). Its case is the
   sharpest yet, because the **obvious rule is green on the defect**: "does this
   number occur anywhere in the artifact?" answers *yes* for `113`, which also
   sits at `patch_cost_sensitivity/*/cases`. What settles it is reading the
   number's *shape* rather than the file's contents, and the blindness of the
   rejected rule is now asserted so the restriction cannot be dropped quietly.
   Method: `docs/policy/gate-falsification.md`.
   **Ceiling:** each rule detects only the shape it was written against, and
   `resultnumbers.py`'s is one table row per experiment.
2. **The gaps in that pattern, both found by hitting them — closed, and the
   second found by reading the record rather than by a red run.** (a) **T-0036.**
   Doc-lint rule 7 read findings definitions, index rows and decision spans, and
   not the numbered list in [`STATE-defects.md`](STATE-defects.md), so two VMs
   took **defect 7** in the same hour and nothing reported it; both copies reach
   the shared base, each tree internally consistent, and the unpushed side
   renumbered by hand. `idcheck.py` is now the one entry point both publishing
   gates call, because a module wired into one gate is not thereby read by the
   other, and it reports a list it cannot read.
   **Ceiling:** a repeated number and nothing else — a dropped entry and a
   withdrawn defect are the same bytes — and there is no allocator here, so this
   is the detection half of a race it cannot prevent.
   (b) Settled by item 3, which falsified its premise.
   (c) **T-0042.** A decision number is written in three places that must agree —
   the `## Dnnn` heading, the row in [`DECISIONS.md`](DECISIONS.md), and the
   `Decisions **…**` header under each record's title — and only the first two had
   a reader. Two of five records were false while every gate passed, with both
   index rows correct throughout. `decisionheader.py` reads the third through the
   same entry point.
   **Ceiling:** identifier sets rather than wording, one line per record.
   A cheaper observation belongs here: a commit published while a **taskless**
   session is open is red on the session step — five runs in one day, every one
   green on the next commit. D027's predicate can only prove a session alive from
   a claim. `docs/operations/ci.md` now says how to recognise the case from the
   run alone; whether a taskless session should publish code commits at all is
   open.
   (d) **Closed in T-0050 (D042, F022).** `reconcile._is_vendored` reused the
   **line cap's** exemption predicate, which answers yes for every `.json`,
   `.jsonl` and `.log`, so `tests/python-versions.json` — the record that decides
   whether a VM can run the work — changed with nothing declared and nothing
   reported. Priced first by a committed script: **72 (session, path) pairs over 17
   paths**, 50 of them the ledger, so 50 closed sessions now report a file they
   cannot declare; a closed stream is not edited, so the residual is written down
   rather than discovered.
   **Ceiling:** forward-only, and `EXPERIMENTS/**/results.json` now needs an
   artifact event — 16 raw captures do.

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
4. **Closed in T-0040, and its ceiling measured rather than guessed.** All five
   file-reading steps run `tools/origin annotate`, so a violation becomes a
   check-run annotation naming the file; falsified against `e53ca23`'s real bytes
   in both directions. GitHub files an annotation on the emitted `file=`:
   `observed` on run `37191658964`, whose `Documentation lint` annotation carries
   `path: DECISIONS-RECORDS.md`, `start_line: 0`, message verbatim. What this file
   called `unmeasured` had been measured once and read wrongly (F021): the run
   quoted for it had a red `Tests` step, so every later `if:`-guarded step was
   skipped and the annotator emitted nothing. Defect 18 is the repair and
   `tools/origin probe` re-measures the rest on every run. **Ceiling:** the probe
   measures the shapes it lists, and nothing observes a `file=` value containing
   `:` or `,`, because this repository has no file whose name contains either.
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
11. **E2 stays scheduled, side A snapshotted (T-0019, VM 0947), one fast-drift
    null measured.** The informative comparison is two snapshots weeks apart, so
    side A (`EXPERIMENTS/009-lockfile-drift-snapshot/snapshot-a.json`, 8
    artifacts: requests/six/packaging/pyparsing plus 4 pulled deps, pip 20.0.2) is
    banked with no verdict, and a same-week rerun found **zero drift at ~21h**.
    Take side B no earlier than days later and diff the closures; fast drift
    shows as a version or hash change.
12. **Do not build a product.** Nothing is selected, and the base rate for
    agent-generated ideas with prior art is high. Three candidate lines have
    returned negative results, and one (knitting) died of prior art rather than of
    measurement — which is the cheapest way to die and the one worth copying.