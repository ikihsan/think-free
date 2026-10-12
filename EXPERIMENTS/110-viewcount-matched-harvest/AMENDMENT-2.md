# E110 AMENDMENT-2 — G0 fired; the labeler matched substrings, and the repair is anchored

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

## What happened

The first run of `analyze.py` stopped at G0, exactly as `PROTOCOL.md` declares:
**planted-need recovery 5 of 10, below the threshold of 9.** No arm comparison
was made and none may be read from that run.

## Cause, measured not guessed

Every failure was the same shape: the row matched a **need** indicator *and* a
**generic** term, and E107's rule sends "both" to `unlabelled`. Two of the
collisions are substring artifacts, not vocabulary disagreements:

| planted text | matched need term | matched generic term |
|---|---|---|
| "…client **library** for event streaming" | `message broker` | `library` |
| "…**serialization** … **helper**s" | `serialization` | `helper` |
| "…**machine learning** model training" | `machine learning` | `learning` |

The third is an outright bug, not a judgement call. Enumerating the two
vocabularies against each other finds three generic terms that are substrings of
need terms:

- `base` ⊂ `database`
- `learning` ⊂ `machine learning`
- `template` ⊂ `template engine`

and the same failure mode runs the other way on ordinary prose:

- `ai` ⊂ **em**`ai`l
- `ml` ⊂ **ht**`ml`
- `cli` ⊂ **c**`li`ient
- `orm` ⊂ plat`orm`

So the labeler was firing on fragments of words it was never given.

## The repair, and why it is not tuning

Terms are matched on **token boundaries** (regex `\b`), multi-word terms
matched as whole phrases. That is a bug fix: it makes the labeler do what
`PROTOCOL.md` says it does ("an explicit technology noun") instead of what
substring containment incidentally does. It is **not** fitted to the G0 probes,
which is the failure mode a passing-gate-by-construction repair would have.

## The cost of the bug, in the run that exposed it

On the 700-row pool, unanchored matching assigns:

| label | rows |
|---|---|
| need | 175 |
| generic | 104 |
| **unlabelled** | **421** |

421 of 700 — 60% — and only 87 of those are genuine "both vocabularies" rows.
The remaining 314 have a description matching **neither** vocabulary at all:
E107's 78-need / 39-generic term list covers barely half of what Python
repositories actually say about themselves. The instrument was discarding the
majority of every population it was pointed at, which is a population it
claimed to classify at 100%.

## Consequence for comparing with E107

E107 labeled with the *unanchored* rule, so its `77 of 80` and `73 of 80`
yields were produced by a labeler with this defect. E110 now reports both: the
anchored rule as the primary result, and E107's unanchored rule re-run on the
same pool as a **sensitivity arm**, so the harvest-design comparison is not
confounded with a labeler change. If the verdict differs between the two rules,
that difference is itself a finding about how much the published deltas rest on
labeling detail.