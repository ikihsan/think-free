<!-- origin-meta
owner: DECISIONS.md
status: active
last-verified: 2026-10-10
-->

# DECISIONS-SCREENING-17

Decisions **D093, D094**. Each entry records a choice that was genuinely
open, the options considered, and what was decided.

## D093 — A rate computed against an instrument's own false positives is an upper bound, and a gate that reads it as a rate will build on artifact (2026-10-10)

**The situation.** E085's protocol declared four gates. G1 (instrument
ceiling) and G2 (control validity, 10 positive and 10 negative controls) both
passed. G3, the rate, returned 6 of 500 imported modules = **0.0120**, Wilson
CI95 [0.0055, 0.0259] — above the declared 0.005 kill line, below the 0.020
build line, with the interval spanning both. The declared verdict was `HOLD`.

G4, declared before the run, was a precision gate: at least 16 of 20
hand-read flagged pairs must be true. Only 6 rows existed, so all 6 were read.
**Three were true and three were not**, precision 0.50 against a declared 0.80.

**The choice.** G3 said HOLD and G4 said FAIL. Two readings were available:

1. Take G3's point estimate, treat HOLD as "not yet a kill", and build the
   checker on 0.012 — the class is present, the direction is alive, and the
   line continues.
2. Treat G4 as bounding G3. Half the numerator was this experiment's own
   artifact, so the corrected rate is 3 of 500 = **0.006**, at the kill line
   rather than above the build line.

**The decision is (2).** The line closes on the corrected rate, and the
prototype is not built as a linter.

**Why this is a rule and not a preference.** The protocol had already declared
that `S_strict` was the **lower bound** and that `undecidable-sdist-only`
would never be folded into the target class — and G4 exists for one stated
reason: *deptry's own lesson (D090) is that a precision figure computed against
a positives-only label set is not a precision figure.* Building on 0.012 would
have meant reading a number as a rate when the protocol had already recorded it
as an upper bound, and would have inverted the one gate written specifically to
catch that.

**What this does not say.** It does not say the class is absent. It was
reproduced end-to-end by hand on this VM: `pip install Crypto` exits 0,
installs a different project plus eight of its dependencies, reports
`Successfully installed Crypto-1.4.1` so `pip list` shows the name satisfied,
and `import Crypto` then raises `ModuleNotFoundError`. It does not say deptry's
blind spot is not real — deptry 0.25.1 returns **0 findings** on a project that
declares `sklearn` and imports it, and never names a provider in any condition
tested. It says the class is real, measurable, and **too rare at ~0.6% of
imported modules to justify a CI gate**, so the incumbent's blind spot costs
little in aggregate.

**The generalisable rule, and it costs nothing to follow.** Every rate this
mission computes is a rate *as this mission's instrument classifies it*. When
a precision gate exists, the honest reading is the interval between the
uncorrected and corrected figures, and the decision belongs at the corrected
one. A protocol that declares a precision gate and then builds on the
uncorrected rate has not used its own gate.

## D094 — An instrument's reachable set includes the shapes it cannot see, and they are named before they are counted (2026-10-10)

**The situation.** E085's resolver answers "which modules does this
distribution provide" by reading a wheel's zip **central directory** over HTTP
`Range`, with nothing downloaded and nothing installed. It resolved 578 real
declared distributions at 0.931 coverage and recovered the true provider for
10 of 10 controls.

Hand-reading its six findings turned up a class the mechanism cannot see by
construction: **`pynvml` 13.0.1 ships no `pynvml` module at all.** It ships
`_pynvml_redirector.pth` and `_pynvml_redirector.py`, and the `.pth` executes
at interpreter startup and injects the module. `import pynvml` **works**, and
prints a deprecation warning. The central directory is a complete list of what
is *in the archive*; a `.pth` makes something importable with nothing in the
archive.

**The choice.** Either report `pynvml` as a shadow name and let the runtime
disagree, or widen the instrument to also read `.pth` entries. Widening was
rejected for this experiment and the limit is named instead.

**The decision.** The instrument ships with the limit named in
`pyprovides/README.md` and `provides.py`, and the hand-read is reported as
three-of-six rather than smoothed.

**Why this is a rule and not a note.** E085 also found four further defects in
its own instrumentation, and two of them **moved the verdict**: a stdlib
detector that missed every standard-library *package* (6 findings became 12),
and a lookup that resolved module names only among declared distributions,
which suppressed the target class by construction. D088 says a gate whose
passing region cannot be reached cannot fail. The same shape applies to an
instrument: **a measurement whose reachable set omits a shape it cannot
detect will report that shape as a finding.** The correction is to enumerate
the instrument's reachable set — including what it structurally cannot see —
in the same document that declares its gates, so a reader can discount the
count rather than discover the discount later.

**The generalisable rule.** Before trusting a classifier's count, name the
inputs it structurally cannot represent — `.pth` redirects, dynamic imports,
project-local code, namespace shims — and decide where they go *before* the
run. E085 got the stdlib and project-local cases wrong and only found out by
reading output; both amendments that fixed them were cheap, and one of them
was cheap only because the raw rows were still there to read.