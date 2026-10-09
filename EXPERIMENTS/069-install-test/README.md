<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# E069 — does E068's generated spec install?

**Verdict: the direction closes, and its own gate passes vacuously.** E068's
spec generator produces a specification pip can install in **3 of the 16
repositories measured** — and all three are repositories that import nothing:
two have an **empty** generated file and the third names the single unrelated
package `temperature==2.7`. **No repository in the population had its imports
verified against a generated spec: the verified count is 0 of 16.** The 13 that
pip refused could not install at all, and the 3 that did have nothing to probe.

This is worth stating plainly because the predeclared gate **passes**. K1 asks
for `GEN` to install cleanly in 3 of 20, and it does, so `analyze.py` labels
the run "mechanism holds". That label is an artifact of the gate's own wording,
and `PROTOCOL.md` Amendment 1 predicted it before the arms ran: *"K1 can
therefore be met only by a specification that installs nothing."* A gate that
can only be crossed by an empty file cannot fail, so it measures nothing. This
is F010's shape again — a declared gate shown not to be able to fail.

**16 of 20 repositories measured.** The run was stopped when the VM reached 95%
disk, the same exhaustion that stopped an earlier attempt. That shortfall does
not leave the gates open: **all 4 unmeasured repositories carry at least one
pin the static arm shows pip will refuse**, so `GEN` cannot install on any of
them and no further measurement can move K1 or K2. K3 can only gain rows, and it
already fails. `results.json` reports this as `gates_determined: true`.

Protocol: [`PROTOCOL.md`](PROTOCOL.md). Every number below regenerates from the
committed per-repository files in `raw/` via `analyze.py`, which writes
`results.json`.

## What was tested

E068 declared **4 of 4 kill gates passed** and "mechanism validated for
pip-based projects". Its own README lists the gap: *"No install test: gates
measure generation quality, not whether `pip install -r generated.txt` works."*

This experiment ran that test on bytes. Three arms per repository, one fresh
Python 3.10.19 virtualenv each:

| Arm | What it is | Why it is here |
|-----|-----------|----------------|
| `GEN` | E068's generated `requirements.txt`, exactly as committed | the mechanism |
| `DECL` | the spec the repository already ships | the incumbent, free to the user |
| `NONE` | nothing installed, source tree only | the floor |

**Oracle validity was established first.** P2 (a fixture importing one real
pinned dependency) passed. P1 — the A1 repositories whose own pinned specs are
known-good — reached "working" for `Profluent-Internships/MMDiff` and
`deeplearning-wisc/args` (2 of the 2 pip-declarable; the other two ship conda
only and are `not_exercised`, per D082 a missing observation and never a fail).
An oracle that recognises a working environment is required before it may judge
a broken one.

## Result

An arm is **verified** only when the install exited 0 *and* every third-party
module the repository imports actually imported. An install that exits 0 on a
repository with no third-party import is **unverified**: nothing was tested, so
it is not a success.

| Arm | Installs and imports verified | Installs, nothing to probe | Installs, import fails | Fails to install | Not exercised |
|-----|-------------------------------|----------------------------|------------------------|------------------|---------------|
| `GEN` | **0 of 16** | 3 | 0 | 13 | 0 |
| `DECL` | 2 of 16 | 0 | 2 | 3 | 9 |
| `NONE` | 0 | 16 | 0 | 0 | 0 |

The three `GEN` installs are `Goallow/Mini-Hes` and `google-research/
google-research`, whose generated specs are **empty files**, and
`EternityYW/Gemini-Commonsense-Evaluation`, whose spec is the single line
`temperature==2.7` — a 213 KB package unrelated to anything that repository
imports. `DECL` is `not_exercised` on 9 of 16 because those repositories ship
no dependency file at all, which is the E067 population finding seen from the
install side.

**Gates** (predeclared, unchanged; the strict column is this reading's own):

| Gate | Condition | Observed | | Strict |
|------|-----------|----------|---|--------|
| K1 mechanism works | `GEN` installs cleanly for ≥ 3 of 20 | 3 of 16 measured | PASS | **0 verified — FAIL** |
| K2 differentiation | `GEN` succeeds where `DECL` fails | 3 of 16 | PASS | **0 verified — FAIL** |
| K3 no harm | `GEN` does not fail where `DECL` installs | 4 repos | FAIL | FAIL |

**Both K1's and K2's passes are artifacts of the three empty repositories.** A
spec that names no package "installs" trivially and "beats" a repository that
ships no spec file by doing nothing. Against the incumbent, on every repository
where anything was actually tested, the generated spec is **0 for 0**.

**K3 fails on its own terms**, and it is the one gate that does not depend on
the empty-spec artifact: on 4 of 16 repositories the repository's own declared
file installs while the generated one fails to install outright. Two of those
four (`ambroiseodt/tsim`, `FARAZLOTFI/underwater-object-tracking`) reach a
fully working environment — every probed module imports — and two
(`cvblab/Mitosis-UTS`, `liujf69/EPP-Net-Action`) install but are then missing
exactly one module their own spec names (`imutils`, `tensorboardx`). The
generated spec fails all four. So the strictest count is **2 repositories the
incumbent runs and the candidate cannot install at all**, plus 2 more where the
incumbent is strictly further along. Either way the direction of the difference
is the same: a spec generator that breaks a repository that already worked is
worse than no tool, and that is measured behaviour rather than a reading.

So the direction closes on K3, and on the honest reading of K1 and K2. It does
not close because the premise was wrong: it closes because **pinning the newest
version of every name an import mentions is not a way to recover an
environment**, and because a generator that is wrong about which package an
import means cannot be repaired by pinning more carefully.

## Why: the resolver pins versions its own target rejects

E068 resolved every pin to the **latest stable version on PyPI**, ignoring
`requires-python`. Its protocol declares the target as **Python 3.10**.

Of 383 pins, 367 were decidable from the metadata E068 had already downloaded:

- **34 pins** (9.3% of decided) name a version whose every release file states
  a floor above 3.10 — `numpy==2.5.3` requires `>=3.12`, `scipy==1.18.1`
  requires `>=3.12`, `pandas==3.0.6` and `scikit_learn==1.9.1` require `>=3.11`.
- **24 pins** name a version PyPI lists with **no downloadable file at all**
  (every upload yanked or removed).
- **16 pins** carry a constraint string this parser does not decide, and are
  counted neither compatible nor blocking — so 58 blocking pins is a **floor**.

**17 of 20 generated specifications contain at least one such pin**, so they
cannot install. The three that can name 0, 0 and 1 packages.

pip's own verdict on the pilot repository agrees with the static arm:
`ERROR: Ignored the following versions that require a different python
version: 2.3.0 Requires-Python >=3.11; ...`, recorded as the `GEN` arm's
`first_failure` for `Itaymanes/K-QA`. The static arm's substitution for the
skipped installs is therefore checked against pip's own answer where both ran,
not assumed.

**A note on cost.** The install run was stopped at 16 of 20 with the VM at 95%
disk, on `JHW2000/JARNet`'s `DECL` arm — a single torch install there reached
9.3 GB. That is the same exhaustion that stopped an earlier attempt, and it is
why this experiment's honest denominator is 16 rather than 20. The shortfall
costs nothing at the gates, for the reason given above: all 4 unmeasured
repositories carry a blocking pin. What it does cost is `DECL` coverage on
those 4, so **K3's 4 rows are a floor, not a total**.

## The same defect, named: the existence bit

`temperature==2.7`, `modules==1.0.0`, `base==0.0.0`, `pytorch==1.0.2`,
`skimage==0.0`, `aligner==0.0.1`: **132 of the 383 pins (34.5%) name a project
whose pinned release's largest distribution file is under 20 KB.** These are not
the intended dependencies. They are unrelated projects that happen to share an
import's name — the near-miss population E064 measured at 16.15%, where
"resolves on PyPI" is exactly the wrong question. E068 resolved a name to a
version and recorded the resolution rate as **78.9%**; a rate that counts
`sklearn` as satisfied by a 3.8 KB placeholder measuring usefulness of nothing.

This count is computed by `pin_compatibility.py` (`near_miss_names`) from the
same cached metadata, with the 20 KB threshold written into the script so a
reader can disagree with the threshold rather than with an unstated judgement.
Size is a proxy for "not the library the code means", not proof of it.

## What this does not say

- **The idea is not disproved, this implementation is.** A resolver that honours
  `requires-python` and rejects yanks is a small change, and pip already does
  both when asked. Nothing here shows that an environment cannot be inferred
  from a repository; it shows that *pinning the newest version of every name* is
  not a way to do it.
- **E067's population finding is untouched.** 11.8% of arXiv computational papers
  with code links ship a machine-runnable spec. That is a real gap in what
  repositories provide. It is not evidence that a generator is wanted, and this
  experiment does not test adoption.
- **The failures are about the artifact, not the need.** 13 of 16 are a defect
  with a known cause and a known repair.
- 20 repositories, one arXiv year, all deep-learning code, all GitHub, of which
  16 were measured. No rate here generalises past that population.
- `DECL` is the strongest alternative available without inventing a mechanism.
  A colleague who reads the README and fixes the install by hand is not
  measured, and is this comparison's honest ceiling.
- Python 3.10 was chosen because E068 resolved for it. **On Python 3.12 the
  excluded pins stop being excluded** and the failure mode changes shape, though
  the name-collision population does not go away. Untested here.
- The oracle, as amended, **cannot catch a spec that omits a dependency the
  repository needs** — it probes what the spec claimed, not what the code wants.
  A generator that silently drops half a dependency could pass every arm here.

## Defects in this experiment's own harness, and in its own verdict

The first two were found by the controls; the rest were found by reading this
document against the bytes it cites, which is the check the controls cannot do.

1. **The oracle probed the wrong set.** It originally checked the modules a
   spec did *not* name, making "working" unsatisfiable by construction. Control
   P1 caught it: both A1 repositories installed with exit 0 and were reported
   not working. Corrected before any arm was interpreted, and recorded in
   `PROTOCOL.md` as an amendment with its reason.
2. **`shutil.rmtree(ignore_errors=True)` hid a removal failure.** 17 GB of torch
   wheels accumulated across 14 repositories; an earlier run was stopped at 88%
   disk with 6 of 20 repositories unmeasured. Removal now reports and refuses to
   measure the next arm without disk for it, and the harness resumes from
   per-repository files instead of re-downloading.
3. **`analyze.py` could not have produced this verdict at all.** It read
   `raw_results.json`, which `harness.py` writes once at the end of a whole run,
   so mid-run it described the pilot's single repository; and it read a
   `controls.json` that no run produces, so `oracle_valid` was `None` and the
   arms would have been interpreted without the controls that license
   interpreting them. It now reads the durable per-repository files and the two
   control files the control run actually writes, and treats a missing control
   as `not all_pass` rather than as a pass.
4. **`installed` counted an untested environment as a success.** The state
   combined "every probed module imported" with "there was nothing to probe",
   which is how three empty generated specs came to satisfy K1 and K2. Split
   into `installed_verified` / `installed_unverified` / `installed_import_fail`;
   every gate now reports both the declared reading and the strict one.
5. **A pip timeout was charged to the mechanism as a failed install.**
   `harness.run()` returns exit `None` when pip exceeds `E069_PIP_TIMEOUT`
   (default 1800 s); `analyze.py` read that as "exit != 0" and scored it a
   failed install. It is the instrument running out of time. Now
   `not_exercised`, with its reason.
6. **This document's own headline did not reproduce.** It reported a
   15-repository run as 20 and reported the near-miss count as "149 of 383",
   which no rule over the committed metadata produces; the computed figure is
   **132 of 383**. Both are corrected above, and the near-miss count is now
   computed by `pin_compatibility.py` rather than asserted in prose.
7. **The declared gate cannot fail, and its own protocol said so.** K1 asks for 3
   clean installs; the only three specs that can install name 0, 0 and 1
   packages. `PROTOCOL.md` Amendment 1 states this before any arm ran, and the
   run confirmed it — one additional repository was measured precisely because
   it carried an empty spec, and that single measurement moved the tool's own
   label from `KILL` to `mechanism holds`. **A gate whose only reachable
   successes are empty files measures nothing**, so this experiment's result is
   read from K3 and from the verified counts, not from K1's label.

Recorded because a harness that cannot fail loudly is the same failure this
experiment was built to detect — and so is a report of it that cannot be
regenerated from its own evidence.