# RAC W1h driver AS RUN: R-14 sensitivity (AD-W1H-12). Each identity-relevant GO construction magnitude is perturbed by +/- STEP
# (the factor multiplied by 1 +/- step, default 2 %; ka amplitude +/- 0.05) one at a time; the reference body and GOR-BODY-03 are
# rebuilt and every accepted GO skeletal row is re-checked with the ordinary AD-G10 rule (not the solver margins). Reported per
# perturbation: rows that are no longer PASS (reference / 03), skin thoracic breadth vs SK, skin flank flare, arm clearance.
# Usage: python3 sensitivity.py params.json out.json [step]
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1g_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn5, gn3, profile_bump as PB, arm_clearance as AC, alpc_invariance as AI

def evaluate(x, name):
    B, sc = gn5.unpack(x); wd = gn5.G + '/sens'
    r, C = gn3.build("GO", name, B, sc, wd=wd); rows = gn3.checks("GO", name, wd=wd)
    bad = ["%s: %s" % (y['result'], y['check'][:70]) for y in rows if (y['cand'] == 'GO' or y.get('b') == 'GO') and y['result'] not in ('PASS', 'REPORT', 'NOT RUN')]
    H = r['r6']['stature']; tb = C['ref_skin']['S2'][0] / H   # AS RUN: plane-section reading (reads ~0.7 % wider than the directional check)
    from arm_measure import load as _load; import bony_envelope as BE
    tbm = BE.fast_stations(_load(wd + '/%s_rest.npz' % name), section=False)['S2'][0] / H   # directional-check reading (thorax_breadth_share)
    base, donor, did = gn5.STRESS["03"]; gn3.build("GO", name + '-03', B, sc, wd=wd, base=base, donor=donor, did=did); rr = gn3.checks("GO", name + '-03', wd=wd)
    bad03 = ["%s: %s" % (y['result'], y['check'][:70]) for y in rr if y['cand'] == 'GO' and AI.keep_row(y['check']) and y['result'] not in ('PASS', 'REPORT', 'NOT RUN')]
    return {"not_pass_ref": bad, "not_pass_251": bad03, "skin_TB_over_H": tb, "skin_TB_vs_SK": tb / gn5.SK_TB - 1, "skin_TB_vs_SK_measure_layer": tbm / gn5.SK_TB - 1,
            "flank_flare": PB.flank_flare(wd + '/%s_r6.npz' % name)['flank_flare'], "arm_clearance_cm": AC.signed_clearance(wd + '/%s_r6.npz' % name), "stature": H}

if __name__ == '__main__':
    x0 = json.load(open(sys.argv[1]))["x"]; out = sys.argv[2]; step = float(sys.argv[3]) if len(sys.argv) > 3 else 0.02
    res = {"step": step, "params": dict(zip(gn5.NAMES, x0)), "base": evaluate(x0, 'S0'), "perturb": {}}
    json.dump(res, open(out, 'w'), indent=1, default=float)
    for i, n in enumerate(gn5.NAMES):
        for sg in (-1, 1):
            x = list(x0)
            x[i] = x0[i] + sg * 0.05 if n == "Aka" else x0[i] * (1 + sg * step)     # factor +/- step (2 %); ka amplitude +/- 0.05
            res["perturb"]["%s %+d" % (n, sg)] = {"value": x[i], **evaluate(x, 'S%d%s' % (i, 'm' if sg < 0 else 'p'))}
            json.dump(res, open(out, 'w'), indent=1, default=float); print(n, sg, len(res["perturb"]["%s %+d" % (n, sg)]["not_pass_ref"]), len(res["perturb"]["%s %+d" % (n, sg)]["not_pass_251"]), flush=True)
