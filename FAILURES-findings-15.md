<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Failures — recorded findings, part 15 (F039)

Continues [`FAILURES-findings-14.md`](FAILURES-findings-14.md), which holds
F037 and F038. **Identifiers are stable across all findings files**: a reference
to `F039` means the same entry wherever it appears.

Source: session `2026-10-05-002`, task T-0063. Runnable evidence:
`EXPERIMENTS/019-corpus-person-diversity/` (`corpus_authors.py`,
`arm_a2_local.py`, `recurrence_probe.py`, `stats.py`, `results.json`, `raw/`).
Every declaration, including both arms added after the first figure was read, is
in that directory's `README.md` and was written down before the figures it
gates. `observed` 2026-10-05; Hacker News's unauthenticated item API and
`hn.algolia.com`; 1401 item fetches and 44 searches; no rate limit refused.

## F039 — The mission's need corpus is 1250 individuals, not a sample of shared needs, and its yield was never interpretable

### What was tested

F029 harvested 1401 "is there a tool that"-shaped Hacker News comments, drew 50
by a stated rule, and recorded **zero survivors** — then read that as a fact
about the generator. Every conclusion the mission draws from that corpus rested
on a quantity nobody had measured: **how many people are in it**. A second
quantity was asserted in passing and never measured either — F029's "term
recurrence over 1273 clauses returns only function words, the top content term
appearing in six".

### What was observed

**Arm A, decisive.** 1401 comments carry **1250 distinct authors** (median 1
comment per author, mean 1.12, maximum 8, across 466 distinct days and 1276
parent stories; 0 deleted or dead). Author was recovered for 1401 of 1401 rows,
so gate A1 held at 100%. The corpus is a **wide audience**, not a few prolific
posters. H1 is supported; H2 — that the corpus is too narrow for a shared need
to appear — is **disproved**.

**Arm A2, no verdict, by the experiment's own declared band.** Under a rule
fixed before the count — a clause's *bottleneck* is the fewest other clauses
sharing any one of its content words — **79.25% of the 1152 eligible clauses
share no content word with any other clause**, and 43 of the 49 sample rows the
0-of-50 screen actually used score 1. That sits inside the declared 50–90% band,
so the experiment reports the distribution and refuses a verdict. The single
highest-frequency content term is `x2f` (119 clauses), a URL-escaping artefact
of the harvester rather than anything about software; the top genuine terms are
`better` 41, `people` 41, `know` 31, `easy` 30 — all generic. F029's sentence is
**confirmed in substance and measured under a declared rule instead of
asserted**.

**The robustness check added after that figure was read came out against it, and
this finding is corrected rather than quietly kept.** 79.25% does *not* mean 79%
of the requests are unique needs — a shared content word is a weak test, since
"file" or "tool" would satisfy it. Two stricter measures disagree with it and
with each other: **57.47%** of clauses share an adjacent content-word bigram,
and **2.90%** share a content word that is rare corpus-wide. Neither shows
sharing. The bigram figure is grammatical coincidence — of 312 shared bigrams the
leading twelve are `china figure`, `single solid`, `solid source`,
`video videos`, `write x2f`, `www x2f`, `actually bad`, `alternative another`,
`behind china`, and `claude code` at three clauses, the only topical collocation
in the corpus with any recurrence at all. The 2.90% are `render`, `websites`,
`directly`, `happening` and `easier`: ordinary English outside the corpus's
top-40, not domain vocabulary. **The claim that survives is the weaker one: no
need-level recurrence is detectable in this corpus.**

**Arm B, the instrument failed its own controls.** Queried for distinct authors
by exact phrase over HN comments: ten mechanically chosen clauses (sample rows
5, 10, … 50), six positive controls, six negative controls. Every clause
returned **0 or 1 distinct author** — the declared floor, since a clause's own
author always appears in its own result. So did **four of the six positive
controls**: `spaced repetition flashcards` returned 34 and `self-hosted email
server` 47, but `atproto personal data server` returned 1, and
`AI coding agent unrequested changes`, `lossy webp conversion` and
`OCI image to rootfs` returned 0. All six negative controls returned 0.

Gate B1's arithmetic passed **degenerately**: the negative median is 0, so its
`3 × median` threshold is 0 and six of six positives clear it. The declared kill
gate is recorded as **not evaluable** rather than met, because the identical
0-or-1 reading that disqualifies the controls disqualifies the clauses.

**Arm B2, inconclusive.** 25 of the 1250 authors (2.0%) wrote a clause naming
both a declared agent-family term and a declared change-family term. Reading the
rows shows most are not F033's cluster at all — buying Windows 11 without
Copilot, hiring staff to use AI, a sensor that detects people at a distance — so
2% is consistent with background co-occurrence of a common term family and
separates nothing.

### What this rules out, and what it does not

**It does not reverse F029.** Those 50 clauses died on their own merits and are
still dead. What changes is what the negative is *allowed to mean*.

**It kills the narrow-audience explanation.** The mission's only demand-side
instrument drew from 1250 different people, so a shared need was available to
appear and mostly did not.

**It supersedes D049's denominator on its own subject.** D049 ruled that
recurrence must be counted per *repository* because "a thousand issues in one
project is one project's problem". F033 then measured that denominator and the
strongest cluster collapsed ~200×. This experiment did not re-open that count,
but it shows the repository was never the unit that could have answered the
question: within the corpus the unit is the person, and the person-level
co-occurrence rate is not measurable from these clauses either.

**It is not a finding about demand.** Distinct-author recurrence is attention in
one audience. Nothing here measures whether these needs are real, and F039 must
not be cited as though it did.

### The instrument defects found, because both would have flattered a conclusion

- **A schema mismatch between two APIs for one site read as perfect recovery.**
  Hacker News's Firebase item API names the author field `by`; the Algolia
  search API names it `author`. The first run of `corpus_authors.py` asked for
  `author`, and recorded **1313 of 1313 rows as `ok` with a null author** — the
  worst possible shape, because a status column said the fetch worked. That
  capture is kept at `raw/corpus_authors.attempt1.jsonl`.
- **A gate can be met degenerately by a zero.** Gate B1's threshold was `3 × the
  median negative control`. The negative median is 0, so the threshold is 0 and
  every control clears it, including the four that returned nothing at all. A
  ratio to a control that can be zero needs a floor, and this one had none.

### The positive consequence, which is not part of the decision

The corpus is **1250 named, publicly identified people who each wrote down, in
public, what was missing**. The mission holds that population and has used it
only as a bag of problem statements. It is the one asset here that is a *demand*
measurement rather than a supply count — and D051 records that choosing what to
do with it is item 0's and belongs to the owner.

### Reproduce

```bash
python3 EXPERIMENTS/019-corpus-person-diversity/corpus_authors.py
python3 EXPERIMENTS/019-corpus-person-diversity/arm_a2_local.py
python3 EXPERIMENTS/019-corpus-person-diversity/recurrence_probe.py
python3 EXPERIMENTS/019-corpus-person-diversity/stats.py
```

Arms A and A2 are local and deterministic. Arms A and B re-fetch from two
unauthenticated public endpoints, so the author and author-count figures are
`observed` on 2026-10-05 and may drift as HN's corpus grows; the capture in
`raw/` is the evidence for the figures quoted here.
---

## F040 — F037's "the artifact is a copied directory" is an instruction, not an observation, and the copies it predicts do not appear where they can be seen

### What was tested

F037 read the four hand-reviewed high-star rows of the prior-art screen's
young-vocabulary arm and concluded that the reader **copies a `.claude/`
directory into their own repository once**, that the hooks then run themselves,
and that "the artifact in use is not a package". That inference is load-bearing
in [`STATE-next-actions.md`](STATE-next-actions.md) item 0, which proposes
testing whether forks and dependents are the serving signal for a young
vocabulary. If the artifact is copied, a versioned channel is not needed and
installs are the wrong measure; if it is not copied, the near-zero install
readings in F037 and F059 need a different explanation.

E020 tested the consequence rather than the sentence: if whole directories are
copied between repositories, **byte-identical content will appear across
repositories**, with no credit given — because a copied config file is anonymous
by construction and no README rule can ever find it.

### What was measured

Population by declared rule: 175 repositories from GitHub repository search over
five claude-config terms, of which **31** carry a `.claude/settings.json`
(`observed`, `EXPERIMENTS/020-copied-config-drift/raw/`). Every one was shallow
cloned and every file under `.claude/` hashed.

| quantity | value |
|---|---|
| file instances under `.claude/` | 2072 |
| distinct file contents | 1950 |
| contents shared by 2+ repositories | **92 (4.7%)** |
| widest shared content | **3** repositories |
| repository pairs overlapping by ≥50% | 2 — **both one author's two repositories** |
| cross-author overlapping pairs | **0** |

And at global scale, through Sourcegraph's unauthenticated streaming index:
**4,540** repositories carry a `.claude/settings.json` path, and **`cp -r
.claude` appears in 687 content matches** against a nonsense-token control that
returns **0**.

### The finding

**Copying is widely documented and barely duplicated.** 687 sites instruct a
reader to copy a `.claude/` directory; 4.7% of distinct configuration file
contents are byte-identical across repositories; and no repository pair from
different authors overlaps by even half. The two facts are compatible and the
compatibility is the point: the copy is *retypewritten or adapted per site*, so
each of those 687 instructions produces a configuration that no longer matches
any upstream the search can name.

This corrects F037's wording rather than its substance. F037 read four documents
and inferred a mechanism from them; the mechanism is real as **documented
practice**, but "the reader copies the directory" overstates it. What the
evidence supports is: the reader is *told* to copy, and adapts what they copy.

### What this does not establish, and why the answer is `inconclusive`

**The drift rate is not measured.** Attribution by README returned **0 of 31** —
23 repositories contain attribution *language* and reading every match by hand
shows nearly all of it is `source code`, `source ~/.bashrc` and "data source";
the two genuine attributions name an *idea* (a Karpathy gist, `livekit/agent-skills`),
not a copied directory. Attribution by identical content returned **0
cross-author pairs**. The declared no-drift gate fires at 0 attributable rows, so
this is **an unanswerable question, not a measurement of low drift** — and the
difference is carried in `results.json` as `drift_rate: null` rather than `0`,
because 017's H2 thresholds were once satisfied by an empty read.

### Two instruments were falsified, and both retractions are held by a test

- **The marker-file probe.** `.claude/agents/README.md` returning 404 does not
  mean `.claude/agents/` is absent. Checked against the contents API on 8
  repositories: **8 of 8 disagreements**, 6 with directories the probe missed.
  Had this gone unnoticed, E020 would have reported that 30 of 31 repositories
  commit nothing but a settings file — an artefact of a probe for a README that
  does not exist. Replaced by `git clone --depth 1`.
- **The version-record regex.** It matched **17 of 31** and every match pins a
  Claude Code CLI version, a hook event, or the repository's own release badge.
  None records the version of a copied configuration, so **17/31 must not be
  cited**, and the test asserts the naive rule is *green* on all 17 — because if
  it were red, nobody would be tempted to reinstate it.

### Why it matters to the mission

Item 0 asks what a fact about supply should tell us about demand, and F037 offered
"the artifact is copied, so install counts read zero" as the reconciliation.
E020 **removes that reconciliation**: the copies are not byte-identical, so the
near-zero install readings are not explained by an invisible distribution channel.
The supply the screen sees really is lightly used.

The remaining live question is sharper and is now owned elsewhere: VM
`instance-20260717-0944` holds an open claim on **T-0064**, "measure whether the
young vocabulary's artifacts are copied into other repositories", using
Sourcegraph. E020 could not do that work — authenticated code search returns 401
here — and its 4.7% is bounded by the population repository search can return.
E020's contribution to T-0064 is the falsified probes and the `cp -r .claude`
count; the drift rate is T-0064's to measure.
