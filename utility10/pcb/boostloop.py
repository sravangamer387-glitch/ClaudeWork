"""Seeded routing with failed nets promoted to the front each round: python3 boostloop.py <board> <seed> [rounds]  -> out/<board> when 0 failures (or best found)."""
import sys, os, json, subprocess, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); mod, seed = sys.argv[1], sys.argv[2]; rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 6
boost = [x for x in os.environ.get("BOOST0", "").split(",") if x]; best = None
for r in range(rounds):
    env = dict(os.environ, BOOST=",".join(boost)); subprocess.run([sys.executable, os.path.join(HERE, "build.py"), mod, "seed", seed], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    d = os.path.join(HERE, "out", f"{mod}_s{seed}"); rr = os.path.join(d, "route_report.json")
    if not os.path.exists(rr): print("round", r, "no report", flush=True); continue
    fails = json.load(open(rr))["route_failures"]; print("round", r, "boost", boost, "failures", len(fails), [f[0] for f in fails], flush=True)
    if best is None or len(fails) < best[0]:
        best = (len(fails), d + "_best")
        if os.path.exists(best[1]): shutil.rmtree(best[1])
        shutil.copytree(d, best[1])
    if not fails: break
    boost += [n for n in dict.fromkeys(f[0] for f in fails) if n not in boost]
dst = os.path.join(HERE, "out", mod)
if best:
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(best[1], dst); print("FINAL failures", best[0], flush=True)
