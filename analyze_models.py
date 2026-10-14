import json
import re

with open('/home/ubuntu/think-free/EXPERIMENTS/092-appliance-diagnosis/pool.jsonl') as f:
    rows = [json.loads(line) for line in f]

# Genuinely unanswered
gu = [r for r in rows if not r['is_answered'] and r['answer_count'] == 0 and r.get('accepted_answer_id') is None]

# Top 40 by view_count
top40 = sorted(gu, key=lambda r: r['view_count'], reverse=True)[:40]

# Extract model numbers
model_number_pattern = re.compile(r'[A-Z][A-Z0-9]{2,}[0-9]+[A-Z]?')

symptom_labels = ['not_spin', 'leaking', 'error_code', 'won_t_turn_on', 'overheating',
    'dispenser_slow', 'tripping_gfci', 'not_draining', 'making_noise']

symptom_patterns = {
    'not_spin': ['not spin', 'won\'t spin', 'not spinning', 'does not spin'],
    'leaking': ['leak', 'leaking', 'water on floor', 'pooling'],
    'error_code': ['error', 'E', 'F', 'code', 'DE', 'PF'],
    'won_t_turn_on': ["won't turn on", 'will not start', 'no power', 'dead'],
    'overheating': ['overheat', 'hot', 'burning smell'],
    'dispenser_slow': ['slow water', 'dispenser slow', 'water flow'],
    'tripping_gfci': ['tripping', 'gfci', 'gfi'],
    'not_draining': ['not drain', 'not draining', 'water left'],
    'making_noise': ['noise', 'rattling', 'banging', 'humming'],
}

model_counts = {}
symptom_hits = {k: 0 for k in symptom_labels}
model_to_symptom_hits = {}

for r in top40:
    body = r['body']
    title = r['title']
    text = title + ' ' + body

    # Find model numbers
    models = model_number_pattern.findall(text)
    plausible_models = []
    for m in models:
        if len(m) >= 4 and any(c.isalpha() for c in m) and any(c.isdigit() for c in m):
            plausible_models.append(m)

    first_model = plausible_models[0] if plausible_models else None

    if first_model:
        model_counts[first_model] = model_counts.get(first_model, 0) + 1
        if first_model not in model_to_symptom_hits:
            model_to_symptom_hits[first_model] = {s: 0 for s in symptom_labels}

    text_lower = text.lower()
    for sym, patterns in symptom_patterns.items():
        for p in patterns:
            if p.lower() in text_lower:
                symptom_hits[sym] = symptom_hits.get(sym, 0) + 1
                if first_model and sym in model_to_symptom_hits.get(first_model, {}):
                    model_to_symptom_hits[first_model][sym] += 1

print('Model counts in top 40:')
for m, c in sorted(model_counts.items(), key=lambda x: -x[1]):
    print(f'  {m}: {c}')

print('\nSymptom hit counts in top 40:')
for sym, c in sorted(symptom_hits.items(), key=lambda x: -x[1]):
    print(f'  {sym}: {c}')

print('\nModel-to-symptom associations:')
for m, syms in model_to_symptom_hits.items():
    total = sum(syms.values())
    print(f'  {m}: {syms} (total: {total})')