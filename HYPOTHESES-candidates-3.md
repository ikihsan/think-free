<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-19
-->

# Candidate under consideration: ArXiv computational reproducibility (E067)

Split out of [`HYPOTHESES.md`](HYPOTHESES.md) on 2026-10-19 at that file's
300-line cap, to make room for the money-axis entry (E196). Moved unchanged in
meaning; the header that followed is repeated below so the file stands alone.

## Candidate under consideration: ArXiv computational reproducibility (E067)

### H-01 — ArXiv reproducibility: a tool can generate machine-runnable environment specs from partial information

**Observation:** E067 measured 34 ArXiv computational papers with code links (sampled from 1,682 papers with code links, 10.9% of 15,397 harvested). Only 4/34 (11.8%) had machine-runnable specs (A1), 1/34 (2.9%) partial (A2), 11/34 (32.4%) docs-only (A3), 18/34 (52.9%) no env info (A4). All four kill gates passed: population ≥20 (34), severity A1<0.50 (0.118), differentiation A4>0.10 (0.529), baseline A5≤code-link (0≤0.118). `observed`.

**Mechanism:** A deterministic tool analyzes a paper's GitHub repository (source code, any existing config files, paper metadata like submission date) and generates a complete, pinned environment specification (conda `environment.yml` or `requirements.txt` with all `==` versions) that installs and runs the paper's main computational entry point.

**Assumptions:**
1. Source code imports and runtime behavior reveal sufficient version constraints
2. Paper submission date correlates with compatible package versions
3. Main entry point is identifiable (README, `main.py`, `__main__.py`, or setup.py `entry_points`)
4. A clean virtual environment can test install + smoke test within resource limits
5. The generated spec's correctness is verifiable by execution, not static analysis

**Prior art:** `repo2docker`/`binder` (builds Docker from existing config files, doesn't invent pinned versions), `pipreqs` (infers imports, no version pinning), `conda-lock`/`poetry lock`/`pip-tools` (resolve from existing specs, don't generate from scratch), `reprozip` (captures runtime deps, needs working env first). **Claimed difference:** Generates complete pinned spec from minimal/no starting spec, with install+run verification.

**Strongest objection:** Information insufficiency — two repos with identical `requirements.txt` (`numpy`, `pandas` unpinned) may need different pinned versions (`numpy==1.21.0` vs `numpy>=1.20`). Static analysis cannot distinguish; tool must run trials or abstain. Version search space is large; compute cost may be prohibitive.

**Kill gate:** On a held-out sample of 20 A2+A3 papers (partial/docs-only env info), the tool generates specs that **install successfully** (≥80% install success rate) **and pass a smoke test** (import main module, run `--help` or minimal execution) for **≥30% of papers**. Baseline (`repo2docker` + latest versions) must achieve <15% on same metric. If tool's install+run rate ≤ baseline + 10pp, abandon.

**Baseline:** `repo2docker` (v2024) run on each repo with no version constraints (uses latest compatible), followed by smoke test. Also: manual version selection by author (upper bound, not run here).

**Experiment:** `EXPERIMENTS/079-arxiv-reproducibility/` — harvest 20 new A2+A3 papers (stride sample from E067's population), run tool and baseline, measure install+run success. Reproduction: `cd EXPERIMENTS/079-arxiv-reproducibility && python3 run.py --sample 20 --gate`.

**Result:** `observed` (witness: FAIL as predicted), `untested` (full experiment)

**Uncertainty:** Whether version search via trial installation is feasible within time budget; whether smoke test (import + `--help`) correlates with full computational reproducibility; whether paper date heuristics narrow version space enough.

**Decision:** `hold` — witness passed (demonstrated information-sufficiency bound), full experiment infrastructure ready but not executed due to environment constraints (needs `python3.8-venv`). Tool prototype over-generates packages from import extraction; static analysis alone cannot resolve version ambiguity without trial installs.

**Reconsider when:** A cheaper version-inference method is found that passes the witness, or trial installation infrastructure is available. The witness FAIL is a structural bound, not an implementation defect.

### Candidate under consideration: Food recall purchase matching (E080)

#### H-01 — Food recall matching: a tool can match consumer purchases against FDA/USDA recall data

**Observation:** FDA publishes recall data with UPC, lot codes, best-by dates, distribution patterns. Consumers have purchase records (receipts, loyalty exports). Matching them could warn consumers of recalled products. `observed` that recall data exists and purchase records exist.

**Mechanism:** Match purchase records to recall records using UPC (exact or prefix), product name (fuzzy), lot code, best-by date. A match triggers a warning.

**Assumptions:**
1. Purchase records contain sufficient identifiers (UPC, product name, date, store)
2. Recall records contain matchable identifiers (UPC, lot codes, best-by dates, distribution)
3. Matching logic can handle real-world noise (truncated UPCs, store brands, missing lot codes)
4. False alarms (warning on non-recalled products) are more damaging than missed recalls

**Prior Art:** Store loyalty programs (Kroger, Safeway, Costco) notify members of recalls on purchased items. FDA recall API exists. Apps like "Food Recalls" show lists but don't match purchases. Claimed difference: universal matching across any purchase source, not store-specific.

**Strongest Objection:** Receipts rarely contain full UPCs or lot codes. Store brands have different UPCs than national brands. Consumers won't manually enter purchases. The matching problem is harder than it appears.

**Kill Gate:** On synthetic fixtures with known ground truth (3 formats × 30 purchases each, 15 recalled), the tool achieves precision ≥80%, recall ≥60% on ≥2 formats, specificity = 1.0. Baseline (random matching) must achieve <10% on same metric.

**Baseline:** Random matching of purchases to recalls.

**Experiment:** `EXPERIMENTS/080-food-recall-matching/` — generate synthetic fixtures with guaranteed identifier linkage, run matching, evaluate gates. Reproduction: `cd EXPERIMENTS/080-food-recall-matching && python3 run.py --gate`.

**Result:** `observed` (synthetic: PASS on 5/5 seeds), `untested` (real-world)

**Uncertainty:** Whether real receipts/loyalty exports have sufficient identifier coverage; whether store-brand UPC divergence breaks matching; whether FDA recall UPC sparsity (~40%) makes matching infeasible; whether consumers would use such a tool.

**Decision:** `hold` — mechanism passes synthetic kill gates but real-world identifier linkage is the unaddressed bottleneck. Loyalty programs already serve their members. Not a candidate for product engineering.
