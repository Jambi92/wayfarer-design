# hv_root_sectors.py BRANCH.npz HEAD [OUT.json] : Halvren root visual-integration order §5 diagnosis / secondary-silhouette measures, per sector around the
# junction centroid (posterior / superior / anterior / inferior, root frame), both sides: height of the junction ring J and of the cuff band above the
# hidden-ear skull; PEDESTAL = height of the root (cuff + transition + root loop) above the head surface extrapolated over the ear zone from the skin 3+ rings
# outside the v005 loop (thin-plate, smoothing 10 -- as HR2); LOOP CREASE = dihedral across the root-loop edges (a crease draws the loop as a second contour);
# inferior fork (lowest free-lobe point vs the lowest raised cuff point below the attachment).
import sys, os, json, numpy as np
os.environ.setdefault('EAR_TOPO', 'v002'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_domains as D
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001'); import ear_branch_lib as E
Lo = E.canonical_layout(); J = np.asarray(Lo['J']); ns = len(Lo['st'])
_HT = {}
def head_true(H, sd):                     # head surface extrapolated from the skin 2 rings beyond the v005 ear zone (family realization), thin-plate, <= 5 cm
    if (H, sd) not in _HT:
        from scipy.interpolate import RBFInterpolator
        fz = np.load('%s/fam/%s_fam.npz' % (D.CF, H)); V0 = fz['V'].astype(float); Q0 = np.asarray(fz['Q']); rd = D.frame(H, sd); zone = set(np.unique(Q0[rd['faces']]).tolist())
        adj = {}
        for q in Q0:
            for k in range(4): adj.setdefault(int(q[k]), set()).update((int(q[(k + 1) % 4]), int(q[(k - 1) % 4])))
        r1 = {w for v in rd['loop'] for w in adj[int(v)] if w not in zone}; r2 = {w for v in r1 for w in adj[v] if w not in zone and w not in r1}
        d0 = V0 - rd['O']; sg = 1 if sd == 'l' else -1; cand = np.nonzero((np.linalg.norm(d0, axis=1) < 5.0) & (sg * V0[:, 0] > 0) & ((d0 @ rd['n']) > -2.5))[0]
        out = np.array([v for v in cand if v not in zone and v not in r1 and v not in r2]); bu = lambda X: np.c_[(X - rd['O']) @ rd['b'], (X - rd['O']) @ rd['u']]
        f = RBFInterpolator(bu(V0[out]), (V0[out] - rd['O']) @ rd['n'], kernel='thin_plate_spline', smoothing=10.0); _HT[(H, sd)] = lambda X: (X - rd['O']) @ rd['n'] - f(bu(X))
    return _HT[(H, sd)]
def sectors(p, H):
    z = np.load(p); rec = json.load(open(p.replace('.npz', '.json'))); V = z['V']; part = z['part']; side = z['side']; out = {}
    for sd in ('l', 'r'):
        fr = rec['sides'][sd]['frame']; O, n, b, u = [np.array(fr[q]) for q in 'Onbu']; sk = D.frame(H, sd)['skull']; f0 = np.nonzero(side == sd)[0][0]
        bu = lambda X: np.c_[(X - O) @ b, (X - O) @ u]; hgt = lambda X: (X - O) @ n - sk(bu(X))
        Jx = V[f0 + J]; c = bu(Jx).mean(0); cv = np.nonzero((part == 'cuff') & (side == sd))[0]; hc = hgt(V[cv]); hj = hgt(Jx)
        ang = lambda X: (lambda a: np.where(a < -135, a + 360, a))(np.degrees(np.arctan2(*(bu(X) - c).T[::-1])))
        aj, ac = ang(Jx), ang(V[cv]); r = {}
        for lo, hi, nm in ((-45, 45, 'posterior'), (45, 135, 'superior'), (135, 225, 'anterior'), (-135, -45, 'inferior')):
            mj = (aj >= lo) & (aj < hi); mc = (ac >= lo) & (ac < hi)
            r[nm] = dict(junction_mean_cm=round(float(hj[mj].mean()), 3), junction_max_cm=round(float(hj[mj].max()), 3), cuff_mean_cm=round(float(hc[mc].mean()), 3),
                         cuff_p90_cm=round(float(np.percentile(hc[mc], 90)), 3), cuff_max_cm=round(float(hc[mc].max()), 3))
        # inferior fork: below the lowest junction point, the free lobe (sheet) and the cuff tab each reach down; fork = vertical gap of their lowest points and
        # the lateral 'notch' depth between them (height above skull of the shallowest point on the segment joining them in side view)
        X = V[f0:f0 + ns]; sh = np.isin(Lo['part'][:ns], ['front', 'back', 'rim']); Us = bu(X[sh])[:, 1]; Uc = bu(V[cv])[:, 1]
        lob = X[sh][np.argmin(Us)]; tab = V[cv][np.argmin(np.where(hc > 0.15, Uc, 1e9))] if (hc > 0.15).any() else None
        ht = head_true(H, sd); rootv = np.nonzero((side == sd) & np.isin(part, ['cuff', 'transition']))[0]; lp = z['v005_to_branch'][np.array(rec['sides'][sd]['root_loop_v005'])]
        rv = np.r_[rootv, lp]; hp = ht(V[rv]); ar = ang(V[rv])
        r['pedestal_vs_true_head'] = {nm: dict(p90_cm=round(float(np.percentile(hp[(ar >= lo) & (ar < hi)], 90)), 3), max_cm=round(float(hp[(ar >= lo) & (ar < hi)].max()), 3))
                                      for lo, hi, nm in ((-45, 45, 'posterior'), (45, 135, 'superior'), (135, 225, 'anterior'), (-135, -45, 'inferior'))}
        Q = np.asarray(z['Q']); L = set(lp.tolist()); nr = np.linalg.norm(V - O, axis=1) < 5; F = np.nonzero(nr[Q].all(1))[0]
        fn = np.cross(V[Q[F, 2]] - V[Q[F, 0]], V[Q[F, 3]] - V[Q[F, 1]]); fn /= np.linalg.norm(fn, axis=1)[:, None]; ed = {}
        for i, f_ in enumerate(F):
            for k in range(4):
                e = tuple(sorted((int(Q[f_][k]), int(Q[f_][(k + 1) % 4]))))
                if e[0] in L and e[1] in L: ed.setdefault(e, []).append(i)
        ea = np.array([ang(((V[e[0]] + V[e[1]]) / 2)[None])[0] for e, fs in ed.items() if len(fs) == 2]); ed_ = np.array([np.degrees(np.arccos(np.clip(fn[fs[0]] @ fn[fs[1]], -1, 1))) for e, fs in ed.items() if len(fs) == 2])
        r['loop_crease_deg'] = {nm: dict(mean=round(float(ed_[(ea >= lo) & (ea < hi)].mean()), 1), max=round(float(ed_[(ea >= lo) & (ea < hi)].max()), 1))
                                for lo, hi, nm in ((-45, 45, 'posterior'), (45, 135, 'superior'), (135, 225, 'anterior'), (-135, -45, 'inferior'))}
        r['inferior_fork'] = dict(lobe_low_cm=round(float(Us.min()), 3), raised_cuff_low_cm=(round(float(bu(tab[None])[0, 1]), 3) if tab is not None else None),
                                  raised_cuff_tab_height_cm=(round(float(hgt(tab[None])[0]), 3) if tab is not None else None))
        out[sd] = r
    return out
if __name__ == '__main__':
    R = sectors(sys.argv[1], sys.argv[2]); print(json.dumps({sd: {k: v for k, v in R[sd].items()} for sd in R}, indent=0)[:1600])
    if len(sys.argv) > 3: json.dump(R, open(sys.argv[3], 'w'), indent=1)
