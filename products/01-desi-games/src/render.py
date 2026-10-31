# -*- coding: utf-8 -*-
"""Print-ready PDF generator for the Desi Games Studio (Pillow with RAQM text shaping for Hindi/Telugu).
Usage: python render.py <out_dir>   (needs: pip install pillow; apt install fonts-noto-core libraqm0)
Cards are 63 x 88 mm, 3 x 3 per A4 page at 200 dpi, with crop marks."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont
import content as C
from content import NAMES, RULES

DPI = 200
def mm(v): return int(round(v * DPI / 25.4))
A4 = (mm(210), mm(297))
CW, CH = mm(63), mm(88)
FD = "/usr/share/fonts/truetype/noto/"
FONTS = {"en": ("NotoSans-Regular.ttf", "NotoSans-Bold.ttf"), "hi": ("NotoSansDevanagari-Regular.ttf", "NotoSansDevanagari-Bold.ttf"),
         "te": ("NotoSansTelugu-Regular.ttf", "NotoSansTelugu-Bold.ttf")}
_cache = {}
def _real(lang, size_pt, bold=False):
    key = (lang, size_pt, bold)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FD + FONTS[lang][1 if bold else 0], int(size_pt * DPI / 72), layout_engine=ImageFont.Layout.RAQM)
    return _cache[key]

class MixedFont:
    """Font proxy: Latin letters are drawn with Noto Sans, everything else with the script's own Noto font
    (the Devanagari/Telugu fonts have no Latin letters, so mixed lines would show empty boxes)."""
    def __init__(self, lang, size_pt, bold): self.lang, self.pt, self.bold = lang, size_pt, bold; self.size = int(size_pt * DPI / 72)
    def runs(self, text):
        out, cur, kind = [], "", None
        for ch in text:
            if ch.isascii() and ch.isalpha(): k = "en"            # Latin letters: Noto Sans
            elif ord(ch) > 127: k = "en" if self.lang == "en" else self.lang   # Devanagari/Telugu letters and symbols: the script font
            else: k = kind or ("en" if self.lang == "en" else self.lang)       # digits, spaces, punctuation: stay in the current run
            if k != kind and cur: out.append((kind, cur)); cur = ""
            kind = k; cur += ch
        if cur: out.append((kind, cur))
        return out
    def real(self, kind): return _real("en" if kind == "en" else self.lang, self.pt, self.bold)

class MDraw(ImageDraw.ImageDraw):
    def text(self, xy, text, fill=None, font=None, **kw):
        if isinstance(font, MixedFont):
            x, y = xy
            for kind, run in font.runs(text):
                f = font.real(kind); super().text((x, y), run, fill=fill, font=f, **kw); x += super().textlength(run, font=f)
        else: super().text(xy, text, fill=fill, font=font, **kw)
    def textlength(self, text, font=None, **kw):
        if isinstance(font, MixedFont):
            return sum(super(MDraw, self).textlength(run, font=font.real(kind), **kw) for kind, run in font.runs(text))
        return super().textlength(text, font=font, **kw)

def font(lang, size_pt, bold=False): return MixedFont(lang, size_pt, bold)

def tri(d, x, y, parts, pt, fill, center_w=None):
    """Draw 'English / Hindi / Telugu' on one line, each part in its own font. parts = [(lang, text), ...]."""
    segs = []
    for i, (lang, t) in enumerate(parts):
        if i: segs.append(("en", "  /  "))
        segs.append((lang, t))
    total = sum(d.textlength(t, font=font(l, pt, True)) for l, t in segs)
    if center_w: x = x + (center_w - total) / 2
    for l, t in segs:
        d.text((x, y), t, font=font(l, pt, True), fill=fill); x += d.textlength(t, font=font(l, pt, True))

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def block(d, x, y, text, f, maxw, fill=(20, 20, 20), gap=1.25, center=False):
    """Draw wrapped text, return the y after the block."""
    for ln in wrap(d, text, f, maxw):
        tx = x + (maxw - d.textlength(ln, font=f)) / 2 if center else x
        d.text((tx, y), ln, font=f, fill=fill)
        y += int(f.size * gap)
    return y

def card_base(color, w=CW, h=CH, band=mm(11)):
    im = Image.new("RGB", (w, h), "white"); d = MDraw(im)
    d.rounded_rectangle((2, 2, w - 3, h - 3), radius=mm(3), outline=color, width=6, fill=(255, 253, 247))
    d.rounded_rectangle((2, 2, w - 3, band), radius=mm(3), fill=color)
    d.rectangle((2, band // 2, w - 3, band), fill=color)
    return im, d

def upside_down(im, text, lang, size_pt, xy, maxw, fill=(90, 90, 90)):
    """Print small text rotated 180 degrees (answers on cards)."""
    t = Image.new("RGBA", (maxw, int(size_pt * DPI / 72 * 1.8)), (0, 0, 0, 0)); td = MDraw(t)
    td.text((0, 0), text, font=font(lang, size_pt), fill=fill + (255,))
    im.paste(t.rotate(180), xy, t.rotate(180))

def sheet(cards, cols=3, rows=3, cw=CW, ch=CH):
    """Lay cards out 3x3 on A4 pages with crop marks; returns list of page images."""
    pages = []
    per = cols * rows
    ox = (A4[0] - cols * cw) // 2; oy = (A4[1] - rows * ch) // 2
    for s in range(0, len(cards), per):
        pg = Image.new("RGB", A4, "white"); d = MDraw(pg)
        for i, c in enumerate(cards[s:s + per]):
            x = ox + (i % cols) * cw; y = oy + (i // cols) * ch
            pg.paste(c, (x, y))
        for cx in range(cols + 1):                                    # crop marks
            for cy in range(rows + 1):
                px, py = ox + cx * cw, oy + cy * ch
                d.line((px - 14, py, px - 4, py), fill=(120, 120, 120), width=2); d.line((px + 4, py, px + 14, py), fill=(120, 120, 120), width=2)
                d.line((px, py - 14, px, py - 4), fill=(120, 120, 120), width=2); d.line((px, py + 4, px, py + 14), fill=(120, 120, 120), width=2)
        pages.append(pg)
    return pages

def save_pdf(pages, path):
    pages[0].save(path, "PDF", resolution=DPI, save_all=True, append_images=pages[1:], quality=88)

# ------------------------------------------------------------------ Cricket Dhamaka
def icon(d, kind, cx, cy, r, col):
    if kind == "Defend":                                              # shield
        d.polygon([(cx - r, cy - r), (cx + r, cy - r), (cx + r, cy + r * 0.2), (cx, cy + r), (cx - r, cy + r * 0.2)], fill=col)
        d.line((cx, cy - r * 0.7, cx, cy + r * 0.6), fill="white", width=8); d.line((cx - r * 0.6, cy - r * 0.1, cx + r * 0.6, cy - r * 0.1), fill="white", width=8)
    elif kind == "Drive":                                             # bat + ball
        d.polygon([(cx - r, cy + r), (cx - r + 40, cy + r), (cx + r * 0.5, cy - r * 0.4), (cx + r * 0.2, cy - r * 0.7)], fill=col)
        d.ellipse((cx + r * 0.5, cy - r * 0.9, cx + r * 0.95, cy - r * 0.45), fill=(200, 40, 40))
    elif kind == "Slog":                                              # starburst
        pts = []
        for i in range(16):
            a = math.pi * 2 * i / 16; rr = r if i % 2 == 0 else r * 0.5
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(pts, fill=col)
        d.text((cx - 28, cy - 34), "6", font=font("en", 22, True), fill="white")
    elif kind == "Yorker":                                            # ball landing on the crease line
        d.line((cx - r, cy + r * 0.7, cx + r, cy + r * 0.7), fill=col, width=10)
        d.ellipse((cx - r * 0.25, cy + r * 0.2, cx + r * 0.25, cy + r * 0.7), fill=(200, 40, 40))
        d.line((cx - r, cy - r * 0.6, cx - r * 0.25, cy + r * 0.3), fill=col, width=6)
    elif kind == "Bouncer":                                           # bounce arrow up
        d.line((cx - r, cy + r * 0.8, cx - r * 0.2, cy + r * 0.8), fill=col, width=8)
        d.line((cx - r * 0.2, cy + r * 0.8, cx + r * 0.8, cy - r * 0.7), fill=col, width=8)
        d.polygon([(cx + r * 0.8, cy - r * 0.9), (cx + r * 0.55, cy - r * 0.45), (cx + r * 1.0, cy - r * 0.5)], fill=col)
        d.ellipse((cx - r * 0.55, cy + r * 0.55, cx - r * 0.1, cy + r), fill=(200, 40, 40))
    elif kind == "Spin":                                              # curved arrow
        d.arc((cx - r, cy - r, cx + r, cy + r), 20, 300, fill=col, width=14)
        d.polygon([(cx + r * 0.8, cy - r * 0.5), (cx + r * 1.15, cy), (cx + r * 0.45, cy - r * 0.05)], fill=col)
        d.ellipse((cx - r * 0.25, cy - r * 0.25, cx + r * 0.25, cy + r * 0.25), fill=(200, 40, 40))

def cricket_card(kind, idx, is_shot):
    col = (30, 120, 70) if is_shot else (170, 40, 50)
    im, d = card_base(col)
    word = NAMES["shot_word"] if is_shot else NAMES["deliv_word"]
    tri(d, mm(0), mm(2), [("en", word["en"]), ("hi", word["hi"]), ("te", word["te"])], 8.5, "white", center_w=CW)
    icon(d, kind, CW // 2, mm(33), mm(15), col)
    names = (NAMES["shots"] if is_shot else NAMES["deliv"])
    y = mm(54)
    for lang, pt in (("en", 15), ("hi", 14), ("te", 13)):
        f = font(lang, pt, True)
        t = names[lang][idx]
        d.text(((CW - d.textlength(t, font=f)) / 2, y), t, font=f, fill=col); y += int(f.size * 1.35)
    return im

def cricket_table_page():
    pg = Image.new("RGB", A4, "white"); d = MDraw(pg)
    d.text((mm(15), mm(12)), NAMES["title"]["en"] + " - " + NAMES["table_title"]["en"], font=font("en", 20, True), fill=(30, 30, 30))
    d.text((mm(15), mm(23)), NAMES["title"]["hi"] + " - " + NAMES["table_title"]["hi"], font=font("hi", 14, True), fill=(30, 30, 30))
    d.text((mm(15), mm(31)), NAMES["title"]["te"] + " - " + NAMES["table_title"]["te"], font=font("te", 13, True), fill=(30, 30, 30))
    x0, y0, cw, ch = mm(15), mm(70), mm(55), mm(50)
    d.rectangle((x0, y0 - mm(20), x0 + 4 * cw - mm(40), y0), fill=(240, 240, 240))
    for j in range(3):                                                # column headers (deliveries)
        xx = x0 + mm(30) + j * mm(52)
        d.rectangle((xx, y0 - mm(20), xx + mm(52), y0), fill=(170, 40, 50), outline="white", width=3)
        for k, (lang, pt) in enumerate((("en", 12), ("hi", 11), ("te", 10))):
            d.text((xx + mm(3), y0 - mm(19) + k * mm(6)), NAMES["deliv"][lang][j], font=font(lang, pt, True), fill="white")
    for i in range(3):
        yy = y0 + i * mm(42)
        d.rectangle((x0, yy, x0 + mm(30), yy + mm(42)), fill=(30, 120, 70), outline="white", width=3)
        for k, (lang, pt) in enumerate((("en", 12), ("hi", 11), ("te", 10))):
            d.text((x0 + mm(2), yy + mm(4) + k * mm(8)), NAMES["shots"][lang][i], font=font(lang, pt, True), fill="white")
        for j in range(3):
            xx = x0 + mm(30) + j * mm(52)
            d.rectangle((xx, yy, xx + mm(52), yy + mm(42)), fill=(255, 253, 247), outline=(150, 150, 150), width=3)
            faces = C.CRICKET_TABLE[i][j]
            for k, fc in enumerate(faces):                            # die face k+1 -> faces[k]
                cx = xx + mm(8) + (k % 3) * mm(15); cy = yy + mm(8) + (k // 3) * mm(17)
                d.rounded_rectangle((cx - mm(5), cy - mm(5), cx + mm(5), cy + mm(5)), radius=mm(1.5), outline=(190, 190, 190), width=2)
                d.text((cx - mm(5), cy - mm(15)), "", font=font("en", 6))
                col = (200, 30, 30) if fc == "W" else (20, 20, 20)
                f = font("en", 14, True); d.text((cx - d.textlength(fc, font=f) / 2, cy - f.size * 0.62), fc, font=f, fill=col)
                f2 = font("en", 6); d.text((cx - mm(4.5), cy + mm(5.2)), str(k + 1), font=f2, fill=(130, 130, 130))
    y = y0 + 3 * mm(42) + mm(8)
    for lang, pt in (("en", 11), ("hi", 11), ("te", 10)):
        y = block(d, mm(15), y, NAMES["table_note"][lang], font(lang, pt), A4[0] - mm(30), gap=1.4) + mm(2)
    return pg

def score_sheet():
    pg = Image.new("RGB", A4, "white"); d = MDraw(pg)
    tri(d, mm(15), mm(12), [("en", "Cricket Dhamaka - Score sheet"), ("hi", "स्कोर शीट"), ("te", "స్కోరు షీట్")], 15, (30, 30, 30))
    for inn in range(2):
        y = mm(35) + inn * mm(120)
        d.text((mm(15), y), f"Innings {inn + 1}   Batter: ______________   Bowler: ______________", font=font("en", 12, True), fill=(30, 30, 30))
        for b in range(12):
            x = mm(15) + (b % 6) * mm(30); yy = y + mm(15) + (b // 6) * mm(28)
            d.rounded_rectangle((x, yy, x + mm(27), yy + mm(24)), radius=mm(2), outline=(120, 120, 120), width=3)
            d.text((x + mm(2), yy + mm(1)), f"Ball {b + 1}", font=font("en", 8), fill=(120, 120, 120))
        d.text((mm(15), y + mm(75)), "Wickets  W [  ]  W [  ]            Total runs: ________", font=font("en", 12, True), fill=(30, 30, 30))
    return pg

# ------------------------------------------------------------------ Ganit Ladder
def ganit_board(path):
    import sim_ganit_mandi as S
    cell = int(59.4 / 25.4 * 150)                                      # 59.4 mm cells at 150 dpi => 594 mm board
    head = int(cell * 1.1); W = cell * 10; H = W + head
    im = Image.new("RGB", (W, H), (255, 248, 230)); d = MDraw(im)
    def centre(n):
        r = (n - 1) // 10; c = (n - 1) % 10
        if r % 2 == 1: c = 9 - c
        return c * cell + cell // 2, head + (9 - r) * cell + cell // 2
    pal = [(255, 224, 178), (200, 230, 201), (187, 222, 251), (248, 187, 208)]
    fnum = lambda s: ImageFont.truetype(FD + "NotoSans-Bold.ttf", s)
    for n in range(1, 101):
        cx, cy = centre(n); r = (n - 1) // 10; c = (n - 1) % 10
        d.rectangle((cx - cell // 2, cy - cell // 2, cx + cell // 2, cy + cell // 2), fill=pal[(r + c) % 4], outline=(120, 100, 80), width=3)
        d.text((cx - cell // 2 + 14, cy - cell // 2 + 8), str(n), font=fnum(int(cell * 0.2)), fill=(70, 50, 30))
        if n in S.QUESTION_SQUARES:
            d.ellipse((cx + cell * 0.05, cy + cell * 0.0, cx + cell * 0.42, cy + cell * 0.37), fill=(240, 120, 20))
            d.text((cx + cell * 0.15, cy - cell * 0.02), "?", font=fnum(int(cell * 0.3)), fill="white")
    d.text((cell * 0.4, cell * 0.12), "GANIT LADDER", font=fnum(int(cell * 0.5)), fill=(120, 40, 20))
    tri(d, cell * 5.2, cell * 0.2, [("hi", "गणित सीढ़ी"), ("te", "గణిత నిచ్చెన")], 28, (120, 40, 20))
    d.text((cell * 5.2, cell * 0.7), "START (0)  ->  FINISH 100", font=fnum(int(cell * 0.2)), fill=(80, 60, 40))
    for a, b in S.LADDERS.items():                                     # ladders
        (x1, y1), (x2, y2) = centre(a), centre(b)
        L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; px, py = -uy, ux
        for s in (-1, 1): d.line((x1 + px * s * 22, y1 + py * s * 22, x2 + px * s * 22, y2 + py * s * 22), fill=(139, 90, 43), width=14)
        for k in range(int(L // 70)):
            t = 35 + k * 70; d.line((x1 + ux * t - px * 22, y1 + uy * t - py * 22, x1 + ux * t + px * 22, y1 + uy * t + py * 22), fill=(160, 110, 60), width=10)
    for a, b in S.SNAKES.items():                                      # snakes: head at a (high), tail at b (low)
        (x1, y1), (x2, y2) = centre(a), centre(b)
        L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; px, py = -uy, ux
        pts = []
        for i in range(61):
            t = i / 60; off = 38 * math.sin(t * math.pi * 3.2) * (1 - 0.25 * t)
            pts.append((x1 + (x2 - x1) * t + px * off, y1 + (y2 - y1) * t + py * off, 20 - 12 * t))
        for x, y, w in pts: d.ellipse((x - w, y - w, x + w, y + w), fill=(34, 139, 34))
        hx, hy, _ = pts[0]; d.ellipse((hx - 26, hy - 26, hx + 26, hy + 26), fill=(20, 110, 30))
        d.ellipse((hx - 14, hy - 12, hx - 4, hy - 2), fill="white"); d.ellipse((hx + 4, hy - 12, hx + 14, hy - 2), fill="white")
        d.ellipse((hx - 11, hy - 9, hx - 7, hy - 5), fill="black"); d.ellipse((hx + 7, hy - 9, hx + 11, hy - 5), fill="black")
    im.save(path, "PDF", resolution=150, quality=85)

def ganit_cards():
    cards = []
    for q, ans in C.table_cards():
        im, d = card_base((230, 120, 20))
        tri(d, 0, mm(2), [("en", "GANIT"), ("hi", "पहाड़ा"), ("te", "ఎక్కం")], 9, "white", center_w=CW)
        f = font("en", 30, True); d.text(((CW - d.textlength(q, font=f)) / 2, mm(38)), q, font=f, fill=(60, 40, 20))
        upside_down(im, f"= {ans}", "en", 14, (mm(18), mm(74)), mm(40))
        cards.append(im)
    return cards

# ------------------------------------------------------------------ India Yatra
def yatra_cards(lang):
    cards = []
    for n, (q, opts, ans) in enumerate(C.yatra_cards(lang), 1):
        im, d = card_base((20, 90, 160))
        d.text((mm(4), mm(1.5)), f"INDIA YATRA  #{n}", font=font("en", 10, True), fill="white")
        y = block(d, mm(5), mm(15), q, font(lang, 12.5 if lang == "en" else 12, True), CW - mm(10), fill=(20, 40, 70), gap=1.4)
        y += mm(3)
        for L, o in zip("ABC", opts):
            d.rounded_rectangle((mm(5), y, CW - mm(5), y + mm(9)), radius=mm(2), outline=(20, 90, 160), width=3)
            d.text((mm(7), y + mm(1)), L, font=font("en", 12, True), fill=(20, 90, 160))
            d.text((mm(14), y + mm(1.2)), o, font=font(lang, 12), fill=(30, 30, 30)); y += mm(11)
        upside_down(im, ans, "en", 10, (mm(28), mm(80)), mm(10))
        cards.append(im)
    return cards

# ------------------------------------------------------------------ Sabzi Mandi
def mandi_item_cards():
    cards = []
    for price, en, hi, te, col in C.ITEMS:
        for _ in range(2):
            im, d = card_base(col)
            f = font("en", 24, True); t = f"Rs {price}"
            d.text(((CW - d.textlength(t, font=f)) / 2, mm(3)), t, font=f, fill="white")
            d.ellipse((mm(14), mm(20), mm(49), mm(55)), fill=col, outline=(60, 60, 60), width=4)
            y = mm(60)
            for lang, nm, pt in (("en", en, 14), ("hi", hi, 13), ("te", te, 12)):
                f = font(lang, pt, True); d.text(((CW - d.textlength(nm, font=f)) / 2, y), nm, font=f, fill=(30, 30, 30)); y += int(f.size * 1.35)
            cards.append(im)
    return cards

NOTE_COL = {1: (200, 170, 120), 2: (170, 190, 150), 5: (120, 170, 200), 10: (200, 150, 120), 20: (210, 120, 150), 50: (150, 120, 200)}
def money_cards():
    w, h = mm(88), mm(44); cards = []
    for den, cnt in C.MONEY.items():
        for _ in range(cnt):
            im = Image.new("RGB", (w, h), "white"); d = MDraw(im); col = NOTE_COL[den]
            d.rounded_rectangle((2, 2, w - 3, h - 3), radius=mm(2.5), outline=col, width=6, fill=tuple(min(255, c + 60) for c in col))
            f = font("en", 34, True); t = f"Rs {den}"
            d.text(((w - d.textlength(t, font=f)) / 2, mm(6)), t, font=f, fill=(40, 40, 40))
            tri(d, 0, mm(30), [("en", "Sabzi Mandi"), ("hi", "सब्ज़ी मंडी"), ("te", "కూరగాయల మార్కెట్")], 8.5, (70, 70, 70), center_w=w)
            cards.append(im)
    return cards

# ------------------------------------------------------------------ rules pages
def rules_pdf(game, path):
    pages = []
    for lang in ("en", "hi", "te"):
        pg = Image.new("RGB", A4, "white"); d = MDraw(pg)
        lines = RULES[game][lang]
        title = {"cricket": NAMES["title"][lang], "ganit": {"en": "Ganit Ladder", "hi": "गणित सीढ़ी", "te": "గణిత నిచ్చెన"}[lang],
                 "yatra": {"en": "India Yatra", "hi": "इंडिया यात्रा", "te": "ఇండియా యాత్ర"}[lang],
                 "mandi": {"en": "Sabzi Mandi", "hi": "सब्ज़ी मंडी", "te": "కూరగాయల మార్కెట్"}[lang]}[game]
        d.text((mm(18), mm(15)), title, font=font(lang, 30, True), fill=(30, 60, 110))
        y = mm(40)
        for i, ln in enumerate(lines):
            y = block(d, mm(18), y, ("" if i == 0 else f"{i}.  ") + ln, font(lang, 14 if i else 15, i == 0), A4[0] - mm(36), gap=1.5) + mm(4)
        pages.append(pg)
    save_pdf(pages, path)

def main(out):
    os.makedirs(out, exist_ok=True)
    cc = [cricket_card(n, i, True) for _ in range(2) for i, n in enumerate(NAMES["shots"]["en"])] + \
         [cricket_card(n, i, False) for _ in range(2) for i, n in enumerate(NAMES["deliv"]["en"])]
    save_pdf(sheet(cc) + [cricket_table_page(), score_sheet()], os.path.join(out, "cricket_dhamaka_print.pdf"))
    ganit_board(os.path.join(out, "ganit_ladder_board.pdf"))
    save_pdf(sheet(ganit_cards()), os.path.join(out, "ganit_ladder_cards.pdf"))
    for lang in ("en", "hi", "te"): save_pdf(sheet(yatra_cards(lang)), os.path.join(out, f"india_yatra_cards_{lang}.pdf"))
    save_pdf(sheet(mandi_item_cards()), os.path.join(out, "sabzi_mandi_items.pdf"))
    save_pdf(sheet(money_cards(), cols=2, rows=6, cw=mm(88), ch=mm(44)), os.path.join(out, "sabzi_mandi_money.pdf"))
    for g in RULES: rules_pdf(g, os.path.join(out, f"rules_{g}.pdf"))
    print("wrote", sorted(os.listdir(out)))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "out")
