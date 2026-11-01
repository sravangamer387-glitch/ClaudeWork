# KINETIC concept

## Problem
Small CNC-style machines, camera sliders and robot joints are driven by hobby stepper drivers that move with trapezoidal or abrupt profiles, shaking the machine and wearing bearings; and bearings fail without warning. Industrial controllers solve both but cost far more and are closed.

## Idea
One open controller that (a) makes smooth, provably limited motion and (b) listens to the motor it drives. The planner's commanded speed becomes an input to the condition-monitoring model, which is the part that makes the AI small enough for a microcontroller.

## Target user and use cases
Makers and small labs: 3-axis plotters and camera sliders, pick-and-place experiments, test rigs for bearings, teaching mechatronics. AI/vision pipelines on a Pi or PC send setpoints; the controller turns them into jerk-limited motion.

## Why this crossover
- Motion planning (Biagiotti-style S-curves) is textbook physics and testable to exact formulas.
- Bearing fault frequencies are fixed multiples of shaft speed, so a 10-feature model beats a large generic network and runs in microseconds.
- Everything is verifiable on a PC before hardware exists (done) and on a bench with a known fault bearing (not done).

## Non-goals
Closed-loop servo control, CAN, high-power drivers (above about 2 A per phase on these modules), safety-rated stops.
