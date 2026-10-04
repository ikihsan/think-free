<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Documentation standards

Enforced by `tools/origin doc lint`. Exit code `2` means a violation.

## Why a hard line limit

An agent reloads `STATE.md` and then follows links. A 900-line file it must read
whole is both expensive and easy to summarise wrongly. The 300-line cap keeps
every document small enough to read completely and cheap enough to link
precisely. It is a correctness constraint, not a style preference.

## The rules

### 1. No tracked file exceeds 300 lines

Applies to **every** file tracked by git: Markdown, Python, YAML, JSON — not
just prose. Code split at 300 lines is normally better code anyway.

Two exemptions, and only two:

| Exempt | Where it is declared |
|---|---|
| Vendored third-party content, kept byte-identical to upstream | `vendor/MANIFEST.md`, by name |
| Append-only logs and machine-generated raw results | Marked in `docs/policy/logging-standard.md` |

Exempt files are **still reported** by lint as `info` lines with their line
counts. Exemption means "not a failure", never "invisible".

### 2. Split at 250 lines, not at 300

300 is the ceiling; 250 is the trigger. When a document passes 250 lines, split
it by section into siblings and leave a short stub. A stub is 40 lines or fewer
and contains: what the document is, a table of the siblings, and the invariant
that makes the split sensible. Never split mid-argument; split where a reader
would otherwise load the whole thing to answer one question.

### 3. Every document declares metadata

Immediately after the title:

```markdown
<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->
```

- `owner` — the index that must link this document. Exactly one.
- `status` — `active`, `draft`, `sealed`, `archived`.
- `last-verified` — the date a human or agent last checked the content against
  reality. Update it when you verify, not when you merely edit.

The block is an HTML comment, so it renders as nothing.

### 4. Every document is linked from exactly one index

An **orphan** is a document no index references: nobody can find it, so it will
rot. An index is any document whose frontmatter declares `index: true`, or the
generated maps `docs/INDEX.md`, `sessions/INDEX.md`, `tasks/INDEX.md`. Indices
list their children explicitly so lint can check both directions.

### 5. Relative links must resolve, inside this repository

A link to `docs/policy/foo.md` that does not exist is a broken link and fails
lint. Use forward slashes and repo-root-relative paths for cross-directory
links so a document can be moved without rewriting every reference silently.
Links to external URLs are not checked; record the retrieval date instead.

**A link must also stay inside the repository.** One that resolves above the
checkout — `../../docs/x.md` from `tasks/`, or an absolute path — is reported as
`link leaves the repository` rather than tested for existence, because existence
is a question about the checkout's *surroundings*: the same bytes passed in a
worktree under `.worktrees/` and failed in the main checkout, which is defect 19
and D041. A link needs one `..` per directory it climbs out of; from `tasks/` that
is one, never two.

### 6. Generated files are marked and never hand-edited

Anything `origin` writes carries:

```markdown
<!-- generated-by: origin <command>; do not edit by hand -->
```

Lint regenerates into a temporary directory and fails if the committed content
differs. To change a generated file, change its source.

### 7. Links are claims too

Prefer linking to the raw artifact over describing it. If a document asserts a
result, the reader must be able to reach `results.json`, the run log, or the
source URL that produced it. A claim with no reachable evidence is treated as
`untested` no matter how confident the prose sounds.

### 8. A commit that falsifies a document is incomplete

If behaviour, structure, or results changed, the documents describing them
change **in the same commit**. If that is impossible, the commit message says
which document is now stale and why, and the next session's first action is to
repair it. Silent staleness is the failure mode this repository exists to
avoid.

### 9. No tracked file may hold an unresolved merge conflict

Rules 1–7 read a document for one property each, so a file can satisfy all of
them and still be a corrupt file. A committed `<<<<<<< HEAD` did exactly that:
three mission records reached the shared base with markers in them while every
gate passed (`FAILURES.md` F013).

`doc lint` now reads every tracked text file for git's marker shape — exactly
seven `<`, `|`, or `>` at column 0 — and reports a block once, at its opening
line. A seven-character `=` is a divider only inside an open block, because
`sessions/*/commands.log` is full of bare `=======` separators that are not
conflicts. Binary and undecodable files are skipped rather than guessed at.

A file whose text must contain a marker at the start of a line — a process
document showing a reader what an unresolved conflict looks like — declares the
waiver and is reported as `info`, never silently skipped:

```markdown
<!-- origin-allow-conflict-markers -->
```

Stated limitation: a marker indented inside a fenced code block is not
detected. Git's `text` merge driver writes markers at column 0, and treating an
indented example in a document as corruption would be the worse failure.

## Writing for a cold reader

- Lead with what the reader must do, not with history.
- State the invariant that makes the document exist in one line at the top.
- Prefer tables for anything with more than three parallel items.
- Record what is **not** true as prominently as what is. Unknowns rot silently
  unless they are written down.
- Use ISO dates (`2026-10-03`) and label them as retrieval or publication dates
  where the difference matters.

## What lint does not check

- Whether prose is clear. A machine cannot tell you this.
- Whether a `last-verified` date is honest. Only review can.
- Whether an argument is true. That is what experiments are for.