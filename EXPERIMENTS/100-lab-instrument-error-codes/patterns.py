# Fault code patterns for lab instruments
# Pre-declared before any harvesting

import re

# Common patterns across vendors
GENERIC_PATTERNS = [
    # Hex codes: 0x1A, 0x402, 0xFFFF
    r'0x[0-9A-Fa-f]{1,8}',
    # Decimal codes: 102, 402, 1001
    r'\b[1-9][0-9]{2,5}\b',
    # Error/Error code prefixes
    r'[Ee]rror\s*[#:]\s*[0-9A-Fa-fxX]+',
    r'[Ee]rror\s*[Cc]ode\s*[#:]\s*[0-9A-Fa-fxX]+',
    r'[Ff]ault\s*[Cc]ode\s*[#:]\s*[0-9A-Fa-fxX]+',
    r'[Ff]ault\s*[#:]\s*[0-9A-Fa-fxX]+',
    # Status codes
    r'[Ss]tatus\s*[Cc]ode\s*[#:]\s*[0-9A-Fa-fxX]+',
]

# Vendor-specific patterns
VENDOR_PATTERNS = {
    'thermo_fisher': [
        # Thermo/Orbitrap: E-XXX, E-XXXX
        r'[Ee]-\d{3,4}',
        # Tune error codes
        r'[Tt]une\s*[Ee]rror\s*\d+',
    ],
    'agilent': [
        # Agilent: 0xXXXX, Err XXX
        r'[Ee]rr\s*\d{1,4}',
        r'[Aa]gilent\s*[Ee]rror\s*\d+',
    ],
    'bruker': [
        # Bruker: Error XXX, Err XXX
        r'[Ee]rror\s*\d{1,4}',
        r'[Bb]ruker\s*[Ee]rror\s*\d+',
    ],
    'waters': [
        # Waters: Error XXX, E-XXX
        r'[Ee]-\d{3,4}',
        r'[Ww]aters\s*[Ee]rror\s*\d+',
    ],
    'illumina': [
        # Illumina: Error #XXXX, E-XXXX
        r'[Ee]rror\s*#\d{3,5}',
        r'[Ee]-\d{4,5}',
    ],
    'pacbio': [
        # PacBio: Error XXX
        r'[Ee]rror\s*\d{1,4}',
    ],
    'oxford_nanopore': [
        # ONT: Error XXX, ERR_XXXX
        r'[Ee]rr_\w+',
        r'[Ee]rror\s*\d{1,4}',
    ],
    'beckman_coulter': [
        # Beckman: Error XXX, E-XXX
        r'[Ee]-\d{3,4}',
        r'[Bb]eckman\s*[Ee]rror\s*\d+',
    ],
    'bd': [
        # BD: Error XXX
        r'[Ee]rror\s*\d{1,4}',
    ],
    'bio_rad': [
        # Bio-Rad: Error XXX
        r'[Ee]rror\s*\d{1,4}',
    ],
    'shimadzu': [
        # Shimadzu: Error XXX, E-XXX
        r'[Ee]-\d{3,4}',
        r'[Ss]himadzu\s*[Ee]rror\s*\d+',
    ],
    'perkinelmer': [
        # PerkinElmer: Error XXX
        r'[Ee]rror\s*\d{1,4}',
    ],
    'jeol': [
        # JEOL: Error XXX
        r'[Ee]rror\s*\d{1,4}',
    ],
    'zeiss': [
        # ZEISS: Error XXX
        r'[Ee]rror\s*\d{1,4}',
    ],
}

# Instrument type keywords for classification
INSTRUMENT_TYPES = {
    'mass_spectrometry': [
        'mass spec', 'mass spectrometer', 'ms', 'lc-ms', 'gc-ms', 'maldi',
        'orbitrap', 'q-exactive', 'fusion', 'eclipse', 'exploris', 'tims',
        'toft', 'q-tof', 'triple quad', 'quadrupole', 'ion trap',
        'agilent 64', 'agilent 65', 'sciex', 'ab sciex', 'waters xevo',
        'waters synapt', 'waters select', 'thermo orbitrap', 'thermo tsq',
        'bruker tims', 'bruker maXis', 'bruker impact',
    ],
    'electron_microscopy': [
        'electron microscop', 'em ', 'tem', 'sem', 'stem', 'feg',
        'cryo-em', 'cryo-tem', 'jeol', 'zeiss', 'thermo fisher', 'fei',
        'talos', 'glacios', 'krios', 'aquilos',
    ],
    'genomics_sequencing': [
        'sequenc', 'illumina', 'miseq', 'hiseq', 'novaseq', 'nextseq',
        'pacbio', 'sequel', 'revio', 'oxford nanopore', 'minion', 'gridion',
        'promethion', 'pacific biosciences',
    ],
    'flow_cytometry': [
        'flow cytometer', 'flow cytometry', 'fac', 'cytoflex', 'celesta',
        'fortessa', 'lyric', 'aurora', 'symphony', 'attune', 'novocyte',
        'beckman coulter', 'bd biosciences', 'sony', 'luminex',
    ],
    'pcr_qpcr': [
        'pcr', 'qpcr', 'real-time pcr', 'digital pcr', 'ddpcr',
        'lightcycler', 'quantstudio', 'viia', 'stepone', 'cfx',
        'roche cobas', 'bio-rad cfx', 'thermo quantstudio',
    ],
    'chromatography': [
        'hplc', 'uhplc', 'lc', 'gc', 'gas chromatograph',
        'agilent 12', 'agilent infinity', 'waters acquity', 'waters alliance',
        'thermo vanquish', 'thermo dionex', 'shimadzu nexera', 'shimadzu lc',
        'perkinelmer flexar', 'sciex exion',
    ],
    'spectroscopy': [
        'spectrophotometer', 'spectrometer', 'uv-vis', 'uv/vis', 'ftir',
        'raman', 'fluorescence', 'fluorometer', 'plate reader', 'microplate',
        'spectramax', 'varioskan', 'clariostar', 'infinite',
    ],
    'microscopy': [
        'microscop', 'confocal', 'fluorescence microscop', 'widefield',
        'spinning disk', 'lightsheet', 'multiphoton', 'stimulated emission',
        'stimulated depletion', 'stimulated emission depletion', 'sted',
        'structured illumination', 'sim', 'airyscan', 'lsm',
    ],
    'lab_automation': [
        'lab automation', 'liquid handler', 'robot', 'automat',
        'hamilton', 'tecan', 'biotek', 'agilent bravo', 'thermo kingfisher',
        'perkinelmer janus', 'beckman coulter biomek', 'opentrons',
    ],
}

# Common fault code mnemonics / categories
FAULT_CATEGORIES = {
    'communication': ['comm', 'communication', 'canbus', 'i2c', 'spi', 'uart', 'ethernet', 'tcp', 'ip', 'network'],
    'temperature': ['temp', 'temperature', 'thermal', 'heater', 'cooler', 'peltier', 'oven', 'chiller'],
    'pressure': ['pressure', 'vacuum', 'pump', 'turbo', 'roughing', 'ion gauge', 'penning'],
    'voltage_current': ['voltage', 'current', 'power', 'supply', 'hv', 'high voltage', 'low voltage', 'bias'],
    'optics': ['optical', 'laser', 'detector', 'photomultiplier', 'pmt', 'apd', 'diode', 'lamp', 'led'],
    'mechanical': ['motor', 'stage', 'arm', 'gripper', 'needle', 'valve', 'actuator', 'encoder', 'limit switch'],
    'fluidics': ['pump', 'valve', 'syringe', 'tubing', 'leak', 'bubble', 'flow', 'pressure', 'primer'],
    'software_firmware': ['firmware', 'software', 'driver', 'firmware version', 'update', 'upgrade', 'boot', 'crash', 'hang', 'freeze'],
}

# Compile all patterns
ALL_PATTERNS = GENERIC_PATTERNS.copy()
for patterns in VENDOR_PATTERNS.values():
    ALL_PATTERNS.extend(patterns)

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in ALL_PATTERNS]

# Instrument type detection patterns
INSTRUMENT_TYPE_PATTERNS = {}
for inst_type, keywords in INSTRUMENT_TYPES.items():
    pattern = '|'.join(re.escape(k) for k in keywords)
    INSTRUMENT_TYPE_PATTERNS[inst_type] = re.compile(pattern, re.IGNORECASE)


def extract_fault_codes(text):
    """Extract fault/error codes from text using all patterns."""
    codes = []
    for pattern in COMPILED_PATTERNS:
        matches = pattern.findall(text)
        codes.extend(matches)
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for c in codes:
        normalized = c.upper()
        if normalized not in seen:
            seen.add(normalized)
            unique.append(c)
    return unique


def detect_instrument_type(text):
    """Detect instrument types mentioned in text."""
    detected = []
    for inst_type, pattern in INSTRUMENT_TYPE_PATTERNS.items():
        if pattern.search(text):
            detected.append(inst_type)
    return detected


def detect_fault_categories(text):
    """Detect fault categories mentioned in text."""
    detected = []
    text_lower = text.lower()
    for category, keywords in FAULT_CATEGORIES.items():
        if any(k in text_lower for k in keywords):
            detected.append(category)
    return detected


def has_fault_code(text):
    """Check if text contains any fault code pattern."""
    return any(p.search(text) for p in COMPILED_PATTERNS)


def has_instrument_context(text):
    """Check if text mentions any lab instrument type."""
    return any(p.search(text) for p in INSTRUMENT_TYPE_PATTERNS.values())


if __name__ == '__main__':
    # Test patterns
    test_texts = [
        "Error E-102 on Thermo Fisher Orbitrap Fusion",
        "Agilent 6460 error 0x402",
        "Bruker timsTOF error 1024",
        "Illumina NextSeq error #1234",
        "Flow cytometer BD Fortessa error 50",
        "PCR QuantStudio 5 error E-003",
        "HPLC Waters Acquity error 0x200",
        "Microscope Zeiss LSM 880 error 1001",
        "Robot Hamilton STAR error 0x0F",
        "Need help with error code 0x402 on my mass spec",
        "Is there a tool to look up fault codes for Orbitrap?",
        "My flow cytometer shows error 50 and won't start",
    ]
    
    for text in test_texts:
        codes = extract_fault_codes(text)
        inst = detect_instrument_type(text)
        cats = detect_fault_categories(text)
        print(f"Text: {text}")
        print(f"  Codes: {codes}")
        print(f"  Instrument types: {inst}")
        print(f"  Fault categories: {cats}")
        print(f"  Has fault code: {has_fault_code(text)}")
        print(f"  Has instrument context: {has_instrument_context(text)}")
        print()