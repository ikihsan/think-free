<!-- origin-meta
owner: docs/INDEX.md
owner: FAILURES.md
status: active
last-verified: 2026-10-09
-->

# Failure findings 35

Split from [`FAILURES-findings-34.md`](FAILURES-findings-34.md) on 2026-10-09.

## F102 — Two sessions on different VMs allocated F093 to two different findings, and the finding index could not tell (2026-10-09)

Session `2026-10-09-003`, found by `doc lint` while landing F101.

`FAILURES.md` indexed **F093 on two lines**, each a complete and unrelated
finding: E061's no-run-worklist population (defined as `## F093` in
[`FAILURES-findings-32.md`](FAILURES-findings-32.md), and cited as F093 by
`STATE.md`, `EXPERIMENTS/061-no-run-worklist/README.md` and
`EXPERIMENTS/061-supplement-drug-adulteration/README.md`) and E065's finding
that web search cannot operationalize `view_count`. Both were allocated the same
identifier on different VMs, and the collision gate correctly refused the
landing.

**Why it matters more than a bookkeeping fix.** A finding identifier is what a
later session cites to check whether a claim was already falsified. Two findings
sharing one identifier means a reader asking "has F093 been answered?" cannot
tell which question is being answered, and the collision is invisible in a diff
because each row was written by a different session against a different base.
This is the class the mission has already recorded as defect 21 (a colliding
identifier must be refused before publication) — **the refusal worked, and this
is the first time it caught two independently-allocated identifiers rather than
a duplicate re-definition.**

**The repair.** The earlier allocation is kept, since it is the one with a body
file and four inbound citations. The later row was renumbered to **F102**, the
next free identifier, with the renumbering stated in the row itself so a reader
who saw the old number can trace it. No finding text was changed.

**Ceiling.** The lint reports collisions and undefined/absent identifiers; it
does not detect two sessions that each allocated the same *new* identifier and
were both merged before the gate ran — which is exactly what happened here and
what the gate then caught. Nothing here says the numbering scheme is sound; it
says one collision was found and repaired.

## F101 — A predeclared install gate whose only reachable successes are empty files cannot fail, and the tool computing it reported the pass as a verdict (E069)

Session `2026-10-09-003`, VM `instance-20260717-0947`.

**What was run.** E069 tested E068's spec generator the way E068's own README
named as its most useful next action — by installing the generated file. Three
arms per repository (`GEN` the generated spec exactly as committed, `DECL` the
spec the repository already ships, `NONE` nothing installed), one fresh Python
3.10.19 virtualenv per arm, 16 of the 20 repositories before the VM reached 95%
disk. Both oracle controls passed first: P2 (a fixture importing one real pinned
dependency) and P1 (the A1 repositories whose own pinned specs are known-good,
2 of the 2 pip-declarable ones).

**What was found.** `GEN` installs cleanly in 3 of 16 — and all three are
repositories that import nothing. Two of the three generated files are **empty**;
the third is the single line `temperature==2.7`, a 213 KB package unrelated to
anything the repository imports. **Verified imports: 0 of 16.** The 13 that pip
refused could not install at all.

**The gate could not fail, and the protocol said so in advance.** K1 asks for 3
clean installs out of 20, so it **passes**, and `analyze.py` labelled the run
`mechanism holds`. `PROTOCOL.md` Amendment 1 predicted exactly this before any
arm ran: *"K1 can therefore be met only by a specification that installs
nothing."* The confirmation was cheap and decisive: one additional repository
was measured **precisely because the static arm showed it carried no blocking
pin** — `google-research/google-research`, whose generated spec is an empty file
— and that single measurement moved the label from `KILL` to `mechanism holds`.
A gate whose only reachable successes are empty files cannot distinguish an
artifact that installs nothing from an artifact that installs everything
correctly. F010's shape again, on an install test rather than a timestamp field.

**The direction closes on K3**, the one gate independent of the artifact: on 4
of 16 repositories the repository's own declared file installs while the
generated one does not, 2 of them (`ambroiseodt/tssim`,
`FARAZLOTFI/underwater-object-tracking`) reaching a fully working environment
and 2 installing but then missing one module their own spec names
(`imutils`, `tensorboardx`). So on every repository where anything was tested
the generated spec is **0 for 0** against the incumbent, and strictly worse on 4.

**The shortfall does not leave the gates open.** All 4 unmeasured repositories
carry at least one pin the static arm shows pip refuses, so `GEN` cannot install
on any of them; `results.json` reports `gates_determined: true`. What the
shortfall does cost is `DECL` coverage on those 4, so K3's 4 rows are a floor.

**Six instrumentation defects, all recorded in the experiment's README.** The
first two were found by the controls; the rest by reading the write-up against
the bytes it cites — which is the check controls cannot do:

1. `analyze.py` **could not have produced this verdict at all.** It read
   `raw_results.json`, written once at the end of a whole run, so mid-run it
   described the pilot's single repository; and it read a `controls.json` that
   no run writes, so `oracle_valid` was `None` and the arms would have been
   interpreted without the controls that license interpreting them.
2. `installed` **counted an untested environment as a success**, combining "every
   probed module imported" with "there was nothing to probe". That is how three
   empty specs satisfied K1 and K2.
3. A **pip timeout was charged to the mechanism** as a failed install:
   `harness.run()` returns exit `None` past `E069_PIP_TIMEOUT`, and `exit != 0`
   scored it a refusal.
4. The README's **own headline did not reproduce** — 15 repositories measured
   reported as 20.
5. Its **near-miss count did not reproduce**: "149 of 383" is produced by no
   rule over the committed metadata (the nearest variants give 126, 132 and
   150). The computed figure is **132 of 383 (34.5%)**, now computed in
   `pin_compatibility.py` with the 20 KB threshold in the script.
6. `doc lint` **hung for 9 minutes** walking 3.6 GB of un-gitignored third-party
   checkouts under `EXPERIMENTS/068-arxiv-spec-generator/repos/`, including a
   510 MB model checkpoint. Fixed under the repository's existing fetched-bytes
   clause; the record is `repos/MANIFEST.json`'s commit shas.

**What it buys, and what it does not.** E068's direction is closed **as
implemented**. This does not disprove that an environment can be inferred from a
repository, and it says nothing about adoption: 16 repositories, one arXiv year,
all deep-learning GitHub code, Python 3.10 only, no GPU. The oracle as amended
cannot catch a spec that *omits* a needed dependency — it probes what the spec
claimed, not what the code wants. The generalisable rule is D088: enumerate what
a kill gate's passing value can actually be made of, before the run.

## F103 — pip's "did you mean" name guard gap is too large across ecosystems (E070)

Session `2026-10-09-001`, VM `instance-20260717-0944`.

**What was run.** E070 tested the claim that pip's `pip install --dry-run` "did you mean" / typo-protection warning adequately protects users from confusingly similar package names. Two ecosystems were tested: PyPI (50 near-miss names from E064's mutated name set) and Crates.io (50 near-miss names).

**What was found.** 0 of 50 PyPI names and 0 of 50 Crates.io names received a "did you mean" warning from pip. The gap fraction is 1.0 (100%) in both ecosystems, with Wilson CI95 [0.929, 1.000]. Kill gate G3 FAILs because the lower CI bound (0.929) exceeds the 0.15 threshold — the claim that pip's warning adequately protects users is not supported by the evidence.

**The gate could not save the candidate, and the protocol said so in advance.** G3 was designed with non-vacuous passing and failing regions (gap fraction ≤ 0.05 → PASS; ≥ 0.15 → FAIL; otherwise inconclusive). The gate properly enumerated its reachable set before the run (the set of names pip would/would not warn about, determinable from `--dry-run` output). The E069 lesson — that a gate whose only passing region consists of vacuous cases cannot fail — was avoided by designing G3 with both a tight passing region and a loose failing region. Both regions were realized: the gap was measured at 1.0, well into the failing region.

**The shortfall does not leave the claim standing.** The gap fraction of 1.0 means pip's "did you mean" warning provides zero protection against confusingly similar package names in either ecosystem. This closes the claim that pip's guard adequately protects users. The generalisable rule is D089: a kill gate whose passing region contains only vacuous cases cannot fail; enumerate the gate's reachable set before the run, and design both passing and failing regions that are non-vacuous for the gate to be informative.

**What it buys, and what it does not.** This finding closes the claim that pip's "did you mean" warning protects users from name confusion. It does not measure whether downloaded packages are malicious, whether they serve the user's actual need, or whether adoption would change. The generalisable rule survives: E069's lesson generalizes — gates must enumerate their reachable sets, and both passing and failing regions must be non-vacuous for the gate to be informative.