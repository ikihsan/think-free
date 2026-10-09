<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E083 — Classification Rules for 3D Printer Fault Codes

Predeclared before any data inspection. Used by `classify.py`.

**AMENDMENT 1 (2026-10-09):** Patterns significantly expanded based on preliminary data inspection showing narrow patterns missed many fault topics. Original patterns were too specific to firmware error codes; real forum titles use diverse symptom language.

## Fault Type Taxonomy

Each topic title is classified into **one primary fault type** based on the most specific matching pattern. Patterns are checked in order (most specific first).

| Fault Type Code | Label | Title Patterns (case-insensitive) | Description |
|---|---|---|---|
| THERMAL_RUNAWAY | Thermal Runaway | `thermal runaway`, `thermal protection`, `thermal cutoff`, `safety.*temp` | Thermal protection triggered |
| MINTEMP | Min Temp Error | `mintemp`, `min temp`, `minimum temp` | Thermistor reads below minimum |
| MAXTEMP | Max Temp Error | `maxtemp`, `max temp`, `maximum temp` | Thermistor reads above maximum |
| HEATING_FAILED | Heating Failed | `heating failed`, `failed to heat`, `heating timeout`, `heating error`, `heater error`, `heater circuit`, `heating issue`, `heat.*error`, `heat.*fail`, `heat.*issue`, `heat.*problem`, `nozzle heat`, `hotend heat`, `bed heat`, `heat.*not.*work`, `heat.*stop`, `heat.*slow` | Heater cannot reach target temperature |
| PROBE_FAILED | Probe Failed | `probe failed`, `probing failed`, `bltouch.*error`, `probe.*error`, `cr.?touch.*error`, `cr.?touch.*fail`, `probe.*issue`, `probe.*problem`, `sensor.*probe`, `leveling.*probe`, `auto.*level.*error`, `mesh.*error`, `bed.*level.*error`, `z.*probe.*error` | Bed probe failure |
| HOMING_FAILED | Homing Failed | `homing failed`, `failed to home`, `homing error`, `home.*fail`, `home.*error`, `homing issue`, `won.*t home`, `can.*t home`, `home.*issue`, `x.*home.*fail`, `y.*home.*fail`, `z.*home.*fail`, `rehome.*fail`, `homing.*issue`, `sensorless.*homing.*fail`, `homing.*sensor` | Axis cannot find home position |
| MCU_SHUTDOWN | MCU Shutdown | `mcu.*shutdown`, `mcu shutdown`, `klipper.*shutdown`, `klipper.*disconnect`, `moonraker.*disconnect`, `mcu.*disconnect`, `kill\(\)`, `printer halted`, `emergency stop` | MCU communication loss / emergency stop |
| TEMP_SENSOR_ERROR | Temperature Sensor Error | `temperature sensor`, `thermistor.*error`, `sensor.*error`, `thermistor.*fail`, `thermistor.*issue`, `thermistor.*problem`, `what thermistor`, `bed thermistor`, `hotend thermistor`, `thermistor replacement`, `thermistor type`, `thermistor blues` | Temperature sensor fault |
| STEPPER_DRIVER_ERROR | Stepper Driver Error | `stepper driver`, `driver error`, `tmc.*error`, `stallguard`, `sensorless.*hom`, `stepper.*fail`, `stepper.*error`, `motor.*error`, `motor.*fail`, `axis.*error`, `stepper.*noise`, `motor.*noise`, `x axis noise`, `y axis noise`, `z axis noise`, `stepper.*skip`, `motor.*skip` | Stepper driver / motor fault |
| CLOGGED_NOZZLE | Clogged Nozzle | `clogged nozzle`, `nozzle clog`, `clog`, `jammed nozzle`, `extruder jam`, `nozzle jam`, `hotend clog`, `heatbreak clog`, `ptfe clog`, `bowden clog`, `filament stuck`, `stuck filament`, `clogged hotend` | Filament path obstruction |
| BED_LEVELING_FAILED | Bed Leveling Failed | `bed leveling failed`, `leveling failed`, `mesh.*failed`, `auto level.*fail`, `bed level.*error`, `leveling.*error`, `auto level.*error`, `mesh.*error`, `bed mesh`, `leveling washers`, `missing leveling`, `z offset`, `z.*offset.*issue`, `probe.*offset`, `bltouch.*offset`, `cr.?touch.*offset`, `bed.*mesh.*issue`, `first layer.*issue`, `first layer.*problem`, `adhesion.*issue`, `not adhering`, `not sticking`, `won.*t stick`, `comes off.*bed`, `print comes off`, `bed adhesion`, `plate.*peel`, `magnetic plate.*peel` | Bed leveling / adhesion failure |
| LAYER_SHIFT | Layer Shift | `layer shift`, `shifting layer`, `offset layer`, `misaligned layers`, `misalignment`, `layer offset`, `layer.*misalign`, `z banding`, `z-banding`, `banding`, `wobble`, `print shift`, `sudden shift`, `position shift` | Mechanical misalignment during print |
| SD_CARD_ERROR | SD Card Error | `sd card`, `sdcard`, `card error`, `read error`, `file error`, `gcode.*error`, `sd init`, `sd.*fail`, `sd.*error`, `card.*fail`, `card.*init`, `micro.*sd`, `sd.*corrupt`, `gcode.*upload.*fail`, `upload.*fail` | Storage/media read failure |
| FILAMENT_RUNOUT | Filament Runout | `filament runout`, `runout sensor`, `out of filament`, `filament.*out`, `no filament`, `runout.*fail`, `runout.*error` | Filament depletion detection |
| EXTRUDER_SKIP | Extruder Skip | `extruder skip`, `skipping extruder`, `clicking extruder`, `extruder.*click`, `extruder.*clicking`, `clicking.*extruder`, `gear.*skip`, `drive gear.*skip`, `extruder.*tension`, `tension.*issue`, `filament.*tension`, `extruder.*grind`, `grinding.*filament`, `extruder.*slip` | Extruder motor skipping steps |
| UNDER_EXTRUSION | Under Extrusion | `under extrusion`, `under-extrusion`, `insufficient extrusion`, `gaps in print`, `not extruding`, `won.*t extrude`, `no extrusion`, `extrusion.*fail`, `extrusion.*issue`, `extrusion.*problem`, `extrude.*fail`, `extrude.*issue`, `under.*extrud`, `poor extrusion`, `weak extrusion`, `thin extrusion` | Insufficient material deposition |
| OVER_EXTRUSION | Over Extrusion | `over extrusion`, `over-extrusion`, `too much filament`, `blobbing`, `over.*extrud`, `excess.*extrusion`, `blob`, `zit`, `elephant foot` | Excessive material deposition |
| RETRACTION_ISSUE | Retraction Issue | `retraction.*issue`, `retraction.*problem`, `retraction.*fail`, `retract.*issue`, `retract.*problem`, `stringing`, `oozing`, `filament.*retract`, `retract.*setting`, `cfs retract`, `spool.*retract` | Retraction / stringing problems |
| FIRMWARE_ERROR | Generic Firmware Error | `firmware error`, `firmware.*fail`, `error:`, `err:`, `exception`, `crash`, `reset`, `firmware.*issue`, `firmware.*problem`, `firmware.*bug`, `downgrade firmware`, `upgrade firmware`, `firmware version`, `firmware update`, `custom firmware`, `start_print`, `gcode.*firmware`, `monochrome firmware`, `multicolor firmware`, `web interface.*missing`, `touchscreen.*firmware` | Firmware-related fault |
| HARDWARE_FAULT | Generic Hardware Fault | `hardware error`, `hardware fault`, `board error`, `mainboard error`, `control board`, `board.*fail`, `board.*issue`, `board.*problem`, `motherboard`, `mainboard.*replacement`, `hotend board`, `toolhead board`, `extruder board`, `replacement.*board`, `wrong plug`, `wiring.*issue`, `connector.*issue`, `cable.*issue`, `wire.*break`, `wiring.*fail`, `stepper.*motor.*replacement`, `y-axis.*replacement`, `x-axis.*replacement`, `z-axis.*replacement`, `shaft.*replacement`, `bearing.*replacement`, `pulley.*replacement`, `belt.*replacement`, `waste chute.*broken`, `chute.*broken`, `part.*replacement`, `replacement part`, `specifications.*supplied` | Hardware component fault |
| CONNECTIVITY_ERROR | Connectivity Error | `connection lost`, `disconnected`, `timeout`, `wifi.*error`, `network error`, `connect.*error`, `connect.*fail`, `won.*t connect`, `can.*t connect`, `connection.*issue`, `connection.*problem`, `buffering`, `keeps buffering`, `upload.*fail`, `gcode.*upload`, `send.*print.*fail`, `usb.*drive.*fail`, `insert.*usb.*fail`, `printer connection`, `moonraker.*disconnect`, `klipper.*disconnect`, `mcu.*disconnect` | Network/communication loss |
| CALIBRATION_ERROR | Calibration Error | `calibration failed`, `calibration error`, `pid.*fail`, `pid tuning`, `calibrat.*issue`, `calibrat.*problem`, `calibrat.*fail`, `shake.*calibrat`, `shaking.*calibrat`, `auto calibrat`, `sensorless.*calibrat`, `vibration.*calibrat`, `input shaper`, `resonance.*calibrat`, `accelerometer`, `adxl`, `input.*shaper`, `resonance` | Calibration procedure failure |
| PRINT_QUALITY | Print Quality Issue | `print quality`, `quality issue`, `quality problem`, `poor quality`, `bad quality`, `rough print`, `surface quality`, `dimensional accuracy`, `warp`, `warping`, `corner lift`, `edge lift`, `taco`, `taco heat bed`, `bed warp`, `bed.*warp`, `heat bed.*warp`, `k2 taco`, `first layer`, `first.layer`, `layer.*issue`, `layer.*problem`, `surface.*issue`, `surface.*problem`, `z seam`, `ghosting`, `ringing`, `vibration`, `artifact`, `defect`, `imperfection`, `rough`, `pillowing`, `top layer`, `bottom layer`, `infill.*issue`, `wall.*issue`, `perimeter.*issue`, `overhang.*issue`, `bridge.*issue`, `support.*issue` | Print quality defects |
| MECHANICAL_ISSUE | Mechanical Issue | `mechanical.*issue`, `mechanical.*problem`, `frame.*issue`, `frame.*hit`, `hits frame`, `axis.*hit`, `bed.*jerk`, `jerking`, `vibration.*issue`, `wobble`, `loose.*belt`, `belt.*tension`, `belt.*loose`, `belt.*skip`, `pulley.*loose`, `grub.*screw`, `set.*screw`, `alignment`, `misaligned`, `rail.*issue`, `linear.*rail`, `bearing.*issue`, `rod.*issue`, `z.*axis.*issue`, `x.*axis.*issue`, `y.*axis.*issue`, `dual.*z.*sync`, `z.*sync`, `lead.*screw`, `trapezoidal.*screw`, `ball.*screw` | Mechanical/frame issues |
| ERROR_CODE | Specific Error Code | `error code`, `error.*\d{3,}`, `\b\d{4,}\b.*error`, `error \d+`, `code \d+`, `fo\d+`, `tr\d+`, `e\d+\b`, `e\d+ error`, `halted.*kill` | Specific numeric error codes |
| OTHER | Other | (no pattern matches) | Does not fit any defined fault type |

## Printer Model Extraction

Extract printer model from title using known model patterns (case-insensitive):

### Creality
- `Ender 3` (V2, V3, Pro, Neo, Max, S1, KE)
- `Ender 5` (Plus, Pro, S1)
- `Ender 6`, `Ender 7`
- `CR-6` (SE, Max)
- `CR-10` (V2, V3, S4, S5, Smart)
- `CR-30`, `CR-200B`
- `K1` (C, Max, SE)
- `K2` (Plus)
- `K3`
- `Halot` (One, Sky, Lite, Plus)
- `Sermoon` (D1, D3)
- `Sonic Pad` (Klipper host)

### LulzBot
- `TAZ` (4, 5, 6, Pro, Workhorse)
- `Mini` (1, 2, 3)

### Prusa (if forum accessible)
- `MK3` (S, S+)
- `MK4` (S)
- `MINI` (+)
- `XL`
- `SL1` (S)

### Bambu Lab (if forum accessible)
- `X1` (Carbon, E)
- `P1` (P, S)
- `A1` (Mini)

### Voron (if forum accessible)
- `Voron` (2.4, Trident, Switchwire, Legacy)

### Generic / Other
- `Klipper` (generic, implies Klipper firmware)
- `Marlin` (generic, implies Marlin firmware)
- `RepRapFirmware` (RRF, Duet)
- `SKR` (BTT SKR boards: SKR 1.3, 1.4, 2.0, Mini E3, Pico)
- `BTT` (BigTreeTech boards)
- `Duet` (Duet 2, 3, Mini 5+)
- `RAMPS`, `RAMBo`, `Archim`, `Mellow`, `Fly`

**Extraction rule**: First matching model pattern in title → model. If none, check tags (if available) → model. If none → "Unknown".

## Firmware Type Inference

From model + title patterns:
- `Klipper` in title or model is Klipper host (Sonic Pad, Fluidd, Mainsail, OctoPrint + Klipper) → `Klipper`
- `Marlin` in title → `Marlin`
- Creality K1/K2/K3/Ender 3 S1/KE/Neo → `Creality OS` (Marlin-derived)
- Bambu Lab → `Bambu Lab`
- Prusa MK3/MK4/MINI/XL → `Prusa Firmware` (Marlin-derived)
- LulzBot → `Marlin` (LulzBot Marlin)
- Voron → `Klipper` (typically)
- Duet → `RepRapFirmware`
- SKR/BTT boards with Klipper mention → `Klipper`
- Default for Creality Ender 3 (non-S1) → `Marlin`
- Default for unknown → `Unknown`

## Structured Case Criteria (for G1/G4 evaluation)

A case is **structured** if the topic discussion (replies) contains:
1. **Root cause identified**: Explicit statement of failed component or condition:
   - Component: `thermistor`, `heater cartridge`, `heating element`, `wiring`, `connector`, `stepper driver`, `TMC2209`, `bed probe`, `BLTouch`, `nozzle`, `hotend`, `heatbreak`, `PTFE tube`, `bowden tube`, `extruder gear`, `drive gear`, `belt`, `pulley`, `motor`, `mainboard`, `motherboard`, `control board`, `SD card`, `microSD`, `firmware`, `bootloader`
   - Condition: `short circuit`, `open circuit`, `broken wire`, `loose connection`, `overheating`, `thermal runaway`, `clogged`, `jammed`, `worn`, `damaged`, `failed`, `dead`, `burnt`, `melted`
2. **Repair action**: Explicit repair/replacement:
   - `replaced`, `swapped`, `changed`, `fixed`, `repaired`, `upgraded`, `tightened`, `cleaned`, `re-seated`, `reflowed`, `reflashed`, `updated firmware`, `adjusted`, `calibrated`
3. **Printer model + firmware context**: Both present in topic

**Classification**: Manual review of 50 random structured cases (or all if < 50). Each case → `SPECIFIC` (names exact part + action) or `GENERIC` (vague: "check wiring", "update firmware", "calibrate").

## Incumbent Tool Survey Criteria (G5)

For each top 10 fault type, check if a **single free tool** provides:
- Fault code → root cause mapping
- Printer-model-specific (not generic)
- Actionable repair procedure
- Accessible without login/paywall

Tools to survey:
- Marlin firmware documentation (marlinfw.org)
- Klipper documentation (klipper3d.org)
- Creality official wiki / support site
- LulzBot support / documentation
- Prusa knowledge base
- Bambu Lab wiki
- Voron documentation
- BTT / SKR documentation
- Duet3D documentation
- Community wikis (RepRap, 3D Printing Stack Exchange, Reddit wikis)
- YouTube channels (teaching repair) — not computational tools
- Discord/Telegram groups — not computational tools

**G5 passes** if no single free tool covers ≥ 50% of top 10 fault types with printer-specific root causes.