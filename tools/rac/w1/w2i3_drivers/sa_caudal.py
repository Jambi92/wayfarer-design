# RAC W2I3 caudal-base contour family (order §5-§10) on the rebuilt L1 + F2 candidate: C0 (alpha 0) / C1 0.2 / C2 0.4 / C3 0.6, neutral carriage.
# Bodies: SA-M188, SA-F188, SA-M168, SA-F168, SA-M208, SA-F208 (accepted §263 centre for the female bodies). Per case: front thigh-gap readings
# (sa_silhouette rule), a front z-buffer decomposition of what is seen through the gap (caudal-base zone / proximal 42 cm of tail vs free tail
# beyond vs posterior body), lowest visible zone point, root section area / RSI / volume / mass share / A50, ventral and dorsal half-depths at
# the landmark and 10 / 20 / 30 cm distal, dorsal-contour rise vs C0 (hump check), landmark and pelvis shift, static lean.
# Usage: python3 sa_caudal.py OUT.json [render]
import sys, os, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i_drivers'))
import sa_rebuild as RB, sa_build as B, sa_silhouette as SIL, sa_carriage as CA
L = RB.L; vary = RB.vary; Sr = vary.S_ROOT
ALPHA = {"C0": 0.0, "C1": 0.2, "C2": 0.4, "C3": 0.6}
BODIES = [("SA-M188", {}, B.H0), ("SA-F188", B.CEN, B.H0), ("SA-M168", {}, 168.0), ("SA-F168", B.CEN, 168.0), ("SA-M208", {}, 208.0), ("SA-F208", B.CEN, 208.0)]
TK = ('tail_root_area', 'tail_RSI_raw', 'tail_vol_L', 'tail_mass_share', 'tail_A50', 'tail_A25', 'tail_taper_raw', 'tail_len_pct', 'height')
def gap_decomp(P, q):
    w, C2, N2, k, o, s = RB.caudal_weight(P, q, RB.LC_DEF); x, f, u = P.T
    zone = (w > 0.02) | ((L.tail > 0.2) & (s > Sr - 42)); free = (L.tail > 0.5) & (s <= Sr - 42)
    sil = SIL.front_tail(P); cr = sil['crotch_u']; res = 0.5
    ix = np.round(x / res).astype(int); iu = np.round(u / res).astype(int); key = (ix + 600) * 100000 + iu
    order = np.lexsort((f, key)); kk = key[order]; vis = order[np.r_[kk[1:] != kk[:-1], True]]
    body = (L.tail < 0.2) & (L.arm < 0.2); out = dict(zone=0, free_tail=0, posterior_body=0); lowz = None
    for lev in np.arange(np.floor(cr) - 1, 0, -res):
        m = body & (np.abs(u - lev) < 0.5); xl = x[m & (x > 0)]; xr = x[m & (x < 0)]
        if len(xl) < 5 or len(xr) < 5: continue
        gl, gr = xl.min(), xr.max()
        if gl <= gr: continue
        vv = vis[(np.abs(u[vis] - lev) < res / 2) & (x[vis] < gl) & (x[vis] > gr)]
        for i in vv:
            if zone[i]: out['zone'] += 1; lowz = lev if lowz is None else min(lowz, lev)
            elif free[i]: out['free_tail'] += 1
            elif f[i] < -4: out['posterior_body'] += 1
    tot = sum(out.values()) or 1
    return dict(pixels=out, share={kk_: v / tot for kk_, v in out.items()}, lowest_visible_zone_u=lowz, crotch_u=cr)
def profile(P, q):
    w, C2, N2, k, o, s = RB.caudal_weight(P, q, RB.LC_DEF); z = (np.linalg.norm(P - C2[k], axis=1) < 24) & ((L.tail > 0.2) | (w > 0.02))
    res = {}
    for dcm in (0, 10, 20, 30):
        m = z & (np.abs(s - (Sr - dcm)) < 1.0)
        if m.sum() > 10: res["%d" % dcm] = dict(ventral=float(np.percentile(-o[m], 98)), dorsal=float(np.percentile(o[m], 98)), top_u=float(P[m, 2].max()), bottom_u=float(P[m, 2].min()))
    return res
if __name__ == '__main__':
    out = {}; render = len(sys.argv) > 2
    for bid, p, h in BODIES:
        base = None
        for cn, a in ALPHA.items():
            P, q, k, info = RB.build_r(p, dict(RB.TARGET, alpha=a), h); M = B.measure(P, q, k); sil = SIL.front_tail(P); cr, prof = CA.front_profile(P); tg = CA.tail_geom(P, q)
            vis = [w for lev, w, g in prof if w > 0]
            r = dict(alpha=a, silhouette=sil, max_visible_width_cm=max(vis) if vis else 0.0, lowest_tail_vertex_u=tg['lowest_tail_vertex_u'], gap=gap_decomp(P, q), sections=profile(P, q),
                     tail={kk: M[kk] for kk in TK}, lean=M['lean_scaled_deg'], root_point=tg['root_point'], caudal_info=info.get('caudal', {}))
            if base is None: base = dict(P=P, M=M, r=r)
            else:
                w0 = RB.caudal_weight(P, q, RB.LC_DEF)[0] == 0
                r['pelvis_outside_zone_max_shift_cm'] = float(np.abs(P[w0] - base['P'][w0]).max())
                r['landmark_shift_cm'] = float(np.linalg.norm(np.array(tg['root_point']) - np.array(base['r']['root_point'])))
                r['tail_delta_pct'] = {kk: 100 * (M[kk] / base['M'][kk] - 1) for kk in TK}
                r['dorsal_rise_cm'] = {d: r['sections'][d]['top_u'] - base['r']['sections'][d]['top_u'] for d in r['sections'] if d in base['r']['sections']}
                r['ventral_rise_cm'] = {d: r['sections'][d]['bottom_u'] - base['r']['sections'][d]['bottom_u'] for d in r['sections'] if d in base['r']['sections']}
                r['dlean'] = M['lean_scaled_deg'] - base['M']['lean_scaled_deg']
            out['%s|%s' % (bid, cn)] = r
            print(bid, cn, 'vis %.1f share %.4f maxw %.1f gap %s lowZone %s root %.1f RSI %.2f hump %s vrise %s' % (sil['visible_extent_cm'], sil['covered_share'] or 0, r['max_visible_width_cm'],
                  {kk: round(v, 2) for kk, v in r['gap']['share'].items()}, r['gap']['lowest_visible_zone_u'], M['tail_root_area'], M['tail_RSI_raw'],
                  {d: round(v, 1) for d, v in r.get('dorsal_rise_cm', {}).items()}, {d: round(v, 1) for d, v in r.get('ventral_rise_cm', {}).items()}), flush=True)
            if render and bid in ("SA-M188", "SA-F188"): np.savez(B.C.S + '/w2i/npz/W2I3-%s-%s.npz' % (bid, cn), v=P.astype(np.float32))
    json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
