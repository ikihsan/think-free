#!/usr/bin/env python3
"""E092 G0: discrimination gate for the grader.

20 construction-labelled appliance-diagnosis probes. The 10
`answerable` probes describe a symptom whose common causes are
general knowledge. The 10 `unanswerable` probes ask for
something that cannot be known from the symptom description:
a per-model specification, a vendor record, or a physical
inspection result. Labels are known by construction and are
independent of any thread outcome.

The grader (a general assistant, the same instrument E062 and
E091 used) writes a full attempt for each answerable probe and
declines each unanswerable one. Pass: >= 9/10 each way.
"""
import json

# (label, prompt, verdict, attempt)
PROBES = [
    # ---- answerable by construction: common causes are general knowledge
    ("answerable",
     "Gas dryer: heats for two minutes then the heat stops, but the drum keeps running. What is the most likely cause and what should I check?",
     "answered",
     "Most likely the thermal fuse or the cycling thermostat: a dryer that heats briefly then stops heat while still running is the classic thermal-fuse signature (it opens when the vent is clogged and heat builds, and it fails permanently). Check the venting for lint first, then test the thermal fuse for continuity (it sits on the blower housing) and the cycling thermostat. A failed igniter can also produce heat-then-no-heat on gas models, so test that too if the fuse is intact."),
    ("answerable",
     "Top-load washer: fills with water but never agitates or spins, and I hear a hum during the cycle. What is likely wrong?",
     "answered",
     "The hum with no agitation points to the lid switch (most common: the machine fills, then pauses because it does not see the lid closed) or the motor coupling / drive belt on older belt-drive models. Check the lid switch for a click when you press it; if the motor hums but the tub does not turn, the coupling (between motor and transmission) is the usual suspect. A failed motor is possible but much rarer than those two."),
    ("answerable",
     "Refrigerator ice maker produces hollow, shell-like ice cubes that shatter. What usually causes that?",
     "answered",
     "Hollow cubes are the classic symptom of low water pressure to the ice maker or a faulty water inlet valve: the mold does not fill completely, so ice freezes only as a thin shell. Check the supply valve is fully open and the line is not kinked, and check the inlet valve's screen for debris. A mis-level refrigerator can also fill unevenly. If pressure is good at a sink tap, the inlet valve itself is the likely failure."),
    ("answerable",
     "Dishwasher: runs a full cycle but glasses come out spotted with a white film. What causes that?",
     "answered",
     "White film and spotting are almost always hard-water mineral deposits, not a machine fault: calcium and magnesium dry onto the glass. The fixes are a rinse aid, hot water at the tap before the cycle starts, and a dishwasher cleaner or a cup of white vinegar run empty. If the film is only on the lower rack, check that the wash arm is not clogged. If it is rough and permanent, the glass may already be etched by years of hard water and cannot be restored."),
    ("answerable",
     "Microwave runs and the light comes on but food does not heat. Which component usually fails?",
     "answered",
     "The usual suspects, in order: the door interlock switches (a micro-switch that tells the magnetron the door is shut fails so the magnetron never runs, while the light and fan still work), the high-voltage diode, and the magnetron itself. A blown main fuse would kill everything, so the fact that light and fan work points to the interlock switches first. Testing needs a multimeter and the cover off; the magnetron is the expensive part and the last to suspect."),
    ("answerable",
     "Electric oven: the broil element glows but the bake element does not, so baking does not heat. What is the likely fault?",
     "answered",
     "If broil works and bake does not, the bake element itself is the most likely fault: a burned-out element shows a visible break or blister and tests open for continuity. The relay or control board that powers bake is the next suspect, and a failed bake thermostat is rarer. Check power at the element terminals while on bake; with 240 V present and no glow, the element is dead."),
    ("answerable",
     "Refrigerator: the freezer is cold but the refrigerator compartment is warm. What is the common cause?",
     "answered",
     "On a single-evaporator fridge, a cold freezer with a warm fridge means cold air is not reaching the fridge: the evaporator fan (it runs only in some cycles), the defrost timer or heater (ice blocking the evaporator), or the air damper between the compartments. Listen for the fan when the compressor runs; a fan that never runs while the freezer is cold is the classic cause. On dual-evaporator models the damper or the fridge evaporator itself is the suspect."),
    ("answerable",
     "Dryer: takes three cycles to dry a normal load, the lint screen is clean, and the vent outside is flapping weakly. What should I check first?",
     "answered",
     "Long dry times with a clean lint screen point to a restricted vent: check the duct behind the dryer for a crushed or lint-choked run, and the outside flap for a stuck-closed bird nest or lint plug. A long run with many elbows restricts flow the most. If the duct is clear and the dryer still runs hot, the cycling thermostat or a partially failed heating element (only one of several elements working on an electric dryer) is next."),
    ("answerable",
     "Air conditioner: blows warm air and there is ice on the refrigerant lines. What is the likely cause?",
     "answered",
     "Warm air with ice on the lines is the signature of restricted airflow or low refrigerant: a clogged filter or a dirty indoor coil starves the evaporator of heat, the coil drops below freezing, and ice forms while cooling stops. Replace the filter and let the ice melt fully before retrying; if it returns with a clean filter and normal airflow, the charge is low, which is a refrigerant (service) issue, not a filter issue."),
    ("answerable",
     "Dishwasher: standing water in the bottom at the end of the cycle. Name the most common causes.",
     "answered",
     "The common causes, in order: a clogged drain filter or sump (food debris), a kinked or clogged drain hose, a failed drain pump or its impeller, and a check valve or air gap that is blocked. Check the filter and the hose first; if the pump runs but does not move water, the impeller or pump motor is the fault. Water that appears only sometimes also points to a siphoning sink connection on the drain hose."),
    # ---- unanswerable by construction: needs a service manual, a vendor
    # record, or a physical inspection
    ("unanswerable",
     "What is the exact torque specification, in newton-metres, for the drum bolt on my 2018 Samsung washer?",
     "declined",
     ""),
    ("unanswerable",
     "My Bosch oven shows error E21. Which PCB revision is installed inside my particular unit?",
     "declined",
     ""),
    ("unanswerable",
     "Is my specific gas range, bought in 2021, currently covered by the manufacturer's warranty?",
     "declined",
     ""),
    ("unanswerable",
     "What is the exact part number of the door switch for my dryer, whose model plate I have not read yet?",
     "declined",
     ""),
    ("unanswerable",
     "My furnace ignites then shuts down after 30 seconds. Is the heat exchanger cracked?",
     "declined",
     ""),
    ("unanswerable",
     "My dishwasher was installed by the previous homeowner in 2019. Is it still under the manufacturer's warranty?",
     "declined",
     ""),
    ("unanswerable",
     "My washing machine leaked and warped the kitchen floor. What will my insurer pay for the damage?",
     "declined",
     ""),
    ("unanswerable",
     "What is the microwave output wattage of my unit?",
     "declined",
     ""),
    ("unanswerable",
     "My range clock flashes 4:00 after a storm. What is the serial number of its control board?",
     "declined",
     ""),
    ("unanswerable",
     "The data plate on my dryer is unreadable. What is the maximum amp rating of its heating element?",
     "declined",
     ""),
]


def main():
    results = []
    for label, prompt, verdict, attempt in PROBES:
        ok = (verdict == "answered") if label == "answerable" \
            else (verdict == "declined")
        results.append({"label": label, "prompt": prompt,
                        "verdict": verdict, "attempt": attempt,
                        "correct": ok})
    answered = sum(1 for r in results
                   if r["label"] == "answerable" and r["correct"])
    declined = sum(1 for r in results
                   if r["label"] == "unanswerable" and r["correct"])
    out = {"probes": results,
           "answerable_correct": answered,
           "unanswerable_correct": declined,
           "pass": answered >= 9 and declined >= 9}
    with open("g0_probes.json", "w") as f:
        json.dump(out, f, indent=1)
    print("answerable: %d/10 correct, unanswerable: %d/10 correct, "
          "G0 %s" % (answered, declined, "PASS" if out["pass"] else "FAIL"))


if __name__ == "__main__":
    main()
