#!/usr/bin/env python3
"""Reference tables for GSA MAS Schedule 70 SINs and SEWP categories (E210).

Transcribed from public GSA Advantage / eLibrary SIN listings and SEWP
category listings, as analyzed in EXPERIMENTS/E210-vehicle-sin-sewp-analysis
and validated (with limits) in EXPERIMENTS/E213-sin-sewp-validation.
"""

# ─── GSA MAS Schedule 70 SIN Reference ────────────────────────────────────────
# Based on GSA MAS Schedule 70 (IT) SINs as of 2024-2025
# Source: GSA Advantage / eLibrary public SIN listings
GSA_SCHEDULE_70_SINS = {
    # Software SINs
    "511210": {
        "name": "Software Publishing",
        "description": "Commercial software products, licenses, subscriptions, SaaS",
        "category": "software",
    },
    "511210S": {
        "name": "Software Publishing - SaaS",
        "description": "Software as a Service offerings",
        "category": "software",
    },
    "511210RC": {
        "name": "Software Publishing - Related Services",
        "description": "Maintenance, support, training for software products",
        "category": "service",
    },
    "518210C": {
        "name": "Cloud Computing Services - Commercial Cloud",
        "description": "IaaS, PaaS, SaaS cloud services",
        "category": "software",
    },
    "518210CS": {
        "name": "Cloud Computing Services - Cloud Related Services",
        "description": "Cloud migration, integration, management services",
        "category": "service",
    },
    # IT Services SINs
    "54151S": {
        "name": "IT Professional Services",
        "description": "Software development, integration, consulting, implementation",
        "category": "service",
    },
    "54151HACS": {
        "name": "Highly Adaptive Cybersecurity Services",
        "description": "Penetration testing, incident response, vulnerability assessment",
        "category": "service",
    },
    "54151SOC": {
        "name": "Security Operations Center Services",
        "description": "Managed SOC, monitoring, threat detection",
        "category": "service",
    },
    "54151RM": {
        "name": "Risk Management Services",
        "description": "Security assessment, authorization, compliance",
        "category": "service",
    },
    "541611": {
        "name": "Administrative Management Consulting",
        "description": "IT strategy, governance, enterprise architecture",
        "category": "service",
    },
    "541612": {
        "name": "Human Resources Consulting",
        "description": "HR systems implementation, HRIS consulting",
        "category": "service",
    },
    "541613": {
        "name": "Marketing Consulting",
        "description": "Digital marketing, CRM, marketing automation",
        "category": "service",
    },
    "541614": {
        "name": "Process/Logistics Consulting",
        "description": "Supply chain, ERP, logistics IT consulting",
        "category": "service",
    },
    # Hardware SINs
    "33411": {
        "name": "Computer and Peripheral Equipment Manufacturing",
        "description": "Servers, storage, workstations, laptops, peripherals",
        "category": "hardware",
    },
    "811212": {
        "name": "Computer and Office Machine Repair",
        "description": "Hardware maintenance, repair, warranty services",
        "category": "service",
    },
    # Telecommunications SINs
    "517311": {
        "name": "Wired Telecommunications Carriers",
        "description": "Voice, data, internet, MPLS, VPN services",
        "category": "telecom",
    },
    "517312": {
        "name": "Wireless Telecommunications Carriers",
        "description": "Cellular, 5G, satellite, wireless connectivity",
        "category": "telecom",
    },
    "517911": {
        "name": "Telecommunications Resellers",
        "description": "Resold telecom services, bandwidth, circuits",
        "category": "telecom",
    },
    # Legacy Schedule 70 SINs (pre-consolidation, still in use)
    "132-51": {
        "name": "IT Professional Services (Legacy)",
        "description": "Legacy SIN for IT services, still active on many contracts",
        "category": "service",
    },
    "132-52": {
        "name": "IT Hardware (Legacy)",
        "description": "Legacy SIN for IT hardware",
        "category": "hardware",
    },
    "132-33": {
        "name": "Peripherals and Storage (Legacy)",
        "description": "Legacy SIN for peripherals and storage",
        "category": "hardware",
    },
    "132-34": {
        "name": "Data Communications (Legacy)",
        "description": "Legacy SIN for networking equipment",
        "category": "hardware",
    },
    "132-54": {
        "name": "Telecommunications Services (Legacy)",
        "description": "Legacy SIN for telecom services",
        "category": "telecom",
    },
    "132-56": {
        "name": "Health IT (Legacy)",
        "description": "Legacy SIN for health IT systems and services",
        "category": "software",
    },
}

# ─── SEWP Category Reference ──────────────────────────────────────────────────
# NASA SEWP (Solutions for Enterprise-Wide Procurement) categories
# Based on SEWP V catalog structure
SEWP_CATEGORIES = {
    "A": {
        "name": "IT Hardware",
        "description": "Computers, servers, storage, networking, peripherals",
        "subcategories": ["A1: Desktop/Laptop", "A2: Server/Storage", "A3: Networking", "A4: Peripherals"],
        "category": "hardware",
    },
    "B": {
        "name": "IT Software",
        "description": "Commercial software, licenses, SaaS, cloud services",
        "subcategories": ["B1: Operating Systems", "B2: Application Software", "B3: Middleware", "B4: Cloud/SaaS"],
        "category": "software",
    },
    "C": {
        "name": "IT Services",
        "description": "Professional services, integration, consulting, maintenance",
        "subcategories": ["C1: Implementation", "C2: Maintenance/Support", "C3: Cybersecurity", "C4: Cloud Services"],
        "category": "service",
    },
    "D": {
        "name": "Telecommunications",
        "description": "Voice, data, video, wireless, satellite communications",
        "subcategories": ["D1: Voice", "D2: Data/Internet", "D3: Wireless/Mobile", "D4: Satellite"],
        "category": "telecom",
    },
    "E": {
        "name": "Audio/Visual",
        "description": "Conferencing, display, collaboration equipment",
        "subcategories": ["E1: Video Conferencing", "E2: Display Systems", "E3: Collaboration Tools"],
        "category": "hardware",
    },
}

# ─── GSA MAS PIID to SIN Mapping Heuristics ───────────────────────────────────
# Common GSA MAS PIID prefixes and their typical SIN coverage
GSA_PIID_SIN_MAP = {
    # Large resellers with broad SIN coverage
    "GS35F": ["511210", "518210C", "54151S", "33411", "517311"],  # Typical broad coverage
    "GS03F": ["511210", "54151S", "33411"],
    "GS00": ["511210", "54151S", "33411", "517311"],
    "47QTCA": ["511210", "518210C", "54151S", "54151HACS", "54151SOC", "54151RM"],  # FAS IT Schedule
    "47QREA": ["511210", "54151S", "33411", "517311"],
    "47Q": ["511210", "518210C", "54151S"],
}

# ─── SEWP PIID to Category Mapping ────────────────────────────────────────────
# SEWP V contract holders and their category coverage
SEWP_HOLDER_CATEGORIES = {
    # Major SEWP V prime contractors
    "NNG15SE": ["A", "B", "C", "D", "E"],  # Full SEWP V scope
    "NNG15SC": ["A", "B", "C", "D", "E"],
    "NNG15SD": ["A", "B", "C", "D", "E"],
    # Category-specific holders (subset)
    "NNG15SE304": ["A", "B"],  # Hardware + Software
    "NNG15SE305": ["B", "C"],  # Software + Services
    "NNG15SE306": ["C", "D"],  # Services + Telecom
    "NNG15SE307": ["A", "D", "E"],  # Hardware + Telecom + AV
}

# ─── Known Small Vendor SIN/Category Success Patterns ─────────────────────────
# Based on public GSA/SEWP award data patterns
SMALL_VENDOR_SIN_AFFINITY = {
    "511210": 0.85,      # Software publishing - high small vendor participation
    "511210S": 0.80,     # SaaS - very high small vendor participation
    "518210C": 0.75,     # Cloud services - high small vendor participation
    "54151S": 0.60,      # IT services - moderate (many small firms)
    "54151HACS": 0.55,   # Cybersecurity services - moderate
    "54151SOC": 0.40,    # SOC services - lower (requires scale)
    "54151RM": 0.50,     # Risk management - moderate
    "33411": 0.20,       # Hardware - low (dominated by large OEMs)
    "811212": 0.30,      # Repair - moderate
    "517311": 0.15,      # Telecom carriers - very low
    "517312": 0.15,      # Wireless - very low
    "517911": 0.25,      # Telecom resellers - low-moderate
    "132-51": 0.65,      # Legacy IT services - moderate-high
    "132-56": 0.70,      # Health IT - moderate-high (niche)
}

SMALL_VENDOR_SEWP_CAT_AFFINITY = {
    "B": 0.80,   # Software - high
    "C": 0.60,   # Services - moderate
    "A": 0.20,   # Hardware - low
    "D": 0.15,   # Telecom - very low
    "E": 0.25,   # AV - low
}
