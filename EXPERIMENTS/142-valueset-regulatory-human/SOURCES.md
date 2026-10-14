<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E142 SOURCES

## Corpus

| | |
|---|---|
| source | US Federal Register API v1 |
| endpoint | `https://www.federalregister.gov/api/v1/documents.json` |
| filter | `conditions[term]=final rule`, `order=newest`, `per_page=10`, 10 pages |
| fields | `document_number`, `title`, `abstract`, `publication_date`, `raw_text_url` |
| fetched | 2026-10-14, once |
| documents | 100 metadata entries; 88 with abstracts; 20 with full text fetched |
| full text | `raw_text_url` for each document, fetched as plain text |

## Reproduce

```bash
cd EXPERIMENTS/142-valueset-regulatory-human
python3 fetch.py           # re-fetches the corpus into raw/
python3 build_arms.py      # raw/ -> arms.jsonl
python3 score.py           # arms.jsonl -> gates.json
python3 explain_misses.py  # classify misses
python3 -m unittest test_e142
```

The corpus is re-fetchable but not committed (1.6 MB, gitignored). The
`fetch.py` script records the exact API parameters. Document metadata is in
`raw/documents.json` (gitignored, re-created by `fetch.py`).

## Instrument

| | |
|---|---|
| M2 | `EXPERIMENTS/140-judge-form-invariance/valueset.py`, imported unchanged |
| M1 | `EXPERIMENTS/114-value-grounding/ground.py`, imported unchanged |

Both are imported, not copied. Neither is edited, forked, or re-tuned.
