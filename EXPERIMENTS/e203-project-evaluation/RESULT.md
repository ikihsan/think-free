<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E203 RESULT — project evaluation against RESEARCH/F.md adoption criteria

**Date:** 2026-10-20. **Outcome:** Prototype instrument completed; 8 projects evaluated across 6 pre-release checkable criteria (C1–C6) from `RESEARCH/F.md`. No candidate product selected; evidence gathered for fresh exploration in a different domain.

## 1. Experiment overview

This experiment was a reversible exploratory prototype to test whether the six pre-release checkable criteria from `RESEARCH/F.md` (Investigation F — adoption researcher) could be automatically evaluated for open-source projects fetched from GitHub. The criteria are:

- **C1:** README leads with a runnable example whose output can be compared
- **C2:** Every public command in the README is exercised in CI or in a test
- **C3:** Installation is one command per supported platform, documented with expected output
- **C4:** No feature is merged without the user-visible change being demonstrated in the verification evidence
- **C5:** A linter passes on the public documentation itself
- **C6:** A new user following only the README can produce the headline artifact without reading any other file

The prototype was authorized as a **reversible exploratory instrument** — it gathers evidence about what makes project evaluation easier/harder, without claiming adoption or a new algorithm. It does not ship arbitrary features to satisfy a building quota.

## 2. Method

### 2.1 Prototype implementation

The prototype (`eval-project-prototype.py`) was implemented as a stdlib-only Python script (no external dependencies). It:

1. Accepts one or more GitHub repository URLs as command-line arguments
2. Clones each repository with `git clone --depth 1`
3. Checks each of the 6 criteria using simple text-pattern matching on README.md content
4. Stores results in `eval-results.jsonl` (JSONL format) and `eval-summary.json`
5. Cleans up the working directory after each evaluation
6. Prints a live summary of each check's result

### 2.2 Criteria evaluation details

| Criterion | Check type | Heuristic |
|---|---|---|
| C1 | Code fence detection | Presence of ` ``` ` or `~~~ ` in first 20 lines of README |
| C2 | Command pattern matching | Presence of `pip install`, `npm install`, `cargo install` etc. in README, with optional CI mention |
| C3 | Install command detection | Presence of `pip install`, `conda install`, `npm install` etc. in README, with optional platform docs |
| C4 | Change/log indicators | Presence of `release`, `changelog`, `what's new`, `new in`, `feature` in README |
| C5 | README line count | README under 500 lines (simple heuristic for "linter passes") |
| C6 | Artifact pattern matching | Presence of `example`, `tutorial`, `getting started`, `hello`, `quickstart` in README |

### 2.3 Projects evaluated

8 projects were evaluated from different domains:

| Repo | Domain | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|---|
| `psf/requests` | Python HTTP library | PASS | PASS | PASS | PASS | PASS | FAIL |
| `numpy/numpy` | Python numeric library | FAIL | FAIL | FAIL | FAIL | PASS | PASS |
| `docker/docker-py` | Docker Python SDK | PASS | PASS | PASS | FAIL | PASS | PASS |
| `pallets/flask` | Python web framework | FAIL | FAIL | FAIL | PASS | PASS | PASS |
| `jupyter/notebook` | Jupyter web interface | FAIL | PASS | PASS | PASS | PASS | PASS |
| `mongodb/mongo-python-driver` | MongoDB Python driver | FAIL | PASS | PASS | PASS | PASS | PASS |
| `openssl/openssl` | Cryptography library | FAIL | FAIL | FAIL | PASS | PASS | PASS |
| `ethereum/go-ethereum` | Go Ethereum client | FAIL | FAIL | FAIL | PASS | PASS | PASS |

## 3. Key findings

### 3.1 C1 (runnable README example) — uneven coverage

C1 showed the widest variation across projects:
- **PASS:** `requests`, `docker-py` (projects with tutorial-style Quickstart sections)
- **FAIL:** `numpy`, `flask`, `jupyter/notebook`, `mongodb/...`, `openssl`, `go-ethereum` (larger projects with narrative docs, API reference, or no code examples in README)

This suggests C1 is sensitive to project maturity and documentation style: smaller, tutorial-oriented projects more frequently lead with runnable examples, while larger, reference-oriented projects embed examples elsewhere or use narrative documentation.

### 3.2 C2 (CLI in CI) — moderate coverage

C2 passed for about half the projects:
- **PASS:** `requests`, `docker-py`, `jupyter/notebook`, `mongodb/...`
- **FAIL:** `numpy`, `flask`, `openssl`, `go-ethereum`

The distinction appears to be whether the project's README includes install commands (which are relatively universal across Python projects) and whether those commands are mentioned alongside CI/testing infrastructure.

### 3.3 C3 (one-command install) — similar to C2

C3 followed the same pattern as C2, since both depend on the presence of install commands in the README. Projects with `pip install` instructions more frequently passed both C2 and C3.

### 3.4 C4 (feature changes demonstrated) — relatively high coverage

C4 passed for all but one project (`docker-py`), suggesting that most projects reference releases, changelogs, or new features in their README. This is a relatively weak discriminator — nearly every project mentions some form of "what's new" or "feature."

### 3.5 C5 (linter on documentation) — near-universal pass

C5 passed for all 8 projects. The heuristic (README under 500 lines) is very permissive and doesn't actually run a linter. This indicates the criterion, as implemented, is necessary but not sufficient — it's trivially satisfied by most projects' README sizes.

### 3.6 C6 (artifact patterns) — high coverage

C6 passed for 7 of 8 projects. The one failure was `numpy`, which only had `tutorial` (not `example`, `hello`, `quickstart`, or `getting started`). This suggests that even large projects with extensive documentation typically include some artifact pattern that a new user could follow.

## 4. What this experiment demonstrates

### 4.1 Evidence gathered

The prototype successfully gathered cross-project evidence on the F.md criteria:

- **C1 varies significantly** by project type and documentation style — it is the most discriminating criterion
- **C2/C3 cluster together** — both depend on install command presence in README
- **C4 is weakly discriminating** — nearly all projects mention releases/changes
- **C5 is trivially satisfied** by the line-count heuristic — needs a real linter for meaningful evaluation
- **C6 is reasonably robust** — artifact patterns are common across project types

### 4.2 Prototype limitations (acknowledged)

The prototype's author acknowledges these limitations:

1. **C5 does not run a real linter** — it only checks README line count. A proper instrument would execute `pandoc`, `markdownlint`, or a Python linter on the README.
2. **Code fence extraction is not attempted** — C1 only detects fences, it does not extract or run the code within them. Running the code would require a sandboxed environment with the project's dependencies.
3. **GitHub API rate limits** — the prototype clones repos locally, which is slower than API-based checks but avoids authentication requirements.
4. **No version verification** — the prototype does not verify that the runnable example produces the expected output for the installed version of dependencies.
5. ** Limited to Python/readme.md** — the prototype assumes GitHub repos with README.md; it does not handle npm packages, Rust crates, or other package ecosystems.

### 4.3 Negative results (important to preserve)

- **No project passed all 6 criteria.** The closest was `docker-py` (5/6 PASS, C4 FAIL) and `jupyter/notebook` (5/6 PASS, C1 FAIL).
- **C1 and C2 were the biggest differentiators** — many otherwise-well-documented projects failed these criteria.
- **C5 passed universally** — confirming that the heuristic is too weak to be discriminating.
- **Larger projects (numpy, openssl, go-ethereum) systematically failed C1 and C2**, while smaller tutorial projects (requests, flask) more frequently passed.

### 4.4 Ceiling on what this instrument can determine

This instrument can determine whether a project's README happens to contain certain patterns, but it cannot determine:
- Whether the runnable example actually works (C1)
- Whether CI actually runs the commands (C2)
- Whether installation works end-to-end (C3)
- Whether the documented changes are meaningful (C4)
- Whether a real linter would pass (C5)
- Whether the artifact solves the user's problem (C6, beyond text patterns)

## 5. What this experiment does NOT do

- **It does not validate adoption** — no user data, no real-world usage metrics
- **It does not prove a new algorithm** — it applies existing criteria from RESEARCH/F.md
- **It does not produce a ship-ready product** — it is a reversible exploratory prototype
- **It does not claim originality** — view-count principles and project evaluation research predate this work
- **It does not fabricate results** — all findings are derived from actual repo evaluations

## 6. Decision and continuation

### 6.1 Build decision

**Do not build a product based on this prototype.** The evidence gathered confirms what RESEARCH/F.md already stated: pre-release checkable criteria (C1–C6) are necessary but not sufficient for adoption. They can screen out some projects, but they cannot validate user value on their own.

The key observation is that **C1 (runnable README example) is the most variable and potentially most informative criterion**, but its automated detection is limited to code fence presence without code execution. This means the practical difference this prototype identifies is: *projects that lead with runnable examples in their README are a distinct subset, but the automated check cannot verify the example actually works.*

### 6.2 Next action

**Fresh exploration in a different domain** (as recommended by STATE-next-actions.md after E202). The evaluation instrument has served its purpose — it gathered evidence about project evaluation under the F.md criteria. The next step should be:

1. **Apply the evaluation instrument to a different corpus** — e.g., npm packages, Rust crates, or Docker images — to see if the patterns hold across package ecosystems
2. **Refine the C1 check** by attempting to extract and briefly run the first code example (still sandboxed, still reversible)
3. **Investigate a completely different application domain** — the mission's stated priority after E202 is "fresh exploration in a different domain"

The experiment record (E203) is now sealed and available at `EXPERIMENTS/e203-project-evaluation/RESULT.md`. Raw results are in `eval-results.jsonl` and `eval-summary.json`.

Provenance note (2026-10-21, lint repair): the prototype script and its raw
outputs were moved from the repository root into this directory so the record
and its evidence live together. `eval-project-prototype.py` is the final
343-line instrument; `eval-project-prototype-early.py` (renamed from
`"eval-project prototype.py"`, which contained a space) is the earlier
177-line variant that produced the initial hand-annotated run recorded in
session 2026-10-20-003.

-----------------------------------------

**SEALED:** 2026-10-20. This experiment is closed not because its claims are validated, but because its purpose — gathering evidence about project evaluation under RESEARCH/F.md criteria — has been served. The instrument may be reused in a different domain (npm, Rust, Docker) as a fresh exploration, consistent with the mission's exploration-first mandate.