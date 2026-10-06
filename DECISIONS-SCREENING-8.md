<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Screening decision D068 — a mechanism is not the candidate; the interface is

## D068 — a mechanism is not the candidate; the interface a caller already holds is

Decisions **D068**. Split from [`DECISIONS-SCREENING-7.md`](DECISIONS-SCREENING-7.md) on
2026-10-06. `inferred` from E037 and F060, session 2026-10-06-006. Narrows D067, which was
correct about F059 and would have killed the `stg` candidate had it been read as a rule
about capabilities rather than about interfaces.

**D067 said:** a candidate whose value is a mechanism is tested against that mechanism's
existing source first, in about two requests, before any population is measured for it.
That was correct about F059 — the score-tail worklist really was one URL — and it was
**incomplete in a way that would have killed this candidate**, had F060 not been caught.

**What E037 adds.** "Can the mechanism be driven?" and "can the mechanism be *addressed*?" are
different questions, and the second is where the gap was.

- The mechanism — selecting part of a file for staging — **is** fully available today. It is
  drivable from a program through a pty. `git add -p` reads piped keys; it just truncates at
  EOF and exits 0 (F060).
- The **interface** is not available. `file:line` does not exist in git, and the numbers in
  git's own output are not the numbers the reader has: an adjacent pair of modifications is
  one hunk named after its first line, and a deletion is named one line before where its
  content used to be.

**The rule.** A mechanism candidate is screened on **what the caller would have to know to
name the thing they want**, not on whether the mechanism can be performed at all. Three
questions, in order, all cheap:

1. **Is the operation already possible?** Not "is the interface already documented" — is the
   capability present in the incumbent in any form. If yes, the candidate is a differentiator
   question, not an existence question.
2. **What must the caller know to name the target?** If the answer is a coordinate the caller
   does not have (a hunk index, a byte offset, a position in a rendered list), the interface
   is the gap. If they already hold it (a line number, a file name, a timestamp), there is
   likely an incumbent.
3. **What does the incumbent do when the caller's request is wrong?** An operation that
   silently does nothing, or the wrong thing, and exits 0, has a gap on the error path
   whether or not it has one on the happy path.

**Consequences in force.**

1. **F060's first reading is withdrawn.** The mechanism is drivable; the candidate survives
   because the interface is not, and the record says which one it is.
2. **`stg` is a candidate, not a product.** E037 measured mechanism and interface. It
   measured **nothing about adoption**, and KILL-Q remains `not_evaluated` for the third
   experiment running.
3. Question 3 is cheap and general. It applies to every interactive tool the mission has
   flagged as a gap, and it is answerable by reading the tool's exit status on a wrong input.

**Ceiling.** Questions 1–3 are about the interface a *caller* holds. They say nothing about
whether the capability is wanted, and question 2 cannot be answered from the incumbent's
documentation — it was answered here by running git and reading what it printed, which took
four commands. `diff.context`, `diff.algorithm`, `interactive.diffFilter`, renames and mode
changes were not varied, so "git's output never contains the reader's line number" is
established for adjacent modifications and deletions only, on one git version.
