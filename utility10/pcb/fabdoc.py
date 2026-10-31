"""Fabrication notes PDF (stackup, finish, rules, drill table, board picture) from a built board. Run with the venv python."""
import sys, os, re, importlib, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
def drill_table(path):
    tools = {}; cur = None
    for line in open(path):
        m = re.match(r"T(\d+)C([\d.]+)", line)
        if m: tools[m.group(1)] = [float(m.group(2)), 0]; continue
        m = re.match(r"^T(\d+)\s*$", line.strip())
        if m: cur = m.group(1); continue
        if cur and re.match(r"^X[-\d.]+Y[-\d.]+", line.strip()): tools[cur][1] += 1
    return tools
def gen(mod):
    B = importlib.import_module("boards." + mod).BOARD; name = B["name"]; out = os.path.join(HERE, "out", mod); W, H = B["size"]
    drl = [f for f in os.listdir(os.path.join(out, "gerbers")) if f.endswith(".drl")]
    tools = {}
    for f in drl:
        for k, v in drill_table(os.path.join(out, "gerbers", f)).items(): tools[f"{f.split('.')[0].split('-')[-1] if '-' in f else 'PTH'}:{k}"] = v
    top = os.path.join(out, name + "_top.svg"); png = os.path.join(out, "_fab_top.png")
    import cairosvg; cairosvg.svg2png(url=top, write_to=png, output_width=1600)
    with PdfPages(os.path.join(out, name + "_fab_notes.pdf")) as pdf:
        fig = plt.figure(figsize=(11.69, 8.27)); ax = fig.add_axes([0.03, 0.30, 0.55, 0.62]); ax.imshow(mpimg.imread(png)); ax.axis("off"); ax.set_title(f"{B['title']}  rev {B.get('rev', 'A')}  -  {W} x {H} mm", fontsize=11)
        notes = ["FABRICATION NOTES", "1. Material: FR-4 TG135, 2 layers, finished thickness 1.6 mm +-10 %.", "2. Copper: 1 oz (35 um) finished, both sides.", f"3. Finish: {'ENIG (gold), required' if mod == 'rainplate' else 'HASL lead-free or ENIG'}.",
                 "4. Solder mask: green, both sides" + ("; mask OPEN over the whole comb area on the rain plate." if mod == "rainplate" else "."), "5. Silkscreen: white, top." , "6. Min track/space 0.2/0.2 mm (power 0.4 mm); min via 0.6/0.3 mm; min annular ring 0.15 mm.",
                 "7. Outline: Edge.Cuts, 2.0-2.5 mm corner radii; tolerance +-0.2 mm.", "8. IPC-6012 class 2; 100 % electrical test (netlist in Gerber job).", "9. No panelisation specified: add 5 mm rails / V-score if the assembler needs it.", "10. Date code / vendor marking: place in silkscreen area only."]
        fig.text(0.62, 0.92, "\n".join(notes), va="top", fontsize=8.2, family="monospace")
        rows = [["Tool", "Dia (mm)", "Count"]] + [[k, f"{v[0]:.2f}", str(v[1])] for k, v in sorted(tools.items())]
        ax2 = fig.add_axes([0.62, 0.40, 0.33, 0.2]); ax2.axis("off"); tb = ax2.table(cellText=rows, loc="upper left", cellLoc="left"); tb.auto_set_font_size(False); tb.set_fontsize(8); tb.scale(1, 1.2)
        fig.text(0.03, 0.22, f"Files: Gerber X2 (F/B Cu, Mask, Paste, Silk, Edge) + Excellon drill in the zip. Board origin = lower-left of Edge.Cuts after fab import; KiCad origin is top-left, y down.", fontsize=8)
        pdf.savefig(fig); plt.close(fig)
    return os.path.join(out, name + "_fab_notes.pdf")
if __name__ == "__main__": print(gen(sys.argv[1]))
