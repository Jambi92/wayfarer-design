# RAC RM-OT-05D: render the true skeletal floor next to the -LEAN skeleton surface and a body (search / Stage A visual). Usage: d_floorview.py TAG BODYPREFIX...
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D); sys.path.insert(0, W1); sys.path.insert(0, W1 + '/rmot05_drivers')
import true_envelope as TE, ot05r_package as PK
S = PK.S; OUT = S + '/rmot05d/floorview'; os.makedirs(OUT, exist_ok=True); PK.R = OUT + '/rend'; os.makedirs(PK.R, exist_ok=True); PK.SH = OUT
tag = sys.argv[1]; ids = []
for bp in sys.argv[2:]:
    nm = os.path.basename(bp); L = dict(np.load(bp + '-LEAN_r6.npz', allow_pickle=True))
    Fv, d, n = TE.floor(L['V'].astype(float), L)
    Lo = dict(L); Lo['V'] = Fv.astype(np.float32); np.savez_compressed(OUT + '/%s-FLOOR_r6.npz' % nm, **Lo)
    for k, p, lab in ((nm + 'L', bp + '-LEAN', nm + ' -LEAN (old guard)'), (nm + 'F', OUT + '/%s-FLOOR' % nm, nm + ' true floor'), (nm, bp, nm + ' body')):
        PK.BODIES[k] = (p, lab); ids.append(k)
        for v in PK.VIEWS:
            q = '%s/%s_nh_%s.png' % (PK.R, k, v[0])
            if os.path.exists(q): os.remove(q)
for v in ('F', 'P', 'RQ'): PK.row_sheet('fv_%s_%s.jpg' % (tag, v), 'RM-OT-05D floor view %s %s' % (tag, v), '', ids, v, headless=True)
