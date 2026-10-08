# E059 — Do popular PyPI packages' import names/commands differ from their pip names? (probe)

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: complete
last-verified: 2026-10-08
-->

## Question

A fresh-observation probe (per D080): is there a real, unserved population of
"I installed `X`, what do I import / run?" — measurable as pip-name vs import-name
and pip-name vs console-command disagreement on real wheels?

## Method

- Demand ordering: `raw/top-pypi.json`, 15,000 most-downloaded PyPI projects
  (hugovk top-pypi-packages, fetched 2026-10-08), stride sample 125 → 120 rows.
- Per row: PyPI JSON metadata → smallest `py3` wheel (≤ 8 MiB) → read
  `top_level.txt`/RECORD for import names and `entry_points.txt` for
  console scripts. Normalize by lower + `[-_.]+ → -`.
- M1: `pip name ∈ import names`? M2: every console script == pip name?
- Kill gate (declared): M1-mismatch share < 0.05 AND M2 < 0.10 → population not
  observed → nothing to build.

## Results

`ok=95`, `M1: 22 of 93 evaluable mismatched (0.237)`, `M2: 7 of 16 evaluable mismatched (0.44)`.

Raw: `raw/results.json`.

## Reading

M1 fires, so the gate is *not* met — the mismatch class is real. But the 22
mismatch rows split:

- namespace-sharing distributions (`google-cloud-*`→`google`, `opentelemetry-*`,
  `cocotbext-*`) and typing stubs (`types-*`→`*-stubs`): documented conventions;
- derivable-by-convention (`dnspython`→`dns`, `clean-fid`→`cleanfid`,
  `redis-py-cluster`→`rediscluster`, prefix strips);
- the unpredictable core known by name (`Pillow`→`PIL`, `scikit-learn`→`sklearn`,
  `PyYAML`→`yaml`, `beautifulsoup4`→`bs4`, `opencv-python`→`cv2`,
  `python-dateutil`→`dateutil`) did **not** occur in this sample at all.

M2's 7 rows are mostly extra entry points (`pylint-config`, `pyreverse`,
`pylint`'s `symilar`, `ipwhois_utils_cli`, `hachoir-*` family); one real
rename-class row (`jupyter-cache`→`jcache`).

## Prior art and serving check

- Reverse direction (import → pip package) is built: `buptanswer/pyimport2pkg`,
  `yyds-fast/yyds-pip-audit` (GitHub repo search, 2026-10-08).
- Forward direction is answered by the served document: the package README
  itself states `import` usage; `pip show -f` lists installed files.
- SO demand query `import name different package name` returns off-topic topic-
  noise, not a concentrated unserved request stream (API probe, 2026-10-08).

## Verdict

KILL for a candidate. The class exists (F091) but the serving channel is the
package's own documentation and the unpredictable residue is a known short list,
not an unserved population. D077 not violated: the mismatch population was
extracted from real wheels, not a trigger harvest. Nothing built.
