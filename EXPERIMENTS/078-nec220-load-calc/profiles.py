#!/usr/bin/env python3
"""
Profile generators for NEC 220 load calculation experiment.
Generates 10 load profiles for synthetic fixtures.
"""

import random
from nec220_core import nec220_calculate

def generate_profile_1_standard():
    """Standard dwelling: lighting, small appliance, laundry, range, dryer, HVAC"""
    sqft = random.randint(1000, 3000)
    return {
        'profile': 'standard',
        'dwelling_sqft': sqft,
        'small_appliance_circuits': 2,
        'laundry_circuits': 1,
        'fixed_appliances_va': [random.randint(1000, 3000) for _ in range(random.randint(2, 4))],
        'range_kw': random.uniform(8, 12),
        'dryer_va': random.randint(5000, 5500),
        'hvac_va': random.randint(4000, 8000),
        'has_heat_pump': False,
        'ev_charger_va': 0,
        'ev_load_management': False,
        'solar_pv_va': 0,
        'storage_inverter_va': 0,
        'storage_grid_charging': False,
    }

def generate_profile_2_ev():
    """Standard + EV charger"""
    base = generate_profile_1_standard()
    base['profile'] = 'with_ev'
    base['ev_charger_va'] = random.choice([7680, 9600, 11520, 15360, 19200])  # 32A-80A @ 240V
    base['ev_load_management'] = random.choice([True, False])
    return base

def generate_profile_3_solar():
    """Standard + Solar PV"""
    base = generate_profile_1_standard()
    base['profile'] = 'with_solar'
    base['solar_pv_va'] = random.randint(5000, 20000)  # 5-20 kW
    return base

def generate_profile_4_heatpump():
    """Standard with heat pump instead of gas furnace + AC"""
    base = generate_profile_1_standard()
    base['profile'] = 'with_heat_pump'
    base['has_heat_pump'] = True
    base['hvac_va'] = random.randint(6000, 15000)  # Heat pump + backup heat
    base['dryer_va'] = random.randint(5000, 5500)  # Electric dryer
    base['range_kw'] = random.uniform(8, 12)  # Electric range
    # Add water heater
    base['fixed_appliances_va'].append(random.randint(3000, 4500))
    return base

def generate_profile_5_storage():
    """Standard + Battery storage"""
    base = generate_profile_1_standard()
    base['profile'] = 'with_storage'
    base['storage_inverter_va'] = random.randint(5000, 12000)  # 5-12 kW inverter
    base['storage_grid_charging'] = random.choice([True, False])
    return base

def generate_profile_6_ev_solar():
    """Standard + EV + Solar"""
    base = generate_profile_1_standard()
    base['profile'] = 'ev_solar'
    base['ev_charger_va'] = random.choice([7680, 9600, 11520, 15360, 19200])
    base['ev_load_management'] = random.choice([True, False])
    base['solar_pv_va'] = random.randint(5000, 20000)
    return base

def generate_profile_7_ev_heatpump():
    """Standard + EV + Heat pump (all-electric except water heater)"""
    base = generate_profile_4_heatpump()
    base['profile'] = 'ev_heat_pump'
    base['ev_charger_va'] = random.choice([7680, 9600, 11520, 15360, 19200])
    base['ev_load_management'] = random.choice([True, False])
    return base

def generate_profile_8_all_electric():
    """All-electric: heat pump, electric range, electric dryer, electric water heater"""
    sqft = random.randint(1500, 3500)
    return {
        'profile': 'all_electric',
        'dwelling_sqft': sqft,
        'small_appliance_circuits': 2,
        'laundry_circuits': 1,
        'fixed_appliances_va': [
            random.randint(3000, 4500),  # water heater
            random.randint(1000, 2000),  # dishwasher
            random.randint(800, 1500),   # disposal
        ],
        'range_kw': random.uniform(8, 12),
        'dryer_va': random.randint(5000, 5500),
        'hvac_va': random.randint(8000, 18000),  # Heat pump with strip heat
        'has_heat_pump': True,
        'ev_charger_va': 0,
        'ev_load_management': False,
        'solar_pv_va': 0,
        'storage_inverter_va': 0,
        'storage_grid_charging': False,
    }

def generate_profile_9_all_electric_solar():
    """All-electric + Solar"""
    base = generate_profile_8_all_electric()
    base['profile'] = 'all_electric_solar'
    base['solar_pv_va'] = random.randint(8000, 20000)
    return base

def generate_profile_10_large():
    """Large dwelling >3500 sqft with multiple HVAC zones"""
    sqft = random.randint(3500, 5000)
    return {
        'profile': 'large_dwelling',
        'dwelling_sqft': sqft,
        'small_appliance_circuits': 3,
        'laundry_circuits': 2,
        'fixed_appliances_va': [
            random.randint(3000, 4500),  # water heater
            random.randint(1000, 2000),  # dishwasher
            random.randint(800, 1500),   # disposal
            random.randint(5000, 8000),  # pool/spa
        ],
        'range_kw': random.uniform(12, 16),
        'dryer_va': random.randint(5000, 5500),
        'hvac_va': random.randint(12000, 25000),  # Multiple zones
        'has_heat_pump': random.choice([True, False]),
        'ev_charger_va': random.choice([0, 9600, 19200]),
        'ev_load_management': random.choice([True, False]),
        'solar_pv_va': random.choice([0, 10000, 20000]),
        'storage_inverter_va': random.choice([0, 8000]),
        'storage_grid_charging': False,
    }

PROFILE_GENERATORS = [
    generate_profile_1_standard,
    generate_profile_2_ev,
    generate_profile_3_solar,
    generate_profile_4_heatpump,
    generate_profile_5_storage,
    generate_profile_6_ev_solar,
    generate_profile_7_ev_heatpump,
    generate_profile_8_all_electric,
    generate_profile_9_all_electric_solar,
    generate_profile_10_large,
]

def generate_all_cases():
    """Generate all 100 cases and return train/val/test splits"""
    all_cases = []
    
    for i, generator in enumerate(PROFILE_GENERATORS):
        for j in range(10):  # 10 cases per profile
            schedule = generator()
            
            # Calculate ground truth using NEC 220
            total_va, solar_va = nec220_calculate(schedule)
            service_amps = nec220_calculate.__globals__['va_to_service_amps'](total_va)
            
            case = {
                'id': f'{schedule["profile"]}_{j:02d}',
                'profile': schedule['profile'],
                'schedule': schedule,
                'ground_truth': {
                    'total_calculated_va': round(total_va, 1),
                    'solar_backfeed_va': solar_va,
                    'minimum_service_amps': service_amps,
                }
            }
            all_cases.append(case)
    
    # Shuffle and split
    random.shuffle(all_cases)
    
    train = all_cases[:30]
    val = all_cases[30:60]
    test = all_cases[60:]
    
    return train, val, test