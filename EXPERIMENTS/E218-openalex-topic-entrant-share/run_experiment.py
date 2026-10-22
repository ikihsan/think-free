#!/usr/bin/env python3
"""
E218: OpenAlex Research Topic Entrant Share
Fresh observation in academic research domain (D083)
Tests whether fragmented research topics admit more newcomer institutions.
"""

import json
import time
import csv
import random
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import urllib.request
import urllib.error

# Configuration
BASE_DIR = Path("/home/ubuntu/think-free/EXPERIMENTS/E218-openalex-topic-entrant-share")
RAW_DIR = BASE_DIR / "raw"
RESULTS_DIR = BASE_DIR / "results"
RAW_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# API settings
BASE_URL = "https://api.openalex.org"
REQUEST_DELAY = 0.1  # seconds between requests
MAX_WORKS_PER_YEAR = 200
BASELINE_YEARS = list(range(2018, 2023))  # 2018-2022
CURRENT_YEARS = [2023, 2024]
MIN_BASELINE_WORKS = 100
MIN_BASELINE_INSTITUTIONS = 10
TARGET_TOPICS = 50

# Gate thresholds
G1_MIN_TOPICS = 20
G2_MIN_CONCENTRATION_RANGE = 0.30
G3_RHO_THRESHOLD = 0.30
G3_PVALUE_THRESHOLD = 0.05
G4_MIN_COVERAGE = 0.90

session_log = []

def log(msg):
    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] {msg}"
    print(entry)
    session_log.append(entry)

def fetch_json(url):
    """Fetch JSON from URL with error handling and rate limiting."""
    time.sleep(REQUEST_DELAY)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'E218-openalex-experiment/1.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
            return data
    except urllib.error.HTTPError as e:
        log(f"HTTP Error {e.code} for {url}: {e.read().decode()}")
        raise
    except Exception as e:
        log(f"Error fetching {url}: {e}")
        raise

def fetch_all_pages(url, max_pages=None):
    """Fetch all pages from a paginated OpenAlex endpoint."""
    results = []
    page_url = url
    page_count = 0
    while page_url and (max_pages is None or page_count < max_pages):
        data = fetch_json(page_url)
        results.extend(data.get('results', []))
        page_url = data.get('meta', {}).get('next_page_url')
        page_count += 1
        if page_count % 10 == 0:
            log(f"  Fetched {page_count} pages, {len(results)} results so far")
    return results

def get_institutions_from_work(work):
    """Extract unique institution IDs from a work's authorships."""
    insts = set()
    for auth in work.get('authorships', []):
        for inst in auth.get('institutions', []):
            inst_id = inst.get('id')
            if inst_id:
                insts.add(inst_id)
    return insts

def fetch_topic_works(topic_id, years, max_per_year=MAX_WORKS_PER_YEAR):
    """Fetch works for a topic in given years, returning institution sets per year."""
    year_institutions = {}
    total_works = 0
    works_with_inst = 0
    
    for year in years:
        # Use 'authorships' in select to get full authorship data including institutions
        url = f"{BASE_URL}/works?filter=topics.id:{topic_id},publication_year:{year}&select=id,authorships,publication_year&per-page={max_per_year}"
        works = fetch_all_pages(url)
        year_inst = set()
        for work in works:
            total_works += 1
            insts = get_institutions_from_work(work)
            if insts:
                works_with_inst += 1
                year_inst.update(insts)
        year_institutions[year] = year_inst
        log(f"  Year {year}: {len(works)} works, {len(year_inst)} institutions")
    
    return year_institutions, total_works, works_with_inst

def compute_top5_share(institutions_counter, total_works):
    """Compute top-5 institution share of works."""
    if total_works == 0:
        return 0.0
    top5 = sum(count for _, count in institutions_counter.most_common(5))
    return top5 / total_works

def compute_hhi(institutions_counter, total_works):
    """Compute Herfindahl-Hirschman Index."""
    if total_works == 0:
        return 0.0
    hhi = sum((count / total_works) ** 2 for count in institutions_counter.values())
    return hhi

def main():
    log("=" * 60)
    log("E218: OpenAlex Research Topic Entrant Share")
    log("Starting experiment")
    log("=" * 60)
    
    # Step 1: Fetch candidate topics
    log("Fetching candidate topics (works_count > 500)...")
    topics_url = f"{BASE_URL}/topics?filter=works_count:>500&per-page=200"
    all_topics = fetch_all_pages(topics_url)
    log(f"Found {len(all_topics)} topics with works_count > 500")
    
    # Stratify by domain and field
    by_domain_field = defaultdict(list)
    for topic in all_topics:
        domain = topic.get('domain', {}).get('display_name', 'Unknown')
        field = topic.get('field', {}).get('display_name', 'Unknown')
        by_domain_field[(domain, field)].append(topic)
    
    log(f"Domains/fields: {len(by_domain_field)} combinations")
    for (domain, field), topics in by_domain_field.items():
        log(f"  {domain} / {field}: {len(topics)} topics")
    
    # Sample topics: up to 10 per domain/field, max 50 total
    sampled_topics = []
    for (domain, field), topics in by_domain_field.items():
        sample_size = min(10, len(topics))
        sampled = random.sample(topics, sample_size)
        sampled_topics.extend(sampled)
        if len(sampled_topics) >= TARGET_TOPICS:
            break
    
    sampled_topics = sampled_topics[:TARGET_TOPICS]
    log(f"Sampled {len(sampled_topics)} topics")
    
    # Save sampled topics
    with open(RAW_DIR / "topics_sample.json", 'w') as f:
        json.dump(sampled_topics, f, indent=2)
    
    # Step 2: Process each topic
    topic_metrics = []
    gate_results = {'G0': 'PENDING', 'G1': 'PENDING', 'G2': 'PENDING', 'G3': 'PENDING', 'G4': 'PENDING'}
    
    # G0: API accessible
    gate_results['G0'] = 'PASS'
    log("G0: PASS - API accessible")
    
    eligible_topics = []
    
    for i, topic in enumerate(sampled_topics):
        topic_id = topic['id'].split('/')[-1]  # e.g., T10941
        display_name = topic['display_name']
        domain = topic.get('domain', {}).get('display_name', 'Unknown')
        field = topic.get('field', {}).get('display_name', 'Unknown')
        
        log(f"\n[{i+1}/{len(sampled_topics)}] Processing {topic_id}: {display_name}")
        log(f"  Domain: {domain}, Field: {field}")
        
        try:
            # Fetch baseline period institutions
            log("  Fetching baseline period (2018-2022)...")
            baseline_year_insts, baseline_total_works, baseline_works_with_inst = fetch_topic_works(topic_id, BASELINE_YEARS)
            
            # Aggregate baseline institutions with work counts
            baseline_inst_counter = Counter()
            for year, insts in baseline_year_insts.items():
                for inst in insts:
                    baseline_inst_counter[inst] += 1
            
            baseline_institutions = set(baseline_inst_counter.keys())
            baseline_n_institutions = len(baseline_institutions)
            
            # Fetch current period institutions
            log("  Fetching current period (2023-2024)...")
            current_year_insts, current_total_works, current_works_with_inst = fetch_topic_works(topic_id, CURRENT_YEARS)
            
            current_inst_counter = Counter()
            for year, insts in current_year_insts.items():
                for inst in insts:
                    current_inst_counter[inst] += 1
            
            current_institutions = set(current_inst_counter.keys())
            current_n_institutions = len(current_institutions)
            
            # Compute metrics
            top5_share = compute_top5_share(baseline_inst_counter, baseline_total_works)
            hhi = compute_hhi(baseline_inst_counter, baseline_total_works)
            fragmentation = 1 - top5_share
            
            # Segment newcomers: institutions in current but not in baseline
            segment_newcomers = current_institutions - baseline_institutions
            n_newcomers = len(segment_newcomers)
            entrant_fraction = n_newcomers / current_n_institutions if current_n_institutions > 0 else 0.0
            
            # Coverage
            baseline_coverage = baseline_works_with_inst / baseline_total_works if baseline_total_works > 0 else 0
            current_coverage = current_works_with_inst / current_total_works if current_total_works > 0 else 0
            overall_coverage = (baseline_works_with_inst + current_works_with_inst) / (baseline_total_works + current_total_works) if (baseline_total_works + current_total_works) > 0 else 0
            
            log(f"  Baseline: {baseline_total_works} works, {baseline_n_institutions} institutions, top5_share={top5_share:.4f}, HHI={hhi:.4f}")
            log(f"  Current: {current_total_works} works, {current_n_institutions} institutions, newcomers={n_newcomers}, entrant_frac={entrant_fraction:.4f}")
            log(f"  Coverage: baseline={baseline_coverage:.2%}, current={current_coverage:.2%}, overall={overall_coverage:.2%}")
            
            # Check eligibility
            eligible = (baseline_total_works >= MIN_BASELINE_WORKS and 
                       baseline_n_institutions >= MIN_BASELINE_INSTITUTIONS)
            
            metrics = {
                'topic_id': topic_id,
                'display_name': display_name,
                'domain': domain,
                'field': field,
                'baseline_works': baseline_total_works,
                'baseline_institutions': baseline_n_institutions,
                'baseline_works_with_inst': baseline_works_with_inst,
                'baseline_coverage': baseline_coverage,
                'top5_share': top5_share,
                'hhi': hhi,
                'fragmentation': fragmentation,
                'current_works': current_total_works,
                'current_institutions': current_n_institutions,
                'current_works_with_inst': current_works_with_inst,
                'current_coverage': current_coverage,
                'segment_newcomers': n_newcomers,
                'entrant_fraction': entrant_fraction,
                'overall_coverage': overall_coverage,
                'eligible': eligible
            }
            
            topic_metrics.append(metrics)
            
            if eligible:
                eligible_topics.append(metrics)
            
            # Save raw data
            with open(RAW_DIR / f"topic_works_baseline_{topic_id}.jsonl", 'w') as f:
                for year, insts in baseline_year_insts.items():
                    for inst in insts:
                        f.write(json.dumps({'year': year, 'institution': inst}) + '\n')
            
            with open(RAW_DIR / f"topic_works_current_{topic_id}.jsonl", 'w') as f:
                for year, insts in current_year_insts.items():
                    for inst in insts:
                        f.write(json.dumps({'year': year, 'institution': inst}) + '\n')
            
        except Exception as e:
            log(f"  ERROR processing {topic_id}: {e}")
            topic_metrics.append({
                'topic_id': topic_id,
                'display_name': display_name,
                'domain': domain,
                'field': field,
                'error': str(e),
                'eligible': False
            })
    
    # Step 3: Evaluate gates
    log("\n" + "=" * 60)
    log("GATE EVALUATION")
    log("=" * 60)
    
    n_eligible = len(eligible_topics)
    log(f"G1: Eligible topics = {n_eligible} (threshold ≥ {G1_MIN_TOPICS})")
    gate_results['G1'] = 'PASS' if n_eligible >= G1_MIN_TOPICS else 'FAIL'
    log(f"  G1: {gate_results['G1']}")
    
    if n_eligible >= 2:
        fragmentations = [t['fragmentation'] for t in eligible_topics]
        entrant_fractions = [t['entrant_fraction'] for t in eligible_topics]
        top5_shares = [t['top5_share'] for t in eligible_topics]
        
        conc_range = max(top5_shares) - min(top5_shares)
        log(f"G2: Concentration range = {conc_range:.4f} (threshold ≥ {G2_MIN_CONCENTRATION_RANGE})")
        gate_results['G2'] = 'PASS' if conc_range >= G2_MIN_CONCENTRATION_RANGE else 'FAIL'
        log(f"  G2: {gate_results['G2']}")
        
        # G3: Spearman correlation
        try:
            from scipy import stats
            rho, p_value = stats.spearmanr(fragmentations, entrant_fractions, alternative='greater')
            log(f"G3: Spearman ρ = {rho:.4f}, one-sided p = {p_value:.4f}")
            log(f"  Threshold: ρ ≥ {G3_RHO_THRESHOLD}, p < {G3_PVALUE_THRESHOLD}")
            g3_pass = (rho >= G3_RHO_THRESHOLD) and (p_value < G3_PVALUE_THRESHOLD)
            gate_results['G3'] = 'PASS' if g3_pass else 'FAIL'
            log(f"  G3: {gate_results['G3']}")
        except ImportError:
            # Manual Spearman calculation if scipy not available
            log("  scipy not available, computing Spearman manually...")
            n = len(fragmentations)
            # Rank the data
            frag_ranks = {v: i+1 for i, v in enumerate(sorted(set(fragmentations)))}
            entr_ranks = {v: i+1 for i, v in enumerate(sorted(set(entrant_fractions)))}
            
            frag_rank_vals = [frag_ranks[v] for v in fragmentations]
            entr_rank_vals = [entr_ranks[v] for v in entrant_fractions]
            
            # Pearson correlation on ranks
            mean_frag = sum(frag_rank_vals) / n
            mean_entr = sum(entr_rank_vals) / n
            
            num = sum((f - mean_frag) * (e - mean_entr) for f, e in zip(frag_rank_vals, entr_rank_vals))
            den_frag = sum((f - mean_frag) ** 2 for f in frag_rank_vals)
            den_entr = sum((e - mean_entr) ** 2 for e in entr_rank_vals)
            
            if den_frag > 0 and den_entr > 0:
                rho = num / (den_frag * den_entr) ** 0.5
                # Approximate p-value using t-distribution
                t = rho * ((n - 2) / (1 - rho**2)) ** 0.5 if rho**2 < 1 else float('inf')
                # One-sided p-value approximation
                import math
                if t > 0:
                    # Very rough approximation for one-sided p
                    p_value = 0.5 * (1 + math.erf(-abs(t) / math.sqrt(2)))
                else:
                    p_value = 1.0
            else:
                rho = 0.0
                p_value = 1.0
            
            log(f"G3: Spearman ρ = {rho:.4f}, approx one-sided p = {p_value:.4f}")
            g3_pass = (rho >= G3_RHO_THRESHOLD) and (p_value < G3_PVALUE_THRESHOLD)
            gate_results['G3'] = 'PASS' if g3_pass else 'FAIL'
            log(f"  G3: {gate_results['G3']}")
        
        # G4: Coverage
        coverages = [t['overall_coverage'] for t in eligible_topics]
        avg_coverage = sum(coverages) / len(coverages)
        log(f"G4: Average institution coverage = {avg_coverage:.2%} (threshold ≥ {G4_MIN_COVERAGE:.0%})")
        gate_results['G4'] = 'PASS' if avg_coverage >= G4_MIN_COVERAGE else 'FAIL'
        log(f"  G4: {gate_results['G4']}")
    else:
        gate_results['G2'] = 'FAIL (insufficient eligible topics)'
        gate_results['G3'] = 'FAIL (insufficient eligible topics)'
        gate_results['G4'] = 'FAIL (insufficient eligible topics)'
        log(f"G2: {gate_results['G2']}")
        log(f"G3: {gate_results['G3']}")
        log(f"G4: {gate_results['G4']}")
    
    # Step 4: Save results
    log("\nSaving results...")
    
    # Metrics CSV
    with open(RESULTS_DIR / "metrics.csv", 'w', newline='') as f:
        if topic_metrics:
            fieldnames = list(topic_metrics[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(topic_metrics)
    
    # Correlation results
    corr_result = {
        'n_topics_total': len(sampled_topics),
        'n_eligible': n_eligible,
        'gates': gate_results,
        'eligible_topics': [
            {
                'topic_id': t['topic_id'],
                'display_name': t['display_name'],
                'domain': t['domain'],
                'field': t['field'],
                'fragmentation': t['fragmentation'],
                'entrant_fraction': t['entrant_fraction'],
                'top5_share': t['top5_share'],
                'baseline_institutions': t['baseline_institutions'],
                'current_institutions': t['current_institutions'],
                'segment_newcomers': t['segment_newcomers']
            }
            for t in eligible_topics
        ]
    }
    
    if n_eligible >= 2:
        corr_result['spearman_rho'] = float(rho)
        corr_result['p_value_one_sided'] = float(p_value)
        corr_result['concentration_range'] = float(conc_range)
        corr_result['avg_coverage'] = float(avg_coverage)
    
    with open(RESULTS_DIR / "correlation.json", 'w') as f:
        json.dump(corr_result, f, indent=2)
    
    # Session log
    with open(BASE_DIR / "session_log.log", 'w') as f:
        f.write('\n'.join(session_log))
    
    # Summary
    log("\n" + "=" * 60)
    log("EXPERIMENT COMPLETE")
    log("=" * 60)
    log(f"Total topics sampled: {len(sampled_topics)}")
    log(f"Eligible topics: {n_eligible}")
    log(f"Gates: G0={gate_results['G0']}, G1={gate_results['G1']}, G2={gate_results['G2']}, G3={gate_results['G3']}, G4={gate_results['G4']}")
    if n_eligible >= 2:
        log(f"Spearman ρ = {rho:.4f}, p = {p_value:.4f}")
    
    overall_pass = all(v == 'PASS' for v in gate_results.values() if v != 'PENDING')
    log(f"Overall: {'ALL GATES PASS' if overall_pass else 'SOME GATES FAIL'}")

if __name__ == "__main__":
    main()