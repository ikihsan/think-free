<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# preflight — three checks on the instrument that produces an evaluation rate

`observed` 2026-10-13, Python 3.8.10.

This package validates LLM evaluation harnesses before you trust their numbers. It catches three structural failure modes that are invisible to a harness's own declared gates:

| check | measures | verdict that withholds the rate |
|---|---|---|
| **C1 concordance** | whether the key's identifiers and the output's identifiers name the same entities | `SILENT_NO_MATCH`, `NO_DISCRIMINATING_PAIRING` |
| **C2 alternate-form FP** | the rate at which a flagger condemns items known to be right, per arm | `ALTERNATE_FORM_FP` |
| **C3 control arm** | whether a declared negative arm is negative, by evidence the key does not use | `CONTROL_NOT_EMPTY` |

The tool exits **0** only when all three checks pass. Otherwise it exits **3** and withholds the headline rate. A caller who wants the number regardless must pass `--anyway`, which prints it *and says the instrument checks failed*.

## Install

```bash
pip install preflight
```

Or run directly from source (stdlib only, no dependencies):

```bash
python3 -m preflight harness_output.jsonl
```

Supported formats: `.jsonl`, `.csv`, `.yaml`/`.yml`, `.xml`

## Use it as a Python package

```python
from preflight import concordance, alternate_form_fp, control_arm, render
from preflight.adapters.jsonl_adapter import adapt_jsonl

# 1. Read harness output and produce key_rows/out_rows via an adapter
key_rows, out_rows = adapt_jsonl("harness_output.jsonl")

# 2. Run the three checks
checks = [
    concordance(key_rows, out_rows),                              # C1
    alternate_form_fp(control_items, flagger, fp_ceiling=0.02),  # C2
    control_arm(control_rows, is_positive, premise=0.0),         # C3
]

# 3. Render the report; exit code 3 means a check failed
text, code = render(checks, rate="recall 0.95")
print(text)
# Exit with the code: 0 if all OK, 3 if any check failed
```

## Adapters — transform harness output into `key_rows`/`out_rows`

The preflight instrument needs its inputs as:
- `key_rows`: list of `{"id": "..."}` dicts
- `out_rows`: list of `{"id": "...", "prediction": "...", "answer": "..."}` dicts

Adapters read a harness's output file and produce these two lists. The **adapter tax** is 3-4 lines of stdlib Python per format.

### Built-in adapters

| Format | Import | Adapter tax |
|---|---|---|
| **JSONL** (one JSON object per line) | `from preflight.adapters.jsonl_adapter import adapt_jsonl` | 4 lines |
| **CSV** (header `id,prediction,answer`) | `from preflight.adapters.csv_adapter import adapt_csv` | 3 lines |
| **YAML** (mapping with `id`, `prediction`, `answer` keys) | `from preflight.adapters.yaml_adapter import adapt_yaml` | 3 lines |
| **XML** (`<row id="..."><prediction>...</prediction><answer>...</answer></row>`) | `from preflight.adapters.xml_adapter import adapt_xml` | 3 lines |

### Custom adapters

For harnesses with different output structures (e.g., `modelscope/evalscope`, `openai/evals`), write a small adapter function that produces `key_rows` and `out_rows` in the expected shape. The adapter pattern is validated across 6 fundamentally different output structures.

## Run the tests

```bash
python3 -m unittest discover -s preflight  # 16 tests, all passing
```

The test suite includes:
- A sound fixture that passes all checks
- Four injected defects (key type flip, key field drop, verifier normalization removed, control arm contaminated)
- Falsification tests that try to make the tool say `OK` when it should not

## What this tool catches (from this repository's own harnesses)

| finding | the harness reported | what was true |
|---|---|---|
| **F118** | verifier recall 1.0000, false-alarm rate 0.0069, `instruments_valid: true` | it flagged 0.3717 of 374 values in correct answers; **false-positive rate 1.00 on its own flags** |
| **F121** | a scorer printing TP/FP/FN for 80 accounts | key held integer `account_id`, answers held `"R001"`; **every answer scored against nothing** |
| **F122** | `G0_C_precision = 0.0` — reader hallucinates | the gate's premise was false: 4 "control" accounts hold real standing orders outside the key's positive set, so **every reader, including the incumbent, scored 0.0** |

Each was a *silent* failure: no exception, a number printed, no gate red.

## Limits and caveats

- **Population limitation (E125):** Only 5 of 22 popular LLM-eval harnesses had qualified committed key/output pairs. The tool is most useful as stdlib-only instrumentation for evaluation harness authors willing to write a small adapter for their specific format.
- **No external dependencies:** The package requires only Python standard library.
- **Two harnesses from one repository:** K1–K4 establish that the checks fire on five committed cases and on four injected defects, and that they stay quiet on a sound fixture. They establish nothing about any harness outside this repository.
- **False-positive rate is arm-specific:** C2 must be run on host text of the kind the instrument will actually be pointed at, and the arms must be reported separately. A single aggregate false-positive rate is a statement about the arms, not about the verifier (F123).
- **K2 gate failed as declared:** The declared easy arm measured 0.9346 false-positive rate instead of the expected ≤0.02, because the verifier scores context-word overlap and a bare sentence naming a value present in the document still scores near zero. This is recorded as F123: a false-positive rate belongs to an arm, not to an instrument, and a quoted one does not transfer.

## Prior art

[`PRIOR-ART.md`](../EXPERIMENTS/124-eval-harness-preflight/PRIOR-ART.md) searched for all three checks. Verdict: **`partially-covered`**. No tool performs all three, none automates C3, and the closest practitioner document (Anthropic's "Demystifying evals for AI agents") already tells practitioners to author a reference solution that passes every grader (C2) and to build balanced problem sets (C3), in prose, by hand, with no measurement and no gate.

## Adoption interest evidence

[`EXPERIMENTS/preflight-adoption-interest.md`](../EXPERIMENTS/preflight-adoption-interest.md) documents observed adoption signals: open issues in `lm-evaluation-harness` and `stanford-crfm/helm` mapping to C1/C2/C3, real audits finding broken scoring (MLS-Bench #103), and a standardization effort (`evaleval/every_eval_ever`). The user population is niche (evaluation engineers, benchmark maintainers).

## License

MIT. See [`LICENSE`](LICENSE).