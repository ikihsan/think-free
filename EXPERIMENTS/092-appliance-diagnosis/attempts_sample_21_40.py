#!/usr/bin/env python3
"""E092 attempt arm, sample rows 21-40.

Split out of `attempts.py` at the 300-line cap. These are the
attempts for the last 20 rows of the 40-row sample (screening ranks 44-87 of
the 150-row screen),
each written from the question's title and body only, from general
knowledge, before any answer, comment, or accepted flag was read.
They live apart from the writer so a change to the code that records
the attempts cannot silently rewrite them; `attempts_sample_1_20.py`
holds the sample's first half. The split is positional only: the
attempts were written in one pass, in sample order, and no remedy
class crosses the midpoint.
"""

# qid -> (class, attempt)
ATTEMPTS_SECOND = {
24395: ("answerable",
 "Agitates but will not spin, with the coupler, pump, and lid switch "
 "verified, points to the clutch and brake assembly (the clutch "
 "engages spin only after the timer advances) or the timer never "
 "reaching spin. First confirm the timer actually advances to the "
 "spin position; if it does and the tub still does not spin, the "
 "clutch or brake is the fault — a common wear item on the Kenmore "
 "80 series. The agitator being stoppable by hand during spin is "
 "consistent with the transmission not engaging spin."),
243267: ("answerable",
 "A microwave that trips the breaker exactly when the door opens "
 "mid-heat points to a door interlock switch arcing or shorting as it "
 "changes state, or a grounding fault in the door harness. Stop using "
 "it, check the door hooks and the door's alignment against the "
 "switch actuators (a misaligned door makes a switch bounce), and "
 "expect to replace the interlock switches. Do not run it with a "
 "door switch defeated."),
78102: ("answerable",
 "A power cord that warms near the plug end and is more pliable there "
 "localizes the fault: a damaged cord at the strain relief, or a "
 "loose or corroded plug-to-outlet contact. Stop using it, check the "
 "cord entry for a cracked strain relief and the prongs for corrosion, "
 "and feel whether the outlet itself is warm (a worn outlet is the "
 "other cause). A heater draws its full load, so a poor connection "
 "heats up; the cord or the outlet must be replaced before use."),
30950: ("answerable",
 "On many stoves the igniters share one ignition module wired so that "
 "all of them spark while any burner calls for ignition, so all five "
 "sparking while one lights is typical behavior — the abnormal version "
 "is sparking that continues after the burner lights. Watch whether "
 "the sparking stops the moment the burner catches: if it stops and "
 "the burner lights reliably, this is normal; if it continues, one "
 "igniter's switch is shorted and should be replaced."),
140208: ("answerable",
 "A smell that appears only in fan mode after cooling, fades in about "
 "two minutes, and disappears when cooling resumes is the evaporator: "
 "in AC mode the coil is cold and dry; in fan mode it warms, and the "
 "moisture on it mildews or the condensate pan sours. Run fan mode "
 "with the vent open to dry the coil, clean the filter and the "
 "condensate pan, and confirm the condensate is draining (portable "
 "units either evaporate it or need a drain). A smell that returns "
 "within a day means the pan or coil needs a cleaner."),
82817: ("answerable",
 "A gas oven that shuts off shortly after preheat and reignites when "
 "the surface burners are clicked points to a weak igniter: it glows "
 "but does not draw enough current to hold the gas valve open, so the "
 "valve closes; clicking a burner resets the circuit. Watch the "
 "igniter during the failure — a dull orange glow instead of bright "
 "white confirms it. The igniter is a cheap, common part; the gas "
 "valve and thermostat are the next suspects if the igniter glows "
 "brightly."),
111339: ("answerable",
 "One burner stuck at medium-high regardless of the knob is the "
 "burner's infinite switch: a failed switch can feed continuous "
 "partial power to that one burner. Turn the breaker off and inspect "
 "the switch wiring for a short; the switch itself is the part to "
 "replace, and it must match the burner's wattage. If the burner "
 "stays hot with the knob off, the switch is welded or shorted and "
 "must be replaced before further use."),
20524: ("answerable",
 "A dryer that spins but never heats, with the timed-dry knob "
 "advancing but auto-dry not, points to the heating circuit: the "
 "thermal fuse first (the #1 cause of spins-but-no-heat; it sits on "
 "the blower housing and kills heat while leaving the motor running), "
 "then the heating element and the thermostats; auto-dry not advancing "
 "adds the moisture sensor to the list. Test the thermal fuse for "
 "continuity, then the element and each thermostat, and check the "
 "sensor contacts."),
105058: ("answerable",
 "A dishwasher that fills, heats, and drains while the wash pump "
 "never runs — relay clicks, no hum, no fault codes — points to the "
 "pump motor, the relay or control board driving it, or the wiring to "
 "the pump: the control thinks it ran. With power off, check the pump "
 "connector for corrosion and the pump motor for continuity; an open "
 "motor means a pump replacement, a good motor means the relay or "
 "board. The clicking relay with a dead motor is the key symptom."),
13812: ("repair",
 "Both elements dead with controls and light working is almost never "
 "two elements at once: it is a lost 240 V leg (120 V still runs "
 "controls and lights but heats nothing), a failed oven relay on the "
 "control board, or the elements' wiring. Check the breaker (a "
 "half-tripped breaker kills one leg) and measure the outlet voltage "
 "(200-240 V). If voltage is right, an appliance tech should check "
 "the relay and element wiring; if a leg is dead, an electrician is "
 "the right call. The diagnosis is knowledge; the fix is a part or a "
 "circuit repair."),
133777: ("answerable",
 "A thermal fuse that blows every few months with a clear exhaust and "
 "a good element points to what the fuse is protecting against: on an "
 "outdoor dryer, ambient heat and lint ingress, or a failing "
 "thermistor reading high and driving the heater until the fuse "
 "opens. Verify exhaust airflow under load, check the thermistor's "
 "resistance against the measured 61-71C, and confirm the machine is "
 "rated for outdoor use — an indoor-rated dryer in sun will overheat. "
 "The fuse is the messenger, not the fault."),
99584: ("answerable",
 "Error E64 means the control sees an open heater circuit; a dryer "
 "that heats fine for ten to twenty minutes and then throws E64 has a "
 "connection that opens when hot: a failing heater terminal (thermal "
 "expansion breaking a marginal crimp), a cracked element (passes "
 "cold, opens hot), or a failing thermal cutout. Check the heater "
 "terminals for heat discoloration and retorque them; test the "
 "element cold and remember a cracked element can pass cold. Clean "
 "connections point to the heater assembly."),
185008: ("vendor",
 "Orange flames with soot on every propane appliance, a backfiring "
 "generator, and two regulators already replaced points to the supply "
 "itself: bad propane, a still-faulty regulator or second stage, or a "
 "leak drawing air into the line. Stop using the appliances (soot "
 "means incomplete combustion and a CO risk) and ask the propane "
 "company for a gas-quality test, simultaneous pressure readings at "
 "every appliance, and a leak-down test with the system pressurized "
 "and isolated. Appliance-level fixes cannot address a problem the "
 "generator shares."),
146599: ("answerable",
 "Lights on but no compressor or fan sound at all means the "
 "compressor is not starting: the start relay or overload (most "
 "common, especially after years in storage), a seized compressor, or "
 "rarely a stuck defrost timer. A full condensation tray says it ran "
 "and defrosted. Unplug, check the relay on the compressor (a rattling "
 "relay has loose guts), and the overload; if the compressor hums "
 "but does not start, the compressor may be seized. After long "
 "storage, oil settles and relays stick — replace the relay before "
 "condemning the compressor."),
28904: ("answerable",
 "A fridge light that only comes on when the freezer door opens means "
 "the door-switch wiring is crossed: the freezer switch is wired into "
 "the fridge light circuit, or the two switches' leads are swapped. "
 "Check the wiring at both door switches against the diagram; this is "
 "a wiring job, not a part. If the wiring is correct, one switch's "
 "contact is cross-conducting and should be replaced. It is a "
 "low-voltage repair once the panel is off."),
147813: ("answerable",
 "Oven bulbs burning out every week or two across several brands "
 "points to heat or voltage: a loose socket contact (arcing kills "
 "bulbs), a bulb not rated for oven use, or high supply voltage. "
 "Check the socket for a loose or corroded contact (wobble the base), "
 "confirm replacements are oven-rated (not LED unless the oven says "
 "so), and measure the supply voltage at the outlet — over about 125 "
 "V kills bulbs. A loose socket contact is the most common cause of "
 "rapid bulb death."),
261313: ("answerable",
 "Error 4U00 on a Bosch hob right after wiring means the hob detected "
 "an installation fault: the 5-wire connection is wrong (terminal "
 "mapping, phase, neutral, or earth), the supply does not match the "
 "hob's rating, or a connection is loose or a strand is shorting "
 "between terminals. Turn the power off and re-check the wiring "
 "terminal-for-terminal against the hob's diagram, confirm the supply "
 "voltage and phase arrangement match the rating plate, and inspect "
 "for stray strands. The manual's 4U00 entry names the exact fault; "
 "a mis-wired terminal is the most common cause."),
132790: ("answerable",
 "Outlets that die or a breaker that pops when a microwave runs "
 "points to an overloaded or damaged circuit: the microwave's "
 "1000-1500 W draw on a shared circuit, or a loose or damaged "
 "connection in the flipped house's wiring (a bad neutral is the "
 "classic — outlets die and breakers pop under load). Move the "
 "microwave to a different circuit and test; check the outlet's "
 "wiring (back-stabbed connections are a common failure in flipped "
 "houses) and the breaker itself. If it follows the microwave, the "
 "microwave is the fault; if it stays on the circuit, the wiring or "
 "breaker is."),
235566: ("answerable",
 "A breaker that is hot to the touch and pops when the oven calls for "
 "full heat is most likely failing itself: a weak contact heats and "
 "trips under load, and the stove is probably fine. Have an "
 "electrician replace the breaker and check the wire torque at its "
 "terminals (a loose wire heats the breaker the same way). If a new "
 "breaker still pops at high heat, then the oven's element or wiring "
 "is shorting — but a hot breaker is the breaker's own signature."),
46163: ("answerable",
 "Hollow, shell-like ice cubes are the signature of low water "
 "pressure to the ice maker or a faulty water inlet valve: the mold "
 "does not fill before the freeze cycle ends. Check the supply valve "
 "is fully open and the line is not kinked, and clear the inlet "
 "valve's screen; if a sink tap on the same line runs weakly, house "
 "pressure is the cause. If pressure is good at a tap, the inlet "
 "valve is the likely fault. A too-warm fridge or a mis-level fridge "
 "can also make hollow ice, but pressure is the first check."),
}
