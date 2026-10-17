<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E175 AMENDMENT 2 — an extractor defect found by its own first run, and the structural limit it uncovered

**Date:** 2026-10-17. **Before any rate was computed on the repaired
extractor.** G1 returned **0 of 21 = 0.0000**, Wilson [0.0000, 0.1546], and the
declared kill fired. Reading the run before accepting the kill: **12 of the 21
rows made zero registry requests at all**, which is not evidence about
registries — it is a defect in `derive.py`.

## The defect, stated so the repair can be checked against it

`derive.py` collected candidate artifacts in **document order** and stopped at
the **first registry hit**. Both are wrong in a way that a reader can confirm:

| row | gold | derived | what happened |
|---|---|---|---|
| 79380514 | `tailwindlabs/tailwindcss` | `npm/cli` | the tag `javascript` produced the candidate `javascript`, and the generic word **npm** was looked up *before* the specific `tailwindcss`; first hit wins, so the pipeline returned npm's own CLI repository |
| 79775796 | `vercel/next.js` | `microsoft/typescript` | same ordering fault — the project's own package name was never reached |
| 79363302 | `microsoft/vscode` | — | tag `vs-code` was de-dashed to `vscode` and the **raw tag was never added**, and `vscode` has no registry entry |

## The repair — general rules only, no per-row patch

1. **Specificity ordering.** Candidates are split into *specific* (a SO tag, a
   `node_modules` path, a backticked token, a stack-frame file, a `name@version`
   form) and *generic* (one of the 40 ecosystem words). **All specific
   candidates are tried before any generic one**, each group in first-seen order.
   The earliest hit within a group still wins.
2. **Both tag forms are candidates** — `vs-code` and `vscode`.
3. **Every failure is classified**, not pooled: `correct`, `wrong_repo` (a
   registry resolved, to a different repository), `no_candidate` (nothing
   registry-backed was named at all), `not_in_registry` (specific names were
   named and none resolved).
4. **G0 now also records `fork` and `parent.full_name`** for every gold
   repository, at no extra request. The gold repositories that no registry can
   name are, on inspection, forks and non-distributed projects — `cplusplus/draft`,
   `itanium-cxx-abi/cxx-abi`, `rust-lang/libs-team`, `duclq92/ffmpeg-kit-audio`
   (a fork), `git-for-windows/git`. Whether that is the actual shape of the
   population is **measured by G0, not assumed here**.

**The rule that keeps this honest:** the repair may change how a candidate is
*ordered and spelled*. It may not add a mapping for any project this run
revealed. `tailwindcss → tailwindlabs/tailwindcss` is obtained by asking npm
about the package the asker named, not by writing down the answer.

If G1 still fires after the repair, the kill stands and the classification above
is the finding: the mechanism fails because **the repository that owns a fix is
often not a package registry entry**.
## Amendment 3 (same date, same hour) — a whitelist of 20 package names was this author's invention and it contradicted the protocol

Reading the 15 `no_candidate` failures showed the ordering repair could not have
helped: `derive.py` held a table `REGISTRY = {"django": "pypi", "react": "npm",
…}` and **only consulted a registry for a name in that table**. Every package the
author had not thought of — including `tailwindcss`, named in the report — was
silently excluded before any request was made. PROTOCOL.md declares the opposite:

> **Registry lookup, in this fixed order:** PyPI … npm … crates.io … The first
> `github.com/<o>/<r>` found is the candidate repository.

The order is over **registries, applied to every candidate**, not over a package
whitelist. The repair restores the protocol: each candidate, specific ones first,
is tried against PyPI, then npm, then crates, and the first hit wins. The
whitelist is deleted.

This is the **second** defect in the same function, and the honest reading is
that the instrument, not the mechanism, produced the 0. Both repairs are logged
rather than folded into a "fixed extractor", because a reader needs to know how
many times this number was wrong before it was right.
