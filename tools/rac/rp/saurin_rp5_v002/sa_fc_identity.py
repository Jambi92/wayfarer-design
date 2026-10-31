# sa_fc_identity.py CAGE.npz OUT.json : Saurin identity metrics (saurin_rp5_v001/sa_identity.py definitions) on SA_RP5_WORK_v001 source vs the full cage,
# SA-M188 and SA-F188 independently (cage realized from its barycentric embedding on each body).
import sys, os, json, types, numpy as np
CG, OUT = sys.argv[1:3]; W = '/tmp/claude-0/rt/sa'
src = open('/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v001/sa_identity.py').read().split("LMm = {k: v['p_cm']")[0].replace("OUT = sys.argv[1]; ", "")
src = src.replace("VM = b['v'].astype(float); F = b['f'].astype(np.int64); VF = np.load(W + '/src/saurin_w2_SA-F188_realization.npz')['v'].astype(float)",
                  "F = b['f'].astype(np.int64); _w = np.load(W + '/work/SA_RP5_WORK_v001.npz'); VM = _w['v_M'].astype(float); VF = _w['v_F'].astype(float)")
ns = {}; exec(src, ns)
z = np.load(CG); Q = z['Q']; fi, bc = z['tri'], z['bc']; Tc = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
LMm = {k: v['p_cm'] for k, v in ns['LM'].items()}; LMf = {k: ns['carry'](v).tolist() for k, v in LMm.items()}; res = {}
for bid, VS, L in (('SA-M188', ns['VM'], LMm), ('SA-F188', ns['VF'], LMf)):
    Vc = (bc[:, :, None] * VS[ns['F'][fi]]).sum(1); s_ = ns['metrics'](VS, L)
    Fsave = ns['F']; ns['F'] = Tc; c_ = ns['metrics'](Vc, L); ns['F'] = Fsave
    res[bid] = {k: dict(source=s_[k], cage=c_[k], diff=round(c_[k] - s_[k], 4) if isinstance(s_[k], (int, float)) else None) for k in s_}
    print(bid, {k: v['diff'] for k, v in res[bid].items()})
res['note'] = ('landmark-defined metrics (lower axial trunk, forearm/arm, femur/leg, rostral projection, orbit spacing) use the same landmark set on source '
               'and cage (cage T-6 landmark fit <= 1 mm); section / extent metrics (stature, thorax, pelvic band, tail areas, heel) are measured on the cage surface itself')
json.dump(res, open(OUT, 'w'), indent=1)
