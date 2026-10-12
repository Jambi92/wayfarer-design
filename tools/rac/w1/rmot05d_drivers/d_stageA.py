# RAC RM-OT-05D Stage A (order §10): the true skeletal envelope versus the old -LEAN guard, with the 05D race surface.
# Section strips (exact plane sections of the meshes, matched frame) of:
#   - Grask shoulder and Grask pelvis / gluteal region;
#   - Gorrund shoulder / thorax and Gorrund pelvis / gluteal region.
# Each strip shows: old -LEAN (MPFB minimum-body) boundary, new true skeletal floor, 05C developmental baseline, 05D race surface.
# Horizontal sections at skeleton-anchored heights (shoulder joint, thorax S2 level, hip joint, gluteal level) and sagittal / coronal
# sections through the shoulder and the gluteal mass. Also writes the allowed-movement table: how far 05D may move inside the old donor
# surface while staying outside the protected floor (per region: floor depth below -LEAN, cm).
# Usage: python3 d_stageA.py GRBODY GOBODY   (05D reference bodies, e.g. GR5DE2 GO5DE2)
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D); sys.path.insert(0, W1); sys.path.insert(0, W1 + '/rmot05c_drivers')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import true_envelope as TE, c_guard as CG
S = CG.S; OUT = S + '/rmot05d/stageA'; os.makedirs(OUT, exist_ok=True)
def section(V, F, keep, axis, val):
    Fk = F[keep[F].all(1)]; segs = []
    A, B, C = V[Fk[:, 0]], V[Fk[:, 1]], V[Fk[:, 2]]; pts = []
    for a, b in ((A, B), (B, C), (C, A)):
        m = (a[:, axis] - val) * (b[:, axis] - val) < 0; t = (val - a[m, axis]) / (b[m, axis] - a[m, axis]); pts.append(a[m] + (b[m] - a[m]) * t[:, None])
    # pair the two crossing points of each face
    da = (A[:, axis] - val) * (B[:, axis] - val) < 0; db = (B[:, axis] - val) * (C[:, axis] - val) < 0; dc = (C[:, axis] - val) * (A[:, axis] - val) < 0
    def cut(a, b): t = (val - a[:, axis]) / (b[:, axis] - a[:, axis]); return a + (b - a) * t[:, None]
    out = []
    for m1, m2, (a1, b1), (a2, b2) in ((da & db, None, (A, B), (B, C)), (db & dc, None, (B, C), (C, A)), (dc & da, None, (C, A), (A, B))):
        if m1.any(): out.append(np.stack([cut(a1[m1], b1[m1]), cut(a2[m1], b2[m1])], 1))
    return np.concatenate(out) if out else np.zeros((0, 2, 3))
def load_pair(n):
    p = CG.path(n); B = np.load(p + '_r6.npz', allow_pickle=True); meta = json.loads(str(B['meta']))
    L = dict(np.load(CG.path(meta['skeleton'].replace('-LEAN', '')) + '-LEAN_r6.npz', allow_pickle=True))
    J = json.loads(str(B['joints'])); JL = json.loads(str(L['joints']))
    a = np.array([JL[k][0] for k in JL]); b = np.array([J[k][0] for k in JL]); sc = np.sqrt(((b - b.mean(0)) ** 2).sum() / ((a - a.mean(0)) ** 2).sum())
    to_b = lambda X: (X - a.mean(0)) * sc + b.mean(0)
    Fv = TE.floor(L['V'].astype(float), L)[0]
    return B, to_b(L['V'].astype(float)), to_b(Fv), J
COL = {'old -LEAN guard (MPFB minimum body)': ('#d62728', '--'), 'true skeletal floor (05D)': ('#1f77b4', '-'), '05C baseline': ('#999999', ':'), '05D race surface': ('#111111', '-')}
def strip(race, n05d, n05c, cuts, fn, title):
    B, Lb, Fb, J = load_pair(n05d); B0 = np.load(CG.path(n05c) + '_r6.npz', allow_pickle=True)
    F = B['F']; keep = B['keep'].astype(bool)
    meshes = [('old -LEAN guard (MPFB minimum body)', Lb), ('true skeletal floor (05D)', Fb), ('05C baseline', B0['V'].astype(float)), ('05D race surface', B['V'].astype(float))]
    fig, axs = plt.subplots(1, len(cuts), figsize=(5.2 * len(cuts), 6.2))
    for ax, (lab, axis, val, xr, yr) in zip(np.atleast_1d(axs), cuts):
        other = [i for i in range(3) if i != axis]
        for name, V in meshes:
            sg = section(V, F, keep, axis, val); c, ls = COL[name]
            for s_ in sg: ax.plot(s_[:, other[0]], s_[:, other[1]], color=c, ls=ls, lw=1.6 if name == '05D race surface' else 1.2)
        ax.set_title(lab, fontsize=10); ax.set_aspect('equal'); ax.set_xlim(*xr); ax.set_ylim(*yr); ax.grid(alpha=0.25)
        ax.set_xlabel('xyz'[other[0]] + ' (cm)'); ax.set_ylabel('xyz'[other[1]] + ' (cm)')
    hs = [plt.Line2D([], [], color=c, ls=ls) for c, ls in COL.values()]; fig.legend(hs, list(COL), loc='lower center', ncol=4, fontsize=9)
    fig.suptitle(title, fontsize=12); fig.tight_layout(rect=[0, 0.06, 1, 0.95]); fig.savefig(OUT + '/' + fn, dpi=110); plt.close(fig)
def allowed(n):
    B, Lb, Fb, J = load_pair(n); keep = B['keep'].astype(bool); n_ = TE.outward_normals(Lb, B['F'], keep)
    d = np.einsum('ij,ij->i', Lb - Fb, n_); V = B['V'].astype(float); s = np.einsum('ij,ij->i', V - Lb, n_)
    W = {k: B['w_' + k] for k in B.files if False}
    regions = {'gluteal (pelvis, posterior)': (B['w_pelvis'] > 0.5) & (V[:, 1] < np.median(V[keep, 1]) - 3),
               'deltoid cap (upper arm, t < 0.3)': (np.maximum(B['w_upperarm_l'], B['w_upperarm_r']) > 0.5) & (V[:, 2] > J['upperarm_l'][0][2] - 12),
               'pectoral / chest front': (B['w_spine_03'] > 0.5) & (V[:, 1] > np.median(V[keep, 1]) + 3),
               'lumbar / abdomen (spine_01)': (B['w_spine_01'] > 0.5),
               'thigh shaft': (np.maximum(B['w_thigh_l'], B['w_thigh_r']) > 0.8), 'shank shaft': (np.maximum(B['w_calf_l'], B['w_calf_r']) > 0.8),
               'knee / ankle / elbow / wrist zones (held)': (np.maximum.reduce([B['w_foot_l'], B['w_foot_r'], B['w_hand_l'], B['w_hand_r']]) > 0.5)}
    out = {}
    for k, m in regions.items():
        m = m & keep
        out[k] = {'floor_depth_below_old_guard_cm_median': round(float(np.median(d[m])), 2), 'p90': round(float(np.percentile(d[m], 90)), 2),
                  '05D_surface_relative_to_old_guard_cm_min': round(float(s[m].min()), 2), '05D_vertices_inside_old_guard': int((s[m] < -0.2).sum()), 'n': int(m.sum())}
    return out
if __name__ == '__main__':
    gr, go = sys.argv[1], sys.argv[2]; gr0, go0 = 'GR5CC', 'GO5CB'
    for race, n, n0 in (('GR', gr, gr0), ('GO', go, go0)):
        B, Lb, Fb, J = load_pair(n); sh = J['upperarm_l'][0]; hip = 0.5 * (J['thigh_l'][0][2] + J['thigh_r'][0][2]); sx = np.sign(sh[0])
        shoulder = [('horizontal at shoulder joint (z = %.0f)' % (sh[2] - 2), 2, sh[2] - 2, (-35, 35), (-25, 25)),
                    ('coronal through shoulder joint (y = %.0f)' % sh[1], 1, sh[1], (-10 * sx + 0, 40 * sx) if sx > 0 else (-40, 10), (sh[2] - 35, sh[2] + 15)),
                    ('horizontal thorax (z = %.0f)' % (hip + 0.75 * (sh[2] - hip)), 2, hip + 0.75 * (sh[2] - hip), (-35, 35), (-25, 25))]
        pelvis = [('horizontal at hip joint (z = %.0f)' % hip, 2, hip, (-35, 35), (-25, 25)),
                  ('horizontal gluteal (z = %.0f)' % (hip - 6), 2, hip - 6, (-35, 35), (-25, 25)),
                  ('sagittal through gluteal mass (x = %.0f)' % (8 * sx), 0, 8 * sx, (-30, 30), (hip - 35, hip + 30))]
        strip(race, n, n0, shoulder, 'stageA_%s_shoulder.png' % race, 'RM-OT-05D Stage A - %s shoulder / thorax (%s): old -LEAN guard vs true floor vs race surface' % (race, n))
        strip(race, n, n0, pelvis, 'stageA_%s_pelvis.png' % race, 'RM-OT-05D Stage A - %s pelvis / gluteal (%s): old -LEAN guard vs true floor vs race surface' % (race, n))
        json.dump(allowed(n), open(OUT + '/stageA_%s_allowed.json' % race, 'w'), indent=1); print(race, 'done', flush=True)
