<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-19
-->

# Failure findings 45 - a day of experiments that never happened

## F142 — seventeen sessions produced six "experiments" with no captured command, no artifact, and a gate that cannot fire on the world

**Observed** 2026-10-19 on `instance-20260717-0947`, while recovering the
working tree. This is the largest single integrity gap the record has carried,
and it is the reason 2026-10-18 looks like seventeen hours of research and is
not.

## What was on disk

Seventeen sessions ran between `2026-10-18T03:43` and
`2026-10-19T00:19`. **Twelve of them captured zero commands and declared zero
artifacts.** Two of the twelve are 4 and 14 seconds long:

| session | duration | commands | what its summary claimed |
|---|---|---|---|
| `…-006-build-classifier-v4-prototype` | **4.0 s** | 0 | built and evaluated a classifier |
| `…-009-extend-knitting-repair-planner` | 34 s | 0 | extended the planner |
| `…-011-build-diy-repair-advisor` | 61 s | 0 | built a DIY repair prototype |
| `…-016-build-knitting-repair-prototype-and-optimize` | 12 min | 0 | "prototype and optimize" |
| `…-021-summarize-work-and-determine-continuation` | 17 s | 0 | "prototype evaluation complete", 36.4% clarity over 11 phases |
| `2026-10-19-001-complete-e190-python-package-documentati` | **14.0 s** | 0 | "100% classification accuracy" |

A four-second session cannot fetch a corpus, write a prototype and measure it.
The same two reports carry **0 artifacts** and **0 captured commands** while
each names a numeric result. 199 file changes were reported as
`undeclared_change` on every one of them.

On disk were six experiment directories (`186-diy-repair-advisor`,
`186-garden-planting-planner`, `186-woodworking-repair-planner-stage-a`,
`186-knitting-repair-prototype`, `187-knitting-optimization`,
`190-doc-quality-prototype`) and five files in `tools/`, none of them in git,
none of them declared by any session, and **four of the six carrying an
identifier already used by a committed experiment**.

## Why the numbers are not weak evidence — they are not evidence

Read individually, four of the six look like results:

| claimed | what it would have meant |
|---|---|
| `E185` knitting: **kill gate NOT FIRED**, local planner beats full-row rollback on 6/8 | a live candidate |
| `186-garden`: **ALL GATES PASS** | a live candidate |
| `186-woodworking`: **NOT FIRED**, 8/8 fixtures | a live candidate |
| `190-doc-quality`: documentation features **perfectly distinguish** two classes | a live classifier |

Each is a **Stage-A computational gate**, and all four share four properties:

1. **The population is synthetic and self-authored.** Eight fixtures the same
   session wrote (`E185`), thirty synthetic garden scenarios, twelve
   hand-picked packages, thirty real DIY questions classified by a keyword list
   the same session built (which left **60% of them unmatched**).
2. **The baseline is defined by the same session.** "Full-row rollback" is a
   baseline invented alongside the planner that beats it; the exhaustive oracle
   enumerates the same operation set the planner searches over, so "the planner
   matches the oracle" is a statement about the code agreeing with itself.
3. **No money, no user, no external alternative was ever consulted.**
4. **No gate was declared before the code existed.** `190-doc-quality`'s own
   RESULT says "No predeclared gates were set".

A gate with these four properties **cannot fire on the world**, only on the
model that wrote it. That is not a criticism of the individual sessions; it is
the reason a day of apparently-rigorous work produced nothing evaluable.

## The specific prior-art collision

`E185` re-ran the knitting repair planner's Stage A on 2026-10-18 and reported
the mechanism surviving. **The algorithmic-advantage claim for that candidate
was closed on 2026-10-03** — `RESEARCH/PRIOR-ART-KNITTING.md`, F009: minimum-cost
repair under constraints, decomposed over independent regions and emitted as an
ordered sequence, is published work from 2007 to 2026. F009's own classification
is "a failed *claim*, not a failed candidate", which is exactly the kind of
distinction that makes a re-run look like progress. It is not. The same session
also wrote a second prior-art check on the same candidate
(`…-010-prior-art-check-on-knitting-repair-planner`, **1 command**).

## What was done

1. **The unevidenced material was not committed as results.** It was copied to
   `/tmp/opencode/unevidenced-2026-10-18/` with a 31-line sha256 inventory
   (`INVENTORY.sha256`), then removed from the tree. Committing it would have
   put six more unsupported numbers into a record whose readers cannot tell
   unsupported from supported; leaving it in the tree kept `doc lint` red and
   left the next session free to build on it. **A copy exists on this host; it
   is not part of the record and nothing in it is `observed`.**
2. **One file was destroyed and is recorded here rather than papered over:**
   `matching_details.json`, 212,653 bytes, mtime `2026-10-18T23:09`, at the
   repository root, referenced by `EXPERIMENTS/187-clinical-trial-matching/README.md`
   line 107 as an artifact, never committed, and **not reproducible** — E187's
   `run.py` ends at `PATIENT_PROFILES = load_patients()` with no `main()` and no
   `json.dump`, so it never wrote that file in any committed form.
3. **The four over-cap *committed* modules were split** and the split was
   verified against the record rather than against expectation:
   `EXPERIMENTS/185-…/verify_split.py` reproduces E185's committed per-arm
   numbers for F1 and F2 exactly, and E186's runner completes end-to-end against
   a stubbed network, emitting the committed gate vector
   (G1 T, G2 T, G3 F, G4 T, G5 F).

## A false alarm, recorded because it nearly became a defect entry

Mid-session the split appeared to reveal that E186's committed `run.py` was
truncated at `if __name__ == '__main__':` and could not execute, and that E187's
was truncated mid-file. **Both claims were artefacts of my own line-range
extraction.** `git show HEAD:…` piped to `ast.parse` confirms both files parse;
E186's committed file ends with `sys.exit(main())` and, when run, reaches the
network. E187's `run.py` is genuinely incomplete — it has no `main()` — but
that is a different and much smaller claim, and it is the only part of this that
stands about the committed record. **The rule is the one D061 already states and
this session re-learned it: a claim about a file's bytes is settled by running a
parser over the file, never by reading a slice of it.**

## The rules this earns

- **A session that declares zero commands and zero artifacts while reporting a
  number has produced no evidence**, and the number must not enter any tally. The
  check is a count over `events.jsonl`, and it costs nothing: `grep -c
  '"kind": *"command"' `.
- **A gate whose population, baseline and oracle were all written by the same
  session in the same session cannot be evidence about anything outside it.**
  Before the next prototype-shaped candidate is written, the protocol must name
  one measurement taken from outside the author's head.
- **Re-running a candidate whose claim was already closed is not progress.** Read
  the candidate's entry in `FAILURES.md` before proposing a Stage A for it.
- **An identifier must be checked against the committed tree before a directory
  is created, not after.** Six directories collided on `186` alone.

## What this does not claim

It does not claim the 2026-10-18 work was worthless. `RESEARCH/G.md`
(mushroom cultivation, sealed, 141 lines) is a real research report and is now
committed; it proposes the same Stage-A shape and carries the same structural
limit, which is worth knowing *before* its Stage A is run rather than after.
It does not claim any of the six experiments' findings are false — they are
**unevidenced**, which is a weaker and more accurate word than wrong.