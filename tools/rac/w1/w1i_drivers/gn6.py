# RAC W1i driver (scratch paths = this session's working directories; kept for provenance).
"""Gorrund W1i structural-continuity re-solve (order reviews/chatgpt-rac-w1i-gorrund-structural-continuity-resolve-order.md).
One skeleton recipe evaluated at the reference AND at every stature-series body (208 / 215 / 222 / 251 cm; same donors as
w1h_drivers/stress5.py) with the CIB bony stations in the loop.
Parameters (16): pelvis X/Y/Z, femur robusticity, clavicle length, upper-thorax length, ka amplitude, kp lower (r 0.18, 0.31),
kp upper (r 0.44, 0.6), kb at r 0 / 0.18 / 0.31 / 0.44 / 0.6 / 0.8, rib-cage bone breadth (spine_02 / spine_03 X). Sculpt profile is a C1 monotone cubic (PCHIP) between nodes
(no slope break at nodes) and stays off the free thigh (confine_legs).
Constraints (slack >= 0), ROBUSTNESS margins larger than the 1 % convention (validation targets, not anatomy; W1i §3, §9):
  every GO skeletal row (reference): strict > / < by 2.5 %, >= / <= by 0.8 %, ~ within 0.006;
  every ALPC-0...4 row at 208 / 215 / 222 / 251 cm with the same margins (incl. lower-thorax depth at 251 cm);
  ALPC-7 at every height pair GO h <= Broad Skarn h (208 / 215 / 222 / 229 cm) with the same margins;
  shares vs GR; chest-lead floors; buttock-lead; stature 229 +/- 2; arm clearance >= 0.5 cm; skin thoracic breadth / stature > SK
  by 2.5 % (directional-check reading); skin flank flare <= 0; waist level inside; slab sanity;
  CONTINUITY (W1i §2, §5, §6), all bounds taken from the accepted reference bodies (MF-M-R, SK, SG, GR, DU-NAT), not invented:
    skeleton (minimum-composition) body: waist / hip-block breadth >= max reference (no shelf; run I8 on - hip-block / thorax is
    reported only, see the note in slacks); waist / thorax breadth >= max reference
    (no pinch beyond the least-pinched reference); |second difference| of the breadth and depth profile <= max reference;
    reference skin: waist / hip-block breadth >= lowest reference skin (no hip shelf); skin hip-block / thorax reported only;
    low composition (GOR-BODY-16 = grid body 0.25 / 0.25): crest breadth >= 1.01 x the narrowest of the 8 measurement-layer levels
    above it, read on plane sections (ALPC-0 shape: a waist above the crest; see waist_rise).
Objective after feasibility: least extreme (squared deviation from the generator value) plus a barrier within 3 % of any bound."""
import sys, os, json, shutil, numpy as np
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1g_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1h_drivers'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gn3, gn4, profile_bump as PB, arm_clearance as AC, alpc_invariance as AI, skeletal_checks as SC, bony_envelope as BE
import trunk_profile as TP
from arm_measure import load
from scipy.optimize import minimize
W1F = gn4.W1F; G = gn3.G; F = gn3.F; S = gn3.S
NAMES = ["pelvisX", "pelvisY", "pelvisZ", "thigh", "clavY", "s03Y", "Aka", "kpL", "kpU", "kb0", "kb18", "kb31", "kb44", "kb60", "kb80", "thorX"]
LO = [0.95, 0.97, 1.0, 1.0, 0.85, 1.0, 0.0, 0.9, 0.85, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.95]
HI = [1.25, 1.10, 1.35, 1.40, 1.05, 1.25, 1.1, 1.7, 1.5, 1.3, 1.45, 1.4, 1.3, 1.2, 1.15, 1.15]
# femur-robusticity upper bound raised 1.25 -> 1.40 in run I6 (W1i): with the stature series in the loop, runs I1-I5 pinned the femur at
# 1.25 while the proximal-femur rows (hip-joint scale / crest >= MF, SK; ALPC-3 proximal femur / S6, shaft / femur at 208-222 cm) stayed
# short (gn6_I5.log). The 1.25 bound was a W1h search-range choice "near the W1f / W1g magnitudes", not anatomy; the order itself
# names "robust proximal legs" and "proximal-femur robusticity" as targets (W1i §2, §6). Femur LENGTH is not scaled.
# thorX (W1i, order §6): skeletal rib-cage breadth = spine_02 / spine_03 bone X scale, so thoracic breadth can be carried by bone
# instead of the upper-thorax soft-tissue sculpt kb80 alone (W1h needed kb80 1.1684, outside its bound)
M_STRICT, M_GE, M_TILDE = 0.025, 0.008, 0.006
SK_TB = json.load(open(gn3.SKP.replace('/skp', '/cand') + '/SK_meas.json'))['combined']['ratio']['thorax_breadth_share']
CLR = 0.5; LEAD_LEAN, LEAD_ENV = 0.0028, 0.0031
HEIGHTS = {"02": (F + '/go/GO2080_build.json', F + '/go/GO2080', 'GO2080'), "215": (G + '/h/GO0M215_build.json', G + '/h/GO0M215', 'GO0M215'),
           "222": (G + '/h/GO0M222_build.json', G + '/h/GO0M222', 'GO0M222'), "03": (G + '/h/GO0M251_build.json', G + '/h/GO0M251', 'GO0M251')}
SKB = {215: S + '/w1i/skb/skp_SKB215', 222: S + '/w1i/skb/skp_SKB222'}     # Broad Skarn 215 / 222 readings (W1h stress build; Skarn unchanged)
PAIRS = {"02": (215, 222, 229), "215": (222, 229), "222": (229,)}         # cross-height ALPC-7 pairs (equal-height 229 pair is in the reference rows)
RS = np.round(np.arange(0.0, 0.80001, 0.025), 3)

def cont(path):
    P = TP.profile(path, RS); b = np.array(P["b"]); d = np.array(P["d"]); m = (RS >= 0.1) & (RS <= 0.7)
    hb = np.nanmax(b[(RS >= 0) & (RS <= 0.2)]); th = np.nanmax(b[(RS >= 0.4) & (RS <= 0.72)]); wm = np.nanmin(b[(RS >= 0.15) & (RS <= 0.45)])
    return {"hip_over_thorax": hb / th, "waist_over_thorax": wm / th, "waist_over_hip": wm / hb, "d2b": float(np.nanmax(np.abs(np.diff(b, 2))[m[1:-1]])), "d2d": float(np.nanmax(np.abs(np.diff(d, 2))[m[1:-1]]))}

REFS = {"MF-M-R": (F + '/final_lean/MF-M-R-LEAN_rest.npz', F + '/final/MF-M-R_rest.npz'), "SK": (F + '/final_lean/SK-LEAN_rest.npz', F + '/final/SK_rest.npz'),
        "SG": (F + '/final_lean/SG-LEAN_rest.npz', F + '/final/SG_rest.npz'), "GR": (G + '/final_lean/GR-LEAN_rest.npz', G + '/final/GR_rest.npz'),
        "DU-NAT": (F + '/final_lean/DU-NAT-LEAN_rest.npz', F + '/final/DU-NAT_rest.npz')}
_RC = S + '/w1i/ref_continuity.json'
if not os.path.exists(_RC):
    json.dump({k: {"skeleton": cont(a), "skin": cont(b)} for k, (a, b) in REFS.items()}, open(_RC, 'w'), indent=1)
RC = json.load(open(_RC))
LIM = {"lean_hip_max": max(v["skeleton"]["hip_over_thorax"] for v in RC.values()), "lean_waist_min": max(v["skeleton"]["waist_over_thorax"] for v in RC.values()),
       "lean_d2b_max": max(v["skeleton"]["d2b"] for v in RC.values()), "lean_d2d_max": max(v["skeleton"]["d2d"] for v in RC.values()),
       "lean_shelf_min": max(v["skeleton"]["waist_over_hip"] for v in RC.values()),
       "skin_hip_max": max(v["skin"]["hip_over_thorax"] for v in RC.values()), "skin_shelf_min": min(v["skin"]["waist_over_hip"] for v in RC.values())}

def unpack(x, frame=None):
    x = [float(v) for v in x]
    tx = x[15] if len(x) > 15 else 1.0
    B = {"pelvis": [x[0], x[1], x[2]], "LR:thigh": [x[3], 1.0, x[3]], "LR:clavicle": [1.0, x[4], 1.0], "spine_03": [tx, x[5], 1.0]}
    if tx != 1.0: B["spine_02"] = [tx, 1.0, 1.0]
    ka = [1 + x[6] * (v - 1) for v in W1F["ka"]]; kp = list(W1F["kp"]); kp[1:5] = [x[7], x[7], x[8], x[8]]
    kb = list(W1F["kb"]); kb[0:6] = x[9:15]
    sc = {"r": W1F["r"], "ka": ka, "kp": kp, "kb": kb, "confine_legs": True, "interp": "pchip"}
    if frame:
        for k, v in frame.get("bone_scales", {}).items(): B[k] = [a * b for a, b in zip(B.get(k, [1, 1, 1]), v)]
        if "kb_nodes" in frame: sc["kb"] = [a * b for a, b in zip(sc["kb"], [1.0] + list(frame["kb_nodes"]) + [1.0])]
        for key in ("ka", "kp"):
            if key in frame:
                sc[key] = [a * frame[key] if (0 < i < len(sc[key]) - 1 and sc["r"][i] >= frame.get("kd_from", 0)) else a for i, a in enumerate(sc[key])]
    B = {k: [round(v, 4) for v in vv] for k, vv in B.items()}; sc = {k: ([round(v, 4) for v in vv] if isinstance(vv, list) else vv) for k, vv in sc.items()}
    return B, sc

def rowslack(rows, m, lab, pre, keep=None):
    for y in rows:
        if not (y['cand'] == 'GO' or y.get('b') == 'GO') or y['result'] in ('REPORT', 'NOT RUN'): continue
        if 'SENSITIVITY' in y['check']: continue
        if keep and not keep(y): continue
        for t, v in y['by_t'].items():
            a, b = v['va'], v['vb']
            if a is None or b is None: continue
            op = y['op']
            if 'ALPC-0' in y['check']: m.append(0.0 if a >= 1 else -0.05); lab.append(pre + 'ALPC-0|' + t); continue
            if op == '>': s = (a - b * (1 + M_STRICT)) / abs(b)
            elif op == '<': s = (b * (1 - M_STRICT) - a) / abs(b)
            elif op == '>=': s = (a - b * (1 + M_GE)) / abs(b)
            elif op == '<=': s = (b * (1 - M_GE) - a) / abs(b)
            elif op == '~': s = (M_TILDE - abs(a - b)) / abs(b)
            else: continue
            m.append(s); lab.append('%s%s|%s' % (pre, y['check'][:60], t))

def pair_rows(wd, gname, skb_h):
    """ALPC-7 rows with GO = this stress body and SKB = Broad Skarn at skb_h"""
    tmp = wd + '/pair_%s_%d' % (gname, skb_h)
    if os.path.exists(tmp): shutil.rmtree(tmp)
    shutil.copytree(gn3.SKP, tmp, symlinks=True, ignore=shutil.ignore_patterns('*_skp.json', '*.jpg', 'skeletal_checks*.json'))
    for t in ('0.0', '0.5', '1.0'):
        for idn, src in (("GO", wd + '/skp_%s/t%s/%s_meas.json' % (gname, t, gname)),
                         ("SKB", (SKB[skb_h] + '/t%s/SKB%d_meas.json' % (t, skb_h)) if skb_h in SKB else gn3.SKP + '/t%s/SKB%d_meas.json' % (t, skb_h))):
            dst = tmp + '/t%s/%s_meas.json' % (t, idn)
            if os.path.lexists(dst): os.remove(dst)
            shutil.copy(src, dst)
    rows = SC.run(tmp); shutil.rmtree(tmp, ignore_errors=True)
    return [r for r in rows if r['cand'] == 'GO' and 'ALPC-7' in r['check']]

def waist_rise(path, section=True):
    """waist search at the measurement-layer levels (9 levels spine_01 ... spine_03 head, trunk = keep & arm weight < 0.2):
    breadth at the crest level (level 0 = S5) / narrowest breadth at levels 1..8 above it. >= 1 means a waist sits above the crest
    (ALPC-0 shape). section=True (W1i default) reads exact plane sections, as the W1h CIB stations do: the measurement layer's
    +/-1 cm vertex slab misses the crest vertex ring on stretched Gorrund meshes (W1h GOR-BODY-16: slab 36.6 cm vs section 42.2 cm at
    the crest level, 21 vertices in the slab; `solver/waist_slab_vs_section.log`). section=False reproduces the measurement layer."""
    d = load(path); V = d["V"].astype(float); J = d["joints"]; hd = lambda n: np.asarray(J[n][0], float)
    armw = np.maximum.reduce([d["w_" + k] for k in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    trunk = d["keep"] & (armw < 0.2)
    TF = d["F"][trunk[d["F"]].all(1)]
    def slab(z):
        if section: return TP.section(V, TF, z)[0]
        P = V[trunk & (np.abs(V[:, 2] - z) < 1.0)]; return float(P[:, 0].max() - P[:, 0].min()) if len(P) > 5 else np.nan
    vv = [slab(z) for z in np.linspace(hd("spine_01")[2], hd("spine_03")[2], 9)]
    return vv[0] / np.nanmin(vv[1:])

GRr = None
def slacks(x, name, with_stress=True, wd=None):
    global GRr
    if GRr is None: GRr = {t: json.load(open(gn3.SKP + '/t%s/GR_meas.json' % t))['combined']['ratio'] for t in ('0.0', '0.5', '1.0')}
    B, sc = unpack(x); wd = wd or G + '/solve6'
    r, C = gn3.build("GO", name, B, sc, wd=wd); rows = gn3.checks("GO", name, wd=wd)
    m, lab = [], []; rowslack(rows, m, lab, '')
    sk = json.load(open(wd + '/skp_%s/%s_skp.json' % (name, name)))
    for t in ('0.0', '0.5', '1.0'):
        R = sk['by_t'][t]['ratio']
        m.append((R['torso_share'] - GRr[t]['torso_share'] * 1.013) / GRr[t]['torso_share']); lab.append('torso>GR|' + t)
        m.append((GRr[t]['leg_share'] * 0.987 - R['leg_share']) / GRr[t]['leg_share']); lab.append('leg<GR|' + t)
        m.append((GRr[t]['arm_share'] * 0.987 - R['arm_share']) / GRr[t]['arm_share']); lab.append('arm<GR|' + t)
    for nm, lv in ((name + '-LEAN', LEAD_LEAN), (name, LEAD_ENV)):
        b = PB.chest_lead(wd + '/%s_r6.npz' % nm); m.append((b - lv) / 0.01); lab.append('chest-lead ' + nm)
    b = PB.buttock_lead(wd + '/%s_r6.npz' % name); m.append((0.023 - b) / 0.01); lab.append('buttock-lead')
    H = r['r6']['stature']; m.append((2.0 - abs(H - 229.0)) / 100); lab.append('stature')
    c = AC.signed_clearance(wd + '/%s_r6.npz' % name); m.append((c - CLR) / 1.0); lab.append('arm clearance %.3f' % c)
    tb = BE.fast_stations(load(wd + '/%s_rest.npz' % name), section=False)['S2'][0] / H
    m.append((tb - SK_TB * (1 + M_STRICT)) / SK_TB); lab.append('skin TB/H > SK %.4f' % tb)
    fl = PB.flank_flare(wd + '/%s_r6.npz' % name)['flank_flare']; m.append((0.0 - fl) / 0.01); lab.append('skin flank flare %.4f' % fl)
    k4 = C.get('station_levels_from_reference', {}).get('S4', 4)
    m.append(0.0 if 0 < k4 < 8 else -0.2); lab.append('waist level index %s' % k4)
    for S_ in ('S2', 'S3', 'S4'):
        mn = min(v['stations'][S_][1] for v in C['per_body'].values()) / C['ref_skin'][S_][1]
        m.append((mn - 0.6) / 0.1); lab.append('slab sanity %s depth %.2f' % (S_, mn))
    # continuity (reference-derived limits)
    cl = cont(wd + '/%s-LEAN_rest.npz' % name); cs = cont(wd + '/%s_rest.npz' % name)
    # W1i run I8: the skeleton hip-block / thorax CAP (<= largest human reference) is dropped as a constraint and only reported: canon
    # ALPC-7 requires Gorrund crest / thorax > equal-height Broad Skarn, whose own skeleton reads hip / thorax 1.097-1.100, so a cap at
    # the human maximum (1.106) cannot coexist with ALPC-7 plus a margin (gn6_I7.log). The giant-pelvis guard becomes a no-shelf
    # guard instead: skeleton waist / hip-block >= the largest reference value (lumbar at least as full, relative to the pelvis, as in
    # the least-shelved accepted reference).
    m.append((cl["waist_over_hip"] - LIM["lean_shelf_min"]) / LIM["lean_shelf_min"]); lab.append('skeleton waist/hip %.3f >= ref max; skeleton hip/thorax %.3f (report)' % (cl["waist_over_hip"], cl["hip_over_thorax"]))
    m.append((cl["waist_over_thorax"] - LIM["lean_waist_min"]) / LIM["lean_waist_min"]); lab.append('skeleton waist/thorax %.3f >= ref max' % cl["waist_over_thorax"])
    m.append((LIM["lean_d2b_max"] - cl["d2b"]) / 0.01); lab.append('skeleton d2 breadth %.4f' % cl["d2b"])
    m.append((LIM["lean_d2d_max"] - cl["d2d"]) / 0.01); lab.append('skeleton d2 depth %.4f' % cl["d2d"])
    # skin: no hip shelf beyond the accepted references (waist / hip-block breadth >= the lowest reference); skin hip / thorax is
    # reported only (Gorrund canon requires pelvis / thorax >= MF, ALPC-2a, so a human ceiling on it would be invented)
    m.append((cs["waist_over_hip"] - LIM["skin_shelf_min"]) / LIM["skin_shelf_min"]); lab.append('skin waist/hip %.3f >= ref min; skin hip/thorax %.3f (report)' % (cs["waist_over_hip"], cs["hip_over_thorax"]))
    wr = waist_rise(wd + '/grid_%s/%s-C025025_rest.npz' % (name, name))
    m.append(wr - 1.01); lab.append('GOR-BODY-16 skin crest / narrowest level above it %.4f >= 1.01' % wr)
    if with_stress:
        for k, (base, donor, did) in HEIGHTS.items():
            nm = name + '-' + k; gn3.build("GO", nm, B, sc, wd=wd, base=base, donor=donor, did=did); rr = gn3.checks("GO", nm, wd=wd)
            rowslack(rr, m, lab, k + ':', keep=lambda y: AI.keep_row(y['check']))
            for hs in PAIRS.get(k, ()):
                rowslack(pair_rows(wd, nm, hs), m, lab, '%s vs SKB%d:' % (k, hs))
    return np.array(m), lab, H, C

def log(f, *a): print(*a, file=f, flush=True)

def barrier(xn):
    lo, hi = np.array(LO), np.array(HI); w = (hi - lo) * 0.03 + 1e-9
    return (np.maximum(0, (lo + w) - xn) / w) ** 2 + (np.maximum(0, xn - (hi - w)) / w) ** 2

if __name__ == '__main__':
    x = np.array(json.loads(sys.argv[1]), float); iters = int(sys.argv[2]); tag = sys.argv[3]; reg = float(sys.argv[4])
    free = json.loads(sys.argv[5]) if len(sys.argv) > 5 else list(range(len(x)))
    f = open(G + '/gn6_%s.log' % tag, 'a'); log(f, 'LIMITS', json.dumps(LIM), 'margins', M_STRICT, M_GE, M_TILDE)
    def sneg(mm): return -mm[mm < 0].sum()
    last = None; J = None
    for it in range(iters):
        m0, lab, H, C = slacks(x, tag + 'c')
        log(f, 'iter', it, json.dumps(dict(zip(NAMES, np.round(x, 4).tolist()))), 'H %.2f neg %d sumneg %.4f' % (H, int((m0 < 0).sum()), sneg(m0)))
        for k in np.where(m0 < 0)[0]: log(f, '   neg', lab[k], round(m0[k], 4))
        json.dump({"x": x.tolist(), "names": NAMES, "sumneg": sneg(m0)}, open(G + '/gn6_%s_cur.json' % tag, 'w'))
        h = 0.02
        def col(i):
            xp = x.copy(); xp[i] += h; mp, _, _, _ = slacks(xp, '%sd%d' % (tag, i)); return i, (mp - m0) / h
        every = int(os.environ.get('GN6_FULLJ_EVERY', '1')); J0 = os.environ.get('GN6_J0')
        if it == 0 and J0:    # restart from a saved Jacobian (same parameterisation and constraint list)
            J = np.load(J0); log(f, '   Jacobian loaded', J0)
        elif it % every and last is not None and len(last[1]) == len(m0):   # Broyden rank-1 update between full Jacobians
            dx, dm = last; J = J + np.outer(dm - J @ dx, dx) / (dx @ dx); log(f, '   Jacobian Broyden update')
        else:
            J = np.zeros((len(m0), len(x)))
            with ThreadPoolExecutor(2) as ex:
                for i, c in ex.map(col, free): J[:, i] = c
        np.save(G + '/gn6_%s_J%d.npy' % (tag, it), J)
        dev = lambda xn: np.where(np.arange(len(xn)) == 6, xn * 0.1, xn - 1)
        obj = lambda d: (np.minimum(0, m0 + J @ d) ** 2).sum() * 1e4 + 0.02 * (d ** 2).sum() + reg * (dev(x + d) ** 2).sum() + 0.5 * barrier(x + d).sum()
        mask = np.zeros(len(x)); mask[free] = 1
        bnds = [(max(-0.1, LO[i] - x[i]), min(0.1, HI[i] - x[i])) if mask[i] else (0, 0) for i in range(len(x))]
        d = minimize(obj, np.zeros(len(x)), method='L-BFGS-B', bounds=bnds).x
        best = None
        for a in (1.0, 0.5, 0.25):
            xn = x + a * d; mn, _, Hn, _ = slacks(xn, tag + 'c')
            sc_ = sneg(mn) + reg * (dev(xn) ** 2).sum() * 1e-2 + 0.005 * barrier(xn).sum()
            log(f, '   step a=%.2f sumneg %.4f neg %d score %.5f' % (a, sneg(mn), int((mn < 0).sum()), sc_))
            if best is None or sc_ < best[0]: best = (sc_, xn, mn)
        cur = sneg(m0) + reg * (dev(x) ** 2).sum() * 1e-2 + 0.005 * barrier(x).sum()
        if best[0] < cur - 1e-6: last = (best[1] - x, best[2] - m0); x = best[1]
        else: log(f, 'no improvement'); break
    json.dump({"x": x.tolist(), "names": NAMES}, open(G + '/gn6_%s_best.json' % tag, 'w'), indent=1)
    log(f, 'DONE', json.dumps(dict(zip(NAMES, np.round(x, 4).tolist()))))
