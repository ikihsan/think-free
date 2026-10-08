<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E057 — Outside developer tooling, does one practical step recur and go unserved?

`observed` 2026-10-08, session 2026-10-08-005, VM `instance-20260717-0947`.
Protocol declared before the fetch: [`PROTOCOL.md`](PROTOCOL.md).

## Verdict

**`KILL`. G1 holds and G2 fails, so the pre-registered decision rule builds nothing.**

| gate | result |
|---|---|
| **G1 population** | **PASS, decisively.** The same step — *identify a physical object from partial evidence when its label is lost* — recurs in **three independent sites**. Bricks: 51 rows from **49 distinct requesters** in the score tail and 43 from 39 in the top tertile. Bicycles: 17/16. Biology: 8/8 tail and 22/22 head. Within Bricks, **19 distinct requesters state the goal in their own words** — 19 of 60 bodies read say *instructions*. |
| **G2 serving** | **FAIL.** Incumbents perform the step, and one of them is a peer-reviewed method. |
| **G3 verdict** | Not reached for the served clusters. Reached only for Bicycles, where it **fails**: an unbranded frame has no ground truth, so the step's correctness is not decidable from artifacts. |

No candidate is opened. What E057 leaves is an instrument, a positive
recurrence result this mission has never had outside developer tooling, and one
correction to a rule the mission has been relying on.

## Population and stratum, as run

`observed`. 365 sites enumerated from the API's own site list; 50 survive the
**published** exclusion list; the **12 alphabetically first** are the population,
chosen before any question text was read: 3D Printing, Amateur Radio, Arqade,
Arts & Crafts, Beer/Wine/Spirits, Biblical Hermeneutics, Bicycles, Bioacoustics,
Biology, Bricks, CS50, Community Building. Stratum: open, no accepted answer, 36
months from 2023-10-24, 100 per page, two arms (votes ascending = score tail;
descending = top tertile, **control B1**). **24 arms, 3992 rows, 3361 unique
question ids, 2336 distinct requesters.** Raw rows in `raw/`, unedited.

A correction to this session's own stream: one session milestone recorded "4,392
rows" from an estimate before the fetch was measured. The measured total is
**3992**. The estimate is not evidence and the README supersedes it.

## G2 — what serves the step

`source-supported`, read from Wikipedia's *Rebrickable* article (a tertiary
source; the primary sources are its references) on 2026-10-08, not from a search
engine, which was returning `cancelled` for every query this session:

- **Brickognize** — "Brickognize: Applying Photo-Realistic Image Synthesis for Lego
  Bricks Recognition with Limited Data", *Sensors* 23(4):1898, 2023,
  doi:10.3390/s23041898. Identifying LEGO bricks from a photo is a **published
  method**, not a gap.
- **RebrickNet** — "an artificial intelligence system for detecting Lego parts in
  photos", shipped by Rebrickable.
- **Brickit** — a physical machine that sorts loose bricks by type and colour,
  listed among the field's software.
- **BrickLink, Brickset, LEGO Builder** — the databases the requesters themselves
  name in the corpus.

**The population names 4 tools in 60 bodies, and all four are these.** So G2 fails
on the corpus's own evidence, not on a search result — which is the discipline
D077 asks for, and it happened to hold here.

This is F082's shape exactly: reading the corpus named the incumbents. What is
new is the rate at which it did so, below.

## What the corpus says about incumbents' quality

`observed`, and reported separately from the gates because a gate verdict and a
quality observation are different claims. 10 of 60 Bricks bodies say the requester
already tried something. What they report:

- *"I tried to use Brickognize but of course I just get the generic police torso
  in the results."* — q19136
- *"I have scanned through Bricklink and I cannot find this part. I can not
  determine what to even call it."* — q18613
- *"I have tried using LEGO Builder and Brickset"* — q19162, with no result stated
- *"No luck online."* — q18622

**Demand for something better is real and in the requesters' own words.** It does
not survive G2, because G2 was declared as *0 incumbents perform the step* and
that is false. A claim that incumbents fail often enough to be worth replacing is
a **different, untested claim**, and it is not what this protocol measured.

## G1 is a weak gate, and that is the reusable part

`observed`. G1 asked for ≥8 distinct requesters in one site. It was met at **19** on
the first read of the first site's bodies, with no effort and no threshold tuning.
Across the three G1 clusters the step is present in **both** arms at similar rate
(identifying rows, tail vs head: Bricks 51/43, Biology 8/22, Bicycles 17/5).
**All the discriminating power in this protocol sat in G2 and G3.** G1 measures
that a step is *recurring*, which in a corpus of 2336 requesters asking about
their own practice is close to free. A gate that is cheap to pass should not be
counted as a screen that did work; the three-way gate reads as a screen because
the second and third gates are expensive and decisive, not because all three are.

## The score-tail rule does not transfer (E033)

`observed`. E033 measured recurrence at 4.5× the Active tab's rate in the score
tail and near zero in the top tertile, and the mission has leaned on that to read
demand from low-scoring questions. Here the two arms carry **100 identifying rows
from 97 requesters (tail) against 103 from 96 (head)** — indistinguishable. The
tail rule was measured on developer tooling and does not carry to a non-developer
population. Denoiminators match (equal page budget per arm, 3 exceptions below),
so this is a rate-per-question comparison, not a population-weighted one.

**Control B1 is void in 3 of 12 sites**: Beer/Wine/Spirits (30 rows), Bioacoustics
(155) and Community Building (11) have so few unanswered questions in the window
that the ascending and descending arms return the identical set. Declared in
advance as a control; it holds in 9 of 12.

## The instrument

`observed`, in [`cluster.py`](cluster.py), [`steps.py`](steps.py),
[`read.py`](read.py), [`diagnose.py`](diagnose.py), [`sensitivity.py`](sensitivity.py).

**The first linkage was wrong and returned a clean zero.** Greedy average-link
over title token sets at J≥0.25, 0.3, 0.34, 0.4, 0.5 produced **0 clusters at
every threshold in both arms** — a result indistinguishable from "no recurring
step exists". `diagnose.py` showed why, and this is worth keeping: on 6-token
titles only **3143 of 19900** pairs share any token at all, and the true same-step
pairs sit at **J=0.40–0.62** (*"Gaps in walls during printing"* ↔ *"Print walls
coming out with gaps/holes"*, 0.50). Sparse graphs do not assemble eight
neighbours by pairwise linkage. Replacing it with connected components of the
token co-occurrence graph (`edge` in 2…6) recovers **8 concepts with ≥8
distinct requesters per arm**, and the count is stable across the whole sweep.

**Sensitivity is declared, not assumed.** `sensitivity.py` injects 12 titles
describing one step, from 12 synthetic user ids, into a real arm and requires the
instrument to recover all 12. Face validity on real data is the hand-read sheet
`handread-template.md`: a cluster is one *step*, not a topic, and that judgement
is made by reading titles, before any body text.

**Two probes were near-vacuous and are recorded as such.** The PHYSICAL-PROCEDURE
shape in `steps.py` fired on 23 rows across the whole corpus, because it requires
a verb from a fixed 15-item list; it is not evidence of absence. And the custom
API filter string that first made every fetch exit 400 was silently dropping the
whole instrument — worth remembering that an HTTP 400 reads as a finding until it
is read as an error.

## What this does not close

- **The population is 12 sites of 365**, self-selected questioners, English, and a
  question is a *formulable* need. F060 measured that this corpus's parent answers
  57% of its statements. A null here does not establish that no unserved step
  exists; it establishes that **this channel does not show one**.
- **Title-level clustering reads a question's framing, not its practice.** Every
  G1 cluster is a hypothesis that was read, and the reading is mine.
- **The exclusion list is a set of priors**, published in `PROTOCOL.md` so it can
  be argued with. `music` and `retrocomput` are known over-reach: neither is
  developer tooling.
- **Web search returned `cancelled` for every query this session.** G2 therefore
  rests on one tertiary source. It is enough for a kill against a peer-reviewed
  method paper, and it is not a systematic prior-art sweep.
- **Nothing was built, released, or contacted.** Reading public text was the whole
  instrument.

## Reproduction

```
python3 EXPERIMENTS/057-unserved-step/fetch.py       # raw/sites + 24 arms + index.json
python3 EXPERIMENTS/057-unserved-step/diagnose.py    # why the first linkage returned zero
python3 EXPERIMENTS/057-unserved-step/cluster.py     # raw/clusters.json, the EDGE sweep
python3 EXPERIMENTS/057-unserved-step/steps.py       # hits-identify-unknown.txt
python3 EXPERIMENTS/057-unserved-step/bodies.py      # bodies-{bricks,bicycles,biology}.json
python3 EXPERIMENTS/057-unserved-step/read.py        # read-*.txt, read-index.json
```
