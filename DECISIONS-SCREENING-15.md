<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-09
-->

# Decisions — screening candidates and judging experiments, part 15

Split out of [`DECISIONS-SCREENING-14.md`](DECISIONS-SCREENING-14.md) on 2026-10-09.
The rule is unchanged: a decision is recorded when the choice was genuinely open,
with evidence, alternatives, and reason.

Decisions **D089–D090**. Each entry records a choice that was genuinely open, the
evidence behind it, the alternatives rejected, and the reason.

## D089 — The arrival instrument is Stack-Exchange-shaped, and a field a platform does not publish is missing rather than zero (2026-10-09)

`observed` 2026-10-09, session 2026-10-09-002, E071, F101.

**The situation.** E069 sat unlanded claiming a `CONFIRMED` result: 100% of
non-software need statements carry `view_count` > 0, "directly contradicting"
E063/E066, where `view_count` is 0% in software corpora — so the instrument's
domain scope is not software-narrow. Four experiments and `MISSION-OUTCOME.json`
rested on it. The comparison's software cells were read as **measured zeros**,
and no one had asked whether they are zeros at all.

E071 asked it with a predeclared kill condition. Eight arrival-field spellings
(`view_count`, `views`, `viewCount`, `viewed`, `viewed_count`, `impressions`,
`hits`, `pageviews`) across 148 returned objects: **Hacker News 0 of 60 items
carry one; the GitHub issues API 0 of 8; Stack Exchange — the surface E062
actually measured — 80 of 80 items carry a positive `view_count`.** All three
gates fired, and the classifier returns `zero` / `positive` / `absent` /
`not_an_object` correctly on five fabricated cases, so `absent` is a distinction
the code draws rather than a default.

**The decision.** **`view_count` is adopted as an arrival measure only where a
platform publishes one, and any population whose surface does not publish an
arrival field reports that cell as a missing observation, never as a zero.** The
E069 headline contrast is withdrawn with it. This is D082 applied to the
instrument's own adoption record rather than to a corpus: a session wrote D082
on 2026-10-08, read its own rule the next day, and harvested a field two of
three platforms do not serve.

**What this does not reopen.** The need-harvest retirement (F098, F100) stands.
Those rows were labelled `unserved-open` from an outcome field — reply count,
close reason, company response — which **both** platforms do return. Only the
`view_count` cells are affected. F100's corpus classification, its 82% GitHub
false-positive rate, and its 55% non-software share are untouched.

**Rejected: keep the instrument and find a platform that publishes arrivals.**
That is not a rejection of the instrument, it is its scope. Stack Exchange
publishes `view_count` and the measure is real there; E070's CFPB arm is a
second surface where an arrival exists by construction (one complaint, one
arrival). What is refused is claiming the instrument works on surfaces that do
not publish the field.

**Rejected: repair it by proxying.** `comments`, `score`, or reactions are
*response* counts, not arrivals, and F039 already measured that response is a
poor proxy for need. Substituting one would make the instrument's name true and
its reading false, which is the error being corrected.

**Ceiling.** Scoped to public documented API response objects — the only surface
E063/E066 harvested and the only one a reproduction can use. This does **not**
claim Hacker News or GitHub expose no view counters anywhere: a web UI or an
undocumented endpoint is untested, and GitHub's per-issue
`reactions.total_count` was probed for and is not an arrival count. The claim is
the narrow one that blocks the landing — the corpora carry no arrival field, so
the software-arm cell cannot be a measured zero.

## D089 — Land an unlanded tree on its corrected record, not on its summary, and never commit the bytes a manifest describes (2026-10-09)

`observed` 2026-10-09, session 2026-10-09-002, E070, F101, defect 26.

**The situation.** Six finished sessions and five experiment directories were
on the tree, uncommitted and unrecorded, while `STATE.md` described E070 as
landed. One of them carried a 5.5 GB CFPB CSV and its 336 MB archive with **no
source manifest**, so `git add -A` would have committed half a gigabyte of
third-party data, and a `MISSION-OUTCOME.json` asserted
`"mission_status": "Phase B complete, instrument validated"` with four
`observed`-sounding claims — two of which E071 has just falsified.

**The decision.** Three rules, each fixing an observed problem:

1. **A landing carries the correction, not the summary.** The four unlanded
   experiments land with E071's finding recorded against them, and
   `MISSION-OUTCOME.json`'s unsupported claims are not preserved as recorded
   facts. An experiment's own summary is an artifact to verify, never the
   record — the gap this session found is exactly the gap that rule closes.
2. **Third-party bulk input is recorded by hash, never committed.** E070's
   `raw/SOURCES.md` carries url, sha256 and bytes per file, and `.gitignore`
   excludes the two bulk files by the same clause already applied to `sdists/`
   and E066's `raw/*.csv`. Only the 6 MB deterministic sample tracks, and the
   manifest records that the sample is the **head** of a date-descending CSV —
   the limitation the original run did not state, and which a reader of the
   hash alone could not know.
3. **The identifier allocator is read before it is trusted, and its output is
   checked against the record.** Defect 26: `NUMBERED_CELL` had no word
   boundary, F097's row quotes the bike serial `SNACEOSF18391`, and the
   allocator handed out **F184** — 83 numbers past the real F100. The rule
   against counting a citation as an allocation was already written in that
   module, and a stricter pattern sat in the gate next door.

**Rejected: delete the unlanded experiments.** They are the record of what was
run, including a falsified claim; deleting the claim and keeping the run is the
one thing an evidence repository must not do. **Rejected: commit the CFPB
sample plus the bulk files.** 5.5 GB of vendored input that nothing verifies.
**Rejected: rewrite `MISSION-OUTCOME.json` into the corrected claim.** A
summary file is an artifact of the session that wrote it; the corrected claim
belongs in F101, D089, and `STATE.md`, where a reader is told what was measured.

**Ceiling.** This governs the landing of work already done. It does not make an
unlanded experiment's *internal* analysis correct — E069's non-software arm is
landed as read, with only its software comparison withdrawn. The `git add` path
was checked with a dry run rather than by attempting the add, so "the bulk
files are excluded" is `observed` from `git add -An`, not from a commit that
was made and inspected.