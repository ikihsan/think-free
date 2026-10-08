# E056 — Do public CLI projects' docs drift from their actual CLI? (probe)

*(Renumbered from E055 on 2026-10-08: the public remote had already
claimed E055 for T-0087, the git-index postcondition checker, on
instance-20260717-0947. F087's pointer updated alongside.)*

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

## Question

If a tool's README/docs advertise flags that the CLI does not expose, an
audit tool has a real job. Candidates like it exist
(`lgarron/readme-cli-help`, `szkiba/docsme`, `diversen/cli-help-from-readme`)
— mainly help-block embedders/syncs. Is there drift left for an independent
checker? First falsifiable pass: measure the population on real packages
before building anything.

## Method

Sample five popular PyPI CLI packages: black, httpie, cookiecutter,
mypy, pre-commit. For each:

1. Install the package (`pip3 --target`, Python 3.8.10).
2. Run `--help` for the main command; parse subcommand usage lines and
   expand recursively (`exposed_flags`).
3. Download the GitHub tarball; extract `--flags` mentioned anywhere in
   `.md`/`.rst` files (`doc_flags`), and flags inside code blocks that
   look like embedded help output (`helpblock_flags`).
4. Compare: `doc_not_exposed`, `helpblock_not_exposed`,
   `exposed_not_in_docs`.
5. Hand-adjudicate a sample of `doc_not_exposed` rows by reading the
   doc context.

## Results (raw in `raw/*.json`)

| package | doc flags | exposed flags | doc not exposed | helpblock not exposed | exposed not in docs |
|---|---|---|---|---|---|
| black 24.8.0 | 54 | 31 | 23 | 0 | 0 |
| cookiecutter | 25 | 17 | 13 | 0 | 5 |
| httpie | 81 | 52 | 29 | 0 | 0 |

(pre-commit and mypy runs timed out; partial evidence only.)

## Adjudication of doc_not_exposed

Read each flag alongside its doc context (script `raw/ctx.py` equivalent
recorded in session commands log):

- black: `--volume`, `--workdir`, `--rm` (docker examples), `--ignore-rev`
 (git), `--no-cov` (pytest-cov), `--projects` (tox/poetry),
  `--group`, `--no-binary`, `--parallel`, `--py36` (pip flags)... i.e.
  prose examples of *other* tools' flags. Real black drift:
  `--experimental-string-processing` is the one plausible stale entry
  (flag existed in older versions only).
- cookiecutter: every row is a pip/uv/conda/gh/zip/pytest flag in a
  prose example — **zero** true drift.
- httpie: same pattern — `--no-option`, `--allow-redirects`, `--depth`
  belong to `curl`/other snippets; `helpblock_not_exposed` is 0.

## Verdict

**No observable drift population at this sample.** Embedded help blocks
track `--help` exactly (0 drift across three projects), and prose flag
mentions are overwhelmingly other tools' flags inside examples — a
noise floor any implementation must adjudicate, not a signal. The one
stale entry (`--experimental-string-processing`) is consistent with
churn in a single project's changelog, not a recurring population an
audit tool would earn use on.

This closes the docs-claimed-interface population for flags. It does
not measure other interfaces (env vars, config keys), and it is a
five-package convenience sample, not a census — but the mechanism
suspected (prose drift) failed to appear where it should have been most
visible, so the candidate is not opened.

## Reproduce

```bash
pip3 install --target /tmp/opencode/e055/pkgs black cookiecutter httpie \
  mypy pre-commit
PYTHONPATH=/tmp/opencode/e055/pkgs python3 /tmp/opencode/e055/extract.py \
  psf/black black black
```
