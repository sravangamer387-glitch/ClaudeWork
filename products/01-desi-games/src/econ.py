#!/usr/bin/env python3
"""Per-game unit economics (marketplace, same fee model as the toy files). GST 5 % assumed for non-electric games (verify)."""
CLOSE, ADS, RET, GST = 30, 0.12, 0.08, 0.05
GAMES = [  # name, price, bom (print + box + packing), ship
    ("Cricket Dhamaka (card game)", 499, 90, 55), ("Ganit Ladder (board + table cards)", 799, 150, 90),
    ("India Yatra (quiz cards, 3 language decks)", 599, 110, 60), ("Sabzi Mandi (items + money + tray)", 799, 180, 90)]
def m(price, bom, ship):
    landed = bom * 1.08; net = price / (1 + GST)
    cont = net - landed - (price * (0 if price < 1000 else .08) + CLOSE + ship) - net * ADS - RET * landed
    return net, cont, cont / net
print("| Game | Price Rs | BOM guess Rs | Contribution Rs | Margin | Margin if BOM +30 % |\n|---|---|---|---|---|---|")
for n, p, b, s in GAMES:
    _, c, pc = m(p, b, s); _, c2, pc2 = m(p, b * 1.3, s)
    print(f"| {n} | {p} | {b} | {c:,.0f} | {pc:.0%} | {pc2:.0%} |")
