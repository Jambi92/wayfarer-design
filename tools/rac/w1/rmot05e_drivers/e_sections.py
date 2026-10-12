# RAC RM-OT-05E section / load-path evidence (order §6.11): shows that the 05E change is organization, not added circumference.
#  1. limb radius profiles along each accepted bone axis (mean section radius vs t, both sides averaged) for thigh / shank / upper arm /
#     forearm: Skarn, Grask E3, Gorrund E1 baseline and the 05E candidates, plus the taper index r(distal 0.85) / r(proximal 0.30) and the
#     segment volume ratio vs E1 (equal-length bins: sum r^2).
#  2. exact plane sections (horizontal) at mid-shank, supramalleolar, mid-forearm, distal forearm, lumbar (S4) and sacral levels.
#  3. posterior sagittal profile (x = 0 slice, posterior half) from scapula to knee.
# Usage: python3 e_sections.py NAME...   (writes S/rmot05e/sections/*)
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D); sys.path.insert(0, W1); sys.path.insert(0, W1 + '/rmot05c_drivers'); sys.path.insert(0, W1 + '/rmot05d_drivers')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import c_guard as CG, race_base as RB
from d_stageA import section
S = CG.S; OUT = S + '/rmot05e/sections'; os.makedirs(OUT, exist_ok=True)
BONE = {'thigh': 'thigh', 'shank': 'calf', 'upperarm': 'upperarm', 'forearm': 'lowerarm'}
def load(n):
    try: p = CG.path(n)
    except FileNotFoundError:
        import e_package as EP; p = EP.B[n][0]           # controls (Skarn) from the package body table
    B = np.load(p + '_r6.npz', allow_pickle=True); return B, B['V'].astype(float), json.loads(str(B['joints']))
def profile(B, V, J, seg, nt=18):
    out = []
    for sd in ('l', 'r'):
        bn = BONE[seg]; w = B['w_%s_%s' % (bn, sd)].astype(float) * B['keep']; m = w > 0.5
        h, ax, ln, ea, el = RB._frame(J, bn, sd); t, tc, r, u, ph = RB._coords(V[m], h, ax, ln, ea, el)
        it = np.clip((t * nt).astype(int), 0, nt - 1); ok = (t >= 0) & (t <= 1)
        prof = np.array([np.sqrt(np.mean(r[ok & (it == i)] ** 2)) if (ok & (it == i)).sum() >= 3 else np.nan for i in range(nt)])   # rms section radius
        out.append(prof)
    p = np.nanmean(np.stack(out), 0); tg = (np.arange(nt) + 0.5) / nt
    return tg, p
COLS = ['#9e9e9e', '#6a3d9a', '#e08214', '#1b9e77', '#d95f02', '#1f78b4', '#e7298a']
if __name__ == '__main__':
    names = sys.argv[1:]; L = {n: load(n) for n in names}; base = 'GO5DE1'
    res = {}
    fig, axs = plt.subplots(1, 4, figsize=(20, 5.2))
    for ax, seg in zip(axs, ('thigh', 'shank', 'upperarm', 'forearm')):
        for k, n in enumerate(names):
            tg, p = profile(*L[n], seg); ax.plot(tg, p, color=COLS[k % len(COLS)], lw=2.2 if n.startswith('GO5E') else 1.4, ls='-' if n.startswith('GO') else '--', label=n)
            ok = ~np.isnan(p); pi = lambda t: float(np.interp(t, tg[ok], p[ok]))
            res.setdefault(n, {})[seg] = {'r_prox_0.30_cm': round(pi(0.3), 2), 'r_dist_0.85_cm': round(pi(0.85), 2), 'taper_index_dist_over_prox': round(pi(0.85) / pi(0.3), 3),
                                          'mean_r2_0.1_0.9': float(np.nanmean(p[(tg > 0.1) & (tg < 0.9)] ** 2))}
        ax.set_title('%s: rms section radius about the accepted bone axis' % seg, fontsize=10); ax.set_xlabel('t along bone (0 = proximal joint, 1 = distal joint)'); ax.set_ylabel('cm'); ax.grid(alpha=0.3)
    axs[0].legend(fontsize=8); fig.suptitle('RM-OT-05E limb section profiles: 05E redistributes the same segment tissue toward constant-section load columns with periarticular collars (no taper), not more circumference', fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.93]); fig.savefig(OUT + '/e_limb_profiles.png', dpi=105); plt.close(fig)
    for n in names:
        for seg in res[n]: res[n][seg]['segment_r2_vs_E1'] = round(res[n][seg]['mean_r2_0.1_0.9'] / res[base][seg]['mean_r2_0.1_0.9'], 3) if base in res else None
    # horizontal sections at skeleton-anchored heights of the baseline (same skeleton -> same joint heights for all Gorrund bodies)
    Bb, Vb, Jb = L[base]
    knee = Jb['calf_l'][0][2]; ank = Jb['foot_l'][0][2]; elb = Jb['lowerarm_l'][0]; wr = Jb['hand_l'][0]; hip = 0.5 * (Jb['thigh_l'][0][2] + Jb['thigh_r'][0][2]); sst = Jb['clavicle_l'][0][2]
    cuts = [('mid-shank', 0.5 * (knee + ank), Jb['calf_l'][0]), ('supramalleolar', ank + 0.12 * (knee - ank), Jb['calf_l'][0]),
            ('mid-forearm', 0.5 * (elb[2] + wr[2]), elb), ('distal forearm', wr[2] + 0.12 * (elb[2] - wr[2]), elb),
            ('lumbar (r 0.35)', hip + 0.35 * (sst - hip), None), ('sacral (r 0.05)', hip + 0.05 * (sst - hip), None)]
    gon = [n for n in names if n.startswith('GO')]
    fig, axs = plt.subplots(1, len(cuts), figsize=(4.0 * len(cuts), 4.6))
    for ax, (lab, z, c) in zip(axs, cuts):
        for k, n in enumerate(gon):
            B, V, J = L[n]; keep = B['keep'].astype(bool)
            if c is not None:                               # limb cut: only the left limb, centred on that limb's axis at height z
                sel = keep & (V[:, 0] * np.sign(c[0]) > 0)
                if 'arm' in lab or 'forearm' in lab: sel &= np.maximum(B['w_lowerarm_l'], B['w_lowerarm_r']) > 0.3
                else: sel &= np.maximum(B['w_calf_l'], B['w_calf_r']) > 0.3
            else: sel = keep & (np.maximum.reduce([B['w_' + a] for a in ('upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r')]) < 0.05)
            sg = section(V, B['F'], sel, 2, z)
            for s_ in sg: ax.plot(s_[:, 0], s_[:, 1], color=COLS[(names.index(n)) % len(COLS)], lw=2.0 if n.startswith('GO5E') else 1.2)
        ax.set_aspect('equal'); ax.set_title('%s (z = %.0f)' % (lab, z), fontsize=10); ax.grid(alpha=0.3)
    hs = [plt.Line2D([], [], color=COLS[names.index(n) % len(COLS)]) for n in gon]; fig.legend(hs, gon, loc='lower center', ncol=len(gon), fontsize=9)
    fig.suptitle('RM-OT-05E exact horizontal sections at skeleton-anchored heights (Gorrund E1 baseline vs 05E candidates)', fontsize=11); fig.tight_layout(rect=[0, 0.07, 1, 0.92])
    fig.savefig(OUT + '/e_sections.png', dpi=105); plt.close(fig)
    # posterior sagittal profile
    fig, ax = plt.subplots(figsize=(6.5, 9))
    for n in names:
        B, V, J = L[n]; keep = B['keep'].astype(bool); h0 = 0.5 * (J['thigh_l'][0][2] + J['thigh_r'][0][2])
        xs = 0.0 if not n.startswith('SK') else 0.0
        for xoff, ls in ((0.0, '-'), (9.0 * np.sign(J['thigh_l'][0][0]), ':')):
            sg = section(V, B['F'], keep, 0, xoff)
            cy = np.median(V[keep & (np.abs(V[:, 2] - h0) < 2), 1])
            pts = np.concatenate([s_ for s_ in sg]) if len(sg) else np.zeros((0, 3))
            post = pts[pts[:, 1] < cy]
            zz = np.arange(h0 - 45, h0 + 75, 1.0); yy = [post[np.abs(post[:, 2] - z) < 0.6, 1].min() if (np.abs(post[:, 2] - z) < 0.6).any() else np.nan for z in zz]
            ax.plot(np.array(yy) - cy, zz - h0, color=COLS[names.index(n) % len(COLS)], ls=ls, lw=2 if n.startswith('GO5E') else 1.2, label=n + (' (midline)' if xoff == 0 else ' (x = 9 cm)'))
    ax.set_xlabel('posterior surface y relative to hip-level section centre (cm)'); ax.set_ylabel('height relative to hip joint (cm)'); ax.grid(alpha=0.3); ax.legend(fontsize=7)
    ax.set_title('RM-OT-05E posterior load path: sagittal posterior profile (scapula -> sacrum -> hamstring)', fontsize=10)
    fig.tight_layout(); fig.savefig(OUT + '/e_posterior_profile.png', dpi=105); plt.close(fig)
    json.dump(res, open(OUT + '/e_limb_profiles.json', 'w'), indent=1); print(json.dumps({n: {s: v['taper_index_dist_over_prox'] for s, v in r.items()} for n, r in res.items()}))
