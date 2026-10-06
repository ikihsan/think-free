<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Decisions — screening candidates and judging experiments, part 8

Decisions **D068–D069**. Each entry records a choice that was genuinely open, the evidence behind it, the alternatives rejected, and the reason.

**Invariant:** the same as [`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md) — every entry governs *what passes*: which candidates and experiments are screened in or out, what a kill-gate condition may mean, and which metric a verdict is taken on. How this repository's own gates are written and run belongs in [`DECISIONS-GATING.md`](DECISIONS-GATING.md); recording and publishing in [`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md). The index is [`DECISIONS.md`](DECISIONS.md).

Split out of `DECISIONS-SCREENING-7.md` on 2026-10-06 (T-0081) when the combined D068 entries found that file at 293 of 300 permitted lines. Two VMs independently created D068 entries on different split bases; both are preserved here. All screening files carry the same invariant.

---

## D068 — A mechanism candidate is screened on what the caller must already know to name the target

**Source:** E037, F060, session 2026-10-06-006, VM `instance-20260717-0944`. `inferred` from E037 and F060. Narrows D067, which was correct about F059 and would have killed the `stg` candidate had it been read as a rule about capabilities rather than about interfaces.

**D067 said:** a candidate whose value is a mechanism is tested against that mechanism's existing source first, in about two requests, before any population is measured for it. That was correct about F059 — the score-tail worklist really was one URL — and it was **incomplete in a way that would have killed this candidate**, had F060 not been caught.

**What E037 adds.** "Can the mechanism be driven?" and "can the mechanism be *addressed*?" are different questions, and the second is where the gap was.

- The mechanism — selecting part of a file for staging — **is** fully available today. It is drivable from a program through a pty. `git add -p` reads piped keys; it just truncates at EOF and exits 0 (F060).
- The **interface** is not available. `file:line` does not exist in git, and the numbers in git's own output are not the numbers the reader has: an adjacent pair of modifications is one hunk named after its first line, and a deletion is named one line before where its content used to be.

**The rule.** A mechanism candidate is screened on **what the caller would have to know to name the thing they want**, not on whether the mechanism can be performed at all. Three questions, in order, all cheap:

1. **Is the operation already possible?** Not "is the interface already documented" — is the capability present in the incumbent in any form. If yes, the candidate is a differentiator question, not an existence question.
2. **What must the caller know to name the target?** If the answer is a coordinate the caller does not have (a hunk index, a byte offset, a position in a rendered list), the interface is the gap. If they already hold it (a line number, a file name, a timestamp), there is likely an incumbent.
3. **What does the incumbent do when the caller's request is wrong?** An operation that silently does nothing, or the wrong thing, and exits 0, has a gap on the error path whether or not it has one on the happy path.

**Consequences in force.**

1. **F060's first reading is withdrawn.** The mechanism is drivable; the candidate survives because the interface is not, and the record says which one it is.
2. **`stg` is a candidate, not a product.** E037 measured mechanism and interface. It measured **nothing about adoption**, and KILL-Q remains `not_evaluated` for the third experiment running.
3. Question 3 is cheap and general. It applies to every interactive tool the mission has flagged as a gap, and it is answerable by reading the tool's exit status on a wrong input.

**Ceiling.** Questions 1–3 are about the interface a *caller* holds. They say nothing about whether the capability is wanted, and question 2 cannot be answered from the incumbent's documentation — it was answered here by running git and reading what it printed, which took four commands. `diff.context`, `diff.algorithm`, `interactive.diffFilter`, renames and mode changes were not varied, so "git's output never contains the reader's line number" is established for adjacent modifications and deletions only, on one git version.

---

## D069 — A serving signal must come from a channel that answers the question asked

**Source:** E039 (EXPERIMENTS/039-need-statement-response), T-0081, VM `instance-20260717-0947`. `observed` 2026-10-06.

### The choice

E039 found that the reply subtree of a public need statement answers "has anyone else hit this?" and almost never "here is what to use": 57% of the 1391 needs draw a reply, **5.5% draw a link**, and **0 draw a link to a host new to their thread**. Meanwhile the same-thread control sits at 46% and 2.4%, so the reply rate ratio is 1.235 against a bar of 1.5 declared in advance (F060).

The open choice was what to do with a channel that demonstrably answers *something* about a need and demonstrably not the thing this mission has been measuring.

**Taken: the channel is read as answering a different question, and the corpus's value is restated accordingly.** The 1401 statements are a population whose requests were *publicly answered by other people*, and that answer is a social signal — recognition that a need is shared — not an artifact-level one. It therefore establishes that a need is *widely recognised*, and establishes nothing whatever about whether a tool serves it. Prior-art adjudication stays where D050 put it: the open web and the clause's own attribute.

### Why the alternatives were rejected

- **Treat 5.5% as a serving rate and adjudicate on it.** Rejected: 0 of 1391 needs drew a link to a host new to its own thread, so the links that exist are the thread's subject echoed back. A rate of *links* is not a rate of *answers*, and the distinction is the whole finding.
- **Treat the 1.235 ratio as a positive signal and re-open the instrument.** Rejected: the ratio was above 1.0 on all three estimators, which is a real effect, but the bar was fixed at 1.5 in advance and re-opening a gate after reading it is the rationalisation `DECISIONS-PRACTICE.md` exists to prevent. The ratio is reported; the verdict follows the gate.
- **Keep the 597 unanswered needs as the invention seat's population.** Rejected: the hand-read found hardware requests, an article request, a platform request and several requests for a toggle in someone else's product, and the declared lexical rule put only 5.6% in the "prevalence wish" class — so the reading that these are mostly praise is **not** supported as a count even though 21 rows looked like it.
- **Re-open the prior-art question on the strength of "no one answered".** Rejected on D050's own terms: an absence of a hit on any corpus is the absence of a hit. Silence in one thread is a weaker absence than that.

### Consequence

**Item 0's proposed axis loses its measurement.** It asked whether "a specific person already told us exactly what they want, and did they use the thing" can be measured. The second half cannot: **1 of 794** requesters whose need drew a reply replied again, and **0 of the 77** whose need drew a link. There is no channel in this corpus that records whether a need was satisfied, so any axis of that shape needs a channel this repository does not have — which is an owner's call about building one, not a screening question this file can settle.

**What D069 does not decide.** It does not say a need corpus is worthless; it says the corpus's public answer is a recognition signal and the mission has been reading it as an artifact signal. It does not resurrect any of E016's three leads (closed as sources by F039, lead 7 as a feature gap by F038), and it does not name a candidate.

**Cost, stated.** The one axis that had survived four separate measurements of the prior-art screen's unsoundness is now measured too and closed on the demand side. That is four measurements agreeing, which is a reason to stop measuring the screen and start deciding on a different basis — the owner's item, recorded as such.