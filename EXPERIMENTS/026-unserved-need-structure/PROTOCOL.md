<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

# E026 protocol — is the corpus's unserved tail structured?

**Written 2026-10-05, before the first text fetch.** Task T-0070.
Declarations here are fixed before any number below is observed.

## The question

E022 (F042) measured that 58.0% of 1401 publicly stated needs were answered
in thread; F043 withdrew the `served` figure; F045 closed the closure of the
corpus. The one sub-population the record has never read is the **589
statements that drew no reply at all**. This experiment asks: does that tail
carry structure — in trigger phrase, in statement length, in story venue — or
is it the diffuse tail any such corpus would produce?

This is the last open reading named for the corpus, and it is a third read of
a population already read three times. The budget is therefore small: text
fetches only, two readings, one null.

## Hypotheses, pre-registered

**H1.** Unserved statements are *shorter* than answered ones (materially
lower median word count): a vagueness signal.

**H2.** At least one trigger phrase is *over-represented* among unserved
statements (≥2× its share in the answered arm): the harvest's blindness is
structured, not uniform.

**H0.** Neither holds. The unserved tail is diffuse. H0 is a live, recorded
outcome, not a failure — it is what the closure of the corpus predicts.

Two worlds fit the record so far, and H1/H2 would distinguish them:
unanswered because the need was vague or off-topic for the thread (H1), or
unanswered because certain kinds of ask systematically get no answer (H2).
A diffuse tail (H0) means neither.

**Out of scope, declared.** Whether any unserved statement names a need no
artifact serves was E012's job (0 of 50, F029) and is not re-run. Whether
unserved requesters built their own need was F042's floor, corrected by F045.

## Instrument

For each of the 1401 rows in
`EXPERIMENTS/022-need-outcomes/raw/outcomes.jsonl`, fetch the comment via the
same Firebase item endpoint E022 used
(`https://hacker-news.firebaseio.com/v0/item/<id>.json`), and keep the raw
text, length in words, `dead`/`deleted` flags, story id, and trigger phrase.
Strip HTML tags before counting words. A failed read is `unreadable`, never
`answered` or `unanswered`.

## Gates, declared before the first fetch

- **A1 (instrument).** ≥95% of the 1401 fetches return a parseable text.
  Below that the run reports `not evaluable`.
- **B1 (H1).** Median word count of unserved statements is at least half the
  answered arm's. Below that, H1 fails.
- **B2 (H2).** Some trigger phrase's share among unserved is ≥2× its share
  among answered. Below that, H2 fails.

A1 passing with both B gates failing is the H0 outcome. One B gate passing is
a structure finding and names the trigger or the length regime; it is not,
by itself, a candidate — it is a measurement of where the corpus's requests
die.

## Limits, declared

One platform, one corpus, one reader of the text. Length is words after tag
stripping, not words a human would count. Trigger phrases are the same 23 E012
used, with the same known limit (F042: the vocabulary marks staters, not
outcomes). Nothing here measures demand, satisfaction, or what the requests
became.
