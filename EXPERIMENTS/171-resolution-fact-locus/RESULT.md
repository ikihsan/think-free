# E171 Result — version_fact pre-condition for E168's G3

**Experiment**: E171 — Pre-condition screen on E168's G3: are the unaided-failed resolutions version facts?

**Protocol**: PROTOCOL.md (with AMENDMENT 1 and AMENDMENT 2)

**Date**: 2026-10-16

## Summary

**G1 FAIL**: version_fact share over 13 unaided rows = 2/13 = 0.1538 < 0.40 threshold.
G1 failing withdraws E168's G3. The version-pinned line closes as served-by-thread
with the reason measured — the missing fact is not a version-history-groundable fact,
it is a property of the thread itself.

**G2**: version_fact share over 11 served rows = 4/11 = 0.3636.

**G0**: PASSED (10/10 probe agreement; constructed labels matched the
any_version signal used to build the probe).

## Classification of the 13 unaided rows

The unaided attempt failed on 13 rows. Each thread's operative resolution was
classified into one of six mutually exclusive classes:

| idx | Classification | version_fact? |
|-----|---------------|--------------|
| 1   | thirdparty_fact | NO |
| 16  | other          | NO |
| 20  | other          | NO |
| 31  | surface_fact   | NO |
| 32  | **version_fact** | YES |
| 38  | other          | NO |
| 43  | surface_fact   | NO |
| 55  | no_fix         | NO |
| 60  | other          | NO |
| 62  | surface_fact   | NO |
| 65  | other          | NO |
| 67  | environment_fact | NO |
| 69  | **version_fact** | YES |

Only 2 of 13 resolutions are `version_fact` — facts about which version of the
named component introduced, removed, changed, or fixed something. The remaining 11
are surface facts, environment facts, no_fix, third-party facts, or other.

G1 gate (≥ 0.40 over 13 unaided rows): **FAIL** (2/13 = 0.1538).

## Classification of the 11 served rows

| idx | Classification |
|-----|---------------|
| 0   | other         |
| 17  | **version_fact** |
| 35  | environment_fact |
| 36  | **version_fact** |
| 37  | other         |
| 48  | thirdparty_fact |
| 61  | **version_fact** |
| 63  | environment_fact |
| 64  | thirdparty_fact |
| 66  | environment_fact |
| 68  | **version_fact** |

4 of 11 served resolutions are `version_fact`.

G2: version_fact share over 11 served rows = 4/11 = 0.3636.

## What this decides

**G1 failing withdraws E168's G3.** The declared bar is version_fact ≥ 0.40 over
the 13 unaided rows. At 2/13 = 0.1538, the ceiling is well below the floor, so
G3 cannot pass even in principle — no amount of version history grounding can
serve rows whose resolutions are not version facts.

**The version-pinned line closes as served-by-thread.** The 13 unserved rows'
resolutions are: surface facts (config keys, API settings), environment facts
(OS/machine state), no_fix statements, third-party service behaviours, and other.
None of these are `version_fact` — they are facts about the thread's context,
the asker's machine, or the absence of a fix. The strongest accessible
alternative (a free general assistant, with or without retrieval) serves this
class at the E126 pool-level rate of 0.6750, but the class itself is not
servable by version-history grounding because the missing information is not
about which version fixed the issue.

This is the cheapest closure this record could produce: G1 fires on its own
pre-condition, E168's G3 is withdrawn, and the version-pinned class closes
without a build candidate. The line closes with a clear, measured reason —
not an assertion.

## Next action (recorded in STATE.md)

Per the named next action, the mission returns to fresh observation in a
domain this record has not touched (E172). The version-pinned line is not
reopened.

[PROTOCOL.md](PROTOCOL.md) ·
[AMENDMENT 1](PROTOCOL-AMENDMENT-1.md) ·
[AMENDMENT 2](PROTOCOL-AMENDMENT-2.md)