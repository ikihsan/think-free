<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Findings 62 to 64 — E038, the prior-art search E037 could not run

## F062 — E037's "not prior art as an interface" rested on git's own documentation, and two tools answer it

**`observed` 2026-10-06.** E037 declared KILL-B not met after checking `git add --help`,
three shell routes and git's behaviour, and its own ceiling said so: *"Web search was
unavailable on this host, so 'no prior art' rests on git's own documentation and behaviour,
not on a search. That is a real gap in KILL-B."* With a search surface available, the gate
was re-run and **two tools take the coordinate E037 claimed was missing**:

- **VS Code's git extension ships `git.stageSelectedRanges`**
  (`extensions/git/src/commands.ts:1777`), staging the intersection of the active editor's
  selection with the working-tree diff. Read at `main`, both files fetched whole.
- **patchutils 0.3.4's `filterdiff --lines=RANGE`**, whose man page reads *"Only include
  hunks that contain lines from the original file that lie within the specified RANGE"*,
  and which works as `git diff -U0 | filterdiff --lines=4 | git apply --cached
  --unidiff-zero`. **Measured, not described: 12 of 30** on E038's cases.

**The claim is narrowed, not withdrawn.** Neither takes the coordinate as an *argument*: VS
Code's comes from an editor selection and is not callable from a script, and `filterdiff`
names the *original* file's line, so a deletion and an insertion at the same point are
indistinguishable to it. Magit, read in full (390 KB), has no line-addressed staging
command at all.

**And the mechanism is not this repository's.** VS Code's `staging.ts:124` carries the
comment *"heuristic: same number of lines on both sides, let's assume line by line"* over
exactly the pairing rule `stagelib._split_run` implements. Two independent
implementations arriving at the same rule is evidence the rule is the natural one, not
that either invented it.

**Lesson, and it is the general one.** E037 declared the gate, found it not met, and
recorded in its own ceiling exactly what it had not checked. That is the record working.
The cost was one session of confident reasoning from an unsearched absence, and the
absence turned out to be populated.

## F063 — an oracle that reads hunk anchors cannot see an over-staging bug, and one test asserted the bug as intended behaviour

**`observed` 2026-10-06.** `stg` was **6 of 6** in E037. It was silently wrong on two of the
six, and E037's instrument was structurally incapable of detecting either.

E037's oracle was `staged_anchors` — the line numbers of the hunks now in the index. A hunk
carrying **two** changes when one was asked for still prints **one clean hunk at the right
anchor**, so over-staging scores as correct. Replaced with the index content
(`git show :f.txt`) — what a commit would actually receive — the bug is immediate:

```
$ git diff -U0              $ stg stage f:4        # asked for X, got X and Y
@@ -3,0 +4,2 @@ c          @@ -3,0 +4,2 @@         stage f:4
+X                          +X                      exit 1  ("success")
+Y                          +Y
```

**The premise in the test was wrong, not just the code.** `test_a_multi_line_insertion_stays_whole`
carried the comment *"there is no valid hunk for half of a two-line insertion."* There is:
git apply takes `@@ -3,0 +4,1 @@` then `@@ -3,0 +5,1 @@` over the same `@@ -3,0 +4,2 @@`,
verified against git 2.25.1 before the code changed. A test written to pin a guess reads as
evidence, and would have kept the bug in place indefinitely.

**Two further defects, both caught by instruments rather than by reading.** The first fix
conflated two offsets — the surplus adds start at content index `nrem + pairs`, not `nrem`,
because the removes come first and then the already-paired adds — and picked the wrong line
out of a three-line run. Caught by the new test. And E037's `driver.py` hardcoded the
filename `f`, so when E038's harness named its file `f.txt` the pty baseline read **0 of
30**: a baseline that cannot see the problem is not a baseline. Fixed to take a path, and
the incumbent immediately read **12 of 30**, consistent with E037's own 4 of 6.

**After the fixes: `stg` 30 of 30, `filterdiff` 12 of 30, `pty_driver` 12 of 30, `naive`
6 of 30**, with 78 wrong-but-exit-0 rows across the three alternatives and none for `stg`.
30 tests green, all against real repositories, no mocks.

**Not withdrawn:** the interface gap is real on the command line, and the candidate stands —
narrower than E037 stated. What is withdrawn is E037's 6 of 6, which was the number the
candidate's headline rested on.

## F064 — a keyword classifier's 100-of-195 was 2-of-30, and two readers disagree exactly where the claim lives

**`observed` 2026-10-06.** E038 classified 195 GitHub issues by keyword and reported **100
"in-population"**. A mechanically selected sample of 61 rows — every third distinct issue,
chosen before any content was read — was labelled by hand, twice, independently.

**Precision 0.067 against reader 1 and 0.033 against reader 2**: of the 30 sample rows the
classifier called "in-population", 2 or 1 are the need. Both readers independently put it in
the 3–7% range, and **both found the strongest row in the sample *outside* its
`in-population` label** — `mcp-multi-root-git#3`, *"no way to stage lines 1-50 separately
from lines 51-100 within one tool call"*, whose whole point is the coordinate. A keyword
match over a repository-wide body search cannot distinguish the need from a pull request
about a CI budget, and a rate built on it is not a measurement.

**Agreement between the readers is high where it is easy and low where the claim is.**
56 of 61 three-way (0.918, κ = 0.734); 59 of 61 collapsed to yes-or-no (0.967, κ = 0.889).
But **all five disagreements sit on the same boundary** — the line between "the operation"
and "the coordinate" — and the `yes-line` sets share one row (Jaccard 0.25). So the
population's *existence* is agreed and its *size* is not: **0.016 if only rows both readers
call `yes-line` count, 0.066 if any row either reader calls it does.** The honest figure is
the range.

**Both readers then found a shared defect in the sample instrument.** Bodies are truncated
to 700 chars; the median real body is 2716. Reader 2, working from full bodies, found four
rows whose label turns on text past the cut, **including the sentence that decided one
`yes-line` call**. The `no` labels are unaffected — false rows are rejected on the first
lines of the title — so the truncation inflates the `yes-` categories specifically, which
is where the ceiling needed to be honest.

**Reading.** 0.016–0.066 of matching GitHub issues is 16 to 66 per thousand, on a platform
that is not a demand population for a developer tool. That is consistent with F027 and F037.
**The capability is asked for, by named people, in at least three projects** — one of them
an agent tool that states the need in the agent's own terms. **Prevalence is not
established**, and prevalence is what would decide whether this is a product.
