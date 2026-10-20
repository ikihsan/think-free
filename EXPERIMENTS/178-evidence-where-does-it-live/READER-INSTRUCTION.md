<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E178 READER INSTRUCTION — the re-key (M2)

**Committed before the reader saw any row.** Given to one reader per batch,
verbatim. The batch directory path and the expected qid list are appended by
the caller; nothing else changes between batches.

---

You are reading failure reports from a question-and-answer site. For each one,
a question is paired with the answer the community voted highest.

Your job is to say what that answer **knows that the question does not say**.

You are given N files in one directory. **Read only those files.** Do not read
any other file in this repository, do not search the web, and do not look up the
question on the internet. You have no other information and you must not want
any.

## For each file, produce exactly one JSON object on its own line

```json
{"qid": 12345678, "missing_evidence": "...", "where": "...", "discriminating": true, "basis": "..."}
```

Five fields, all five always present, no extra fields, no markdown fences, no
commentary before or after the lines. Output the lines in the same order as the
files.

### `missing_evidence`

**The single most load-bearing fact or artefact that the key answer depends on
and the question does not contain.** One sentence. It must be a *thing*, not a
topic: "the installed version of the library the reporter is actually calling"
is a thing, "version issues" is a topic.

Rules:

- **If the key answer's resolution is reachable from the question's own text
  with no fact added, write `"none"`** and `"where": "none"` and
  `"discriminating": null`. Do not invent a missing fact to fill the field. This
  is a real and useful answer; do not avoid it.
- If the answer needs more than one fact, name the one that changes what you
  would tell the reporter, and say so inside the sentence if you must
  ("their exact compiler flags, which select between these two causes").
- Copy identifiers verbatim from the documents (`8.0.19`, `libc6`, `glibc`,
  `numpy 1.24`, `python3.11`) when the documents name them. Do not translate an
  identifier into a description of its kind.

### `where`

Where that thing lives. Apply these in order and take the **first that fits**.

1. `"asker_only"` — it is a property of *this reporter's instance*, so no
   document anywhere could state it: the version they have installed, the flag
   they passed, the value in their config or environment, the contents of their
   data, their operating system's build, the steps they actually ran.
2. `"third_party"` — it is a property of some organisation **other than** the
   one answering and other than the reporter, and that organisation states it
   in its own documentation, store, or specification: a framework's internal
   behaviour, a standard's text, another package's defaults.
3. `"publishable"` — it is a property of the organisation that answers, and it
   is stated in something that organisation **publishes**: changelog, release
   note, specification, commit, source file, documentation of its own
   behaviour, upstream issue thread.
4. `"none"` — with `missing_evidence: "none"`.

**Tie-breaks, declared:**

- A fact that has both an instance part and a published part
  (`which version they are on` + `what that version changed`) is bucketed by
  the **instance part**, because the instance part is the one no document
  states. Say so in `basis` when you do this.
- `"publishable"` requires a **specific published artefact you can name**, not
  the possibility that the organisation might publish it. If you cannot name
  the artefact (the changelog, the flag's documentation page, the issue
  thread, the source file), the bucket is `"asker_only"` or
  `"third_party"`.
- Where you are genuinely torn between `asker_only` and `third_party`, take
  `asker_only`.

**Do not weigh which answer is more useful.** Both buckets lead somewhere in
the experiment that commissioned you, so a preference in either direction makes
your output worthless as a measurement. Apply the rules mechanically.

### `discriminating`

- `true` — **the resolution would plausibly be a different resolution if this
  fact took a different value.** The posted symptoms leave more than one cause
  open and this fact selects between them. A version whose changelog between two
  releases says exactly this is `true`; a version that merely confirms the
  diagnosis the symptoms already forced is `false`.
- `false` — the resolution is the same with or without this fact; the fact
  confirms it.
- `null` — only with `"where": "none"`.

Judge this against the **key answer**, not against what you would have needed.
Do not decide it from your own diagnosis of the problem.

### `basis`

One clause, and it must **quote at least six consecutive words** from the key
answer (or from the question, when `"where": "none"`) that show why. Verbatim
quotation only. `basis` is checked mechanically and a non-quoting basis fails
the run's reader control.

---

## What happens to your output

It is scored by a script that rejects any line with a missing field, a value
outside the declared vocabulary, a `basis` that does not quote, a duplicated
`qid`, or a `qid` that is not in your batch. If the reader control fails, every
number downstream of this batch is reported as `not_established` instead of as a
measurement. Precision in the format is worth more than volume.