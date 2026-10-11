#!/usr/bin/env python3
"""E092 grades, sample rows 1-20.

Split out of `grades.py` at the 300-line cap. Each grade is
written against the thread's own convergence (its highest-scored
answers, its accepted answer, and the asker's follow-up where one
exists), with the reason the attempt did or did not meet the
protocol's served definition. These are the first 20 rows of the
40-row sample (screening ranks 2-43); `grades_sample_21_40.py`
holds the rest. The grades live apart from the writer so a change to
the code that records them cannot silently rewrite the record the
experiment's gates are computed from.
"""

# qid -> (served, thread_resolution, reason)
GRADES_FIRST = {
3969: (True,
 "drain water siphoning back through the low drain run to the "
 "utility sink (top answer, score 8); the accepted answer names "
 "the clogged front filter instead",
 "The attempt's primary hypothesis is the thread's top-voted "
 "cause (drain water backing up, drain-hose height) and its "
 "actions (drain-only cycle, check the drain path) cover the "
 "accepted answer's class as well."),
21181: (True,
 "a dirty or worn timer-switch — the 'sweet spot' is worn timer "
 "contacts or gears (top answer, score 4); several lower answers "
 "name the lid/door switch",
 "The attempt names the timer/cycle switch first and the lid "
 "switch second, matching both of the thread's cause classes, "
 "with the drain-the-tub action the thread also gives."),
41231: (True,
 "air in the system: a new filter is full of air; bleed it by "
 "dispensing or by refilling the filter in the sink (top answer, "
 "score 5)",
 "The attempt's first hypothesis is an air lock and its first "
 "action is to dispense two to three gallons — the thread's "
 "resolution, verbatim."),
32313: (True,
 "a bleach/cleaner cycle for a modern water-saving machine, plus "
 "a drain-path check if standing water persists (accepted answer, "
 "score 5); other answers name the sump, the drain-hose loop and "
 "sewer gases",
 "The attempt names the sump/drain class and prescribes the hot "
 "empty cycle with a dishwasher cleaner — the accepted answer's "
 "action — with the drain-hose check the other answers add."),
16434: (True,
 "isolate the three possibilities first — the machine, the "
 "downstream wiring, or the GFCI outlet itself — by swapping the "
 "outlet (accepted answer, score 2); a leaking pump and starved "
 "inlet screens appear in lower answers",
 "The attempt names machine-side ground faults and includes the "
 "thread's key first action: test on another outlet to isolate "
 "the machine from the outlet."),
186085: (True,
 "grease or nothing beats oil here; the black film is lubricant "
 "plus dust; use a dry lubricant (spray Teflon or graphite) — "
 "accepted answer, score 8",
 "The attempt agrees on the cause (degraded lubricant or surface "
 "wear), agrees oil/grease is the wrong choice, and prescribes "
 "cleaning plus dry lubrication — the thread's resolution. The "
 "wax-motor/solenoid naming in the attempt is the same component "
 "class the thread names."),
1171: (True,
 "check the vent's exit flap first — outside air is coming in "
 "(accepted answer, score 14); the 25-foot run with two elbows "
 "may exceed the vent length limit (score 6), and moist air "
 "condensing in the vent is the mechanism (score 1)",
 "The attempt names the condensation mechanism, the vent-length "
 "problem, and the damper/flap check — all three of the thread's "
 "answers — with insulation and a shorter run as the actions."),
3113: (True,
 "the vent from freezer to fridge has frozen over with ice — warm "
 "the freezer to melt it (top answer, score 15); the evaporator "
 "fan (score 2) and the door alignment (score 3) also appear",
 "The attempt's two named causes are the thread's top two "
 "mechanisms (blocked/frozen vent, evaporator fan), with the "
 "overnight-wait and fan-listen actions the thread gives."),
38026: (True,
 "a supply-side problem: contamination or water in the line "
 "(accepted answer, score 9); the gas-company technician's own "
 "resolution for a similar report was a household humidifier "
 "(score 5)",
 "The attempt correctly classifies the row vendor-side and routes "
 "to the gas company for a gas-quality analysis and regulator "
 "inspection — the accepted answer's class. The humidifier cause "
 "is not named."),
74802: (True,
 "the beeper was simply turned off: press and hold COOK TIME for "
 "five seconds to turn tones on (accepted answer, score 2, from "
 "the Owner Manual); a breaker reset also worked for another user",
 "The attempt's first hypothesis is the sound setting and its "
 "first action is the manual check, followed by the control "
 "reset — the thread's two resolutions in order."),
25889: (False,
 "the water under the drum is supposed to be there; the smell is "
 "the rubber lining — bleach wash and prop the door open (top "
 "answer, score 1); a pinched drain hose appears only in a "
 "comment",
 "The attempt's primary hypothesis (incomplete draining) is "
 "contradicted by the thread's top answer, and its resolution "
 "(mildew maintenance, ventilation) is absent. The drain-hose "
 "check the attempt does name matches a comment, not an answer."),
4700: (True,
 "the household drain: a clogged flexible drain hose (top answers, "
 "score 4 x2 — blow into the hose to test; the crawlspace run can "
 "freeze), and the wrong hose entirely (score 1)",
 "The attempt names the drain-side class the thread converges on "
 "and prescribes the same isolation test (run the hose into a "
 "bucket), which is the thread's blow-into-the-hose test."),
100820: (False,
 "chloramine in the water supply attacks the molded plastic "
 "reservoir, releasing white flakes — the filter is not the cause "
 "and the reservoir must be replaced (top answer, score 2)",
 "The attempt names the wrong class (mineral sediment, carbon "
 "fines) where the thread converges on the reservoir plastic, and "
 "its resolution (replace the reservoir / remove the filter) is "
 "absent. Flushing is shared, but the fault class is not."),
244273: (True,
 "the suspension rods (accepted answer, score 1: primary suspicion, "
 "with leveling re-checked); the rod's elastomer damper "
 "disintegrates and the rods must be replaced as a set (score 0); "
 "the asker's service tech quoted the drum bearing/axle at half a "
 "new machine",
 "The attempt names worn suspension and leveling first — the "
 "thread's primary suspicion — then the bearings, matching the "
 "asker's own narrowed diagnosis and the follow-up comment."),
78804: (True,
 "the automatic defroster is out (check the defrost heater, limit "
 "switch, or timer) or a badly closing door seal is letting humid "
 "air in (both score 1)",
 "The attempt names both causes with the same tests: a full "
 "defrost, then the gasket check, then the defrost components if "
 "the ice returns quickly — the thread's differential, in order."),
100808: (True,
 "check the leveling first (cheap fix); if it is the bearings the "
 "repair is expensive and often means replacing the machine; "
 "continuing to run it damages the drum and shaft (top answers, "
 "score 2 x2)",
 "The attempt names the bearing class the thread and the asker's "
 "hypothesis converge on, answers the question asked (consequences "
 "of continued use: spin-tube and outer-tub wear), and gives the "
 "by-hand spin test the thread's answers imply."),
44874: (False,
 "swap the fridge's breaker with another of the same rating to "
 "test whether the breaker has de-rated itself — the cheapest, "
 "fastest first test (top answer, score 2)",
 "The attempt's cause class (compressor start relay, grounded "
 "winding) does not include the thread's top answer — a failing "
 "breaker — and none of the attempt's actions would find it. The "
 "question asked what to look at FIRST; the thread says the "
 "breaker."),
44314: (False,
 "the defrost heaters are not turning off — a stuck thermal "
 "switch or timer keeps them running, which heats the cabinet "
 "(top answer, score 4)",
 "The attempt names condenser coils, condenser fan, and the "
 "compressor/charge — a different cause class from the thread's "
 "top answer — and none of its actions would find a stuck defrost "
 "heater."),
36138: (True,
 "the detergent cup's cover is not opening: the solenoid that "
 "pulls the catch fails and needs replacement (accepted answer, "
 "score 8; confirmed by score 4)",
 "The attempt names the pop mechanism (wax motor / solenoid — the "
 "same component class) and the cup-stuck alternative, with the "
 "free-movement test the thread's description implies."),
57462: (True,
 "a ground fault: a short between hot and ground somewhere between "
 "the plug and the compressor — possibly the receptacle itself "
 "(top answer, score 1); a defrost-element oxidation ground fault "
 "appears in a lower answer",
 "The attempt's cause class (wire-to-ground fault from damaged "
 "insulation, beginning at defrost) matches the thread's, and its "
 "actions (dry fully, inspect insulation, ohm each wire to the "
 "frame) would find the fault the thread describes."),
}
