#!/usr/bin/env python3
"""Shaded preview PNGs of every STL in out/ (matplotlib, no GPU) + a sectioned view of the sensor block. usage: python3 render.py"""
import glob, os
import numpy as np, trimesh, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

def shade(ax, tm, color=(0.55, 0.62, 0.72)):
    tris = tm.vertices[tm.faces]; n = tm.face_normals; light = np.array([0.4, -0.5, 0.75]); light /= np.linalg.norm(light)
    k = np.clip(0.35 + 0.65 * np.abs(n @ light), 0, 1)[:, None]
    pc = Poly3DCollection(tris, facecolors=np.hstack([np.array(color) * k, np.ones((len(k), 1))]), edgecolors="none"); ax.add_collection3d(pc)
    lo, hi = tm.bounds; c = (lo + hi) / 2; r = (hi - lo).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r); ax.set_box_aspect((1, 1, 1))
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")

for f in sorted(glob.glob(os.path.join(OUT, "*.stl"))):
    tm = trimesh.load(f); name = os.path.basename(f)[:-4]
    fig = plt.figure(figsize=(9, 4.6))
    for i, (el, az) in enumerate([(25, -60), (60, 120)]):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d"); shade(ax, tm); ax.view_init(el, az)
    fig.suptitle(f"{name}   {tm.extents[0]:.1f} x {tm.extents[1]:.1f} x {tm.extents[2]:.1f} mm", fontsize=10); fig.tight_layout()
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=90); plt.close(fig)

# section of the sensor block through the bore axis (XZ plane and YZ plane) to show the ports
sb = trimesh.load(os.path.join(OUT, "trishna_sensor_block.stl"))
fig, axs = plt.subplots(1, 2, figsize=(10, 5.4))
for ax, (normal, title, idx) in zip(axs, [((0, 1, 0), "section y = 0 (LEDs +X, transmission PD -X)", (0, 2)), ((1, 0, 0), "section x = 0 (scatter PD, DS18B20 on +Y)", (1, 2))]):
    sec = sb.section(plane_origin=(0, 0, 0), plane_normal=normal)
    for ent in sec.entities:
        pts = sec.vertices[ent.points]; ax.plot(pts[:, idx[0]], pts[:, idx[1]], "k-", lw=1)
    ax.set_aspect("equal"); ax.set_title(title, fontsize=9); ax.grid(alpha=0.3); ax.set_xlabel("mm"); ax.set_ylabel("z (up in service), mm")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "trishna_sensor_block_sections.png"), dpi=110); plt.close(fig)
print("rendered", len(glob.glob(os.path.join(OUT, "*.png"))), "images")
