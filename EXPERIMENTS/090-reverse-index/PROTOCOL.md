<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E090 — can a module→distribution index for PyPI be built, and does it reach the modules real code imports?

Declared 2026-10-10, before any run. Task T-0089.

## The question

`pyprovides/README.md` lists, under *what is not measured*:

> **Which distribution provides a module**, in the general case. There is no
> reverse index on PyPI, and a central directory only answers forward. The
> 10-of-10 recovery above comes from controls with a known provider.

So the tool is named for a question it cannot answer, and the obstacle has never
been measured. Two facts would settle it:

1. **Is the index buildable?** What does it cost — requests, bytes, wall clock —
   to read every top-level module name from a slice of PyPI's wheels?
2. **Does it reach?** For module names that appear in real Python code, what
   share does the index resolve, and how does that compare with what a
   developer gets today from the existing mechanism?

## Why this is not T-0088

VM `0947` holds T-0088, "measure whether real Python import-error reports name
a module and no distribution" — the **demand** question. This is the
**capability** question: whether the instrument can answer at all. They are
answered on different populations for different decisions, and either one can
close the artifact alone. No population or corpus is shared.

## Population and sampling unit

**Unit: a distinct top-level module name.** Import statements are reported
separately and never used for a rate, because one popular module appears in
thousands of statements and would decide every proportion by itself.

**Population: top-level module names imported by real Python repositories**,
harvested mechanically. Repository selection, harvesting rules and the standard
library exclusion are fixed in `harvest.py` and declared there before the run.
No module name is ever chosen, curated or filtered by whether it is a known
cross-name case; the cross-name cases are *found*, not planted.

**Oracle: none is needed, and that is deliberate.** The index is built by
reading each wheel's zip central directory, which is the file list. A module
name can only enter the index if a wheel's directory names a file for it. So
"the index answers M with project P" is correct by construction, and coverage is
`|imports ∩ index keys| / |imports|`. There is no classifier, no hand label and
no self-assessment anywhere in this experiment.

**Limits of that oracle, stated now.** A `.pth` redirector can make a module
importable without shipping a file for it; `pynvml` 13.0.1 does. Such a module
is counted as uncovered. A wheel that nests entries under `site-packages/` is
reported as a top-level name, which is what the archive contains. Both are
E085's recorded limits and neither is repaired here.

## The index, and K

The ranked project list is `top-pypi-packages.min.json`
(`hugovk.dev/top-pypi-packages`, Hugovk, sourced from BigQuery, retrieved
2026-10-10): the **15,000 most-downloaded PyPI projects**, newest version of
each. It is a biased slice — biased *toward popular* — and the experiment's job
is to measure how much that bias costs, not to assume it is small. It is
downloaded once, its sha256 recorded, and not regenerated.

Coverage is reported at K ∈ {500, 1000, 2500, 5000, 10000, 15000}.

**Reach set.** 15,000 of PyPI's ~600,000 projects is 2.5% of the namespace, so
K cannot exceed 15,000 within this protocol. Anything above that is a different
experiment and is not claimed.

## Baseline: the strongest accessible alternative

What a developer gets today when they read `No module named 'M'`:

1. `pip install M`. This does PEP 503 name normalization (`M` → lowercase, runs
   of `-_.` collapsed) and then installs the project of that name, whatever it
   is — whether or not it ships `M`. This is the incumbent and it is free.
2. Failing that, a web search or a general assistant.

**Baseline B = the set of module names M for which step 1 leaves the import
working**: a project of normalized name M exists on PyPI *and* its wheel ships
M. Every additional module the index resolves over B is what the artifact would
add over the incumbent, and G3 is measured there.

## Gates, declared before the run

**G0 — instrument discrimination. Run FIRST, before any population row is read.**
E088's failure (F109) was seven sessions resting on an instrument never shown to
separate a real answer from a fake one. Three arms, all labels known by
construction:

| arm | n | must be |
|---|---|---|
| known cross-name pairs (`bs4`→`beautifulsoup4`, `cv2`→`opencv-python`, `PIL`→`pillow`, `sklearn`→`scikit-learn`, `Crypto`→`pycryptodome`, `dateutil`→`python-dateutil`, `dotenv`→`python-dotenv`, `zmq`→`pyzmq`, `OpenGL`→`PyOpenGL`, `serial`→`pyserial`, `MySQLdb`→`mysqlclient`, `psycopg2`→`psycopg2-binary`, `yaml`→`PyYAML`, `jwt`→`PyJWT`, `usb`→`pyusb`, `attr`→`attrs`, `win32api`→`pywin32`, `Tkinter`→`tk`, `fitz`→`PyMuPDF`, `docx`→`python-docx`, `lxml`→`lxml`) | 20 | ≥ 18 resolved to the named project |
| **negative controls**: 30 module names of things that do not exist | 30 | **0** resolved to any project |
| forward direction, E085's own controls | 10 | ≥ 8 recovered |

**If G0 fails, the run stops and the experiment reports that.** The negative arm
matters as much as the positive one: an index that answers for names that
provide nothing is worse than no index.

**G1 — buildable within real resources.** The K=15000 index is built within this
VM's actual limits: ≤ 3 h wall clock, ≤ 10 GB transferred, ≤ 20 GB on disk.
The K-curve is reported whether or not the top of the curve is reached; a curve
that runs out of budget is data, not a failure.

**G2 — coverage. KILL GATE.** At K=15000, with the baseline fallback **disabled**
so the number is the index's own: coverage ≥ **0.70** of the population's
distinct top-level module names.

*Reachable set, enumerated per D088.* Coverage can only be raised by (i) module
names whose provider is inside the ranked 15,000, and (ii) counting fewer
module names. A coverage of 0.70 is therefore reachable by either an index that
covers 70% of the population, or a population of 0.70-sized denominators — so
the **denominator is printed next to every figure and both readings are given**.
**If coverage < 0.70, E090 records that the general reverse resolver is not
buildable at any K reachable by this protocol, and pyprovides' 'what is not
measured' becomes 'measured, and negative'.**

**G3 — value over the incumbent.** Of the population's distinct module names,
the share resolved by the index **and not by baseline B**. Threshold **0.02**.

*Reachable set.* This can be met only by modules whose providing project's name
differs from the module name, **and** whose provider is inside the ranked 15,000,
**and** for which `pip install M` either fails or leaves the import broken. A
figure of 0.02 is therefore reachable only by a population with at least 2%
such rows; with the denominator printed, a reader can see which. **If G3 fails,
the practical difference over `pip install` is not measurable on this population
and the artifact's case rests on whatever else is measured — not on this gate.**

## What is measured regardless of gate outcome

Cost per project (requests, bytes, seconds) as a **distribution**, not a mean:
the mean is not what a build costs, the tail is. Coverage at every K. The share
of imported module names whose provider is outside the ranked 15,000 — the
number that bounds every future version of this idea. Status counts (`no-wheel`,
`no-such-project`, wheel read failure) reported separately, because E085's
record shows a status mix can silently become a result.

## Controls on the selection effects that could fake a pass

- **The ranked list's popularity bias** is the selection variable; coverage is
  therefore also reported per repository, so a reader can see whether one
  well-known repository is deciding the pooled figure.
- **Standard library and each repository's own local modules** are excluded,
  using the running interpreter's own module list and the repository's own
  top-level directories. Both exclusions are counted and printed.
- **Reused observations**: each distinct module name enters the population once.
  Statement counts are reported but never divided into.

## Kill and stop conditions

- G0 fails → stop, report.
- G2 fails → the general reverse resolver is not buildable under this protocol;
  record, do not extend K.
- G3 fails → the practical difference over `pip install` is not measured on this
  population; record, do not look for a population where it passes.
- Network unreachable → `not_evaluated`, never `FAIL` and never a cached row read
  as an answer.