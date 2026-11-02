"""Katha Cubes: 6 story dice x 6 words in English / Hindi / Telugu (words drawn as printed text; icons to be drawn by an illustrator).
Checks: 36 distinct English words, each die has one category, 6^6 = 46,656 distinct stories. Writes CSV and a cube-net SVG per die."""
import csv, os
DICE = {"Who": [("Elephant", "हाथी", "ఏనుగు"), ("Fisherman", "मछुआरा", "జాలరి"), ("Princess", "राजकुमारी", "రాకుమారి"), ("Robot", "रोबोट", "రోబో"), ("Monkey", "बंदर", "కోతి"), ("Grandmother", "दादी", "బామ్మ")],
        "Where": [("Railway station", "रेलवे स्टेशन", "రైల్వే స్టేషన్"), ("Mango orchard", "आम का बाग़", "మామిడి తోట"), ("Moon", "चाँद", "చంద్రుడు"), ("Charminar", "चारमीनार", "చార్మినార్"), ("Cricket ground", "क्रिकेट मैदान", "క్రికెట్ మైదానం"), ("Beach", "समुद्र तट", "సముద్ర తీరం")],
        "Wants": [("A lost kite", "खोई पतंग", "తప్పిపోయిన గాలిపటం"), ("A sweet laddoo", "मीठा लड्डू", "తీపి లడ్డు"), ("A secret map", "गुप्त नक्शा", "రహస్య పటం"), ("A friend", "एक दोस्त", "ఒక స్నేహితుడు"), ("Rain", "बारिश", "వర్షం"), ("A drum", "ढोल", "డోలు")],
        "Problem": [("Gets stuck", "फँस जाना", "చిక్కుకుపోవడం"), ("Is very late", "बहुत देर", "చాలా ఆలస్యం"), ("Loses the way", "रास्ता भूलना", "దారి తప్పడం"), ("Is afraid of the dark", "अँधेरे का डर", "చీకటి భయం"), ("Cannot stop laughing", "हँसी नहीं रुकती", "నవ్వు ఆగదు"), ("Is very hungry", "बहुत भूख", "చాలా ఆకలి")],
        "Helper": [("A clever crow", "चतुर कौआ", "తెలివైన కాకి"), ("A magic flute", "जादुई बाँसुरी", "మాయా వేణువు"), ("An auto driver", "ऑटो वाला", "ఆటో డ్రైవర్"), ("A talking parrot", "बोलता तोता", "మాట్లాడే చిలుక"), ("A kind teacher", "दयालु शिक्षक", "దయగల ఉపాధ్యాయుడు"), ("A tiny dragon", "छोटा ड्रैगन", "చిన్న డ్రాగన్")],
        "Ending": [("Everybody dances", "सब नाचते हैं", "అందరూ నృత్యం చేస్తారు"), ("A big feast", "बड़ी दावत", "పెద్ద విందు"), ("A new friend", "नया दोस्त", "కొత్త స్నేహితుడు"), ("A surprise gift", "अचानक तोहफ़ा", "అనుకోని బహుమతి"), ("It rains sweets", "मिठाइयों की बारिश", "మిఠాయిల వర్షం"), ("They fly home", "उड़कर घर", "ఎగిరి ఇంటికి")]}
OUT = os.path.join(os.path.dirname(__file__), "..", "out")
words = [w[0] for ws in DICE.values() for w in ws]; assert len(words) == len(set(words)) == 36
with open(os.path.join(OUT, "katha_cubes_words.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["die", "face", "english", "hindi", "telugu", "hindi_OK?", "telugu_OK?"])
    for d, ws in DICE.items():
        for i, x in enumerate(ws, 1): w.writerow([d, i] + list(x) + ["", ""])
S = 40; net = ['<svg xmlns="http://www.w3.org/2000/svg" width="260mm" height="%dmm" viewBox="0 0 260 %d" font-family="Noto Sans, Noto Sans Devanagari, Noto Sans Telugu, sans-serif"><g stroke="red" fill="none" stroke-width="0.3" font-size="4" >' % (6 * 62, 6 * 62)]
for di, (d, ws) in enumerate(DICE.items()):
    oy = di * 62 + 5; pos = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (1, 2)]
    for (cx, cy), x in zip(pos, ws):
        px, py = 10 + cx * S, oy + cy * 18 if False else oy + cy * 18
        net.append(f'<rect x="{10+cx*S}" y="{oy+cy*18}" width="{S}" height="18"/><text x="{12+cx*S}" y="{oy+cy*18+6}" fill="black" stroke="none">{x[0]}</text><text x="{12+cx*S}" y="{oy+cy*18+11}" fill="black" stroke="none">{x[1]}</text><text x="{12+cx*S}" y="{oy+cy*18+16}" fill="black" stroke="none">{x[2]}</text>')
net.append("</g></svg>")
open(os.path.join(OUT, "katha_cubes_net.svg"), "w", encoding="utf-8").write("\n".join(net))
txt = f"36 distinct English words on 6 dice ({', '.join(DICE)}). Distinct stories: {6**6:,}. Hindi and Telugu were written by me and are UNREVIEWED; the net SVG is a layout sheet (use a printer/illustrator for final 25 mm cubes with icons)."
open(os.path.join(os.path.dirname(__file__), "..", "docs", "results_story.md"), "w").write(txt + "\n"); print(txt)
