#!/usr/bin/env python3
import urllib.request, json

# Explore NSF SBIR awards - get more
url = 'https://api.nsf.gov/services/v1/awards.json?keyword=SBIR&printFields=id,title,amount,awardeeName,startDate,expDate,estimatedTotalAmt,fundProgramName,awardeeStateCode,awardeeCity'
with urllib.request.urlopen(url) as r:
    data = json.load(r)
    awards = data.get('response', {}).get('award', [])
    print(f'Total awards returned: {len(awards)}')
    
    # Aggregate by awardee
    org_stats = {}
    for award in awards:
        name = award.get('awardeeName', 'Unknown')
        # Use estimatedTotalAmt if available, else amount
        amount = award.get('estimatedTotalAmt') or award.get('amount') or 0
        try:
            amount = float(amount)
        except:
            amount = 0
        if name not in org_stats:
            org_stats[name] = {'total': 0, 'count': 0}
        org_stats[name]['total'] += amount
        org_stats[name]['count'] += 1
    
    sorted_orgs = sorted(org_stats.items(), key=lambda x: x[1]['total'], reverse=True)
    total_amount = sum(s['total'] for s in org_stats.values())
    total_count = sum(s['count'] for s in org_stats.values())
    
    print(f'\nTotal amount: ${total_amount:,.0f}')
    print(f'Total awards: {total_count}')
    print(f'Distinct awardees: {len(org_stats)}')
    print(f'\nTop 20 awardees by total funding:')
    for i, (name, stats) in enumerate(sorted_orgs[:20]):
        share = stats['total'] / total_amount * 100 if total_amount else 0
        print(f'  {i+1}. {name}: ${stats["total"]:,.0f} ({stats["count"]} awards, {share:.1f}%)')
    
    top10_share = sum(s['total'] for _, s in sorted_orgs[:10]) / total_amount * 100 if total_amount else 0
    print(f'\nTop 10 share: {top10_share:.1f}%')
    if top10_share < 80:
        print('FRAGMENTED: Top 10 < 80%')
    else:
        print('CONCENTRATED: Top 10 >= 80%')
    
    # By program
    programs = {}
    for award in awards:
        prog = award.get('fundProgramName', 'Unknown')
        amount = award.get('estimatedTotalAmt') or award.get('amount') or 0
        try:
            amount = float(amount)
        except:
            amount = 0
        if prog not in programs:
            programs[prog] = {'total': 0, 'count': 0}
        programs[prog]['total'] += amount
        programs[prog]['count'] += 1
    
    print('\nBy program:')
    for prog, stats in sorted(programs.items(), key=lambda x: x[1]['total'], reverse=True):
        print(f'  {prog}: ${stats["total"]:,.0f} ({stats["count"]} awards)')