# RAC W1i driver: R-14 sensitivity on the final W1i candidate (order §8, §9), stricter than W1h: every one of the 15 gn6 values is
# perturbed alone by factor x (1 +/- 2 %) (ka amplitude +/- 0.05); the reference AND all four stature bodies (208 / 215 / 222 / 251 cm)
# are rebuilt and re-checked with the ORDINARY AD-G10 rule (not the solver margins): every GO reference skeletal row, ALPC-0...4 at each
# stature, ALPC-7 at every cross-height pair, thoracic breadth > SK (directional reading, 1 % convention), flank flare, arm clearance,
# skeleton / skin continuity readings and the low-composition waist reading.
# Usage: python3 sens6.py params.json out.json [step]
import sys, os, json, numpy as np
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gn6, gn3
from arm_measure import load
import bony_envelope as BE, profile_bump as PB, arm_clearance as AC, alpc_invariance as AI

def bad(rows, keep=None):
    return ["%s: %s" % (y['result'], y['check'][:80]) for y in rows if (y['cand'] == 'GO' or y.get('b') == 'GO') and y['result'] not in ('PASS', 'REPORT', 'NOT RUN')
            and (keep is None or keep(y))]

def evaluate(x, name):
    wd = gn6.G + '/sens6'; B, sc = gn6.unpack(x)
    r, C = gn3.build("GO", name, B, sc, wd=wd); H = r['r6']['stature']
    out = {"stature": H, "not_pass": {"ref": bad(gn3.checks("GO", name, wd=wd))}}
    tb = BE.fast_stations(load(wd + '/%s_rest.npz' % name), section=False)['S2'][0] / H
    out["skin_TB_vs_SK"] = tb / gn6.SK_TB - 1
    out["flank_flare"] = PB.flank_flare(wd + '/%s_r6.npz' % name)['flank_flare']; out["arm_clearance_cm"] = AC.signed_clearance(wd + '/%s_r6.npz' % name)
    out["skeleton"] = gn6.cont(wd + '/%s-LEAN_rest.npz' % name); out["skin"] = gn6.cont(wd + '/%s_rest.npz' % name)
    out["low_comp_waist_rise"] = gn6.waist_rise(wd + '/grid_%s/%s-C025025_rest.npz' % (name, name))
    for k, (base, donor, did) in gn6.HEIGHTS.items():
        nm = name + '-' + k; gn3.build("GO", nm, B, sc, wd=wd, base=base, donor=donor, did=did)
        out["not_pass"][k] = bad(gn3.checks("GO", nm, wd=wd), keep=lambda y: AI.keep_row(y['check']))
        for hs in gn6.PAIRS.get(k, ()):
            out["not_pass"]["%s vs SKB%d" % (k, hs)] = bad(gn6.pair_rows(wd, nm, hs))
    return out

def summary(v):
    n = sum(len(a) for a in v["not_pass"].values())
    return n, any(s.startswith("FAIL") for a in v["not_pass"].values() for s in a), v["skin_TB_vs_SK"] >= 0.01

if __name__ == '__main__':
    x0 = json.load(open(sys.argv[1]))["x"]; outp = sys.argv[2]; step = float(sys.argv[3]) if len(sys.argv) > 3 else 0.02
    res = {"step": step, "params": dict(zip(gn6.NAMES, x0)), "base": evaluate(x0, 'Z0'), "perturb": {}}
    json.dump(res, open(outp, 'w'), indent=1, default=float); print('base', summary(res["base"]), flush=True)
    jobs = []
    for i, n in enumerate(gn6.NAMES):
        for sg in (-1, 1):
            x = list(x0); x[i] = x0[i] + sg * 0.05 if n == "Aka" else x0[i] * (1 + sg * step); jobs.append(("%s %+d" % (n, sg), x[i], x, 'Z%d%s' % (i, 'm' if sg < 0 else 'p')))
    def run(j):
        k, val, x, nm = j; return k, {"value": val, **evaluate(x, nm)}
    with ThreadPoolExecutor(2) as ex:
        for k, v in ex.map(run, jobs):
            res["perturb"][k] = v; json.dump(res, open(outp, 'w'), indent=1, default=float); print(k, summary(v), flush=True)
