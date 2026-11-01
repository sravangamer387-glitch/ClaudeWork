"""Assembly section drawing (side view, plane y = 0) and cross-section: hilt halves, PCB, battery tube, crystal, from the generated STL files + the board/battery envelopes."""
import os, math
import numpy as np, trimesh, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import hilt as H
OUT = H.OUT
parts = {k: trimesh.load(os.path.join(OUT, k + ".stl")) for k in ("hilt_upper", "hilt_lower", "crystal")}
fig, ax = plt.subplots(2, 1, figsize=(16, 9), gridspec_kw={"height_ratios": [1, 1.2]})
for name, col in (("hilt_upper", "#4c6ef5"), ("hilt_lower", "#7048e8")):
    sec = parts[name].section(plane_origin=[0, 0.0, 0], plane_normal=[0, 1, 0])
    if sec is not None:
        for e in sec.entities: pts = sec.vertices[e.points]; ax[0].plot(pts[:, 0], pts[:, 2], color=col, lw=1.0)
ax[0].add_patch(Rectangle((H.BX0, H.BZ), H.BOARD_L, H.BOARD_T, fc="#2f9e44", ec="k", lw=0.5)); ax[0].text(H.BX0 + 2, H.BZ + 2.5, "PCB 146 x 26 x 1.6 (components up)", fontsize=8)
ax[0].add_patch(Rectangle((H.BX0 + 12, -14.3), 140, 12.6, fc="#fab005", ec="k", lw=0.5, alpha=0.5)); ax[0].text(H.BX0 + 16, -9.5, "3 x AAA in line (about 134 mm) in the battery tube", fontsize=8)
ax[0].add_patch(Rectangle((H.HEAD_X0, 5.4), H.HEAD_X1 - H.HEAD_X0, 12.4, fc="#99e9f2", ec="k", lw=0.4, alpha=0.6)); ax[0].text(H.HEAD_X0 + 2, 19, "diffuser crystal over six WS2812B pixels", fontsize=8)
ax[0].annotate("", xy=(0, -22), xytext=(H.L, -22), arrowprops=dict(arrowstyle="<->")); ax[0].text(H.L / 2, -25, f"overall {H.L:.0f} mm", ha="center")
ax[0].set_aspect("equal"); ax[0].set_title("ASTRADAND: longitudinal section (y = 0)"); ax[0].set_xlim(-5, H.L + 5); ax[0].set_ylim(-28, 24); ax[0].axis("off")
th = np.linspace(0, 2 * math.pi, 200); ax[1].plot(H.R_OUT * np.cos(th), H.R_OUT * np.sin(th), "#4c6ef5"); ax[1].plot(H.R_IN * np.cos(th), H.R_IN * np.sin(th), "#4c6ef5", lw=0.6)
ax[1].add_patch(Rectangle((-13, H.BZ), 26, H.BOARD_T, fc="#2f9e44", ec="k")); ax[1].add_patch(Circle((0, -8.0), 5.25, fc="#fab005", ec="k", alpha=0.6)); ax[1].add_patch(Circle((0, -8.0), 8.2, fill=False, ec="#868e96", ls="--"))
ax[1].add_patch(Rectangle((H.LED_Y - 3.4, 5.4), 6.8, 12.4, fc="#99e9f2", ec="k", alpha=0.6)); ax[1].add_patch(Rectangle((-12, H.BZ + H.BOARD_T), 24, 3, fc="none", ec="k", ls=":")); ax[1].text(0, 7.5, "components (up to 3 mm)", ha="center", fontsize=8)
ax[1].text(0, -2.5, "AAA 10.5 mm", ha="center", fontsize=8); ax[1].set_aspect("equal"); ax[1].set_title("cross-section: shell 34 mm, wall 2.4 mm, board and battery"); ax[1].axis("off")
plt.tight_layout(); plt.savefig(os.path.join(OUT, "assembly_section.png"), dpi=110); print("assembly_section.png written")
