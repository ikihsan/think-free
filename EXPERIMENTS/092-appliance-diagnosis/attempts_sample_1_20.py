#!/usr/bin/env python3
"""E092 attempt arm, sample rows 1-20.

Split out of `attempts.py` at the 300-line cap. These are the
attempts for the first 20 rows of the 40-row sample (the sample's
highest-arrival half, screening ranks 2-43 of the 150-row screen),
each written from the question's title and body only, from general
knowledge, before any answer, comment, or accepted flag was read.
They live apart from the writer so a change to the code that records
the attempts cannot silently rewrite them; `attempts_sample_21_40.py`
holds the sample's other half. The split is positional only: the
attempts were written in one pass, in sample order, and no remedy
class crosses the midpoint.
"""

# qid -> (class, attempt)
ATTEMPTS_FIRST = {
3969: ("answerable",
 "Water that appears half an hour after a load and smells foul is "
 "drain water getting back into the tub, not fresh water: the usual "
 "causes are a drain hose set too low (water siphons back), a failed "
 "check valve or drain-pump seal, or a leaking door bellow (which "
 "would give fresh water). Check the drain hose height against the "
 "manual (it must rise to the recommended height before turning down), "
 "run a drain-only cycle and watch for seep-back, and inspect the "
 "bellows. Foul smell means the drain side; clean-smelling water means "
 "the door seal."),
21181: ("answerable",
 "Stuck full of water before the rinse cycle, fixable only by finding "
 "a knob sweet spot, points to an intermittent electrical contact in "
 "the timer/cycle switch or its knob, or a lid switch the machine does "
 "not see. Drain the tub first (emergency drain or a hose lowered to "
 "floor level), then check the lid switch for a click. If the machine "
 "only advances when the knob is wiggled, the timer or the knob's "
 "wiring pads are the fault; on an Ultimate Care II the timer is the "
 "common wear item for exactly this symptom."),
41231: ("answerable",
 "Slow dispenser flow immediately after a filter change is usually an "
 "air lock in the filter housing, a filter that was not flushed, a "
 "partially closed saddle valve, or a wrong/clogged filter. Dispense "
 "two to three gallons to clear air, confirm the saddle valve is "
 "fully open, and check the seat seal for the leak seen at the "
 "housing. If flow stays slow after several gallons, the filter is "
 "clogged or the wrong part for that GE model."),
32313: ("answerable",
 "A rotting-garbage smell with standing water under the filter "
 "assembly means debris in the sump or a partially blocked drain: a "
 "clean filter does not clean the sump strainer or the drain. Remove "
 "the lower filter and sump cover, clear the strainer and the drain "
 "of food, check the drain hose for a clog, and run a hot empty cycle "
 "with a dishwasher cleaner. If the standing water is deep rather "
 "than the usual shallow puddle, the drain pump or its check valve is "
 "the fault."),
16434: ("answerable",
 "A washer that trips a GFCI mid-cycle has a ground fault: most often "
 "water from a leaking hose, pump seal, or inlet valve reaching a live "
 "part, or (on heated models) a cracked heating element grounding "
 "through the water. Dry the machine, check hoses and the pump area "
 "for leaks, and briefly test on a non-GFCI outlet to confirm the "
 "fault is in the machine rather than the outlet. Do not bypass the "
 "GFCI; a machine that trips it is unsafe until the leak is found."),
186085: ("answerable",
 "The black film on the axle is degraded lubricant or the nylon roller "
 "surface stripping, and these rollers are plain nylon bushings that "
 "are not meant to hold grease: oil and grease migrate and gum the "
 "bushing. Clean the axles and rollers of all old lubricant, dry "
 "thoroughly, and run them dry (nylon is self-lubricating) or with a "
 "silicone lubricant sparingly. Replace any roller with a flat spot or "
 "a crack. If the film reappears, the roller material itself is "
 "failing and the rollers should be replaced, not re-lubricated."),
1171: ("answerable",
 "Condensation that drips in a long, upward vent run in hot humid "
 "weather is the exhaust cooling and condensing in the attic section, "
 "then running back. Insulate the vent where it passes through the "
 "attic, keep the run as short and straight as the installation "
 "allows, and make sure the roof cap has a working damper. A crushed "
 "or lint-choked duct makes it worse. If the dryer is gas, have the "
 "installation checked for combustion safety before continuing to use "
 "it."),
3113: ("answerable",
 "After a fridge is left open all day, a cold freezer with a warm "
 "fridge points to cold air not reaching the fridge: the evaporator "
 "fan (it only runs in some cycles), a blocked vent between the "
 "compartments, or a defrost problem — or it may simply need 24 hours "
 "to recover. Listen for the fan whenever the compressor runs; if it "
 "never runs while the freezer is cold, the fan or its damper is the "
 "fault. Clear the vent and give it overnight before replacing "
 "anything."),
38026: ("vendor",
 "Orange flames on every gas appliance at once, with normal measured "
 "pressure, is a supply-side problem, not an appliance problem: "
 "pressure can be right while the gas itself is wrong, or a regulator "
 "is still faulty, or air is being drawn into the line. Stop using the "
 "appliances (soot means incomplete combustion and a CO risk) and ask "
 "the gas company specifically for a gas-quality analysis, a "
 "regulator inspection, and a leak-down test with the system "
 "pressurized and isolated. Appliance-level fixes cannot address a "
 "problem every appliance shares."),
74802: ("answerable",
 "The beeper works from the buttons but the timer-end signal does not "
 "sound, so the speaker is good and the fault is in the end-of-cycle "
 "signal path: a control setting (many Whirlpool ovens have a "
 "signal/sound on-off option) or the timer buzzer circuit. Check the "
 "manual for a sound or signal setting first, then reset the control "
 "(breaker off for one to two minutes). If the setting is on and the "
 "reset does not restore the end-of-cycle beep, the buzzer or its "
 "drive on the control board has failed."),
25889: ("answerable",
 "Water heard under the drum after the spin cycle, with a mildew "
 "smell, is incomplete draining: a clogged drain pump, a kinked drain "
 "hose, or a too-low standpipe. If the water is fresh-smelling "
 "instead, a leaking inlet valve dribbles water in continuously while "
 "the machine does not fully drain. Check the drain hose for clogs "
 "and the standpipe height, run a drain-only cycle and watch the pump, "
 "and treat the smell with a cleaner once the drain is clear."),
4700: ("answerable",
 "Two dishwashers in a row that do not drain, with the old one's hose "
 "and trap already cleaned, points to the household drain, not the "
 "machines: a clogged shared drain line, a blocked air gap, or a "
 "drain hose without the required high loop (which lets the machine "
 "siphon). Run the drain hose into a bucket: if the machine pumps "
 "freely into the bucket, the machine is fine and the shared drain "
 "line or air gap is the blockage; if it does not pump, the pump or "
 "its check valve is the fault."),
100820: ("answerable",
 "White filaments in fridge water right after a filter change are "
 "usually mineral sediment stirred up by the new filter's first flow, "
 "or carbon fines from a filter that was not flushed. Run two to four "
 "gallons through the dispenser to flush it. If the filaments persist "
 "after flushing, the supply lines are shedding scale (common after "
 "plumbing work) and the line should be flushed at the supply; a "
 "sediment filter at the supply is the durable fix. White and hard "
 "means scale; black means carbon fines."),
244273: ("answerable",
 "Out-of-balance with the lightest loads, banging, and repeated "
 "repositioning on a front-loader points to worn suspension shocks, "
 "tub bearings, or a leveling problem: worn shocks let the tub slam at "
 "spin even with small loads. Re-level the machine first (every foot "
 "should resist rocking with the door open), confirm no shipping bolts "
 "remain, and push the tub: it should resist, not swing. If leveling "
 "does not fix it, the shock absorbers or bearings need replacement; "
 "the service manual's balance test will confirm which."),
78804: ("answerable",
 "Ice that builds in the vent between freezer and fridge until it "
 "blocks airflow is the defrost system not clearing the evaporator, "
 "or humid air leaking past a door gasket. Defrost the vent fully "
 "(low heat, carefully, since the structure is foam), then check the "
 "freezer gasket with a dollar-bill test. If ice returns within days "
 "of a full defrost, the defrost heater, defrost thermostat, or "
 "defrost timer is the fault; if it returns slowly over weeks, the "
 "gasket is the leak."),
100808: ("answerable",
 "A spin-cycle noise that starts when the water is gone, without "
 "grinding or shaking, is most consistent with worn tub bearings or a "
 "worn spin tube: bearing noise is load-dependent and loudest when "
 "the empty tub spins fast. Open the cabinet and spin the tub by "
 "hand: a rumble that worsens with speed is the bearing; also inspect "
 "the belt and pulley for wear. If it is the bearings, continued use "
 "wears the spin tube and outer tub, so repair now rather than "
 "later."),
44874: ("answerable",
 "An intermittent breaker trip on a ten-year-old fridge in hot "
 "weather is most often the compressor start relay or overload "
 "(tripping on start, especially in heat), or a grounded winding from "
 "a damp connection after defrost. Watch the timing: a trip within "
 "seconds of the compressor starting points to the start relay; a "
 "trip after running points to the compressor or a grounded winding. "
 "Clean the condenser coils; an electrician can megger the winding to "
 "ground."),
44314: ("answerable",
 "Sides that are hot to 105F with loud running, when the machine used "
 "to run cool and quiet, is a change, and the technician's 'that is "
 "how it works' only holds for a clean machine: the usual cause is "
 "clogged condenser coils, then a failed condenser fan, then a "
 "compressor working too hard (low charge or wear). Clean the coils "
 "first and listen for the condenser fan; if coils and fan are clean "
 "and it still runs hot and loud, a service call for the compressor "
 "or charge is warranted."),
36138: ("answerable",
 "A detergent cup that never opens is usually the wax motor (the "
 "small cylinder that pops the cup) or a stuck, clogged cup — not "
 "the detergent brand. Check the cup for clogs and free movement by "
 "hand; if it moves freely but still will not pop during a cycle, "
 "the wax motor or its wiring is the fault, and it is a cheap, "
 "accessible part on most machines. Hot water and rinse aid will not "
 "fix a cup that never opens."),
57462: ("answerable",
 "The evidence in the question points to a ground fault from moisture: "
 "the ground wire reading 'all over the place' to the frame means "
 "damaged insulation or a chafed wire, and it began at defrost, when "
 "water enters connections. Leave the machine off and open for 24 "
 "hours to dry fully, then re-test. Inspect the ground wire's "
 "insulation and any wire routing near the frame or compressor for "
 "chafing, and ohm each wire to the frame one at a time. A machine "
 "that trips only when the ground is connected has a wire-to-frame "
 "fault and should not run until it is found."),
}
