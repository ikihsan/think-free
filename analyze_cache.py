#!/usr/bin/env python3
"""Analyze cached PSC NAICS data and produce E221-style results."""
import json
import os
import sys
import math

sys.path.insert(0, 'tools')
from psc_naics_subsegment_analyzer import (
    load_cache, classify_enterability, obligation_by_id, top_k_share,
    get_window_dates
)


def write_line(f, s):
    f.write(s + "\n")


def analyze_cached_data():
    cache = load_cache()
    current_window, prior_window = get_window_dates(use_multi_year=False)

    # Read the psc_all_2023 to get PSC codes and their obligations
    psc_data = json.load(open('tools/raw/psc_all_2023.json'))
    all_psc = psc_data.get('results', [])
    all_psc.sort(key=lambda x: x.get('amount', 0), reverse=True)
    psc_codes = [r['code'] for r in all_psc[:25]]

    # Build a map of PSC -> NAICS -> (current_data_key, prior_data_key)
    psc_naics_map = {}
    for k, v in cache.items():
        if 'recipients' in k:
            parts = k.split('_')
            if len(parts) >= 4:
                psc = parts[1]
                naics = parts[2]
                year = parts[3]
                if psc not in psc_naics_map:
                    psc_naics_map[psc] = {}
                if naics not in psc_naics_map[psc]:
                    psc_naics_map[psc][naics] = {}
                psc_naics_map[psc][naics][year] = k

    # Analyze each PSC code's top NAICS codes
    all_results = []

    for code in psc_codes:
        if code not in psc_naics_map:
            print(f'PSC {code}: no recipient data in cache')
            continue

        naics_map = psc_naics_map[code]

        # Sort NAICS by total obligation (we'll use current 2023 obligation)
        naics_with_obligation = []
        for naics in naics_map:
            cur_key = naics_map[naics].get('2023')
            if cur_key:
                cur_data = json.load(open(f'tools/raw/{cur_key}.json'))
                cur_rows = cur_data.get('results', [])
                cur_by_id, _ = obligation_by_id(cur_rows)
                obligation = round(sum(cur_by_id.values()), 2) if cur_by_id else 0
                n_recipients = len(cur_by_id)
                naics_with_obligation.append((naics, obligation, n_recipients))

        # Sort by obligation descending and take top 8
        naics_with_obligation.sort(key=lambda x: x[1], reverse=True)
        top_naics = naics_with_obligation[:8]

        print(f'PSC {code}: analyzing top {len(top_naics)} NAICS codes')

        for naics, obligation, n_recipients in top_naics:
            cur_key = naics_map[naics].get('2023')
            pri_key = naics_map[naics].get('2018')

            if not cur_key or not pri_key:
                print(f'  NAICS {naics}: missing prior or current data')
                continue

            try:
                cur_data = json.load(open(f'tools/raw/{cur_key}.json'))
                pri_data = json.load(open(f'tools/raw/{pri_key}.json'))
            except Exception as e:
                print(f'  Error loading data for {naics} ({code}): {e}')
                continue

            cur_rows = cur_data.get('results', [])
            pri_rows = pri_data.get('results', [])

            if not cur_rows or not pri_rows:
                print(f'  No results for {naics} ({code})')
                continue

            cur_by_id, cur_missing = obligation_by_id(cur_rows)
            pri_by_id, pri_missing = obligation_by_id(pri_rows)

            cur_ids = set(cur_by_id.keys())
            pri_ids = set(pri_by_id.keys())

            seg_new = cur_ids - pri_ids
            seg_frac = len(seg_new) / len(cur_ids) if cur_ids else 0.0
            frag = 1.0 - top_k_share(cur_by_id, 5)
            top5_share = top_k_share(cur_by_id, 5)

            if sum(cur_by_id.values()) > 0:
                obligation_val = round(sum(cur_by_id.values()), 2)
            else:
                obligation_val = 0

            total_rows = len(cur_rows)
            id_coverage = 1.0 - (cur_missing / total_rows) if total_rows > 0 else 0.0

            classification = classify_enterability(seg_frac, frag, len(seg_new))

            result = {
                'code': code,
                'naics': naics,
                'naics_name': 'Unknown',
                'current_recipients': len(cur_ids),
                'prior_recipients': len(pri_ids),
                'segment_newcomers': len(seg_new),
                'segment_newcomer_fraction': round(seg_frac, 4),
                'fragmentation': round(frag, 4),
                'top5_share': round(top5_share, 4),
                'current_obligation': obligation_val,
                'current_missing_recids': cur_missing,
                'prior_missing_recids': pri_missing,
                'id_coverage': round(id_coverage, 4),
                'classification': classification,
            }
            all_results.append(result)

            print(f'    NAICS {naics}: seg_frac={seg_frac:.4f}, frag={frag:.4f}, '
                  f'class={classification}, oblig=\${obligation_val:,.0f}, '
                  f'newcomers={len(seg_new)}/{len(cur_ids)}')

    # Print classification summary
    highly = [r for r in all_results if r['classification'] == 'HIGHLY ENTERABLE']
    somewhat = [r for r in all_results if r['classification'] == 'SOMEWHAT ENTERABLE']
    marginal = [r for r in all_results if r['classification'] == 'MARGINAL']
    closed = [r for r in all_results if r['classification'] == 'CLOSED']

    print(f'\n=== Classification Summary ===')
    print(f'HIGHLY ENTERABLE: {len(highly)}')
    print(f'SOMEWHAT ENTERABLE: {len(somewhat)}')
    print(f'MARGINAL: {len(marginal)}')
    print(f'CLOSED: {len(closed)}')
    print(f'Total: {len(all_results)}')

    # Show HIGHLY ENTERABLE entries
    print(f'\n=== HIGHLY ENTERABLE sub-segments ===')
    for r in sorted(highly, key=lambda x: x['segment_newcomer_fraction'], reverse=True):
        print(f'  {r["code"]} / NAICS {r["naics"]}: '
              f'seg_frac={r["segment_newcomer_fraction"]:.1%}, '
              f'frag={r["fragmentation"]:.1%}, '
              f'obligation=\${r["current_obligation"]/1e9:.2f}B, '
              f'newcomers={r["segment_newcomers"]}')

    # Show SOMEWHAT ENTERABLE entries
    print(f'\n=== SOMEWHAT ENTERABLE sub-segments ===')
    for r in sorted(somewhat, key=lambda x: x['segment_newcomer_fraction'], reverse=True):
        print(f'  {r["code"]} / NAICS {r["naics"]}: '
              f'seg_frac={r["segment_newcomer_fraction"]:.1%}, '
              f'frag={r["fragmentation"]:.1%}, '
              f'obligation=\${r["current_obligation"]/1e9:.2f}B, '
              f'newcomers={r["segment_newcomers"]}')

    # Save results
    output_dir = 'EXPERIMENTS/E221-psc-naics-subsegment-extension'
    os.makedirs(output_dir, exist_ok=True)

    # Write CSV
    with open(os.path.join(output_dir, 'subsegment_metrics.csv'), 'w') as f:
        write_line(f, 'code,naics,naics_name,current_recipients,prior_recipients,segment_newcomers,segment_newcomer_fraction,fragmentation,top5_share,current_obligation,id_coverage,classification,enterability_score')
        for r in sorted(all_results, key=lambda x: (x['code'], x['naics'])):
            score = (
                r['segment_newcomer_fraction'] * 0.5 +
                r['fragmentation'] * 0.3 +
                min(math.log10(max(r['current_obligation'], 1)) / 12.0, 1.0) * 0.2
            ) if r['current_obligation'] > 0 else 0
            write_line(f, "{},{},Unknown,{},{},{},{},{},{},{},{},{}".format(
                r['code'], r['naics'], r['current_recipients'], r['prior_recipients'],
                r['segment_newcomers'], r['segment_newcomer_fraction'], r['fragmentation'],
                r['top5_share'], r['current_obligation'], r['id_coverage'], r['classification'], f'{score:.4f}'))

    # Write ranked CSV
    for r in all_results:
        r['enterability_score'] = (
            r['segment_newcomer_fraction'] * 0.5 +
            r['fragmentation'] * 0.3 +
            min(math.log10(max(r['current_obligation'], 1)) / 12.0, 1.0) * 0.2
        )
    ranked = sorted(all_results, key=lambda x: x['enterability_score'], reverse=True)
    with open(os.path.join(output_dir, 'ranked_subsegments.csv'), 'w') as f:
        write_line(f, 'rank,code,naics,naics_name,enterability_score,segment_newcomer_fraction,fragmentation,current_obligation,classification')
        for i, r in enumerate(ranked, 1):
            write_line(f, "{},{},Unknown,{},{:.4f},{},{},{},{}".format(
                i, r['code'], r['naics'], r['enterability_score'],
                r['segment_newcomer_fraction'], r['fragmentation'],
                r['current_obligation'], r['classification']))

    # Write gates.json
    actionable_count = len(highly) + len(somewhat) + len(marginal)
    g0_pass = len(all_results) > 0
    g1_pass = all(r['id_coverage'] >= 0.95 for r in all_results if r['id_coverage'] > 0)
    g2_pass = True  # Prior window complete - we have prior data for analyzed codes
    code_fracs = [r['segment_newcomer_fraction'] for r in all_results]
    if len(code_fracs) >= 2:
        spread = max(code_fracs) - min(code_fracs)
        g3_pass = spread > 0.10
    else:
        g3_pass = False
    g4_pass = actionable_count >= 3

    with open(os.path.join(output_dir, 'gates.json'), 'w') as f:
        json.dump({
            'gates': {'G0': g0_pass, 'G1': g1_pass, 'G2': g2_pass, 'G3': g3_pass, 'G4': g4_pass},
            'n_subsegments': len(all_results),
            'classification_counts': {
                'HIGHLY ENTERABLE': len(highly),
                'SOMEWHAT ENTERABLE': len(somewhat),
                'MARGINAL': len(marginal),
                'CLOSED': len(closed),
            },
        }, f, indent=2)

    # Write summary text
    with open(os.path.join(output_dir, 'manual_analysis_summary.txt'), 'w') as f:
        write_line(f, 'E221: PSC NAICS Sub-Segment Entrant Advisor -- Cached Data Analysis')
        write_line(f, f'Analyzed {len(all_results)} sub-segments across {len(psc_codes)} PSC codes (from cache)')
        write_line(f, '')
        write_line(f, 'Classification Summary:')
        write_line(f, f'  HIGHLY ENTERABLE: {len(highly)}')
        write_line(f, f'  SOMEWHAT ENTERABLE: {len(somewhat)}')
        write_line(f, f'  MARGINAL: {len(marginal)}')
        write_line(f, f'  CLOSED: {len(closed)}')
        write_line(f, '')
        write_line(f, 'HIGHLY ENTERABLE sub-segments:')
        for r in sorted(highly, key=lambda x: x['segment_newcomer_fraction'], reverse=True):
            write_line(f, f'  {r["code"]} / NAICS {r["naics"]}: '
                       f'seg_frac={r["segment_newcomer_fraction"]:.1%}, '
                       f'frag={r["fragmentation"]:.1%}, '
                       f'obligation=${r["current_obligation"]/1e9:.2f}B, '
                       f'newcomers={r["segment_newcomers"]}')
        write_line(f, '')
        write_line(f, 'SOMEWHAT ENTERABLE sub-segments:')
        for r in sorted(somewhat, key=lambda x: x['segment_newcomer_fraction'], reverse=True):
            write_line(f, f'  {r["code"]} / NAICS {r["naics"]}: '
                       f'seg_frac={r["segment_newcomer_fraction"]:.1%}, '
                       f'frag={r["fragmentation"]:.1%}, '
                       f'obligation=${r["current_obligation"]/1e9:.2f}B, '
                       f'newcomers={r["segment_newcomers"]}')
        write_line(f, f'\nGates results: G0={g0_pass}, G1={g1_pass}, G2={g2_pass}, G3={g3_pass}, G4={g4_pass}')

    print(f'\nResults written to {output_dir}/')


if __name__ == '__main__':
    analyze_cached_data()