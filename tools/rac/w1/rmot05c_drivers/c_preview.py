# RAC RM-OT-05C preview: race base-surface organization (race_base.organize) of a composition state on an existing 05B skeleton
# (-LEAN carries the accepted 05A / 05B architecture). Same arithmetic as skeleton_envelope.make(base=...). Search tool only.
# envelope(body_prefix, spec, out_id, comp=None): comp = donor composition id suffix (e.g. 'C000050') for a low-composition diagnostic.
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D); sys.path.insert(0, W1); sys.path.insert(0, W1 + '/rmot05_drivers')
import skeleton_envelope as SE, race_base as RB
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; PREV = S + '/rmot05c/prev'; os.makedirs(PREV, exist_ok=True)
DD = [S + '/w2c/donor', S + '/w2d/h', S + '/w1g/donor']
def find(n):
    for d in DD:
        if os.path.exists('%s/%s_r6.npz' % (d, n)): return d + '/' + n
    raise FileNotFoundError(n)
def envelope(body_prefix, spec, out_id, comp=None, st='r6'):
    B = np.load(body_prefix + '_%s.npz' % st, allow_pickle=True); meta = json.loads(str(B['meta']))
    L = dict(np.load(body_prefix + '-LEAN_%s.npz' % st, allow_pickle=True))
    dr, dl = meta['tissue_donor']
    if comp: dr = dr.split('-C')[0] + '-' + comp
    R = np.load(find(dr) + '_%s.npz' % st, allow_pickle=True); Dn = np.load(find(dl) + '_%s.npz' % st, allow_pickle=True)
    f, sc = SE.simil(Dn, R); tissue = R['V'].astype(float) - f(Dn['V'])
    J = json.loads(str(L['joints'])); Jf = {k: [f(a).tolist(), f(b).tolist()] for k, (a, b) in J.items()}
    V0 = f(L['V'].astype(float)) + tissue
    V, info = RB.organize(V0, L, Jf, spec, skel=f(L['V'].astype(float)))
    keep = L['keep'].astype(bool); V[:, 2] -= V[keep, 2].min()
    Bo = dict(B); Bo['V'] = V.astype(np.float32); np.savez_compressed('%s/%s_%s.npz' % (PREV, out_id, st), **Bo)
    info['stature'] = float(V[keep, 2].max())
    return info
