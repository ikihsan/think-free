<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E091 Amendment 1 — the block is false, and two instrument defects are in the committed data

Written **before** any assistant judgement on this population, and before the
thread outcomes were re-read. Session `2026-10-11-003`.

## 1. The stated block does not hold

`VERDICT.md` records the experiment as **BLOCKED — no GPT-4o or Claude 3.5
Sonnet API access**. Three things in this repository contradict that:

- `PROTOCOL.md` line 26 defines the instrument as *GPT-4o, Claude 3.5 Sonnet,
  **or equivalent***.
- `EXPERIMENTS/066-need-answerability/PROTOCOL.md` line 29 defines the same
  instrument as *"the reader (this model) attempts each need against its own
  knowledge — the strongest accessible free alternative"*, and E062 used the
  identical construction.
- The agent running this session **is** a general-purpose assistant answering
  from its own knowledge. That is the instrument E062 and E066 already ran.

So the experiment was not blocked on infrastructure; it was blocked on a
narrower reading of its own protocol than the protocol states. `assistant_query.py`
is a placeholder that prints the block message and exits 0 — a script whose
success path is the block itself.

**Consequence for the record.** One whole experiment line, and the task that
carried it (T-0090, marked `status: done` with the block recorded in its
notes), stood unrun behind a condition the record already met twice.

## 2. Defect A — every stored `first_post` is truncated at 200 characters

All 20 population rows and all 20 probe rows store a `first_post` cut at ~200
characters. Re-fetching the full first post from the Discourse API:

| | characters |
|---|---|
| on disk, 20 population rows | 3 959 |
| re-fetched, same rows | 10 326 |
| **fraction retained** | **0.383** |

Nine of 20 rows do not even match their own full text as a prefix, because the
cut lands mid-word (`"...but, I"` for topic 26273). Running the instrument on
that text measures *whether an assistant can answer a truncated problem
statement*, which is a different and easier question than the one declared.
The defect biases **toward `unserved`** — an assistant shown half a question
answers less often — so it would have moved K1 in a known direction.

Repair: re-fetch full first posts. Digests of both versions are in
`fetch.py --verify`.

## 3. Defect B — 19 of the 20 calibration probes ARE the 20 population rows

`PROTOCOL.md` G0 asks for 20 probes, noting they "can be outside the top-20".
In the committed data they are not: **19 of 20 population ids also appear in
`probes.jsonl`**, the twentieth (`86`) being the only population row absent.

Consequences, both of which the mission's own record already names:

- **G0 and K1 measure the same rows.** A discrimination gate and the
  measurement it licenses cannot be the same 20 rows; agreement between them
  is not independent evidence. This is F049's shape — *a test's population is
  part of the property it checks*.
- **The probe labels are the contested quantity.** `probes.jsonl` labels a row
  `unserved` when *the thread ends unresolved*. F096's finding is precisely
  that **unanswered on a platform is not unserved** — 17 of 20 thread-unremedied
  needs were answered anyway. Calibrating "can the instrument answer this"
  against "did the thread resolve" assumes the proposition under test.

Repair: G0 is rebuilt on labels known by construction, independent of thread
outcome (§4).

## 4. Corrected design

**Arm A — tool-shapedness, run on all 20 rows, reported as a parallel screen.**
E062's G3 rubric applied to every row: is the remedy a self-contained program
(not contact-the-vendor, not a hardware repair, not waiting for a firmware
fix)? It answers a *different* question from Arm B, so it does not gate it.

> **Design correction, made before any rubric was applied to any row.** This
> amendment originally declared Arm A as a gate that could "end the experiment
> before the expensive arm runs", with Arm B on survivors only. That was wrong
> and it is recorded rather than quietly fixed. F096 is a claim about assistant
> answerability; Arm A is a claim about tool-shapedness. Letting Arm A end the
> run would report a tool-shapedness result under a replication heading. K1 and
> K2 need all 20 rows, so Arm B now runs on all 20, and Arm A is reported
> beside it. The purpose Arm A actually serves is stated below.
>
> No rubric had been applied to any row when this correction was made.

**Arm B — assistant answerability, on all 20 rows.** The instrument is this
model, per E062/E066. Three changes make it checkable rather than
self-graded:

1. **Answers are written before thread outcomes are read**, and hashed. Grading
   then compares a fixed text against the thread rather than a judgement made
   after seeing the answer key.
2. **Grading is against the thread, not against confidence.** For a resolved
   thread, `served` means the attempt contains that fix or an equivalent
   correct one. For an unresolved thread, the attempt is graded on whether it
   is a specific, correct, actionable remedy, and the reasoning is recorded
   per row.
3. **Prior exposure is declared, not hidden.** While inspecting the repaired
   data I read the full threads of 3 of the 20 rows (`12736`, `4261`, `9165`)
   before writing any attempt. Those 3 are marked `prior_exposed` and reported
   apart; the headline number is over the **17 unexposed rows**, with the
   full-20 figure given alongside. This is F049/D061's rule applied to the
   reader rather than to a fixture.

**Why Arm A is still worth running.** If K1 fails — if a general assistant
serves *less* here than on Stack Exchange — the interesting question becomes
whether the residual is a population a program could serve. A venue where needs
genuinely go unserved but whose remedy is a bent impeller is not a candidate
route, and Arm A is what distinguishes those two outcomes.

**Gates (declared before the run).**

| gate | condition | if not met |
|---|---|---|
| **G0 discrimination** | on probes whose labels are known by construction and independent of thread resolution, the instrument recovers ≥ 8 of 10 answerable and ≥ 8 of 10 unanswerable | the instrument does not discriminate; the served share is not reported |
| **A1 population** | ≥ 20 rows with full (untruncated) first posts and recorded digests | the stored population cannot support the measurement; stop |
| **K1 served share** | Wilson CI95 lower bound ≥ 0.50 | F096 does not replicate in this venue |
| **K2 vs E062** | cannot reject E062's 17/20 = 0.85, CI95 [0.621, 0.948] | the venue confound is real |

**Ceilings, stated now.** One reader (this model) serves as both instrument and
judge — E062's protocol asked for two readers after F049, and that is a
departure, not a repetition. A frontier model is a **stronger** assistant than
the median free one a reader would reach, so a high served share is an upper
bound on what an ordinary reader would experience. Arm A's rubric is likewise a
single reader's application of a three-clause test.

**What this experiment cannot produce.** It does not produce a candidate. E062's
own protocol says so and this one repeats it: the outcome is a number about how
many stated needs a free assistant serves, in a venue where the assistant is
weakest.
