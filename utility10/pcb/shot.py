import sys,subprocess,glob,os
b=sys.argv[1]; d=sys.argv[2] if len(sys.argv)>2 else "out/"+b
pcb=glob.glob(d+"/*.kicad_pcb")[0]
for name,layers in (("top","F.Cu,Edge.Cuts,F.Silkscreen"),("bot","B.Cu,Edge.Cuts,B.Silkscreen")):
    svg=f"/tmp/shots/{b}_{name}.svg"
    subprocess.run(["kicad-cli","pcb","export","svg","--layers",layers,"--page-size-mode","2","--exclude-drawing-sheet","-o",svg,pcb],check=True,capture_output=True)
    subprocess.run(["rsvg-convert","-w","1600","-b","white",svg,"-o",svg[:-3]+"png"],check=True)
print("ok")
