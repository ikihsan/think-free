<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Failures — recorded findings, part 3 (F013 onwards)

Continues [`FAILURES-findings-2.md`](FAILURES-findings-2.md), which holds
F009–F012 and reached the 300-line cap at F013. **Identifiers are stable across
all three files**: a reference to `F012` means the same entry wherever it
appears. New findings are appended here.

**The invariant is unchanged by the split.** Findings are separated from
`FAILURES.md`'s live list because a reader must be able to tell a disproved
claim from a still-open question. The files split by line cap, not by subject:
part 1 holds F001–F008, part 2 every finding after it up to the cap, part 3 the
rest.

## F013 — Three mission records were committed with conflict markers, and every gate passed

Source: T-0021, commit `fd7b4a1`, repaired in `FAILURES.md`, `FAILURES-findings-2.md`,
and `DECISIONS-GATING.md`. Rule: `tools/originlib/conflicts.py`, doc lint rule 6.

**What happened.** The third identifier collision of 2026-10-03 was renumbered by
hand while a rebase was in progress, and the commit went out with `<<<<<<< HEAD`
still in three mission records. `FAILURES.md` and `FAILURES-findings-2.md` each
held a complete block; `DECISIONS-GATING.md` held one block plus a terminator
left behind with nothing open. F011 and F012 were ambiguous exactly where the
markers sat: the renumber had deleted an F011 that had meanwhile become a
different VM's finding, so the "empty" side of the conflict was wrong and the
records were unreadable in the region that decides what is disproved.

**Why every gate passed.** `doc lint` checked line counts, metadata, links,
orphans, and generated-file drift — never whether the *text* was a resolved file.
`session verify` checks the event stream. `skills verify` checks vendored
hashes. Reconciliation compares trees, not content. A marker is a content defect
in files that every existing rule reads for a different reason.

**Fix and its falsification.** The repair keeps both sides of all three regions,
because both sides carried distinct claims (F011 and F012 are different
findings). The gate is `doc lint` rule 6: exactly seven `<`, `|` or `>` at
column 0 opens or closes a block, a seven-character `=` divider belongs to a
block only when one is open, and a block is reported once at its opening line. A
file may declare `origin-allow-conflict-markers`, reported as `info` so a waiver
is never silent.

**The rule was wrong before it was right.** The first implementation reported
only *malformed* blocks. Run against the three historical files it found one
defect out of four, because a well-formed `<<<<<<< / ======= / >>>>>>>` triple
is exactly what a committed unresolved conflict looks like. The kill gate — scan
the pre-fix bytes, require a finding per defect — is what caught it. Same clause
shape as D024: the gate clause was implemented as a weaker proxy.

**Classification.** Record-keeping defect, found by reading the base branch
rather than by a gate. Fourth collision of the evening, and the first one whose
damage outlived the session that caused it.

**Lesson kept.** A gate that checks structure cannot catch a structural mistake
in content, and a repair performed by hand during a rebase is the highest-risk
edit in the repository. What made this survivable was that the markers were
still text: nothing had been lost, only made ambiguous.