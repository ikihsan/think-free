<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Experiments that tested a method rather than a candidate (E012–E027)

Split out of [`HYPOTHESES.md`](HYPOTHESES.md) on 2026-10-09 at its line cap.

**The invariant that makes the split sensible:** every entry below is an
experiment whose *subject* was one of this mission's own methods — the
generator, the serving channel, a rate, a counting rule, a disclosure floor,
the shape of a corpus's tail, or a screen's own verdict. **None of them
produced a candidate, and none is a candidate.** They are kept together because
they answer one question together — *what did each of our own instruments
actually measure?* — and a reader asking that question should not have to load
the live candidate index to get it.

What each changed is named in its own last sentence, and every change is a
decision in [`DECISIONS.md`](DECISIONS.md) or a finding in [`FAILURES.md`](FAILURES.md).
The live candidate list, the kill gates still attached to candidates, and the
experiments that *did* test a candidate mechanism are in
[`HYPOTHESES.md`](HYPOTHESES.md).

**E012 tested the generator, not a candidate** (`EXPERIMENTS/012-candidate-harvest/`).
Its declared kill gate: if one harvested need statement yielded a candidate passing
Screen 1 and Screen 3, live harvesting becomes the mission's candidate generator.
50 statements drawn by a stated rule from 1401 harvested; **0 survived** — 38%
prior art, 30% stating no mechanism, 24% not software needs, 8% needing hardware.
No candidate entered or left this table because none was produced. What it
changed is the pipeline's *inputs*: a need corpus supplies a problem statement and
cannot supply recurrence, while an issue corpus counted by repository does
(F029, D049). The corpus is kept as a dated, countable problem-statement source
and the harvesting route is closed as a generator.

**E021 tested a serving channel, not a candidate**
(`EXPERIMENTS/021-copied-artifact-serving/`, T-0064). F037 left one reading
standing for the prior-art screen's young-vocabulary failure: the artifact a
coding-agent user commits is a **directory copied** into their repository, so
install channels would miss the field entirely. The declared gate asked whether
copying is a **larger** channel than installing. It is **0.118×** — 1,026 indexed
repositories holding a `.claude/hooks/` directory against 8,676 monthly installs
across four channels (F041, D053). No candidate entered or left the table; what
changed is that **the screen was reading the dominant channel**, so the twelve
prior-art deaths stand. Renumbered from F040/D052/`020-` on the unpushed side: the
other VM took those numbers for `EXPERIMENTS/020-copied-config-drift`, which
closed the same escape hatch from the other end.

**E023 tested a rate against its own baseline, not a candidate**
(`EXPERIMENTS/023-served-baseline/`, T-0067). F042 had concluded from a
hand-labelled **15/39 = 0.385** `served` rate that the corpus records needs the
world *absorbed conversationally*. That cell had no control. Drawn properly —
ordinary comments in the need arm's own stories, restricted to answered so both
arms share the "a reply exists" condition — the control arm reads **0.368**, and
two readers labelling the identical 39 rows agree at **κ = 0.923** (F043). The
withdrawal is of the *inference*: a reply naming an artifact is not distinguishable
from what an ordinary comment receives. E022's other two numbers stand. **No
candidate entered or left the table.** What changed is D055: a rate read from a
trigger-harvested corpus without a control arm is a description of Hacker News,
and any such corpus bounds its own outcome readings.

**E024 counted the mission's own kill reasons, not a candidate**
(`EXPERIMENTS/024-kill-reason-causes/`, T-0068). "Twelve candidates, twelve
prior-art deaths" was carried in four summaries and was the premise of E015,
E016, E017, E021 and of item 0; neither its count nor its cause had a gate.
Counted from the primary records against a population rule and a declared
precedence written first: **prior art is 10 of 18 eligible rows = 0.556 over a
population of 20**, so the plurality reading survives and the count of twelve is
false — but by a **one-row margin, since every prior-art row moved to another
category puts the share at 0.500** (F044). **Seven of the 18 died of something
else**: a mechanism its own test refuted or confirmed into uselessness (F001,
F006, F008, F012), a claim no available observation could establish, and one
promoted then parked with no reason recorded. **No candidate entered or left the
table and no prior-art verdict is falsified** — this measures what candidates
were killed *by*, which F035 measured separately. What changed is D056: a cause
claim about this record is counted from primary sources with the deciding
sentence quoted, a majority gate is reported with its sensitivity, and a control
that cannot fail is discarded rather than reported as a pass.

**One recorded result belongs to none of these.** T-0034 measured the test suite
on the CPython versions the fleet's own record named as never run, and found two
gates asserting that the machine running them was covered by that record
(`FAILURES-findings-4.md` F018, F019). It changed what the evidence base covers
and it closed no candidate, so it is recorded here only because the session
logged an `experiment_result` and the tooling requires this file to change when
one does. Nothing below rests on it, and no candidate's state moved.

**E025 tested the disclosure floor under F042's third number, not a candidate**
(`EXPERIMENTS/025-need-staters-builderhood/`, T-0069). F042's build arm read
**0 of 24** unserved requesters building what they asked for, and the record called
that a *floor on disclosure* rather than an estimate of building — but
`STATE-next-actions.md` item 0 then carried it as "the people who state a need are
not the people who build it", which is what the floor could not support. E025 read
the missing channel over **1750 authors with zero refusals**: **278 of 1250
need-staters (22.2%, CI [0.200, 0.246]) have publicly shipped something** against
**139 of 500 (27.8%, CI [0.241, 0.319])** ordinary commenters in the same stories.
The declared hypothesis (≥2×, disjoint intervals) **fails at 0.80× with overlapping
intervals.** **No candidate entered or left the table** and no prior-art verdict is
falsified. What changed is D057: an absence declared by an instrument is a
candidate for measurement, not a finding. The sentence is corrected at the source —
need-staters are a fifth builders, they build *less* than their neighbours, and the
rate at which they build **what they asked for** is unchanged (F045).

**E026 tested the shape of the corpus's unserved tail, not a candidate**
(`EXPERIMENTS/026-unserved-need-structure/`, T-0070). All 1401 comments
fetched (100%, A1 passes). Unserved statements are **not** shorter — median
55 words against 58 (ratio 0.948, B1 fails) — and trigger shares do not
predict answer rate (χ² = 34.33, 23 df, p ≈ 0.06). B2 fired as pre-registered
on two triggers at ≥2× share, but they pool 9 rows, so the structure claim is
withdrawn by its own sensitivity (D058). **No candidate entered or left the
table.** What changed: the corpus's last open reading is closed — the
unserved tail is diffuse in the dimensions measured, with one hint resting on
9 rows and not established (F046).

**E027 re-read F029's own screen, not a candidate**
(`EXPERIMENTS/027-cause-of-death-reread/`, T-0071). **31 of E012's 50 verdicts
were assigned from a regex-extracted clause rather than a comment**, so the
`vague` category — 15 rows — was measured on an extract. Two blind readers
re-read those 31 from the full text, R committed before S existed. **6 of the
15 `vague` kills state a mechanism or a named artifact in the part the screen
never read**, and index 46's clause stops *at* its trigger phrase, so its
recorded reason was true of the extract and false of the comment. The declared
six-label agreement gate **failed** (κ = 0.4627 against a floor of 0.6) and the
restated table is **inconclusive**; the separately-declared per-row gate fired
on 8 of 31, with the conservative reader's flips a strict subset of the other
reader's. **No candidate entered or left the table and F029's 0-of-50 stands**,
because none of the 8 re-opened rows is a candidate: two are features of
products the commenters do not own, one was already built by the commenter, one
is an open-source ride-hailing platform, and the rest need hardware, issuers or
per-vendor surfaces. What changed: `vague` is withdrawn as a cause of death at
its recorded size, the generator's closure is now **confirmed by a re-read
rather than carried forward**, and D059 holds that reader agreement is measured
on the grouping the decision consumes (F047).
