# regvalue — Regulatory Value Verification Tool

A deterministic, standard-library-only tool that verifies whether values (money, dates, citations, percentages, quantities, numbers) in a regulatory summary/submission are grounded in the source regulatory text.

## Installation

No installation required. Standard library only (Python 3.8+).

```bash
# Run from repository root
python3 tools/regvalue/regvalue.py --help
```

## Usage

### Compare two local files

```bash
# Canonical mode (distinguishes money from bare numbers)
python3 tools/regvalue/regvalue.py reference.txt summary.txt

# Numeric mode (matches \$12,500,000 with 12500000 dollars)
python3 tools/regvalue/regvalue.py reference.txt summary.txt --mode numeric

# JSON output
python3 tools/regvalue/regvalue.py reference.txt summary.txt --json
```

### Fetch from Federal Register API

```bash
# Fetch a Federal Register document and verify its SUMMARY
python3 tools/regvalue/regvalue.py --fetch 2024-12345

# With numeric mode and JSON output
python3 tools/regvalue/regvalue.py --fetch 2024-12345 --mode numeric --json
```

## Comparison Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `canonical` (default) | Compares (kind, value) pairs — distinguishes money from num, date formats normalized | Strict verification; catches formatting differences |
| `numeric` | Compares only numeric values, ignoring kind and formatting | Lenient verification; catches value errors regardless of presentation |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All values grounded (match) |
| 1 | Ungrounded values found (mismatch) |
| 2 | Error (file not found, fetch failed, etc.) |

## Output Format

### Text (default)
```
Verdict: mismatch
Reference values: 42
Submission values: 38
Missing from submission (4):
  - ['money', '12500000.0']
  - ['date', '(2024, 1, 15)']
Extra in submission (2):
  - ['num', '1995.0']
```

### JSON (`--json`)
```json
{
  "verdict": "mismatch",
  "n_reference": 42,
  "n_submission": 38,
  "missing": [["money", "12500000.0"], ["date", "(2024, 1, 15)"]],
  "extra": [["num", "1995.0"]]
}
```

## Value Types Extracted

| Kind | Examples | Canonical Form |
|------|----------|----------------|
| `money` | `$12,500,000`, `$5 million`, `$2.5 billion` | `("money", 12500000.0)` |
| `date` | `January 15, 2024`, `Jan 15, 2024`, `1/15/2024` | `("date", (2024, 1, 15))` |
| `code` | `10 CFR 52.63(a)`, `42 U.S.C. 1395`, `91 FR 52593` | `("code", "10cfr5263(a)")` |
| `pct` | `5.5%`, `3 percent` | `("pct", 5.5)` |
| `qty` | `100 lbs`, `50 kg`, `30 days` | `("qty", 100.0)` |
| `num` | `123`, `1,234.56` | `("num", 123.0)` |

## Testing

```bash
# Run regvalue tests
PYTHONPATH=tools:tests python3 -m unittest tools.regvalue.test_regvalue -v
```

## Evidence Base

This tool implements the M2 deterministic canonicalizer from the Think Free mission's experiment E140/E142:

- **E140**: 0 false positives in 929 values against model-written expert answers on Federal Register rules
- **E142**: 1.0 detection, 0.0 false positives, 0 misses, 0.90 resolved share on 20 Federal Register SUMMARY sections written by agencies
- **E143**: The pre-pass does NOT maintain exactness on SUPPLEMENTARY INFORMATION sections (explanatory text, not summary genre) — 100% condemn rate due to genre mismatch, not instrument failure

**Key finding**: The instrument is exact on the **summary genre** (short texts asserting values drawn from a source document) but not on explanatory regulatory text or encyclopedic QA.

## Limitations

- **Genre-limited**: Works on Federal Register SUMMARY sections (agency-written summaries of rules). Does not work on SUPPLEMENTARY INFORMATION (explanatory text), encyclopedic QA (SQuAD), or general prose.
- **Binding blind spot**: Does not verify *what* a value is about (binding). A value may be present in the source but attributed to the wrong rule/provision.
- **Century/decade forms**: Does not extract `19th`, `1980s`, `1100s` — the `\b\d` pattern requires a digit boundary.
- **Canonical money key collision**: `canonical()` keys by `(kind, number)`, so `$12,500,000` and `12500000 dollars` are different keys in canonical mode (but match in numeric mode).

## Prior Art

Before claiming novelty, run a prior-art check on:
- Regulatory compliance verification tools
- XBRL/financial statement validation
- SEC filing verification tools
- Legal citation checkers

## License

Part of the Think Free repository. See root LICENSE.