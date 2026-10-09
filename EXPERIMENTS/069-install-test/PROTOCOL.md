<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# E069 — does E068's generated spec actually install, and does the repo's own declared spec do better?

## Question

E068 declared four kill gates passed and recorded "mechanism validated for
pip-based projects". None of the four gates installs anything: they measure
extraction, line syntax, name overlap between a generated file and an AST scan,
and whether a name resolves to *a* version on PyPI. E068's own README names the
install test as its most useful next action, and records "No install test: gates
measure generation quality, not whether `pip install -r generated.txt` works"
as an epistemic limit.

This experiment runs that test, and puts the strongest accessible alternative
beside it: the spec the repository already ships, which is what a person
actually types today.

## Population

The 20 test repositories E068 already fetched and extracted (A2 x1, A3 x11,
A4 x8), unmodified, at the commits `repos/MANIFEST.json` records. The four A1
ground-truth repositories are **excluded from the arms and used only as a
positive control** for the oracle (section "Oracle validity"), because their
spec is known to work and a test that cannot detect a known-good environment
measures nothing.

## Arms

| Arm | Definition | What it represents |
|-----|------------|--------------------|
| **GEN** | E068's generated pinned `requirements.txt` for the repo, exactly as committed in `cache/generated_specs/` | the candidate mechanism |
| **DECL** | the repository's own declared spec, installed as shipped: its `requirements*.txt`, else `pyproject.toml`, else `setup.py`, else nothing | the incumbent workflow, which costs the user nothing extra |
| **NONE** | no install; only the repository's own source tree on the path | the floor: what "the repo" gives you for free |

`NONE` is the control that makes `DECL` interpretable: for a repo that ships no
dependency list, `DECL` and `NONE` are the same thing, and any gain `GEN` shows
over `NONE` is a gain over having nothing. `NONE` names no package, so under the
oracle as amended its probe set is empty by construction and its `working` value
is **not applicable** — the floor arm is read as "installs nothing, imports
nothing", not as a failure.

## Predeclared kill gate

| Gate | Condition | Meaning |
|------|-----------|---------|
| **K1** (the mechanism works) | `GEN` installs cleanly in a fresh virtualenv for **>= 3 of 20** repos | if the generated file cannot be installed in three cases, the mechanism is not a mechanism |
| **K2** (the differentiation) | `GEN` succeeds on at least one repo where `DECL` fails | if `GEN` never beats the spec the repo already ships, there is no user-visible difference to adopt |
| **K3** (no harm) | `GEN` does not install cleanly on a repo where `DECL` does | a spec generator that breaks a working repo is worse than no tool |

**KILL** if K1 fails. **The direction closes** if K1 passes and K2 fails, with
K3 as a note. `GEN` remains a mechanism claim, never a product claim: a passing
install test says the file is well-formed and resolvable, not that anyone wants
it.

## Oracle: does the environment work?

`pip install` exiting 0 is necessary and not sufficient, so the oracle has two
parts and both are recorded per repo per arm:

1. **install**: `python -m pip install -r <spec>` in a fresh virtualenv, exit
   code and the first failing requirement line.
2. **import**: after the install, `python -c "import <module>"` for each
   top-level module the repository's own source imports that is neither stdlib,
   nor a first-party directory of the repo, **nor unmentioned by the arm's
   spec**. A repo counts as **working** for an arm when every such module
   imports.

   **Amended 2026-10-09 after control P1, before any arm was interpreted.** The
   first wording probed the *complement*: the modules the spec did not name.
   That makes "working" unsatisfiable by construction, since no spec supplies
   an import it never mentions. P1 exposed it — both pip-declarable A1
   repositories installed with exit 0 and were still reported not working, on
   modules their own pinned spec had never claimed. The oracle now probes what
   the arm said it would provide. A consequence worth stating: a spec that
   omits a dependency the repo needs is **not** caught by this oracle, and that
   gap is recorded as a limit rather than quietly left as a pass condition.

The import test is what separates "pip found a wheel for every pin" from "the
repository runs". Version pins matter here and nowhere else: a pin set that
installs and then fails `import torch` because two pins conflict at runtime is
the failure mode E068's gates cannot see, and it is the reason the generated
`torch==2.14.1 / numpy==2.5.3` pairing in `cache/generated_specs/` deserves a
run rather than a reading.

## Oracle validity (run first, before any arm is interpreted)

The import oracle must recover independent real positive examples, not only
failures. Declared before the arms:

- **P1**: the A1 repositories' own pinned specs must produce a working
  environment for **at least 1 of the pip-declarable A1 repositories**. Their
  specs are pinned and E067 classified them as known-good; a harness that cannot
  recognise a working environment cannot be used to judge a broken one.
  **Amended 2026-10-09, before any arm was run, from "2 of 4" to "1 of the
  pip-declarable ones":** 3 of the 4 A1 repositories ship a conda
  `environment.yml` and no pip-declarable file at all (`illidanlab/
  inversion-influence-function`, `Profluent-Internships/MMDiff`, `qzhb/BSSARD`),
  so a threshold of 2 of 4 could not be reached by any harness. A conda spec is
  **not** translated to pip here, because name translation is the mechanism
  under test in the `GEN` arm and would confound the control. Those three are
  recorded `not_exercised` — a missing observation, which per D082 is never a
  pass and never a fail.
- **P2**: a synthetic positive — a fixture package on the path plus a pinned
  `requirements.txt` naming one real dependency — must import successfully. This
  catches an oracle that is simply always-false.

If P1 or P2 fails, the arms are **not** interpreted and the harness is repaired
first. A test that cannot find a success is not evidence of failure.

## Environment

**Python 3.10.19**, a standalone CPython fetched with `uv python install
3.10`, and one fresh virtualenv per repo per arm, sequential. 3.10 rather than
this VM's own 3.8.10 because **E068 resolved every pin against 3.10** and
declares that as its target: testing the generator's output on an interpreter it
was not resolved for would measure the mismatch, not the mechanism. The chosen
interpreter's path and `sys.version` are recorded in `results.json`. The VM's
3.8.10 is not used and its absence from the arms is a limit, not a result.

`torch` is present in 18 of 20 generated specs and its 3.10 wheel is ~555 MB;
the run records fetch time and the wheel bytes pip reports per arm, so the cost
of the population is data rather than a footnote. Each virtualenv is removed
before the next arm of the same repository, and `results.json` records whether
it was.

## Amendment 1 — 2026-10-09, after the controls and before the arm run

The first pilot on `Itaymanes/K-QA` cost one virtualenv and produced pip's own
verdict on E068's generated spec: `ERROR: Could not find a version that
satisfies the requirement numpy==2.5.3`. Extrapolating from that, a static arm
was added (`pin_compatibility.py`) that asks the **metadata E068 already
downloaded** whether each pin admits the interpreter E068's own `PROTOCOL.md`
declares as its target. It costs no virtualenv and no download.

That arm decides most of the GEN outcome before a byte is installed, so the
install run is scoped to what it still decides:

- **GEN on the 17 repositories whose spec contains a pin the static arm shows
  pip will refuse: not installed, decided by the static arm.** The reason each
  spec cannot install is recorded per repository. Running 17 further
  virtualenvs to be told `No matching distribution found` again would cost
  roughly 30 GB of torch wheels on a VM with 12 GB free and would change no
  gate. This is a decision about cost, declared here rather than discovered at
  repository 14, and the static arm's prediction is checked against pip's own
  answer on the one repository where both ran (`Itaymanes/K-QA`) so the
  substitution is falsified rather than assumed.
- **GEN on the 3 repositories with no blocking pin: installed for real**, so
  K1 is not decided by the static arm alone.
- **DECL and NONE on every repository**: run in full. These are cheap (NONE
  installs nothing) and they are the incumbent and the floor.

`K1`'s threshold of "3 of 20" was written before the static arm existed and is
kept unchanged. Note what it means in practice: the only three specifications
that can install are the two that name **no packages at all**
(`Goallow/Mini-Hes`, `google-research/google-research`, both 0 pins) and one
with a single pin. K1 can therefore be met only by a specification that
installs nothing, which is a fact about the population's information content,
not about the mechanism.

## Epistemic limits, declared before the run

- 20 repositories, all deep-learning code, all from one arXiv year. The
  population is not ML research at large and no rate is generalised past it.
- This VM is 2 CPUs with ~950 MB RAM and no GPU. A repo whose scripts need a GPU
  is **not** testable here; the import oracle is deliberately narrower than
  "the paper's results reproduce", and a repo that imports cleanly but needs a
  GPU to run counts as `not_exercised`, never as a pass.
- The spec generator is taken exactly as E068 committed it. Improving it is out
  of scope; a fix that makes `GEN` pass would be a different experiment.
- `DECL` is the strongest alternative *available without inventing a new
  mechanism*. A colleague who reads the README and fixes the install by hand is
  not measured, and is the honest ceiling of what this comparison can claim.
- A negative result closes the claim and population actually tested.
