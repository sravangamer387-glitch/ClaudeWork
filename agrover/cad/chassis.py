"""Ag-rover chassis plates for laser cutting (6 mm plywood or acrylic) as one SVG per plate (mm, 1 unit = 1 mm). UNPROTOTYPED first-pass layout.
Plates: base (400 x 300) with 4 motor-bracket slots, battery strap slots, electronics mounting holes and wire pass-throughs; top deck (360 x 260) for the solar panel; sensor bracket.
usage: python3 chassis.py -> out/base_plate.svg, out/top_deck.svg, out/sensor_bracket.svg, out/chassis_info.json"""
import os, json
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"); os.makedirs(OUT, exist_ok=True)
def svg(name, w, h, cuts, holes, note):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">', f'<!-- {note} -->', f'<rect x="0.1" y="0.1" width="{w-0.2}" height="{h-0.2}" rx="8" fill="none" stroke="red" stroke-width="0.2"/>']
    for (x, y, cw, ch) in cuts: s.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="none" stroke="red" stroke-width="0.2"/>')
    for (x, y, d) in holes: s.append(f'<circle cx="{x}" cy="{y}" r="{d/2}" fill="none" stroke="red" stroke-width="0.2"/>')
    s.append("</svg>"); open(os.path.join(OUT, name + ".svg"), "w").write("\n".join(s))
W, H = 400, 300
motor_slots = [(20, 20, 70, 6), (310, 20, 70, 6), (20, 274, 70, 6), (310, 274, 70, 6)]          # slots for 4 U-bracket motor mounts (bolt through slot to slide the axle)
bolt_holes = [(x + 10, y + 3, 4.2) for (x, y, w, h) in motor_slots] + [(x + 60, y + 3, 4.2) for (x, y, w, h) in motor_slots]
strap = [(120, 90, 60, 5), (120, 205, 60, 5)]                                                   # battery strap slots (cable ties or velcro)
elec = [(260 + dx * 20, 100 + dy * 20, 3.2) for dx in range(4) for dy in range(5)]              # 20 mm grid of M3 holes for the electronics sub-plate
passthru = [(200, 150, 20)]
svg("base_plate", W, H, strap + motor_slots, bolt_holes + elec + passthru, "base plate 400x300, 6 mm")
svg("top_deck", 360, 260, [], [(30 + 60 * i, 30, 5.2) for i in range(5)] + [(30 + 60 * i, 230, 5.2) for i in range(5)], "top deck 360x260 with 10 standoff holes M5 (solar panel on top, tilt by shims)")
svg("sensor_bracket", 120, 50, [], [(15, 25, 3.2), (105, 25, 3.2), (60, 25, 16.5), (30, 25, 16.5), (90, 25, 16.5)], "front bracket: three 16 mm ultrasonic transducer holes (left, centre, right) and two M3 mounts")
json.dump(dict(base_plate_mm=[W, H], top_deck_mm=[360, 260], sensor_bracket_mm=[120, 50], material="6 mm plywood or acrylic", note="check the motor bracket and wheel dimensions of your chosen gear motors before cutting"), open(os.path.join(OUT, "chassis_info.json"), "w"), indent=1)
print("ok")
