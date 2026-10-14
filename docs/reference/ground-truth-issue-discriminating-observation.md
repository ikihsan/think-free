# Ground Truth Issue: Discriminating-Observation Procedure Experiments

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

## Summary

**Both F141 and E142-improved discriminating-observation experiments measured against the wrong population.**

- **E092's 40-row sample** (which has grades/ground truth) is **100% answered questions** — 0 of 40 are genuinely unanswered.
- **F116's genuinely unanswered pool** (95 rows) has **NO grades/ground truth** — 0 of 95 have grades.
- Therefore, neither experiment actually tested on genuinely unanswered questions.

## Details

### E092 Sample (40 rows, has grades)
| Metric | Value |
|--------|-------|
| Total rows | 40 |
| Genuinely unanswered (is_answered=false, answer_count=0, no accepted_answer) | **0** |
| Answered (has answer or accepted answer) | 40 |

### F116 Genuinely Unanswered Pool (95 rows, no grades)
| Metric | Value |
|--------|-------|
| Total rows | 95 |
| Has grades in grades.jsonl | **0** |
| No ground truth available | 95 |

### Experiments Affected

| Experiment | Population Used | Ground Truth | Actually Tested |
|------------|-----------------|--------------|-----------------|
| F141 | E092 40-row sample | E092 grades | **Answered questions** |
| E142-improved | E092 40-row sample | E092 grades | **Answered questions** |

## Consequence

The discriminating-observation line **cannot be properly evaluated** without grading the 95 genuinely unanswered rows. The reported results (Wilson CI95 lower bound, served share, wrong-first-hypothesis rate) are measurements on **answered questions**, not the target population of genuinely unanswered questions.

## Options

1. **Grade the 95 genuinely unanswered rows** — requires human evaluation of thread resolutions
2. **Close the line as unevaluable** — without ground truth, no experiment can validate the procedure
3. **Use a different venue with graded genuinely unanswered questions** — e.g., Stack Overflow with accepted answers on unanswered questions

## Recommendation

Given the mission's evidence standards (never fabricate results, label claims accurately), **the discriminating-observation line should be closed as unevaluable** unless the 95 genuinely unanswered rows are graded. The F141 and E142-improved results should be re-labeled as measurements on *answered* questions, not *genuinely unanswered* questions.

## Evidence

- `EXPERIMENTS/092-appliance-diagnosis/pool.jsonl` — 707 total rows
- `EXPERIMENTS/092-appliance-diagnosis/grades.jsonl` — 40 rows (E092 sample)
- F116 correction: `/search/advanced?answered=false` returns answered questions; genuinely unanswered = 95 rows
- Verification: `python3 -c "import json; pool=[json.loads(l) for l in open('EXPERIMENTS/092-appliance-diagnosis/pool.jsonl')]; grades={g['qid'] for g in [json.loads(l) for l in open('EXPERIMENTS/092-appliance-diagnosis/grades.jsonl')]}; genuine=[r for r in pool if not r.get('is_answered') and r.get('answer_count',0)==0 and not r.get('accepted_answer_id')]; print(len(genuine), len([r for r in genuine if r['question_id'] in grades]))"` outputs `95 0`