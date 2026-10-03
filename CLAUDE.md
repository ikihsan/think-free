<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# CLAUDE.md

This repository keeps one agent contract: **`AGENTS.md`**. Read it first; it is
the canonical instruction set for every agent working here.

@AGENTS.md

Two local notes that matter in Claude Code specifically:

- Project skills live in `.claude/skills/<name>/`, and each entry is a symlink
  to `../../.agents/skills/<name>`. The real files live in `.agents/skills/`.
  Edit the real file, never the symlink target's copy in another tool's tree.
- Do not add rules to this file. They belong in `AGENTS.md` so every agent sees
  them. This file exists only to point at it.