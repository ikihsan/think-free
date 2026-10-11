#!/usr/bin/env python3
"""E092 grades, sample rows 21-40.

Split out of `grades.py` at the 300-line cap. Each grade is
written against the thread's own convergence (its highest-scored
answers, its accepted answer, and the asker's follow-up where one
exists), with the reason the attempt did or did not meet the
protocol's served definition. These are the last 20 rows of the
40-row sample (screening ranks 44-87); `grades_sample_1_20.py`
holds the first half. The grades live apart from the writer so a change to
the code that records them cannot silently rewrite the record the
experiment's gates are computed from.
"""

# qid -> (served, thread_resolution, reason)
GRADES_SECOND = {
24395: (True,
 "examine how the agitator attaches to the drive shaft — it is "
 "slipping, or the clutch is slipping (top answer, score 2); a "
 "rubber-band return in the drain/spin switch also fails (score 1)",
 "The attempt names the clutch (in the thread's top answer) and "
 "the timer-advance check, with a diagnostic path consistent with "
 "the thread's reasoning. The agitator-slip and rubber-band "
 "causes are not named."),
243267: (True,
 "the door interlock switches: a sagging door changes the "
 "microswitch sequence and trips the breaker (top answer, score "
 "14); a switch shorting to frame on door-open (score 10); the "
 "asker's follow-up confirms it was the switches' timing — "
 "primary and secondary must open top-first",
 "The attempt names the interlock-switch class and the door-"
 "alignment/actuator cause, matching the thread's convergence and "
 "its confirmed resolution, with the stop-using-it safety action."),
78102: (True,
 "the plug is not making good connection at the outlet — a high-"
 "resistance connection that heats (top answer, score 1); "
 "hotspots are very bad, replacement plugs cost about $4",
 "The attempt's cause class (loose/corroded plug-to-outlet "
 "contact, damaged cord at the strain relief) matches the thread's "
 "top answer, and its actions (check prongs, feel the outlet, "
 "replace the cord or outlet) are the thread's fixes."),
30950: (True,
 "yes — typical for gas stovetops without a standing pilot: all "
 "igniters fire in parallel from one module to reduce complexity "
 "(accepted answer, score 9; explained independently at scores 3 "
 "and 1)",
 "The attempt states the thread's resolution — shared ignition "
 "module, typical behavior — plus the abnormal variant (sparking "
 "that continues after lighting) that the thread's answers imply "
 "is the failure mode."),
140208: (True,
 "the evaporator and condensate: brush the coils, clean the "
 "evaporation tank/pan, and confirm the condensate drains (top "
 "answer, score 1); spores/bacteria on the evap coils (score 0); "
 "a comment warns a burnt-winding smell could be a motor meltdown",
 "The attempt names the evaporator/pan class the thread "
 "converges on, with the dry-the-coil and clean-the-pan actions "
 "the thread's answers give."),
82817: (True,
 "the igniter: the asker's follow-up comment records that a "
 "technician replaced the igniter and the oven worked — matching "
 "the accepted answer's hypothesis (score 1)",
 "The attempt's primary hypothesis is the weak igniter (glows but "
 "cannot hold the valve open), with the watch-the-glow test the "
 "thread implies — the thread's confirmed resolution."),
111339: (True,
 "the surface element controller has failed; replace it (accepted "
 "answer, score 4, confirmed by the comments' part numbers)",
 "The attempt names the same component (infinite switch / surface "
 "element controller) and the same action — replace it, matched to "
 "the burner's wattage."),
20524: (True,
 "the heating element had a break on its hidden back side — found "
 "by resistance testing and replaced (accepted answer, score 0, "
 "the asker's own follow-up); an in-line thermal protection device "
 "is the other named cause (score 2)",
 "The attempt names the thermal fuse first (the standard #1 cause) "
 "and the heating element second with the continuity test that is "
 "exactly how the thread's resolution was found."),
105058: (True,
 "test the pump motor's own leads for continuity — 25 megohms "
 "through the motor in the asker's follow-up: the motor is shot "
 "(accepted answer, score 2, names the correct wires)",
 "The attempt names the pump motor, its drive relay/board, and "
 "the wiring, and prescribes the continuity test on the pump "
 "motor that the thread's resolution used."),
13812: (True,
 "check the circuit breaker first (flip off and on), then route "
 "the call: an electrician or a large appliance repair shop "
 "(accepted answer, score 5; score 4 names the repair shop); the "
 "asker's follow-up: the elements and the probe tested fine, and "
 "the service sticker inside the drawer was used",
 "The attempt names the breaker check (the thread's first action) "
 "and the lost-240V-leg differential that the follow-up's "
 "good-elements result is consistent with, and routes to the same "
 "two trades the thread names."),
133777: (True,
 "replace the thermostat next to the fuse — it is reading low or "
 "failing intermittently, so the dryer runs hotter than the "
 "control allows (accepted answer, score 3: 'the thermostat "
 "solved it after I went through about 5 thermal fuses')",
 "The attempt names the sensor-fault class the thread's accepted "
 "answer confirms (a temperature sensor driving excess heat) with "
 "a resistance check against measured temperature, plus the "
 "airflow checks the thread's other answers give. The specific "
 "part is the thermostat, not the thermistor the attempt names."),
99584: (True,
 "the heating coil had a broken circuit in one of its three legs, "
 "found with a multimeter and replaced (the asker's own follow-up, "
 "score 1)",
 "The attempt names the cracked-element class (passes cold, opens "
 "hot) — the thread's resolution — with the resistance test that "
 "found it, and the terminal-connection check the mechanism "
 "implies."),
185008: (False,
 "insufficient vaporization/pressure: operate one device at a time "
 "(score 28) and hold the low-pressure side above 11 inches of "
 "water column with all appliances firing — below that, look for "
 "an obstruction (accepted answer, score 25, from a propane "
 "service technician)",
 "The attempt names bad propane, a faulty regulator, and an air "
 "leak — the thread's minority causes — and its actions (gas-"
 "quality analysis, leak-down) would not find the vaporization/"
 "pressure problem the thread converges on, whose test is a "
 "water-column gauge under full load."),
146599: (False,
 "a frozen coil from low refrigerant: the asker left it off for a "
 "day, the coil thawed, and it worked again; a shirtsleeve "
 "diagnosis in the comments ties the full condensation tray to a "
 "frozen coil and low Freon",
 "The attempt's cause class (start relay, overload, seized "
 "compressor) does not match the thread's converged cause (frozen "
 "coil / low refrigerant), and its resolution (thaw, check the "
 "charge) is absent."),
28904: (False,
 "a control-board fault: there was an undiscovered third magnetic "
 "switch below the fridge door, and pressing buttons on the "
 "control board fixed the light (accepted answer, score 2, with "
 "the asker's and commenters' follow-ups)",
 "The attempt's crossed-wiring hypothesis was not the cause: the "
 "thread's resolution was the control board and an undiscovered "
 "switch, neither of which the attempt names."),
147813: (True,
 "no fault was found: the asker's follow-up (accepted answer, "
 "score 4) records the latest bulb lasting 10+ months — a streak "
 "of bad bulbs; the comments give the real differential (loose "
 "socket, supply voltage, a loose neutral in the panel)",
 "The attempt's differential (socket contact, bulb rating, supply "
 "voltage) is the thread's diagnostic path, and its tests would "
 "correctly conclude 'no fault' on this machine — which is what "
 "the thread found."),
261313: (True,
 "the wiring/phase configuration: hobs are mostly single-phase "
 "despite the 'three-phase' name — check the terminal mapping "
 "against the diagram and the supply against the rating plate "
 "(accepted answer, score 7, with the volt-meter and breaker-count "
 "checks of scores 4 and 2)",
 "The attempt names the terminal-mapping, phase-arrangement, and "
 "supply-matching classes the thread converges on, with the same "
 "actions (re-check terminal-for-terminal, confirm supply matches "
 "the plate)."),
132790: (True,
 "an AFCI breaker tripping on a genuine arc fault — poor contacts "
 "and back-stabbed connections top the hit-list (top answer, "
 "score 3); the comments add undersized wire and shared neutrals",
 "The attempt names the arc-fault class (loose/damaged connection, "
 "back-stabs) and the isolation test (move the microwave to "
 "another circuit) that the thread's answers imply — an exact "
 "overlap with the thread's convergence."),
235566: (False,
 "a heating element with deteriorated insulation: the magnesium-"
 "oxide tube expands when hot and shorts the inner wire to the "
 "sheathing — replace the elements (top answer, score 17); a bad "
 "breaker is 'less likely'",
 "The attempt's primary (a failing breaker, stove probably fine) "
 "is the thread's less-likely cause, and its action (replace the "
 "breaker) is not the thread's resolution (replace the elements)."),
46163: (True,
 "insufficient water flow to the ice maker: the clamp-on saddle "
 "valve was the restriction; soldering in a 1/4-inch brass line "
 "with a proper shut-off valve fixed it permanently (top answer, "
 "score 4)",
 "The attempt's primary class (low water pressure/flow to the ice "
 "maker) and its supply-side checks (valve open, line not kinked, "
 "weak tap flow on the same line) are the thread's resolution "
 "class — the saddle valve is a supply restriction."),
}
