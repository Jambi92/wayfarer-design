# vf_comp.py OUT.json : Vael elf-frame order §13 composition-firewall diagnostic. The same configuration-1 / configuration-2 sources (VD2 and VD2 + VEF1 VF2)
# are rebuilt at three source compositions -- narrow / low muscle (muscle 0, weight 0), balanced (0.5 / 0.5, the reference), broad / higher muscle
# (muscle 1.0, weight 0.5) -- with the skeleton held (height macro held). If VEF1 is a structural (skeletal-frame) term and not a thinness preset, its
# effect is a near-constant RELATIVE change across compositions (shoulder span, mid-shaft sections) while the absolute composition differences
# between states are preserved. Builds go to $VF_DIR/comp (bpy); measurements reuse vf_eval.py's shaft section.
import sys, os, json, subprocess, numpy as np
OUT = sys.argv[1]; VF = os.environ.get('VF_DIR', '/tmp/claude-0/rt/vf'); RB = '/home/claude/wayfarer-design/reviews/reference-assets/builds'
W1 = '/home/claude/wayfarer-design/tools/rac/w1'; BP = '/home/claude/stc/bin/python3'; D = VF + '/comp'; os.makedirs(D, exist_ok=True)
COMP = {'narrow_low_muscle': {'muscle': 0.0, 'weight': 0.0}, 'balanced': None, 'broad_high_muscle': {'muscle': 1.0, 'weight': 0.5}}
SRC = {'c1': {'VD2': RB + '/VAL4-R1-VD2_build.json', 'VF2': VF + '/cand/VAL4-R1-VD2-VF2_build.json'}, 'c2': {'VD2': RB + '/VALF178-R1-VD2_build.json', 'VF2': VF + '/cand/VALF178-R1-VD2-VF2_build.json'}}
jobs = []
for c, S in SRC.items():
    for st, ov in COMP.items():
        if ov is None: continue
        op = os.path.join(D, 'ov_%s.json' % st); json.dump(ov, open(op, 'w'))
        for t, b in S.items():
            nid = '%s-%s-%s' % (c, t, st)
            if not os.path.exists(os.path.join(D, nid + '_rest.npz')): jobs.append([BP, W1 + '/build_variant.py', b, op, D, nid])
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), jobs))
def shaft(z, b, H):
    V = z['V'].astype(float); keep = z['keep']; J = json.loads(str(z['joints'])); out = []
    for sd in ('l', 'r'):
        h, t = np.array(J[b + '_' + sd][0]), np.array(J[b + '_' + sd][1]); ax = t - h; L = np.linalg.norm(ax); ax /= L
        grp = ('upperarm', 'lowerarm') if b in ('upperarm', 'lowerarm') else ('thigh', 'calf')
        wb = sum(z['w_' + g + '_' + sd] for g in grp); q = V - h; tt = q @ ax; P0 = q - np.outer(tt, ax)
        s = keep & (wb > 0.3) & (np.abs(tt - 0.5 * L) < 2.5 * H / 173.14) & (np.linalg.norm(P0, axis=1) < 14.0 * H / 173.14)
        P = P0[s]; ev, evc = np.linalg.eigh(np.cov(P.T)); a1, a2 = evc[:, -1], evc[:, -2]; out.append(np.sqrt(((P @ a1).max() - (P @ a1).min()) * ((P @ a2).max() - (P @ a2).min())))
    return float(np.mean(out))
def meas(p):
    z = np.load(p); V = z['V'].astype(float); keep = z['keep']; H = V[keep, 2].max() - V[keep, 2].min(); J = json.loads(str(z['joints']))
    up = np.linalg.norm(np.array(J['upperarm_l'][0]) - np.array(J['upperarm_r'][0]))
    wa = sum(z['w_' + k] for k in ('upperarm_l', 'upperarm_r')); m = keep & (wa > 0.3); bid = V[m, 0].max() - V[m, 0].min()
    return dict(stature=H, clavicle_span=up, bideltoid_proxy=bid, **{b: shaft(z, b, H) for b in ('upperarm', 'lowerarm', 'thigh', 'calf')})
res = dict(note=__doc__ if False else 'see header', states={})
for c, S in SRC.items():
    for st in COMP:
        if COMP[st] is None:
            a = meas({'c1': '/tmp/claude-0/rt/vd/cand/VAL4-R1-VD2_rest.npz', 'c2': '/tmp/claude-0/rt/vd/cand/VALF178-R1-VD2_rest.npz'}[c]); b = meas(S['VF2'].replace('_build.json', '_rest.npz'))
        else:
            a = meas(os.path.join(D, '%s-VD2-%s_rest.npz' % (c, st))); b = meas(os.path.join(D, '%s-VF2-%s_rest.npz' % (c, st)))
        res['states']['%s %s' % (c, st)] = dict(VD2={k: round(v, 3) for k, v in a.items()}, VF2={k: round(v, 3) for k, v in b.items()}, VF2_vs_VD2_pct={k: round(100 * (b[k] / a[k] - 1), 2) for k in a})
        print(c, '%-18s' % st, res['states']['%s %s' % (c, st)]['VF2_vs_VD2_pct'], '| VD2 upperarm %.2f thigh %.2f cm' % (a['upperarm'], a['thigh']))
json.dump(res, open(OUT, 'w'), indent=1)
