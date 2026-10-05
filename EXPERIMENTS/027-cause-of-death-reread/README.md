# E027 — is F029's cause of death an artefact of the clause extractor?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Date:** 2026-10-05. **T-0071.** Protocol in
[`PROTOCOL.md`](PROTOCOL.md), written before any row was classified. Numbers
from [`results.json`](results.json), computed by `stats.py` from the two
captures and from E012's committed population.

**Verdict: the kill gate fires and the agreement gate fails.** Eight of the 31
clause-killed rows are survivor-relevant to **two readers working
independently** from the full comment, and the more conservative reader's
survivor-relevant set is a **strict subset** of the other reader's — no flip is
contested. At the same time Cohen's κ over the six declared categories is
**0.4627**, below the pre-registered floor of 0.6, so **the restated cause
table is inconclusive and no cause share is reported as a fact.**

## The belief under test

F029 screened 50 mechanically-drawn Hacker News need statements and **0
survived**: `prior_art` 19, `vague` 15, `not_a_software_need` 12,
`needs_hardware` 4. That result closed the live-need generator (D049, D051),
emptied item 0d's invention seat, and is carried in four files as a fact about
the world's stated needs.

**31 of the 50 verdicts were assigned from a clause, not from a comment.**
`sample_needs.py::clause()` takes *the text between the matched trigger phrase
and the first sentence break*, capped at 300 characters. Two consequences were
visible in the committed file before this protocol existed:

- **13 of the 31 carry at least 20 further words of comment** the screen never
  read. The median residual across all 50 is 0, so this is a minority shape.
- **3 of the 50 clauses are not substrings of their own text** — all from the
  cap or the sentence split.

And one recorded reason is a claim about the whole document made without
reading it: index 10's verdict asserts *"no mechanism stated anywhere in the
comment"*. F030 established that a prior-art verdict from one query is wrong in
both directions; this is that shape one stage earlier.

## Method

| step | script | what it fixes |
|---|---|---|
| population | `population.py` | the 31 clause-based kills, with `cause`, `reason` and `name` **stripped**; `--selftest` asserts the rule and the absence of any leaked field |
| reader R | `raw/reader_r.jsonl` | all 31 rows from the full comment, blind; committed to git before reader S existed |
| reader S | `raw/reader_s.jsonl` | all 31 rows again, blind to the original verdict **and** to R |
| report | `stats.py` | every number, from the captures only |
| falsify the gates | `recheck.py --selftest` | C1 and B1 against fabricated populations, in both directions |

**Two readers, because F044 named that as its own ceiling.** E024 counted 20
kill reasons with one reader at a one-row margin; E023 measured κ = 0.923 for a
second reader on an identical population and that number changed what the
experiment was allowed to say.

## Results

| gate | declared | observed | verdict |
|---|---|---|---|
| **A1** | 31 rows, each with non-empty text | 31 of 31, no leaked field | pass |
| **B1** | Cohen's κ ≥ 0.6 over six categories | **0.4627** (po 0.5806, pe 0.2196, 18/31) | **FAILS — restated table inconclusive** |
| **C1** | fires at ≥5 rows survivor-relevant to **both** readers; refuses at 3–4; dead at ≤2 | **8 of 31**; union of either reader 15 | **FIRES** |

### The eight convergent flips

Both readers independently put these in a survivor-relevant category from the
full text. Six of the eight were killed `vague`.

| idx | original | R | S | what the clause cut |
|---|---|---|---|---|
| 2 | `vague` | mechanism_stated | mechanism_stated | "weight them accordingly in a quick access list on the home screen" |
| 11 | `needs_hardware` | mechanism_stated | mechanism_stated | an age proof that survives government, IdP and site collusion |
| 15 | `vague` | mechanism_stated | mechanism_stated | the sentence naming the browser as the leak vector |
| 19 | `vague` | mechanism_stated | mechanism_stated | the sentence *before* the clause: "Time for a modernized port" |
| 20 | `vague` | **self_built** | **self_built** | the commenter names the artifact they shipped, with a URL |
| 27 | `vague` | mechanism_stated | mechanism_stated | "use an Automation our RPA, zapier-like section… parameters" |
| 37 | `vague` | mechanism_stated | mechanism_stated | the automation workflow proposed after the wish |
| 46 | `vague` | mechanism_stated | prior_art | the entire need is one word after the clause: "Is there an open source **Uber**" |

**6 of the 15 `vague` kills are not vague.** Index 46's clause stops at the
trigger phrase, so the recorded reason — *"the clause has no subject"* — was
true of the extract and false of the comment.

### The structure of the disagreement, which is the usable half

The 13 disagreements are **all one-directional**. Reader R's survivor-relevant
set is a **strict subset** of reader S's; the difference is rows S read more
generously (11, 17, 43) and rows S routed to `prior_art` where R saw no artifact
(10, 29, 44, 46). **No row that R called survivor-relevant is disputed by S.**
That is why the gate was declared per row and not over the table.

A **post-hoc binary κ** on the split the gate actually asks about is **0.5412**
— still below the declared floor, reported as structure and **used in no
verdict**. It is recorded because it is the sharpest instance in this record of
`docs/policy/gate-falsification.md`'s subject: **a gate can ask about a grouping
its own categories do not deliver agreement on.** The declared six-category κ
is partly depressed by two readers disagreeing about *which* non-survivor label
a row takes — `still_vague` versus `not_a_software_need` — which cannot change
any decision.

## What this does and does not change

**`vague` is withdrawn as a cause of death at its recorded size.** Six of its
fifteen rows state a mechanism or an artifact in the comment the screen did not
read. The category was measured on an extract, and the recorded reason for one
row asserts a property of a document that was never read.

**F029's 0-of-50 survives its own repair, and that is the more useful result.**
Eight rows would now go forward to Screen 1 and Screen 3. Read against the
comments, none is a candidate:

- **idx 2** and **idx 27** are features of products the commenters do not own —
  a Spotify home-screen playlist and a Budibase roadmap item.
- **idx 20** was already built by the commenter, which is F045's builderhood
  finding landing inside the very population F029 declared had no standing need.
- **idx 46** is an open-source Uber, and S's `prior_art` reading is the better one.
- **idx 19** is a game port; **idx 37** needs per-vendor consent surfaces;
  **idx 15** is one browser fingerprint; **idx 11** needs issuers and regulators.

So the generator is **closed for a repaired reason rather than an unrepaired
one**: 8 of 50 rows change category, 0 become candidates, and `prior_art`
remains the largest cause. D049 and D051 stand. **F029's 0 of 50 is confirmed
by a re-read, not merely carried forward.**

**No prior-art verdict moves.** The 19 `prior_art` rows were held out by design,
because E016 already re-adjudicated that category on three corpora with six
positive controls — a stronger procedure than a second prose reader.

## Ceilings

- **Two readers from the same model family as the original screen.** They are
  blind to the labels, not to how the original phrased its reasons. E016
  declared the same limit for itself.
- **The restated six-category table is not usable.** B1 failed and the protocol
  says so; no cause share from this experiment is a fact. What survives is the
  convergent subset, which is a smaller claim than a table and the only one the
  protocol licenses.
- **A clause-based verdict that survives re-reading is still right for the
  clause.** C1 says the rule moved verdicts at a rate that changes the table;
  it does not say the extractor was wrong for every row.
- **31 of F029's 50 rows only.** This cannot be read as a full re-screen of
  F029, and the 19 held-out rows are the reason.
- One corpus, one platform, one 50-row sample drawn by E012's stated rule.