"""ASTRADAND spell cards (63 x 88 mm) -> SVG per card + one A4 print sheet PDF (3 x 3, crop marks). Hindi names need native-speaker proofreading before print."""
import os, math, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sim"))
import numpy as np, cairosvg
import gesture_sim as G
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"); os.makedirs(OUT, exist_ok=True)
INFO = {
 "agni": ("AGNI", "अग्नि", "Fire", "Draw a circle, starting at the top, clockwise.", "Flickering orange flame; warm rising tune.", 25, "#e8590c"),
 "vajra": ("VAJRA", "वज्र", "Lightning", "Draw a bold Z: across, down-left, across.", "Crackling white flashes; sharp zaps.", 35, "#4c6ef5"),
 "jala": ("JALA", "जल", "Water", "Draw a wave: two smooth humps left to right.", "Rolling blue wave along the crystal.", 20, "#1c7ed6"),
 "raksha": ("RAKSHA", "रक्षा", "Shield", "Draw a triangle, apex first, clockwise.", "Pulsing teal shield glow; deep two-note chime.", 30, "#0ca678"),
 "prakash": ("PRAKASH", "प्रकाश", "Light", "Draw a straight line upward.", "Bright golden flash that fades to a glow.", 10, "#f59f00"),
 "vayu": ("VAYU", "वायु", "Wind", "Draw a check mark: short down, long up.", "Green sweep running along the crystal.", 15, "#37b24d"),
}
def glyph(name, w=40, h=40, ox=0, oy=0, colour="#222"):
    T = G.SHAPES[name]; Q = T - T.mean(axis=0); sc = max(np.ptp(Q[:, 0]), np.ptp(Q[:, 1])); Q = Q / sc * min(w, h) * 0.85
    pts = [(ox + w / 2 + x, oy + h / 2 - y) for x, y in Q]
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts[::3] + [pts[-1]])
    ex, ey = pts[-1]; px, py = pts[-4]; ang = math.atan2(ey - py, ex - px); a1 = (ex - 3.2 * math.cos(ang - 0.45), ey - 3.2 * math.sin(ang - 0.45)); a2 = (ex - 3.2 * math.cos(ang + 0.45), ey - 3.2 * math.sin(ang + 0.45))
    return f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><polygon points="{ex:.1f},{ey:.1f} {a1[0]:.1f},{a1[1]:.1f} {a2[0]:.1f},{a2[1]:.1f}" fill="{colour}"/><circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="1.7" fill="#2b8a3e"/>'
def card(name):
    en, hi, el, how, fx, cost, col = INFO[name]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="63mm" height="88mm" viewBox="0 0 63 88" font-family="Noto Sans, DejaVu Sans, sans-serif">
<rect x="0.5" y="0.5" width="62" height="87" rx="3" fill="#10141f" stroke="{col}" stroke-width="1.2"/><rect x="3" y="3" width="57" height="82" rx="2" fill="none" stroke="{col}" stroke-width="0.4" stroke-dasharray="1.5,1"/>
<text x="31.5" y="11" text-anchor="middle" font-size="6.5" font-weight="700" fill="{col}">{en}</text><text x="31.5" y="17.2" text-anchor="middle" font-size="4.6" fill="#e9ecef" font-family="Noto Sans Devanagari, Noto Sans, sans-serif">{hi}  -  {el}</text>
<rect x="9" y="21" width="45" height="38" rx="2" fill="#f1f3f5"/>{glyph(name, 40, 34, 11.5, 23)}
<text x="31.5" y="64" text-anchor="middle" font-size="2.4" fill="#dee2e6">{how}</text><text x="31.5" y="70" text-anchor="middle" font-size="2.5" fill="#adb5bd">{fx}</text>
<circle cx="10" cy="77" r="4.2" fill="{col}"/><text x="10" y="78.6" text-anchor="middle" font-size="4.4" font-weight="700" fill="#10141f">{cost}</text><text x="16" y="78.2" font-size="2.6" fill="#ced4da">mana</text>
<text x="31.5" y="83" text-anchor="middle" font-size="2.2" fill="#868e96">green dot = start; hold TRIGGER while drawing</text></svg>'''
def combo():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="63mm" height="88mm" viewBox="0 0 63 88" font-family="Noto Sans, DejaVu Sans, sans-serif"><rect x="0.5" y="0.5" width="62" height="87" rx="3" fill="#10141f" stroke="#e64980" stroke-width="1.2"/>
<text x="31.5" y="12" text-anchor="middle" font-size="6" font-weight="700" fill="#e64980">MAHASTRA</text><text x="31.5" y="18" text-anchor="middle" font-size="4.6" fill="#e9ecef" font-family="Noto Sans Devanagari, Noto Sans, sans-serif">महास्त्र  -  Combo</text>
<text x="31.5" y="32" text-anchor="middle" font-size="3.4" fill="#f8f9fa">Cast AGNI, then VAJRA</text><text x="31.5" y="38" text-anchor="middle" font-size="3.4" fill="#f8f9fa">within 4 seconds.</text>
<text x="31.5" y="50" text-anchor="middle" font-size="2.8" fill="#ced4da">The crystal turns magenta; long fanfare;</text><text x="31.5" y="55" text-anchor="middle" font-size="2.8" fill="#ced4da">only the normal costs are paid (25 + 35).</text>
<text x="31.5" y="68" text-anchor="middle" font-size="2.6" fill="#868e96">Tip: draw the second shape right after the first.</text></svg>'''
def rules():
    L = ["Hold the TRIGGER, draw the shape in the air,", "release. The crystal shows the spell.", "", "Mana starts at 100 (the lit crystals).", "It refills 2 every second.", "A fizzle (unknown shape) costs 5.", "Each spell has a 1 s cooldown.", "", "After 45 s of stillness the wand sleeps.", "Wave it or press the trigger to wake it.", "Red blink = batteries low."]
    t = "".join(f'<text x="31.5" y="{22 + i * 5}" text-anchor="middle" font-size="2.7" fill="#dee2e6">{l}</text>' for i, l in enumerate(L))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="63mm" height="88mm" viewBox="0 0 63 88" font-family="Noto Sans, DejaVu Sans, sans-serif"><rect x="0.5" y="0.5" width="62" height="87" rx="3" fill="#10141f" stroke="#adb5bd" stroke-width="1.2"/><text x="31.5" y="13" text-anchor="middle" font-size="5.5" font-weight="700" fill="#f8f9fa">HOW TO CAST</text>{t}</svg>'
def back():
    rings = "".join(f'<circle cx="31.5" cy="44" r="{r}" fill="none" stroke="#5c7cfa" stroke-width="0.5" stroke-dasharray="{1 + r % 4},{1.5 + r % 3}"/>' for r in range(6, 30, 4))
    rays = "".join(f'<line x1="31.5" y1="44" x2="{31.5 + 28 * math.cos(a * math.pi / 6):.1f}" y2="{44 + 28 * math.sin(a * math.pi / 6):.1f}" stroke="#364fc7" stroke-width="0.3"/>' for a in range(12))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="63mm" height="88mm" viewBox="0 0 63 88" font-family="Noto Sans, DejaVu Sans, sans-serif"><rect x="0.5" y="0.5" width="62" height="87" rx="3" fill="#0b1020" stroke="#5c7cfa" stroke-width="1.2"/>{rays}{rings}<text x="31.5" y="81" text-anchor="middle" font-size="4" letter-spacing="0.8" fill="#91a7ff">ASTRADAND</text></svg>'
cards = {n: card(n) for n in G.NAMES}; cards["combo"] = combo(); cards["rules"] = rules(); cards["back"] = back()
for k, v in cards.items(): open(os.path.join(OUT, f"card_{k}.svg"), "w").write(v)
# A4 sheet: 3 x 3 cards with crop marks
order = G.NAMES + ["combo", "rules", "back"]; W, H = 210, 297; cw, ch = 63, 88; mx = (W - 3 * cw) / 2; my = (H - 3 * ch) / 2
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">']
for i, k in enumerate(order):
    x = mx + (i % 3) * cw; y = my + (i // 3) * ch; inner = cards[k].split(">", 1)[1].rsplit("</svg>", 1)[0]
    parts.append(f'<g transform="translate({x},{y})" font-family="Noto Sans, DejaVu Sans, sans-serif">{inner}</g>')
for i in range(4):
    for edge in (mx + i * cw,): parts.append(f'<line x1="{edge}" y1="2" x2="{edge}" y2="{my - 1}" stroke="black" stroke-width="0.15"/><line x1="{edge}" y1="{H - my + 1}" x2="{edge}" y2="{H - 2}" stroke="black" stroke-width="0.15"/>')
    for edge in (my + i * ch,): parts.append(f'<line x1="2" y1="{edge}" x2="{mx - 1}" y2="{edge}" stroke="black" stroke-width="0.15"/><line x1="{W - mx + 1}" y1="{edge}" x2="{W - 2}" y2="{edge}" stroke="black" stroke-width="0.15"/>')
parts.append("</svg>"); open(os.path.join(OUT, "spell_cards_A4.svg"), "w").write("\n".join(parts))
cairosvg.svg2pdf(url=os.path.join(OUT, "spell_cards_A4.svg"), write_to=os.path.join(OUT, "spell_cards_A4.pdf")); cairosvg.svg2png(url=os.path.join(OUT, "spell_cards_A4.svg"), write_to="/tmp/shots/cards.png", output_width=900, background_color="white")
print("cards written", len(cards))
