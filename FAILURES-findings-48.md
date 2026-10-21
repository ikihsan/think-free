<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# Findings — failures and negative results, part 48

This file holds **F149, F150** (session `2026-10-20-001`, E202) and **F151**
(session `2026-10-21-001`). Continued from
[`FAILURES-findings-47.md`](FAILURES-findings-47.md) (F147–F148). See
[`FAILURES.md`](FAILURES.md) for the index.

---

## F149 — the deterministic line-anchor rewrite works and is dominated by the CSS route

**Date:** 2026-10-20. **Experiment:** [E202](EXPERIMENTS/202-line-anchor-rewrite/RESULT.md).
**Question.** E162 closed the deterministic *repairer* (0 of 125 eliminated,
because the nodes carry no author-written string). The remaining class is the
machine-generated empty self-link `<a id="__codelineno-N-M" name="…"
href="#…"></a>` that `pymdownx.highlight` emits with `anchor_linenums` on. Can
that class be eliminated by a deterministic, invention-free *rewrite* of the
anchor element that keeps its line-permalink target?

**What was measured.** A targeted `topic:mkdocs` harvest (fixed selection rule,
no replacement after any number was seen): 98 fetched records / 85 distinct
files, 79 HTTP-200 records / 73 files. **3 pages / 3 hosts qualify** (contain
`__codelineno` or `anchor_linenums`). On those three pages, axe-core 4.14.0 in
jsdom, four arms: 0 control, 1 the rewrite, 2 the upstream CSS mitigation, 3 the
`anchor_linenums: false` route simulated by deletion.

**The result.**

| gate | declared | result |
|---|---|---|
| G1 elimination | ≥ 90% of AA-tagged empty-self-link instances removed | **PASS — 83/83 = 1.0** (kill < 0.60 not fired) |
| G2 no fabrication | 0 added strings | **PASS — 0** |
| G3 no regression | no new rule id, no AA increase | **PASS** |
| G5 target survival | 100% of rewritten targets resolvable | **PASS — 260/260** |
| baseline dominance | if arm 2 removes as much as arm 1, arm 1 is dominated | **FIRES — arm 2 removes 83/83** |
| G4 population | ≥ 12 pages / ≥ 6 hosts | **FAIL — 3 / 3** |
| D demand | ≥ 3 independent public reports captured | **PASS — 3 of 3** |

**The kill gate did not fire; the route still closes.** Arm 2
(`a[id^="__codelineno"],a[name^="__codelineno"],a[href=""]{visibility:hidden}`)
removes exactly the same class, changes nothing in the DOM, loses no target and
needs no migration. The protocol declared this outcome in advance: *if arm 2
removes as much of the class as arm 1, arm 1 is dominated and the answer is a
negative one about the rewrite, whatever G1 says.* Arm 1's only claim to
preference is that it works where the stylesheet is not shipped (a raw HTML
export, a pasted fragment) — a scope statement, not a score. Arm 3 destroys all
**260** targets, which is the price of the configuration route.

**The population finding matters more than the mechanism.** A fresh
`topic:mkdocs` harvest puts the pattern on **3 of 65 HTTP-200 pages (4.6%)**,
against E162's **90 of 125 (72.0%)** instances on 27 pages selected for fame and
defect density. So E162's "every accessibility score in circulation is computed
on a denominator that is mostly plumbing" is a property of *its* corpus, not of
mkdocs sites. The two numbers are not the same quantity (pages vs instances), and
neither is a web prevalence estimate; both are recorded with their populations.

**Prior art and demand.** GitHub repository search for `codelineno` returns
**0 repositories** — no post-hoc rewriter or stripper exists. The CSS remedy is
shipped by many projects (`cloudfoundry/docs-bosh`, `syn54x/ferro-orm`,
`zensical/docs`, `radiusred/codecrew-www`); `__codelineno remove` returns **53**
manual-fix issues. Three independent public reports naming the class were
captured (`radiusred/codecrew-www#57` empty line-anchor tab stops,
`coleam00/mcp-crawl4ai-rag#5` noisy anchors in crawled Markdown,
`gpt-cmdr/ras-commander#462` duplicate line IDs — the last a related-not-identical
complaint).

**What is decided.** The rewrite route closes as **dominated**. The remedy is
build configuration (`anchor_linenums: false`, or the CSS rule, or authored text
inside the anchor), which prior art already ships. **No candidate is proposed.**
E162 is not falsified: the deterministic *repairer* still eliminates nothing,
because the nodes carry no author-written string (F148); E202 adds that the
*class* is common only where the highlighter's option is on.

**Instrument defects, declared.** `fetch2.js` overwrote its own output files (13
files carry two records, 6 with differing `sha256`); AMENDMENT-2's census
sentence mislabelled the collision as fetch failures; the merge rule's
"different outcomes" clause was ambiguous and was resolved to "the retry
supersedes the timeout" before the verdict, with the literal reading reported
beside it; `pages/054-…html` got one axe attempt instead of two. None affects an
arm measurement; all are bounded by the census. See
[`AMENDMENT-3.md`](EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-3.md).

---

## F150 — `origin id next D` is fooled by a product-and-service code, and reports D305

**Date:** 2026-10-20. **Where:** `tools/originlib/idalloc.py`, `_numbers()`.
**Symptom.** `tools/origin id next D` printed `D305`, described as
"highest D304". The highest real decision in the repository is **D126**.

**Mechanism.** For kind `D`, `_numbers()` reads every `DECISIONS*.md` file and
counts every `D\d{3}` token in a table row (`NUMBERED_CELL`), not only the row's
identifier cell. `DECISIONS.md`'s D123 row quotes the federal product-and-service
code **`D304`** (telecommunications, $20.37B) as subject matter, so **304**
enters the decision set and the allocator hands out **D305**. The docstring
already records the same defect on the F side — defect 26, the bike serial
`SNACEOSF18391` read as finding 183, skipping 83 numbers — and the `\b` boundary
was the repair there; it does not reach a data value inside a cell's prose.

**Why it matters.** A session that allocates its decision id from the tool's
answer would open a **178-number gap** (D127–D304 unused) and, worse, would
place its decision out of sequence with every existing one. This session nearly
did exactly that while recording E202's route closure, and cross-checked by
listing the `## Dnnn` headings instead.

**Rule.** A table row's identifier is the **id cell**, not every number the
row's prose happens to contain; and an allocator that has once been fooled by
subject matter must be cross-checked by the session that trusts it, because it
reports a confident number. The repair is in `idalloc._numbers` and needs a test
that a `D\d{3}` inside a cell's prose is not counted; **not done here** — it is
a tooling change owned by a different task than the experiment.

---

## Identifier note carried by this session

The E202 experiment directory was built at `EXPERIMENTS/200-line-anchor-rewrite/`
and renumbered to **202** because `STATE-next-actions.md` (a pushed record)
names "E200 (size-screen: …)" as a completed money-axis screen. The unpushed
side yields under the standing renumbering rule (F133, F146); the recorded
command paths (`commands.log` seq 4–20) refer to the pre-rename location. The
referenced money-axis E199–E201 has **no committed experiment directory in any
fetched ref**, and the committed `EXPERIMENTS/199-…` is a different experiment
(a PyPI view-count matched harvest); the claim is marked unverified in
`STATE-next-actions.md` rather than deleted, because the work may exist on
another VM.

---

## F151 — the suite's negation fixture pins a git exit code this VM's git no longer shows, and nothing in the tree changed

**Date:** 2026-10-21. **Session:** `2026-10-21-001`. **No experiment** — a
verification run during a landing, recorded so the red gate is not misattributed.

**Question.** Does the full suite pass on the tree this session is landing?

**What was measured (observed, captured through `tools/x`).** `env
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests` →
**Ran 849 tests in 1306.120s, FAILED (failures=1)**, exit 1. The single failure
is `test_the_naive_exit_code_rule_would_be_wrong` in
`tests/test_check_ignore_negation.py`, whose own assertion message already says
it: *"git no longer exits 0 for a negated path, so this fixture no longer
demonstrates the defect and the test above is proving less than it claims."*

**Isolated probe (observed).** In a throwaway repository containing `*.json`
then `!a.json`, on this host (`instance-20260717-0944`, `git version 2.50.1`):
`git check-ignore --quiet -- a.json` on the negated path exits **1**, and a
genuinely ignored path exits **0**. So the failing assertion is about git's own
semantics, not about this repository's `.gitignore` (the landing's `.gitignore`
change adds one E202 `pages/` rule and cannot reach
`EXPERIMENTS/000-capability/raw/capture.json`). The three assertions the test
exists to protect all pass: `is_ignored` reads negated → not ignored, ignored →
ignored, unmatched → not ignored.

**Provenance (untested).** The test was committed 2026-10-19 (`0bdfdd86`); no
captured green run of it exists in this record. `tests/git-versions.json` names
2.25.1, 2.55.0 and 2.56.0 and lists **2.26–2.54 as never run**, and `doctor`
reports 2.50.1 here as *unrecorded* — today's run is the first captured full
suite inside that range. Whether git ever exited 0 for a negated path, on which
version, and whether this host was ever green with this test, are **untested**.
The same session corrected STATE.md's reload-point claim that this VM runs
`git` 2.25.1 (observed: 2.50.1).

**Why it is recorded, not fixed.** Two wrong repairs are visible from here:
weakening the assertion to buy a green gate, and blaming the landing commit,
which does not decide this behaviour. The honest repair — a fixture that states
the git version its premise was verified on and skips or inverts elsewhere — is
a tooling change with its own owner, not something to do inside a session that
was landing evidence (F018, F019's rule, one step further: the *premise*, not
just the environment record, has to be versioned).

**Rule.** A fixture that pins another tool's exit code states the version it was
verified on; a gate whose premise depends on the host's toolchain is only as
green as the record of that toolchain.

---

## F152 — "fragmented ⇒ a small program can enter" was an inference, and on NIH SBIR segments it is unsupported: the kill gate fired and fragmentation turned out to be a size proxy

**Date:** 2026-10-21. **Experiment:** [E208](EXPERIMENTS/E208-sbir-entrant-share/RESULT.md).
**Question (predeclared).** Across NIH SBIR R41/R42 spending categories, is
fragmentation (1 − top-5 award-amount share) associated with the fraction of a
category's FY2023 awardees that are newcomers to that segment (no award in the
category in FY2018–FY2022)?

**What was measured.** Complete R41/R42 census FY2014–FY2023 (every year
fetched = the API's `meta.total`; 3,407 rows), identity
`organization.external_org_id` (100% coverage), analysis population the 64
categories with ≥ 10 distinct FY2023 organizations. Instrument gates G0–G2 all
PASS: the fetch reproduces E207 exactly (368 rows, 147 cat-101 grants, 134
orgs, top-5 0.1159).

**The result.** **G3 (the declared kill gate) FAILS: Spearman ρ = −0.2456**
(one-sided permutation p = 0.9754, 10,000 permutations, seed 20261021) against
a declared ρ ≥ +0.40 and p < 0.05 — the association runs **slightly the wrong
way**, and the nine-year sensitivity window agrees (ρ = −0.2748). G4 passes
(cat 101 segment-entrant fraction 0.5075 ≥ 0.30), so the headline category is
enterable; it is simply not *more* enterable than the rest.

**Why the sign is what it is (exploratory, post-hoc, labeled as such).**
**ρ(fragmentation, category size) = 0.9711**: in this population "fragmented"
is almost perfectly redundant with "many awardees". And larger categories have
*fewer* newcomers proportionally (ρ = −0.2583; smaller half 0.604 vs larger
half 0.503), so the negative headline ρ is size, not entry behaviour.

**What survives the closure.** Entry itself is common and was never in doubt
after measurement: **0.527** of the 2,106 category-organization memberships in
FY2023 are segment newcomers, **0.407** domain newcomers, median category
0.538, three categories at 1.0. The accessibility screen measures
concentration; read as an *entry* signal it would be reporting category size.

**Scope.** This closes the entry-by-fragmentation claim for NIH SBIR R41/R42
FY2014–FY2023 only. The federal IT codes (E196–E198), where the pattern was
first claimed, are **untested** on entry; a negative here does not close them.

**Rule: a screen's axis is a candidate explanation only after its correlation
with the obvious confound is measured.** Fragmentation was reported for five
experiments before anyone asked what it correlated with; the answer is 0.97
with category size, and it costs one fetch to find out. See
[`FAILURES.md`](FAILURES.md) F152, [D129].
