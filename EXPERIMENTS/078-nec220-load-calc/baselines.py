#!/usr/bin/env python3
"""
Baseline calculators for NEC 220 load calculation experiment.
Common rule-of-thumb methods that electricians use.
"""

from nec220_calculator import va_to_service_amps

# Standard service sizes
STANDARD_SIZES = [100, 125, 150, 200, 225, 300, 400]

def baseline_no_demand_factors(schedule):
    """Baseline A: Sum of ALL nameplate ratings with NO demand factors, round up to standard size.
    This is the classic 'add everything up' mistake that causes massive oversizing."""
    total_va = 0
    
    # Sum all nameplate ratings (NO demand factors at all)
    sqft = schedule.get('dwelling_sqft', 2000)
    total_va += sqft * 3  # General lighting at 100%
    total_va += schedule.get('small_appliance_circuits', 2) * 1500
    total_va += schedule.get('laundry_circuits', 1) * 1500
    total_va += sum(schedule.get('fixed_appliances_va', []))  # 100% of all appliances
    total_va += schedule.get('range_kw', 0) * 1000  # Full nameplate
    total_va += schedule.get('dryer_va', 0)  # Full nameplate
    total_va += schedule.get('hvac_va', 0)  # Full nameplate
    total_va += schedule.get('ev_charger_va', 0)  # Full nameplate
    total_va += schedule.get('storage_inverter_va', 0)  # Full nameplate
    # Solar doesn't add to load
    
    # NO 0.8 factor - just raw sum
    return va_to_service_amps(total_va)

def baseline_200a_default(schedule):
    """Baseline B: 200A default for any dwelling >1500 sqft, 150A otherwise.
    Common contractor rule of thumb."""
    sqft = schedule.get('dwelling_sqft', 2000)
    return 200 if sqft > 1500 else 150

def baseline_va_div_240(schedule):
    """Baseline C: Total VA / 240V with NO demand factors, round up to standard size.
    Simplistic 'convert everything to amps' method."""
    total_va = 0
    
    sqft = schedule.get('dwelling_sqft', 2000)
    total_va += sqft * 3  # General lighting
    total_va += schedule.get('small_appliance_circuits', 2) * 1500
    total_va += schedule.get('laundry_circuits', 1) * 1500
    total_va += sum(schedule.get('fixed_appliances_va', []))
    total_va += schedule.get('range_kw', 0) * 1000
    total_va += schedule.get('dryer_va', 0)
    total_va += schedule.get('hvac_va', 0)
    total_va += schedule.get('ev_charger_va', 0)
    total_va += schedule.get('storage_inverter_va', 0)
    
    # Simple VA/240, no demand factors
    return va_to_service_amps(total_va)

def baseline_contractor_heuristic(schedule):
    """Baseline D: Contractor heuristic - 3VA/sqft + 20A per major appliance circuit.
    Another common oversizing rule."""
    sqft = schedule.get('dwelling_sqft', 2000)
    base_va = sqft * 3
    
    # Count major appliance circuits
    major_circuits = 0
    major_circuits += 2  # small appliance
    major_circuits += 1  # laundry
    major_circuits += len(schedule.get('fixed_appliances_va', []))
    if schedule.get('range_kw', 0) > 0:
        major_circuits += 1
    if schedule.get('dryer_va', 0) > 0:
        major_circuits += 1
    if schedule.get('hvac_va', 0) > 0:
        major_circuits += 1
    if schedule.get('ev_charger_va', 0) > 0:
        major_circuits += 1
    if schedule.get('storage_inverter_va', 0) > 0:
        major_circuits += 1
    
    # 20A per major circuit at 240V = 4800 VA each
    total_va = base_va + major_circuits * 4800
    return va_to_service_amps(total_va)

BASELINES = {
    'no_demand_factors': baseline_no_demand_factors,
    '200a_default': baseline_200a_default,
    'va_div_240': baseline_va_div_240,
    'contractor_heuristic': baseline_contractor_heuristic,
}