<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E072 — can a kill gate fail on missing files in git repos?

Session `2026-10-09-00x-experiment-git-file-presence`, declared 2026-10-09.

## The question

E070 demonstrated the kill gate protocol fix in the package-naming domain (PyPI JSON API), and E071 demonstrated the same fix in the configuration-validity domain (YAML config files). **Can the protocol fix generalize a third time, to a git-repository domain?** This experiment tests whether enumerating passing regions before the run, and having analyze.py read pre-existing bytes from disk, enables a kill gate to fail when git repos lack a required file.

## Background

E070 used the PyPI JSON API with a corpus of package names — some resolved to real packages (pass), some were nonexistent (fail). The kill gate had non-vacuous passing regions because some names resolved to real packages, enabling the gate to properly fail when no real packages were in the corpus.

E071 used YAML config files from disk — some had all required keys (pass), some were missing keys (fail). The kill gate had non-vacuous passing regions because some configs had content and all required keys, enabling the gate to properly fail when no configs had all keys.

E069's fatal defect was that the kill gate's passing region contained only vacuous cases (empty-name corner cases), so the gate could never fail. E070 and E071 fixed this by (a) enumerating passing regions before the run, and (b) having analyze.py read pre-existing bytes. This experiment asks whether Fix(a)(b) generalizes to a third domain: git repository file presence.

## Kill gate (G1)

**If the gate has no non-vacuous passing regions (i.e., all "pass" cases are empty/ambiguous corner cases), the gate cannot fail.** This gate is the question, not the verdict.

If every "pass" case in the declared passing region is a repo that trivially satisfies the requirements (or no repos are tested), the gate cannot fail and the experiment terminates.

## Passing-region enumeration (G2)

Before the run begins, the experiment must declare:

- **What counts as a "pass" case**: e.g., "a git repository at the specified path contains a FILE named `README.md` at its root"
- **What counts as a "fail" case**: e.g., "a git repository at the specified path that does not contain `README.md` at its root, or the path is not a valid git repository"
- **The exact input corpus**: a fixed, pre-existing set of git repository paths on disk for the run to evaluate

If the declared passing region contains only vacuous cases (e.g., empty repo paths, repos that exist but are not git repos, repos where the check is trivially satisfied regardless of content), the gate cannot fail.

## Search strategy (G3)

For each git repo path in the corpus:

1. **Read the repo path from disk** — a fixed path that already exists before the run starts
2. **Check if the repo contains the required file**: use `git ls-files` or check if the file exists at the repo root
3. **Record the outcome**: `pass` (file exists in repo), `fail` (file does not exist or path is not a valid git repo), or `error` (unreadable path)
4. **`analyze.py` reads from pre-existing files on disk** — not files it writes at runtime

All checks use git-local operations only; no network required beyond the local repo.

## Thresholds

- **G1 (gateability)**: the declared passing region must contain at least one non-vacuous case. If every "pass" case is an empty path, a non-git path, or a repo where the check is trivially satisfied regardless of content, the gate cannot fail and the experiment ends.
- **G2 (search executed)**: for each repo path in the corpus, check the repo and record the result
- **G3 (negative control)**: include at least one repo that does not have the required file — should register as "fail", verifying the instrument detects the absence

## Negative controls (G3)

- A repo path known to not contain the required file (e.g., a path to a directory that is not a git repo, or a git repo missing the file)
- This should register as "fail", verifying the instrument does not falsely pass repos lacking the file

## Resource limits

- Max 10 repo paths in the corpus
- Max 5 minutes wall time for checking all repos
- Repo paths are read from a fixed input directory on disk

## Oracle

Automated: `analyze.py` exit code 0 = gate passes, 1 = gate fails. No human review required for the gate verdict itself.

## Reproduce

```bash
cd EXPERIMENTS/072-git-file-presence
python3 search.py      # checks git repos for required file, writes raw/results.jsonl
python3 outcome.py     # computes G1, G2, G3 verdicts, writes results.json
```