<!-- origin-meta
owner: docs/INDEX.md
status: draft
last-verified: 2026-10-10
-->

# pyprovides — which distribution provides this module, with nothing installed

**Prototype. Not a product, not released, no adoption.** What is measured and
what is not is stated below rather than implied.

```bash
./pyprovides which Crypto     # which distribution provides this module
./pyprovides scan .           # find dependency names shadowed by other projects
```

Standard library only, Python 3.8+, no install step.

## The practical difference

You import a module and want to know what to install, or you declared a
dependency and want to know it is the one you meant. The existing answer is an
installed environment:

- **`deptry` 0.25.1**, the strongest tool for this shape of question, resolves
  imports against an **installed virtualenv**. Measured on 13 repositories with
  nothing installed: 974 findings, 951 of them `DEP001` reporting `numpy`,
  `scipy` and each project's *own* package as missing. Its documentation says
  it must run inside the project's virtualenv, and that is true — it simply
  cannot be used before the install, on someone else's pull request, or in a
  read-only sandbox.
- **`pip install <name>`** tells you whether a name exists. It does not tell
  you what it *provides*.

This reads the answer from PyPI instead. A wheel is a zip file, and a zip's
**central directory sits at the end of the file and names every entry**. So the
complete list of modules a distribution ships is two HTTP `Range` requests away,
with **zero payload bytes downloaded and nothing installed**.

```python
from pyprovides import provides
status, modules, detail = provides("scikit-learn")
# ('ok', {'sklearn', 'sklearn.utils', ...}, {'wheel_bytes': 12582912,
#                                            'bytes_fetched': 65536, ...})
```

A 12 MB wheel is answered from a 64 KiB window.

## What is measured

| claim | how | where |
|---|---|---|
| the mechanism works on real distributions | 578 declared distributions from 24 real repositories resolved at **0.931** | `EXPERIMENTS/085-declared-not-provided/results.json` |
| it recovers the true provider | **10 of 10** positive controls | `control-results.json` |
| it does not fire on correct declarations | **0 of 10** false flags | `control-results.json` |
| the class it detects is real | `pip install Crypto` → exit 0, wrong project + 8 deps, `import Crypto` fails | `silent-class-proof.txt` |
| the incumbent cannot do this | deptry 0.25.1 run for real, installed and not installed | `deptry-baseline.json`, `controlled-comparison.json` |

17 tests, no mocks of the code under test: the zip tests build a real zip with
`zipfile` and read it back through the same parser. The network tests are real
and are skipped when PyPI is unreachable rather than faked.

```bash
python3 -m unittest discover -s pyprovides
```

## What is not measured

- **That anyone wants it.** No adoption, no usage, no feedback. E085's G3 came
  back **HOLD** and its G4 precision gate **FAIL**ed: the class this detects
  occurs in about **0.6%** of imported modules in that corpus, and the flagged
  rows were half instrument artifact. The linter idea is closed on measured
  grounds, not on a screen.
- **Which distribution provides a module**, in the general case. There is no
  reverse index on PyPI, and a central directory only answers forward. The
  10-of-10 recovery above comes from controls with a known provider.
- **Anything but Python.** `npm`, `cargo` and `crates` ship the same wheel
  layout; none was measured.

## Known limits

- **A `.pth` redirector is invisible.** A distribution can make a module
  importable without shipping a file for it. `pynvml` 13.0.1 does exactly this
  and still imports cleanly, so this tool calls it a shadow name and the
  runtime disagrees. It is a warning, not a broken install — but the tool
  cannot tell the difference from metadata.
- **`no-wheel` is its own status, on purpose.** A project that ships only an
  sdist tells you nothing about whether `pip install` will fail loudly or
  install silently. That needs an install test. E070 ran one: 3 of 3 such
  installs failed loudly.
- **Latest release, not your pin.** Metadata is the newest version on PyPI.
- Some wheels are non-compliant — `pynvml` nests entries under
  `site-packages/`, which is reported as a top-level name because that is what
  the archive actually contains.