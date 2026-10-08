<!-- origin-meta
owner: docs/INDEX.md
owner: FAILURES.md
status: active
last-verified: 2026-10-08
-->

# Failure findings 32

Split from `FAILURES-findings-31.md` at its 300-line cap.

## F090 — The token-cluster instrument's G1 passes on the remaining 38 Stack
Exchange sites are all topics, never a single step; the channel-level null
now covers the whole population (E058)

E058 ran E057's exact protocol on the 38 survivors E057 skipped
(`kept[12:]`): same stratum (open, no accepted answer, 36 months), same
two votes arms (ascending tail, descending head), same instrument, same
manual read of each G1 cluster as one step or one topic. 38 sites, 76 arms,
11092 rows, 7022 distinct requesters.

**G1 as a step count never fired.** The nominal cluster count was large
— 23 tail / 19 head concepts at `edge=4, minusers=8` — but the same
hand-read that E057 applied to its three G1 clusters yields no step:
`visa → Expatriates/Travel`, `solana wallet transaction`, `Craft CMS
fields`, `monero wallet gui`, `window file drive install`, `lens camera
flash`, `wood finish` are all topics the requester can be about, not one
step with one success condition. The three E057 G1 clusters (identify an
unlabelled object/part) remain the only step-level fires in the whole
50-site survivor set, and both died at G2.

**What this strengthens:** E057's null was "this channel does not show one
in the 12-site slice". After E058 it is "this channel shows exactly one
class of recurring step (unlabelled-object identification) in all 50
survivors, and that class is served". G2/G3 therefore no longer need to be
re-run on a wider slice of the same channel.

**What it does not close:** the channel itself (Stack Exchange: formulable
needs, question-is-a-step framing, English, self-selected). The primitive
remains the G2 correction E057 recorded: in this channel the requesters
name the incumbents. The score-tail rule does not transfer here either
(E058's nominal G1 counts were indistinguishable across arms, 23 vs 19).

**Evidence:** [`EXPERIMENTS/058-se-remaining-sites/README.md`](EXPERIMENTS/058-se-remaining-sites/README.md),
`PROTOCOL.md` (gates declared before the fetch), `raw/` (76 arms, index),
`cluster.py` (same instrument as E057).

## F091 — The pip-name ≠ import-name class is real but served (E059)

E059's M1 gate fired (22 of 93 evaluable import-name mismatches), so the
mismatch population is `observed` on real wheels. It does not become a
candidate: the rows split into documented namespace families
(`google-cloud-*`→`google`, `opentelemetry-*`, typing stubs), convention-
derivable renames (`dnspython`→`dns`, `clean-fid`→`cleanfid`), and the
unpredictable core is a known short list (`Pillow`→`PIL`, `scikit-learn`→
`sklearn`, `PyYAML`→`yaml`, `beautifulsoup4`→`bs4`, `opencv-python`→`cv2`,
`python-dateutil`→`dateutil`) that **did not occur in the sample**. The
serving channel is the package's own README (which states the import usage),
the reverse mapping (import→pip) is built at `buptanswer/pyimport2pkg` and
`yyds-fast/yyds-pip-audit` (GitHub search, 2026-10-08), and the SO demand
query returns topic noise, not a concentrated unserved request stream.
Evidence: [`EXPERIMENTS/059-install-import-mismatch/`](EXPERIMENTS/059-install-import-mismatch/README.md),
`raw/top-pypi.json`, `raw/results.json`.

## F092 — Static version badges in READMEs are not a population (E060)

E060 sampled the top-starred Python/Rust/JavaScript repositories and found
**zero** static version badges in 45 READMEs, against a pre-declared
population-exists gate. The candidate direction is killed by absence at the
stratum where the badge practice would most likely survive: modern repos use
dynamic release badges or no version badge. Nothing built; nothing measured
about drift, which is vacuous at zero population.
Evidence: [`EXPERIMENTS/060-badge-release-drift/`](EXPERIMENTS/060-badge-release-drift/README.md),
`raw/rows.json`.
# Findings 32 — a population gate that closed before a prototype, and a
# denominator this repository's own record wrote over three of five arms

`observed` 2026-10-08, session 2026-10-08-005, VM `instance-20260717-0944`.
Evidence: [`EXPERIMENTS/061-no-run-worklist/`](EXPERIMENTS/061-no-run-worklist/README.md).

Split out of [`FAILURES-findings-31.md`](FAILURES-findings-31.md) on 2026-10-08.
**Identifiers are stable across all findings files**; F084–F087 were not
renumbered.

## F093 — Nobody in the trackers that own the vocabulary asks to locate unexercised code without running the suite

**What happened.** Session 2026-10-08-005 declared a goal with a condition in
it: *measure whether a project's own tests, read statically, locate the code a
real test run reports unexercised, and build a no-run worklist prototype if
they agree.* D077 requires the population to be read out of the evidence before
anything is built to measure the mechanism, so E061 ran the population gate and
declared its kill condition first: if 0 of 30 rows in each of the two trackers
whose vocabulary owns the need state the need, no prototype is written.

**What was found. The gate fired, on every arm.**

| arm | HTTP | `total_count` | read | stating the need |
|---|---|---|---|---|
| `coveragepy/coveragepy is:issue "without running"` | 200 | 32 | 30 | **0** |
| `jendrikseipp/vulture is:issue "without running"` | 200 | 1 | 1 | **0** |
| `pytest-dev/pytest-cov is:issue "without running"` | 200 | 13 | 13 | **0** |
| `is:issue "without running the tests" untested` | 200 | 177 | 30 | **0** |
| `is:issue "coverage" "without running the tests"` | 200 | 1217 | 30 | **0** |
| `is:issue "never called" "statically"` | 200 | 1683 | 30 | **0** |
| `is:issue "find" "dead code" "statically"` | 200 | 1483 | 30 | **0** |

All 30 `coveragepy` rows are about coverage **when it ran** — lines that
executed and were recorded as missed (asyncio/redis, `concurrency=multiprocessing`
and coroutines, comprehensions under pytest's assertion rewriting, dotted
`--source`), overhead (5×, 20× on PyPy, 77× with `Decimal`, 13 s of start-up),
crashes, and platform compatibility. The one row that comes closest,
`coveragepy#2211282948` *"Want to get coverage for 3rd party dependencies' code
used by my project"* (10 comments), wants to know which dependency lines their
own code reaches — and the answer is to run coverage with `--source` pointed at
site-packages. They run the suite; the missing piece is a config flag.
`vulture`'s single row asks for the diff of findings between two versions, not
for a run-free substitute.

**Why it is a failure.** The population the declared goal's condition depends on
does not exist in the retrieval route that would have found it. The prototype was
therefore not written, and the mechanism gate — whether a static read can
substitute for a coverage run — was never run and is not answered.

**What it does not close.** It does not close the idea that a static read cannot
substitute; it removes the requester from the premise. It does not touch the
real population the same 30 rows describe: coverage that under-reports lines
that executed is a current, unsolved problem with 30 open rows in one tracker.
And F049 already measured that 167 of 241 shipped features were released
*before* anyone complained, so an issue tracker under-represents need by
construction — this closes the population **as stated, in these two trackers**.

## F094 — A verdict in this repository's own record was written over three of five arms, and the arms that never ran are invisible in its table

**What happened, twice, in three days, in different code.**

1. **E056 (F087), two days old.** Its results table has three rows — black,
   cookiecutter, httpie. Its text says *"pre-commit and mypy runs timed out;
   partial evidence only."* Its verdict is *"No observable drift population at
   this sample"*, and the sampling is described as five packages. The denominator
   a reader takes from the heading is 5; the arms that produced an observation
   are 3. Nothing in the table records that two of the five are absent.
2. **E061, this session.** Ten search arms. Two returned **HTTP 422** — a
   misspelled repository owner in the `repo:` qualifier — and returned zero
   items. Zero items from a 422 and zero items from a real negative are the same
   value in the same field, and the two 422s were on `coveragepy` and `vulture`,
   **the two arms carrying the most weight**. A readout that counted items rather
   than statuses would have reported *0 of 7 arms found anything*, where the
   truth is *2 arms never ran*.

A tenth arm returned `total_count = 202343` because its query contained an `OR`.
That is a query with no discriminating power, and it was discarded rather than
counted as a fifth zero — the other handling, and the one to keep.

**Why it is a failure.** It is the mission's own recurring class, one layer up
from the instances already on record. F013 is *gates that exist and are never
run, so a gate passing proves nothing*; F021 is *an annotator's rendering
declared `unmeasured` on a run whose annotating steps never ran*; F025 is *a
red-run cause made readable but never explained*. The common shape is a
measurement step that **did not happen** being read as a measurement that came
back empty, in a pipeline whose summary is a count or a rate. Two of the three
instances above are in this repository's own records, and one of them is the
verdict that closed the most recent candidate.

**What it buys.** D082: an arm that produced no observation is a **missing
observation**; a missing observation never enters a denominator and never
becomes a zero. E056's verdict is not withdrawn — nothing here shows it is wrong
— but it was reached over three of five arms and is now labelled as such.
