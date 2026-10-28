# vf_ear_root.py OUT.json : Vael elf-frame order §21 -- ear-branch proposal evidence: does the frozen Fenn-v002 engineering ear root interface (the
# 52-vertex root loop per side on v005, reused unchanged by frozen Aelari AE-E2) fit the Vael VF2 head? Reads the root loop (v005 indices from
# FENN_EAR_BRANCH_MAP_v005_v002.json) on each family realization (same v005 vertex order) and reports, per side and normalised by head height: loop
# perimeter, vertical / AP extent, plane tilt (normal vs the lateral axis), centroid position relative to the head (height below vertex, AP offset from the
# tragus-less head centre), planarity, and the minimum edge length -- against frozen Fenn (both configurations), frozen Aelari (both) and Marchfolk v005.
import json, numpy as np
OUT = __import__('sys').argv[1]
RL = json.load(open('/home/claude/wayfarer-design/reviews/rac-rp3-evidence/fenn_ear_v002/mapping/FENN_EAR_BRANCH_MAP_v005_v002.json'))['root_loops_v005']
BODIES = {'Vael VF2 c1': '/tmp/claude-0/rt/vf/prod/fam/VAL4-R1-VD2-VF2_fam.npz', 'Vael VF2 c2': '/tmp/claude-0/rt/vf/prod/fam/VALF178-R1-VD2-VF2_fam.npz',
          'Fenn c1 (FNL4-CF2)': '/tmp/claude-0/rt/fn/final/fam/FNL4-CF2_fam.npz', 'Fenn c2 (FNF181-CF2)': '/tmp/claude-0/rt/fn/final/fam/FNF181-CF2_fam.npz',
          'Aelari c1 (AEL1-R1)': '/tmp/claude-0/rt/ae/final/fam/AEL1-R1_fam.npz', 'Aelari c2 (AELF190-R1)': '/tmp/claude-0/rt/ae/final/fam/AELF190-R1_fam.npz',
          'Marchfolk v005 c1': '/tmp/claude-0/rt/v5/cand/MF-M-R_v005.npz'}
res = dict(root_loop='52 v005 vertices per side (FENN_EAR_BRANCH_MAP_v005_v002.json)', bodies={})
import os
for nm, p in BODIES.items():
    if not os.path.exists(p): res['bodies'][nm] = 'missing'; continue
    V = np.load(p)['V'].astype(float); top = V[:, 2].max(); out = {}
    hd = V[V[:, 2] > top - 26]; HH = 0.0
    for sd in ('l', 'r'):
        L = V[RL[sd]]; c = L.mean(0); per = float(np.linalg.norm(np.roll(L, -1, 0) - L, axis=1).sum()); e = np.linalg.norm(np.roll(L, -1, 0) - L, axis=1)
        u, s, vt = np.linalg.svd(L - c); nrm = vt[2]; nrm = nrm if nrm[0] * (1 if sd == 'l' else -1) > 0 else -nrm
        out[sd] = dict(perimeter_cm=per, vertical_extent_cm=float(L[:, 2].max() - L[:, 2].min()), ap_extent_cm=float(L[:, 1].max() - L[:, 1].min()),
                       centroid_below_vertex_cm=float(top - c[2]), centroid_lateral_cm=float(abs(c[0])), centroid_ap_cm=float(c[1] - hd[:, 1].mean()),
                       plane_tilt_from_lateral_deg=float(np.degrees(np.arccos(min(1.0, abs(nrm[0]))))), planarity_rms_cm=float(s[2] / np.sqrt(len(L))), min_edge_cm=float(e.min()), max_edge_cm=float(e.max()))
    hh = top - V[V[:, 2] > top - 30][:, 2].min()
    res['bodies'][nm] = dict(sides=out, mean={k: float(np.mean([out[s][k] for s in out])) for k in out['l']})
for nm, d in res['bodies'].items():
    if d == 'missing': print(nm, 'missing'); continue
    m = d['mean']; print('%-24s per %.2f  vert %.2f  ap %.2f  below-vertex %.2f  lat %.2f  tilt %.1f  planar %.3f  edges %.3f-%.3f' % (nm, m['perimeter_cm'], m['vertical_extent_cm'], m['ap_extent_cm'], m['centroid_below_vertex_cm'], m['centroid_lateral_cm'], m['plane_tilt_from_lateral_deg'], m['planarity_rms_cm'], m['min_edge_cm'], m['max_edge_cm']))
json.dump(res, open(OUT, 'w'), indent=1)
