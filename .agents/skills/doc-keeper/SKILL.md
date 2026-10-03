---
name: doc-keeper
description: Update the documentation graph when behaviour, structure, or results change, and keep every document under the 300-line cap. Use AFTER changing code, docs, or repository structure, before any commit, when a document has become false, or when doc lint fails. Triggers - "update the docs", "doc lint fails", "document this change", "the README is out of date", "add a new doc", or any change to commands, file layout, or recorded results.
license: MIT
compatibility: agent-agnostic
metadata:
  scope: repository-wide
  enforcement: tools/origin doc lint
---

# Doc keeper

A commit that makes a document false is an incomplete commit. This skill is the
checklist for not shipping one.

Standards: [`docs/policy/doc-standards.md`](../../../docs/policy/doc-standards.md).
Map: [`docs/INDEX.md`](../../../docs/INDEX.md).

## After changing behaviour or structure

Ask four questions. Each has a definite answer, found by searching, not guessing.

1. **Does a command reference change?** `AGENTS.md` has a command table;
   `docs/reference/cli-reference.md` has details. Both must match the code.
2. **Did a file or directory appear, move, or disappear?** Update the zone table
   in `AGENTS.md` and regenerate `docs/INDEX.md`.
3. **Did a recorded result change?** Update the document that states it and the
   raw artifact it points to. A result without a reachable artifact counts as
   `untested`.
4. **Did a rule change?** Update the policy document *and* any skill that
   repeats the rule. A rule stated in two places will drift.

```bash
tools/origin doc index      # regenerate the three generated maps
tools/origin doc lint       # must exit 0
```

## Writing a new document

```markdown
# Title

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

One or two sentences: the invariant that makes this document exist.
```

Then link it from exactly one index. An unlinked document is an orphan and
fails lint, because nobody will find it and it will rot.

Choose the owner deliberately:

| Document | Owner |
|---|---|
| Policy, standards, definitions | the `docs/policy/` index entry |
| How to do something | `docs/process/` |
| Running things here or elsewhere | `docs/operations/` |
| Generated tables and schemas | `docs/reference/` |
| Generated indexes | `sessions/INDEX.md`, `tasks/INDEX.md` |

## The 300-line cap

300 lines is the ceiling. **250 is the trigger**: at 250, split.

Split by section into siblings, leave a stub of 40 lines or fewer, and move the
content. A stub states what the family of documents is, lists the siblings, and
gives the invariant that makes the split sensible.

Split when a reader would otherwise load the whole file to answer one question.
Do not split mid-argument.

The cap applies to every tracked file, not just prose. A 400-line Python module
is telling you it has two responsibilities.

Two exemptions, both declared, both still reported by lint as `info`:

- vendored third-party content, listed in `vendor/MANIFEST.md`;
- machine data and raw logs (`.json`, `.jsonl`, `.log`).

## Generated files

Anything containing `<!-- generated-by: ... -->` is rebuilt by a command. Never
hand-edit one: `doc lint` regenerates and fails if the committed content
differs. To change one, change its source.

```bash
tools/origin doc index --check    # exit 2 if anything is stale
```

## What to do when lint fails

| Failure | Cause | Fix |
|---|---|---|
| `exceeds the 300-line cap` | File grew | Split it |
| `missing origin-meta block` | No metadata | Add the block |
| `orphan document` | Nothing links to it | Link it from its owner index, or delete it |
| `broken link` | Target does not exist | Fix the path or create the target |
| `generated file is stale` | Indexes not regenerated | `tools/origin doc index` |
| `exempt from cap` (info) | Vendored or data file | Nothing; informational |

Do not silence a lint failure by weakening the rule. The rules exist because
this repository is read by something with a small context window.

## Writing for a cold reader

- Lead with what to do, not with history.
- State what is **not** true as prominently as what is. Unknowns rot silently.
- Use ISO dates, and label them as retrieval or publication dates where the
  difference matters.
- Prefer linking to the raw artifact over describing it.
- One table beats three paragraphs of parallel structure.