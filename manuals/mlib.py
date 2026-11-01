"""Helpers for generating MANUFACTURING_MANUAL.md files from the repository's own data (READMEs, release folders)."""
import os, re, csv, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p): return open(os.path.join(ROOT, p)).read() if os.path.exists(os.path.join(ROOT, p)) else ""
def section(text, head, level=2):
    m = re.search(r"^" + "#" * level + r" " + head + r".*?\n(.*?)(?=^#{1," + str(level) + r"} |\Z)", text, re.S | re.M | re.I)
    return m.group(1).strip() if m else ""
def first_line(text, key):
    for l in text.splitlines():
        if l.lower().startswith(key.lower()): return l.strip()
    return ""
def board_info(release_dir, name):
    d = os.path.join(ROOT, release_dir)
    ver = json.load(open(os.path.join(d, "5_verification", "verification.json"))); rdy = json.load(open(os.path.join(d, "5_verification", "readiness.json")))
    bom = list(csv.DictReader(open(os.path.join(d, "2_assembly", name + "_BOM_full.csv"))))
    readme = open(os.path.join(d, "README.md")).read()
    return dict(ver=ver, rdy=rdy, bom=bom, readme=readme, dir=release_dir)
def bom_table(bom, only=None):
    rows = ["| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |", "|---|---|---|---|---|---|"]
    for r in bom:
        if r["Value"] == "TP": continue
        asm = r["Assembly"]
        if only and asm != only: continue
        rows.append(f"| {r['Ref']} | {r['Value']} | {r['Footprint'].split(':')[-1]} | {r['Manufacturer part'] or '-'} | {r['LCSC #'] or '-'} | {asm} |")
    return "\n".join(rows)
def count_tp(bom): return sum(1 for r in bom if r["Value"] == "TP")
def prod_bom(readme):
    s = section(readme, r"Designed production BOM")
    return s
def gen_header(title, readme_first_line, status):
    return f"# {title}: manufacturing manual\n\n> **Status:** {status}\n> {readme_first_line}\n"
