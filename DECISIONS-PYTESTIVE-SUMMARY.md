<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# pyprovides — Decision Summary

## What was produced

### Packaging for PyPI distribution
- Built `dist/pyprovides-0.1.0-py3-none-any.whl` and `dist/pyprovides-0.1.0.tar.gz`
- Package structure: standard library only, Python 3.8+, MIT license
- Console script entry point: `pyprovides = pyprovides.pyprovides_cli:main`

### Code restructuring for doc lint compliance
- **`pyprovides/pyprovides/fix_import.py`**: Reduced from 342 to 259 lines (under 300-line cap)
  - Removed `main()` prototype demo function (moved to separate file)
  - Kept all core module functions: `extract_module_names`, `resolve_module`, `suggest_install`, `pyfix_suggest`, `run_manual_baseline`, `run_pyfix_prototype_test`, `mean`, `run_command`, patterns
- **`pyprovides/pyprovides/prototype.py`** (new): Contains the `main()` prototype demo that was previously in `fix_import.py`
  - Runs E086 alias cases test: 12/12 resolution accuracy, 4.12x mean speedup
  - Outputs: "PROTOTYPE RESULT: Demonstrated practical difference"
- **`pyprovides/pyprovides/pyprovides_cli.py`**: Updated CLI import from `.fix_import` to `.prototype`

### Shell/editor integration files (new, not product)
- **`pyfix.fish`**: Fish shell function wrapping `pyprovides fix-import`
- **`pyfix.zsh`**: Zsh function wrapping `pyprovides fix-import`
- **`pyprovides/pyprovides/__main__.py`**: Allow `python3 -m pyprovides` invocation

### Experiment file reference
- **`EXPERIMENTS/09X-pyfix-prototype/prototype.py`**: Existing experiment file (already in repo, not modified in content)

## Verified functionality

- `pyprovides find psycopg2` → `psycopg2-binary 2.9.13` (alias resolution)
- `pyprovides which psycopg2` → provides itself
- `pyprovides fix-import -- python3 -c "import psycopg2"` → resolves to psycopg2-binary
- `pyprovides fix-import -- python3 -c "import sklearn"` → resolves to scikit-learn
- All 27 existing unit tests pass
- `tools/origin doc lint` exits 0 (7675 files checked)

## Key decisions

### Package name line: CLOSED
- Measured genuine rate of "which distribution provides this module?" reports: 2–4 of 858 import-error reports (0.23–0.47%), well under the 1% gate (F113, D102)
- The resolver line as a whole is closed per measured evidence
- This tool stays a prototype, not a product for general distribution

### Prototype line: OPEN (evidence-gathering)
- 100% resolution accuracy on 12 alias cases from E086 experimental data
- 4.12x mean speedup over manual baseline for resolvable cases
- Mechanism validated: 15/19 discrimination probes resolved (E086)
- Empirical speedup: 2.44x for psycopg2 alias case (E086)
- **Prototype is explicitly reversible and exploratory** — no product claim
- Differentiates from `deptry` (requires installed virtualenv) by working with **nothing installed**
- Known limitation: `.pth` redirectors invisible, latest release metadata only

### Adoption path: None claimed
- No adoption claims, no user metrics, no release
- Documented for independent reproduction and evaluation
- Package available at `dist/` but not uploaded to PyPI (no credentials configured)

## What remains unknown

- Whether the mechanism would be useful in actual developer workflows outside the E086 test cases
- Generalizability beyond the 12 tested alias cases (cv2, psycopg2, MySQLdb, sklearn, yaml, bs4, Crypto, PIL, dateutil, jwt, serial, dotenv)
- Real-world import error patterns not captured in the controlled test set

## Next actions (single most useful)

1. **If PyPI credentials become available**: Run `origin release check` and publish the package
2. **Run fresh-observation experiment** on real-world import error patterns to measure generalizability beyond E086 test cases
3. **Consider shell/editor integration** as a reversible exploratory step (already provided as `pyfix.fish` and `pyfix.zsh`)
4. **Document boundary conditions** in README: what the tool can and cannot do, measured rates

## Artifact check

- Package builds successfully: `python3 setup.py sdist bdist_wheel` ✓
- All imports work: `from pyprovides import provides, find_provider, fix_import` ✓
- All 27 unit tests pass ✓
- Doc lint passes ✓
- Git commit recorded: `eafb6588` "pyfix prototype: restructure for doc lint 300-line cap, move main() to prototype.py, update CLI import, add shell integration files" ✓