<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E177 AMENDMENT 1 — `filter=withbody` returns tags as strings

**Declared before the re-run.** `fetch.py`'s first run raised
`TypeError: string indices must be integers` at the tag line and wrote no
`rows.json`. No answer body was read and no measurement was taken before the
fix. The default Stack Exchange filter returns tag objects and `withbody`
returns bare strings; the line now accepts both.

This is an instrument defect of the shape F044 names — the two filters are both
in use in this repository — and it is recorded because a re-run that silently
produced different rows would be worse than a crash. Nothing in the protocol's
definitions, arms, gates or bars changed.