<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Evidence-driven roadmap

Stages are ordered by dependency, not by date. Evidence can send work back to an
earlier stage; there is no calendar here and none is promised.

Status legend: **done**, **partial**, **not started**, **blocked**.

## A — Independent exploration

**Status: partial.** All six roles sealed; the consolidation below is partial.

- [x] Verify the environment and record actual limits (`EXPERIMENTS/000-capabilities`)
- [x] Preserve the mission and boundaries (`MISSION.md`)
- [x] Sealed reports A–D (`RESEARCH/A.md`–`D.md`)
- [x] Investigation E: three falsifiable mechanisms. Sealed 2026-10-03 (T-0002).
      E1 and E2 remain `untested`; E3's declared gate could not fail (F010)
- [x] Investigation F: adoption researcher — six pre-release checkable criteria.
      Sealed 2026-10-03 (T-0003); the criteria become a gate at stage D, not a
      candidate screen
- [ ] Consolidate the reports into competing hypotheses, preserving
      disagreements. Partly done in `HYPOTHESES.md`; the cross-report screen is
      `RESEARCH/SYNTHESIS.md` (T-0012).

## B — Experimental discovery

**Status: partial.** Thirty-two experiments have run; three invention claims are
disproved, one declared gate could not fail, one mechanism was confirmed while its
candidate died of it, the prior-art screen is measured (F035, F034), read against its
own extract (F047) and asked what its evidence is evidence of (F048: **use is not
fit**), the demand corpus has been followed forward twice (F049), and **the
recurrence zero has been checked for the venue it was a result about and survived a
venue change** (F053, F054). None validated.

- [x] Write the experiment protocol (`docs/process/experiment-protocol.md`)
- [x] Run E001 as a baseline check; kill gate met, motivating example disproved (F001)
- [x] Write kill gates for the three held candidates in `HYPOTHESES.md` (T-0001, 2026-10-03)
- [x] Apply the information-sufficiency test to the three held candidates (`003`, T-0008:
      W1/W3 survive, W2 spec insufficient, F007)
- [x] Run the A1 masking experiment on the PPNA sidewalk extract (`002`, T-0005/6/7:
      count-budget gate met, fieldwork-cost gate fails, F006)
- [x] Test the knitting candidate's Stage-A planner twice: per-error rule
      suboptimal (`004`, T-0010), whole-neighbourhood search exact (`005`, T-0011)
- [x] Search the knitting candidate's last kill-gate condition (`RESEARCH/PRIOR-ART-KNITTING.md`,
      T-0015): the algorithmic advantage is prior art (F009)
- [x] Run the ventilation candidate's measurement-design kill gate
      (`006-ventilation-measurement-design`, T-0014): gate not met, formulation
      stopped (`FAILURES.md` F008)
- [x] Run E3's build-timestamp census over 200 PyPI wheels (`007`, T-0013): declared 5% gate
      met at 0.965, but the metric measures DOS-epoch pinning (F010)
- [x] Attribute the byte difference (`008`, T-0017): 398 of 398 differing bytes are timestamp
      fields, so E3's mechanism is supported and its candidate abandoned (F012)
- [x] Measure the prior-art screen's coverage (`016`, T-0062): 6 of 6 controls recovered,
      3 of 12 adjudicable kills have no prior art (F035/F036)
- [x] Measure the prior-art screen's own population (`017-incumbent-artifact-type`, T-0061):
      14 of 18 young-vocabulary rows are executable code, so F034's premise failure is not a
      population artefact (F037)
- [x] Test the consequence F037 inferred (`020-copied-config-drift`, T-0065): copying is
      instructed in 687 places and duplicated in 4.7% of contents, so readers adapt (F040)
- [x] Read the disclosure floor under F042's build arm (`025-need-staters-builderhood`, T-0069):
      278/1250 = 0.222 of need-staters have publicly shipped something against 0.278 for ordinary
      commenters in the same stories, so the 0-of-24 was a floor (F045, D057)
- [x] Ask what the screen's evidence is evidence of (`028-incumbent-fit`, T-0072): `sharp`, at
      437M downloads/month, documents nothing about its clause — **use is not fit** (F048, D060)
- [x] Ask whether need-staters build what they state (`029`, T-0073): **167 of the 241 who
      shipped had shipped *before* they complained**, so 69% was never askable; the link bounds
      at [−0.0156, +0.1125], consistent with zero (F049, D061)
- [x] Read the departure population for the gap, not the move (`031-unfilled-requirement`,
      T-0075): **the seek and move strata are identical at 0.347 each**, so the "unfilled"
      premise is retired by measurement; 0 of 100 clause pairs recur (F051, D062)
- [x] Ask what the recurrence zeros were a result *about* (`032-venue-recurrence`, T-0076):
      all 3,856 comment ids behind F039/F042/F043/F049/F051 are Hacker News and four of five
      experiments re-read one file at 100% id overlap, so "three populations" was two corpora on
      one platform (F053); **E032 then changed the venue and nothing else** — 0 of 32 candidate
      pairs and 0 of 60 control pairs, difference 0.0000 CI95 [−0.0602, +0.1072], κ = 0.8344,
      20/20 positives — so the zero is **not** that platform's properties, and the generalisation
      becomes a venue-agnostic **bound of 0.0223** pooled with E031's 100 (F054)
- [x] Ask whether that bound is a fact about the world or a fact about the draw
      (`033-question-recurrence`, T-0077): read recurrence off **Stack Exchange's own
      duplicate-closure judgement** instead of a linkage rule this repository invented, over 1000
      questions — **0.0540 CI95 [0.0416, 0.0698]** against the 0.0223 bound, so **the bound is
      refuted** (F055). **The zeros were a stratum effect**: the top 60 by score, which is what
      `sort=votes` draws, contains **0** duplicate closures against a mean of 3.37 over all 941
      sliding windows, and the rate runs **0.0180 in the top score tertile against 0.0808 in the
      bottom**. A second claim — that repeats go unanswered (0.5556 against 0.2114) — was
      **withdrawn by the run itself as mechanical**, since zero of the 54 duplicates has an
      accepted answer and closure does not answer a question. The edge arm
      failed its gate (6 of 24), so the closure's canonical is treated as unreadable and the
      declared visibility product is not printed
- [ ] Measure recurrence on a population that is **not** selected by answer state — the
      D7 counterfactual says the current draws are, and it says it without needing a canonical
- [ ] Run at least two materially different falsification experiments before any
      commitment decision. Only the knitting line has had two, and no candidate has two.
- [ ] Independently reproduce or review each result, checking oracle and baseline

## C — Commitment

**Status: not started. Nothing may be selected yet.** Select only when evidence
demonstrates technical possibility, differentiation against the strongest existing
approach, practical value, and an adoption path; otherwise pivot. Criteria in
`docs/process/hypothesis-lifecycle.md`.

## D — Engineering

**Status: not started. No product exists.** Smallest independently usable
implementation; behavioural tests that can fail on a meaningful defect; honest
limits documented alongside capabilities; reproducible build and installation,
security review, real examples.

## E — Public release

**Status: not started. Blocked on C and D, and on the user's push authorization.**

- [ ] Licence, install path, demo, honest comparison, contributor guide
- [x] `origin release check` implemented against `RELEASE-MANIFEST.md` (T-0022)
- [ ] Push with explicit user authorization
- [ ] No unreleased behaviour described as shipped — the front-door directive makes
      this an agreement the machine checks, not a promise

## F — Real-world validation

**Status: not started.** Observe actual use and adoption friction. No fabricated
feedback, no unsolicited outreach.

## G — Expansion

**Status: not started.** Improve reliability, capability, accessibility and
interoperability in response to observed problems.

## H — Sustained reassessment

**Status: ongoing.** Reassess whether continuing is justified. Reopen a rejected
candidate only when the evidence that killed it is invalidated, not because effort
was previously spent.

The **infrastructure track** — session logging, task dispatch, doc lint, indexes, CI
diagnosis, identifier allocation and the falsified-gate catalogue — moved to
[`ROADMAP-infrastructure.md`](ROADMAP-infrastructure.md) on 2026-10-06 at the 300-line
cap, by invariant rather than by size.

## Sequencing note

The infrastructure track finished ahead of stage B because stage B is blocked on judgement, not
tooling — twice over: on what no experiment here can answer (whether a knitter follows a generated
repair plan, whether E3's finding generalises beyond one builder, item 8) and, since E016, on
which axis a candidate is selected. **That blocker has narrowed nine times**
(F035, F037, F039, F041, F042, F043, F048, F053, F054, F055, D053–D055, D060) and resolves to
an owner decision. **The twelve prior-art deaths stand**, and F048 leaves them resting on a rule they
do not yet meet. E022 followed the demand-side asset forward and E023 withdrew its one
uncontrolled number (F043, D055); E032 showed the recurrence zero is not one platform's
property (F053, F054), and **E033 then showed the bound that zero produced was an artefact
of the draw** (F055). See [`STATE-in-flight.md`](STATE-in-flight.md).

The tooling itself is not finished, and what remains is *fleet* work rather than invention
work: the exercised-version records exist and `doctor` reads them (T-0033), every CPython
minor from 3.8 to 3.14 has run the suite (T-0034, D035), identifiers are allocated from the
shared base with the record printed (T-0031), and a red CI run is diagnosable without admin
rights (F020, T-0038). The floor claim is two things it is not: nothing about 3.15
onwards, and a green row is evidence about that row and not the version below it. A suite that
only passes where its author works is not a suite — the interpreter assertion failed on every
version the record lacked (F018), the git assertion on every runner whose git nobody recorded
(F019), the credential fixture on every runner exporting `GITHUB_TOKEN` (T-0035): **each green
where written.**
- [x] A red gate step names the file it rejected (`tools/origin annotate`, T-0040,
      defect 17). The five file-reading steps ran a gate, printed a report and exited, so
      the check run's only annotation was "Process completed with exit code 2" and the log
      that says which rule failed needs admin rights. A violation now carries the file and
      line its own rule knows; falsified against `e53ca23`'s own bytes in both directions,
      and `observed` on run `37196459285` filing all seven.
- [x] A diagnostic step runs whenever the job runs, and a probe measures it on the same run
      (T-0046, defect 18, F021, D038). An `if:` naming no status function gets an implicit
      `success()`, so a red `Tests` step skipped all five gate steps on two runs. `always() &&`
      on each, plus `tools/origin probe`
- [x] A refusal is followable by the tool that gave it (T-0048, D039,
      `tools/originlib/landrebase.py`). `sync land` stopped on a real conflict and said *resolve
      it and land again*; the second `land` refused on the dirty tree that resolving leaves, so
      the only way out was a hand-run `git rebase --continue`, which records no `base_advance` —
      defect 2's ceiling reached through a message rather than a mistake. `land` now completes
      the rebase and reads the pre-rebase tip from git's own `orig-head`. Falsified both ways
- [x] A command's own write is declared by the bytes it wrote, whatever its suffix (T-0050, D042,
      F022). `reconcile` asked the *line cap's* exemption predicate, true for every `.json`,
      `.jsonl` and `.log`, so the undeclared-change report skipped every data-file edit — including
      the version records that decide whether a VM can run the work. The two questions are named
      separately now and reconciliation asks its own; the claim ledger and `vendor/hashes.json` are
      declared by their writers' bytes. Priced **before** the repair by
      `tools/sweep_unlogged_data.py`: 72 (session, path) pairs over 17 paths, 50 the ledger. The
      general form: an exemption is a claim about what another check covers, and the cheap way to
      write one is to borrow a predicate.
- [x] A claim is publishable from inside the session that made it (T-0055, D044, defect 21,
      F023). `task claim` committed then called `push`, which refuses a dirty tree — and an open
      session guarantees one, so the claim stayed local and **no other VM could see it**: the
      exclusivity the command exists for was not in force. Falsified both ways
- [x] Standard-library test suite, with [`tests/git-versions.json`](tests/git-versions.json)
      recording how much of the suite each git version has run. A test's correctness depends on
      every clock the code under it reads (T-0044, defect 15)
- [x] A gate is falsified against the bytes of the defect it guards. Six ways an instrument is
      wrong about what it measures are now named: **cannot fail** (F010), **fires on coincidence**
      (F050), **cannot fire** (F051), **passes on the condition it detects** (F052), **reads its
      input's file instead of its labels** (E032, `link.py`), **is pointed at a population where
      the thing it measures is rare** (F055, 4.5× — no gate involved at all), and **cannot be
      separated from a property of its own label** (F055's D9: 0 of 54 duplicates has an
      accepted answer, so the "unanswered" gap was largely what closure does)
