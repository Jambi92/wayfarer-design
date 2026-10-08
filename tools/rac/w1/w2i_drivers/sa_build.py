# RAC W2I Saurin body builder + measurement. NON-CANON diagnostics; the frozen SA-M anatomy (aff1b52) is never written back.
# Creator states (frame, composition, tail, sex-related A / E / B, lower-trunk bound) use the ACCEPTED creator-biology / §263 tool chain at the
# reference stature (vary.warp / tissue.fwarp; constant 187.9 cm as validated in Part 7 / §263).
# Stature route (W2I; order §4 "no uniform scaling"): Saurin has no generator and no skeleton, so stature is changed by REGIONAL factors in the
# same sense as the accepted human native short-adult route (native_short.py): one length factor k for every vertical body segment, girth
# (x, f) k^0.654, head (uniform about the neck / head junction) k^0.688, hands k^0.842, feet k^0.942 - the accepted W2 generator-allometry
# betas (native_short_allometry.json) - and the TAIL ISOMETRIC (uniform k about the caudal-base landmark) because SAURIN §256.9 states
# "stature is isometric for every tail relationship; tail length is defined in % of standing height". k is solved so standing height (tail
# excluded) hits the target. The Part 7 / §263 "168 / 208 cm" creator checks used the global height factor (uniform scale); they are reported
# beside the regional route as the creator-convention cross-check, not used as the W2 family.
# Usage: python3 sa_build.py OUT.json [SAVE_DIR]
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_common as C
from sa_common import V, F, L, vary, fsets3
BETA = json.load(open('/home/claude/wayfarer-design/tools/rac/w1/native_short_allometry.json'))["betas"]
H0 = 187.881473082305; ss = vary.ss
TOR = C.TOR
def station(u0):
    return int(np.argmin(np.abs(V[:, 2] - u0) + 100 * (~TOR) + 10 * (np.abs(V[:, 0]) > 3)))
ST = {"inlet": station(152.0), "costal": C.I123, "platform": station(100.0), "hip": C.I91}    # phase-A axial stations (thoracic inlet, costal margin, pelvic platform, hip-joint level)
WH = L.head; WT = L.tail; u0 = V[:, 2]
WHAND = L.arm * ss((99 - u0) / 3); WFOOT = ss((10 - u0) / 3) * (1 - L.tail)
II = np.arange(200)
def stature_map(P, q, k, extra=None):
    """apply the regional stature route with length factor k to the vertices P and to the tail axis q['_C2']"""
    kg, kh, ka, kf = k ** BETA["girth"], k ** BETA["head"], k ** BETA["hand"], k ** BETA["foot"]
    B = lambda X: X * np.array([kg, kg, k])
    C2 = q['_C2']; kr = int(vary.S_ROOT * 2); root = C2[kr]
    tr = np.arange(len(C2)) > kr + 20; hp = C2[np.where(tr)[0][np.argmin(np.abs(C2[tr, 2] - 166.0 * P[:, 2].max() / H0))]]      # neck / head junction on the current axis
    piv_w = {sd: P[(L.arm > 0.5) & (L.side == sd) & (np.abs(u0 - 97) < 1)].mean(0) for sd in (1, -1)}                              # wrists (current geometry)
    piv_a = {sd: np.append(P[(L.leg > 0.5) & (L.side == sd) & (np.abs(u0 - 8) < 1)].mean(0)[:2], 0.0) for sd in (1, -1)}          # ankles, projected to the ground
    def comp(X, wh, wt, wha, wfo, sides):
        out = B(X)
        for w, piv, f_ in ((wh, hp, kh), (wt, root, k)):
            if w is None: continue
            R = B(piv) + f_ * (X - piv); out = out + w[:, None] * (R - B(X))
        if wha is not None:
            for sd in (1, -1):
                m = (sides == sd)
                R = B(piv_w[sd]) + ka * (X - piv_w[sd]); out = out + (wha * m)[:, None] * (R - B(X))
                R = B(piv_a[sd]) + kf * (X - piv_a[sd]); out = out + (wfo * m)[:, None] * (R - B(X))
        return out
    Pn = comp(P, WH, WT, WHAND, WFOOT, L.side)
    C2 = q['_C2']; i = np.arange(len(C2)); wt_ = ss((vary.S_ROOT + 3 - i * 0.5) / 8.0); wh_ = ss((C2[:, 2] - 166) / 8.0)
    q2 = dict(q); q2['_C2'] = comp(C2, wh_, wt_, None, None, None); q2['_s'] = q.get('_s', 1.0) * k
    return Pn, q2
def at_stature(P, q, h):
    if abs(h - H0) < 1e-6: return P, dict(q), 1.0
    k = h / P[:, 2].max()
    for _ in range(8):
        Pn, q2 = stature_map(P, q, k); hh = Pn[:, 2].max(); k *= h / hh
        if abs(hh - h) < 0.01: break
    Pn, q2 = stature_map(P, q, k); return Pn, q2, k
def measure(P, q, k=1.0):
    M = C.measure(P, q); H = M['height']; sH = H / H0
    for nm, i in ST.items(): M['u_' + nm] = float(P[i, 2])
    M['thoracic_vertical'] = M['u_inlet'] - M['u_costal']; M['lower_trunk_costal_hip'] = M['u_costal'] - M['u_hip']; M['lower_trunk_costal_platform'] = M['u_costal'] - M['u_platform']
    for x in ('thoracic_vertical', 'lower_trunk_costal_hip', 'lower_trunk_costal_platform', 'shoulder_b', 'thorax_w', 'pelvis_w', 'thorax_d', 'head_depth', 'head_len', 'tail_len'):
        M[x + '_over_H'] = M[x] / H
    M['lean_scaled_deg'] = float(np.degrees(np.arctan2((M['heel_f'] + 8.4 * sH) - M['com_f'], M['com_u'] - 9.0 * sH)))     # stature-scaled §257 static model
    M['k_len'] = k
    x, f, u = P.T; ft = u < 1.5 * sH
    for sd, nm in ((1, 'L'), (-1, 'R')):
        m = ft & (L.side == sd) & (WFOOT > 0.5)
        if m.sum() > 20: M['foot_len_' + nm] = float(np.ptp(f[m])); M['foot_breadth_' + nm] = float(np.ptp(x[m]))
    if 'foot_len_L' in M: M['foot_len_over_H'] = 0.5 * (M['foot_len_L'] + M['foot_len_R']) / H; M['foot_breadth_over_H'] = 0.5 * (M['foot_breadth_L'] + M['foot_breadth_R']) / H
    return M
NAR, BRD, Mx = fsets3.NARROW, fsets3.BROAD, fsets3.M
CEN = fsets3.CEN
def tail(pct, base):
    return {'tail_len': pct / 64.613, 'tail_base': base}
BODIES = []      # (id, params, stature, note)
for h in (168, 188, 203, 208):
    hh = H0 if h == 188 else float(h)
    BODIES += [("SA-M%d" % h, {}, hh, "male centre"), ("SA-F%d" % h, CEN, hh, "§263 female centre")]
    BODIES += [("SA-M%d-N" % h, NAR, hh, "Narrow"), ("SA-M%d-B" % h, BRD, hh, "Broad")]
    BODIES += [("SA-M%d-LT90" % h, {'trunk_len': 0.90}, hh, "lower-trunk -10 % species bound (AD-R36)")]
for h in (168, 203): BODIES += [("SA-F%d-LT90" % h, Mx(CEN, {'trunk_len': 0.90}), float(h), "female-shifted body at the -10 % lower-trunk request (CONSTRAIN to bound)")]
COMP = {"MULO": {'muscle': -1.0}, "MUHI": {'muscle': 1.0}, "FALO": {'fat': -1.0}, "FAHI": {'fat': 1.0}, "MUFAHI": {'muscle': 1.0, 'fat': 1.0}, "MIN": {'muscle': -1.0, 'fat': -1.0}}
for nm, c in COMP.items():
    BODIES += [("SA-M188-" + nm, c, H0, "composition"), ("SA-F188-" + nm, Mx(CEN, c), H0, "composition (female centre)")]
BODIES += [("SA-M208-B-MUHI", Mx(BRD, {'muscle': 1.0}), 208.0, "Broad + high muscle at the Gorrund overlap"), ("SA-M208-B-MUFAHI", Mx(BRD, {'muscle': 1.0, 'fat': 1.0}), 208.0, "Broad + high muscle + fat at 208")]
# §263 sex stress cases (female centre)
BODIES += [("SA-F188-N", Mx(CEN, NAR), H0, "Narrow female centre"), ("SA-F188-B", Mx(CEN, BRD), H0, "Broad female centre"), ("SA-FREF188", fsets3.REF, H0, "accepted +10 % reference female"),
           ("SA-F188-N-B30", Mx(CEN, NAR, {'vfull': 3.0}), H0, "Narrow + B 3.0 requested"), ("SA-F188-N-B21", Mx(CEN, NAR, {'vfull': 2.1}), H0, "Narrow + B clamped 2.1"),
           ("SA-F188-N-FAHI", Mx(CEN, NAR, {'fat': 1.0}), H0, "Narrow + high fat, B 1.6"), ("SA-F188-N-FAHI-B15", Mx(CEN, NAR, {'fat': 1.0, 'vfull': 1.5}), H0, "Narrow + high fat, B clamped 1.5")]
# tails (§256; RM-UB-04 anchors and low end) - coupled base from the accepted Part 7 pairs (55 % base 0.83-0.85, 78 % base 1.15, Broad 80 % base 1.16, 80 % base 1.22 = rule)
BODIES += [("SA-M188-T55", tail(55, 0.85), H0, "tail 55 % + coupled base"), ("SA-M188-T78", tail(78, 1.15), H0, "RM-UB-04 anchor: Balanced, reference composition, ~78 %"),
           ("SA-M188-T80", tail(80, 1.22), H0, "Balanced 80 % with rule base (beyond the Balanced anchor)"), ("SA-M188-B-T80", Mx(BRD, tail(80, 1.16)), H0, "RM-UB-04 anchor: Broad 80 %"),
           ("SA-M188-N-FAHI-T72", Mx(NAR, {'fat': 1.0}, tail(72, 1.10)), H0, "RM-UB-04 anchor: Narrow + high fat ~72 %"), ("SA-M188-N-FAHI-T78", Mx(NAR, {'fat': 1.0}, tail(78, 1.15)), H0, "Narrow + high fat at 78 % (beyond its anchor)"),
           ("SA-M168-T55", tail(55, 0.85), 168.0, "short stature + short tail"), ("SA-M208-B-T80", Mx(BRD, tail(80, 1.16)), 208.0, "tallest Broad + 80 % tail"),
           ("SA-M188-T55-B83", tail(55, 0.83), H0, "low end: 55 % with the length^1.18 coupled base (0.83)")]
# creator-convention cross-check (Part 7: global height factor = uniform scale)
BODIES += [("SA-M168-UNIF", {'height': 168.0}, H0, "Part 7 creator convention (uniform), cross-check only"), ("SA-M208-UNIF", {'height': 208.0}, H0, "Part 7 creator convention (uniform), cross-check only")]
if __name__ == '__main__':
    out = {}; save = sys.argv[2] if len(sys.argv) > 2 else None
    keep = {"SA-M168", "SA-M188", "SA-M203", "SA-M208", "SA-F188", "SA-M188-N", "SA-M188-B", "SA-M208-B", "SA-M168-LT90", "SA-M203-LT90", "SA-M188-MIN", "SA-M188-MUFAHI",
            "SA-M188-T55", "SA-M188-T78", "SA-M188-B-T80", "SA-M188-N-FAHI-T72", "SA-F168", "SA-F208", "SA-M208-B-MUHI"}
    for bid, p, h, note in BODIES:
        P, q = C.build(p); P2, q2, k = at_stature(P, q, h); M = measure(P2, q2, k); M['note'] = note; M['params'] = {a: b for a, b in p.items()}; out[bid] = M
        print(bid, round(M['height'], 2), 'k %.4f' % k, 'LT %.2f' % M['lower_trunk_costal_hip'], 'd/w %.3f' % M['thorax_d_over_w'], 'tail %.1f%%' % M['tail_len_pct'], 'lean %.2f' % M['lean_scaled_deg'], flush=True)
        if save and bid in keep: np.savez(save + '/%s.npz' % bid, v=P2.astype(np.float32))
    json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
