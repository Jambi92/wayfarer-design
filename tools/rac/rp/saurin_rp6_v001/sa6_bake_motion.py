# sa6_bake_motion.py NAME BODYDIR ARTDIR OUTDIR : motion-pop check of a per-body bake (offline bake validation order 8e3b7b4d, added after the first
#   offline pass found narrow adaptive pose keys: 0.2-1.8 cm switched on inside 0.25-1.75 deg on END_FAHI / END_MUFAHI).
#   Every anatomical pose is played 0 -> 1 on a grid of 1/240 of its full angle plus every driver transition (bake family samples, bake pose-key centres and
#   tent edges, packaged-blend family samples).  Per column (prod = packaged blend v004, bake = v004 + K) the corrected surface RELATIVE to plain LBS (posed space)
#   is recorded, and the measure is the FRAME EXCURSION: max over start f, over every grid point g with f < g <= f + 1/30, of max over the mesh
#   |rel(g) - rel(f)|  (cm).  One frame = 1/30 of the full angle, i.e. 30 fps with the full move in 1 s (the elbow's 130 deg in 1 s is the fast case); a tent
#   narrower than a frame is caught even if it rises and falls inside the frame.
#   PROPOSED MOTION GATE (bake only): frame excursion <= max(0.50 cm, the packaged blend's own excursion on the same pose)  -- the bake may not add a pop
#   beyond what the accepted package already does, and 0.50 cm covers the v004 elbow slope break (0.42-0.45 cm/frame) recorded for review.
#   Stateless evaluator: reverse playback equals forward.  MOTION_SHARD='i/n' -> poses[i::n] (merge with --merge).  -> OUTDIR/MO_<NAME>.json
import sys, os, json, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v004.json')
CAP, GRID, FRAME = 0.50, 240, 1.0 / 30.0
if sys.argv[1] == '--merge':        # sa6_bake_motion.py --merge NAME OUTDIR
    nm, OD = sys.argv[2:4]; import glob; out = None
    for p in sorted(glob.glob(os.path.join(OD, 'MO_%s.s*of*.json' % nm))):
        j = json.load(open(p)); out = out or dict(j, poses={}); out['poses'].update(j['poses'])
    out['clean'] = all(v['pass'] for v in out['poses'].values()); out['failing'] = sorted(k for k, v in out['poses'].items() if not v['pass'])
    out['worst'] = max(({'pose': k, **v} for k, v in out['poses'].items()), key=lambda v: v['bake']['frame_excursion_cm'])
    json.dump(out, open(os.path.join(OD, 'MO_%s.json' % nm), 'w'), indent=1)
    print(nm, 'MOTION clean', out['clean'], 'poses', len(out['poses']), 'failing', out['failing'], 'worst', out['worst']['pose'], out['worst']['bake']['frame_excursion_cm'], flush=True); sys.exit(0)
import sa6_blend as BL, sa6_layer_harness as H, sa6_correctives as CC
from sa6_bake import peak_mb
nm, BD, AD, OD = sys.argv[1:5]; os.makedirs(OD, exist_ok=True); art = os.path.join(AD, 'BK_%s.json' % nm); t_all = time.time()
b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]; R, z = BL.rig_of(nm, b, BD); K = CC.Correctives.load(R, art)
P0 = H.Blend(H.load_base(R, b['cfg']), [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()]); suite = R.suite('anat')
FAM = list(K.F.values()) + [f for st in [P0.B] + [s_ for _, s_ in P0.S] for f in getattr(st, 'F', {}).values()]
SH = os.environ.get('MOTION_SHARD'); si, sn = (int(x) for x in SH.split('/')) if SH else (0, 1); tag = '.s%dof%d' % (si, sn) if SH else ''
OUT = os.path.join(OD, 'MO_%s%s.json' % (nm, tag))
out = json.load(open(OUT)) if os.path.exists(OUT) else dict(status='RP6 RIG PILOT / NOT FROZEN', name=nm, artifact=os.path.basename(art),
    gate=dict(measure='frame excursion: max_f max_{f<g<=f+1/30} max_v |rel(g)-rel(f)|, rel = corrected - plain LBS (posed), cm', frame='1/30 of the full angle',
              grid='1/%d of the full angle + every driver transition' % GRID, pass_rule='bake <= max(%.2f cm, prod on the same pose)' % CAP), poses={})
for pn in sorted(suite)[si::sn]:
    if pn in out['poses']: continue
    t0 = time.time(); spec = suite[pn]; T1 = R.pose(spec); full = max(abs(dg) for _, _, _, dg in spec); fr = set(np.round(np.arange(0, 1.0 + 1e-9, 1.0 / GRID), 6))
    for f in FAM:
        if not any(e[0] == f['bone'] for e in spec): continue
        x1 = K.driver(T1, f)
        if abs(x1) > 1e-6: fr.update(round(s_ / x1, 6) for s_ in f['samples'])
    for k, pk in K.PK.items():
        x1 = K.driver(T1, dict(bone=pk['drivers'][0][0], axis=pk['drivers'][0][1])); s_ = pk['drivers'][0][2]; w = (pk.get('width') or [abs(s_)])[0]
        if abs(x1) > 1e-6 and any(e[0] == pk['drivers'][0][0] for e in spec): fr.update(round(c / x1, 6) for c in (s_ - w, s_, s_ + w))
    FR = np.array(sorted(f for f in fr if 0 <= f <= 1)); rel = {'prod': [], 'bake': []}; kact = 0.0
    for f in FR:
        T = R.pose([(bb, p, a, dg * f) for bb, p, a, dg in spec]); L = R.skin(T); dP = P0.delta(T); dK = K.delta(T); kact = max(kact, float(np.abs(dK).max()))
        rel['prod'].append((R.skin(T, R.V + dP) - L).astype(np.float32)); rel['bake'].append((R.skin(T, R.V + dP + dK) - L).astype(np.float32))
    res = dict(n_samples=int(len(FR)), full_deg=float(full), k_max_cm=round(kact, 5))
    for c in ('prod', 'bake'):
        A = rel[c]; best = (0.0, 0, 0)
        for i in range(len(FR)):
            j = i + 1
            while j < len(FR) and FR[j] - FR[i] <= FRAME + 1e-9:
                e = float(np.linalg.norm(A[j] - A[i], axis=1).max())
                if e > best[0]: best = (e, i, j)
                j += 1
        v = int(np.linalg.norm(A[best[2]] - A[best[1]], axis=1).argmax())
        res[c] = dict(frame_excursion_cm=round(best[0], 4), at=[float(FR[best[1]]), float(FR[best[2]])], at_deg=[round(float(FR[best[1]] * full), 2), round(float(FR[best[2]] * full), 2)],
                      vertex=v, region=str(R.ql[np.nonzero((R.Q == v).any(1))[0][0]]))
    lim = max(CAP, res['prod']['frame_excursion_cm']); res['limit_cm'] = round(lim, 4); res['pass'] = bool(res['bake']['frame_excursion_cm'] <= lim + 1e-6)
    res['seconds'] = round(time.time() - t0, 1); out['poses'][pn] = res; json.dump(out, open(OUT, 'w'), indent=1)
    print('%s %-24s %s prod %.3f bake %.3f cm/frame (limit %.3f) K %.3f | %d samples %.0fs %.0f MB' % (nm, pn, 'PASS' if res['pass'] else 'FAIL', res['prod']['frame_excursion_cm'],
          res['bake']['frame_excursion_cm'], lim, kact, len(FR), res['seconds'], peak_mb()), flush=True)
out['seconds'] = round(time.time() - t_all, 1); out['peak_mb'] = round(peak_mb(), 1); json.dump(out, open(OUT, 'w'), indent=1)
