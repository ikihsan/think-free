<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E055 — protocol amendment 3: the `not_evaluated` was the probe's blind spot

Written 2026-10-08 after run 3 and after the first ceiling probe, and before the
second one. Base protocol: [`PROTOCOL.md`](PROTOCOL.md); earlier amendments:
[`PROTOCOL-AMENDMENT-1.md`](PROTOCOL-AMENDMENT-1.md),
[`PROTOCOL-AMENDMENT-2.md`](PROTOCOL-AMENDMENT-2.md). Runs 1-3 and the first
ceiling probe are preserved unedited at `raw/results-run1.json` through
`raw/ceiling-run1.json`.

The verdict runs 1-3 produced is `do_not_build` with `verdict_state: partial`,
because `ceiling.py` recorded **`K3_away_from_U0: not_evaluated`**.

## The partial came from an instrument, and the instrument is replaceable

Both probes so far read the tool's *optional* `--as-numbered-lines` report. That
report prints every line the selection **spans**, so away from `-U0` its line
list contains context lines as well as carried ones and cannot tell the two
apart — which is why `ceiling.py`'s C10 is falsified away from `-U0` and the
boolean was recorded as undecidable there.

The tool's **primary** output has no such ambiguity. `filterdiff --lines=N`
emits a unified diff, and in a unified diff a carried line is exactly a `+` or
`-` body line while a context line begins with a space. Measured on bytes before
this amendment was written, on `a,b,c,d,e → a,B,c,D,e` naming line 2:

| context | selected patch carries | named beyond the want |
|---|---|---|
| `-U0` | old 2, new 2 | — |
| `-U1` | old 2 and 4, new 2 and 4 | **4** |
| `-U3` | old 2 and 4, new 2 and 4 | **4** |
| default | old 2 and 4, new 2 and 4 | **4** |

So the same number the `--as-numbered-lines` reader had to guess at is
**unambiguous in the patch's own markers at every context**, and the default
context a caller actually gets is one where the tool names the carried line.

## What this may change

Only `K3_away_from_U0`. KILL-C is already `do_not_build` on the `-U0` evidence,
and this can only confirm or strengthen that: if the patch markers name the
carried line at every context, K3 fails everywhere and the negative is no longer
context-bound. Nothing here can turn `do_not_build` into `build`, because K3's
question — *does the arm's own output give the caller no way to derive the same
verdict* — is answered by the arm's primary output whenever that output names the
carried line, and the ceiling rows already record that it does. **The direction
of this change is adverse to building**, and that is why it is recorded here
rather than folded into the code silently.

## Controls, both required, both about the new reader and neither about KILL-C

- **C11, agreement with git.** The lines the patch walk reports as carried must
  equal the lines `git diff --cached -U0` says the index actually touches, on
  every probed row. This is C8's comparison, run through a second reader: it
  holds the *walk* to git's own statement of the post-state rather than to the
  other probe, so the two readers cannot agree merely by sharing a bug.
- **C12, the walk is not trivially "everything".** On a fixture where the
  selection is exact, the walk must report the wanted line and **no** other
  line. Without this, a reader that reported the whole hunk would satisfy C11
  on the over-staging rows and make K3 unfalsifiable in the direction that
  matters.

C11 and C12 are the same pair `ceiling.py` used (C9, C10), pointed at the new
reader. C10's falsification stands and is not redefined away: `--lines` really
does select whole **hunks**, which is a property of the tool and the reason away
from `-U0` it over-stages every case probed.
