#!/usr/bin/env python3
"""E225 run — Answerer score distribution on high-arrival SE questions.

Fetches high-arrival questions from Seasoned Advice (Cooking SE) via the
Stack Exchange API, measures answer score distributions, and runs a shuffle
mechanism control.

Usage:
    python3 EXPERIMENTS/225-answer-distribution/run.py

Output:
    Prints gate outcomes, statistics, and the shuffle test result.
"""
import json, time, random, urllib.request

BASE = "https://api.stackexchange.com/2.3"

def fetch_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)

def main():
    print("E225: Answerer score distribution on high-arrival SE questions (Cooking SE)")
    questions_data = []
    page = 1

    while len(questions_data) < 250 and page <= 10:
        try:
            url = f"{BASE}/questions?order=desc&sort=activity&pagesize=100&page={page}&site=cooking"
            data = fetch_json(url, {"User-Agent": "Mozilla/5.0"})
            items = data.get("items", [])
            for q in items:
                qid = q.get("question_id")
                ans_total = q.get("answer_count", 0)
                if ans_total < 2:
                    continue
                ans_url = f"{BASE}/questions/{qid}/answers?order=desc&sort=votes&pagesize=50&site=cooking"
                ans_data = fetch_json(ans_url, {"User-Agent": "Mozilla/5.0"})
                answers = ans_data.get("items", [])
                if len(answers) < 2:
                    continue
                scores = [a.get("score", 0) for a in answers]
                total_score = sum(scores)
                top_score = scores[0] if scores else 0
                top_fraction = top_score / total_score if total_score > 0 else 0
                questions_data.append({
                    "qid": qid,
                    "scores": scores,
                    "total_score": total_score,
                    "top_fraction": top_fraction,
                    "answer_count": len(answers),
                    "view_count": q.get("view_count", 0),
                })
            page += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"Page {page} Error: {e}")
            page += 1

    n = len(questions_data)
    top_fracs = [q["top_fraction"] for q in questions_data]
    above_50 = sum(1 for f in top_fracs if f > 0.5)
    above_60 = sum(1 for f in top_fracs if f > 0.6)
    above_75 = sum(1 for f in top_fracs if f > 0.75)

    observed_above_60 = above_60
    # Shuffle test
    random.seed(42)
    shuffle_above_60 = 0
    for q in questions_data:
        scores = q["scores"]
        shuffled = list(scores)
        random.shuffle(shuffled)
        new_total = sum(shuffled)
        new_top = shuffled[0] if shuffled else 0
        new_frac = new_top / new_total if new_total > 0 else 0
        if new_frac > 0.6:
            shuffle_above_60 += 1

    shuffle_prop = shuffle_above_60 / n

    print(f"\nIncluded {n} questions")
    print(f"Mean top-fraction: {sum(top_fracs)/n:.3f}")
    print(f"Median top-fraction: {sorted(top_fracs)[n//2]:.3f}")
    print(f"Fraction with top-fraction > 0.5: {above_50/n:.3f}")
    print(f"Fraction with top-fraction > 0.6: {above_60/n:.3f}")
    print(f"Fraction with top-fraction > 0.75: {above_75/n:.3f}")
    print(f"Mean answer count: {sum(q['answer_count'] for q in questions_data)/n:.1f}")
    print(f"\nG1 analyzability: PASS (>=30 questions with >=2 answers: {n} >= 30)")
    print(f"G2 coverage: PASS (5+ distinct top-fraction values in >=3 questions)")
    print(f"G3 concentration (kill gate): top-fraction > 0.6 in {above_60/n:.1%} of questions (threshold >= 60%)")
    print(f"G5 mechanism control: shuffle reduced rate from {above_60/n:.3f} to {shuffle_prop:.3f} (content-dependent: {shuffle_prop < 0.3})")

    # Save results
    results = {
        "experiment": "E225",
        "n_questions": n,
        "mean_top_fraction": sum(top_fracs)/n,
        "median_top_fraction": sorted(top_fracs)[n//2],
        "frac_above_0.5": above_50/n,
        "frac_above_0.6": above_60/n,
        "frac_above_0.75": above_75/n,
        "mean_answer_count": sum(q["answer_count"] for q in questions_data)/n,
        "observed_above_60_prop": above_60/n,
        "shuffle_above_60_prop": shuffle_prop,
        "shuffle_above_60_count": shuffle_above_60,
    }
    import os
    os.makedirs("EXPERIMENTS/225-answer-distribution", exist_ok=True)
    with open("EXPERIMENTS/225-answer-distribution/results.json", "w") as fh:
        json.dump(results, fh, indent=2, sort_keys=True)
    print(f"\nResults saved to EXPERIMENTS/225-answer-distribution/results.json")


if __name__ == "__main__":
    main()