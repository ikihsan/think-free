# E029 — protocol amendment 3

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Declared 2026-10-05, after reader r2's first labels and reader r1's first labels
both existed, after one gate table had been computed once and discarded, and before
either rate has been read.** No arm comparison has been published. The thresholds in
[`PROTOCOL.md`](PROTOCOL.md) are unchanged, and nothing in this amendment widens
them.

This amendment records two defects. The first voided the experiment's primary
comparison. The second produced 222 plausible-looking labels whose id-to-pair
mapping was wrong, and which no downstream check could have told apart from correct
ones.

## 1. The mismatched arm was the treatment arm, renamed

The control is supposed to be *the same 74 shipped builds, paired with a different
author's need*. The first implementation paired **the partner's own need with the
partner's own items**:

```python
other = partner[e["author"]]
body = render(pop[other]["need"]["text"], later_items(other, ...))   # both from `other`
```

Since the derangement ran over the same 74 eligible authors, the "mismatched" arm
contained **exactly the same 74 (need, items) pairs as the matched arm, in a
different row order**. It was a replicate, not a control. All 74 rows were
self-paired, and 0 were cross-paired.

**How it was found.** The lexical arm — which feeds no gate and exists only as a
sanity reading — printed **byte-identical means** for the two arms:

| arm | mean content-word overlap | rows with zero overlap |
|---|---|---|
| matched | 0.044952 | 32 / 74 |
| mismatched | 0.044952 | 32 / 74 |
| mismatched *(repaired)* | **0.023632** | **40 / 74** |

Two different pairings cannot produce identical word-overlap statistics across 74
rows. The number was the alarm, and it is the argument for computing an arm that
feeds no gate: it had no incentive to look right.

**The repair** keeps the matched author's need and takes the items from the partner:

```python
body = render(e["need"]["text"], later_items(other, pop[other]["need"], builds))
```

Verified: matched 74/74 self-paired, mismatched 74/74 cross-paired, **0** empty
SHIPPED sections (amendment 2's repair still holds). Two tests now hold the pairing
directly — `test_the_mismatched_arm_is_cross_paired_not_a_relabelled_replicate` and
`test_the_lexical_arms_differ` — and `view_key.json` records `partner` per control row
so the property is readable rather than inferred.

## 2. A label file with 222 correct row ids and a wrong row-to-pair mapping

`make_reader_views.py` shuffles rows with a seed, and the row list feeds the shuffle.
Amendment 2 changed the row list, so regenerating the view **reordered** it.

Reader r1 read the first view, noticed the file change mid-task, discarded its own
first pass, and re-labelled from the regenerated view — reporting the file's md5 as
`ba5e5481…`, which is the regenerated view. But it emitted the rows **in the
previous view's order**. The result was a file with the complete, correct set of 222
row ids in a plausible-looking order, in which **the id-to-pair mapping was wrong**.

Nothing downstream could detect it. Every id existed, no id repeated, every label was
in the vocabulary, and the id *set* matched the key exactly.

**What I did to it was worse, and is recorded because it is the more useful half.**
Seeing one positional mismatch against the first view (`X72` where the view said
`M72`), I wrote `repair_reader_ids.py` to re-key the file positionally against the
first view. It reported a 221/222 agreement and "repaired" one id. But the file it
was given was keyed to neither view, and re-keying it to the first view overwrote
r1's real ordering with a false one. **The script was wrong and is deleted.** The
lesson is that a high agreement rate against the *wrong* reference looks exactly like
success, and a repair needs its reference to be established rather than chosen.

**The redesign.** No labels are carried across a view change at all:

- the view is **frozen** at md5 `d604f1f93b36be02ba0e1df1df5f6a6d`, identical for both
  readers, and both readers are given one pass over it with an instruction not to
  re-read it;
- there is no partial re-read and no assembly step. One reader, one pass, one file.
- `test_labels_come_from_the_view_now_on_disk` asserts each label file's **order**
  matches the frozen view's order, which is the property that was violated; asserting
  only the id *set* is what let the bad file through.

All four earlier label files and both earlier views are retained under
`superseded/` rather than deleted, because this repository keeps failed runs and
because the record of how the id mapping was lost is itself evidence.

**Three files this session declared as artifacts are no longer at their declared
paths, and the distinction matters.** `raw/view_r1_xonly.txt` and
`raw/view_r2_xonly.txt` were **moved** into `superseded/` — they are the partial
re-reads this amendment abandons, kept because a later reader should be able to see
what the repair threw away. `assemble_labels.py` was **deleted**: it existed only to
merge a full-view pass with a partial re-read, and with no partial carry-over there
is nothing to merge. That is the third script in this experiment to be deleted after
proving wrong (`repair_reader_ids.py` was the second, and it made things worse), and
the pattern is the finding: **each repair added a layer that the next defect made
unnecessary.** The lesson is not "write fewer scripts" — it is that a repair should
be justified by the property it restores, not by the mismatch it can see.

## What this cost, stated plainly

Three reader passes were spent and neither produced a usable matched/control
comparison. The run was invalidated by its own instrument, not by a result. Two of
the three defects were found by tests written before the data existed, and one — the
replicate — was found by an arm that fed no gate. That is the only part of this
sequence that generalises.

## Unchanged

Every gate and threshold. The reader population is still 74. The lexical arm still
feeds no gate. The story-title arm is still the one that can kill H1, and its
asymmetry — a headline is not a missing-capability statement, so a reader may find it
easier to call unrelated — is still a limit on how to read B2 rather than a reason to
drop the arm.
