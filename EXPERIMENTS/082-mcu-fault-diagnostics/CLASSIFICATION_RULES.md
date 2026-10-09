<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E082 — Classification rules for microcontroller fault root cause specificity

Session `2026-10-09-024`, VM `instance-20260717-0947`, declared 2026-10-09.

## Fault type taxonomy (predeclared)

Fault types are grouped into these categories for concentration analysis (G2):

| Category | Canonical name | Variants / indicators |
|----------|----------------|----------------------|
| ARM Cortex-M HardFault | `HardFault` | `HardFault`, `hard fault`, `hardfault`, `Hard Fault` |
| ARM Cortex-M MemManage | `MemManage` | `MemManage`, `Memory Management Fault`, `mem manage`, `MemManage Fault` |
| ARM Cortex-M BusFault | `BusFault` | `BusFault`, `Bus Fault`, `busfault`, `IBUSERR`, `PRECISERR`, `IMPRECISERR`, `UNSTKERR`, `STKERR` |
| ARM Cortex-M UsageFault | `UsageFault` | `UsageFault`, `Usage Fault`, `usagefault`, `DIVBYZERO`, `UNALIGNED`, `NOCP`, `INVSTATE`, `UNDEFINSTR`, `INVPC` |
| ARM Cortex-M SecureFault | `SecureFault` | `SecureFault`, `Secure Fault`, `LSERR`, `SFARERR` |
| Stack overflow | `StackOverflow` | `stack overflow`, `stackover flow`, `stack overrun`, `stack exhaustion`, `MSP`, `PSP`, `stack pointer` |
| Watchdog reset | `WatchdogReset` | `watchdog`, `WDT`, `IWDG`, `WWDG`, `watchdog reset`, `watchdog timeout` |
| Brownout / power reset | `BrownoutReset` | `brownout`, `BOR`, `POR`, `PDR`, `power-on reset`, `brownout reset`, `power failure`, `VDD` |
| Clock failure | `ClockFailure` | `clock failure`, `HSE`, `LSE`, `PLL`, `clock security`, `CSS`, `clock monitor`, `oscillator failure` |
| Null pointer dereference | `NullPointer` | `null pointer`, `NULL`, `0x0`, `0x00000000`, `dereference`, `access violation` |
| Unaligned memory access | `UnalignedAccess` | `unaligned`, `UNALIGNED`, `alignment fault`, `alignment trap`, `misaligned` |
| Division by zero | `DivByZero` | `division by zero`, `divide by zero`, `DIVBYZERO`, `divide error` |
| Undefined instruction | `UndefinedInstr` | `undefined instruction`, `UNDEFINSTR`, `illegal instruction`, `invalid opcode` |
| FPU / coprocessor fault | `FPUFault` | `FPU`, `coprocessor`, `NOCP`, `floating point`, `VFP`, `NEON` |
| Peripheral fault (USB) | `USBFault` | `USB`, `PHY`, `endpoint`, `NAK`, `STALL`, `CRC error`, `babble` |
| Peripheral fault (CAN) | `CANFault` | `CAN`, `bus off`, `error passive`, `stuff error`, `form error`, `ACK error` |
| Peripheral fault (Ethernet) | `EthFault` | `Ethernet`, `MAC`, `PHY`, `CRC error`, `collision`, `jabber` |
| DMA fault | `DMAFault` | `DMA`, `transfer error`, `FIFO error`, `address error` |
| ADC/DAC fault | `ADCFault` | `ADC`, `DAC`, `conversion error`, `overrun`, `watchdog` |
| Interrupt / priority fault | `IRQFault` | `interrupt`, `priority`, `NVIC`, `pending`, `tail-chaining`, `late arrival` |
| Bootloader / flash fault | `FlashFault` | `flash`, `bootloader`, `erase`, `program`, `verify`, `write protect`, `read protect` |
| RTOS / context switch fault | `RTOSFault` | `FreeRTOS`, `ThreadX`, `Zephyr`, `context switch`, `task`, `semaphore`, `mutex`, `queue` |
| Other / unspecified | `Other` | Catch-all for fault types not matching above |

## Root cause specificity classification (for G4)

A structured case's answer is classified as **specific** (meets G4) if it explicitly identifies **at least one** of:

1. **Specific register value or bit pattern** — e.g., "CFSR shows `IBUSERR` (bit 1) set", "HFSR `FORCED` bit indicates escalated fault", "PC = 0x08001234 points to the faulting instruction"
2. **Specific code pattern or line** — e.g., "the `memcpy` at line 42 writes past the buffer", "the ISR at `0x08000400` doesn't clear the interrupt flag", "recursive function call without base case at `main.c:15`"
3. **Specific hardware fix or measurement** — e.g., "add 10µF capacitor at VDD pin", "HSE crystal needs 20pF load capacitors", "pull-up resistor missing on NRST", "measure VBAT with multimeter"
4. **Specific peripheral configuration correction** — e.g., "DMA channel priority must be higher than USB", "ADC sampling time too short for high-impedance source", "CAN baud rate prescaler wrong for 500kbps"
5. **Specific vendor erratum or silicon bug** — e.g., "STM32F4 erratum 2.1.7: Flash access during CPU1/CPU2 concurrent access", "ESP32 rev 0 watchdog bug"

A structured case's answer is classified as **non-specific** (does not meet G4) if it only contains:

- Generic advice: "use a debugger", "check your code", "add print statements", "step through in IDE"
- Tool recommendations without diagnosis: "use STM32CubeIDE", "try SEGGER J-Link", "use OpenOCD"
- Requests for more information: "post your linker script", "show your startup code", "what does the call stack show"
- Vague descriptions: "it's a stack problem", "memory corruption", "timing issue", "interrupt conflict"
- "Check wiring" / "check connections" without specifying what to measure or where

## MCU family extraction (for G3)

MCU families are extracted from tags and body text. Canonical families:

| Family | Tag patterns | Part prefixes |
|--------|--------------|---------------|
| STM32 | `stm32`, `stm32f1`, `stm32f4`, `stm32h7`, `stm32g0`, `stm32l4`, `stm32wb`, `stm32wl` | `STM32F`, `STM32H`, `STM32G`, `STM32L`, `STM32W` |
| ARM Cortex-M (generic) | `arm`, `cortex-m`, `cortex-m0`, `cortex-m3`, `cortex-m4`, `cortex-m7`, `cortex-m33` | N/A |
| AVR / ATmega / ATtiny | `atmel`, `avr`, `atmega`, `attiny`, `arduino` | `ATmega`, `ATtiny`, `AT90` |
| PIC / dsPIC | `pic`, `dsPIC`, `pic16`, `pic18`, `pic24`, `pic32` | `PIC1`, `PIC2`, `PIC3`, `dsPIC` |
| ESP32 / ESP8266 | `esp32`, `esp8266`, `espressif` | `ESP32`, `ESP8266` |
| nRF52 / nRF51 | `nrf52`, `nrf51`, `nordic` | `nRF52`, `nRF51` |
| MSP430 / MSP432 | `msp430`, `msp432`, `ti-msp` | `MSP430`, `MSP432` |
| TM4C / Tiva / Stellaris | `tm4c`, `tiva`, `stellaris`, `lm4f` | `TM4C`, `LM4F` |
| LPC (NXP) | `lpc`, `lpc17`, `lpc43`, `lpc55`, `nxp` | `LPC17`, `LPC43`, `LPC55` |
| Kinetis (NXP) | `kinetis`, `k20`, `k22`, `k64`, `k66`, `k80`, `k82` | `MK20`, `MK22`, `MK64`, `MK66`, `MK80`, `MK82` |
| EFM32 / Gecko (Silicon Labs) | `efm32`, `gecko`, `silabs`, `silicon-labs` | `EFM32` |
| SAM / SAMD (Microchip) | `sam`, `samd`, `samc`, `same`, `saml`, `samg`, `samv`, `samrh` | `ATSAMD`, `ATSAMC`, `ATSAME`, `ATSAML`, `ATSAMG`, `ATSAMV`, `ATSAMRH` |
| RP2040 / RP2350 (Raspberry Pi) | `rp2040`, `rp2350`, `raspberry-pi-pico`, `pico` | `RP2040`, `RP2350` |
| Other / unknown | (not matched above) | |

## Structured case criteria (predeclared)

A case is **structured** if ALL of the following are true:

1. Question contains ≥1 fault/exception indicator (from taxonomy above)
2. Question has ≥1 MCU family tag
3. Question has ≥1 answer from user with reputation > 100
4. Question has accepted answer OR answer with score ≥ 3
5. The accepted/high-scored answer explicitly states a root cause (from specific/non-specific criteria above) AND the root cause is not "could not determine" or "need more info"

## Inter-rater reliability (if multiple readers)

If multiple readers classify, Cohen's κ ≥ 0.70 required for G4 to be considered valid. Single-reader classification is accepted for preliminary evaluation; κ requirement applies to any confirmatory study.