# RAC W1j sensitivity protocol (order §4, §7.5): identical to W1i (w1i_drivers/sens6.py: each of the 16 values alone x (1 +/- 2 %), ka
# amplitude +/- 0.05; ordinary AD-G10 rule on every GO reference row, ALPC-0...4 at every stature body, every ALPC-7 pair, thoracic
# breadth > SK beyond 1 %), on the W1j stature series (true 208 cm donor with its equal-height Broad Skarn 208 pair, 215, 222, 251 cm;
# gn7 patches the series), plus the low-composition continuity readings of the reference and 208 cm grid bodies.
# Usage: python3 sens7.py candidate.json out.json prefix [step]
import sys, os, json, numpy as np
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gn7, gn6, sens6

def evaluate(x, name):
    ev = sens6.evaluate(x, name); wd = gn6.G + '/sens6'
    ev["low_comp"] = {b: {**gn6.cont(wd + '/grid_%s/%s-C025025_rest.npz' % (b, b)), "waist_rise": gn6.waist_rise(wd + '/grid_%s/%s-C025025_rest.npz' % (b, b))}
                      for b in (name, name + '-208')}
    ev["skeleton_208"] = gn6.cont(wd + '/%s-208-LEAN_rest.npz' % name)
    return ev

if __name__ == '__main__':
    x0 = json.load(open(sys.argv[1]))["x"]; outp = sys.argv[2]; pre = sys.argv[3]; step = float(sys.argv[4]) if len(sys.argv) > 4 else 0.02
    res = {"step": step, "params": dict(zip(gn7.NAMES, x0)), "base": evaluate(x0, pre + '0'), "perturb": {}}
    json.dump(res, open(outp, 'w'), indent=1, default=float); print('base', sens6.summary(res["base"]), flush=True)
    jobs = []
    for i, n in enumerate(gn7.NAMES):
        for sg in (-1, 1):
            x = list(x0); x[i] = x0[i] + sg * 0.05 if n == "Aka" else x0[i] * (1 + sg * step); jobs.append(("%s %+d" % (n, sg), x[i], x, '%s%d%s' % (pre, i, 'm' if sg < 0 else 'p')))
    def run(j):
        k, val, x, nm = j; return k, {"value": val, **evaluate(x, nm)}
    with ThreadPoolExecutor(2) as ex:
        for k, v in ex.map(run, jobs):
            res["perturb"][k] = v; json.dump(res, open(outp, 'w'), indent=1, default=float); print(k, sens6.summary(v), flush=True)
