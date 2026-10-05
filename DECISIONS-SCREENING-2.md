# Decisions — screening candidates and judging experiments, part 2

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

Decisions **D048–D051**. Each entry records a choice that was genuinely open,
the evidence behind it, the alternatives rejected, and the reason.

**Invariant:** the same as [`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md) —
every entry governs *what passes*: which candidates and experiments are screened
in or out, what a kill-gate condition may mean, and which metric a verdict is
taken on. How this repository's own gates are written and run belongs in
[`DECISIONS-GATING.md`](DECISIONS-GATING.md); recording and publishing in
[`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md). The index is
[`DECISIONS.md`](DECISIONS.md).

Split out of `DECISIONS-SCREENING.md` on 2026-10-05 (T-0063) when D051 pushed
that file past the 300-line cap. D048–D050 moved verbatim; numbering is
continuous and unchanged, so any existing reference to a decision id still
resolves. **The split continues the same invariant rather than narrowing it**,
which is why this header repeats the screening invariant instead of inventing a
new one — a narrower invariant is what
[`DECISIONS-SESSIONS.md`](DECISIONS-SESSIONS.md) had to revert after T-0030,
when two files' prose contradicted each other.

## D048 — The next-action list carries at least one invention item (2026-10-04)

Observed: F031 measured where effort went over two days — 1.3% of day-two
commits touched `EXPERIMENTS/`, 4.8:1 lines of record-keeping to
world-measurement, and `STATE-next-actions.md` held no action that could
produce or advance a candidate. No candidate moved as a result, and no
artefact had reported the trend; the drift had become executable.

Decision: `STATE-next-actions.md` must always include at least one action
whose success is a candidate produced, tested, revived, or explicitly
rejected, and that item is reviewed whenever the list is rewritten. Record-
keeping repairs remain legitimate, but they may not crowd out the only zone
whose contents measure something outside this repository.

Rejected: (a) fixing this with a hard quota in the linter, which prices
sessions instead of informing the human choice; (b) declaring the ratio
invalid because lines are a weak proxy, which is true of the metric, not of
the trend it caught; (c) letting the item be optional because invention
cannot be scheduled, which is how the list filled with gates.

Consequence: the allocation measurement stays runnable
(`tools/measure_allocation.py`, held by `tests/test_allocation_measurement.py`),
and the next-action list is expected to show an invention item beside any
infrastructure item.

## D049 — A need corpus supplies problem statements; recurrence comes from a repository-denominated issue corpus (2026-10-04)

Observed: F029. A harvest of 1401 unmet-need statements from Hacker News
comments created after 2024-01-01, screened by a stated rule that drew 50 of
them, yielded **zero survivors** — 38% already served by a tool, 30% stating
no mechanism, 24% not software needs, 8% needing hardware. The prior generator's
own record is 3 live candidates from 16 (18.75%), none validated. The corpus has
no internal recurrence signal either: term recurrence over 1273 clauses returns
only function words. But the same cluster, measured in a different unit, gives
5805 open issues across 28 repositories for `"not asked for"` and 14510 across
29 for `"unrelated changes"`, with `claude-code` and `copilot-cli` in the sets.
F030: one search query decides a prior-art verdict wrongly in both directions —
502 hits from `in:readme` that were `awesome-go`, and 0 hits that became 29-83
on a second phrasing.

Decision: the candidate pipeline has two distinct inputs and they may not be
substituted for each other. A **problem statement** comes from a dated,
countable need corpus; a **recurrence signal** comes from issues counted by
repository, because a thousand issues in one project is one project's problem
and a hundred issues in a hundred projects is a cross-project one. A need
statement alone may not be promoted to a candidate on the strength of its own
existence. And a prior-art verdict requires more than one phrasing, on more than
one corpus, with the phrasings written down.

Rejected: (a) keeping the harvest as the candidate generator, refuted by the
0-against-50 measurement; (b) taking GitHub's issue count as a measure of
prevalence, which is full-text self-selection and needs a repository-signal
filter before it means anything; (c) treating F030's four revised verdicts as
candidate gaps, which is the error the decision exists to prevent; (d) declaring
candidate generation solved and moving on, since 0 of 50 says this generator is
spent, not that the pipeline is.

Consequence: `EXPERIMENTS/012-candidate-harvest/` is retained with its raw
capture and four runnable probes. The next candidate action is to build the
repository-signal filter and re-harvest through it, testing first the cluster
with the strongest measured recurrence — changes a coding agent makes that
nobody asked for — against a stated falsification of its own.

## D050 — A prior-art verdict must read the open web and judge the clause's attribute, and an unserved need goes to a mechanism step (2026-10-05)

Observed: F035, from E016's two declared arms. Six of six positive controls
were re-adjudicated *served*, so the procedure works; and of the twelve
adjudicable judgement kills in F029, **three are no prior art found** on two
GitHub phrasings, three registry keywords and two open-web phrasings each —
item 7 (annotate once, choose metric/log/trace per code path at runtime), item
12 (tag HN posts and authors inside an HN client), item 16 (a daily word game
that shows the solution order so a player can give up). One further kill was
never adjudicable: its clause and E012's reason asked different questions.
The count is 3 against a threshold of 3 and one row decides it, because item
16's open-web results include ten answer-aggregator sites that reveal solutions
outside the game.

Also observed: **corpus carriage.** GitHub's repository index carried every
verdict the code corpora carried; the registries carried none on their own; and
the open web carried four served verdicts that two code corpora returned
nothing for, including twelve named hosted services for url-popularity that two
code corpora could not see at all. F036: the first web instrument tried answered
HTTP 200 with 380 well-formed results unrelated to every one of the 38 queries.

Decision: two changes, and they are separable.

1. **A prior-art verdict is only admissible when it reads the open web and
   judges the clause's distinguishing attribute.** Code indices decide whether a
   *category* exists; only the open web shows whether something *serves the
   clause*, because hosted, commercial and vendor features are invisible to
   every code index. Attribute, not category: item 42 was killed correctly
   because `git add -p` serves it, and `dingdugan/model.tracker` and all five of
   item 49's artifacts serve their clauses with 0 to 2 stars between them. A
   category is served, an attribute is not, and only the second answers the
   question a need statement asks. An open-web probe carries a known-answer
   control, a nonsense-token control and per-query titles, or its output is not
   evidence.
2. **An unserved need goes to a mechanism step, and F029's generator verdict is
   narrowed rather than reversed.** Screen 1 and Screen 3 still apply to a need
   with no solution found, so the harvest stays refuted as a *candidate*
   generator; but three needs that no artifact on three corpora serves are the
   first leads this mission has that do not come from its own sealed reports,
   and they are worth a mechanism question each.

Rejected: (a) treating the three as candidates or as gaps, which is the error
F030's rule exists to prevent and which MISSION.md forbids — an absence of a hit
on three corpora is the absence of a hit; (b) reporting the arm as a comfortable
pass because 3 ≥ 3, when the margin is one attribution row and the looser rule
gives 2 and reverses the direction, which is recorded in `results.json` instead;
(c) re-opening all 19 kills for a better search now that the procedure is known
to work, since 9 of 12 are served and the recoveries are strong; (d) promoting
the need-harvest corpus back to a generator on the strength of three survivors
out of fifty, which is 6% and is not a generator; (e) treating the four
open-web-carried verdicts as an argument for *more* corpora before the mission
has read the one it knows it needs.

Consequence: E016 closes with both arms answered and its raw captures kept. The
three items are listed in `STATE-next-actions.md` as the invention item's
contents, each with the clause it came from and the two phrasings per corpus
that found nothing. The next screen of anything in this mission reads
`docs/process/experiment-protocol.md`'s prior-art rule as amended here.

## D051 — A yield measured on a harvested corpus is uninterpretable until that corpus's population is measured (2026-10-05)

Observed: F039, from E019's three arms. **Arm A, decisive.** E012's corpus is
1401 Hacker News comments, and nobody had counted its authors. They are **1250
distinct authors** — median 1 comment per author, maximum 8, across 466 days
and 1276 parent stories, with author recovered for 1401 of 1401 rows. The corpus
is a *wide* audience, not a few prolific posters, so the narrow-audience
explanation for F029's 0 of 50 is disproved.

**Arm A2, no verdict by its own declared gate.** Under a rule fixed before the
count — a clause's *bottleneck* is the fewest other clauses sharing any one of
its content words — **79.25% of the 1152 eligible clauses share no content word
with any other clause**, and 43 of the 49 sample rows the 0-of-50 screen used
score 1. That is inside the declared 50–90% band, so the experiment refuses a
verdict and reports the distribution. The top document-frequency content term is
`x2f`, a URL-escaping artefact of the harvester, and the top genuine terms
(`better` 41, `people` 41, `know` 31, `easy` 30) are all generic. That is F029's
"recurrence returns only function words", now measured under a declared rule
instead of asserted.

**Arm B, the instrument failed its own controls.** Ten mechanically chosen
clauses and six positive plus six negative controls, queried for distinct authors
by exact phrase over HN comments. **Four of the six positive controls returned 0
or 1 distinct author**: `spaced repetition flashcards` returned 34 and
`self-hosted email server` 47, while `lossy webp conversion` and
`OCI image to rootfs` returned 0. Gate B1's arithmetic passed degenerately,
because the negative controls' median is 0 and 3 × 0 is 0. The kill gate is
therefore recorded as **not evaluable**, not met — the same 0-or-1 reading that
disqualifies the controls disqualifies the clauses.

Decision: **a number produced from a harvested corpus is uninterpretable until
that corpus's population has been measured, and it is measured by distinct
people, not by rows.**

1. E012's 0 of 50 is a fact about the corpus's *composition*, not about the
   screens' quality and not about the world's needs. 1250 individuals each asked
   once, and 79% of those requests share no content word with any other; a
   per-row screen cannot aggregate what the corpus does not contain. This
   **does not reverse F029** — those 50 clauses did die on their own merits —
   but it changes what the negative is allowed to mean. D049's rule that
   recurrence comes from a repository-denominated issue corpus is superseded on
   its own subject: the repository is not the right denominator either, and
   F033's ~200× collapse was measured with it.
2. **A need statement harvested from this corpus may not be promoted to a
   candidate.** That closes the two leads E016 left open — items 12 and 16 — as
   *sources*. Their mechanism questions are not worth asking, because the premise
   underneath them, that anyone shares the request, was never measured and cannot
   be measured from this corpus.
3. **Every future harvest states its population before its yield.** The
   measurement cost here was ~90 seconds and 1401 unauthenticated requests. It
   is the cheapest gate in this repository, and E012 drew 50 clauses without it.

Rejected: (a) reversing F029, which the evidence does not support — those 50 rows
are still dead; (b) treating 79.25% as a verdict, which the experiment's own
declared band forbids; (c) reading the clause results as evidence that nobody
else wants these things, which is exactly what four failed positive controls
forbid; (d) re-phrasing the positive controls until they score and then reading
the clauses off the same instrument, which is F030's error committed on purpose;
(e) choosing a candidate-selection axis here, which is item 0's and belongs to
the owner.

Consequence: `EXPERIMENTS/019-corpus-person-diversity/` keeps all three raw
captures, including `raw/corpus_authors.attempt1.jsonl` — the 1313-row capture
that recorded every row `ok` with a null author because the Firebase item API
names the field `by` and Algolia names it `author`, so a schema mismatch between
two APIs for one site read as full recovery. The **positive** consequence is
recorded where the next reader looks and is not part of this decision: the corpus
is 1250 named, publicly identified people who each wrote down what was missing,
which is a population the mission holds and has never used. Item 0 remains the
owner's choice; this removes one axis from the table and names that population.