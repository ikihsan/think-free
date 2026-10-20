<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# preflight — three checks on the instrument that produces an evaluation rate

`observed` 2026-10-13, Python 3.8.10, `instance-20260717-0947`.

The mission lost three results in three days to defects in the *harness* that
produced the number (F118, F121, F122). None raised, none turned a declared
gate red. This builds the check that would have caught them, and measures it
against the harnesses that failed.

| file | what it is |
|---|---|
| [`PROTOCOL.md`](PROTOCOL.md) | pre-declared before any code: the question, the three checks, five cases, four gates, the baseline. Committed ahead of `run.py`. |
| [`AMENDMENT-1.md`](AMENDMENT-1.md) | written after the first run, before the added case was written: the declared easy arm fired, and why that is a result rather than a bug to patch. |
| [`RESULT.md`](RESULT.md) | the run, the gate accounting including the failure, and what changed as a build decision. |
| [`PRIOR-ART.md`](PRIOR-ART.md) | what already exists for each of the three checks. Verdict `partially-covered`: no tool does all three, none does C3, and the closest practitioner document already names two of the three in prose. |
| [`results.json`](results.json) | raw output: six cases, each with every measurement behind its verdict. |
| [`preflight/`](preflight) | the tool. 4 modules, standard library only, no model calls, no domain knowledge. |
| [`test_preflight.py`](test_preflight.py) | 16 tests, all passing. Four are injected defects on a sound fixture; the rest try to make the tool say `OK` when it should not. |
| [`adapters/`](adapters) | built-in adapters for JSONL, CSV, YAML, and XML harness formats. |

## Run it

```bash
cd EXPERIMENTS/124-eval-harness-preflight
python3 -m unittest discover -s tests  # 16 tests, all passing
python3 run.py                            # the six committed cases
```

## Use it as a Python package

```python
from preflight import concordance, alternate_form_fp, control_arm, render

checks = [
    concordance(key_rows, output_rows),                      # C1: join concordance
    alternate_form_fp(control_items, flagger, fp_ceiling=0.02),  # C2: alternate-form FP
    control_arm(control_rows, is_positive, premise=0.0),     # C3: control arm
]
text, code = render(checks, rate=recall)   # code 3 and the rate withheld
```

Exit code **3** means an instrument check failed and the rate is withheld.
Pass `--anyway` to print the number *and* say the checks failed, so a caller
who wants an unvouched rate has to ask for it.

## Adapters — transform harness output into `key_rows`/`out_rows`

The preflight instrument needs its inputs as `key_rows` (list of `{"id": "..."}`)
and `out_rows` (list of `{"id": "...", "prediction": "...", "answer": "..."}`).
Adapters read a harness's output file and produce these two lists. The **adapter
tax** is 3-4 lines of stdlib Python per format.

### Built-in adapters

| Format | Import | Adapter tax |
|---|---|---|
| **JSONL** (one JSON object per line) | `from preflight.adapters.jsonl_adapter import adapt_jsonl` | 4 lines |
| **CSV** (header `id,prediction,answer`) | `from preflight.adapters.csv_adapter import adapt_csv` | 3 lines |
| **YAML** (mapping with `id`, `prediction`, `answer` keys) | `from preflight.adapters.yaml_adapter import adapt_yaml` | 3 lines |
| **XML** (`<row id="..."><prediction>...</prediction><answer>...</answer></row>`) | `from preflight.adapters.xml_adapter import adapt_xml` | 3 lines |

### JSONL adapter

```python
from preflight.adapters.jsonl_adapter import adapt_jsonl

key_rows, out_rows = adapt_jsonl("output.jsonl")
```

### CSV adapter

```python
from preflight.adapters.csv_adapter import adapt_csv

key_rows, out_rows = adapt_csv("output.csv")
```

### YAML adapter

```python
from preflight.adapters.yaml_adapter import adapt_yaml

key_rows, out_rows = adapt_yaml("output.yaml")
```

### XML adapter

```python
from preflight.adapters.xml_adapter import adapt_xml

key_rows, out_rows = adapt_xml("output.xml")
```

## Full workflow example

```python
from preflight import concordance, alternate_form_fp, control_arm, render
from preflight.adapters.jsonl_adapter import adapt_jsonl

# Read a JSONL harness output and produce key_rows/out_rows
key_rows, out_rows = adapt_jsonl("harness_output.jsonl")

# Run the three checks
checks = [
    concordance(key_rows, out_rows),                              # C1
    alternate_form_fp([{"arm": "a", "value": "1000", "correct": True}],
                      lambda i: "grounded" if i["value"] in ("1000",) else "ungrounded_value",  # C2
    control_arm([{"id": "a", "evidence": "daily"}}, lambda r: "monthly" in r.get("evidence", "")),  # C3
]

# Render the report; exit code 3 means a check failed
text, code = render(checks, rate="recall 0.95")
print(text)
# Exit with the code: 0 if all OK, 3 if any check failed
```

## Limits and caveats

- **Population limitation (E125):** Only 5 of 22 popular LLM-eval harnesses had
  qualified committed key/output pairs. The tool is most useful as stdlib-only
  instrumentation for evaluation harness authors willing to write a small adapter
  for their specific format.
- **No external dependencies:** The package requires only Python standard library.
- **Two harnesses from one repository:** K1–K4 establish that the checks fire on
  five committed cases and on four injected defects, and that they stay quiet on
  a sound fixture. They establish nothing about any harness outside this
  repository.
- **False-positive rate is arm-specific:** C2 must be run on host text of the kind
  the instrument will actually be pointed at, and the arms must be reported
  separately. A single aggregate false-positive rate is a statement about the
  arms, not about the verifier.

## License

MIT. See the `LICENSE` file in the root of this repository.