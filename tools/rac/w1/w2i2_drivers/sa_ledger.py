# RAC W2I2-A (order §3): vertical stature-budget ledger. Standing height is decomposed into reproducible vertical contributions:
#   ground -> ankle (J-2 ankle) | ankle -> knee | knee -> hip (J-2 hip) | hip -> hip-joint station u91 (Saurin pelvic transition; MPFB 0 by
#   definition) | lower axial trunk (station -> costal u123; MPFB rig hip -> spine_03 costal proxy) | thoracic (costal -> inlet u152; MPFB
#   costal proxy -> suprasternal) | neck (inlet / suprasternal -> chin) | head height (chin -> vertex).  Shares of standing height (tail excluded).
# Saurin from the regional-route bodies (sa_build) + J-2 joints (sa_joints transport); MPFB from rig joints and the meas json.
# Also reports the comparator leg shares that bound the candidates (Durrim, Marchfolk, Grask, Fenn / Aelari / Vael, Sagekin, Halvren, Skarn).
# Usage: python3 sa_ledger.py OUT.json
import sys, os, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i_drivers')); sys.path.insert(0, os.path.dirname(D))
import sa_build as B, sa_joints as SJ
from arm_measure import load
R = '/home/claude/wayfarer-design/reviews'
REG = {}
for f in ('rac-w2c-gr-evidence/registry.json', 'rac-w2d-go-evidence/registry.json', 'rac-w2e-sg-evidence/registry.json', 'rac-w2g-hv-evidence/registry.json', 'rac-w2f-elf-evidence/registry.json'):
    REG.update(json.load(open(R + '/' + f)))
CL = json.load(open(R + '/rac-w2h-sr-evidence/closure/registry_closure.json')); REG['DU137C'] = CL['DU137']
W = SJ.anchors(SJ.base_joints())

def sa_ledger(P, q, k):
    M = B.measure(P, q, k); H = M['height']; J, _ = SJ.transport(P, W)
    a = 0.5 * (J['AL'][2] + J['AR'][2]); kn = 0.5 * (J['KL'][2] + J['KR'][2]); hp = 0.5 * (J['HL'][2] + J['HR'][2])
    chin = M['height'] - M['head_depth']
    seg = {"ground_ankle": a, "ankle_knee": kn - a, "knee_hip": hp - kn, "hip_pelvic_transition": M['u_hip'] - hp, "lower_axial_trunk": M['u_costal'] - M['u_hip'],
           "thoracic": M['u_inlet'] - M['u_costal'], "neck": chin - M['u_inlet'], "head_height": M['head_depth']}
    return dict(height=H, cm=seg, share={kk: v / H for kk, v in seg.items()}, sum_check=sum(seg.values()) - H, hip_share=hp / H, station_share=M['u_hip'] / H, head_len=M['head_len'],
                head_len_ratio=M['head_len'] / H)
def mp_ledger(key):
    e = REG[key]; m = json.load(open(e['meas'] + '_meas.json'))['combined']; H = m['stature']; mm = m['mean']
    d = load(e['meas'] + '_rest.npz'); J = d['joints']; h = lambda n: float(J[n][0][2])
    kn = 0.5 * (h('calf_l') + h('calf_r')); hp = mm['hip_height']; a = mm['ankle_height']; cost = m['suprasternal_u'] - m['thoracic_vertical']; HH = m['ratio']['HH_share'] * H
    seg = {"ground_ankle": a, "ankle_knee": kn - a, "knee_hip": hp - kn, "hip_pelvic_transition": 0.0, "lower_axial_trunk": cost - hp, "thoracic": m['thoracic_vertical'],
           "neck": (H - HH) - m['suprasternal_u'], "head_height": HH}
    return dict(height=H, cm=seg, share={kk: v / H for kk, v in seg.items()}, sum_check=sum(seg.values()) - H, hip_share=hp / H)
if __name__ == '__main__':
    out = {"saurin": {}, "comparators": {}}
    for bid, p, h in (("SA-M188", {}, B.H0), ("SA-F188", B.CEN, B.H0), ("SA-M168", {}, 168.0), ("SA-M203", {}, 203.0), ("SA-M208", {}, 208.0)):
        P, q = B.C.build(p); P2, q2, k = B.at_stature(P, q, h); out["saurin"][bid] = sa_ledger(P2, q2, k)
        print(bid, {kk: round(v, 4) for kk, v in out["saurin"][bid]['share'].items()}, 'sum %.2e' % out["saurin"][bid]['sum_check'], flush=True)
    for key in ("MF168", "MF190", "MF203", "DU137C", "GR208", "GR218", "FN181", "AE190", "VA190", "AE203", "SG190", "HV190", "SK190", "SK208", "GO208"):
        if key not in REG: print('missing', key); continue
        try: out["comparators"][key] = mp_ledger(key); print(key, round(out["comparators"][key]['hip_share'], 4), {kk: round(v, 4) for kk, v in out["comparators"][key]['share'].items()}, flush=True)
        except Exception as ex: print('fail', key, ex)
    json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
