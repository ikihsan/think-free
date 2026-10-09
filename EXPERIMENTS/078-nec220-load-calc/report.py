#!/usr/bin/env python3
"""
Gate evaluation and result printing for NEC 220 load calculation experiment.
"""

from nec220_core import STANDARD_SIZES

def evaluate_gates(test_results):
    """Evaluate all gates"""
    gates = {}
    
    # G1: Automated correctness (100% match oracle)
    auto_correct = test_results['models']['nec220_auto']['correct']
    gates['G1_auto_correctness'] = {
        'threshold': 1.0,
        'achieved': auto_correct / test_results['total_cases'],
        'pass': auto_correct == test_results['total_cases'],
        'detail': f'{auto_correct}/{test_results["total_cases"]} correct'
    }
    
    # G2: Baseline A (no demand factors) oversizing ≥30%
    baseline_no_demand_oversized = test_results['models']['no_demand_factors']['oversized']
    gates['G2_baseline_no_demand_oversizing'] = {
        'threshold': 0.30,
        'achieved': baseline_no_demand_oversized / test_results['total_cases'],
        'pass': baseline_no_demand_oversized / test_results['total_cases'] >= 0.30,
        'detail': f'{baseline_no_demand_oversized}/{test_results["total_cases"]} oversized by ≥1 size'
    }
    
    # G3: Baseline B (200A default) oversizing ≥5%
    baseline_200a_oversized = test_results['models']['200a_default']['oversized']
    gates['G3_baseline_200a_oversizing'] = {
        'threshold': 0.05,
        'achieved': baseline_200a_oversized / test_results['total_cases'],
        'pass': baseline_200a_oversized / test_results['total_cases'] >= 0.05,
        'detail': f'{baseline_200a_oversized}/{test_results["total_cases"]} oversized by ≥1 size'
    }
    
    # G4: Baseline C (VA/240) oversizing ≥30%
    baseline_va_div_oversized = test_results['models']['va_div_240']['oversized']
    gates['G4_baseline_va_div_oversizing'] = {
        'threshold': 0.30,
        'achieved': baseline_va_div_oversized / test_results['total_cases'],
        'pass': baseline_va_div_oversized / test_results['total_cases'] >= 0.30,
        'detail': f'{baseline_va_div_oversized}/{test_results["total_cases"]} oversized by ≥1 size'
    }
    
    # G5: Baseline D (contractor heuristic) oversizing ≥40%
    baseline_contractor_oversized = test_results['models']['contractor_heuristic']['oversized']
    gates['G5_baseline_contractor_oversizing'] = {
        'threshold': 0.40,
        'achieved': baseline_contractor_oversized / test_results['total_cases'],
        'pass': baseline_contractor_oversized / test_results['total_cases'] >= 0.40,
        'detail': f'{baseline_contractor_oversized}/{test_results["total_cases"]} oversized by ≥1 size'
    }
    
    # G6: Automated never oversizes
    auto_oversized = test_results['models']['nec220_auto']['oversized']
    gates['G6_auto_not_oversized'] = {
        'threshold': 0.0,
        'achieved': auto_oversized / test_results['total_cases'],
        'pass': auto_oversized == 0,
        'detail': f'{auto_oversized}/{test_results["total_cases"]} oversized by ≥1 size'
    }
    
    # G7: All profiles have ≥80% cases passing G1
    profile_pass = 0
    for profile, stats in test_results['profiles'].items():
        if stats['correct'] >= stats['total'] * 0.8:
            profile_pass += 1
    gates['G7_profile_coverage'] = {
        'threshold': len(test_results['profiles']),
        'achieved': profile_pass,
        'pass': profile_pass == len(test_results['profiles']),
        'detail': f'{profile_pass}/{len(test_results["profiles"])} profiles ≥80% correct'
    }
    
    return gates

def print_results(test_results, gates):
    """Print evaluation results"""
    print("=" * 60)
    print("NEC 220 LOAD CALCULATION - EVALUATION RESULTS")
    print("=" * 60)
    
    print("\n--- Model Performance (Test Split) ---")
    for model_name, stats in test_results['models'].items():
        correct = stats['correct']
        oversized = stats['oversized']
        total = test_results['total_cases']
        print(f"  {model_name}: {correct}/{total} correct ({correct/total*100:.1f}%), {oversized}/{total} oversized ({oversized/total*100:.1f}%)")
    
    print("\n--- Gate Results ---")
    for gate_name, gate in gates.items():
        status = "PASS" if gate['pass'] else "FAIL"
        print(f"  {gate_name}: {status} (achieved {gate['achieved']:.3f} vs threshold {gate['threshold']}) - {gate['detail']}")
    
    print("\n--- Per-Profile Breakdown (Test) ---")
    for profile, stats in test_results['profiles'].items():
        total = stats['total']
        correct = stats['correct']
        o_nd = stats['oversized_no_demand']
        o_200a = stats['oversized_200a']
        o_vd = stats['oversized_va_div']
        o_ch = stats['oversized_contractor']
        print(f"  {profile}: {correct}/{total} correct, no_demand_oversized={o_nd}/{total}, 200a_oversized={o_200a}/{total}, va_div_oversized={o_vd}/{total}, contractor_oversized={o_ch}/{total}")
    
    # Negative controls
    print("\n--- Negative Controls ---")
    import random
    from nec220_core import nec220_calculate, va_to_service_amps
    
    random_schedule = {
        'dwelling_sqft': random.randint(1000, 5000),
        'small_appliance_circuits': random.randint(2, 4),
        'laundry_circuits': random.randint(1, 2),
        'fixed_appliances_va': [random.randint(500, 5000) for _ in range(random.randint(0, 6))],
        'range_kw': random.uniform(0, 16),
        'dryer_va': random.choice([0, 5000, 5500]),
        'hvac_va': random.randint(0, 25000),
        'has_heat_pump': random.choice([True, False]),
        'ev_charger_va': random.choice([0, 7680, 9600, 19200]),
        'ev_load_management': random.choice([True, False]),
        'solar_pv_va': random.choice([0, 5000, 15000]),
        'storage_inverter_va': random.choice([0, 5000, 10000]),
        'storage_grid_charging': random.choice([True, False]),
    }
    random_result = nec220_calculate(random_schedule)
    random_amps = va_to_service_amps(random_result[0])
    print(f"  Random schedule: {random_amps}A service (no crash)")
    
    minimal_schedule = {
        'dwelling_sqft': 1000, 'small_appliance_circuits': 2, 'laundry_circuits': 1,
        'fixed_appliances_va': [], 'range_kw': 0, 'dryer_va': 0, 'hvac_va': 0,
        'has_heat_pump': False, 'ev_charger_va': 0, 'ev_load_management': False,
        'solar_pv_va': 0, 'storage_inverter_va': 0, 'storage_grid_charging': False,
    }
    minimal_result = nec220_calculate(minimal_schedule)
    minimal_amps = va_to_service_amps(minimal_result[0])
    print(f"  Minimal schedule: {minimal_amps}A service")
    
    empty_modern = {
        'dwelling_sqft': 2000, 'small_appliance_circuits': 2, 'laundry_circuits': 1,
        'fixed_appliances_va': [1200, 1500, 2000], 'range_kw': 10, 'dryer_va': 5000,
        'hvac_va': 6000, 'has_heat_pump': False, 'ev_charger_va': 0,
        'ev_load_management': False, 'solar_pv_va': 0, 'storage_inverter_va': 0,
        'storage_grid_charging': False,
    }
    empty_result = nec220_calculate(empty_modern)
    empty_amps = va_to_service_amps(empty_result[0])
    print(f"  Empty modern loads: {empty_amps}A service")