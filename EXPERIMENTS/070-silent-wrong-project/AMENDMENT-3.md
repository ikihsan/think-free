<!-- origin-meta
owner: EXPERIMENTS/070-silent-wrong-project/PROTOCOL.md
status: active
last-verified: 2026-10-09
-->

# E070 — Amendment 3 (declared 2026-10-09,
before the first classification row was
recorded)

Reading the PC sample (unrecorded) exposed a
structural blindness in the control queries,
and the mechanism arm predicts it.

## The blindness

A silent-class report often **cannot name the
intended project** — not knowing the right
name *is* the failure. The report names the
name the user *typed*. A query that requires
both names (e.g. `telegram python-telegram-bot`)
therefore asks for text the B population does
not contain. The beautifulsoup pair recovered
B rows only because `beautifulsoup4` is the
word the answers use, not because the reports
contain it.

Consistent with this, the first PC reading
found, in the telegram pair's rows:

- `pip install telegram-bot` — a **third**
  near-miss name, resolving to a different
  real project whose 2013 `setup.py` dies
  with a circular-import error that never
  names the right package (a G row: the
  refusal is cryptic, not a guard);
- `pip install aiogram` — a different library
  entirely, install fine, import failing on
  the wrong interpreter (E).

No B row. Not because the failure is absent —
arm M installed `telegram` 0.0.1 silently on
bytes — but because the query cannot see the
report shape.

## The amendment

Add, for each control pair, the **typed-name**
query — the name a user would actually have
typed: `pip install telegram`, `pip install
sklearn`, `pip install beautifulsoup`, `pip
install color`. These are control queries, not
prevalence queries, so they do not touch the G
sample.

**K1a, restated (before the new rows are
fetched):** at least **2 of the 4 control
pairs** yield ≥ 1 B row across their queries
(pair-naming or typed-name). The gate's teeth
are unchanged — the instrument must recover
real silent-class reports on at least two
independent control pairs — but the recovery
channel now matches the report shape the
population produces.

K1b and K1c are unchanged (all 4 pairs yield
≥ 1 B∪G∪F row; κ ≥ 0.75 on the 20 % full-body
second pass).

## Why this is not weakening the gate

The original K1a asked a pair-naming query to
recover a report shape that structurally lacks
the second name. The restated K1a asks the
same question through a channel that can
physically contain the answer. It is stricter
in one way (the typed-name query also returns
the *guards'* own documentation and the
placeholder packages' own pages, which must be
classified E, not silently skipped) and it
keeps the failure condition: zero B rows on
two pairs still fails the instrument.

## The `bs4` placeholder, for the record

`bs4` on PyPI is a 0.0.x placeholder whose
own description is a pointer at
`beautifulsoup4`; installing it succeeds and
adds `beautifulsoup4` as a dependency. It is
the same class as the `sklearn` placeholder —
a real, different artifact a near-miss name
resolves to — and rows that installed it are
B rows with the note `placeholder`.
