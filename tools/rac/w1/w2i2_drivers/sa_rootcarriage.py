# RAC W2I2-C (order §12-§14): measurement-only PROXIMAL / ROOT carriage family for SAU-SILHOUETTE.
# Lever: sa_cand root pitch (upward pitch of the free-tail direction ramping smoothly from 0 at the caudal-base landmark to theta over the
# proximal LP cm; distal tail_curv neutral 0). LP choice: the smallest of 10 / 15 / 20 cm whose added bend keeps the maximum smoothed
# (5 cm window) centreline curvature inside the bend zone at or below the as-built maximum of the free tail at +8 deg (no new curvature
# extreme = no kink). Tested pitch 0 / +2 / +4 / +6 / +8 deg on SA-M188, SA-F188, SA-M208 (reference tails) plus SA-M188 55 % / 78 % tails.
# Per state: sa_carriage front thigh-gap readings, lowest tail point, root tangent, proximal curvature, tip height, distal elevation, invariance
# (caudal base, non-tail vertices, tail section readings) and static lean (same-state, interim guard).  Usage: python3 sa_rootcarriage.py OUT.json [save]
import sys, os, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i_drivers'))
import sa_cand as SC, sa_build as B, sa_silhouette as SIL, sa_carriage as CA
C = B.C; L = B.L; vary = SC.vary; H0 = B.H0; Mx = B.Mx
PITCH = [0.0, 2.0, 4.0, 6.0, 8.0]
CASES = [("SA-M188", {}, H0), ("SA-F188", B.CEN, H0), ("SA-M208", {}, 208.0), ("SA-M188-T78", B.tail(78, 1.15), H0), ("SA-M188-T55", B.tail(55, 0.85), H0)]
def smooth_curv(C2, kr):
    seg = C2[:kr + 1]; t = np.diff(seg, axis=0); t /= np.linalg.norm(t, axis=1)[:, None]; w = 10                  # 5 cm windows (0.5 cm spacing)
    a = np.degrees(np.unwrap(np.arctan2(t[:, 2], -t[:, 1]))); ak = np.convolve(a, np.ones(w) / w, mode='valid')
    c = np.abs(ak[w:] - ak[:-w]) / (w * 0.5)                                                                     # deg / cm over 5 cm
    return c, a
def root_metrics(q, LP):
    C2 = q['_C2']; kr = int(vary.S_ROOT * 2); c, a = smooth_curv(C2, kr); n = len(c)
    zone = slice(max(n - int(2 * LP) - 10, 0), n)                                                                  # bend zone next to the root
    return dict(root_tangent_deg=float(np.mean(a[kr - 6:kr])), tangent_10cm_deg=float(np.mean(a[kr - 26:kr - 20])), max_curv_zone=float(c[zone].max()), max_curv_free=float(c.max()),
                centreline_min_u=float(C2[:kr, 2].min()))
if __name__ == '__main__':
    out = {"LP_choice": {}}; save = len(sys.argv) > 2
    P, q = C.build({}); base = root_metrics(q, 20.0); out["LP_choice"]["as_built"] = base; LPc = None
    for LP in (10.0, 15.0, 20.0):
        P, q = C.build({'tail_root_pitch': 8.0, 'tail_root_len': LP}); m = root_metrics(q, LP); ok = m['max_curv_zone'] <= base['max_curv_free'] + 1e-9
        out["LP_choice"]["LP%d" % LP] = dict(**m, ok=ok); print('LP', LP, m, ok, flush=True)
        if ok and LPc is None: LPc = LP
    LPc = LPc or 20.0; out["LP"] = LPc
    for cid, p, h in CASES:
        b0 = None
        for th in PITCH:
            pp = Mx(p, {'tail_root_pitch': th, 'tail_root_len': LPc}) if th else dict(p)
            P, q = C.build(pp); P2, q2, k = B.at_stature(P, q, h); M = B.measure(P2, q2, k)
            sil = SIL.front_tail(P2); cr, prof = CA.front_profile(P2); tg = CA.tail_geom(P2, q2); rm = root_metrics(q2, LPc); vis = [w for lev, w, g in prof if w > 0]
            r = dict(root_pitch_deg=th, LP_cm=LPc, silhouette=sil, width_profile=prof, max_visible_width_cm=max(vis) if vis else 0.0, visible_levels=len(vis), tail=tg, root=rm,
                     lean=M['lean_scaled_deg'], tail_readings={kk: M[kk] for kk in CA.TAILK}, tail_min_u=M['tail_min_u'], reach_behind_heel=M['tail_reach_behind_heel'])
            nt = L.tail < 1e-6
            if b0 is None: b0 = dict(P=P2, M=M, r=r)
            else:
                r['nontail_vertices_max_shift_cm'] = float(np.abs(P2[nt] - b0['P'][nt]).max())
                r['root_point_shift_cm'] = float(np.linalg.norm(np.array(tg['root_point']) - np.array(b0['r']['tail']['root_point'])))
                r['tail_readings_delta_pct'] = {kk: 100 * (M[kk] / b0['M'][kk] - 1) for kk in CA.TAILK}
                r['dlean_vs_0deg'] = M['lean_scaled_deg'] - b0['M']['lean_scaled_deg']
            out['%s|pitch%+d' % (cid, th)] = r
            print(cid, 'pitch %+d' % th, 'vis %.1f share %.4f maxw %.1f lowest %.1f crotch %.1f tip %.1f elev %.1f rootT %.1f curvZ %.2f dlean %.3f nontail %.1e' % (
                sil['visible_extent_cm'], sil['covered_share'] or 0, r['max_visible_width_cm'], tg['lowest_tail_vertex_u'], sil['crotch_u'], tg['tip_u'], tg['distal20_elevation_deg'],
                rm['root_tangent_deg'], rm['max_curv_zone'], r.get('dlean_vs_0deg', 0), r.get('nontail_vertices_max_shift_cm', 0)), flush=True)
            if save and cid in ("SA-M188", "SA-F188", "SA-M208"): np.savez(C.S + '/w2i/npz/%s-R%d.npz' % (cid, th), v=P2.astype(np.float32))
    json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
