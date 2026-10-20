<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E177 AMENDMENT 5 — one of the 60 treatment answers had unescaped quotes

**Declared before the repair is applied.**

`ans/answers.jsonl` was written one JSON object per line, and line 36
(qid 79806553) contains a literal `"` inside the answer string — it quotes
PyCharm's own message — which makes that line invalid JSON. **59 of 60 lines
parse; one does not.**

**Repair.** `repair.py` reads the raw line, takes the text between the first
`"answer": "` and the trailing `"}` as the answer verbatim, re-escapes the
interior quotes, and rewrites the line. The **content is not edited, trimmed or
summarised** — the same characters, correctly escaped. The script refuses to
touch any line that already parses, refuses any line whose qid is not in
`ans/order.json`, and prints the before/after character counts so a reader can
confirm nothing was dropped.

**Why it matters to record.** This is the fourth instrument defect of this
experiment and the second of a *format* kind (with AMENDMENT-4), both in a
pipeline whose only job was to move bytes between readers. The record's FORMAT
section should carry the general lesson: a model asked for JSON Lines will
eventually emit an unescaped quote, and a parser that stops is better than a
parser that guesses — but a script that re-escapes without re-reading is
also the place a silent content change would hide. Hence the character counts.