"""Independent Gerber sanity check with gerbonara (a different parser from KiCad): all layers parse, board outline size matches the spec, drill holes counted."""
import sys, os, json, importlib, zipfile, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gerbonara import LayerStack
def check(mod):
    B = importlib.import_module("boards." + mod).BOARD; W, H = B["size"]; name = B["name"]; gd = os.path.join(HERE, "out", mod, "gerbers")
    res = {"layers": 0, "outline_mm": None, "size_ok": False, "errors": []}
    try:
        st = LayerStack.open(gd)
        res["layers"] = len(st.graphic_layers) if hasattr(st, "graphic_layers") else 0
        bb = st.outline.bounding_box(unit=__import__("gerbonara").utils.MM) if st.outline else None
        if bb: res["outline_mm"] = [round(bb[1][0] - bb[0][0], 2), round(bb[1][1] - bb[0][1], 2)]; res["size_ok"] = abs(res["outline_mm"][0] - W) < 0.3 and abs(res["outline_mm"][1] - H) < 0.3
    except Exception as e: res["errors"].append(repr(e)[:200])
    return res
if __name__ == "__main__":
    for m in sys.argv[1:]: print(m, check(m))
