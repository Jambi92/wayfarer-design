# val2lib.py : RAC §7 joint validator v2 as a library (MPFB Family Propagation Standard v1, §6). Same maths as the v003 / Skarn validator_v2.py
# (byte-identical station verdicts, regression-checked); validator_v2.py is now a thin CLI over evaluate().
# Validator hierarchy (order a18371c §2, d921903 §4): ordinary band method -> D1 undefined-side fallback -> D3 same-digit pole ownership -> D4 stature-normalised
# station geometry -> D5 interdigital endpoint validity -> D6 non-digit foreign-segment ownership. AUTHORITATIVE = D1 + D3 + D4 + D5 + D6.
#  D1 (accepted, 85b7c1c): a band side whose ray exit is UNDEFINED (no candidate vertex in the probe ball faces the side, normal . side <= 0.3) is
#     excluded from the band minimum (status PASS_FALLBACK_DEFINED_SIDES when this changes the verdict). If NO side is defined, the station uses the
#     closed-ring test at an anatomical radius (thumb MCP 3.0 cm; other stations keep their ring radius) -> PASS_FALLBACK_CLOSED_RING.
#  D3 (accepted, 85b7c1c): for digit stations a pole is a crease pole only if its nearest digit axis is the station's own digit.
#  D4 (ACCEPTED, a18371c): station geometry (band half-width W, probe radius R, pole radius Rp, ring radius / axial window, anatomical fallback
#     radius) is defined on the family reference body (Marchfolk configuration 1, stature 173.143 cm) and scaled by s = stature / 173.143.
#  D5 (ACCEPTED 33a2dfe; d5=True; authoritative with D4): digit stations only -- a band side is undefined when the endpoint selected at either band
#     end lies farther from its probe line than the band half-width W, i.e. no surface vertex of the digit's own cross-section answers the probe (the
#     selection fell through to a vertex across an inter-digital web / cleft). The side is then excluded exactly as in D1. Every side always reports
#     its two endpoint offsets (endpoint_offset_cm) as diagnostics.
#  D6 (ACCEPTED d921903 -- proposed c6c7940; d6=(W, bone_names); AUTHORITATIVE with D4 + D5): non-digit stations only -- a band side is undefined
#     when the endpoint selected at either band end lies on a FOREIGN body segment, i.e. its dominant skin bone (largest deform weight, carried through
#     the family map) is not one of the station's own bones (the two segments meeting at the joint plus the adjacent trunk segment). Example: the hip
#     +p (lateral) probe ball reaches the forearm hanging beside the hip in the R-6 stance and counts forearm loops. Excluded exactly as D1 / D5
#     (if every side becomes undefined the station falls back to closed rings, as D1). Never modify geometry to satisfy a foreign-segment side.
import numpy as np
from core3lib import *
REF_STATURE_CM = 173.143
D6_OWN = {'neck': ('neck_01', 'head', 'spine_03'), 'shoulder': ('clavicle_{s}', 'upperarm_{s}', 'spine_03', 'spine_02'), 'elbow': ('upperarm_{s}', 'lowerarm_{s}'),
          'wrist': ('lowerarm_{s}', 'hand_{s}'), 'hip': ('pelvis', 'spine_01', 'thigh_{s}'), 'knee': ('thigh_{s}', 'calf_{s}'), 'ankle': ('calf_{s}', 'foot_{s}', 'ball_{s}')}
def evaluate(V, Q, meta, ref_stature=0.0, names=None, loops=None, au=None, d5=False, d6=None):
    V = np.asarray(V, float); Q = np.asarray(Q); nV = len(V)
    H = {k: np.array(v) for k, v in meta['heads'].items()}; T_ = {k: np.array(v) for k, v in meta['tails'].items()}; JC = {k: np.array(v) for k, v in meta['joint_cubes'].items()}
    loops = closed_loops(Q, nV) if loops is None else loops; au = Auditor(V, Q) if au is None else au; S = stations(meta); JR = {j[0]: j for j in ring_stations(meta)}
    ANAT_RING_R = {'thumb_mcp': 3.0}
    STATURE = float(V[:, 2].max() - V[:, 2].min()); SCALE = STATURE / ref_stature if ref_stature > 0 else 1.0
    if SCALE != 1.0:
        S = [(nm, c, d, Wd * SCALE, Rr * SCALE, need, (Rp * SCALE if Rp is not None else None)) for nm, c, d, Wd, Rr, need, Rp in S]
        JR = {k: (j[0], j[1], j[2], j[3] * SCALE, j[4] * SCALE) for k, j in JR.items()}; ANAT_RING_R = {k: v * SCALE for k, v in ANAT_RING_R.items()}
    if names is not None: S = [s for s in S if s[0] in names]
    def chain_fingers(s):
        return {fg: [H['%s_01_%s' % (fg, s)], H['%s_02_%s' % (fg, s)], H['%s_03_%s' % (fg, s)], T_['%s_03_%s' % (fg, s)]] for fg in ('thumb', 'index', 'middle', 'ring', 'pinky')}
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
    def owner(p, s, group): return min(group, key=lambda g: segdist(V[p], AX[s][g]))
    R = {}
    for nm, c, d, Wd, Rr, need, Rp in S:
        c = np.asarray(c, float); d = unit(np.asarray(d, float)); pp = unit(np.cross(d, [0, 1.0, 0] if abs(d[1]) < 0.9 else [1.0, 0, 0])); qq = unit(np.cross(d, pp)); sides = []
        for side, sn in ((pp, '+p'), (-pp, '-p'), (qq, '+q'), (-qq, '-q')):
            def undefined(p0):
                cand = au.kd.query_ball_point(p0 + side * Rr * 0.5, Rr * 0.9)
                return bool(len(cand) == 0 or not (au.VN[np.array(cand)] @ side > 0.3).any())
            ua, ub = undefined(c - d * Wd), undefined(c + d * Wd); a = au.surf(c - d * Wd, side, Rr); b = au.surf(c + d * Wd, side, Rr); ent = dict(side=sn, defined=not (ua or ub))
            offs = []
            for p0, e_ in ((c - d * Wd, a), (c + d * Wd, b)):
                r_ = V[e_] - p0; offs.append(round(float(np.linalg.norm(r_ - (r_ @ side) * side)), 4))
            ent['endpoint_offset_cm'] = offs
            if d5 and ent['defined'] and digit_of(nm) is not None and max(offs) > Wd: ent['defined'] = False; ent['D5_undefined'] = True
            if d6 is not None and digit_of(nm) is None:
                key6 = nm.split('_')[0]; own6 = {b.format(s=nm[-1]) for b in D6_OWN[key6]}; dom = [str(d6[1][int(np.argmax(d6[0][e_]))]) for e_ in (a, b)]; ent['endpoint_dominant_bone'] = dom
                ent['endpoint_dominant_weight'] = [round(float(d6[0][e_].max()), 3) for e_ in (a, b)]; ent['endpoints'] = [int(a), int(b)]
                if ent['defined'] and any(x not in own6 for x in dom): ent['defined'] = False; ent['D6_undefined'] = True
            if np.linalg.norm(V[a] - V[b]) < 0.7 * 2 * Wd: ent['merged'] = True; sides.append(ent); continue
            _, pred = dijkstra(au.G, indices=a, return_predecessors=True, limit=4 * Wd + 3 * Rr)
            if pred[b] < 0: ent['no_path'] = True; sides.append(ent); continue
            path = [b]
            while path[-1] != a: path.append(int(pred[path[-1]]))
            e = np.diff(V[path], axis=0); ent['loops'] = int((np.abs(e @ d) > 0.5 * np.linalg.norm(e, axis=1)).sum())
            if d6 is not None: ent['path'] = [int(x) for x in path]
            sides.append(ent)
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
        d5u = [x['side'] for x in sides if x.get('D5_undefined')]
        if d5u and st_d3.startswith('PASS_FALLBACK'): st_d3 += '+D5_INTERDIGITAL_UNDEFINED'
        d6u = [x['side'] for x in sides if x.get('D6_undefined')]
        if d6u and st_d3.startswith('PASS_FALLBACK'): st_d3 += '+D6_FOREIGN_SEGMENT_UNDEFINED'
        R[nm] = dict(required=need, sides=sides, D5_undefined_sides=d5u, D6_undefined_sides=d6u, valid_sides=[x['side'] for x in sides if x['defined'] and 'loops' in x], band_loops_legacy=band_legacy, band_loops_defined=band_def, closed_rings=rings_std, closed_rings_anatomical=rings_anat, loops_legacy=loops_legacy, loops_v2=loops_d1,
                     margin=int(loops_d1 - need), loop_mode=mode, crease_poles=[int(p) for p in cre], crease_poles_own_digit=cre_own, crease_poles_adjacent_digit=adj, within2_poles=[int(p) for p in w2],
                     within2_own_digit=w2_own, within2_adjacent_digit=adj_w2, local_loop_cm=round(h, 4), firm_legacy=bool(firm_legacy), strict_legacy=bool(strict_legacy), firm_D1=bool(firm_d1),
                     strict_D1=bool(strict_d1), firm_D1_D3=bool(firm_d3), strict_D1_D3=bool(strict_d3), status_D1=st_d1, status_D1_D3=st_d3)
    summ = dict(legacy_firm_fail=sorted(k for k, v in R.items() if not v['firm_legacy']), D1_firm_fail=sorted(k for k, v in R.items() if not v['firm_D1']), D1_D3_firm_fail=sorted(k for k, v in R.items() if not v['firm_D1_D3']),
                D1_strict_fail=sorted(k for k, v in R.items() if not v['strict_D1']), D1_D3_strict_fail=sorted(k for k, v in R.items() if not v['strict_D1_D3']),
                D1_fallback_passes={k: v['status_D1'] for k, v in R.items() if v['status_D1'].startswith('PASS_FALLBACK')},
                D1_D3_non_plain={k: v['status_D1_D3'] for k, v in R.items() if v['status_D1_D3'] != 'PASS'},
                margin_zero=sorted(k for k, v in R.items() if v['margin'] == 0), firm_pass_count=int(sum(v['firm_D1_D3'] for v in R.values())), stations=len(R))
    return dict(validator='RAC §7 validator v2 (D1 + D3 accepted 85b7c1c; D4 stature-normalised station geometry accepted a18371c; D5 interdigital endpoint validity accepted 33a2dfe; D6 foreign-segment endpoint accepted d921903)', D5_applied=bool(d5), D6_applied=d6 is not None, station_scale=SCALE, reference_stature_cm=ref_stature,
                stature_cm=STATURE, anatomical_ring_radius_cm=ANAT_RING_R, summary=summ, stations=R)
