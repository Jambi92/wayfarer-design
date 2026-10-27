# validator_v2.py CAND.npz OUT.json : RAC §7 station validator v2 (order 2d34a0c §2 D1 + proposed D3). Same band / ring maths as audit.py (RP2 method),
# plus two documented measurement rules. Every station reports the legacy verdict AND the v2 verdict with an explicit status.
#  D1 (authorised, order 2d34a0c §2): a band side whose ray-exit is UNDEFINED (no candidate vertex in the probe ball faces the side direction,
#     normal . side <= 0.3 for all -> audit.py would pick an endpoint by candidate tie order) is excluded from the band minimum; the band uses only the
#     defined sides (status PASS_FALLBACK_DEFINED_SIDES when this changes the verdict). If NO side is defined, the station falls back to the literal
#     closed-ring test with a radius appropriate to the anatomical segment (thumb MCP: 3.0 cm, the thenar cross-section; all other stations keep
#     their station radius) -> status PASS_FALLBACK_CLOSED_RING.
#  D3 (PROPOSED, not yet authorised -- reported separately): for digit stations (finger / thumb MCP + IP, toe joints) a pole counts as a crease pole
#     of the station only if it lies on that digit, i.e. its nearest digit axis (bone / joint chain, same hand / foot) is the station's own digit.
#     The station pole radius (toe stations: 1.15 x (half joint spacing + 0.6 cm) = 1.0-1.5 cm) exceeds the toe spacing, so poles of the
#     NEIGHBOURING toe are otherwise counted.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core3lib import *
cz = np.load(sys.argv[1]); OUT = sys.argv[2]; V = cz['V'].astype(float); Q = np.asarray(cz['Q']); meta = json.loads(str(cz['meta'])); nV = len(V)
H = {k: np.array(v) for k, v in meta['heads'].items()}; T_ = {k: np.array(v) for k, v in meta['tails'].items()}; JC = {k: np.array(v) for k, v in meta['joint_cubes'].items()}
loops = closed_loops(Q, nV); au = Auditor(V, Q); S = stations(meta); JR = {j[0]: j for j in ring_stations(meta)}
ANAT_RING_R = {'thumb_mcp': 3.0}
# D4 (PROPOSED, MPFB Family Propagation Standard v1): station geometry (band half-width W, probe radius R, pole radius Rp, ring radius / window,
# anatomical fallback radius) is defined on the family reference body (Marchfolk configuration 1, stature REF_STATURE) and scaled by
# s = race stature / REF_STATURE, so a frozen topology is audited with the same anatomical band on every family member. --scale-ref 0 = off.
REF_STATURE = float(sys.argv[sys.argv.index('--scale-ref') + 1]) if '--scale-ref' in sys.argv else 0.0
STATURE = float(V[:, 2].max() - V[:, 2].min()); SCALE = STATURE / REF_STATURE if REF_STATURE > 0 else 1.0
if SCALE != 1.0:
    S = [(nm, c, d, Wd * SCALE, Rr * SCALE, need, (Rp * SCALE if Rp is not None else None)) for nm, c, d, Wd, Rr, need, Rp in S]
    JR = {k: (j[0], j[1], j[2], j[3] * SCALE, j[4] * SCALE) for k, j in JR.items()}; ANAT_RING_R = {k: v * SCALE for k, v in ANAT_RING_R.items()}
# digit axes
def chain_fingers(s):
    out = {}
    for fg in ('thumb', 'index', 'middle', 'ring', 'pinky'):
        pts = [H['%s_01_%s' % (fg, s)], H['%s_02_%s' % (fg, s)], H['%s_03_%s' % (fg, s)], T_['%s_03_%s' % (fg, s)]]; out[fg] = pts
    return out
def chain_toes(s):
    out = {}
    for t in range(1, 6):
        ks = sorted([n for n in JC if n.startswith('%s-toe-%d-' % (s, t))], key=lambda n: int(n.split('-')[-1])); pts = [JC[k] for k in ks]; pts.append(pts[-1] + (pts[-1] - pts[-2]) * 1.0); out['toe%d' % t] = pts
    return out
def segdist(p, pts):
    best = 1e9
    for a, b in zip(pts[:-1], pts[1:]):
        ab = b - a; t = np.clip((p - a) @ ab / (ab @ ab), 0, 1); best = min(best, float(np.linalg.norm(p - (a + t * ab))))
    return best
AX = {s: dict(chain_fingers(s), **chain_toes(s)) for s in ('l', 'r')}
def digit_of(nm):
    s = nm[-1]
    if nm.startswith('toe'): return s, nm.split('_')[0], [k for k in AX[s] if k.startswith('toe')]
    for fg in ('thumb', 'index', 'middle', 'ring', 'pinky'):
        if nm.startswith(fg + '_'): return s, fg, [k for k in AX[s] if not k.startswith('toe')]
    return None
def owner(p, s, group):
    return min(group, key=lambda g: segdist(V[p], AX[s][g]))
R = {}
for nm, c, d, Wd, Rr, need, Rp in S:
    c = np.asarray(c, float); d = unit(np.asarray(d, float)); pp = unit(np.cross(d, [0, 1.0, 0] if abs(d[1]) < 0.9 else [1.0, 0, 0])); qq = unit(np.cross(d, pp)); sides = []
    for side, sn in ((pp, '+p'), (-pp, '-p'), (qq, '+q'), (-qq, '-q')):
        def undefined(p0):
            cand = au.kd.query_ball_point(p0 + side * Rr * 0.5, Rr * 0.9)
            return bool(len(cand) == 0 or not (au.VN[np.array(cand)] @ side > 0.3).any())
        ua, ub = undefined(c - d * Wd), undefined(c + d * Wd); a = au.surf(c - d * Wd, side, Rr); b = au.surf(c + d * Wd, side, Rr); ent = dict(side=sn, defined=not (ua or ub))
        if np.linalg.norm(V[a] - V[b]) < 0.7 * 2 * Wd: ent['merged'] = True; sides.append(ent); continue
        _, pred = dijkstra(au.G, indices=a, return_predecessors=True, limit=4 * Wd + 3 * Rr)
        if pred[b] < 0: ent['no_path'] = True; sides.append(ent); continue
        path = [b]
        while path[-1] != a: path.append(int(pred[path[-1]]))
        e = np.diff(V[path], axis=0); ent['loops'] = int((np.abs(e @ d) > 0.5 * np.linalg.norm(e, axis=1)).sum()); sides.append(ent)
    counted = [x['loops'] for x in sides if 'loops' in x]; counted_def = [x['loops'] for x in sides if 'loops' in x and x['defined']]
    band_legacy = min(counted) if counted else 0; band_def = min(counted_def) if counted_def else None
    rn = ring_name(nm); rings_std = len(encircling(V, loops, *JR[rn][1:5])) if rn in JR else 0
    key_ = '_'.join(nm.split('_')[:2]); rings_anat = len(encircling(V, loops, JR[rn][1], JR[rn][2], ANAT_RING_R[key_], JR[rn][4])) if (rn in JR and key_ in ANAT_RING_R) else rings_std
    near = np.nonzero(np.linalg.norm(au.e0 - c, axis=1) < Rr)[0]; h = float(np.median(au.wE[near])) if len(near) else 0.3
    Rp_ = Rr if Rp is None else Rp; PV = V[au.poles]; pb = (PV - c) @ d; pr = np.linalg.norm((PV - c) - np.outer(pb, d), axis=1)
    cre = au.poles[(np.abs(pb) <= 0.5 * h) & (pr <= Rp_)]; w2 = au.poles[(np.abs(pb) <= 2 * h) & (pr <= Rp_)]
    dg = digit_of(nm); own = lambda ids: [int(p) for p in ids if dg is None or owner(p, dg[0], dg[2]) == dg[1]]
    cre_own, w2_own = own(cre), own(w2); adj = sorted(set(int(p) for p in cre) - set(cre_own)); adj_w2 = sorted(set(int(p) for p in w2) - set(w2_own))
    loops_legacy = max(rings_std, band_legacy)
    if band_def is None: loops_d1 = rings_anat; mode = 'closed_ring_fallback'
    else: loops_d1 = max(rings_std, band_def); mode = 'band_all_sides' if all(x['defined'] for x in sides if 'loops' in x) else 'band_defined_sides'
    firm_legacy = loops_legacy >= need and len(cre) == 0; strict_legacy = loops_legacy >= need and len(w2) == 0
    firm_d1 = loops_d1 >= need and len(cre) == 0; strict_d1 = loops_d1 >= need and len(w2) == 0
    firm_d3 = loops_d1 >= need and len(cre_own) == 0; strict_d3 = loops_d1 >= need and len(w2_own) == 0
    def status(firm, real_loops_ok, crease_n):
        if not firm: return 'FAIL_LOOPS' if not real_loops_ok else 'FAIL_CREASE_POLE'
        if firm_legacy: return 'PASS'
        return {'closed_ring_fallback': 'PASS_FALLBACK_CLOSED_RING', 'band_defined_sides': 'PASS_FALLBACK_DEFINED_SIDES'}.get(mode, 'PASS')
    st_d1 = status(firm_d1, loops_d1 >= need, len(cre)); st_d3 = status(firm_d3, loops_d1 >= need, len(cre_own))
    if st_d3 == 'PASS' and not firm_d1 and firm_d3: st_d3 = 'PASS_SCOPED_ADJACENT_DIGIT_POLE'
    if st_d3.startswith('PASS_FALLBACK') and len(adj): st_d3 += '+SCOPED_ADJACENT_DIGIT_POLE'
    R[nm] = dict(required=need, sides=sides, band_loops_legacy=band_legacy, band_loops_defined=band_def, closed_rings=rings_std, closed_rings_anatomical=rings_anat, loops_legacy=loops_legacy, loops_v2=loops_d1,
                 loop_mode=mode, crease_poles=[int(p) for p in cre], crease_poles_own_digit=cre_own, crease_poles_adjacent_digit=adj, within2_poles=[int(p) for p in w2], within2_own_digit=w2_own,
                 within2_adjacent_digit=adj_w2, local_loop_cm=round(h, 4), firm_legacy=bool(firm_legacy), strict_legacy=bool(strict_legacy), firm_D1=bool(firm_d1), strict_D1=bool(strict_d1),
                 firm_D1_D3=bool(firm_d3), strict_D1_D3=bool(strict_d3), status_D1=st_d1, status_D1_D3=st_d3)
summ = dict(legacy_firm_fail=sorted(k for k, v in R.items() if not v['firm_legacy']), D1_firm_fail=sorted(k for k, v in R.items() if not v['firm_D1']), D1_D3_firm_fail=sorted(k for k, v in R.items() if not v['firm_D1_D3']),
            D1_strict_fail=sorted(k for k, v in R.items() if not v['strict_D1']), D1_D3_strict_fail=sorted(k for k, v in R.items() if not v['strict_D1_D3']),
            D1_fallback_passes={k: v['status_D1'] for k, v in R.items() if v['status_D1'].startswith('PASS_FALLBACK')},
            D1_D3_non_plain={k: v['status_D1_D3'] for k, v in R.items() if v['status_D1_D3'] != 'PASS'})
json.dump(dict(validator='RAC §7 validator v2 (D1 + D3 accepted, order 85b7c1c; D4 station scaling proposed)', station_scale=SCALE, reference_stature_cm=REF_STATURE, stature_cm=STATURE, anatomical_ring_radius_cm=ANAT_RING_R, summary=summ, stations=R), open(OUT, 'w'), indent=1)
print(json.dumps(summ, indent=1))
