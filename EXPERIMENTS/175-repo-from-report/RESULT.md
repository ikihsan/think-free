<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E175 RESULT — the registry route derives the wrong repository, and the declared kill fires

**Date:** 2026-10-17. **G1 = 0 of 21 = 0.0000, Wilson 95% [0.0000, 0.1546]. The
declared kill (G1 < 0.20) fires. Nothing is built, and G2 is not run** — the
protocol says so, and spending index requests to measure the second stage of a
pipeline whose first stage returns a confidently wrong repository 20 times out
of 21 would measure nothing.

## The question

E174 reopened the version-pinned line on a fact E170 stored and did not report:
given the repository, the developer's own error string reaches the fix on **5 of
the 8** rows that have one, at a median of **one matching document in the whole
repository**. The only open step left was `report → repository`. Could it be
done mechanically, without a model and without a search engine, by asking a
public registry where the artifact the report names is developed?

## Population, and the ceiling it exposes

200 rows drawn by a committed seed from the pool's unexposed remainder, after
excluding the 40 E126 graded and the 13 E169 read in full. 181 question ids
returned by the API, **145 with answers**, 17 distinct gold repositories.

| | count | of 145 answered | of 200 drawn |
|---|---|---|---|
| answers contain a GitHub **repository** link (Gold-R) | **21** | **0.1448** | 0.1050 |
| answers contain a GitHub **issue/PR** link (Gold-D) | **10** | **0.0690** | 0.0500 |

This is the conditioning every rate in E168, E170, E174 carries, measured
directly for the first time: **about one high-arrival Stack Overflow question in
seven records its fix as a link to a repository, and one in fourteen to a
specific tracker document.** It is a ceiling on this line, stated before the
mechanism was measured.

## G0 — instrument-limited, and the limit is reported rather than read

The **first** run confirmed **17 of 17** gold repositories present, **1 of them a
fork** (`git-for-windows/git`), none archived. Later runs' G0 reads "5 of 17
present" and that number is **withdrawn**: `raw/repos.jsonl` shows
`HTTP Error 403: rate limit exceeded` on the unauthenticated core API
(60 requests/hour, spent across three runs of this script). An instrument-limited
rate is not a rate (D114). The valid figure is the first run's.

## G1 — 0 of 21, after four declared instrument repairs

| failure class | rows | meaning |
|---|---|---|
| `correct` | **0** | derived repository equals the gold |
| `wrong_repo` | **20** | a registry resolved, to a real but different repository |
| `not_in_registry` | 1 | candidates were named, none resolved anywhere |
| `no_candidate` | 0 | — |

The instrument was repaired four times, each repair declared in
[`PROTOCOL-AMENDMENT-2.md`](PROTOCOL-AMENDMENT-2.md) with its reason, and each
repair committed before the next run:

1. **Candidates were collected in document order and the first registry hit
   won**, so the generic word `npm` was looked up before the project's own
   package name and returned `npm/cli` for a Tailwind report.
2. **A 20-entry whitelist of package names decided which registry to ask.** It
   was this author's invention, it contradicted the protocol's declared order,
   and it excluded every package not on it.
3. **A loose body sweep** treated any hyphenated lowercase word as a package
   name — the strategy F131 had already measured as a noise source.
4. **Specific candidates now precede generic ones**, both tag spellings are
   kept, every registry is tried for every candidate, and candidates come only
   from sources that name an artifact.

The numbers did not move. What survived the repairs is a clean, reproducible
failure:

| row | gold repository | derived | first candidate |
|---|---|---|---|
| 79363302 | `microsoft/vscode` | `hapijs/code` | `code` |
| 79716280 | `more-itertools/more-itertools` | `alexfernandez/performance` | `performance` |
| 79442978 | `tailwindlabs/tailwindcss` | `oovm/tailwind-rs` | `tailwind-css` |
| 80002935 | `fmtlib/fmt` | `orsinium/advice` | `advice` |
| 79836280 | `powershell/powershell` | `christkv/node-git` | `git` |
| 79606837 | `microsoft/vs-solutionpersistence` | `rumpl/c` | (2 candidates) |

Every one of those is a **real repository with a real project URL**, reached
through a real registry lookup. The pipeline is not failing to find something;
it is confidently finding the wrong thing, because **a package registry is keyed
by distributable name, and the name a failure report carries is not the name its
project is published under.**

## Why, read off the 17 gold repositories

`microsoft/vscode`, `powershell/powershell`, `git-for-windows/git`,
`fmtlib/fmt`, `cplusplus/draft`, `itanium-cxx-abi/cxx-abi`, `rust-lang/libs-team`,
`baldurk/renderdoc`, `vercel/next.js`, `tailwindlabs/tailwindcss-intellisense`.

These are **applications, language runtimes, standards bodies, working groups
and language libraries**. None is a package-registry entry under the name a
report would use; several are not distributed through a registry at all. The one
project here that *is* on PyPI under its own name, `more-itertools`, was still
missed, because the candidate that resolved first was the ordinary English word
`performance` from the post.

So the failure has two parts, and the second is the interesting one:

- **Coverage.** The projects that own fixes are not registry entries.
- **Collision.** Where a name *is* a registry name, it is a common word owned by
  an unrelated package — `code`, `git`, `advice`, `tailwind-css`. Every collision
  yields a plausible, wrong answer, which is worse for a user than an abstention.

## What this closes, and what it does not

- **Closes:** the registry route. Declared, tested, killed at 0/21 with the
  reason measured rather than asserted. No retriever, no extractor, nothing
  built from it.
- **Does not close:** the step itself. `report → repository` remains the open
  step, and the measurement says the *source* is wrong, not the task: a **project
  index** (a map from project to tracker) is the right shape of source, and such
  indexes exist as prior art — libraries.io, ecosyste.ms, Homebrew and winget
  manifests, GitHub topics, Wikidata. Building another is not a contribution, so
  no prior-art screen is run and no novelty is claimed.
- **Does not establish:** anything about developers, about LLM-written
  extractors (which would do better and are not measured here), or about the 79%
  of answered high-arrival questions whose fixes are **not** a GitHub link at
  all — the largest bucket, and the one this line has never had a handle on.

## The number that matters most for the build decision

E174's 0.3846 was measured on 13 rows drawn from a corpus where tracker links
appear in **1 question in 14**. E175 now measures how such a repository is
reached and gets **0**. Composed honestly — and composition across two
experiments with different populations is an inference, not a measurement — the
best case for any tool of this shape on high-arrival Stack Overflow questions is
a small fraction of a small fraction. The version-pinned line closes for good,
with its ceiling named.

## Raw evidence

[`PROTOCOL.md`](PROTOCOL.md) · [`PROTOCOL-AMENDMENT-1.md`](PROTOCOL-AMENDMENT-1.md)
(draw 200, cap 12 lookups) · [`PROTOCOL-AMENDMENT-2.md`](PROTOCOL-AMENDMENT-2.md)
(three further instrument repairs, declared before each run) ·
[`sample.py`](sample.py) · [`derive.py`](derive.py) · [`qtext.py`](qtext.py) ·
[`run.py`](run.py) · [`sample.json`](sample.json) · [`queries.json`](queries.json)
(seed and drawn ids, committed before the first request) ·
[`derivation.json`](derivation.json) — the three raw capture files named in the
original write-up (`raw/se.jsonl`, `raw/http.jsonl`, `raw/repos.jsonl`) were
never committed and are not preserved in the tree.