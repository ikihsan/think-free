<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E125 amendment 1 — three instrument corrections, made after a pilot

Written 2026-10-13, after a pilot run of `probe.py` and **before** the
measurement run. The gates G1–G5 in `PROTOCOL.md` are unchanged. Nothing here
was decided by looking at a C1 verdict, because the pilot produced three pairs
and no verdict was read from any of them yet.

## What the pilot showed

`probe.py` found 3 qualified pairs across 22 repositories. Before that could be
read as a fact about harnesses, the candidate list it drew from had to be
checked, because a low count from a capped draw is a fact about the draw.

**Correction 1 — the candidate list was a prefix, not the population.**
`fetch.py` took the first 25 data files per group in tree order. Counting
output-shaped data files over each repository's **full** path listing gives
**140** across the population — `suyoumo/ClawProBench` 86, `trpc-group/trpc-agent-go`
26, `openai/evals` 9, `responsibleai/ASSERT` 5 — against 38 key-shaped files.
The pilot read a small fraction of those. The pilot's pair count therefore
measured the cap, not the population.

Repair: candidate selection is driven over the **complete** listing with
declared patterns and a declared cap of 60 per group, applied identically to
all 22 repositories.

**Correction 2 — `load_rows` reported YAML as readable.** `DATA` included
`.yaml`/`.yml`, and the loader sniffed content rather than dispatching on the
extension, so a YAML file fell through to the CSV branch and "parsed" into rows.
The repositories' GitHub workflow files appeared as 55-, 59- and 34-row record
sets. A file the loader cannot parse must be `unreadable`, never `clean`.

Repair: the loader is extension-dispatched and reads **JSON, JSON-Lines, CSV,
TSV and nothing else**. There is no YAML parser in a standard-library-only
loader, so a `.yaml` file is `unsupported format`. A `.md` or `.txt` file is
`unsupported format` for the same reason. This is stricter than the pilot and it
is the honest answer to Q1: a third party needs a real parser for those, and
those lines would be M1 tax.

**Correction 3 — 26 files were Git-LFS pointer text, not data.** The partial
clone fetched no blobs by design; for LFS-tracked paths the blob is a three-line
pointer beginning `version https://git-lfs.github.com/spec/v1`. The loader read
it as a one-column record set. A pointer is not data.

Repair: content beginning with that line is `git-lfs pointer; content not in this
clone`, counted as unreadable.

## The field vocabulary was calibrated against the population, once

The pilot's field-name frequency table is committed as `fieldnames.json`. The
side vocabularies in `probe.py` were replaced by **stem matching**: a field is
an identifier if its name, lower-cased with non-alphanumerics removed, contains
one of the declared id stems; likewise for the key side and the output side. The
stems are listed in `probe.py` beside the frequency that motivated each.

This calibration can only *add* proposed pairs. It cannot bypass M4, which is
unchanged: a shared identifier-shaped field **name** and row counts within an
order of magnitude, or the pair is refused and the refusal is recorded.

## What is still true of the pilot

One thing survived the corrections and is worth stating early: across the pilot's
readable files, output-shaped fields appeared far less often than label-shaped
ones. That is a hint about the population and it is **not** a result; the
measurement run decides it, over the full listing rather than a capped prefix.