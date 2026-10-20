<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# E181 READER INSTRUCTION — `EXT` (the fact)

**Committed before `EXT` saw a file.** Given to one reader, verbatim. Nothing
changes between rows. The expected qid list and the directory path are appended
by the caller and nothing else does.

---

You are reading real failure reports from a question-and-answer site.

Each file gives you one question **exactly as the reporter posted it**, then
**the comments on the question**, then **the comments on the answer that was
accepted**. The accepted answer itself is not in the file and you must not go
and get it: do not open any other file in this repository, do not search the
web, and do not look the question up. You have what is in the file and you must
not want anything else.

Your job is to say what a competent helper would need to be **told** before they
could answer this question correctly.

## For each file, produce exactly one JSON object on its own line

```json
{"n": 1, "qid": 79723342, "fact": "...", "source": "comment", "quote": "..."}
```

Six fields, always all six, no extra fields, no fences, no commentary. Same
order as the files.

### `fact`

**The one fact or artefact the comments supply that the question does not, and
without which the right answer changes.** One sentence. It must be a *thing*,
not a topic: "the LangChain version the reporter has installed" is a thing,
"version issues" is a topic.

- Copy identifiers **verbatim** from the documents — `1.4.2`, `libc6`,
  `--legacy-peer-deps`, `com.apple.security.cs.allow-jit`, `Bun 1.2`,
  `python3.11`, a file path, a flag, a config key. Do not translate an
  identifier into its kind.
- If the answer needs more than one fact, name the one that changes what you
  would tell the reporter, and say so in the sentence.
- **The fact must be absent from the question as posted.** If the question
  already states it, it is not the missing fact.

### `source`

Where in the file you took it from: `"question_comments"` or
`"answer_comments"`. If what you are naming is not actually written anywhere in
the file, set `"fact": null` and continue.

### `quote`

**The comment span you took it from, copied exactly, one line, no more than 200
characters.** If `"fact": null`, this is `null`.

### When `fact` is `null`

Set it to `null` when the comments do not actually supply the deciding fact.
**This is a real and useful answer and you must not avoid it.** A guessed fact
is worse than a null here, because a null row is excluded and reported and a
guessed row is scored as if it were evidence. If you are unsure, say null.

## What you are not doing

You are not deciding whether the question is good, whether it deserves an
answer, whether the accepted answer is right, or whether anything could be done
about it. You are naming one thing and quoting where you found it.