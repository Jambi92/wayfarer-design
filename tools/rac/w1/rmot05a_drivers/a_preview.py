# RAC RM-OT-05A quick preview: arch sculpt displacement computed on the skeleton (-LEAN) R-6 surface and carried onto the reference-composition
# body (ref + disp; skeleton_envelope.make's lean->ref similarity is ~1, so this equals the full route to < 0.1 cm). Search tool only.
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D); sys.path.insert(0, W1); sys.path.insert(0, D)
sys.path.insert(0, W1 + '/rmot05_drivers')
import arch_sculpt as AS, ot05r_package as PK
S = PK.S; OUT = S + '/rmot05a/prev'; os.makedirs(OUT, exist_ok=True)
def make(src, arch, out_id):
    """src = prefix of the reference body (…/GR218R/GR218R); writes OUT/out_id_r6.npz"""
    L = dict(np.load(src + '-LEAN_r6.npz', allow_pickle=True)); R = dict(np.load(src + '_r6.npz', allow_pickle=True))
    V2, J2 = AS.apply(L['V'], L, arch); disp = V2 - L['V']
    R['V'] = (R['V'] + disp).astype(np.float32); z0 = R['V'][R['keep'].astype(bool), 2].min(); R['V'][:, 2] -= z0
    np.savez_compressed(OUT + '/%s_r6.npz' % out_id, **R); PK.BODIES[out_id] = (OUT + '/' + out_id, out_id)
    for t in ('', '_nh'):
        for v in PK.VIEWS:
            p = '%s/%s%s_%s.png' % (PK.R, out_id, t, v[0])
            if os.path.exists(p): os.remove(p)
    return float(np.abs(disp).max())
