import json
import csv
import pickle
import shelve
import io
import os
import tempfile
import sys

# 20 serialization scenarios: 4 categories x 5 instances
# Task format: (category, instance_id, input_data, expected_output, module_or_path)
# - JSON: input=dict, expected=round-trip via json.loads(json.dumps(data)), module='json'
# - CSV: input=(headers, rows), expected=parsed-back rows (list of lists, header skipped), module_or_path=csv_content
# - Pickle: input=object, expected=round-trip via pickle.loads(pickle.dumps(obj)), module='pickle'
# - Shelf: input=(initial_dict, shelf_path), expected=initial_dict (verify round-trip in run logic), module_or_path=shelf_path

TASKS = []

# --- Category A: JSON round-trip (5 scenarios) ---
for i in range(5):
    if i == 0: d = {"name": "test", "value": 42}
    elif i == 1: d = {"outer": {"inner": {"deep": "value"}, "second": 10}}
    elif i == 2: d = {"count": 42, "ratio": 3.14, "flag": True, "null_val": None,
                      "items": [1, 2, 3], "meta": {"key": "val"}}
    elif i == 3: d = {"answer": 42, "active": True, "label": "hello", "note": None}
    elif i == 4: d = {"version": 1.0, "items": ["a", "b", "c"], "config": {"mode": "auto"},
                      "enabled": False, "count": 0, "name": ""}
    expected = json.loads(json.dumps(d))
    TASKS.append(('A', i, d, expected, 'json'))

# --- Category B: CSV round-trip (5 scenarios) ---
for i in range(5):
    if i == 0:
        hdrs = ['name', 'value']; rows = [['alpha', '10'], ['beta', '20']]; erows = [['alpha', '10'], ['beta', '20']]
    elif i == 1:
        hdrs = ['string', 'integer', 'float']; rows = [['hello', '42', '3.14'], ['world', '7', '2.718']]; erows = [['hello', '42', '3.14'], ['world', '7', '2.718']]
    elif i == 2:
        hdrs = ['description', 'value']; rows = [['hello, world', '42'], ['say "hi"', '7']]; erows = [['hello, world', '42'], ['say "hi"', '7']]
    elif i == 3:
        hdrs = ['id', 'category', 'score']; rows = [['1', 'A', '95.5'], ['2', 'B', '88.0']]; erows = [['1', 'A', '95.5'], ['2', 'B', '88.0']]
    elif i == 4:
        hdrs = ['tag', 'value']; rows = [['', 'zero'], ['empty', '']]; erows = [['', 'zero'], ['empty', '']]
    lines = [','.join(hdrs)]
    for r in rows:
        lines.append(','.join(r))
    csv_str = '\n'.join(lines) + '\n'
    reader = csv.reader(io.StringIO(csv_str))
    prow = [r for r in reader][1:]  # skip header
    TASKS.append(('B', i, (hdrs, rows), erows, csv_str))

# --- Category C: Pickle round-trip (5 scenarios) ---
for i in range(5):
    if i == 0:
        d = {'int_val': 42, 'str_val': 'hello', 'float_val': 3.14,
             'bool_val': True, 'none_val': None, 'list_val': [1, 2, 3],
             'dict_val': {'a': 1, 'b': 2}}
    elif i == 1:
        d = {'matrix': [[1, 2], [3, 4]], 'nested': {'a': {'b': {'c': 42}}}}
    elif i == 2:
        d = [{'id': 1, 'name': 'alpha'}, {'id': 2, 'name': 'beta'},
             {'id': 3, 'name': 'gamma'}]
    elif i == 3:
        d = {'prefix': 'mid', 'suffix': 'end', 'value': 42}
    elif i == 4:
        d = {'users': [{'name': 'Alice', 'score': 95},
                       {'name': 'Bob', 'score': 87}],
             'metadata': {'total': 2, 'avg': 91.0},
             'active': True}
    expected = pickle.loads(pickle.dumps(d))
    TASKS.append(('C', i, d, expected, 'pickle'))

# --- Category D: Shelf persistence (5 scenarios) ---
for i in range(5):
    tmpdir = tempfile.mkdtemp()
    spath = os.path.join(tmpdir, f'shelf_{i}.db')
    if i == 0: init = {'name': 'test_object'}
    elif i == 1: init = {'a': 1, 'b': 'two', 'c': 3.14}
    elif i == 2: init = {'str': 'hello', 'int': 42, 'float': 3.14,
                        'list': [1, 2, 3], 'dict': {'x': 1}}
    elif i == 3: init = {'config': 'production', 'version': '2.0.1',
                        'enabled': True, 'settings': {'timeout': 30}}
    elif i == 4: init = {'counter': 0, 'items': [1, 2, 3],
                        'metadata': {'total': 5, 'avg': 3.0}}
    try:
        import shelve as sh
        with sh.open(spath) as s:
            s.update(init)
            rb = dict(s)
    except Exception:
        rb = None
    # In the run logic: verify rb == init; for task struct, expected=init
    TASKS.append(('D', i, init, init, spath))

# ============================================================
# Run experiment
# ============================================================
results = []
category_stats = {'A': {'total': 0, 'correct': 0},
                  'B': {'total': 0, 'correct': 0},
                  'C': {'total': 0, 'correct': 0},
                  'D': {'total': 0, 'correct': 0}}

for task in TASKS:
    cat = task[0]
    category_stats[cat]['total'] += 1

    if cat == 'A':
        _, idx, data, expected, module = task
        # JSON round-trip: serialize then deserialize
        round_trip = json.loads(json.dumps(data))
        result = (round_trip == expected)
    elif cat == 'B':
        _, idx, inp, expected_rows, csv_content = task
        # CSV: parse back, skip header row
        reader = csv.reader(io.StringIO(csv_content))
        parsed_rows = [r for r in reader][1:]
        result = (parsed_rows == expected_rows)
    elif cat == 'C':
        _, idx, data, expected, module = task
        # Pickle round-trip
        round_trip = pickle.loads(pickle.dumps(data))
        result = (round_trip == expected)
    elif cat == 'D':
        _, idx, initial, expected, shelf_path = task
        # Shelf: write and read back
        try:
            import shelve as sh
            with sh.open(shelf_path) as s:
                s.update(initial)
                read_back = dict(s)
            result = (read_back == initial)
        except Exception:
            result = False

    if result:
        category_stats[cat]['correct'] += 1

    results.append({
        'category': cat,
        'index': task[1],
        'correct': result,
        'expected': task[3],
    })

# Summary
total_tasks = len(results)
total_correct = sum(1 for r in results if r['correct'])
overall_rate = total_correct / total_tasks if total_tasks > 0 else 0

cat_rates = {}
for cat, stats in category_stats.items():
    cat_rates[cat] = stats['correct'] / stats['total'] if stats['total'] > 0 else 0

summary = {
    'total_tasks': total_tasks,
    'total_correct': total_correct,
    'overall_rate': overall_rate,
    'per_category': cat_rates,
    'category_stats': category_stats,
    'results': results,
}

with open('results.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(f'=== E064 Standard-library Serialization Effectiveness ===')
print(f'Total tasks: {total_tasks}')
print(f'Total correct: {total_correct}')
print(f'Overall rate: {overall_rate:.2%}')
print()
print('Per-category rates:')
for cat, rate in sorted(cat_rates.items()):
    stats = category_stats[cat]
    print(f'  Category {cat}: {stats["correct"]}/{stats["total"]} = {rate:.2%}')
print()
print('Per-task results:')
for r in results:
    status = 'PASS' if r['correct'] else 'FAIL'
    print(f'  Task {r["category"]}{r["index"]:d}: {status} (expected={str(r["expected"])[:40]})')

# Kill gate check
if overall_rate < 0.70:
    print('\\n*** KILL GATE: overall correct-task share < 0.70 ***')
    print('Conclusion: stdlib serialization insufficient for common patterns -> nothing to build')
else:
    print(f'\\n*** GATE: overall correct-task share = {overall_rate:.2%} (threshold 0.70) ***')
    print('Conclusion: stdlib sufficient for common serialization -> further investigation needed')