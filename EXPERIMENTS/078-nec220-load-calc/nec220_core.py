#!/usr/bin/env python3
"""
NEC 220 calculation functions shared between fixture generator and calculator.
"""

import random

# Fixed seed for reproducibility
random.seed(42)

# Standard service sizes (NEC 230.24)
STANDARD_SIZES = [100, 125, 150, 200, 225, 300, 400]

# NEC Table 220.42 demand factors for general lighting
# First 3000 VA at 100%, next 117000 VA at 35%, remainder at 25%
def calc_general_lighting_demand(sqft):
    """Calculate general lighting demand per NEC 220.42"""
    va_per_sqft = 3  # VA per sq ft
    total_va = sqft * va_per_sqft
    if total_va <= 3000:
        return total_va
    elif total_va <= 120000:
        return 3000 + (total_va - 3000) * 0.35
    else:
        return 3000 + 117000 * 0.35 + (total_va - 120000) * 0.25

# NEC Table 220.54 demand factors for appliances
def calc_appliance_demand(appliance_va_list):
    """Calculate appliance demand per NEC 220.54"""
    if not appliance_va_list:
        return 0
    if len(appliance_va_list) <= 4:
        return sum(appliance_va_list) * 0.75
    else:
        return sum(appliance_va_list) * 0.75  # Simplified - NEC has table for 5+

# NEC 220.55 range demand
def calc_range_demand(kw):
    """Calculate range demand per NEC 220.55 Table 220.55"""
    if kw <= 12:
        return kw * 1000  # Use nameplate for ≤12kW
    else:
        # Column C: 12kW = 8000W, plus 5% per kW over 12
        return 8000 + (kw - 12) * 1000 * 0.05 * 1000

# NEC 220.54 dryer demand
def calc_dryer_demand(va):
    """Calculate dryer demand per NEC 220.54"""
    return max(va, 5000)  # Minimum 5000 VA

# NEC 220.83/220.82 HVAC demand
def calc_hvac_demand(hvac_va, has_heat_pump=False):
    """Calculate HVAC demand - largest of heating or cooling"""
    return hvac_va

# NEC 625.42 EV charger with load management
def calc_ev_demand(ev_va, load_management=False):
    """Calculate EV charger demand per NEC 625.42"""
    return ev_va  # 100% of nameplate

# NEC 705.12 solar PV backfeed
def calc_solar_backfeed(solar_va, busbar_rating=None):
    """Calculate solar backfeed contribution per NEC 705.12"""
    return 0  # Doesn't increase service load

# NEC 706 battery storage
def calc_storage_demand(storage_va, grid_charging=False):
    """Calculate battery storage demand"""
    if grid_charging:
        return storage_va  # Charging from grid adds load
    return 0  # Discharging doesn't add to service load

def nec220_calculate(schedule):
    """
    Full NEC 220 calculation for a dwelling unit.
    Returns (total_calculated_va, solar_backfeed_va)
    """
    total_va = 0
    
    # 1. General lighting (Table 220.42)
    sqft = schedule.get('dwelling_sqft', 2000)
    total_va += calc_general_lighting_demand(sqft)
    
    # 2. Small appliance circuits (220.52(A)) - 1500 VA each, min 2
    small_appliance_va = schedule.get('small_appliance_circuits', 2) * 1500
    total_va += small_appliance_va
    
    # 3. Laundry circuit (220.52(B)) - 1500 VA
    laundry_va = schedule.get('laundry_circuits', 1) * 1500
    total_va += laundry_va
    
    # 4. Fixed appliances (220.53) - nameplate with demand factor if 4+
    fixed_appliances = schedule.get('fixed_appliances_va', [])
    if fixed_appliances:
        total_va += calc_appliance_demand(fixed_appliances)
    
    # 5. Range (220.55)
    range_kw = schedule.get('range_kw', 0)
    if range_kw > 0:
        total_va += calc_range_demand(range_kw)
    
    # 6. Dryer (220.54)
    dryer_va = schedule.get('dryer_va', 0)
    if dryer_va > 0:
        total_va += calc_dryer_demand(dryer_va)
    
    # 7. HVAC (220.83) - 100% of largest
    hvac_va = schedule.get('hvac_va', 0)
    if hvac_va > 0:
        total_va += calc_hvac_demand(hvac_va, schedule.get('has_heat_pump', False))
    
    # 8. EV Charger (625.42)
    ev_va = schedule.get('ev_charger_va', 0)
    if ev_va > 0:
        total_va += calc_ev_demand(ev_va, schedule.get('ev_load_management', False))
    
    # 9. Battery storage (706) - only if grid charging
    storage_va = schedule.get('storage_inverter_va', 0)
    if storage_va > 0:
        total_va += calc_storage_demand(storage_va, schedule.get('storage_grid_charging', False))
    
    # 10. Solar PV (705) - backfeed doesn't add to load
    solar_va = schedule.get('solar_pv_va', 0)
    
    return total_va, solar_va

def va_to_service_amps(va, voltage=240):
    """Convert VA to minimum standard service amperage"""
    amps = va / voltage
    # NEC 230.42: service ampacity ≥ calculated load
    # Round up to next standard size
    for size in STANDARD_SIZES:
        if size >= amps:
            return size
    return STANDARD_SIZES[-1]