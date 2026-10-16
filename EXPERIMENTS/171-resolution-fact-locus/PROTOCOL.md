<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E171 — before G3 is run: is the resolution a fact the component's version history publishes?

Predeclared **before any row is classified and before any fetch**.

## Why this exists and what it is not

E168's G3 asks whether an attempt grounded in the component's **published
version history** recovers rows the unaided attempt fails, declared bar
≥ 0.60. G3 has never run because it needs a fresh blinded `version_pinned`
sample, because the session that read the 24 threads destroyed its own
blinding.

Running G3 costs a fresh Stack Exchange draw and 30 hand-written grounded
attempts. **Before spending that, the mechanism's own pre-condition has never
been tested: does the thread's resolution even consist of a fact that the
component's version history publishes?** If most resolutions are a
config key, an API surface, a local file permission, a third-party service's
behaviour, or "there is no fix yet", then no amount of version history
grounds the attempt, G3 is arithmetically unable to pass, and the sample is
never drawn.

This is a **pre-fetch screen on the experiment**, in E142's shape. It is not a
service screen, not a population estimate, and not an attempt.

## What is already committed (no new population)

| file | rows | use |
|---|---|---|
| `../168-version-pinned-need/classified.jsonl` | 299 | `vp`, `vp_sub`, title, tags, views |
| `../168-version-pinned-need/grades-unaided.jsonl` | 24 | the unaided attempt's served/unserved verdict **and the grader's stated reason** |
| `../169-version-pinned-reach/threads-all.json` | 78 | the fetched thread bodies and answers for the `vp=1` stratum |

**Reuse is declared and is the point.** Every population used here has been
read by a prior session. This experiment therefore measures a property of
**text already on disk**, not a capability, so it needs no blinding and no
fresh sample. That is exactly why it can run before G3 rather than after.

**Contamination is declared and does not bite here.** The reader has seen these
threads. The label is a property of the thread's text, not a prediction about
it, so pre-existing exposure cannot bias it in the way it biases an attempt.

## The question

For each row of the `vp=1` stratum that has a fetched thread, **what kind of
thing is the thread's resolution?** Six mutually exclusive classes, assigned
by reading the accepted answer (or the highest-scoring answer when none is
accepted), with the question body available for context:

| class | the resolution is… | version history can state it? |
|---|---|---|
| **`version_fact`** | a fact about *which version* of the named component introduced, removed, changed, or fixed something | **yes** |
| **`surface_fact`** | a fact about the component's *current* API/config surface — a setting key, a manifest element, an enum value, a method signature — true regardless of version | no |
| **`environment_fact`** | a fact about the asker's machine, account, permissions, file ownership, or OS state | no |
| **`thirdparty_fact`** | a fact about some other service's behaviour (a CDN, a proxy, a SaaS backend, a browser) | no |
| **`no_fix`** | the thread states no fix exists, or no fix had shipped | no |
| **`other`** | none of the above; describe in one line | — |

**`version_fact` is the only class E168's G3 mechanism can serve.** It is the
whole experiment.

### Assignment rule, written before the first row

- Read the **accepted** answer if the thread has one; otherwise the
  highest-scoring answer. Record which was used.
- Assign by the resolution's **operative content** — the step the asker must
  take — not by the post's shape. A row whose thread says *"upgrade
  EntityFrameworkCore.Design to 10.0.2 or greater solves it"* is
  `version_fact` even though the post never mentions a version.
- A resolution that contains a version **and** a surface fact is
  `version_fact`: G3's arm could serve it, so it counts in the arm's favour.
- `no_fix` is assigned when the thread says so, not inferred from the thread
  being unhelpful.
- One class per row. No `mostly` labels. Free text is recorded but never used
  to overrule the class.

## Gates, declared before any label exists

| gate | rule | reading if it fails |
|---|---|---|
| **G0 discrimination** | the classifier recovers **≥ 8 of 10** labels on a 10-row probe set whose classes were fixed **by the presence of an explicit operative sentence in the answer** (a version number in the operative step, or the absence of any). | the instrument does not discriminate; no rate is read and the screen is withdrawn. |
| **G1 (the pre-condition)** | over the **13 rows the unaided attempt failed** (E168's own unserved set, used as the denominator because G3's denominator is exactly this set): **`version_fact` ≥ 0.40**. | **G3 cannot pass its declared 0.60 bar** — the ceiling is below the floor — so E168's G3 is withdrawn **without drawing the sample**, and the version-pinned line closes as served-by-thread with the reason measured. |
| **G2 (the arm's complement)** | over the **11 rows the unaided attempt served**, `version_fact` share, reported against G1's. | not a gate; the comparison is the finding. If served rows are version-pinned *more* often than failed rows, version-pinning is a property of the venue and not of the failure, which strengthens the closure. |

**Kill gate: G1 failing withdraws E168's G3 and closes the line.** G0 failing
withdraws this screen. Nothing here can open a product.

## Why the bar is 0.40 and not 0.60

G3's declared bar is `grounded` serves **≥ 0.60** of the rows the unaided arm
fails. Grounding on version history can only ever help a row whose resolution
*is* a version fact, so `version_fact` share is a **ceiling** on G3. A ceiling
at or below the bar is decisive. 0.40 is declared as the bar because it is the
highest value that leaves a route open while still being far enough below 0.60
that G1 firing is informative — **and because the 13-row denominator makes
0.40 ≈ 6 rows and 0.60 ≈ 8 rows**, so the two are separated by two rows and
the Wilson interval is reported alongside.

## Controls

1. **G0 is the instrument's own positive control** and runs first. It is the
   ten rows where an explicit operative sentence makes the class readable
   without judgement; a classifier that cannot get those right has no business
   labelling the other 11.
2. **Served-vs-unserved split (G2)** is the negative direction: the same
   instrument on the 11 rows the assistant already served.
3. **A placebo on the reader** is not available (one reader), which is
   declared as a limitation rather than papered over.
4. **`version_fact` rates on both denominators are reported**, so no single
   rate can be quoted without its comparison.

## What this does not decide

- It does not measure whether version history is **reachable** — E170 already
  measured that a lexical query does not reach a fix (1/8, 2/13), and this
  screen says nothing about ranking.
- It does not claim a product, and **no prior-art screen is run**: G1 passing
  would license G3, not a build.
- One reader, no inter-rater agreement, 13 + 11 rows.
- The threads were fetched by E168/E169 with GitHub-link filters, so this
  population is biased toward rows whose resolution cites a tracker item.

## What it changes

Either **E168's G3 is withdrawn on its own pre-condition** and the
version-pinned line closes with the reason measured rather than asserted —
the cheapest closure this record could produce — or **G3 is confirmed
runnable** and `STATE.md`'s named next action becomes a fresh sample and 30
grounded attempts, with the ceiling on what those attempts can achieve already
on record.