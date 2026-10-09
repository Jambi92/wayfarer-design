# RAC W2I1 D4 (closure order §7-§9): bounded NEUTRAL-RESTING-CARRIAGE diagnostic for SAU-SILHOUETTE.
# Lever: the accepted carriage parameter only (vary.warp 'tail_curv', deg; negative = lift). It rotates the free-tail centreline segments
# DISTAL to the caudal-base landmark (S_ROOT) with the angle growing toward the tip, so the caudal base, root integration, tail length, section
# shape (base breadth / depth, taper, mass) and every non-tail vertex are untouched by construction (verified below). Tested 0 / +4 / +8 / +12 deg
# upward (+8 = the validated §256.8 lift limit; +12 lies OUTSIDE the validated +8 lift ... +10 droop range and is reported as such).
# Per state: front thigh-gap visible extent / covered share / width profile (sa_silhouette rule), lowest free-tail point vs crotch and ground,
# distal-tail elevation ("raised flag" check), root-zone tangent continuity, invariance of root / length / sections / body, static lean change.
# Usage: python3 sa_carriage.py OUT.json [RENDER]
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_build as B, sa_silhouette as SIL
C = B.C; L = B.L; H0 = B.H0; Mx = B.Mx; vary = C.vary
CURVS = [0.0, -4.0, -8.0, -12.0]
CASES = [("SA-M188", {}, H0), ("SA-F188", B.CEN, H0), ("SA-M168", {}, 168.0), ("SA-M208", {}, 208.0), ("SA-M188-T78", B.tail(78, 1.15), H0), ("SA-M188-T55", B.tail(55, 0.85), H0)]
TAILK = ('tail_len', 'tail_len_pct', 'tail_root_area', 'tail_vol_L', 'tail_RSI_raw', 'tail_taper_raw', 'tail_A50', 'tail_A25', 'tail_A75', 'tail_mass_share', 'height')
def front_profile(P):
    """visible tail width per 1-cm level inside the thigh gap (front orthographic), top -> bottom"""
    x, f, u = P.T; tail = L.tail > 0.5; body = (L.tail < 0.2) & (L.arm < 0.2)
    near = body & (np.abs(x) < 3.0) & (u < 0.6 * u.max()) & (u > 0.25 * u.max()); cr = u[near].min(); prof = []
    for lev in np.arange(np.floor(cr) - 1, 0, -1.0):
        m = body & (np.abs(u - lev) < 0.5); xl = x[m & (x > 0)]; xr = x[m & (x < 0)]
        if len(xl) < 5 or len(xr) < 5: continue
        gl, gr = xl.min(), xr.max()
        if gl <= gr: continue
        t = tail & (np.abs(u - lev) < 0.5) & (x < gl) & (x > gr)
        w = max(min(x[t].max(), gl) - max(x[t].min(), gr), 0.0) if t.any() else 0.0
        prof.append((float(lev), float(w), float(gl - gr)))
    return float(cr), prof
def tail_geom(P, q):
    C2 = q['_C2']; kr = int(vary.S_ROOT * 2); free = C2[:kr]                       # free tail: indices below the root (toward the tip)
    T = np.gradient(C2, axis=0); T /= np.linalg.norm(T, axis=1)[:, None]
    i1, i2 = kr, max(kr - 20, 1)                                                     # root tangent vs 10 cm distal (0.5 cm spacing)
    kink = float(np.degrees(np.arccos(np.clip(T[i1] @ T[i2], -1, 1))))
    d = free[0] - free[min(40, len(free) - 1)]                                       # distal 20 cm of the centreline (tip end)
    elev = float(np.degrees(np.arctan2(d[2], -d[1])))                               # + = tip rising above horizontal going backward
    tv = L.tail > 0.5
    return dict(root_point=C2[kr].tolist(), tip_u=float(free[0, 2]), centreline_min_u=float(free[:, 2].min()), lowest_tail_vertex_u=float(P[tv, 2].min()),
                root_tangent_change_10cm_deg=kink, distal20_elevation_deg=elev, tip_f=float(free[0, 1]))
if __name__ == '__main__':
    out = {}; save = len(sys.argv) > 2
    for cid, p, h in CASES:
        base = None
        for cv in CURVS:
            pp = Mx(p, {'tail_curv': cv}) if cv else dict(p); P, q = C.build(pp); P2, q2, k = B.at_stature(P, q, h); M = B.measure(P2, q2, k)
            sil = SIL.front_tail(P2); cr, prof = front_profile(P2); tg = tail_geom(P2, q2); vis = [w for lev, w, g in prof if w > 0]
            r = dict(carriage_lift_deg=-cv, silhouette=sil, width_profile=prof, max_visible_width_cm=max(vis) if vis else 0.0, visible_levels=len(vis),
                     first_visible_below_crotch_cm=(cr - next(lev for lev, w, g in prof if w > 0)) if vis else None, tail=tg, lean=M['lean_scaled_deg'],
                     tail_readings={kk: M[kk] for kk in TAILK}, tail_min_u=M['tail_min_u'], reach_behind_heel=M['tail_reach_behind_heel'])
            nt = (L.tail < 1e-6)
            if base is None: base = dict(P=P2, M=M, r=r)
            else:
                r['nontail_vertices_max_shift_cm'] = float(np.abs(P2[nt] - base['P'][nt]).max())
                r['root_point_shift_cm'] = float(np.linalg.norm(np.array(tg['root_point']) - np.array(base['r']['tail']['root_point'])))
                r['tail_readings_delta_pct'] = {kk: 100 * (M[kk] / base['M'][kk] - 1) for kk in TAILK}
                r['dlean_vs_0deg'] = M['lean_scaled_deg'] - base['M']['lean_scaled_deg']
            out['%s|lift%+d' % (cid, -cv)] = r
            print(cid, 'lift %+d' % -cv, 'vis %.1f cm share %.4f maxw %.1f' % (sil['visible_extent_cm'], sil['covered_share'] or 0, r['max_visible_width_cm']),
                  'lowest tail %.1f crotch %.1f tip %.1f elev %.1f kink %.2f' % (tg['lowest_tail_vertex_u'], cr, tg['tip_u'], tg['distal20_elevation_deg'], tg['root_tangent_change_10cm_deg']),
                  'dlean %.2f' % r.get('dlean_vs_0deg', 0), 'nontail %.2e' % r.get('nontail_vertices_max_shift_cm', 0), flush=True)
            if save and cid in ("SA-M188", "SA-F188", "SA-M208"):
                np.savez(B.C.S + '/w2i/npz/%s-C%d.npz' % (cid, -cv), v=P2.astype(np.float32))
    json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
