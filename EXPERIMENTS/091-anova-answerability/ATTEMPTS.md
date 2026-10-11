<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E091 Arm B — assistant attempts, written from first post only

Written **before** the thread outcomes for these rows were read, per
`AMENDMENT-1.md` §4. The instrument is this model answering from its own
knowledge, per E062/E066.

Three rows (`12736`, `4261`, `9165`) are marked **prior_exposed**: I read their
threads while inspecting the repaired data, before writing any attempt. They are
excluded from the headline number and reported apart.

Each attempt is graded later against the thread, not against my confidence.

---

**86 — Bluetooth PIN** (69 552 views) — *prior_exposed: no*

> The Bluetooth PIN for Anova devices is **0000**... actually I am not confident
> of that. What I can say: the PIN is printed on the label on the bottom of the
> unit and in the packaging insert; the default pairing PIN for Anova's
> Bluetooth is `0000` on most units. Pairing requires the phone to be on the
> 2.4 GHz-equivalent setup for Wi-Fi models; for Bluetooth-only pairing the app
> must be installed. On the Android app availability question — the Anova app
> shipped for both platforms from launch, so if Play Store does not show it,
> their phone's region or Play Store account is filtering it, or the APK must be
> sideloaded from Anova's site.

*Confidence: low on the exact PIN; high on the app-availability half.*

**12241 — won't connect to WiFi** (45 961 views) — *prior_exposed: no*

> This is the most common first-week failure and it is almost always one of:
> 1. The cooker only supports the **2.4 GHz** band and the phone/router is on 5 GHz or a
>    band-steering mesh. Join the 2.4 GHz SSID during setup, then move back.
> 2. The password entered is the Wi-Fi password but the network is WPA3-only or has
>    no separate 2.4 GHz SSID.
> 3. Not actually unpaired — unplug the cooker 30 s, delete it from the app, reboot the
>    phone and router, and pair again.
> 4. 5 GHz-only router or a mesh node that will not bridge the two bands.
>
> Re-pairing from scratch resolves most of these.

*Confidence: high.*

**1096 — long lasting beep** (30 587 views) — *prior_exposed: no*

> A continuous beep from an Anova Precision Cooker is almost always **not** the water
> level. In order of likelihood:
> 1. **Water below the minimum line** — the unit beeps continuously rather than the
>    usual alert when the level drops mid-cook (evaporation over a long cook).
> 2. **Temperature not reached within the timeout** — a long cook on high setpoint with a
>    large volume can exceed the heat-up allowance.
> 3. **Probe not submerged / not touching the food** — reads low, never reaches setpoint.
> 4. **Dry-heating** — running with no water at all.
>
> Refill past the min line mid-cook and confirm the probe is immersed. If it beeps with
> correct water level and an immersed probe, it is a unit fault.

*Confidence: medium-high on the water-level-first ordering.*

**5021 — current temp stuck at 32 degrees** (23 790 views) — *prior_exposed: no*

> A stuck current temperature with the motor running means the heating element is
> energised and the circulation works, but the **temperature sensor is not reading**.
> The 32 °C figure is characteristic of a failed/loose thermistor or a broken trace on
> the display board. This is not a user-fixable condition: it needs the sensor or board
> replaced. Check the probe is seated in the water and the app is not merely showing a
> stale reading after a reconnect — force-quit and reopen the app to rule that out —
> but if the displayed current temp never moves, expect a service replacement.

*Confidence: medium-high that this is a hardware fault, low on the specific repair.*

**722 — clamp broken, alternatives?** (20 464 views) — *prior_exposed: no*

> Yes — this is a common workaround and it does not need the vendor:
> - **A photography C-clamp** clamped around the pot rim is the standard fix.
> - **A large binder clip or two**, if the clamp's jaw is the failure.
> - **A carabiner**, or a strap clamp wrapped around the pot and hooked to a fixed
>   point above.
> - Silicone tubing or a handle strap looped around the pot and secured.
>
> Any of these holds the circulator against the pot wall so the sleeve stays submerged.

*Confidence: high on the C-clamp; medium on the alternatives.*

**26273 — vacuum seal not sealing** (19 200 views) — *prior_exposed: no*

> Sucking air with no heat is a **thermostat or thermal-fuse failure**, not a gasket
> problem — the gasket would let air in, but the pump running with the heater never
> engaging points at the heat-cut thermostat or the thermal fuse on the sealing bar.
> Test: if it still sucks and never heats, it is the thermostat/fuse. If the gasket were
> the issue the unit would reach vacuum and then the seal would fail to hold, which is a
> different symptom. Gaskets are not usually sold separately; the seal bar assembly is a
> replaceable part through support, otherwise the sealer is not economically repairable.

*Confidence: medium-high on thermostat/fuse over gasket.*

**717 — snooze the beep?** (17 020 views) — *prior_exposed: no*

> There is no snooze on the Anova Precision Cooker — the alarm is a fixed repeating alert
> and the unit does not stop it from the app. Workarounds:
> - Put a towel or cloth over the top of the unit to damp the buzzer (it does not stop
>   the alert logic, only muffles it).
> - The beep is also tied to the water level sensor; keeping the level above the min
>   line changes the alert.
> - Unplugging is the only hard stop, which ends the cook.
>
> A feature request for a mute is the only real fix.

*Confidence: high that no snooze exists; medium on the towel trick's effectiveness.*

---

**12736 — shuts off during cooks** — **PRIOR EXPOSED** (thread read before this attempt)

**4261 — connect more than one phone** — **PRIOR EXPOSED**

**9165 — straighten the impeller** — **PRIOR EXPOSED**
