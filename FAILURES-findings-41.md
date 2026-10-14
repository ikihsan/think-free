<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# Findings — failures and negative results, part 41

Split out of [`FAILURES-findings-40.md`](FAILURES-findings-40.md), which held
F119–F124. See [`FAILURES.md`](FAILURES.md) for the index. **Identifiers are
stable across all findings files.**

## F125 — `preflight` returned a non-blocking `OK` on two paths that measured nothing, and the only way to find out was to point it at a real foreign run (E134)

**Date:** 2026-10-14. `EXPERIMENTS/134-preflight-real-run/`. Raw:
[`results_e134.json`](EXPERIMENTS/134-preflight-real-run/results_e134.json).

### What was asked

`preflight` is a stdlib-only package that measures three properties of an
evaluation instrument and **withholds a rate unless all three hold**. E124 built
it and validated it on five committed cases, all from this repository. E125 then
kept it internal after finding only two genuine key/output pairs among 22 popular
harnesses. E128–E133 re-opened it by writing adapters for four formats *this
repository had constructed itself*. **No run of a foreign harness had ever been
observed.** E134 ran one.

### What happened

Neither defect was found by reading the code. Both were found by running the
committed package on output bytes it had never seen, and reading the verdict.

**1. C1 reports `OK` when there is no key to join against.** On Arm A, a real run
of `EleutherAI/lm-evaluation-harness` v0.4.4 on `openbookqa`, the key side could
not be built at all — the run does not record which split it evaluated, and
`n-samples.original = 500` matches **both** the declared `validation` and
`test` splits, which hold 500 rows each. `concordance` returned
`verdict: OK`, `best_rate: 0.0`, `key_rows: 0`, `output_rows: 5`. The
`SILENT_NO_MATCH` branch is guarded on `key_rows_n and out_rows_n`, so with no key
rows the function falls through to the default. A tool whose purpose is to refuse
to report a rate against a check that saw nothing reported one.

**2. C2 reports `OK` on a flagger that flags nothing.** On Arm B, a third-party
published run, 200 rows were labelled correct by recomputing each verdict from the
run's own shipped `filtered_resps`, `target` and `doc_to_choice` — an independent
label, not the shipped `acc`. **Zero** rows were labelled incorrect. The
margin-abstention flagger at `tau = 0` flags nothing: `verdict: OK`, Wilson lower
bound `0.0000`, `recall_on_incorrect: None`. `alternate_form_fp` guards an empty
*correct* arm (`NO_LABELLED_CORRECT_ITEMS`) and had no guard for an empty
*incorrect* arm. Compounding it, `report.CLEAN` listed that "measured nothing"
verdict among the passes.

### Why this is the finding and not a bug ticket

F118's rule was that a verifier's control must include the case where the
subject is right and the form is different. This is the same rule one level
further out: **a verifier's positive arm is the arm the data cannot supply.** On
a real published run every row is right, so a flagger that abstains everywhere
scores a perfect pass on the only number the check reports. D109 already recorded
that a false-positive rate belongs to an arm rather than to an instrument; this is
the same fact about the *absence* of an arm, and it is the first time it has been
observed on a population the package would actually be sold for.

**Rule.** A check that cannot name a case it would condemn must not return a
clean verdict. "Measured nothing" is a withholding verdict, and the withholding
is the measurement.

### Repaired, and how it was falsified

`preflight/test_vacuous_passes.py`, 9 tests, four of which are the defect cases.
Falsified against the pre-fix code: **4 of 4 defect cases reported a
non-blocking `OK`; 0 of 4 do after the repair.** The repair is three places:
`concordance` returns `NO_KEY_ROWS` / `NOTHING_TO_COMPARE` before the
`SILENT_NO_MATCH` branch; `alternate_form_fp` returns
`NO_LABELLED_INCORRECT_ITEMS` when no arm holds an incorrect item; and
`report.CLEAN` is `("OK",)`. **Behaviour change, stated rather than absorbed:** a
C2 run with an empty *correct* arm now withholds where it used to pass. That is
E124's `test_no_labelled_correct_items_reports_that_it_measured_nothing`, which
asserted exit 0 "measured nothing, so nothing was condemned" — the reasoning
E134 disproves on real data. Its assertion is now exit 3, with the reason
recorded in the test.

### What this does not establish

That `preflight` is useful. E134's declared failure condition fired: Arm A is
clean under C1, R1 recomputation agrees with every printed rate on both arms, and
**lm-eval's plumbing is internally consistent on the rows it shipped.** The tool
found no defect in a foreign harness. It found two in itself.

## F126 — `recall_on_incorrect` computed its complement, so a flagger that caught every wrong item reported `recall 0.0` (E134)

**Date:** 2026-10-14. Same run, same check, found by writing the regression test
for F125's second arm.

`alternate_form_fp` reported
`"recall_on_incorrect": round(1.0 - incorrect["rate"], 4)` — the share of *wrong*
items the flagger **did not** condemn, under the name of the share it did. A
perfect flagger read `0.0`; a flagger that condemned nothing read `1.0`.

**It had not propagated.** E124's reported arms (0.0069 / 0.1970 / 0.6667 /
0.9346 / 1.0000) and E134's are all `correct_items` false-positive rates; nothing
in any record quotes this field, and E134's own runs returned `None` for it. The
number was wrong and unquoted, which is the smallest bad case available and still
a case: a field whose name states the opposite of what it computes is the same
defect as a check that cannot fail, one level in.

Repaired to `round(incorrect["rate"], 4)`, with the complement reported beside it
under its own name, `miss_rate_on_incorrect`. `preflight/test_vacuous_passes.py`
holds all four operating points (catches all / three quarters / half / one in
twenty) to the correct value, so the field cannot drift back to a complement that
happens to agree at 0.0.

## F127 — the repository's own gate was red on 467 violations while `STATE.md` recorded it as green, and four of the five causes were a class of document no rule can hold (E134)

**Date:** 2026-10-14, found while landing E134.

`tools/origin doc lint` exits 2 on 467 violations in the tree this session
inherited. `STATE.md` records `doc lint checks 1088 files and exits 0`. Both were
true of different trees; the second had stopped being true of the first, and no
gate had said so because the gate is the thing that was broken.

Five causes, all from commits landed in the preceding hours:

| # | cause | count | fix |
|---|---|---|---|
| 1 | 30 READMEs and 17 `git ls-tree` listings fetched verbatim from other people's repositories by E125. Their internal links and paths name *that* repository. | 402 | `doclint.check_meta` and the link rule now skip files `vendor/MANIFEST.md` declares exempt, as the cap and the orphan rule already did; globs declared with the reason |
| 2 | E065's synthetic bank extracts and E126's two grading sheets — machine-written data, never declared exempt | 51 | `exempt:` globs, each with a reason |
| 3 | E130's `PROTOCOL.md` and `CONTINUATION.md` had no title and no `origin-meta` | 4 | added |
| 4 | five `RESULT.md` files linked `PRIOR-ART.md`, `PROTOCOL.md` and `test_adapter.py` — **files named and never written** | 6 | links replaced by the plain name, each with a sentence saying the file does not exist and where the search that was actually run is recorded |
| 5 | two VMs allocated **D046** from the same base against two unrelated decisions and both landed | 1 | the one with no cross-references is renumbered **D110** in a new `DECISIONS-RECORDS-2.md` |

Cause 1 is the one worth keeping. **A link rule for this repository cannot hold a
third party's README, and the only way to make it hold one is to rewrite upstream
bytes** — which is the reason the evidence copy exists. The repair is not to
weaken the rule: the rule is unchanged for every authored document, and the
exemption is a declared glob covering one class, with the reason written down
beside it. Cause 4 is the one worth not excusing: five documents claimed a
prior-art check they do not contain, and a prior-art check is the obligation
`prior-art-check` exists for.

**Rule.** A gate that has been red since the last land will not announce itself.
The claim "the gates are green" is a measurement with a date on it, and the date
has to be the tree it was measured on.

**Second, smaller, and in this session's own work.** The link rule's exemption
needed `globs` threaded into `check_links`, which pushed `tools/originlib/doclint.py`
to 312 lines. The repair was the standing one: the rule moved to a new
`tools/originlib/doclint_links.py`, the seventh time that file has been split at
its cap, and `doclint._links` was renamed public (`doclint_links.links`) because
the control in `tests/test_link_escape.py` had been reaching into a private to
read the tree.
