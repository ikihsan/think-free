<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E144 — Electrical Engineering SE: the largest untouched non-software technical SE site with diagnostic needs

Predeclared **before any population row is fetched**.
Follows E143 (`../143-crossvalidated-service-test/`), which closed Cross Validated at served-share 1.0 and program-shaped residue 0.

## Question

On **Electrical Engineering Stack Exchange** (`electronics.stackexchange.com`) — the largest untouched non-software technical SE site where the practitioner is an electrical engineer or technician and resolutions are plausibly self-contained diagnostic procedures — what share of the highest-arrival recent unanswered questions is:

1. **diagnosis-shaped** (a specific circuit, component, or system exhibits a symptom; the question asks what is wrong or what causes it), and of those, what share is **answerable** (general knowledge suffices) versus **specific** (needs the asker's schematic, measurements, or environment, absent from the post)?
2. **execution-shaped** (the remedy is an action on the asker's own design, board, or system producing an artifact — redesign, component selection, calculation), split `program` (a self-contained script/tool the asker runs) versus `manual` (needs the asker's judgment, physical access, or equipment)?
3. of the **answerable diagnosis-shaped** class, what share does a free general assistant serve in full?

**Why this venue.** The venue sweep (E126/E127/E143) closed the Q&A venue classes: non-software SE (E062), Anova appliance (E091), Home Improvement appliance (E092), Stack Overflow (E126), Cross Validated (E143). All served; the program-shaped residue was 2% in SO, 0% in CV. Electrical Engineering SE is the largest untouched non-software technical venue (~200k questions) where:
- (a) the domain practitioner is an **electrical engineer or technician** — a domain expert, not a programmer;
- (b) the resolution is **plausibly a self-contained diagnostic procedure** (circuit analysis, fault isolation, component selection, calculation) — the only class a tool could serve, and the one the candidate-seat question needs;
- (c) the site is **large enough to justify a candidate** (> 50k questions).

Among qualifying non-software technical SE sites, **Electrical Engineering SE is the largest by question count** (~200k). Physics SE (~100k), Chemistry SE (~80k), and Aviation SE (~40k) are smaller. This rule was stated before any fetch.

**The new measurement.** The diagnosis-shaped share in a high-diagnostic-density venue, the answerable-class served share, and whether any execution-shaped `program` residue exists. E143 tested program-shaped residue in a computation-native venue (statistics) and found 0%. Electrical Engineering SE is a **diagnosis-native** venue — the native idiom is circuit fault isolation — so the diagnosis-shaped population is the primary signal, and any execution-shaped `program` residue (e.g., a script for component selection, BOM optimization, or thermal calculation) is the candidate signal.

## Domain selection rule (stated, not by comfort)

Among Stack Exchange sites — the platform class with the most validated instrument (public questions, `view_count` arrival metadata, answers as serving signal) — choose the site in a domain the mission has **not** measured as a need-venue, where:

- (a) the domain is **non-software technical** (the practitioner is an engineer, technician, or scientist — not a programmer);
- (b) the resolution is **plausibly a self-contained diagnostic procedure or computation** (circuit analysis, fault isolation, component selection, calculation) — the only class a tool could serve, and the one the candidate-seat question needs;
- (c) the site is **large enough to justify a candidate** (> 50k questions).

Among qualifying sites, choose the **largest by question count**.
Electrical Engineering SE (~200k questions) is the top hit under this rule.
Physics SE (~100k) and Chemistry SE (~80k) are the next candidates; both are science rather than engineering domains.
Aviation SE (~40k) is below the threshold and was partially probed via E091/E098 on different venues.

## Population and sample

- **Venue:** `site=electronics`, Stack Exchange API v2.3 (unauthenticated), the same surface E062/E079/E092/E126/E143 used.
- **Pool:** questions with `accepted=false` (no accepted answer) **and** `creation_date >= 2025-01-01` (unix 1735689600; recency declared so 2025–2026 methods are the population, not a decade of accumulated legacy).
- **Two arms, because the API cannot rank by `view_count`:**
  - **Arm A (votes):** `sort=votes&order=desc`, 2 pages of 100 (200 questions). The vote-stratum limitation is declared, not hidden (E033/E034, E126/E143's stratum finding).
  - **Arm B (creation):** `sort=creation&order=desc`, 1 page of 100 — the newest unanswered, a second stratum. Composition agreement between arms bounds the stratum concern; disagreement *is* the finding.
- **`view_count` is a covariate, never a selection rule** (E034/E113's lesson). The attempt sample is the top 20 by `view_count` **within** Arm A's diagnosis-shaped rows, after screening.

## Screening (title + body only, before any answer or comment is read)

Each row is classified by shape:

- **diagnosis** — a specific circuit, component, or system exhibits a symptom whose cause the asker does not know. Sub-class:
  - `answerable` — general knowledge suffices (textbook fault, known failure mode, standard calculation);
  - `specific` — the answer requires the asker's schematic, measurements, PCB layout, BOM, or environment, which the post does not contain.
- **execution** — the remedy is an action on the asker's own design, board, or system producing an artifact. Sub-class:
  - `program` — a self-contained script/tool the asker runs (component selector, BOM optimizer, thermal calculator, SPICE script generator);
  - `manual` — needs the asker's judgment, physical probing, soldering, equipment access, or vendor interaction.
- **other** — design review, component recommendation without symptom, purchase advice, code/firmware debugging, meta, opinion, off-topic, typo, or "debug this for me" with no general content.

**Crucial distinction from E143:** "component recommendation without symptom" is `other` (not diagnosis), because the asker knows what they need and is asking for a part choice. "My circuit does X but should do Y, what's wrong?" is `diagnosis`.

## Gates (declared before measurement)

| gate | rule |
|---|---|
| **G0 discrimination** | 20 construction-labelled probes (10 answerable diagnosis, 10 specific diagnosis), labels known by construction and independent of any thread. Pass: ≥ 9/10 answered, ≥ 9/10 declined. Fail: the instrument fails and no rate is read. |
| **G1 population** | the two arms together contain ≥ 60 diagnosis-shaped rows of ≥ 300 fetched. Fail: the class is too thin at high arrival; the line narrows and closes. |
| **G2 composition** | reported per arm and pooled, with Wilson CI95. No threshold — the mix is the finding. |
| **K1 served share** (answerable diagnosis class, n = 20) | Wilson CI95. Lower bound ≥ 0.50: served — the venue closes like the others. Upper bound < 0.50: an unserved answerable diagnosis population exists — the line reopens with the concrete reason. Straddling: extend the sample once, to 40 (E092/E143's rule). |
| **K2 execution share** | the execution-shaped share, pooled, with its `program`/`manual` split. Reported, not gated: it is the measurement the venue exists to produce. |
| **K3 program-shaped residue** | count of rows whose remedy is a self-contained program, across all screened rows. Zero: no program-shaped population exists regardless of shares (E091/E143's K2 shape). |

## Attempt discipline (E091/E143's defects carried forward)

1. Attempts are written from title + body, from general knowledge only — no web, no thread content — and committed to `attempts.jsonl` **before** any answer or comment is read. Every row carries an explicit `attempt_first` flag.
2. Grading reads the thread (answers, accepted answer, comments) and grades served/unserved with a reason; every row's flag is checked against its own reason (E091 defect 2).
3. Every denominator is filled before any rate is computed (E091 defect 3).
4. The attempt arm is the same model family as the grader (the E062/E091/E092/E126/E143 shape) — declared as a limitation, not hidden.

## Served definition (E092/E143's, unchanged)

**Served:** the attempt names the likely fault and the action that resolves it, at the specificity the thread's own resolution reaches, and is consistent with the thread's converged answer.
**Unserved:** wrong fault, vacuous ("could be many things"), or a correct resolution that requires information not in general knowledge (per-design schematic, unshared measurements, vendor-only datasheet, proprietary firmware).

## What this does not establish

- Two strata, not the whole pool; vote-sorted and creation-sorted arms over-represent their strata (E033/E034's lesson, declared).
- One reader (the session's model); no human baseline.
- `accepted=false` means no *accepted* answer; threads may still carry converged answers, which grading uses.
- The diagnosis share and execution share are properties of this venue's curation and population as much as of the need.
- A high-diagnosis-density venue is not the only venue where a diagnosis-shaped unserved population could be large; it is the largest such untouched venue.

## Decision this changes

Either E144 supplies the composition that every future high-diagnosis-density-venue screen needs — and, if the answerable diagnosis class is unserved or the execution-shaped `program` residue is large and unserved, a concrete population a tool could serve — or it extends the composition finding to the largest untouched non-software technical venue and closes the candidate-seat question more firmly. Both outcomes are recorded as such.