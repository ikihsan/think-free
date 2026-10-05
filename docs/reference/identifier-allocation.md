<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Identifier allocation

How an F, D or T number is chosen, and why the choice is recorded. Every number
in this repository is a reference other documents resolve, so a number that
means two things breaks a reference rather than looking untidy.

This exists because of defect 5 in [`../../STATE-defects.md`](../../STATE-defects.md):
between 2026-10-03 and 2026-10-04, twelve times, two VMs took the same number.
`83aa9a4` and `569a7ce` each added a different `tasks/T-0024-*.md`; commit
`e6eb992` carries two `## F010` definitions; and one task on this VM was
renumbered through T-0026, T-0027, T-0028 and T-0029 in four separate commits
before it could be published. `observed`, from the history rather than from a
report about it.

**The thirteenth was the residual race below, caught exactly as it predicts.**
On 2026-10-04, 35 seconds apart, both VMs ran `task new` and both took
**T-0046**: this VM at `10:06:54Z`, `instance-20260717-0944` at `10:07:29Z`.
The other VM published its T-0046 (`measure how GitHub files an annotation on the
`file=` property`, `b2b8f34`) and claimed it; this VM's push was refused
non-fast-forward, which is the first of the two catches named below. The unpushed
side renumbered to **T-0047**, landed, and resolved the `tasks/CLAIMS.jsonl`
conflict by keeping all four lines. The 35 seconds are the measurement: the window
is *two VMs allocating between their own fetches*, and nothing here closes it.

## The rule

**Read the shared base. Never read the working tree alone.**

```bash
tools/origin id next F        # also D and T; --json prints every number it read
tools/origin task new --goal … --verify …    # uses the same allocation for T
```

`id next` fetches, then reads the numbered records at `origin/<base>` *and*
this working tree, and returns one above the highest number either side defines.
Uncommitted definitions count: a number this VM is about to commit is one it
must not hand out twice.

| Kind | Read at the base | Also read |
|---|---|---|
| `T` | `tasks/T-NNNN-*.md` | `tasks/CLAIMS.jsonl`, so a withdrawn task's number is not recycled |
| `F` | `## Fnnn` and `\| Fnnn \|` rows in root `FAILURES*.md` | a row with no definition is an allocated number too — that is what a half-finished renumbering leaves behind |
| `D` | `## Dnnn` and the spans in root `DECISIONS*.md` | a span declares both endpoints, which is what makes the decision log's numbering continuous |

A number only *mentioned* in prose is not an allocation. Treating a citation as
an allocation would make the allocator drift upward with every reference, so
only headings and table rows count.

## Read the line it prints

The source line is the only record of which copy of the ledger decided the
number. Three states are distinguishable, and a caller that collapses them
reports a confident number in every one (D030):

| Printed | State | Action |
|---|---|---|
| `origin/…@<sha> and this working tree (highest …)` | The base was read and is current | None |
| `origin/…@<sha>, last seen before a fetch failed (…)` | A published snapshot is being used; it may already be stale | Push and check before relying on the number |
| `this working tree only (…)` | No base, or none readable | The number is this VM's opinion; land the work and re-read |

`--json` adds `local_highest`, `remote_highest`, `fetched` and every identifier
that was read, so a disagreement between two VMs can be diagnosed without
re-deriving either side.

## The ceiling

**Two reads cannot be made atomic by reading either of them.** This narrows the
window from "however stale this VM's tree is" — hours, in practice — to "two
VMs that allocate between their own fetches". That residual collision is real
and is caught downstream rather than prevented:

- a non-fast-forward push rejection, which is `git` saying another VM published
  first, not this tooling;
- the detector half, T-0030, which refuses a commit that gives one identifier
  two definitions.

Renumbering is still a manual act on the side that has not been pushed, and it
is still recorded where the next reader looks. See
[`../process/multi-vm-coordination.md`](../process/multi-vm-coordination.md).

## The 2026-10-05 collision, and what it did to the session record

Both VMs allocated **T-0064** and both called their experiment **E019** within 23
minutes of each other, while working the same question by different routes. The
unpushed side (VM 0947) renumbered to **T-0065** and
`EXPERIMENTS/020-copied-config-drift`; the ledger kept both lines, because it is a
sequence of events.

**A consequence worth knowing before it happens again: renumbering a directory
invalidates the session's own artifact declarations.** The artifacts were declared
under the pre-renumber names, so that session's reconciliation reports **121
integrity errors** naming `EXPERIMENTS/019-copied-config-drift/…` for files that
exist and are declared under their current paths. Nothing is missing. The session
was already closed when this was discovered, so the note could not be appended to
the event stream, and it is recorded here instead — which is the same rule this
file exists to enforce.

**Declare the post-renumber paths, not the pre-renumber ones**, and re-run
`session artifact --dir <new path>` after a directory rename rather than trusting
the declarations made before it.

## What this does not do

- It does not reserve a number. Nothing here stops a VM holding a number it has
  not pushed yet, which is the residual race above.
- It does not read prose, so a number allocated in a commit message and never
  written into a numbered record is invisible to it.
- It does not check that a published record is *consistent*: two definitions of
  one number still pass it. That is T-0030's rule, not this one's.