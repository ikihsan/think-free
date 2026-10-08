<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-08
-->

# Prior Art Check: E065/E066 (Recurring Expense Detection) and E067 (ArXiv Reproducibility)

Per D083, prior art checks with three vocabularies (user, academic, infrastructure) are mandatory for fresh observations before candidate selection. Both E065/E066 and E067 passed kill gates; this records the precise differentiation.

---

## E065/E066 — Recurring Expense Detection from Bank CSVs

**Claim:** A deterministic, stdlib-only algorithm can detect recurring expenses (subscriptions, bills, memberships) from raw bank transaction CSV data with ≥85% precision and ≥80% recall, with ≤5% FPR. No external dependencies, no credentials, no API.

### 1. User Vocabulary (what practitioners search for)

| Query / Need | Existing Solutions Found | Gap |
|---|---|---|
| "categorize bank transactions automatically csv" | Most results point to Plaid, YNAB, Mint, Monarch — all require account linking | **No local-only CSV tool** |
| "find subscriptions in bank statement python" | Scripts using Plaid API, or manual regex on specific bank formats | **No general CSV parser with recurring detection** |
| "detect recurring payments from csv open source" | `bank-statement-analyzer` (manual categorization), `csv-to-ynab` (conversion only) | **No recurring detection logic** |
| "personal finance transaction categorization open source local" | Firefly III, Actual, Beancount, hledger — all require manual recurring entry or API | **No auto-detection from raw CSV** |

**User verdict:** The specific need — "drop a bank CSV in, get recurring expenses out, no accounts linked, no cloud" — is unserved by open-source tools. Commercial SaaS (Rocket Money, Monarch, Simplifi, YNAB) all require Plaid/Nordigen linking.

### 2. Academic Vocabulary (research literature)

| Search Term | Relevant Work | Gap |
|---|---|---|
| "recurring transaction detection" | ML-based approaches (KDD papers, ICAIF workshops) using supervised learning on labeled transaction data | **Requires training data; not deterministic/std-lib** |
| "subscription detection from transaction data" | Few papers; mostly proprietary bank-internal systems | **Not open source** |
| "financial transaction categorization machine learning" | Abundant (SWIFT, bank internal); uses NLM/transformers on merchant text | **Heavy ML, not stdlib, needs training** |
| "periodicity detection in transaction sequences" | Signal processing approaches (FFT, autocorrelation) on synthetic or proprietary data | **Not packaged as usable tool; no merchant normalization** |

**Academic verdict:** Mechanism (periodicity + amount consistency) is known in literature, but no open-source, deterministic, stdlib-only implementation exists. ML approaches dominate; they need training data and are not the same mechanism.

### 3. Infrastructure Vocabulary (existing tools and APIs)

| Tool / Platform | Recurring Detection? | Mode | Credentials Required? |
|---|---|---|---|
| **Plaid Transactions API** | Yes (`recurring` field) | Live API | Yes (paid, account linking) |
| **Nordigen / GoCardless** | Limited (bank-dependent) | Live API | Yes (account linking) |
| **Firefly III** | Manual rules only | Self-hosted PFM | No (but manual) |
| **Actual Budget** | Manual rules only | Local-first PFM | No (but manual) |
| **Beancount / hledger / Ledger** | Manual recurring entries | Plain-text accounting | No (but manual) |
| **GnuCash** | Scheduled transactions (manual) | Desktop app | No (but manual) |
| **MoneyManagerEx** | Recurring transactions (manual) | Desktop app | No (but manual) |
| **Homebank** | Recurring transactions (manual) | Desktop app | No (but manual) |
| **skrooge** | Recurring transactions (manual) | Desktop app | No (but manual) |
| **gnucash-python / piecash** | Programmatic access to manual entries | Library | No (but reads manual data) |
| **ofxtools / ofxstatement** | Parse OFX/QFX; no recurring detection | Parsers only | No |
| **csv2ofx / csv2qif** | Format conversion only | Converters | No |

**Infrastructure verdict:** No open-source, CSV-only, no-credentials, deterministic recurring expense detector exists. The Plaid `recurring` field is the only automated detector, but it requires live bank linking and paid subscription. All open-source PFMs require manual recurring transaction entry.

### Differentiation Summary for E065/E066

| Dimension | Our Approach | Incumbent Best |
|---|---|---|
| **Input** | Raw bank CSV (export) | Live API (Plaid) or manual entry |
| **Credentials** | None | Required (Plaid) or manual |
| **Deterministic** | Yes (stdlib only) | No (ML) or N/A (manual) |
| **Local-only** | Yes | No (cloud SaaS) |
| **Merchant normalization** | Token-based (stdlib) | Proprietary (Plaid) or manual |
| **Real data validation** | Berka (0.70 precision, 0.99 recall) | Not published for open tools |
| **License** | MIT (proposed) | Mixed (GPL, AGPL, proprietary) |

**The precise gap:** CSV-only, deterministic, no credentials, local-first, open-source recurring detection. This is a *different population* (privacy-conscious, export-only users) not served by Plaid-based tools.

---

## E067 — ArXiv Reproducibility: Environment Spec Generation from Partial Info

**Claim:** A tool that generates machine-runnable environment specifications (Dockerfile, conda `environment.yml`, pinned `requirements.txt`) FROM partial information (README install instructions, unpinned dependencies, import statements) for repositories that have NO working environment specification.

### 1. User Vocabulary

| Query / Need | Existing Solutions Found | Gap |
|---|---|---|
| "generate dockerfile from requirements.txt" | `dockerfile-generator` templates, `pip2docker` (abandoned), `dep2docker` (abandoned) | **Template-based; needs working env as input** |
| "generate requirements.txt from imports python" | `pipreqs`, `pigar`, `importanize`, `pydeps` — scan imports, output unpinned `requirements.txt` | **Outputs unpinned; doesn't resolve versions** |
| "create conda environment from README" | No tools found | **No tool reads README install instructions** |
| "reproduce arxiv paper environment automatically" | Manual process only; Binder/Code Ocean run existing specs | **No generator from partial info** |
| "pin dependencies from import statements" | `pip-tools`/`pip-compile` require working env + `setup.py`/`pyproject.toml` | **Needs working env to resolve** |

**User verdict:** Tools exist to *extract* imports (`pipreqs`, `pigar`) or *compile* lockfiles from working environments (`pip-tools`, `poetry`, `uv`, `conda-lock`). No tool generates a *runnable, pinned environment spec* from *partial information* (README + unpinned deps + imports) for a repo with no working environment.

### 2. Academic Vocabulary

| Search Term | Relevant Work | Gap |
|---|---|---|
| "computational reproducibility environment capture" | CDE (Computing Development Environment), ReproZip, CARE, SciUnit — capture *running* environments | **Capture from execution, not generate from source** |
| "software dependency resolution for reproducibility" | Spack, EasyBuild, Guix, Nix — build from source with full specs | **Require complete specs as input** |
| "environment specification inference" | Few papers (e.g., "Inferring Python Dependencies" ICSE'22) — ML to predict deps from imports | **Research prototypes; not maintained tools** |
| "Dockerfile generation from source code" | `dockerize` (abandoned), academic prototypes — heuristic-based | **Not maintained; don't handle version resolution** |

**Academic verdict:** The *problem* (reproducibility crisis, missing environment specs) is well-documented (Nature 2016, NeurIPS reproducibility checklist). The *solution* (generators from partial info) exists only as research prototypes, not maintained tools. Execution platforms (Binder, Code Ocean, Codespaces) run existing specs; they don't generate them.

### 3. Infrastructure Vocabulary

| Tool / Platform | Generates Specs? | From What Input? | Maintained? |
|---|---|---|---|
| **Binder / mybinder.org** | No — *runs* existing specs | `requirements.txt`, `environment.yml`, `Dockerfile`, `apt.txt` | Yes |
| **GitHub Codespaces** | No — *runs* devcontainer | `.devcontainer/devcontainer.json` + `Dockerfile` | Yes |
| **Code Ocean** | No — *runs* existing capsules | User-provided environment spec | Yes (commercial) |
| **pip-tools / pip-compile** | Yes — *lockfiles* | Working env + `setup.py`/`pyproject.toml`/`requirements.in` | Yes |
| **poetry lock** | Yes — *lockfiles* | Working env + `pyproject.toml` | Yes |
| **uv lock / uv pip compile** | Yes — *lockfiles* | Working env + `pyproject.toml`/`requirements.in` | Yes |
| **conda-lock** | Yes — *lockfiles* | Working env + `environment.yml` | Yes |
| **pipreqs / pigar** | Partial — unpinned `requirements.txt` | Import statements only | Low maintenance |
| **dep2docker / pip2docker** | Partial — Dockerfile template | `requirements.txt` | Abandoned (2018/2019) |
| **renv (R)** | Yes — lockfile | Working R environment | Yes |
| **repology.org** | Tracks versions | Package databases | Yes (service) |

**Infrastructure verdict:** All existing tools *require a working environment* to generate lockfiles or *run* existing specs. None generate a *runnable, pinned environment specification* from *partial information* (README + unpinned deps + imports) for a repository that has **no working environment at all**. This is the precise gap: spec generation from *incomplete* information.

### Differentiation Summary for E067

| Dimension | Proposed Generator | Incumbent Best |
|---|---|---|
| **Input** | README + unpinned deps + imports | Working environment + complete spec |
| **Output** | Pinned `requirements.txt` / `environment.yml` / `Dockerfile` | Lockfile (from working env) or runs existing |
| **Version resolution** | Heuristic (latest compatible, PyPI metadata) | Exact resolution (from working env) |
| **Non-Python deps** | Detect via `apt`/`brew` hints in README | Manual in Dockerfile |
| **Maintained tool** | None | `pip-tools`, `poetry`, `uv`, `conda-lock` (but need working env) |
| **Target population** | Repos with NO environment spec | Repos WITH environment spec |

**The precise gap:** Generate runnable environment specs FROM partial information FOR repositories that have no working environment. This is distinct from lockfile generation (which needs a working env) and execution platforms (which need an existing spec).

---

## Conclusion

Both domains pass the prior art check with clear, documented differentiation:

1. **E065/E066 (Recurring Expense Detection):** The mechanism is technically validated (synthetic + real Berka data). The differentiation is **CSV-only, no credentials, no API, fully local, deterministic, open-source**. This serves a different population than Plaid-based SaaS. No open-source tool occupies this niche.

2. **E067 (Environment Spec Generation):** The problem is real and severe (only 11.8% of code-linked ArXiv papers have runnable specs). The differentiation is **generation from partial info for repos with NO working environment** — all incumbents require a working environment or run existing specs. No maintained tool does this.

**Next steps per D083:**
- E065/E066: Test unmodified detector on real modern bank exports (Firefly III/Actual/beancount test fixtures, OFX samples) with predeclared gates; parallel read incumbents' import workflows for recurring detection (D077).
- E067: Build minimal spec generator (README + unpinned deps + imports → pinned requirements.txt/environment.yml/Dockerfile); test on E067's A2/A3/A4 repos where A1 ground truth exists. Kill gate: generated spec successfully installs/runs on ≥30% of test repos.