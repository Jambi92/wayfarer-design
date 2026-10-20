# delta15b.py V014.npz V015.npz OUTDIR : RP1F author-change masks (every moved vertex assigned to its feature) + delta control vs v014
import sys, json, os, numpy as np
a, b, out = sys.argv[1:4]; os.makedirs(out, exist_ok=True); fl = np.array([1, -1, 1])
V0 = np.load(a)['V'] * fl; V1 = np.load(b)['V'] * fl; d = np.linalg.norm(V1 - V0, axis=1) * 10
E = '/tmp/claude-0/rp1f/'; toes = json.load(open(E + 'toe_frames.json')); hands = json.load(open(E + 'hand_frames.json'))
feats = [('C_WHISKER_PADS', np.array([-2.7, -62.8, 183.2]), 6.0), ('C_WHISKER_PADS', np.array([6.8, -62.6, 183.2]), 6.0)]
feats += [('B_FOOT_CLAWS_' + k[0], np.array(v['T']), 2.5) for k, v in toes.items()]
feats += [('A_HAND_CLAWS_' + k[2], np.array(v['T']), 3.2) for k, v in hands.items()]
mv = np.where(d > 1e-4)[0]; lab = np.full(len(mv), '', object)
D = np.stack([np.linalg.norm(V0[mv] - c, axis=1) / r for _, c, r in feats], 1); j = D.argmin(1); ok = D[np.arange(len(mv)), j] < 1
for i in np.where(ok)[0]: lab[i] = feats[j[i]][0]
R = {}
for nm in sorted(set(f[0] for f in feats)):
    m = mv[lab == nm]; np.save(os.path.join(out, nm + '_vertices.npy'), m)
    R[nm] = dict(moved_vertices=int(len(m)), max_displacement_mm=round(float(d[m].max()), 3) if len(m) else 0.0,
                 bbox_cm=[V1[m].min(0).round(2).tolist(), V1[m].max(0).round(2).tolist()] if len(m) else None)
R['outside_masks_moved_vertices'] = int((~ok).sum()); R['outside_masks_max_mm'] = round(float(d[mv[~ok]].max()), 4) if (~ok).any() else 0.0
R['total_moved_vertices'] = int(len(mv))
R['bbox_delta_mm'] = dict(min=((V1.min(0) - V0.min(0)) * 10).round(4).tolist(), max=((V1.max(0) - V0.max(0)) * 10).round(4).tolist())
R['stature_delta_mm'] = round(float(((V1[:, 2].max() - V1[:, 2].min()) - (V0[:, 2].max() - V0[:, 2].min())) * 10), 4)
json.dump(R, open(os.path.join(out, 'delta_v014_to_v015.json'), 'w'), indent=1)
print({k: (v['moved_vertices'], v['max_displacement_mm']) if isinstance(v, dict) and 'moved_vertices' in v else v for k, v in R.items()})
