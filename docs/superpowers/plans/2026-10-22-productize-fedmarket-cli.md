# Fedmarket CLI Productization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the fedmarket CLI tool into a properly distributable Python package with documentation, installers, CI/CD, and PyPI publishing capability.

**Architecture:** The fedmarket package already exists with all core functionality. This plan focuses on productization: fixing packaging issues, adding missing entry points, comprehensive documentation, CI/CD pipeline, and preparing for PyPI release.

**Tech Stack:** Python 3.8+, setuptools, pytest, ruff, mypy, GitHub Actions for CI/CD, PyPI for distribution.

## Global Constraints

- All code must pass existing tests (`python3 -m pytest tests/`)
- Line length: 100 chars (ruff)
- Type hints encouraged but not required (mypy `disallow_untyped_defs = false`)
- No new external dependencies beyond current `dependencies = []` in pyproject.toml
- Must maintain compatibility with Python 3.8+
- All documentation must stay under 300-line cap per file
- MIT License maintained

---

### Task 1: Fix Package Structure and Entry Points

**Files:**
- Modify: `fedmarket/pyproject.toml`
- Modify: `fedmarket/fedmarket/__init__.py`
- Create: `fedmarket/fedmarket/__main__.py` (ensure it exists and works)

**Interfaces:**
- Consumes: existing package structure
- Produces: working `fedmarket` and `fedmarket-decide` console scripts

- [ ] **Step 1: Verify current entry points work**

```bash
cd /home/ubuntu/think-free/fedmarket
pip install -e .
fedmarket --help
fedmarket-decide --help
```

Expected: Both commands show help text

- [ ] **Step 2: Fix pyproject.toml entry_points if needed**

Current pyproject.toml has:
```toml
[project.entry-points]
console_scripts = {fedmarket = "fedmarket.cli:main", fedmarket-decide = "fedmarket.decide_cli:main"}
```

Verify these match actual module paths. The cli.py has `main()` at line 33, decide_cli.py has `main()` at line 55.

- [ ] **Step 3: Ensure __main__.py exists and works**

```python
# fedmarket/fedmarket/__main__.py
"""fedmarket package entry point."""

from .cli import main

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Test wheel build**

```bash
pip wheel --no-deps -w dist .
ls dist/
```

Expected: `fedmarket-0.1.0-py3-none-any.whl` created

- [ ] **Step 5: Commit**

```bash
git add fedmarket/pyproject.toml fedmarket/fedmarket/__main__.py
git commit -m "fix: ensure package entry points work for distribution"
```

---

### Task 2: Add Missing CLI Entry Point for Exploration Mode

**Files:**
- Modify: `fedmarket/pyproject.toml`
- Verify: `fedmarket/fedmarket/explore.py` has main()

**Interfaces:**
- Consumes: existing explore.py module
- Produces: `fedmarket-explore` console script

- [ ] **Step 1: Verify explore.py has main()**

Check `fedmarket/fedmarket/explore.py` lines 203-234 - it has `if __name__ == "__main__":` block with argparse.

- [ ] **Step 2: Add fedmarket-explore to pyproject.toml entry_points**

```toml
[project.entry-points]
console_scripts = {
    fedmarket = "fedmarket.cli:main",
    fedmarket-decide = "fedmarket.decide_cli:main",
    fedmarket-explore = "fedmarket.explore:main"
}
```

- [ ] **Step 3: Test the new entry point**

```bash
pip install -e .
fedmarket-explore --help
fedmarket-explore --all
```

Expected: Shows help and runs all 27 profile combinations

- [ ] **Step 4: Commit**

```bash
git add fedmarket/pyproject.toml
git commit -m "feat: add fedmarket-explore console script entry point"
```

---

### Task 3: Create Comprehensive Documentation

**Files:**
- Create: `fedmarket/docs/USER_GUIDE.md`
- Create: `fedmarket/docs/DECISION_GUIDE.md`
- Create: `fedmarket/docs/API_REFERENCE.md`
- Create: `fedmarket/docs/EXPERIMENTS.md`
- Modify: `fedmarket/README.md` (update to link to new docs)

**Interfaces:**
- Consumes: existing README.md content
- Produces: structured documentation under docs/ directory

- [ ] **Step 1: Create USER_GUIDE.md with installation, quick start, modules, output format**

```markdown
# User Guide

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->

## Installation

```bash
pip install fedmarket
# or from source:
pip install -e .
```

## Quick Start

```bash
# Full assessment of PSC 7030 (live USAspending API)
fedmarket --code 7030

# Save results to JSON
fedmarket --code DA10 --output da10.json

# Run specific modules only
fedmarket --code 7030 --modules recipient,award

# Offline survival analysis (no network)
fedmarket --code 7030 --survival
```

## Module Reference

| Module | Flag | Description | Network |
|--------|------|-------------|---------|
| recipient | `--modules recipient` | Screen score, award distribution, concentration | Yes |
| award | `--modules award` | Software/service/hardware categorization | Yes |
| time | `--modules time` | Recent 12mo vs 5yr comparison | Yes |
| agency | `--modules agency` | Funding/awarding agencies, federal accounts | Yes |
| vehicle_sin | `--modules vehicle_sin` | GSA MAS SIN & SEWP category analysis | Yes |
| subaward | `--modules subaward` | Prime-specific subaward trace | Yes |
| survival | `--survival` | Entry survival & graduation (offline) | No |

## Output Format

JSON structure with all modules...
```

- [ ] **Step 2: Create DECISION_GUIDE.md with two-axis framework explanation**

```markdown
# Decision Guide

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->

## Two-Axis Framework

### Axis 1: Entry Accessibility
How easy is it to enter the market?
- Screen score (recipient count × (1 - top-10 concentration))
- ≤$40k award fraction
- Recipient count
- Software market fit (%)

### Axis 2: Business Sustainability
How likely are recipients to return and grow?
- Survival % (UEI match, FY20-21 → FY23-25)
- Graduation % (returning recipients >$100k aggregate)
- Net-positive return %

## Profile-Based Recommendations

| Profile | Budget | GTM | Focus | Best Code | Vehicle |
|---------|--------|-----|-------|-----------|---------|
| Quick Entry | ≤$40k | Direct | Software | **7030** | Direct Sales |
| Balanced | ≤$100k | GSA MAS | Software/SaaS | **DA10** | GSA MAS 511210/511210S/518210C |
| Enterprise | Enterprise | Direct | Services | **DA01** | GSA Schedule 54151S |
| Subcontract | ≤$100k | Subcontract | Software | **DA10** | Sub to Peraton/Highlight |

## Usage

```bash
# Interactive
fedmarket-decide

# Scripted
fedmarket-decide --budget leq_40k --gtm direct --focus software --json
```

## Caveats

Key tradeoffs and trend warnings from E204...
```

- [ ] **Step 3: Create API_REFERENCE.md for programmatic use**

```markdown
# API Reference

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->

## Core Functions

### `fedmarket.decide.assess_code(psc_code: str) -> dict`
Returns static metrics for a PSC code.

### `fedmarket.decide.decide_code(budget: str, gtm: str, focus: str) -> dict`
Returns recommendation with rationale and next steps.

### `fedmarket.data.assess_code(psc_code: str) -> dict`
Low-level static data lookup.

### `fedmarket.explore.explore_rankings(budget, gtm, focus) -> dict`
Rank all codes for a profile.

### `fedmarket.explore.explore_all_profiles() -> dict`
All 27 profile combinations.
```

- [ ] **Step 4: Create EXPERIMENTS.md linking to source experiments**

```markdown
# Experiment Provenance

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->

| Module | Experiment | Date | Key Finding |
|--------|------------|------|-------------|
| recipient | E202 | 2026-10-20 | Screen score, recipient analysis |
| award | E203 | 2026-10-20 | 64.5% software in 7030 |
| time | E204 | 2026-10-20 | 7030 concentrating (45%→64% top-10) |
| agency | E205 | 2026-10-20 | DA10 has GSA Schedule (7.8%) |
| vehicle_sin | E210 | 2026-10-20 | DA10: 28% small vendor GSA MAS share |
| subaward | E209+ | 2026-10-20 | DA10: 8.1% sub/prime ratio |
| survival | E211 | 2026-10-21 | DA10: 72.6% survival, 41.2% graduation |

See `EXPERIMENTS/` in repository root for raw data and RESULT.md files.
```

- [ ] **Step 5: Update README.md to link to new docs**

Add at top of README.md:
```
## Documentation
- [User Guide](docs/USER_GUIDE.md)
- [Decision Guide](docs/DECISION_GUIDE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Experiment Provenance](docs/EXPERIMENTS.md)
```

- [ ] **Step 6: Commit**

```bash
git add fedmarket/docs/ fedmarket/README.md
git commit -m "docs: add comprehensive documentation (USER_GUIDE, DECISION_GUIDE, API_REFERENCE, EXPERIMENTS)"
```

---

### Task 4: Add GitHub Actions CI/CD Pipeline

**Files:**
- Create: `fedmarket/.github/workflows/ci.yml`
- Create: `fedmarket/.github/workflows/release.yml`

**Interfaces:**
- Consumes: pyproject.toml test configuration
- Produces: automated testing on PR/push, automated release on tag

- [ ] **Step 1: Create CI workflow**

```yaml
# fedmarket/.github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      - name: Run lint
        run: |
          ruff check .
      - name: Run type check
        run: |
          mypy fedmarket/
      - name: Run tests
        run: |
          python3 -m pytest tests/ -v
      - name: Test CLI entry points
        run: |
          fedmarket --help
          fedmarket-decide --help
          fedmarket-explore --help
```

- [ ] **Step 2: Create release workflow**

```yaml
# fedmarket/.github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      packages: write
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install build dependencies
        run: |
          pip install build twine
      - name: Build package
        run: |
          python -m build
      - name: Check package
        run: |
          twine check dist/*
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          twine upload dist/*
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
```

- [ ] **Step 3: Test CI locally with act (if available) or push to trigger**

```bash
# Push to trigger CI
git push origin HEAD
```

- [ ] **Step 4: Commit**

```bash
git add fedmarket/.github/workflows/
git commit -m "ci: add GitHub Actions CI/CD pipeline for testing and PyPI release"
```

---

### Task 5: Add Version Management and Changelog

**Files:**
- Create: `fedmarket/CHANGELOG.md`
- Modify: `fedmarket/pyproject.toml` (ensure version is single source of truth)

**Interfaces:**
- Consumes: pyproject.toml version
- Produces: changelog for releases

- [ ] **Step 1: Create CHANGELOG.md**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `fedmarket-explore` CLI command for exploring all 27 profile combinations
- Comprehensive documentation (USER_GUIDE, DECISION_GUIDE, API_REFERENCE, EXPERIMENTS)
- GitHub Actions CI/CD pipeline

### Fixed
- Package entry points for proper distribution

## [0.1.0] - 2026-10-22

### Added
- Initial release of fedmarket CLI toolkit
- PSC code assessment via USAspending API (recipient, award, time, agency modules)
- GSA MAS SIN & SEWP vehicle analysis (vehicle_sin module)
- Prime-specific subaward trace (subaward module)
- Offline entry survival analysis (survival module)
- Two-axis decision framework (fedmarket-decide interactive and scripted)
- Profile exploration across 27 combinations (fedmarket-explore)
- Static data from experiments E202-E211
- JSON output for all modules
```

- [ ] **Step 2: Add version reading utility**

```python
# fedmarket/fedmarket/_version.py
"""Version reading from pyproject.toml (single source of truth)."""

import tomllib
from pathlib import Path

def get_version() -> str:
    """Read version from pyproject.toml."""
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject, "rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]

__version__ = get_version()
```

- [ ] **Step 3: Update __init__.py to expose version**

```python
# fedmarket/fedmarket/__init__.py
"""fedmarket: Federal Marketplace Assessment Toolkit."""

from ._version import __version__

__all__ = ["__version__"]
```

- [ ] **Step 4: Commit**

```bash
git add fedmarket/CHANGELOG.md fedmarket/fedmarket/_version.py fedmarket/fedmarket/__init__.py
git commit -m "feat: add version management and changelog"
```

---

### Task 6: Add Pre-commit Hooks and Development Tooling

**Files:**
- Create: `fedmarket/.pre-commit-config.yaml`
- Modify: `fedmarket/pyproject.toml` (add pre-commit to dev deps)

**Interfaces:**
- Consumes: ruff, mypy configurations
- Produces: automated code quality checks on commit

- [ ] **Step 1: Create .pre-commit-config.yaml**

```yaml
# fedmarket/.pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
        args: [--config-file=pyproject.toml]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-json
```

- [ ] **Step 2: Add pre-commit to dev dependencies in pyproject.toml**

```toml
[project.optional-dependencies]
dev = ["pytest>=7.0", "ruff>=0.1", "mypy>=1.0", "pre-commit>=3.0"]
```

- [ ] **Step 3: Install and test pre-commit**

```bash
cd /home/ubuntu/think-free/fedmarket
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files
```

- [ ] **Step 4: Commit**

```bash
git add fedmarket/.pre-commit-config.yaml fedmarket/pyproject.toml
git commit -m "dev: add pre-commit hooks for code quality"
```

---

### Task 7: Validate Package Build and Test Installation

**Files:**
- No new files (validation only)

**Interfaces:**
- Consumes: all previous tasks
- Produces: verified working package

- [ ] **Step 1: Clean build**

```bash
cd /home/ubuntu/think-free/fedmarket
rm -rf dist build *.egg-info
pip wheel --no-deps -w dist .
```

- [ ] **Step 2: Test install from wheel**

```bash
pip install dist/fedmarket-0.1.0-py3-none-any.whl
fedmarket --help
fedmarket-decide --help
fedmarket-explore --help
```

- [ ] **Step 3: Test offline survival mode works after install**

```bash
fedmarket --code 7030 --survival
```

Expected: Shows survival analysis with 53.3% baseline

- [ ] **Step 4: Run full test suite**

```bash
python3 -m pytest tests/ -v
```

- [ ] **Step 5: Test decision CLI scripted mode**

```bash
fedmarket-decide --budget leq_40k --gtm direct --focus software --json
fedmarket-decide --budget leq_100k --gtm gsa_mas --focus saas --json
```

- [ ] **Step 6: Commit any fixes needed**

```bash
git add -A
git commit -m "fix: any issues found during package validation"
```

---

### Task 8: Prepare for PyPI Release

**Files:**
- Verify: `fedmarket/LICENSE` exists (MIT)
- Verify: `fedmarket/README.md` has proper description
- Verify: `fedmarket/pyproject.toml` has all required metadata

**Interfaces:**
- Consumes: complete package
- Produces: PyPI-ready package

- [ ] **Step 1: Verify PyPI metadata completeness**

Check pyproject.toml has:
- name, version, description, readme, requires-python
- license (MIT)
- authors
- classifiers (including Development Status, Intended Audience, License, Python versions, Topics)
- dependencies (empty list is fine)
- optional-dependencies (dev)
- entry-points (3 console scripts)
- package discovery configuration

- [ ] **Step 2: Verify LICENSE file exists**

```bash
cat fedmarket/LICENSE
```

- [ ] **Step 3: Build and verify package metadata**

```bash
cd /home/ubuntu/think-free/fedmarket
python -m build
twine check dist/*
```

- [ ] **Step 4: Test install from TestPyPI (optional)**

```bash
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ fedmarket
```

- [ ] **Step 5: Document release process in RELEASE_PROCESS.md**

```markdown
# Release Process

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->

## To Release a New Version

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with release notes
3. Commit: `git commit -am "chore: release vX.Y.Z"`
4. Tag: `git tag vX.Y.Z`
5. Push: `git push origin main --tags`
6. GitHub Actions will build and publish to PyPI automatically
7. Create GitHub Release (auto-generated by release workflow)

## Requirements

- PYPI_API_TOKEN secret configured in GitHub repository settings
- Main branch protected with required CI checks
```

- [ ] **Step 6: Commit**

```bash
git add fedmarket/RELEASE_PROCESS.md
git commit -m "docs: add release process documentation"
```

---

## Execution Order

Tasks 1-3 can be done in parallel (independent files).
Tasks 4-6 can be done in parallel (independent files).
Task 7 depends on 1-6 completing.
Task 8 depends on 7 completing.

## Total Estimated Time

~2-3 hours for full implementation with testing.

## Success Criteria

1. `pip install fedmarket` works from PyPI (after release)
2. All three CLI commands work: `fedmarket`, `fedmarket-decide`, `fedmarket-explore`
3. All tests pass on Python 3.8-3.13
4. CI/CD pipeline runs on push/PR and releases on tag
5. Documentation is complete and linked from README
6. Package builds without warnings (`twine check` passes)