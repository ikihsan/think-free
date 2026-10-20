<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E168 — the version-pinned class: is it a population, and does the strongest
# alternative fail on it?

Predeclared **before any row of the pool is classified** and before any
attempt is written. Follows E091/E092/E126/E143's service design and
D103's composition rule (unserved share is a property of what a community
owns).

## The observation that prompted this

E126 graded 40 blind attempts on Stack Overflow and read 13 of them unserved.
The record wrote only "Stack Overflow is served at 0.6750" and never
characterised the 13. Reading those 13 reasons on 2026-10-16, every one is
the **same shape**: the assistant named the fault *category* and got the
**version-pinned fact** wrong or could not name it at all.

> "Diagnosis correct (Spring Boot 4 restructured) but cannot name resolution —
> explicitly states 'I do not know the exact new package.'" / "Diagnosis WRONG —
> attempt says 'no public API to revert.' Thread converged on
> UIDesignRequiresCompatibility in Info.plist." / "Attempt says 'JetBrains plugin
> does not read .github/copilot-instructions.md.' Thread: feature IS supported
> (version 722431+)."

That is a **positive structural finding**, and this mission has none: after
seven service closures every row was unanswerable-in-principle, and the read
was "the strongest alternative serves it." If this shape holds it says the
alternative fails for a reason with a name and a remedy.

## Question

1. **G1 (sizing).** In a 300-row high-arrival Stack Overflow pool, what share
   of rows are **version-pinned** — the resolution depends on a fact whose
   truth varies by component version or by the asker's local environment,
   rather than on a version-invariant fact?
2. **G2 (the alternative).** On blind attempts over version-pinned rows, what
   share does a free general assistant serve in full, against a control arm of
   non-version-pinned rows drawn the same way?
3. **G3 (mechanism — the product gate).** Of the version-pinned rows the
   unaided attempt gets wrong, what share is recovered by an attempt grounded
   in only (a) the post and (b) the component's own **published version
   history**, which is the artefact a tool could retrieve automatically?

## Population

- **Pool:** `EXPERIMENTS/126-stackoverflow-service-test/screening.jsonl`,
  300 rows, already fetched, hashed and committed. No new fetch.
- **Reuse is declared.** E126 read 40 of these rows' threads and graded them
  (`grading-results.jsonl`). Those 40 are **excluded from the G2/G3 sample** and
  reported separately; G1 is reported on all 300 and on the 260 ungraded rows.
- **Declared exposure:** two rows of this pool (indices 1 and 2 of the file:
  a Docker/Zscaler macOS warning, a YouTube Error 153 embed) were seen while
  establishing the file's schema, before this protocol. Both stay in the pool
  and both are flagged in the classification output.

## Classification rubric (`version_pinned`), applied to title+body only

Assign each row `vp = 1` **iff both** hold:

- **(C1) version- or environment-dependent.** The resolution depends on a fact
  that is true of *some* versions and false of others — existence of an API or
  flag in a named release, a renamed/moved package or import path, a syntax or
  configuration key introduced/changed/removed in a release, a changed default,
  or the version the asker's own dependency graph actually resolves. The fault
  category alone does not qualify.
- **(C2) knowable outside the post.** The fact is not the asker's private code,
  data, or business logic. (If C1 holds but the fact is only in the asker's
  code, `vp = 0`, sub-label `private`.)

Rows with `vp = 1` take exactly one sub-label:

- **`docs`** — the varying fact is published in the component's own version
  history (release notes, migration guide, changelog, versioned API reference).
- **`local`** — the varying fact is what the asker's own resolved state is:
  which version a lockfile pins, which transitive version wins, what a manifest
  resolves to. Knowable from a manifest, not from documentation.

Tie-break order: `local` over `docs` (a row needs the asker's resolved graph
either way); `private` over both for `vp = 0`. Work from title+body only; do
not open a thread, an answer, or a comment during classification.

## Arms and blinding

- **Sample:** up to 30 `vp = 1` rows not in E126's graded 40, drawn by a stated
  rule (descending `view_count` within the classification result, which is the
  same arrival rule E126 used). Floor 24 rows; below that the run is
  `underpowered`, reported as such.
- **Two attempts per sampled row, both written blind** (attempt written before
  any thread, answer, or comment is read; `attempt_first = True` recorded):
  - **`unaided`** — from general knowledge. This is E126's instrument verbatim
    and is the strongest accessible alternative as this mission has measured it
    in six venues.
  - **`grounded`** — same writing, but the writer may additionally consult only
    (a) the post's own text and (b) the component's **published version
    history** for the version the post names. Nothing else; no thread, no
    search results, no local state inspection. This arm stands in for what a
    retrieval tool would put in front of a model.
- **Then** threads are read and both arms are graded by the E126 rubric:
  `served` requires the attempt to converge on the thread's resolution, or name
  the correct fault *and* a resolution consistent with it. One reader, as in
  every prior run.

## Gates, declared before any number exists

| Gate | Condition | Meaning if it fails |
|---|---|---|
| **G1** | `vp = 1` share ≥ 5.0% of 300 (≥15 rows) **and** Wilson 95% lower bound > 2.0% | not a population; E126's program-shaped residue (2.0%) was the bar and this must clear it. Class closes. |
| **G2** | assistant-served on `vp = 1` ≤ 0.50 **and** ≤ control share − 0.20 | the alternative serves this class like the rest; no structural failure to exploit. |
| **G3** | of `vp = 1` rows the unaided arm fails, `grounded` serves ≥ 0.60 | grounding on the component's own version history is not the mechanism; no product follows. |

**Kill gate: G1 or G3 failing closes the class.** G2 failing closes the
"structural failure" reading but leaves G3 measurable — the two are reported
separately and G2 never masks G3.

**Self-falsification the run must survive.** The classifier is the instrument,
so a re-read of 20 sampled rows by the same reader after the first pass must
reproduce `vp` on ≥ 18 of 20; the first-pass label is kept, never the re-read,
for every number in this report.

## What this does not decide

- It does not claim a product. G3 establishes only that version-history
  grounding changes answers on rows where the unaided arm fails.
- It does not reopen any killed candidate (`stg`, `preflight`).
- It does not re-open E126's closure of Stack Overflow. E126 measured the
  venue's answerable class; this measures one class inside it.
- It does not test adoption, distribution, or willingness to pay.