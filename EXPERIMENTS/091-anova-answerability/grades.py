"""E091 grade table: the reader's per-row judgements, as data.

Separated from `score.py` so the computation has no say over its own inputs, and
so the three defects found in the inherited harness (see RESULT.md §2) are
visible here rather than buried in arithmetic.

Each GRADES entry is (id, served, reason, attempt_first, tool_shaped):

  served        bool. Does this row's attempt contain the remedy the thread
                converged on? For unresolved threads, is it a specific, correct,
                actionable remedy? Graded against the thread, never against the
                instrument's confidence.
  reason        str. Why. Kept so a reader can disagree with any single row.
  attempt_first bool. Was the attempt written from the first post alone, BEFORE
                the thread was read? This is an explicit flag, not a string
                match: the inherited harness inferred it by searching the reason
                prose for 'PRIOR EXPOSED', which silently reclassified ten
                thread-exposed rows as attempt-first and reported 18 where the
                harness's own comment says 7.
  tool_shaped   bool. Arm A: is the remedy a self-contained program? Not
                contact-the-vendor, not a hardware repair, not waiting on a
                firmware fix, not a fact. Reported beside Arm B, never gating it
                (AMENDMENT-1 §4 design correction).
"""

# id, served, reason, attempt_first, tool_shaped
GRADES = [
    ("86", False,
     "MISS. Attempt guessed the PIN is 0000 and that pairing uses a printed label. "
     "The thread's answer is that there IS no PIN: the device pairs through the app, "
     "not through a system PIN prompt. The attempt's stated low confidence was "
     "correct; its content would have sent the user down a wrong path. NOTE: the "
     "need itself is answerable - this is an instrument error, not a servability limit.",
     True, False),
    ("12241", True,
     "HIT. Attempt's item 1 (join the 2.4 GHz SSID during setup) and item 3 (unplug "
     "30s, delete from app, reboot phone and router, re-pair) are exactly the fixes the "
     "thread reports working, including reply [4] 'phone connected to a 2.4 network' and "
     "reply [14] 'restarted my phone after restarting the Anova and the router'. The "
     "thread also surfaces a cause the attempt missed - spaces in SSID or password - but "
     "the graded criterion is whether the attempt resolves the stated problem, and it does.",
     True, False),
    ("1096", False,
     "PARTIAL MISS. Attempt ranked water level first and said 'if it beeps with correct "
     "water level and an immersed probe, it is a unit fault'. The thread has a specific "
     "user repair at reply [18], confirmed by reply [16], and the attempt's own fallback "
     "- unit fault, return it - is the majority advice (replies [5]-[15] are support "
     "replies offering return/exchange). Graded unserved: the attempt does not contain "
     "the fix.",
     True, False),
    ("5021", False,
     "HIT on mechanism, MISS on outcome. Attempt correctly identified the sensor/ADC "
     "failure and said 'not user-fixable, expect service replacement'. The thread's "
     "convergent answer (reply [9], expanded over [11]-[19]) is a $3 TM7707 ADC "
     "replacement the user performed. Graded unserved because the attempt does not "
     "contain the remedy that resolved it, even though its diagnosis was right.",
     True, False),
    ("722", True,
     "HIT. Attempt's lead recommendation - a photography C-clamp - is precisely the fix "
     "in reply [13] ('I fixed mine twice! My solution is an aluminum C-clamp... for as "
     "little as about $10'), the most-endorsed user workaround in the thread. Reply [4] "
     "(cup hook) and [9] (3D-printed bracket) are alternatives the attempt gestured at.",
     True, False),
    ("26273", False,
     "MISS. Attempt asserted the thermostat/thermal fuse was at fault and that the gasket "
     "was not. The thread's convergent user fix is the opposite in the cases that "
     "resolved: reply [8] 'both times it was fixed by cleaning the seal and sealing "
     "surface', and reply [4] on bag handling / over-filling. Reply [7] does name a failed "
     "vacuum sensor, so the attempt's neighbourhood was not absurd, but it led with the "
     "wrong cause. The need itself is answerable - instrument error, not a servability limit.",
     True, False),
    ("717", True,
     "HIT. Attempt said there is no snooze, that the beep cannot be stopped from the app, "
     "and offered a dampening workaround plus 'unplugging ends the cook'. The thread "
     "confirms all three: replies [5] and [8] ('the ONLY way to stop the beeping is to "
     "physically unplug'), and reply [11] from Anova staff confirming the timer button "
     "stops it. The attempt's core claim is the thread's core claim.",
     True, False),
    # ---- thread-exposed rows: graded, but excluded from the attempt-first subset ----
    ("12736", False,
     "THREAD-EXPOSED. No attempt was written. Reply [5] converges on a physical steam "
     "shield and a UPS; the remedy is an artifact, not an answer. Recorded as a missing "
     "observation, never as a zero.",
     False, False),
    ("4261", False,
     "THREAD-EXPOSED. No attempt was written. The thread's answer is a vendor product "
     "decision ('currently it cannot, but it is a feature we are planning on "
     "implementing'), which is not assistant-answerable in any case.",
     False, False),
    ("9165", False,
     "THREAD-EXPOSED. No attempt was written. Reply [1] from staff is a loose stainless "
     "skirt plus contact-support. An assistant would say the same, but the grade is not "
     "attempt-first and is reported apart.",
     False, False),
    ("9020", False,
     "THREAD-EXPOSED. No attempt was written. The stated problem is an alarm re-firing "
     "each time the bath rounds to setpoint. Reply [2] has support walking the user "
     "through pressing the triangle button twice; reply [11] finds a reseated coil "
     "housing. Not assistant-answerable: the fix arrived by phone call.",
     False, False),
    ("6924", False,
     "THREAD-EXPOSED. No attempt was written. The thread's answer to the literal question "
     "is that there is no PIN and pairing happens in the app (replies [1], [8]) - that "
     "part is answerable. The thread never resolved: the user hit an app-availability "
     "wall on a non-Play-Store tablet and gave up at reply [7]; the only path offered "
     "was an APK sideload (reply [9]). Graded unserved. CORRECTED: the inherited "
     "harness set served=False while its reason text read 'Graded served on that "
     "basis'. Resolved to False because the thread does not converge and the residual "
     "blocker is a software-availability fact no explanation reaches - the direction "
     "that does not inflate the served share.",
     False, False),
    ("132", False,
     "THREAD-EXPOSED. No attempt was written. Low-water alarm on a three-week-old unit. "
     "Reply [5] connects the two sensors with a jumper wire after staff reply [1] calls "
     "the unit defective and offers a return. A general assistant does not know this repair.",
     False, False),
    ("4681", True,
     "THREAD-EXPOSED. No attempt was written. The thread's resolution is the documented "
     "credential constraint - replies [9] and [11] give Anova's own rule that the Wi-Fi "
     "password must be 8-18 characters with no special characters, linking the support "
     "article - plus reply [1] on disabling 5 GHz. That is public vendor documentation an "
     "assistant could produce.",
     False, False),
    ("3051", False,
     "THREAD-EXPOSED. No attempt was written. Wrong SKU delivered; the remedy is a "
     "support return/exchange resolved by staff escalating the ticket (replies [14], "
     "[17], [19]). An order-record action.",
     False, False),
    ("8811", False,
     "THREAD-EXPOSED. No attempt was written. Broken password-reset deep link; reply [4] "
     "'manual intervention by the support team'. An assistant cannot fix a vendor's "
     "broken reset token.",
     False, False),
    ("10550", False,
     "THREAD-EXPOSED. No attempt was written. App timer resetting to blank; replies [3] "
     "and [8] converge on 'a bug, the product team knows', and reply [17] confirms it "
     "still occurring in January 2019. An assistant can say 'this is an app bug' but "
     "cannot fix it, and the thread's remedy is waiting on the vendor.",
     False, False),
    ("13044", False,
     "THREAD-EXPOSED. No attempt was written. Timer/temperature unit confusion; reply [2] "
     "is the dev team aware and working on it. Not assistant-answerable.",
     False, False),
    ("12987", False,
     "THREAD-EXPOSED. No attempt was written. Missing iOS push notifications; reply [10] "
     "is a confirmed vendor bug and reply [17] reports the vendor had abandoned the "
     "forum. Not assistant-answerable.",
     False, False),
    ("5115", True,
     "THREAD-EXPOSED. No attempt was written. The user asks the technical reason the "
     "phone must be on 2.4 GHz during setup. Reply [1] gives exactly that: the unit's "
     "radio is 2.4 GHz 802.11b/g/n only and the app passes the credentials over that "
     "band. Public hardware documentation an assistant can produce.",
     False, False),
]

# Arm A is assessed on EVERY row. The inherited harness carried notes for 10 and
# divided tool_shaped by all 20, scoring 10 unassessed rows as False - a
# denominator that understated the rate by construction.
ARM_A_NOTES = {
    "86": "Remedy is 'the app does the pairing' - a vendor design fact, not a program.",
    "12241": "Remedy is router/network configuration. A program could diagnose; the fix is "
             "in the asker's network.",
    "1096": "Remedy alternates between a user repair and a vendor return/exchange.",
    "5021": "Remedy is component-level board work - a physical repair.",
    "722": "Remedy is a physical C-clamp. That is an artifact, not a program.",
    "26273": "Remedy alternates between cleaning, bag handling, and a control-board part.",
    "717": "Remedy is a mute the vendor declined to build. No program serves it.",
    "12736": "Remedy is a steam shield and a UPS - artifacts.",
    "4261": "Remedy is a vendor product decision, deferred for years.",
    "9165": "Remedy is a warranty claim or a physical repair.",
    "9020": "Remedy is a button sequence arrived at by a support phone call, or a reseated "
            "coil housing. NEW THIS SESSION - previously unassessed.",
    "6924": "Remedy is sideloading the vendor's APK. NEW THIS SESSION - previously "
            "unassessed.",
    "132": "Remedy is a jumper wire between two sensors - hardware repair. NEW THIS SESSION "
           "- previously unassessed.",
    "4681": "Remedy is changing a Wi-Fi password to meet the vendor's documented rule. "
            "Nearest miss in the set: a checker for the vendor's published credential "
            "constraint is a program, but it is a one-off against one vendor's published "
            "document and the vendor's own setup wizard covers it. NEW THIS SESSION - "
            "previously unassessed.",
    "3051": "Remedy is a return/exchange against an order. NEW THIS SESSION - previously "
            "unassessed.",
    "8811": "Remedy is manual account intervention by the vendor's support team. NEW THIS "
            "SESSION - previously unassessed.",
    "10550": "Remedy is a vendor software fix. NEW THIS SESSION - previously unassessed.",
    "13044": "Remedy is a vendor software fix. NEW THIS SESSION - previously unassessed.",
    "12987": "Remedy is a vendor software fix. NEW THIS SESSION - previously unassessed.",
    "5115": "Remedy is a hardware specification, already in the app's docs. NEW THIS SESSION "
            "- previously unassessed.",
}
