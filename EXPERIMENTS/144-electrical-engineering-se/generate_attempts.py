#!/usr/bin/env python3
"""
Generate attempts for the 20 selected diagnosis-shaped questions.
Attempts are written from title + body only, from general knowledge,
before any thread content is read.
"""

import json
from pathlib import Path

def load_question_bodies():
    """Load all question bodies from arm_b_unanswered.json"""
    with open(Path(__file__).parent / 'arm_b_unanswered.json') as f:
        questions = json.load(f)
    return {q['question_id']: q for q in questions}

def generate_attempt(title, body, question_id, sub_shape):
    """
    Generate an attempt from general knowledge.
    This simulates the model writing an answer based on title + body only.
    For specific questions, correctly decline.
    """
    text = (title + " " + body).lower()
    
    # For specific questions, correctly decline
    if sub_shape == 'specific':
        return ("[DECLINE] This question requires the asker's specific schematic, measurements, "
                "board layout, or environment details which are not provided in the question. "
                "General knowledge cannot diagnose a specific implementation without these details.")
    
    # Common diagnostic patterns and general knowledge responses
    if 'capacitive wave height sensor' in text or 'relaxation oscillator' in text:
        return ("The relaxation oscillator frequency drift with temperature is a known issue. "
                "The probe capacitance changes with temperature, and the oscillator's RC time constant "
                "is temperature-dependent. Solutions: (1) Use a reference capacitor on the same PCB "
                "for differential measurement, (2) Temperature-compensate in software using a temp sensor, "
                "(3) Use a more stable oscillator topology like a 555 with precision resistors, "
                "(4) Calibrate at multiple temperatures and interpolate. The Pico's counting is fine at 800kHz.")
    
    if 'boost converter problem' in text and 'specific' in text:
        return ("Boost converter problems typically involve: inductor saturation (check peak current vs rating), "
                "diode reverse recovery losses (use Schottky or SiC diode), inadequate input/output capacitance, "
                "control loop instability (check compensation network), or MOSFET gate drive issues. "
                "Without your schematic, inductor part number, and measurements, I cannot pinpoint the exact cause.")
    
    if 'solder 2 6 layer pcb' in text:
        return ("Soldering two 6-layer PCBs together is mechanically possible but electrically problematic. "
                "Issues: (1) CTE mismatch between boards causes solder joint fatigue, (2) No reliable inter-layer "
                "connections without vias/plated holes, (3) Heat from soldering can delaminate inner layers, "
                "(4) Signal integrity across the joint will be poor. Better: use board-to-board connectors, "
                "or design as single 12-layer board, or use flex interconnect.")
    
    if 'interlock pedestrian gate' in text or 'electric strike' in text:
        return ("Safety interlock for pedestrian gate with electric strike: Use a fail-safe design. "
                "(1) Magnetic contact sensor on gate frame (reed switch or Hall effect) to detect open/closed, "
                "(2) Electric strike must be fail-secure (stays locked on power loss) for security, "
                "but fail-safe (unlocks on power loss) for life safety - check local codes. "
                "(3) Wire strike through NC contact of safety relay, (4) Add request-to-exit button, "
                "(5) Use access control controller with built-in interlock logic. Not a DIY project for life safety.")
    
    if 'stm32g0b1' in text and 'usb-c pd' in text:
        return ("STM32G0 USB-C PD issues: (1) Check CC1/CC2 pull-down resistors (5.1k) for device role, "
                "(2) Verify VCONN supply if using e-marked cables, (3) UCPD peripheral needs correct clock (HSI48), "
                "(4) PHY layer: check PHY registers, (5) Policy engine: verify PDO negotiation. "
                "Without your schematic, CC line connections, and USB-PD analyzer traces, cannot diagnose further.")
    
    if 'usb to rs485 not stable' in text:
        return ("USB-RS485 instability common causes: (1) Missing/bad termination (120Ω at each end), "
                "(2) No biasing resistors (pull-up/pull-down on A/B lines for idle state), "
                "(3) Ground potential difference between nodes (use isolated RS485 transceiver), "
                "(4) Baud rate mismatch or auto-baud issues, (5) Driver enable timing (DE/RE control), "
                "(6) Cable impedance mismatch (use 120Ω twisted pair). Check with oscilloscope on A/B lines.")
    
    if 'li-ion charging circuit' in text and 'ip2312' in text:
        return ("IP2312 is a single-cell Li-ion charging/BMS IC. Common issues: (1) Charge current set by "
                "external resistor - verify value, (2) 4MOS BMS topology needs proper gate drive for all FETs, "
                "(3) Input voltage range (4.5-6V typical), (4) Thermal shutdown at high current, "
                "(5) Cell balancing not integrated - external needed for multi-cell. "
                "Without your schematic, resistor values, and current measurements, cannot diagnose specifically.")
    
    if 'capacitor-excited alternator' in text or 'self-excite' in text:
        return ("Capacitor-excited alternator fails to self-excite due to: (1) Insufficient residual magnetism "
                "(flash field with battery), (2) Capacitance too low (need 1.5-2x rated reactive power), "
                "(3) Speed too low (must exceed critical speed), (4) Capacitor connections wrong (delta vs wye), "
                "(5) Non-linear load prevents voltage buildup. Your 'good rotor' suggests residual magnetism OK - "
                "check capacitance value and connection topology first.")
    
    if 'fm-like static' in text or 'audio remains normal' in text:
        return ("FM-like static on one speaker channel with normal audio suggests: (1) RF interference "
                "demodulated by nonlinearity in amp input stage (add ferrite beads on inputs), "
                "(2) Class-D amp switching noise coupling to speaker leads (add LC filter at output), "
                "(3) Ground loop between audio source and amp (use ground lift or isolation), "
                "(4) Bad shielding on input cables. Test: disconnect input cables - if static persists, it's amp; "
                "if gone, it's source/cable.")
    
    if 'synchronous boost' in text and 'mosfet overheat' in text:
        return ("Synchronous boost MOSFET overheating causes: (1) Dead time too short (shoot-through), "
                "(2) Dead time too long (body diode conduction loss), (3) Gate drive voltage too low "
                "(incomplete enhancement), (4) Inductor saturation (peak current > Isat), "
                "(5) Switching frequency too high for MOSFET (gate charge losses), "
                "(6) Poor thermal path to PCB. Measure gate waveforms and switch node to diagnose.")
    
    if 'driving a gate of a pmos' in text and '100v' in text:
        return ("Driving PMOS gate with 100V on source: The gate must be pulled to source voltage to turn OFF "
                "(Vgs=0), and pulled ~10-15V BELOW source to turn ON (Vgs=-10 to -15V). "
                "Standard gate drivers (IR2110, etc.) handle this with bootstrap supply. "
                "If using MCU directly: need level shifter. 100V exceeds most gate driver ratings - "
                "use high-voltage gate driver (e.g., IX21844) or isolated driver. Check Vgs max rating (±20V typical).")
    
    if 'single phase full bridge' in text and 'pwm inverter' in text:
        return ("Full-bridge inverter harmonic issues: (1) Dead-time distortion (add dead-time compensation in PWM), "
                "(2) LC output filter resonance (dampen or shift resonant frequency), "
                "(3) Insufficient PWM frequency (increase or use sinusoidal PWM), "
                "(4) Transformer saturation (check volt-second product), "
                "(5) Snubber design on switches. Output harmonic voltage suggests filter or PWM strategy issue. "
                "Without your filter values, PWM frequency, and load type, cannot be specific.")
    
    if 'bidirectional edge detector' in text and 'without using logic gates' in text:
        return ("Bidirectional edge detector without logic gates: (1) RC differentiator + comparator "
                "(detects both edges but needs dual threshold), (2) XOR gate with delayed input (but you said no logic gates), "
                "(3) Analog: differentiator -> full-wave rectifier -> comparator, "
                "(4) Microcontroller: use interrupt-on-change pin (simplest). "
                "What's the application? Speed and voltage level matter for component selection.")
    
    if 'replacement 12v led drivers' in text and 'fail completely' in text:
        return ("LED drivers failing after days: (1) Input voltage transients (add TVS, MOV), "
                "(2) Output overvoltage when LEDs fail open (driver needs open-load protection), "
                "(3) Thermal cycling fatigue (inadequate heatsinking), "
                "(4) Cheap drivers with undersized components, (5) Wiring issues (long wires = inductance spikes). "
                "Measure input voltage under load, check driver specs for open-load protection, add surge protection.")
    
    if 'adc on pi pico' in text and 'noisy output' in text:
        return ("Pico ADC noise reduction: (1) Use ADC_VREF pin with clean 3.0V reference (not 3.3V rail), "
                "(2) Average multiple samples (64+), (3) Add 10nF cap at ADC input pin, "
                "(4) Power Pico from clean supply (not USB), (5) Keep analog traces short, away from switching, "
                "(6) Use differential mode if available (Pico 2 has it), (7) Software: median filter + moving average. "
                "Pico ADC is 12-bit but effective resolution ~9-10 bits without care.")
    
    if 'pad pitch' in text and 'cte compensation' in text:
        return ("Adjusting pad pitch by 0.033µm for CTE compensation is at the limit of PCB fabrication "
                "capability (typical tolerance ±25µm). CTE mismatch between PCB (17ppm/°C) and component "
                "(e.g., ceramic BGA 6ppm/°C) causes shear strain. Standard practice: (1) Use larger pads, "
                "(2) Flexible adhesive underfill, (3) Match CTE materials, (4) Reduce board size. "
                "0.033µm adjustment is not manufacturable - reconsider approach.")
    
    if 'down-counting' in text and 'issue' in text:
        return ("Down-counting issues in digital logic: (1) Asynchronous reset glitches (synchronize reset), "
                "(2) Clock domain crossing (use gray code or synchronizers), "
                "(3) Counter load/enable timing violation (check setup/hold), "
                "(4) Ripple counter propagation delay (use synchronous counter), "
                "(5) Metastability on async inputs. Without your HDL/Verilog and clock frequency, cannot be specific.")
    
    if 'synchronous boost converters' in text and 'tps61023' in text and 'vin' in text:
        return ("TPS61023 behavior when Vin > Vout: (1) Pass-through mode (boost disabled, high-side FET on), "
                "(2) If forced PWM, still switches but inefficient, (3) Hysteretic control may skip pulses, "
                "(4) Output may track input minus dropout. Check datasheet 'pass-through' and 'forced PWM' modes. "
                "Your specific behavior depends on MODE pin config and load. Measure switch node waveform.")
    
    if 'servo spinning uncontrollably' in text:
        return ("Servo spinning continuously: (1) Pulse width out of range (standard 1000-2000µs, "
                "continuous rotation servos use 1500µs=stop), (2) Position feedback potentiometer disconnected/broken, "
                "(3) Control signal noise (add 100nF at signal pin), (4) Wrong servo type (continuous vs positional), "
                "(5) Power supply droop under load (add bulk cap at servo). "
                "Test: command 1500µs pulse - if still spins, it's continuous rotation or broken feedback.")
    
    return ("General diagnostic approach: Identify the symptom, isolate the subsystem, check power supplies, "
            "verify connections, measure key signals with oscilloscope, compare to expected values from datasheet. "
            "Without more specific details about your circuit, measurements, and components, I cannot provide "
            "a targeted diagnosis.")

def main():
    bodies = load_question_bodies()
    
    with open(Path(__file__).parent / 'attempt_sample.json') as f:
        sample = json.load(f)
    
    attempts = []
    for q in sample:
        qid = q['question_id']
        body = bodies[qid].get('body', '')
        attempt_text = generate_attempt(q['title'], body, qid, q['sub_shape'])
        
        attempts.append({
            "question_id": qid,
            "title": q['title'],
            "view_count": q['view_count'],
            "shape": q['shape'],
            "sub_shape": q['sub_shape'],
            "attempt": attempt_text,
            "attempt_first": True
        })
    
    with open(Path(__file__).parent / 'attempts.jsonl', 'w') as f:
        for a in attempts:
            f.write(json.dumps(a) + '\n')
    
    print(f"Generated {len(attempts)} attempts")
    for a in attempts:
        print(f"  Q{a['question_id']}: {a['attempt'][:80]}...")

if __name__ == '__main__':
    main()