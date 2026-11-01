# MITTI-NETRA concept
**Problem.** Farms and small civil structures have few sensors because cabled installations and subscriptions are costly, and mains and WiFi are absent. Soil moisture drives irrigation decisions; slow tilt or strain drift in a wall, shed or slope often precedes visible failure.

**Idea.** One cheap node that sleeps almost all the time, wakes on a timer or on an accelerometer interrupt, evaluates drift locally and uses a cellular (LTE-M / NB-IoT) link only when it has something to say. The adaptive schedule reports every 6 h normally, hourly after rain, every 30 min on WATCH and every 10 min on ALARM; a low battery stretches routine reports but never throttles an alarm.

**Crossover.** Edge decision-making (debounced alarm state machine, adaptive interval) keeps cellular airtime and battery use low. The same node doubles as the field gateway for a camera companion that sends a few numbers (canopy cover) instead of images.

**Non-goals.** Certified structural health monitoring; safety-critical alarms; long-range mesh; indoor use.
