# RAC RM-OT-05B preview: recompute a body's composition envelope exactly as skeleton_envelope.make does (sculpted -LEAN skeleton + aligned
# donor tissue field), with the race-surface remap applied to the tissue field. Search tool; writes PREV/<id>_r6.npz.
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D); sys.path.insert(0, W1); sys.path.insert(0, W1 + '/rmot05_drivers')
import skeleton_envelope as SE, race_surface as RS
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; PREV = S + '/rmot05b/prev'; os.makedirs(PREV, exist_ok=True)
DD = [S + '/w2c/donor', S + '/w2d/h', S + '/w1g/donor']
def find(n):
    for d in DD:
        if os.path.exists('%s/%s_r6.npz' % (d, n)): return d + '/' + n
    raise FileNotFoundError(n)
def envelope(body_prefix, spec, out_id, st='r6', donor=None):
    """body_prefix = .../GRA218/GRA218 ; donor = (ref_prefix, lean_prefix) or from the body meta"""
    B = np.load(body_prefix + '_%s.npz' % st, allow_pickle=True); meta = json.loads(str(B['meta']))
    L = dict(np.load(body_prefix + '-LEAN_%s.npz' % st, allow_pickle=True))
    dr, dl = donor or [find(x) for x in meta['tissue_donor']]
    R = np.load(dr + '_%s.npz' % st, allow_pickle=True); Dn = np.load(dl + '_%s.npz' % st, allow_pickle=True)
    f, sc = SE.simil(Dn, R); tissue = R['V'].astype(float) - f(Dn['V']); Vs = L['V'].astype(float); Vf = f(Vs)
    J = json.loads(str(L['joints'])); Jf = {k: [f(a).tolist(), f(b).tolist()] for k, (a, b) in J.items()}
    T2, info = RS.apply(Vf, tissue, L, Jf, spec)
    V = Vf + T2; keep = L['keep'].astype(bool); V[:, 2] -= V[keep, 2].min()
    Bo = dict(B); Bo['V'] = V.astype(np.float32); np.savez_compressed('%s/%s_%s.npz' % (PREV, out_id, st), **Bo)
    V0 = Vf + tissue; V0[:, 2] -= V0[keep, 2].min()
    return {"repro_err_cm": float(np.abs(V0 - B['V']).max()), "max_change_cm": float(np.linalg.norm(V - V0, axis=1).max()), "info": info}
