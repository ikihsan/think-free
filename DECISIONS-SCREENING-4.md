<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Decisions — screening candidates and judging experiments, part 4

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

Decisions **D059, D060, D061**. Split from
[`DECISIONS-SCREENING-3.md`](DECISIONS-SCREENING-3.md) at the 300-line cap: the
invariant that moved is *what a verdict's own evidence must be*, which is what
D050, D059 and D060 share and what the other entries in part 3 are about. A
decision does not go into whichever decision file has room.

## D059 — Agreement is measured on the grouping a decision uses, and a verdict may not need the table it was declared over (2026-10-05)

Observed: F047, from E027's A1/B1/C1.

**Context.** E027 re-read the 31 clause-based cause-of-death verdicts of F029
from the full comment with two blind readers. It declared two gates. **B1** was
Cohen's κ ≥ 0.6 over the six categories. **C1** was a per-row gate: fires when
≥ 5 rows are survivor-relevant to *both* readers. B1 **failed** at κ = 0.4627.
C1 **fired** at 8 of 31. The two gates disagree, and the disagreement is
informative rather than embarrassing: the post-hoc binary κ on the split C1
actually asks about is **0.5412**, and the gap is entirely two readers
disagreeing about *which* non-survivor label a row takes (`still_vague` versus
`not_a_software_need`) — a disagreement that cannot change any decision.

**Decision.** Two rules. (a) A reader-agreement gate is computed **on the
grouping the decision consumes**, not on the label set the protocol happened to
declare, and a disagreement confined to labels no decision reads is reported as
harmless rather than as a failure. (b) A **per-row gate may stand on its own**
when the declared table-level gate fails: the two answer different questions,
and a verdict that needs the table is not licensed by a table the readers do
not agree on.

**Consequence.** E027's restated six-category table is `inconclusive` and the
restated cause share is not used. The per-row gate stands on 8 of 31, and
F029's 0-of-50 is **confirmed by a re-read** because none of the 8 re-opened rows
is a candidate — a stronger basis than the original screen's clause-based
verdicts, which is a perverse but real result.

**Ceiling.** This governs how agreement is measured, not what may be concluded
from it. Two readers from one model family agreeing is still one model family,
and E027's C1 is a claim about 8 rows of one 50-row sample, not a restated
cause table. The `prior_art` half of F029 was not re-read here and was not
re-read anywhere by a procedure stronger than E016's.

## D060 — A prior-art kill rests on evidence of fit, and use is not fit (2026-10-05)

Observed: F048, from E028's declared positive control C2 failing in both
directions.

**Context.** Prior art is this mission's plurality kill reason — 10 of 18 (F044)
— and it killed all twelve candidates from the six sealed reports. D050 already
requires a verdict to *"judge the clause's attribute"* rather than a category, and
F035 measured that procedure recovering 6 of 6 positive controls. What no
verdict in this record had been checked against is **what its evidence is
evidence of.**

E028 tested the one row in the population with the strongest evidence of use
available anywhere in this record: `H03`, where the incumbent `sharp` carries
**436,835,441 downloads per month** and E016 called the row *"served beyond
argument, on install counts as well as on existence."* Two blind readers read
`sharp`'s and the other stored documentation and both returned `partial` — no
document states a latency figure or claims the clause's multi-second case is
solved. **The row with the best evidence of use is a row whose documentation
establishes nothing about the clause's attribute.**

**Decision.** Three rules, each from a specific observation.

1. **A prior-art kill must rest on evidence of fit, and evidence of use is not
   evidence of fit.** A download count, a star count, an install total and a
   copy count all speak to whether a thing is used. None of them says the thing
   does what a clause asked for. A screen that cites them has measured its
   instrument, which D050 already ruled insufficient.
2. **A control for an attribute test is chosen on fit demonstrated in
   documentation, never on use demonstrated anywhere.** E028's C2 was selected
   by adoption and failed for exactly that reason, and its failure is why the
   experiment returned `not_evaluated` rather than a number. The gate was not
   moved afterwards; D058 forbids that.
3. **An instrument that tests fit carries its own recorded ceiling for what it
   did not read.** E028 shows at most the **four artifacts the screen listed
   first**, and 1,800 characters of each stored capture. A row's `serves` label
   means that much and no more, so an artifact listed fifth could serve and the
   row would still read `does_not_serve`. Any future fit instrument publishes
   that bound with the number.

**Consequence.** E028 publishes **no verdict on fit**: `not_evaluated`, with
neither A3 nor B1 read as an answer. The five rows both readers read as
`does_not_serve` are a description of 14 rows, not a reopened population, and the
twelve deaths and the corpus closure are untouched. What changes is the rule a
*future* screen must satisfy, and it is a real change: **the existing prior-art
verdicts in this record are justified by existence and by use, and no verdict in
this record has yet been shown to rest on evidence of fit.** E016's H2 stays
`not evaluable`.

**Ceiling.** This decides what a kill must rest on; it does not establish that
any particular verdict fails that test, and it does not reopen anything. It also
does not license treating *absence of documented fit* as *demonstrated absence of
fit* — E028's rubric records a documentation's **silence** as evidence of no
documented fit, and a product that does the thing without saying so is
invisible in both directions. Distinguishing those two needs a different
instrument again, and naming it is what E028 leaves open.
## D061 — A reader's labels are admissible only if they can be tied to the exact
## bytes the reader saw (2026-10-05)

**Decision.** A judgement made by a model over rows of text is evidence only when
the artefact it was made from is *frozen and identified*, and only when the
labelling is checked mechanically against that artefact rather than by the reader's
own account of what it did. Concretely, three requirements:

1. **The input is identified, not described.** The view is hashed and the digest
   recorded beside the result. Reader r1's report carried the digest; that is the
   part of its report that mattered.
2. **Row ids are checked by order, not by set.** An id *set* can be complete while
   the id-to-pair mapping is wrong, and nothing downstream can tell.
3. **The verification is a command, not a self-check.** A reader that has drifted
   cannot notice by looking harder.

**Why now.** E029 produced a label file with **222 correct row ids and a wrong
row-to-pair mapping**: a reader detected the view being regenerated beneath it,
discarded its own pass, re-labelled correctly, and then emitted rows in the
*previous* view's order. A second reader returned four duplicated and four missing
ids. Both passed an id-set check. The defence D059 requires — that a verdict rest
on evidence of the property it claims — is meaningless if the evidence cannot be
tied to the bytes it was read from.

**The part that is about me.** I saw one positional mismatch, concluded the file was
mis-keyed, and wrote a repair that re-keyed it against the wrong reference. It
reported **221 of 222 agreeing** and overwrote a correct ordering with a false one.
The script is deleted. *A high agreement rate against an unestablished reference is
indistinguishable from success*, so a repair must establish its reference before
measuring agreement against it.

**Consequence.** E029's reader arm is `not_evaluated`, refused twice: κ = 0.5004
against a floor of 0.6, and the declared negative control's separation 0.0405 against
0.20. Three reader passes produced no usable comparison. The demand-corpus closure
stands, confirmed on an instrument 10× larger than E022's rather than refuted.

**Ceiling.** This governs how a judgement is *bound to its input*. It does not make
any reader better: κ = 0.5004 is a real disagreement between two passes of one model
family, and no amount of provenance tracking moves it. E029 also shows the cheap
half of the defence — a test over the population — catching two of three defects
before the data were read, which is the part worth copying.
