<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E141 — SOURCES

## The corpus

`raw/` is **not tracked**: `EXPERIMENTS/*/raw/` is gitignored wholesale, and the
negations beneath it cannot re-include a file whose parent directory is
excluded. One unauthenticated request reproduces the file and
`build_arms.py` refuses to run on any other bytes, so the record that matters
is this one — url, digest, field mapping — and it is here rather than in the
ignored directory for exactly that reason.

| | |
|---|---|
| what | SQuAD v2.0 **dev** — 11,873 questions over 1,204 paragraphs, 35 Wikipedia articles |
| file | `raw/dev-v2.0.json` (gitignored; fetch the url below) |
| bytes | 4,370,528 |
| sha256 | `80a5225e94905956a6446d296ca1093975c4d3b3260f1d6c8f68bc2ab77182d8` |
| url | `https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json` |
| retrieved | 2026-10-14, one request, by `curl` |
| why this URL | The canonical `rajpurkar/SQuAD-Dataset` GitHub repository carries **train-v2.0.json only** — the dev split is not published there, and the path that would hold it returns 404 (observed 2026-10-14). The SQuAD Explorer's copy is the first-party SQuAD site and serves the identical dev split, under a different field spelling: rows carry `is_impossible` and no `isAnswerable` key, which is why `build_arms.py` reads `is_impossible` and `test_squad.py` checks arm membership against that field rather than against a constant. |
| licence | **not verified in this run.** SQuAD is generally distributed under CC BY-SA 4.0 and its paragraphs are Wikipedia text, but this run fetched a single JSON file and read no licence file, so treat the licence as `untested` and check it before redistributing these bytes. Nothing here is redistributed: `raw/` is gitignored, and the fetch is one unauthenticated request. |
| attribution carried in the data | `arms.jsonl` keeps the article `title` on every row, so the per-article Wikipedia attribution is preserved in the derived record that *is* tracked. |

`build_arms.py` refuses to run on any file whose size or digest differs from
the two values above, so the population cannot drift silently under the gates.
`test_squad.py::Corpus::test_identity` re-derives the digest from the bytes on
every test run.

## What was and was not fetched

One file, once, before `build_arms.py` first ran. No API key, no account, no
network access after that. Nothing in this experiment calls a service.

## The instruments

Not fetched. Both are imported from this repository, unchanged:

- `EXPERIMENTS/140-judge-form-invariance/valueset.py` (E140's M2)
- `EXPERIMENTS/114-value-grounding/ground.py` (E114's extractor and M1)

PROTOCOL.md §5 forbids editing either for this corpus, and neither is edited.
