# RAC W3B RM-UF-04 (facial fields) / RM-UB-08 (body fields): independent SIZE and RELIEF sweeps per named field, combined corners, guards.
# DIAGNOSTIC GUARDS (thresholds proposed for author review; every measured value is kept in results):
#   S1 FUNCTIONAL SPAN: angle one scale unit spans over the field's tightest functional bend (size / bend radius, deg). Deformable fields
#      (fine expressive, articulation, contact): <= max(30 deg, canonical) - beyond, rigid units facet / bridge the bend ("plate-like rigidity",
#      lids / mouth margin / joints that cannot fold). Structural / ventral: <= max(60 deg, canonical) - beyond, a unit wraps the limb / trunk
#      curvature as an encircling plate (armor band).
#   S2 HIERARCHY: fine expressive / articulation / contact unit size <= 0.80 x the adjacent structural field (and <= its relief); a shrinking
#      structural field must stay >= 1.25 x the finer fields it borders (order section 18: articulation / fine fields finer than structural).
#   S3 INTEGUMENT VOCABULARY: relief amplitude >= the subtlest accepted scale relief anywhere on the canonical body (mouth margin, 0.0116 cm;
#      below = smoother than any accepted Saurin integument = "human-skin patch"); aspect (relief / size) <= max(0.30, canonical) (0.30 = the
#      most pronounced accepted relief/size outside the hand; beyond = tubercular / spiky / armored read).
#   S4 TOPOLOGY: EXCESS folded faces on the surfaced field over the canonical surface's own count (orientation vs the unsurfaced base)
#      <= max(2, 10 % of the canonical count) (a reseeded field moves its folds, so new-face counts are not comparable); sliver faces < 25 % of the field's median face area excluded - the base
#      carries clusters of near-degenerate faces whose orientation flips numerically under any relief change).
#   S5 CROWDING / SEAM: nearest-neighbour spacing CV <= max(0.35, 1.25 x canonical) (collisions / density steps).
#   S6 VENTRAL: >= 6 units across the ventral field width (never continuous belly-scute armor).
# Usage: python3 w3b_scale_run.py size|relief REGION[,REGION...] | corners REGION smin smax rmin rmax
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_scale as SC, w3b_regions as RG
W = C.W + '/scale'; os.makedirs(W, exist_ok=True)
CAN = json.load(open(C.W + '/scale_canon_metrics.json'))
CLS = {k: c for c, ks in RG.CLASS.items() for k in ks}
DEFORM = lambda k: k.startswith(('A_', 'C_')) or k in ('face_orbital_eyelid', 'face_mouth_margin', 'face_rostrum_cheek', 'face_jaw_corner', 'face_auricular')
FLOOR = min(v['relief_cm'] for v in CAN.values()); ASP = 0.30
_fl = None
def faces_area():
    global _fl
    if _fl is None:
        Z = SC.ref(); V = Z['Vu']; F = Z['Fu']; _fl = 0.5 * np.linalg.norm(np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]), axis=1)
    return _fl
def flips(rel, aff):
    Z = SC.ref(); V = Z['Vu']; F = Z['Fu']; N = Z['N'].astype(np.float64); m = np.zeros(len(V), bool); m[aff] = True
    fi = np.where(m[F].all(1))[0]; fa_ = faces_area()[fi]; fi = fi[fa_ >= 0.25 * np.median(fa_)]; Fq = F[fi]     # slivers (< 25 % of the field's median face area) excluded
    Pa = V + rel[:, None] * N; Pr = V + Z['disp'][:, None] * N
    cr = lambda P: np.cross(P[Fq[:, 1]] - P[Fq[:, 0]], P[Fq[:, 2]] - P[Fq[:, 0]])
    nb = cr(V); fa = (cr(Pa) * nb).sum(1) < 0; fc = (cr(Pr) * nb).sum(1) < 0      # orientation vs the unsurfaced base face
    return {"new": int((fa & ~fc).sum()), "total": int(fa.sum()), "canonical": int(fc.sum())}
def ventral_units(k, size):
    Z = SC.ref(); m = RG.masks()[k]; V = Z['Vu'][m]
    if k == 'V_chest_abdomen': w = np.ptp(V[np.abs(V[:, 2] - 125) < 2, 0])
    elif k == 'V_throat_anterior_neck': w = np.ptp(V[np.abs(V[:, 2] - 160) < 2, 0])
    else: w = np.ptp(V[np.abs(V[:, 1] - np.median(V[:, 1])) < 3, 0])
    return float(w / size), float(w)
def guards(k, fm, rel, aff, s_adj=None):
    c = CAN[k]; g = {}; val = {}
    if fm.get('size_cm') is None: return {'S0_units': False}, {'span_deg': float('nan'), 'flips': -1}     # < 4 units left in the field core
    span = np.degrees(fm['size_cm'] / c['bend_radius_cm']); lim = max(30.0 if DEFORM(k) else 60.0, c['span_deg'] + 1e-6); val['span_deg'] = span; g['S1_span'] = span <= lim
    if k in RG.ADJ:
        a = CAN[RG.ADJ[k]]; ratio = fm['size_cm'] / a['size_cm']; val['size_over_adjacent_structural'] = ratio
        g['S2_hierarchy'] = ratio <= max(0.80, c['size_cm'] / a['size_cm'] + 1e-6) and fm['relief_cm'] <= max(a['relief_cm'], c['relief_cm'])
    finer = [j for j, a in RG.ADJ.items() if a == k]
    if finer:
        r = min(fm['size_cm'] / CAN[j]['size_cm'] for j in finer); val['size_over_finest_bordering'] = r; g['S2_hierarchy'] = g.get('S2_hierarchy', True) and r >= 1.25
    g['S3_floor'] = fm['relief_cm'] >= FLOOR - 1e-9; g['S3_aspect'] = fm['aspect'] <= max(ASP, c['aspect'] + 1e-6); val['aspect'] = fm['aspect']
    fd = flips(rel, aff); nf = fd['total'] - fd['canonical']; val['flips'] = nf; val['folds_total'] = fd['total']; val['folds_canonical'] = fd['canonical']; val['folds_new_faces'] = fd['new']
    g['S4_topology'] = nf <= max(2, 0.10 * fd['canonical'])          # EXCESS folds over the canonical surface's own count (a reseeded field moves its folds)
    g['S5_crowding'] = fm['size_cv'] <= max(0.35, 1.25 * c['size_cv'])
    if k.startswith('V_'):
        n, wd = ventral_units(k, fm['size_cm']); val['units_across'] = n; g['S6_ventral'] = n >= 6
    return g, val
_W = {}
def run_case(k, s, r, rng=7, reseed=None):
    if k not in _W: _W[k] = SC.weight(RG.masks()[k])
    w = _W[k]
    rel, seeds, R, H, aff, pure = SC.variant(w, s, r, rng_seed=rng, reseed=(s != 1.0 or rng != 7) if reseed is None else reseed)
    fm = SC.field_metrics(w >= 0.9, pure, seeds); g, val = guards(k, fm, rel, aff)
    g = {a: bool(b) for a, b in g.items()}; val = {a: (float(b) if not isinstance(b, int) else b) for a, b in val.items()}
    return dict(region=k, cls=CLS[k], s=s, r=r, rng=rng, reseeded=bool((s != 1.0 or rng != 7) if reseed is None else reseed), metrics=fm, guards=g, values=val, valid=bool(all(g.values())), fails=[a for a, b in g.items() if not b])
def run(cases, out=os.environ.get('W3B_OUT', 'results.json')):
    rp = W + '/' + out; res = json.load(open(rp)) if os.path.exists(rp) else {}
    for k, s, r, rng, *rs in cases:
        rs = rs[0] if rs else None
        tag = '%s|s%.3f|r%.3f|g%d%s' % (k, s, r, rng, '|reseeded' if rs else '')
        if tag in res: continue
        res[tag] = run_case(k, s, r, rng, rs); json.dump(res, open(rp, 'w'), indent=1)
        x = res[tag]; mt = dict(size_cm=float('nan'), relief_cm=float('nan'), aspect=float('nan')); mt.update({a: b for a, b in x['metrics'].items() if b is not None})
        print(tag, 'size %.4f relief %.4f asp %.3f span %.1f flips %s %s' % (mt['size_cm'], mt['relief_cm'], mt['aspect'],
              x['values']['span_deg'], x['values']['flips'], 'OK' if x['valid'] else 'FAIL ' + ','.join(x['fails'])), flush=True)
SIZES = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.75, 2.0, 2.5]
RELIEFS = [0.25, 0.4, 0.5, 0.6, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0]
if __name__ == '__main__':
    mode = sys.argv[1]; regs = sys.argv[2].split(',')
    if regs == ['face']: regs = RG.CLASS['face']
    if regs == ['body']: regs = RG.CLASS['structural'] + RG.CLASS['articulation'] + RG.CLASS['ventral'] + RG.CLASS['contact']
    if mode == 'size': run([(k, s, 1.0, 7, True) for k in regs for s in SIZES])      # every size value incl. 1.0 on a reseeded field (attributable deltas)
    if mode == 'relief': run([(k, 1.0, r, 7) for k in regs for r in RELIEFS])
    if mode == 'cases': run([(a.split('@')[0], float(a.split('@')[1]), float(a.split('@')[2]), int(a.split('@')[3]) if a.count('@') > 2 else 7) for a in sys.argv[2].split(';')])
