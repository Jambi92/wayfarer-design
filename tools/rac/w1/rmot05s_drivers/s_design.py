# RM-OT-05S interface design: per half-plane column (0.25 deg) of the baseline mesh, explicit anchors and a designed
# no-garment profile, blended with the existing profile by an explicit weight w(theta):
#   ledge s_led(theta) : band lower ledge (faces facing down the arm axis, |n.d| > 0.55), 2-deg medians, smoothed
#   A(theta)           : profile point at s = s_led - 1.8 on the arm side (exposed arm skin; the 05Q seam-band level)
#   B(theta)           : first profile point after the ledge with s >= s_B(theta) (sector: 05Q s_hi + 1.8; anterior beyond
#                        the sector: s_hi(88) + 1.8); if the profile turns down first (posterior lip / fold-edge peak), B is
#                        2.5 cm of arclength beyond that peak on the trunk / fold side. A and B are smoothed along theta
#                        (Gaussian, sigma 3 deg) in 3-D and re-projected onto their columns.
#   D(theta, u)        : cubic Hermite curve A -> B in the half-plane, end tangents = the profile tangents at A and B,
#                        magnitudes = chord length (removes ledge, lip and curled fold edge; INFERRED)
#   P(theta, u)        : (1 - w) * S_AB(u) + w * D(u), u = normalized arclength; w: 0 at the region ends (= baseline
#                        surface, so both ends meet unchanged geometry), smoothstep to 1 inside (see ZONES)
# Writes columns.npz (theta, A/B arclength, design samples) and design plots. No mesh is modified here.
import argparse, json, os, sys, numpy as np, trimesh
from scipy.ndimage import gaussian_filter1d
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import s_lib
ZONES = dict(posterior=dict(core=-80.0, full_in=-88.0, full_out=-116.0, far=-136.0), anterior=dict(core=74.0, full_in=82.0, full_out=104.0, far=122.0))
def wfun(th, z):
    sgn = np.sign(z['far'] - z['core']); x = (th - z['core']) * sgn
    a = abs(z['full_in'] - z['core']); b = abs(z['full_out'] - z['core']); c = abs(z['far'] - z['core'])
    ss = lambda t: t * t * (3 - 2 * t)
    return np.where(x <= 0, 0, np.where(x < a, ss(np.clip(x / a, 0, 1)), np.where(x <= b, 1, np.where(x < c, ss(np.clip((c - x) / (c - b), 0, 1)), 0))))
def build(fr, V, F, fn, name, step=0.25, NU=64):
    z = ZONES[name]; th = np.arange(min(z['core'], z['far']), max(z['core'], z['far']) + 1e-6, step)
    t_, s_, r_ = fr.tsr(V[F].mean(1)); na = fn @ fr.d
    bins = np.arange(th.min() - 6, th.max() + 6.01, 2.0); led = []
    for b in bins:
        k = (t_ >= b) & (t_ < b + 2) & (na < -0.55) & (s_ > -1.5) & (s_ < 3.5) & (r_ < 15)
        led.append(np.median(s_[k]) if k.sum() >= 2 else np.nan)
    led = np.array(led); ok = ~np.isnan(led); led = gaussian_filter1d(np.interp(bins + 1, (bins + 1)[ok], led[ok]), 1.0); s_led = np.interp(th, bins + 1, led)
    sB_sector = np.interp(th, fr.lt, fr.shi) + 1.8; s_hi88 = np.interp(fr.tb, fr.lt, fr.shi) + 1.8
    cols = []; A3 = []; B3 = []
    for k, t in enumerate(th):
        P, fid = s_lib.profile(fr, V, F, t, (8.0, s_led[k] - 4.0)); L = s_lib.arclen(P)
        iA = np.argmax(P[:, 1] >= s_led[k] - 1.8); lA = np.interp(s_led[k] - 1.8, [P[iA - 1, 1], P[iA, 1]], [L[iA - 1], L[iA]])
        iL = np.argmax(P[:, 1] >= s_led[k]); in_sector = fr.ta <= t <= fr.tb
        sB = sB_sector[k] if in_sector else (99.0 if name == 'posterior' else s_hi88)
        lB = None; peak = None; smax = -1e9
        for i in range(iL, len(P)):
            if P[i, 1] > smax: smax = P[i, 1]; ip = i
            if P[i, 1] >= sB: lB = L[i - 1] + (sB - P[i - 1, 1]) / max(P[i, 1] - P[i - 1, 1], 1e-9) * (L[i] - L[i - 1]); break
            if smax - P[i, 1] > 0.3: peak = ip; break
        if lB is None: lB = L[peak] + 2.5 if peak is not None else L[-1]
        cols.append((P, L)); A3.append(fr.to3(t, *s_lib.at_len(P, L, lA)[0][::-1])[0]); B3.append(fr.to3(t, *s_lib.at_len(P, L, lB)[0][::-1])[0])
    A3 = gaussian_filter1d(np.array(A3), 3.0 / step, axis=0, mode='nearest'); B3 = gaussian_filter1d(np.array(B3), 3.0 / step, axis=0, mode='nearest')
    w = wfun(th, z); out = dict(theta=th, w=w, s_led=s_led, lA=[], lB=[], S=[], D=[], P=[])
    for k, t in enumerate(th):
        P, L = cols[k]; rad, _ = fr.dirs(t)
        qa = np.array([(A3[k] - fr.O) @ rad, (A3[k] - fr.O) @ fr.d]); qb = np.array([(B3[k] - fr.O) @ rad, (B3[k] - fr.O) @ fr.d])
        lA, _ = s_lib.project(P, L, qa); lB, _ = s_lib.project(P, L, qb)
        u = np.linspace(0, 1, NU); S_ab = s_lib.at_len(P, L, lA + u * (lB - lA))
        def tang(l):
            p0 = s_lib.at_len(P, L, l - 0.4)[0]; p1 = s_lib.at_len(P, L, l + 0.4)[0]; v = p1 - p0; return v / max(np.linalg.norm(v), 1e-9)
        pa, pb = S_ab[0], S_ab[-1]; ch = np.linalg.norm(pb - pa); ta_, tb_ = tang(lA) * ch, tang(lB) * ch
        h00 = 2 * u**3 - 3 * u**2 + 1; h10 = u**3 - 2 * u**2 + u; h01 = -2 * u**3 + 3 * u**2; h11 = u**3 - u**2
        D = h00[:, None] * pa + h10[:, None] * ta_ + h01[:, None] * pb + h11[:, None] * tb_
        # resample D by its own arclength so that u is normalized arclength on both curves
        Ld = s_lib.arclen(D); D = s_lib.at_len(D, Ld, u * Ld[-1])
        out['lA'].append(lA); out['lB'].append(lB); out['S'].append(S_ab); out['D'].append(D); out['P'].append((1 - w[k]) * S_ab + w[k] * D)
    for k_ in ('lA', 'lB', 'S', 'D', 'P'): out[k_] = np.array(out[k_])
    return out, cols
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--mesh'); ap.add_argument('--frame'); ap.add_argument('--out'); a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    fr = s_lib.Frame(a.frame); m = trimesh.load(a.mesh, process=False); V = np.asarray(m.vertices); F = np.asarray(m.faces)
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    for name in ('posterior', 'anterior'):
        o, cols = build(fr, V, F, m.face_normals, name)
        np.savez(os.path.join(a.out, 'design_%s.npz' % name), **{k: v for k, v in o.items()})
        pick = np.linspace(0, len(o['theta']) - 1, 12).astype(int); fig, ax = plt.subplots(2, 6, figsize=(21, 8))
        for j, k in enumerate(pick):
            A = ax[j // 6][j % 6]; P, L = cols[k]; A.plot(P[:, 0], P[:, 1], color='0.6', lw=2.5, label='baseline profile')
            A.plot(o['D'][k][:, 0], o['D'][k][:, 1], 'g--', lw=1, label='designed D (w=1)'); A.plot(o['P'][k][:, 0], o['P'][k][:, 1], 'b-', lw=1.2, label='target (w=%.2f)' % o['w'][k])
            A.plot(*o['S'][k][0], 'ko', ms=4); A.plot(*o['S'][k][-1], 'ks', ms=4)
            A.set_title('%s theta %.1f  w=%.2f' % (name, o['theta'][k], o['w'][k]), fontsize=8); A.set_aspect('equal'); A.set_xlim(2, 22); A.set_ylim(-6, 14); A.grid(alpha=.3); A.legend(fontsize=6)
        plt.tight_layout(); plt.savefig(os.path.join(a.out, 'design_%s_columns.png' % name), dpi=70); plt.close()
        print(name, 'columns', len(o['theta']), 'chord A-B cm', np.round([np.linalg.norm(o['S'][k][-1] - o['S'][k][0]) for k in pick], 2).tolist())
