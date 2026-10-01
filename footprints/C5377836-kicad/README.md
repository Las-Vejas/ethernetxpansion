# HCTL HC621601A-M911-A (LCSC C5377836) - KiCad symbol, footprint, 3D model

## Read this first: what is built, what is sourced, what is NOT verified
Built by me: the symbol, the footprint and an updated simplified 3D model.
Sourced from the HCTL drawing (datasheet.pdf): all pad positions and drill sizes, body outline, pin names, LED polarity.
NOT verified:
- I could not run KiCad here. No KiCad 10, no ERC, no DRC, no 3D viewer check. The files were only parsed with a third-party S-expression library (kiutils) and paren-checked. I wrote them in the KiCad 9 file format, which KiCad 10 should open and upgrade on save. Open them once and tell me if anything is rejected.
- The symbol was never rendered. Check how it looks in the symbol editor.
- No physical part, no PCB fit test, no solder test.
- Pad sizes (1.6 mm signal, 1.7 mm LED, 2.6 mm shield) are my choice. The drawing only gives drill sizes. Check against your fab rules.
- The two 3.20 mm locating-post holes are non-plated (NPTH). The drawing does not say plated or not.
- The 3D model is still the simplified one (see below), not manufacturer CAD.

## Correction to the earlier 3D model
Re-reading the drawing for the footprint, I found the earlier STEP had pin Y positions off by 0.11-0.22 mm: signal rows were 9.00/6.46 mm from the post line instead of 8.89/6.35 mm, and the LED pins were 3.89 mm instead of 4.11 mm. I fixed model.py and regenerated STEP/STL; the 3dshapes/ files here replace the earlier ones. All 14 pin centers in the STEP now match the footprint pads (checked numerically, 0.0000 mm difference). Port, contact and tab details are still approximations.

## Files
- HCTL.kicad_sym: symbol HC621601A-M911-A
- HCTL.pretty/RJ45_HCTL_HC621601A-M911-A_Vertical_TH.kicad_mod: footprint
- 3dshapes/HC621601A-M911-A.step (+ .stl): simplified 3D model, origin = midpoint of the locating posts at PCB surface
- source/model.py (CadQuery), source/gen_kicad.py (regenerates symbol + footprint), source/datasheet.pdf
- fp_preview.png: plot of the footprint pads read back from the file (not a KiCad screenshot)

## Footprint (datasheet page 1 "recommended PCB layout", component side)
Origin = midpoint of the two locating posts. Pin 1 = square pad at (5.715, 8.89) in KiCad coordinates, bottom-right.
- Pins 1-10: drill 0.90, pad 1.6. Rows 2.54 apart, 1.27 stagger, 2.54 pitch. Odd pins at y=+8.89, even at y=+6.35.
- Pins 11-14 (LEDs): drill 1.02, pad 1.7, at x = +-3.785 and +-6.325, y = -4.11.
- Locating posts: 2x NPTH 3.20 at x = +-5.715, y = 0.
- Shield: 2x pad "SH", drill 1.63, pad 2.6, at x = +-7.95, y = +3.89.
- Fab outline 16.10 x 16.90 mm. The connector opening faces up, away from the PCB; the LED/latch side is toward the top of the pad view (-Y).

## Symbol pins (datasheet page 3, all typed passive so ERC will not complain about power pins)
1 VCC_CT (datasheet "VCC", PHY-side center-tap bus) | 2 TD1+ | 3 TD1- | 4 TD2+ | 5 TD2- | 6 TD3+ | 7 TD3- | 8 TD4+ | 9 TD4- | 10 GND_BS (datasheet "GND", cable-side 75 ohm termination via 1000 pF/2 kV)
11 LED_G_A / 12 LED_G_K (green) | 13 LED_Y_A / 14 LED_Y_K (yellow). Anode/cathode taken from the diode symbols on page 3.
SH = shield. The symbol's Footprint field is HCTL:RJ45_HCTL_HC621601A-M911-A_Vertical_TH, LCSC field is C5377836.
Check pin 1 (VCC_CT) against your PHY's magnetics requirements before routing; I only transcribed the drawing.

## Install
1. Copy HCTL.pretty/, HCTL.kicad_sym and 3dshapes/ into your project folder.
2. Preferences > Manage Symbol Libraries: add project library, nickname HCTL, path ${KIPRJMOD}/HCTL.kicad_sym.
3. Manage Footprint Libraries: add nickname HCTL, path ${KIPRJMOD}/HCTL.pretty.
4. The footprint's 3D path is ${KIPRJMOD}/3dshapes/HC621601A-M911-A.step. If you put the folder elsewhere, change it in the footprint's 3D settings. No rotation or offset should be needed; if the model looks mirrored or offset, tell me.

## Source
https://www.lcsc.com/product-detail/C5377836.html
https://datasheet.lcsc.com/datasheet/pdf/a6450734ef0cdf4aa798ffe8304b55e8.pdf?productCode=C5377836
