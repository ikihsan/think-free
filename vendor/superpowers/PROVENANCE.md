<!-- origin-meta
owner: vendor/MANIFEST.md
status: active
last-verified: 2026-10-03
-->

# Superpowers — provenance

Superpowers is vendored under the MIT licence. It is third-party work, not ours,
and this file exists so a reader can tell exactly what came from where.

## What was taken

The `skills/` directory of `obra/superpowers` at tag `v6.2.0`, copied verbatim.
Fourteen skills, 452 KiB, 38 Markdown files.

## Licence

MIT, Copyright (c) 2025 Jesse Vincent. The full text ships alongside this file
at [`LICENSE`](LICENSE) and must travel with any redistribution of these
files.

## Verification performed at vendoring time

- Cloned `https://github.com/obra/superpowers` at tag `v6.2.0`, resolving to
  commit `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9`.
- Ran `diff -rq <clone>/skills .agents/skills`.
- Result: no differences. This is an `observed` fact about the copy on
  2026-10-03, not a permanent guarantee.
- Recorded per-file SHA-256 in [`../hashes.json`](../hashes.json).

## Not taken, and why

- Upstream `CLAUDE.md` — contributor rules for the Superpowers repository
  itself, including a PR-rejection policy. Irrelevant and misleading here.
- `hooks/` and `.claude-plugin/` — tied to one agent's plugin loading mechanism
  and one installation layout.
- `.opencode/`, `.codex-plugin/`, `.cursor-plugin/`, `.kimi-plugin/`, `.pi/`,
  `.agents/plugins/` — per-agent extension shims for tools this repository does
  not depend on.
- `RELEASE-NOTES.md` (91 KiB) — useful when updating, not needed in the tree.
  Read it from upstream at update time.

## Relationship to this repository

These skills are used as authored. Local behaviour is adjusted only through
`AGENTS.md`, which overrides three things: where plans are written, when a
design needs human approval, and how skills are discovered. No vendored file has
been edited. If an override stops being true, fix `AGENTS.md` rather than
patching a vendored file.

## Security note

Vendored skill text is instructions an agent may follow. It is upstream code
under an active licence, reviewed by its maintainers, and recorded here by hash
so a change is visible. It is not, however, code this repository has audited
line by line. Anyone extending these skills should read them first.