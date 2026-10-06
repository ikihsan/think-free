<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Findings 61 and 62 — split from `FAILURES.md` at the 300-line cap

## F060 — `git add -p` is not unreachable from a program; it is unreachable *by line number*, and a wrong answer exits 0

**`observed` 2026-10-06**, E037, session 2026-10-06-006, VM `instance-20260717-0944`,
git 2.25.1. Raw: `EXPERIMENTS/037-line-staging/raw/compare.jsonl`.

This corrects a reading this record carried for one hour and then acted on, and it is the
same shape as **F020**: a per-route fact generalised to the tool.

**What was wrong.** The D067 reachability probe found that keys piped into `git add -p`
staged 0 of 4 changes and **exited 0**, and recorded the mechanism as not drivable without a
terminal. Both halves of that were wrong.

- **The keys were read.** `git add -p` reads stdin when it is not a TTY. The run consumed
  `s`, `n`, `n`, hit EOF with hunks still pending, discarded the rest, and exited **0**.
  Not ignored — truncated, silently.
- **It is drivable through a real terminal.** `driver.py`, written for this experiment to be
  the strongest possible form of the baseline, drives `git add -p` over a pty to the right
  answer on **4 of 6** cases. It costs **133 lines** of caller code.

**What survives, and is the actual gap.** The capability is drivable; the *interface* is
not addressable in the coordinate the caller has.

- **`s` splits only at context boundaries.** Two adjacent modified lines are one change pair
  and `s` leaves it whole. The hunk header says line 1; the reader is looking at line 2.
  Line 2 of an adjacent pair is reachable only through the `e` editor, which opens a patch
  in `$EDITOR`. The driver's own log records the run count falling 2 → 1 with the hunk still
  spanning both lines.
- **The numbers git prints are not the numbers the reader has.** Deletions are quoted by the
  line whose content moved up, which is one past git's `+start` for a zero-count hunk.
- **A wrong answer exits 0.** In 2 of the naive route's 3 failures `git add -p` staged
  nothing where one change was wanted, or staged **two** where one was wanted, and returned
  success. `naive`'s deletion case put `[3, 5]` in the index when `[3]` was asked for.

**Why this is the finding and not the kill.** The declared kills were: a program drives
`git add -p` with no more code than the call (**not met** — 133 lines), git takes
`file:line` (**not met** — `git add f:2` is a pathspec error), the prototype loses a case
the incumbent wins (**not met** — 6 of 6 against 4 of 6). KILL-A is not met *on the
measurement*, and the measurement's own baseline is the reason: the honest comparison had
to be a 133-line program, and a candidate that requires the competitor to be 133 lines
longer is a different claim from "the competitor cannot do it".

**Not established.** That the incumbent route is impossible. That a better driver cannot
reach 6 of 6. That anyone wants this. Web search was unavailable on this host, so "no prior
art" rests on git's documentation and behaviour rather than on a search.

---

## F061 — the corpus's own generator was answered inside the corpus

**`observed` 2026-10-06**, session 2026-10-06-006, no new requests. Reading all **589**
never-answered need statements from `EXPERIMENTS/022-need-outcomes/raw/outcomes.jsonl`
joined to `EXPERIMENTS/026-unserved-need-structure/raw/texts.jsonl`, **557 distinct
authors**, median one statement each.

One comment, `46891298`, unprompted, states the generator's own obsolescence:

> I'm really enjoying these LLMs for making ad-hoc tooling / apps for myself. Things that I
> only need for a day or a week, that don't need to work perfectly (I can work around bugs).
> It's really liberating. Instead of saying "gosh I wish there was an app that…" I just make
> the app and use it and move on.

This is **F049** (69% of need-staters had already shipped something before they complained)
stated from the other side: the wish is no longer the bottleneck, the tooling is. It is the
sixth generator question to close, and the first one closed by a member of the population
rather than by a screen.

A lexical count over the 589 shows what the population actually asks for. Recorded because it
is the first theme count on this corpus that was not built to support a prior conclusion:

| theme | rows |
|---|---|
| finding the right existing thing | 70 |
| AI/LLM context, cost or tool-call visibility | 58 |
| non-interactive / scriptable / batch operation | 50 |
| local-first, self-hosted or offline | 43 |
| cannot turn off, limit or control a feature | 17 |
| git version control specifically | 11 |
| selective or partial operation on a collection | 10 |

The lexical counts are an upper bound and overlap heavily — 330 of the 589 match the trigger
`i wish there was`, which is a **wish**, not a specification, and most of those are not
buildable as stated. They are recorded as a description of the corpus, **not** as a demand
estimate.
