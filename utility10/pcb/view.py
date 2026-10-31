import sys, subprocess, os
mod, name = sys.argv[1], sys.argv[2]; out = f"out/{mod}"
subprocess.run(["kicad-cli", "pcb", "export", "svg", "--layers", "F.Cu,F.SilkS,Edge.Cuts,F.Fab", "--output", f"{out}/view.svg", "--page-size-mode", "2", f"{out}/{name}.kicad_pcb"], capture_output=True)
subprocess.run(["/tmp/venv/bin/python", "-c", f"import cairosvg; cairosvg.svg2png(url='{out}/view.svg', write_to='{out}/view.png', output_width=1500)"])
