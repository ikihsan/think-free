#!/usr/bin/env python3
"""
E083 — Classification logic for 3D printer fault codes.
Predeclared rules from CLASSIFICATION_RULES.md.
"""

import re
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Fault Type Patterns (ordered by specificity)
# ---------------------------------------------------------------------------

FAULT_PATTERNS = [
    # Most specific patterns first (from CLASSIFICATION_RULES.md AMENDMENT 1)
    ("THERMAL_RUNAWAY", r"thermal runaway|thermal protection|thermal cutoff|safety.*temp"),
    ("MINTEMP", r"mintemp|min temp|minimum temp"),
    ("MAXTEMP", r"maxtemp|max temp|maximum temp"),
    ("HEATING_FAILED", r"heating failed|failed to heat|heating timeout|heating error|heater error|heater circuit|heating issue|heat.*error|heat.*fail|heat.*issue|heat.*problem|nozzle heat|hotend heat|bed heat|heat.*not.*work|heat.*stop|heat.*slow"),
    ("PROBE_FAILED", r"probe failed|probing failed|bltouch.*error|probe.*error|cr.?touch.*error|cr.?touch.*fail|probe.*issue|probe.*problem|sensor.*probe|leveling.*probe|auto.*level.*error|mesh.*error|bed.*level.*error|z.*probe.*error"),
    ("HOMING_FAILED", r"homing failed|failed to home|homing error|home.*fail|home.*error|homing issue|won.*t home|can.*t home|home.*issue|x.*home.*fail|y.*home.*fail|z.*home.*fail|rehome.*fail|homing.*issue|sensorless.*homing.*fail|homing.*sensor"),
    ("MCU_SHUTDOWN", r"mcu.*shutdown|mcu shutdown|klipper.*shutdown|klipper.*disconnect|moonraker.*disconnect|mcu.*disconnect|kill\(\)|printer halted|emergency stop"),
    ("TEMP_SENSOR_ERROR", r"temperature sensor|thermistor.*error|sensor.*error|thermistor.*fail|thermistor.*issue|thermistor.*problem|what thermistor|bed thermistor|hotend thermistor|thermistor replacement|thermistor type|thermistor blues"),
    ("STEPPER_DRIVER_ERROR", r"stepper driver|driver error|tmc.*error|stallguard|sensorless.*hom|stepper.*fail|stepper.*error|motor.*error|motor.*fail|axis.*error|stepper.*noise|motor.*noise|x axis noise|y axis noise|z axis noise|stepper.*skip|motor.*skip"),
    ("CLOGGED_NOZZLE", r"clogged nozzle|nozzle clog|clog|jammed nozzle|extruder jam|nozzle jam|hotend clog|heatbreak clog|ptfe clog|bowden clog|filament stuck|stuck filament|clogged hotend"),
    ("BED_LEVELING_FAILED", r"bed leveling failed|leveling failed|mesh.*failed|auto level.*fail|bed level.*error|leveling.*error|auto level.*error|mesh.*error|bed mesh|leveling washers|missing leveling|z offset|z.*offset.*issue|probe.*offset|bltouch.*offset|cr.?touch.*offset|bed.*mesh.*issue|first layer.*issue|first layer.*problem|adhesion.*issue|not adhering|not sticking|won.*t stick|comes off.*bed|print comes off|bed adhesion|plate.*peel|magnetic plate.*peel"),
    ("LAYER_SHIFT", r"layer shift|shifting layer|offset layer|misaligned layers|misalignment|layer offset|layer.*misalign|z banding|z-banding|banding|wobble|print shift|sudden shift|position shift"),
    ("SD_CARD_ERROR", r"sd card|sdcard|card error|read error|file error|gcode.*error|sd init|sd.*fail|sd.*error|card.*fail|card.*init|micro.*sd|sd.*corrupt|gcode.*upload.*fail|upload.*fail"),
    ("FILAMENT_RUNOUT", r"filament runout|runout sensor|out of filament|filament.*out|no filament|runout.*fail|runout.*error"),
    ("EXTRUDER_SKIP", r"extruder skip|skipping extruder|clicking extruder|extruder.*click|extruder.*clicking|clicking.*extruder|gear.*skip|drive gear.*skip|extruder.*tension|tension.*issue|filament.*tension|extruder.*grind|grinding.*filament|extruder.*slip"),
    ("UNDER_EXTRUSION", r"under extrusion|under-extrusion|insufficient extrusion|gaps in print|not extruding|won.*t extrude|no extrusion|extrusion.*fail|extrusion.*issue|extrusion.*problem|extrude.*fail|extrude.*issue|under.*extrud|poor extrusion|weak extrusion|thin extrusion"),
    ("OVER_EXTRUSION", r"over extrusion|over-extrusion|too much filament|blobbing|over.*extrud|excess.*extrusion|blob|zit|elephant foot"),
    ("RETRACTION_ISSUE", r"retraction.*issue|retraction.*problem|retraction.*fail|retract.*issue|retract.*problem|stringing|oozing|filament.*retract|retract.*setting|cfs retract|spool.*retract"),
    ("FIRMWARE_ERROR", r"firmware error|firmware.*fail|error:|err:|exception|crash|reset|firmware.*issue|firmware.*problem|firmware.*bug|downgrade firmware|upgrade firmware|firmware version|firmware update|custom firmware|start_print|gcode.*firmware|monochrome firmware|multicolor firmware|web interface.*missing|touchscreen.*firmware"),
    ("HARDWARE_FAULT", r"hardware error|hardware fault|board error|mainboard error|control board|board.*fail|board.*issue|board.*problem|motherboard|mainboard.*replacement|hotend board|toolhead board|extruder board|replacement.*board|wrong plug|wiring.*issue|connector.*issue|cable.*issue|wire.*break|wiring.*fail|stepper.*motor.*replacement|y-axis.*replacement|x-axis.*replacement|z-axis.*replacement|shaft.*replacement|bearing.*replacement|pulley.*replacement|belt.*replacement|waste chute.*broken|chute.*broken|part.*replacement|replacement part|specifications.*supplied"),
    ("CONNECTIVITY_ERROR", r"connection lost|disconnected|timeout|wifi.*error|network error|connect.*error|connect.*fail|won.*t connect|can.*t connect|connection.*issue|connection.*problem|buffering|keeps buffering|upload.*fail|gcode.*upload|send.*print.*fail|usb.*drive.*fail|insert.*usb.*fail|printer connection|moonraker.*disconnect|klipper.*disconnect|mcu.*disconnect"),
    ("CALIBRATION_ERROR", r"calibration failed|calibration error|pid.*fail|pid tuning|calibrat.*issue|calibrat.*problem|calibrat.*fail|shake.*calibrat|shaking.*calibrat|auto calibrat|sensorless.*calibrat|vibration.*calibrat|input shaper|resonance.*calibrat|accelerometer|adxl|input.*shaper|resonance"),
    ("PRINT_QUALITY", r"print quality|quality issue|quality problem|poor quality|bad quality|rough print|surface quality|dimensional accuracy|warp|warping|corner lift|edge lift|taco|taco heat bed|bed warp|bed.*warp|heat bed.*warp|k2 taco|first layer|first.layer|layer.*issue|layer.*problem|surface.*issue|surface.*problem|z seam|ghosting|ringing|vibration|artifact|defect|imperfection|rough|pillowing|top layer|bottom layer|infill.*issue|wall.*issue|perimeter.*issue|overhang.*issue|bridge.*issue|support.*issue"),
    ("MECHANICAL_ISSUE", r"mechanical.*issue|mechanical.*problem|frame.*issue|frame.*hit|hits frame|axis.*hit|bed.*jerk|jerking|vibration.*issue|wobble|loose.*belt|belt.*tension|belt.*loose|belt.*skip|pulley.*loose|grub.*screw|set.*screw|alignment|misaligned|rail.*issue|linear.*rail|bearing.*issue|rod.*issue|z.*axis.*issue|x.*axis.*issue|y.*axis.*issue|dual.*z.*sync|z.*sync|lead.*screw|trapezoidal.*screw|ball.*screw"),
    ("ERROR_CODE", r"error code|error.*\d{3,}|\b\d{4,}\b.*error|error \d+|code \d+|fo\d+|tr\d+|e\d+\b|e\d+ error|halted.*kill"),
]


# ---------------------------------------------------------------------------
# Printer Model Patterns
# ---------------------------------------------------------------------------

MODEL_PATTERNS = [
    # Creality
    (r"\bender\s*3\s*(v2|v3|pro|neo|max|s1|ke)?\b", "Ender 3"),
    (r"\bender\s*5\s*(plus|pro|s1)?\b", "Ender 5"),
    (r"\bender\s*6\b", "Ender 6"),
    (r"\bender\s*7\b", "Ender 7"),
    (r"\bcr-?6\s*(se|max)?\b", "CR-6"),
    (r"\bcr-?10\s*(v2|v3|s4|s5|smart)?\b", "CR-10"),
    (r"\bcr-?30\b", "CR-30"),
    (r"\bcr-?200b\b", "CR-200B"),
    (r"\bk1\s*(c|max|se)?\b", "K1"),
    (r"\bk2\s*(plus)?\b", "K2"),
    (r"\bk3\b", "K3"),
    (r"\bhalot\s*(one|sky|lite|plus)?\b", "Halot"),
    (r"\bsermoon\s*(d1|d3)?\b", "Sermoon"),
    (r"\bsonic pad\b", "Sonic Pad"),
    # LulzBot
    (r"\btaz\s*(4|5|6|pro|workhorse)?\b", "TAZ"),
    (r"\bmini\s*(1|2|3)?\b", "Mini"),
    # Prusa
    (r"\bmk3\s*(s|\+)?\b", "MK3"),
    (r"\bmk4\s*(s)?\b", "MK4"),
    (r"\bmini\s*\+\b", "MINI+"),
    (r"\bxl\b", "XL"),
    (r"\bsl1\s*(s)?\b", "SL1"),
    # Bambu Lab
    (r"\bx1\s*(carbon|e)?\b", "X1"),
    (r"\bp1\s*(p|s)?\b", "P1"),
    (r"\ba1\s*(mini)?\b", "A1"),
    # Voron
    (r"\bvoron\s*(2\.4|trident|switchwire|legacy)?\b", "Voron"),
    # Boards / Firmware
    (r"\bklipper\b", "Klipper"),
    (r"\bmarlin\b", "Marlin"),
    (r"\breprapfirmware\b|\brrf\b|\bduet\b", "Duet/RepRapFirmware"),
    (r"\bskr\s*(1\.3|1\.4|2\.0|mini|e3|pico)?\b", "BTT SKR"),
    (r"\bbtt\b|\bbigtreetech\b", "BTT Board"),
    (r"\bramps\b", "RAMPS"),
    (r"\brambo\b", "RAMBo"),
    (r"\barchim\b", "Archim"),
    (r"\bmellow\b", "Mellow"),
    (r"\bfly\b", "Fly Board"),
]


# ---------------------------------------------------------------------------
# Firmware Type Inference
# ---------------------------------------------------------------------------

FIRMWARE_RULES = [
    (r"\bklipper\b", "Klipper"),
    (r"\bmarlin\b", "Marlin"),
    (r"\bk1\b|\bk2\b|\bk3\b|\bender\s*3\s*(s1|ke|neo)\b|\bcreality os\b", "Creality OS"),
    (r"\bbambu\b", "Bambu Lab"),
    (r"\bmk3\b|\bmk4\b|\bmini\+\b|\bxl\b|\bsl1\b|\bprusa\b", "Prusa Firmware"),
    (r"\btaz\b|\bmini\s*(1|2|3)?\b|\blulzbot\b", "Marlin"),
    (r"\bvoron\b", "Klipper"),
    (r"\bduet\b|\brrf\b|\breprapfirmware\b", "RepRapFirmware"),
    (r"\bskr\b|\bbtt\b|\bbigtreetech\b", "Klipper"),  # Often Klipper on BTT
    (r"\bender\s*3\b|\bender\s*5\b|\bcr-?10\b|\bcr-?6\b", "Marlin"),
]


def classify_fault_type(title: str) -> str:
    """Classify a topic title into one fault type."""
    title_lower = title.lower()
    for fault_code, pattern in FAULT_PATTERNS:
        if re.search(pattern, title_lower, re.IGNORECASE):
            return fault_code
    return "OTHER"


def extract_printer_model(title: str, tags: List = None) -> str:
    """Extract printer model from title and tags."""
    search_text = title.lower()
    if tags:
        # Tags from Discourse API can be strings or dicts with 'name' key
        tag_names = []
        for tag in tags:
            if isinstance(tag, str):
                tag_names.append(tag)
            elif isinstance(tag, dict) and "name" in tag:
                tag_names.append(tag["name"])
        if tag_names:
            search_text += " " + " ".join(tag_names).lower()

    for pattern, model in MODEL_PATTERNS:
        if re.search(pattern, search_text, re.IGNORECASE):
            return model

    return "Unknown"


def infer_firmware_type(title: str, model: str) -> str:
    """Infer firmware type from title and model."""
    search_text = (title + " " + model).lower()

    for pattern, firmware in FIRMWARE_RULES:
        if re.search(pattern, search_text, re.IGNORECASE):
            return firmware

    return "Unknown"


def classify_topic(topic: Dict) -> Dict:
    """Classify a single topic, returning enriched dict."""
    title = topic.get("title", "")
    tags = topic.get("tags", [])

    fault_type = classify_fault_type(title)
    model = extract_printer_model(title, tags)
    firmware = infer_firmware_type(title, model)

    result = topic.copy()
    result["fault_type"] = fault_type
    result["printer_model"] = model
    result["firmware_type"] = firmware
    result["has_fault_indicator"] = fault_type != "OTHER"
    result["views"] = topic.get("views", 0)
    result["reply_count"] = topic.get("reply_count", 0)

    return result


def classify_topics(topics: List[Dict]) -> List[Dict]:
    """Classify a list of topics."""
    return [classify_topic(t) for t in topics]


def get_fault_distribution(classified: List[Dict]) -> Dict[str, int]:
    """Get fault type distribution for topics with fault indicators."""
    dist = {}
    for t in classified:
        if t.get("has_fault_indicator"):
            ft = t.get("fault_type", "OTHER")
            dist[ft] = dist.get(ft, 0) + 1
    return dist


def get_model_distribution(classified: List[Dict], fault_type: str = None) -> Dict[str, int]:
    """Get printer model distribution, optionally filtered by fault type."""
    dist = {}
    for t in classified:
        if not t.get("has_fault_indicator"):
            continue
        if fault_type and t.get("fault_type") != fault_type:
            continue
        model = t.get("printer_model", "Unknown")
        if model != "Unknown":
            dist[model] = dist.get(model, 0) + 1
    return dist


def get_top_fault_models(classified: List[Dict], top_n: int = 10) -> Dict[str, Dict[str, int]]:
    """Get printer model distribution for top N fault types."""
    fault_dist = get_fault_distribution(classified)
    top_faults = sorted(fault_dist.items(), key=lambda x: x[1], reverse=True)[:top_n]

    result = {}
    for fault_type, _ in top_faults:
        result[fault_type] = get_model_distribution(classified, fault_type)

    return result


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python3 classify.py <topics.jsonl>")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        topics = [json.loads(line) for line in f]

    classified = classify_topics(topics)

    # Print summary
    fault_dist = get_fault_distribution(classified)
    total_with_fault = sum(fault_dist.values())
    print(f"Total topics: {len(topics)}")
    print(f"Topics with fault indicators: {total_with_fault}")
    print(f"\nFault type distribution:")
    for ft, count in sorted(fault_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ft}: {count}")

    print(f"\nTop 10 fault types model coverage:")
    top_models = get_top_fault_models(classified, 10)
    for ft, models in top_models.items():
        print(f"  {ft}: {len(models)} models - {sorted(models.items(), key=lambda x: x[1], reverse=True)[:5]}")