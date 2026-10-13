# preflight — Three checks on the instrument that produces an evaluation rate

**preflight** validates LLM evaluation harnesses before you trust their numbers.

Every evaluation harness prints a rate: accuracy, F1, pass@k. But the harness
itself is an instrument, and instruments can be miscalibrated. preflight runs
three checks on the harness's own output and **withholds the rate** when the
instrument is unsound.

```
$ preflight jsonl ./harness_output/
C1_concordance            OK                       100/100 outputs matched
C2_alternate_form_fp      OK                       worst FP lower bound 0.0000 ≤ 0.02
C3_control_arm            OK                       0/5 positives in control arm
preflight: all 3 instrument checks OK
```

If a check fails, the rate is **withheld** (exit code 3):

```
$ preflight jsonl ./bad_harness/
C1_concordance            SILENT_NO_MATCH          50 key rows and 50 output rows, and no pairing matches
C2_alternate_form_fp      ALTERNATE_FORM_FP        the flagger condemns correct items beyond the declared ceiling (Wilson lower bound > 0.02) on arm(s): in_situ
C3_control_arm            CONTROL_NOT_EMPTY        3 of 5 rows in the declared negative arm carry a true positive (Wilson lower bound 0.2771 > premise 0.0000)
WITHHELD: preflight not reported. 3 of 3 instrument checks failed.
  - C1_concordance: SILENT_NO_MATCH -- 50 key rows and 50 output rows...
  - C2_alternate_form_fp: ALTERNATE_FORM_FP -- the flagger condemns correct items...
  - C3_control_arm: CONTROL_NOT_EMPTY -- 3 of 5 rows in the declared negative arm...

Run the checks against your own instrument, or pass --anyway to print a number this tool does not stand behind.
```

## Why preflight?

The mission behind preflight measured its own harnesses and found:
- **F121**: A scorer joined on `account_id` (integer) against answers keyed `"R001"` (string) — matched nothing, printed `recall=0.0000` for a reader that answered every item correctly.
- **F122**: A control arm declared "no positives" actually contained standing orders — every reader scored identically on it, so the gate could not separate subjects.
- **F118**: A verifier's controls used verbatim and corrupted strings, but the real task was faithful paraphrase — the verifier condemned 24 of 24 correct paraphrases (false-positive rate 1.00).

These defects were **in the harness**, not the model. The harness's own gates were green. preflight catches them.

## The three checks

| Check | What it catches | What you supply |
|-------|-----------------|-----------------|
| **C1: concordance** | Key and output identifiers don't join (F121) | `key_rows`, `out_rows` — both must share at least one field name |
| **C2: alternate-form FP** | Verifier condemns correct output written differently (F118) | `items` with `value` and independent `correct` label, plus a `flagger` function |
| **C3: control arm** | Declared negative arm actually contains positives (F122) | `rows` with `evidence` and an `is_positive` predicate that reads outside the key |

## Adapters: the tax is small

preflight doesn't know your harness's output format. You supply an **adapter** — a few lines of Python that transforms your harness output into the four structures preflight expects.

**Built-in adapters** (stdlib-only, 8–38 lines):
- `jsonl` — per-task JSON files (E130)
- `csv` — CSV with columns `sample_id, model_output, expected, correct` (E131)
- `yaml` — YAML list of entries (E132, requires `pip install pyyaml`)
- `xml` — XML with `<entry>` elements (E133)

**Custom adapter** — write a Python module exporting `adapt(harness_dir)`:

```python
# my_adapter.py
import json, os

def adapt(harness_dir):
    key_rows, out_rows, items, rows = [], [], [], []
    for filename in sorted(os.listdir(harness_dir)):
        if not filename.endswith(".jsonl"):
            continue
        with open(os.path.join(harness_dir, filename)) as f:
            for line in f:
                data = json.loads(line)
        # ... transform to preflight format ...
    return key_rows, out_rows, items, rows
```

Then run:
```bash
preflight my_adapter.py ./harness_output/
```

## Real harnesses tested

| Harness | Output structure | Adapter size |
|---------|------------------|--------------|
| `modelscope/evalscope` | Two files (predictions + reviews), joined by `index` | ~8 lines |
| `openai/evals` | Single append-only event stream, filter for `"match"`, join by `sample_id` | ~10 lines |
| Per-task JSON (E130) | One JSON file per task | 12 lines |
| CSV (E131) | Single CSV file | 37 lines |
| YAML (E132) | Single YAML file | 35 lines |
| XML (E133) | Single XML file | 38 lines |

The pattern holds: **the adapter is a few lines of harness-specific code, not a loader library**.

## Installation

```bash
pip install preflight-eval
# Or with YAML support:
pip install preflight-eval[yaml]
```

## Usage

```bash
# Built-in adapter
preflight jsonl ./my_harness_output/
preflight csv ./my_harness_output/
preflight yaml ./my_harness_output/     # requires pyyaml
preflight xml ./my_harness_output/

# Custom adapter
preflight my_adapter.py ./my_harness_output/

# Override false-positive ceiling (default 0.02)
preflight jsonl ./harness/ --fp-ceiling=0.05

# Print rate even when checks fail (you take responsibility)
preflight jsonl ./harness/ --anyway
```

## Library usage

```python
from preflight import concordance, alternate_form_fp, control_arm, render
from preflight.adapters import get_builtin_adapter

# Using built-in adapter
adapt = get_builtin_adapter("jsonl")
key_rows, out_rows, items, rows = adapt("./harness_output/")

# Or custom adapter
from my_adapter import adapt
key_rows, out_rows, items, rows = adapt("./harness_output/")

checks = [
    concordance(key_rows, out_rows),
    alternate_form_fp(items, my_flagger, fp_ceiling=0.02),
    control_arm(rows, my_is_positive, premise=0.0),
]

text, code = render(checks, rate=my_recall, label="my_harness")
print(text)
# code == 0 → rate is trustworthy; code == 3 → rate withheld
```

## Known limitation: C2 false-positive rate is arm-specific

The C2 check measures false-positive rate **per arm**. A verifier may have a clean
"verbatim" arm (FP rate 0.0069) but a condemned "in_situ" arm (FP rate 0.9346).
The tool reports arms separately and fails if **any** arm exceeds the ceiling.

This is by design: **a false-positive rate belongs to an arm, not to an instrument,
and a quoted one does not transfer** (F123, D109). The ceiling applies per arm.

## License

MIT License — see [LICENSE](LICENSE).

## Origin

preflight was developed as part of the [Think Free](https://github.com/ikihsan/think-free) mission — an independent invention project seeking unusually useful open-source tools. The tool emerged from measuring the mission's own evaluation harnesses and finding they silently produced wrong numbers.

## Status

**Alpha** — the tool works on the mission's harnesses and six adapter formats.
Whether it serves a broader population is `untested`. The C2 arm-specific
false-positive rate behavior is a deliberate design choice, not a bug.