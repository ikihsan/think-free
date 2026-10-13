<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-13
-->

# 124 — preflight checks on the instrument that produces an evaluation rate

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

## Run it

```
cd EXPERIMENTS/124-eval-harness-preflight
python3 run.py                      # the six cases; prints a report per case
python3 -m unittest test_preflight  # 16 tests
```

`run.py` reads only files already committed to this repository: E114's
`ground.py`, `checked.jsonl`, `flags-verified.jsonl` and `raw/text/`, and
E116's `key.jsonl` and `answers.jsonl`. It fetches nothing.

## Use it

```python
from preflight import concordance, alternate_form_fp, control_arm, render

checks = [
    concordance(key_rows, output_rows),                      # C1
    alternate_form_fp(control_items, flagger, fp_ceiling=0.02),  # C2
    control_arm(control_rows, is_positive, premise=0.0),     # C3
]
text, code = render(checks, rate=recall)   # code 3 and the rate withheld
```

Exit 3 means an instrument check failed and the rate is not printed. `--anyway`
in the CLI prints the number *and* says the checks failed, so a caller who wants
an unvouched rate has to say so.

## Limits, in one paragraph

Two harnesses from one repository, and fixtures built by the author to break it.
K1–K4 establish that the checks fire on five committed cases and on four
injected defects, and that they stay quiet on a sound fixture. They establish
nothing about any harness outside this repository, and no case here measures an
arm on which the E114 verifier is demonstrably sound (F123).