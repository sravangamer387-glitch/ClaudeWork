"""Run several randomised-order routing attempts in parallel and keep the best one: python3 multi.py <board> [n_seeds]"""
import sys, os, subprocess, json, shutil, time
HERE = os.path.dirname(os.path.abspath(__file__)); mod = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
best = None; seeds = list(range(1, n + 1)); running = []
def finish(p, s):
    global best
    rr = os.path.join(HERE, "out", f"{mod}_s{s}", "route_report.json")
    if os.path.exists(rr):
        f = len(json.load(open(rr))["route_failures"]); print("seed", s, "failures", f, flush=True)
        if best is None or f < best[0]: best = (f, s)
while seeds or running:
    while seeds and len(running) < 3:
        s = seeds.pop(0); running.append((subprocess.Popen([sys.executable, os.path.join(HERE, "build.py"), mod, "seed", str(s)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), s))
    time.sleep(3)
    for p, s in list(running):
        if p.poll() is not None: running.remove((p, s)); finish(p, s)
    if best and best[0] == 0:
        for p, s in running: p.kill()
        break
f, s = best; src = os.path.join(HERE, "out", f"{mod}_s{s}"); dst = os.path.join(HERE, "out", mod)
if os.path.exists(dst): shutil.rmtree(dst)
shutil.copytree(src, dst)
# the board file name is unchanged inside; copy ok. Clean up the others
for k in range(1, n + 1): shutil.rmtree(os.path.join(HERE, "out", f"{mod}_s{k}"), ignore_errors=True)
print("BEST seed", s, "failures", f)
