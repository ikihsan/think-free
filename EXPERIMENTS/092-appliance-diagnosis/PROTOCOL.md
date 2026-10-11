<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E092 — appliance-fault diagnosis as a general need, outside one vendor's forum

Session `2026-10-11-004`. Declared before any population row is
read. Follows E091 (`../091-anova-answerability/`, F114, D103),
whose §6 named this test.

## Question

On a **multi-vendor knowledge venue** — Home Improvement Stack
Exchange, tag `appliances` — what share of the highest-arrival
unanswered appliance-fault **diagnosis** needs is answerable-class,
and what share of those does a free general assistant serve in
full?

D103's reopening condition: a venue whose ownership mix is
reported, whose answerable-class unserved share clears the gate
after vendor- and repair-bound rows are screened out, and whose
population contains a program-shaped remedy.

## Why this venue

Multi-vendor, unlike Anova (one vendor's forum). It exposes
`view_count` — independent arrivals — through the same public
Stack Exchange API E062 and E079 exercised. Its curation closes
pure product-support questions, so the venue also tests whether
E062's 17-of-20 on non-software Stack Exchange extends to the
appliance-diagnosis class specifically.

## Record repair carried into this protocol

E091's `RESULT.md` §3 and F114 describe E062's 17/20 population
as "Steam". That is false. E062's `AMENDMENT-1.md` retired the
Steam arm **before any row was fetched** (Valve's per-game
feature-request boards no longer exist; the probe is
`raw/steam-probe.json`), and the 17/20 was measured on six
non-software Stack Exchange sites — the top-20 by view_count
being 12 `diy`, 4 `woodworking`, 2 `cooking`, 1 `gardening`,
1 `bicycles` (`raw/answerability-top20.tsv`). The 0.85 is a
number about a mostly-physical-domain **knowledge** population,
not a software population. E091's own composition finding stands
on its own 20 rows; the contrast it drew is corrected in place
in F114 and `RESULT.md`.

## Population and sample

- **Pool:** questions on site `diy`, tag `appliances`,
  `answered=false` (no accepted answer), fetched via
  `/2.3/search/advanced`, all pages, ranked by `view_count`.
- **Screening** (title + body only, before any answer or comment
  is read): each row is classified
  - **shape** — `diagnosis` (a specific device exhibits a symptom;
    the question asks what is wrong or what causes it) or `other`
    (installation, wiring, purchase, technique, code, …);
  - for diagnosis rows, **remedy class** (E091's taxonomy):
    `answerable` (knowledge, or an action the asker can take
    alone), `repair` (needs a physical repair or artifact),
    `vendor` (return, account action, product decision, vendor
    software fix).
- **Sample:** the 40 highest-view_count diagnosis-shaped rows.

## Gates (declared before measurement)

| gate | rule |
|---|---|
| **G0 discrimination** | 20 construction-labelled probes (10 answerable, 10 unanswerable), labels known by construction and independent of thread outcome. Pass: ≥ 9/10 answered, ≥ 9/10 declined. Fail: the instrument fails and the numbers are not read. |
| **G1 population** | the top 150 by view_count of the unanswered pool contains ≥ 40 diagnosis-shaped rows. Fail: the class is too thin at high arrival; the line narrows and closes. |
| **G2 composition** | reported for every row (required by D103, no threshold). The mix is the finding. |
| **K1 served share** (answerable class) | Wilson CI95. Lower bound ≥ 0.50: served by the general assistant — **the line closes for good**. Upper bound < 0.50: an unserved answerable-class population exists — **the line reopens** with the concrete reason. Straddling: extend the sample once, to 80 rows. |
| **K2 Arm A** | count of rows, across all 40, whose remedy is a self-contained program. Zero: no candidate exists regardless of K1 (E091's shape). |

## Attempt discipline (E091's defects carried forward)

1. Attempts are written from title + body, from general
   knowledge only — no web, no thread content — and committed to
   `attempts.jsonl` **before** any answer or comment is read.
   Every row carries an explicit `attempt_first` flag.
2. Grading reads the thread (answers, accepted answer, comments)
   and grades served/unserved with a reason; every row's flag is
   checked against its own reason (E091 defect 2).
3. Every denominator is filled before any rate is computed
   (E091 defect 3).
4. Fisher exact uses the implementation pinned in
   `../091-anova-answerability/test_fisher.py`, checked against
   exhaustive enumeration — not a fresh tail (E091 defects 4–5).

## Served definition

**Served:** the attempt names the likely fault and the action
that resolves it, at the specificity the thread's own resolution
reaches, and is consistent with the thread's converged answer.
**Unserved:** wrong fault, vacuous ("could be many things"), or a
correct resolution that requires information not in general
knowledge (per-model service spec, vendor-only part, code
compliance).

## What this does not establish

One venue, one reader, 40 rows; the attempt arm is the same
model family as the grader (the E062/E091 shape); the
composition is a property of the venue's curation rules as much
as of the need, which is exactly what G2 reports.

## Decision this changes

D103's reopening condition. Either E092 supplies the concrete
reason that reopens appliance-fault diagnosis as a route — a
program-shaped remedy in an unserved answerable-class population
— or it closes the line for good.
