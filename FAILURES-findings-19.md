<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Failures — recorded findings F045

Split out of [`FAILURES-findings-18.md`](FAILURES-findings-18.md), which held
F044 and had room. This file exists for F045.

See [`FAILURES.md`](FAILURES.md) for the index. **Identifiers are stable across
all findings files.**

## F045 — A fifth of the people who publicly state a need have publicly shipped something, and they build *less* than their neighbours

Source: session `2026-10-05-013`, 2026-10-05. Full record:
[`EXPERIMENTS/025-need-staters-builderhood/`](EXPERIMENTS/025-need-staters-builderhood/).
T-0069. **Confirms rather than withdraws F042's third number's caveat, reopens no
candidate, and falsifies no prior-art verdict.**

**The belief under test.** F042 measured **0 of 24** unserved requesters building
the thing they had asked for, and the record labelled that arm a *floor on
disclosure* rather than an estimate of building. The zero was then carried into
[`STATE-next-actions.md`](STATE-next-actions.md) item 0 as *"the people who state a
need are not the people who build it"* and used in item 0d to close the corpus.
**Self-disclosure is exactly what that sentence denies**, so the escape hatch had
never been tested: need-staters might build at an ordinary rate and simply not say
so.

**The instrument and its gate.** One Hacker News Algolia query per author for items
tagged both that author and `show_hn`. Gate A1, declared before the first fetch:
**6 of 6** verified positive controls recovered, nonsense account **0**. Zero
refusals in 1750 authors.

| arm | authors | with ≥1 `show_hn` | rate | Wilson CI95 |
|---|---|---|---|---|
| need — stated a need | 1250 | 278 | **0.2224** | [0.2002, 0.2463] |
| control — ordinary commenter, same stories | 500 | 139 | **0.2780** | [0.2405, 0.3188] |

**The hypothesis failed, and failed in the opposite direction.** H1 predicted the
need arm at ≥2× the control arm. It reads **0.80×**, with overlapping intervals.
Need-staters announce *less* than ordinary commenters in the same stories, so the
disclosure-floor reading is **not supported**: the instrument E022's arm lacked was
available, and it finds the need arm if anything **under**-represented among
builders. Item 0d's closure of the corpus is **confirmed rather than withdrawn**,
and the caveat on F042's third number becomes a measurement instead of an excuse.

**What is newly true, and it is the useful half.** **22.2%** of the people who
publicly wrote "is there a tool that…" have publicly shipped something. So
*"need-staters are not builders"* is **false as an absolute**. What survives is
weaker and relative: they build less than their neighbours, and the rate at which
they build **what they asked for** is still the 0-of-24 floor it always was. F042's
third cell is **bounded, not repaired**.

**Three things it does not do.** F029's 0 of 50, F039's 1250 individuals and the
corpus closure are untouched — a population that builds something *else* is not a
population of standing unmet need. No prior-art death moves. F043's withdrawal of
the `served` figure is untouched, since it was decided by its own control.

**Ceilings.** The tag is set by HN, not the author, so **the floor is inherited,
not lifted**: this cannot see a build that was never announced, in either arm. It
is a lower bound on disclosure, and it says nothing about whether what was built
was good, used, or related to the need. The confounder is severe and reported, not
corrected: within the control arm, authors with a `show_hn` post have a **median
2416 total HN items against 467** without one, so the tag tracks HN activity
strongly. That is why the control arm comes from the need arm's own stories — a
control drawn from HN at large would be dominated by heavy posters — but the
exposure is shared, not equal. Arms are not matched on tenure, and the control arm
stopped at the **declared 500**, which resolves a 2× ratio to about ±0.035 and is
not a claim that 1250 control authors would give the same ratio.

### The instrument defect this run found in itself

**Gate A1's original control set was wrong and nearly produced a false positive.**
PROTOCOL.md named four accounts *believed* to have shipped a `Show HN:` item. Two
returned 0, and reading all their indexed stories shows why: `patio11` and
`chromium` have no post titled `Show HN` at all. They were never positive
controls. Reading "4 of 4" as a pass would have been a **false positive produced by
a faulty gate**, and the instrument itself had been correct throughout.

This is F036's shape — a control asserted positive by belief rather than verified
against what it is a control for — and it is the sharpest instance in this record,
because the defect was in the gate protecting the finding rather than in the
finding. Corrected by sampling the `show_hn` tag itself, before either arm ran,
with the four originals **kept in the capture with their zeros**;
`EXPERIMENTS/025-need-staters-builderhood/test_gates_falsified.py` asserts they
stay recorded as empty so a later reader cannot quietly restore them. **The gate
threshold was never moved; only the membership of the control population was
corrected, against the instrument's own output.**

## F046 — The corpus's unserved tail is diffuse, and its one structured hint rests on 9 rows (2026-10-05)

Source: session `2026-10-05-014`, 2026-10-05. Full record:
[`EXPERIMENTS/026-unserved-need-structure/`](EXPERIMENTS/026-unserved-need-structure/).
T-0070.

**What was asked.** The last open reading of the E022 corpus: do the 589
statements that drew no reply carry structure — a vagueness signal, a trigger
penny it all hangs on — or are they the diffuse tail any such corpus
produces? Protocol written before the first text fetch.

**What was measured.** All 1401 comments fetched (100%, gate A1 passes).
Unserved statements are **not** shorter — median 55 words against 58
(ratio 0.948), so B1 fails. One pre-registered gate did fire: B2, two
trigger phrases at ≥2× share in the unserved arm (`does anyone know a tool`
4.14×, `is there a python library` 2.07×).

**What the firing gate is worth.** The two firing triggers carry 4 and 5
rows total, and the corpus-wide chi-square of trigger × answered is χ² =
34.33 on 23 df, p ≈ 0.06 — not significant at 0.05. B2 is a true firing of
a gate written before the data, and the structure claim it would carry does
not survive its own sensitivity. The honest reading is H0: the unserved
tail is **diffuse** in length and trigger, with one hint at answer rates of
0.25 and 0.40 against the corpus's 0.58 that rests on 9 rows and is not
established.

**What it changes.** The E022 corpus's readings are now all taken: outcomes
(F042), served-baseline control (F043), builderhood (F045), need-stater
population (F039), candidate generation (F029), and now the shape of the
unserved tail (F046). No hidden structured sub-population remains at this
resolution, so the closure of the corpus as a generator stands on
measurement, not on the absence of a reading.

**Ceiling.** One platform, one corpus, one reader of the text; length is
stripped words, not judged vagueness; triggers are E012's 23, which F042
showed mark staters rather than outcomes. A decision would need a
population too small to defend at this sample.

## F047 — F029's `vague` cause of death was measured on a regex, and 6 of its 15 rows are not vague (2026-10-05)

Source: session `2026-10-05-015`, 2026-10-05. Full record:
[`EXPERIMENTS/027-cause-of-death-reread/`](EXPERIMENTS/027-cause-of-death-reread/).
T-0071. **Withdraws a cause of death at its recorded size, and confirms the
conclusion it was carrying. Falsifies no prior-art verdict and produces no
candidate.**

**The belief under test.** F029 screened 50 harvested need statements and **0
survived**: `prior_art` 19, `vague` 15, `not_a_software_need` 12,
`needs_hardware` 4. That result closed the live-need generator (D049, D051),
emptied item 0d's invention seat, and is carried in four files as a fact about
the world's stated needs. **31 of the 50 verdicts were assigned from a clause,
not a comment** — `sample_needs.py::clause()` takes the text between the matched
trigger phrase and the first sentence break, capped at 300 characters.

Two consequences were visible in the committed file before the protocol was
written: **13 of the 31 carry at least 20 further words of comment the screen
never read**, and **3 of the 50 clauses are not substrings of their own text**.
One recorded reason asserts *"no mechanism stated anywhere in the comment"* —
a claim about the whole document made without reading it, which is F030's shape
one stage earlier.

**What was measured.** The 31 clause-based kills, re-read from the **full
comment** by two readers blind to the original verdict and, for the second, to
the first reader. Protocol and gates written first; both gates falsified against
fabricated populations in both directions before their results were read
(`recheck.py --selftest`).

| gate | declared | observed | verdict |
|---|---|---|---|
| A1 | 31 rows, each with non-empty text, no leaked field | 31 of 31 | pass |
| B1 | Cohen's κ ≥ 0.6 over the six categories | **0.4627** | **FAILS — the restated table is inconclusive** |
| C1 | fires at ≥5 rows survivor-relevant to **both** readers | **8 of 31** | **FIRES** |

**Six of the fifteen `vague` kills are not vague.** Both readers independently
read a stated mechanism or a named artifact in the part the screen did not read.
Index 46's clause stops *at the trigger phrase*, so its recorded reason — "the
clause has no subject" — was true of the extract and false of the comment
(the need is the single word after it: "Uber"). Index 20's commenter names the
artifact **they built themselves**, with a URL. Index 19's mechanism is in the
sentence *before* the clause. Index 27's is the sentence after it. **`vague` is
withdrawn as a cause of death at its recorded size.**

**What survives is narrower and it is the more useful half.** All 13
disagreements are one-directional: the conservative reader's survivor-relevant
set is a **strict subset** of the other reader's, so no flip is contested. But
**F029's 0-of-50 stands**, because none of the 8 re-opened rows is a candidate:
two are features of products the commenters do not own (a Spotify playlist, a
Budibase roadmap item), one was already built by the commenter, one needs
per-vendor consent surfaces or a single browser fingerprint, one needs issuers
and regulators, one is a game port, and one is an open-source Uber that S
better classified as prior art. **The generator is closed for a repaired reason
rather than an unrepaired one** — D049 and D051 stand, and F029's 0 of 50 is now
confirmed by a re-read rather than carried forward.

**Three things it does not do.** No prior-art verdict moves: the 19 `prior_art`
rows were held out by design, because E016 already re-adjudicated that category
on three corpora with six positive controls, a stronger procedure than a second
prose reader. No candidate enters. And the restated six-category table is **not
usable** — B1 failed and the protocol says so, so no cause share from this
experiment is a fact.

**The transferable part is about gate design, and it is the sharpest instance of
`docs/policy/gate-falsification.md` in this record.** A post-hoc binary κ on the
split the gate actually asks about is **0.5412**, against 0.4627 for the six
declared labels, and the gap is entirely two readers disagreeing about *which*
non-survivor label a row takes (`still_vague` versus `not_a_software_need`) —
a disagreement that cannot change any decision. **A gate can ask about a grouping
its own categories do not deliver agreement on.** The pre-registered six-category
floor was the wrong floor, and the protocol said the table was inconclusive while
the per-row gate it also declared was unambiguous. D059.

**Ceilings.** Two readers from the same model family as the original screen,
blind to the labels but not to how the original phrased its reasons. 31 of
F029's 50 rows only. A clause-based verdict that survives re-reading is still
right for the clause: C1 says the rule moved verdicts at a rate that changes the
table, not that it was wrong for every row. One corpus, one platform, one
50-row sample.
