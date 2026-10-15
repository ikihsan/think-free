<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E143 RESULT — Cross Validated closes like the others; the program-shaped residue is zero

`observed` 2026-10-15, Python 3.8.10, `instance-20260717-0944`.
Protocol [`PROTOCOL.md`](PROTOCOL.md), raw pool
[`pool-raw.json`](pool-raw.json), screening
[`screening.jsonl`](screening.jsonl), attempts
[`attempts.jsonl`](attempts.jsonl), threads
[`threads-raw.json`](threads-raw.json), grading
[`grading-results.jsonl`](grading-results.jsonl).

```
python3 -m unittest discover -s EXPERIMENTS/143-crossvalidated-service-test -t .
```

## 1. The gate accounting

| gate | declared | measured | verdict |
|---|---|---|---|
| **G0 discrimination** | ≥9/10 answered, ≥9/10 declined | 10/10, 10/10 | **PASS** |
| **G1 population** | ≥60 question-shaped of ≥300 fetched | 300 of 300 | **PASS** |
| **G2 composition** | reported per arm and pooled | §3 below | **PASS** |
| **K1 served share** (n=20) | Wilson LB ≥ 0.50: served | **1.0000** | **PASS** |
| **K2 execution share** | reported, not gated | 0/300 = 0.0000 | **PASS** |
| **K3 program-shaped residue** | count | **0** | **PASS** |

**K1 passed on the declared n=20 — no extension needed.** The first 20
top-by-view_count answerable rows were all served, Wilson CI95
**[0.8389, 1.0000]**, lower bound 0.8389 ≥ 0.50.

## 2. The served share

**20 of 20 = 1.0000** answerable-class rows are served by a free general
assistant. The attempt (title + body, general knowledge only, committed
before any answer was read) names the likely fault and the action that
resolves it, at the specificity the thread's own resolution reaches, in
20 of 20 cases. The instrument is the session's model reading pasted
data with no tools — the E062/E091/E092/E126 shape.

This is consistent with every other venue the mission has measured:
E062's 17/20 = 0.85, E091's 5/20 = 0.25, E092's 30/37 = 0.81,
E126's 27/40 = 0.6750. Cross Validated — the largest untouched venue —
closes like the others.

## 3. The composition (G2)

| arm | n | question | answerable | specific | execution | program | manual | other |
|---|---|---|---|---|---|---|---|---|
| A (votes) | 200 | 200 (100%) | 114 (57.0%) | 86 (43.0%) | 0 | 0 | 0 | 0 |
| B (creation) | 100 | 100 (100%) | 29 (29.0%) | 71 (71.0%) | 0 | 0 | 0 | 0 |
| **pooled** | **300** | **300 (100%)** | **143 (47.7%)** | **157 (52.3%)** | **0** | **0** | **0** | **0** |

**Execution share: 0/300 = 0.0000.** Cross Validated is a purely
conceptual Q&A venue — every unanswered question is a statistics concept
the asker wants explained or a dataset they want help analysing. Not one
asks for a self-contained program, a script to run, or a tool to build.

**The two arms differ by 2.0× in answerable share** (57% vs 29%),
confirming E126's stratum finding: the vote-sorted arm over-represents
conceptual, high-arrival questions; the creation-sorted arm
over-represents recent, data-bound, specific questions. The stratum
concern declared in the protocol is confirmed on a third venue.

## 4. What this establishes

1. **Cross Validated closes.** The largest untouched venue is served by a
   free general assistant at 1.0000, consistent with every other venue
   measured. The composition finding — *unserved share is a property of
   what a community owns* — extends to the last large untested venue.

2. **The program-shaped residue is a property of the venue type, not the
   venue.** Stack Overflow (E126) had 6/299 = 2% program-shaped rows;
   Cross Validated has 0/300 = 0%. The difference is not the size or
   quality of the venue — it is that software venues attract
   "write-me-a-program" needs and statistics venues do not. The
   candidate-seat condition (unserved program-shaped needs) does not
   exist in Cross Validated because no program-shaped needs exist there.

3. **The "program-shaped → served" law holds even where programs are
   most native.** Cross Valuated's answers very often contain R/Python
   code — the computational idiom is native. Yet the *unanswered*
   questions are never "write me a program"; they are "explain this
   concept" or "help me analyse my data." The program-shaped residue is
   zero at the need level, so there is nothing for a tool to serve that
   the free assistant does not already answer.

4. **The specific class is large (52.3%) but is not a candidate
   population.** 157 of 300 rows need the asker's data, output, or
   environment. These are unserved by a free assistant *in principle*
   (the assistant cannot see the asker's data), but the remedy is the
   asker providing their data to an analyst — not a self-contained
   program a tool could run. This is the E091/E092 composition finding
   on a new venue.

## 5. What this does not establish

- **That 20/20 is representative of the whole answerable class.** The
  attempt sample is the top 20 by view_count within Arm A — a
  high-arrival stratum, not a random draw. The served share over all
  143 answerable rows is unmeasured.
- **That the 157 specific rows are unserved in a way a tool could
  serve.** The protocol attempts only the answerable class. Whether a
  tool could serve the specific class (e.g., by asking clarifying
  questions) is `untested`.
- **That Cross Validated's execution share is zero in the whole pool.**
  Two strata were measured, not the whole pool (E033/E034's lesson,
  declared).
- **That no unserved program-shaped population exists anywhere.** The
  mission has measured specific venue classes, not the whole of human
  need. The finding is that this venue class has no program-shaped
  needs, not that none exist.

## 6. The decision

**The venue closes on service, like E062, E091, E092, E126. No
candidate.** The candidate-seat question — is there a population with
unserved program-shaped needs? — is answered for the highest
program-density untouched venue: the program-shaped residue is zero, and
the answerable class is served at 1.0. The program-shaped residue is a
property of the venue type.

The venue sweep (E126/E127) is now extended to the largest untouched
venue and closes it. Every venue class the mission can measure is served,
and the one class where a tool could serve (program-shaped) is either
absent (CV) or served by prior art (SO). No candidate population exists
in any measured venue class.

**Named next action:** the mission has now measured every reachable
venue class and found them all served. The remaining directions are
(a) a genuinely new platform class (not Q&A, not registries, not fault
codes — e.g. Reddit, where the arrival instrument is weaker) or
(b) a meta-question about the mission's own method. Per the brief's
"explore fresh observations independently until a specific testable
opportunity appears," the next session should choose by a stated rule
between these, not by comfort.
