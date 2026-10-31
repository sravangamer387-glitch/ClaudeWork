# 20 experiments (Prayog kit)

Topic areas only: **mapping to specific syllabus chapters must be verified by a teacher before printing.** Experiments marked VALIDATED have their analysis checked against simulated noisy data (`validation.md`). Hardware accuracy is not yet verified.

## 1. Cooling of hot water (Newton's law)
*Topic:* Heat  |  *Sensors:* NTC temperature  |  *Analysis check:* VALIDATED

**Procedure**
1. Heat 200 ml water to about 85 C, pour into an insulated cup, place the NTC in the water.
2. Log temperature every 30 s for 30 minutes; note the room temperature.
3. Plot ln(T - T_room) against time.

**Expected result:** A straight line; slope = -k with k about 0.002 per s for a plain cup (the simulation recovers k to 5 %).

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 2. Melting ice: temperature plateau
*Topic:* Heat  |  *Sensors:* NTC temperature  |  *Analysis check:* not simulated

**Procedure**
1. Crushed ice with a little water, NTC in the mixture, stir gently.
2. Log for 20 minutes while it melts, then 10 minutes as it warms.
3. Mark the plateau.

**Expected result:** Temperature stays near 0 C (within about 1.5 C of the NTC's accuracy) until the ice has melted, then rises.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 3. Light intensity and distance
*Topic:* Light  |  *Sensors:* LDR (lux)  |  *Analysis check:* VALIDATED

**Procedure**
1. Torch and LDR on a metre scale in a dark room.
2. Log lux at 20, 30, ... 110 cm.
3. Plot log(lux) against log(distance).

**Expected result:** Slope about -2 (inverse-square law); the simulation recovers -2.00 within 4 %. Stray light makes it shallower: shield the LDR.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 4. Loudness and distance
*Topic:* Sound  |  *Sensors:* Microphone level  |  *Analysis check:* not simulated

**Procedure**
1. Speaker playing a steady tone, microphone at increasing distances.
2. Log the mean level at 0.5, 1, 1.5, 2 m.
3. Plot level against distance.

**Expected result:** Level falls roughly with the inverse of distance in a quiet open space; rooms add echoes and flatten the trend.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 5. Speed of sound by echo
*Topic:* Sound  |  *Sensors:* Ultrasonic distance  |  *Analysis check:* VALIDATED

**Procedure**
1. Ultrasonic module facing a wall at 0.3, 0.5, ... 2.1 m (tape measure).
2. Log the echo time (microseconds) 10 times at each distance.
3. Plot distance against echo time; c = 2 x slope.

**Expected result:** About 343 m/s at 20 C, rising 0.6 m/s per degree; simulation recovers 344 m/s within 2 %.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 6. Pendulum: g from period and length
*Topic:* Motion  |  *Sensors:* Photogate  |  *Analysis check:* VALIDATED

**Procedure**
1. String and steel ball, photogate at the lowest point.
2. Lengths 0.3 to 1.0 m; log the period over 10 swings.
3. Plot period squared against length; g = 4 pi squared / slope.

**Expected result:** g about 9.8 m/s2 (Hyderabad about 9.78); simulation recovers 9.82 within 2 %. Keep swing angles under 10 degrees.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 7. Free fall: g from drop time
*Topic:* Motion  |  *Sensors:* Two photogates  |  *Analysis check:* VALIDATED

**Procedure**
1. Drop a steel ball through two gates a known height apart.
2. Heights 0.2 to 0.9 m.
3. Plot height against time squared; g = 2 x slope.

**Expected result:** About 9.8 m/s2; needs timing to better than 1 ms (the photogate gives microseconds).

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 8. Speed of a trolley on a slope
*Topic:* Motion  |  *Sensors:* Photogate  |  *Analysis check:* not simulated

**Procedure**
1. Card flag of known width (5 cm) on a trolley rolling down a slope.
2. Log the beam-interruption time at three gate positions.
3. Speed = width / time.

**Expected result:** Speed rises along the slope; compare with the energy calculation v = sqrt(2 g h) (smaller because of friction).

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 9. Ohm's law
*Topic:* Electricity  |  *Sensors:* Voltage probes (2)  |  *Analysis check:* VALIDATED

**Procedure**
1. Resistor (47 ohm) with a 5 V supply through a variable series resistor.
2. Measure voltage across the resistor and across a 1 ohm shunt (current = V/1).
3. Plot V against I.

**Expected result:** Straight line through the origin; slope = resistance (47 ohm recovered within 3 %). Keep currents under 100 mA.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 10. Series and parallel resistors
*Topic:* Electricity  |  *Sensors:* Voltage probes  |  *Analysis check:* not simulated

**Procedure**
1. Build series and parallel combinations of 100 and 220 ohm.
2. Measure the voltage drops.
3. Compare with the calculated values.

**Expected result:** Series: voltages share in proportion to resistance; parallel: equal voltage.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 11. Capacitor charging: RC time constant
*Topic:* Electricity  |  *Sensors:* Voltage probe  |  *Analysis check:* VALIDATED

**Procedure**
1. Charge a 4.7 mF capacitor through 1 kohm from 5 V.
2. Log voltage every 0.5 s for 15 s.
3. Plot ln(5 - V) against time; tau = 1 / |slope|.

**Expected result:** Tau = R x C = 4.7 s; simulation recovers 4.72 s within 4 %.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 12. Magnetic field of a bar magnet
*Topic:* Magnetism  |  *Sensors:* Hall sensor  |  *Analysis check:* VALIDATED

**Procedure**
1. Magnet end-on to the Hall sensor, moved away in 5 mm steps.
2. Log the field in mT.
3. Plot log(B) against log(distance).

**Expected result:** Field falls steeply: exponent about -3 on the axis (simulation recovers -3.07 within 7 %).

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 13. Soil drying curve
*Topic:* Life science  |  *Sensors:* Soil moisture  |  *Analysis check:* not simulated

**Procedure**
1. Pot of wet soil in sunlight, sensor inserted.
2. Log moisture % every 30 minutes for 2 days.
3. Plot against time.

**Expected result:** Moisture decreases smoothly; faster in sun and wind. Compare shaded and sunny pots.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 14. Day temperature and light log
*Topic:* Earth science  |  *Sensors:* NTC + LDR  |  *Analysis check:* not simulated

**Procedure**
1. Place the sensors outdoors in shade.
2. Log both every 5 minutes for 24 hours.
3. Plot temperature and light together.

**Expected result:** Light peaks near noon; temperature peaks 2-3 hours later (thermal lag).

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 15. Colour and light reflection
*Topic:* Light  |  *Sensors:* IR reflective sensor  |  *Analysis check:* not simulated

**Procedure**
1. Coloured paper sheets at 5 mm from the sensor.
2. Log the reading for white, yellow, red, green, blue, black.
3. Rank colours.

**Expected result:** White reflects most, black least; compare ranking with a phone-camera brightness estimate.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 16. Conductivity of salt solutions
*Topic:* Chemistry  |  *Sensors:* Conductivity probe  |  *Analysis check:* VALIDATED

**Procedure**
1. Distilled water plus 0, 0.5, ... 3 g salt per 100 ml.
2. Dip the two-nail probe 2 cm each time; rinse between readings.
3. Plot reading against concentration.

**Expected result:** Roughly linear at low concentration; simulation recovers the slope within 7 %. Probe polarisation: read quickly.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 17. Human reaction time
*Topic:* Biology  |  *Sensors:* Button + LED  |  *Analysis check:* VALIDATED

**Procedure**
1. LED lights after a random delay; press the button as fast as possible.
2. Collect 40 trials per student.
3. Mean and standard deviation; compare hands.

**Expected result:** About 0.2 s mean with 0.03-0.05 s spread; simulation recovers 0.21 s within 10 %.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 18. Insulation test: three cups
*Topic:* Heat  |  *Sensors:* 3 x NTC  |  *Analysis check:* not simulated

**Procedure**
1. Same hot water in three cups: bare, wrapped in cloth, wrapped in foil.
2. Log all three for 30 minutes.
3. Compare the cooling constants k.

**Expected result:** Insulated cups have smaller k; rank the materials.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 19. Water level by ultrasound (tank calibration)
*Topic:* Mathematics and technology  |  *Sensors:* Ultrasonic distance  |  *Analysis check:* not simulated

**Procedure**
1. Sensor facing down from the top of a transparent container of known cross-section area.
2. Add 200 ml of water at a time and log the distance to the surface.
3. Plot volume against (empty distance minus measured distance).

**Expected result:** A straight line whose slope equals the container's cross-section area; this is the principle of tank-level sensing.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

## 20. Greenhouse jar model
*Topic:* Earth science  |  *Sensors:* 2 x NTC  |  *Analysis check:* not simulated

**Procedure**
1. Two identical jars in sunlight, one with a lid.
2. Log both temperatures for 2 hours.
3. Compare.

**Expected result:** The covered jar warms more and stays warmer; discuss the limits of the model.

**Common errors:** loose connections, unshielded sensors, reading before values settle, wrong units. Repeat each measurement three times.

