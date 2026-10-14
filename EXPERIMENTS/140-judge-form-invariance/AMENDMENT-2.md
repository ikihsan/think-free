<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E140 — AMENDMENT 2

Written 2026-10-14, still **before any instrument has been run on any arm** and
before any judge has seen an item. No M1 verdict, no M2 verdict and no grade
exists. What exists is `arms.jsonl`, the blinded batches, and a reading of the
corpus's shape. Four things are repaired here; two of them are defects the
protocol itself introduced.

## 1. §5 of AMENDMENT-1, which `build_arms.py` cites and which was missing

`surface_paraphrase`'s docstring refers to "AMENDMENT-1.md sections 1 and 5".
Section 5 did not exist. The rule it should have recorded:

`_protect` lifts **every** extracted value span out of the text before any
transform runs and restores it afterwards, keyed by offset so a value that
occurs twice is protected twice. An earlier version protected `code` spans
only, and on a docket/FR pair the `;\s*` → `. ` rewrite re-split the run so
`ground.extract` returned two values where the verbatim arm had one. **The
protection must cover every span the extractor can return**, because the
transforms are punctuation rewrites and punctuation is what the extractor
groups on.

## 2. K4's report on the `C` arm was not a defect count

`build_arms.py` checked "same numeric multiset as V" on `P` **and** `C`. That
is the right test for `P` and `P2` and the wrong test for `C`: a corruption
that leaves the multiset unchanged has corrupted nothing. Run that way, every
genuine corruption is reported as a dropped item — 12 of 15 on a corpus where
12 items *should* be corrupted.

**Repair:** `P` and `P2` are checked on multiset equality with `V`; `C` is
checked on **exactly one reference value replaced** (one value in `C` not in
`V`, one in `V` not in `C`). The K4 rule itself is unchanged for the arms it
was written for; what changed is that `C` is now measured by the property the
`C` arm is supposed to have.

## 3. Blinding was broken by the orchestrator, and the repair moves the judge

PROTOCOL.md §deviations 3 promised the judge never learns which arm an item
came from. It was broken in the run that read the corpus: the session printed
the batch key (arm label beside every item in all six batches) and printed
`V`, `P` and `C` side by side for one judge item. The key is in
`judge_batches.json`, so this was avoidable by not looking.

**Repair: the judge is no longer the orchestrating session.** Each batch is
graded in its own agent session that receives the rubric and that batch's item
text inline, and is instructed to open no file. It therefore cannot read
`arms.jsonl`, the key, the protocol, or the orchestrator's transcript. The
orchestrator's knowledge of the key cannot enter a grade it does not write.

**What this changes in the declared deviations.** Deviation 1 ("the judge is
the session's agent") becomes: the judge is a *separate agent session of the
same model family*, which cannot introspect its own weights either. This is a
different arrangement from the protocol's, chosen after the leak, and it is
strictly more blinded than what was declared — not less. The cost is
uncontrolled model variation between batches, which §deviations 2 already
declared uncontrolled.

**Shuffle seed.** With the judge moved out of process, the presentation order
is reshuffled with `SEED + 1`, fixed in this amendment, and the key is **not
read by the orchestrator before every grade is written to disk**. The old
seed's key is retained in git at the pre-measurement commit so the change is
auditable.

## 4. G0's denominator was the wrong population, in a way that guaranteed a red gate

Three of the fifteen answers are correct *and* carry no extractable value —
they answer "this document states no dollar amounts" — so the corrupter has
nothing to replace and `C` is byte-identical to `V` on those three items
(`corruption_mode: null`). Two of the three are judge items.

PROTOCOL.md §GATES read "(10 of 15 judge items)". That count was already
stale after AMENDMENT-1 §3 reduced the subset to ten answers. Independently of
that, **8 of the 10 `C` judge items are corrupted and 2 are not**, and the 2
un-corrupted ones are the same text twice: once under `V` and once under `C`.
A judge asked to grade `I` a submission that is exactly the expert answer
cannot do so without being wrong, and the item pair also leaks that two items
are identical.

**Repair, both parts, declared here:**

- The 2 un-corrupted `C` rows are **excluded from the judge arm** and are
  reported as a count, because they are duplicates of `V` rows rather than a
  third state. The judge sees 28 items: 10 `V`, 10 `P`, 8 `C`.
- **G0's denominator is the 8 corrupted `C` items**, and the declared rate is
  unchanged: ≥ 0.667, i.e. ≥ 6 of 8. The protocol's rate is kept and its item
  count is corrected, rather than the reverse.

K1 keeps all 15 items for the deterministic instruments, because M2 does not
see a duplicate and 12 of 15 items carry a real corruption.

## 5. P2's selection rule selected the answers with nothing in them

PROTOCOL.md §Arms chose P2's five items as "the 5 judge items with the
shortest verbatim answer". The three shortest answers are the three
no-dollar-amount answers, which contain **zero** values. That rule therefore
lands P2 where there is nothing to reword, and the protocol's own estimate of
"n ≈ 120 values" is wrong by construction.

**Repair:** P2 is the **5 judge items carrying the most values**, with no
length cap — a cap would re-introduce the defect being repaired. The rule is
applied by `build_arms.py` and the resulting value count is reported. This is
selected on a property of the corpus that is checkable before any measurement,
not on any result.

**What stays true.** P2 is still five items, still one writer, still reported
with an interval and **no gate**, and K4 still applies to it: an item whose
canonical value multiset differs from `V` is dropped and counted.

**The contamination this leaves.** The writer is a separate agent session
that sees only the five questions and answers and no arm label; the judge is a
different session per batch and sees the P2 text blind. Writer and judge are
therefore different sessions, which is the strongest separation available
here, and both are the same model family, which is a ceiling.
