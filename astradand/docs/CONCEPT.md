# ASTRADAND: concept, ideation and selection

## 1. The brief
One fantasy/science-fiction product, thought through from idea to manufacturing files: not a toy knock-off but something with a real engineering core, buildable with this repository's toolchain (KiCad board generator, firmware, CAD, laser/print files), and honest about what is unproven.

## 2. Three candidates, scored
Scores 1-5 (5 best). Weights: play value 3, engineering depth 3, manufacturability with our tools 3, demand/price fit 2, compliance risk (inverse) 2, margin 2.

| Candidate | Idea | Play | Depth | Mfg | Demand | Risk (5 = low) | Margin | Weighted |
|---|---|---|---|---|---|---|---|---|
| **A. ASTRADAND** | A hilt-style gesture wand: hold the trigger, draw a rune in the air, the crystal blazes with fire, water or lightning; mana and combos | 5 | 5 | 4 | 4 | 4 | 3 | **86** |
| B. Dragon-egg hatchery | A warm, glowing "egg" that reacts to touch and slowly hatches over days (heater, touch sensing, sound) | 4 | 3 | 3 | 3 | 2 (heater + children) | 3 | 64 |
| C. Rune-stone oracle | NFC rune stones on a board that tell a branching story (needs NFC readers per slot) | 4 | 3 | 2 | 3 | 4 | 2 | 65 |

**Chosen: A.** It has the richest engineering (motion sensing and a real recogniser), it can be tested on a computer before any hardware exists, and the product is one PCB, one printed shell and a few paper parts.

## 3. The product
**ASTRADAND** (astra = divine weapon, danda = staff): a 232 mm, 34 mm diameter hilt. A six-pixel "crystal" light bar sits in an offset slit on the head. The player holds the trigger, draws one of six shapes in the air, and releases:

| Spell | Gesture | Effect | Mana |
|---|---|---|---|
| Agni (fire) | circle, clockwise from the top | flickering orange flame, warm rising tune | 25 |
| Vajra (lightning) | bold "Z" | white flashes, sharp zaps | 35 |
| Jala (water) | wave, two humps | blue wave running along the crystal | 20 |
| Raksha (shield) | triangle, apex first | pulsing teal shield, two-note chime | 30 |
| Prakash (light) | straight line upward | golden flash fading to a glow | 10 |
| Vayu (wind) | check mark | green sweep | 15 |

Mana starts at 100 (shown as lit crystals), refills 2 per second, a fizzle costs 5, each spell has a 1 s cooldown, and **Agni then Vajra within 4 s is the combo Mahastra** (magenta crystal, long fanfare). A coin motor gives a haptic pulse; a piezo gives the sounds. The wand sleeps after 45 s still and wakes on motion.

## 4. World (one paragraph of lore for the box and cards)
In Kshetra, an age after the sky-cities fell, the Yantra-smiths forged hilts from star-iron and tuned them to the old rune-shapes. A hilt does not obey words: it obeys the stroke. Apprentices of the Vyoma Order learn six strokes first. When the combination of fire then lightning is drawn in one breath, the hilt is said to open the Mahastra.
(English text only; any Hindi/Telugu lore or names in print need native-speaker review; the Devanagari spell names on the cards are unreviewed.)

## 5. Market and positioning (what I could and could not find)
- Found: an interactive licensed gesture wand (Kymera) lists at about USD 60-70 outside India; Comic Con Bengaluru 2025 reported more than 50,000 visitors in two days. No Indian price for interactive wands and no fantasy-prop market size was found.
- Target: 9-16-year-olds and cosplayers/collectors, sold at conventions, hobby stores and online. Price guidance in `economics.md`: **Rs 2,999** (Rs 2,499 only with a direct channel and a lean BOM).
- Original IP: no licensed names, shapes or sounds. Sanskrit-derived words are generic nouns; run a trademark search before launch.

## 6. Engineering core
1. **Recogniser:** integrate the gyro (after removing the bias measured while idle and undoing the wand roll from gravity) into a 2-D tip path, resample to 16 points, normalise, match six templates within +-20 degrees of rotation. On 1,800 synthetic casts per noise level: 100 % at nominal noise and 98.3 % at 1.6x (see `gesture_results.md`). Rejection thresholds were tuned so that tiny tremors and straight sweeps never cast; 8 % of random scribbles still match a spell. **Synthetic data only: real hands will do worse until tuned on recorded gestures.**
2. **Hardware:** ATmega328P (3.3 V, 8 MHz internal), MPU-6050 6-axis IMU on I2C at 50 Hz, six WS2812B-Mini pixels behind a high-side switch (zero standby draw), differential piezo, haptic motor, 3 x AAA with reverse-polarity protection; board 146 x 26 mm.
3. **Firmware:** portable C core (`ad_core.c`: recogniser, mana/combos, LED effects with a hard current budget, sound tables, power manager) + Arduino-core board code. 83 host checks pass under sanitizers; the C verdicts match the Python reference on 46 of 46 test traces.
4. **Mechanics:** two-half FDM shell (prototype) with board rails, battery saddle, screw bosses, an offset light slit with a diffuser "crystal", trigger cap, tip and pommel; laser-cut display stand; carton dieline; spell cards.

## 7. What is not done (read this)
No hardware exists. The MPU-6050 register sequence, WS2812 bit-bang timing, wake-on-motion sleep, piezo drive and battery estimate are unverified on a real board. The shell has not been printed or fitted to the PCB and battery. The gesture set has never been tried by a human hand. Toy-safety testing, battery and EMC compliance are not done; LED eye-safety (diffused, but not measured) is untested. Economics are estimates.
