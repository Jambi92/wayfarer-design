# sa6_path_scan.py STATE CFG W1,W2,.. POSES OUTDIR [LAYERS] : dense creator-weight scan of one base -> state path (corrective-layer validation, layer v004+).
#   Steering tool, not a gate: builds the path bodies at the given weights (same geometry method as sa6_blend precompute), and evaluates only the given poses
#   (all four angle fractions; the sa6_blend.evaluate ownership rules unchanged) with the packaged layer RP6_LAYERS.  Used to find the creator weights between
#   knots where the interpolated creator keys still leave a rig defect, so knots can be added there; the full 34-pose suite on held-out bodies is the gate.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
st, cfg, ws, poses, OD = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(',')], sys.argv[4].split(','), sys.argv[5]
if len(sys.argv) > 6: os.environ['RP6_LAYERS'] = sys.argv[6]
import sa6_blend as BL
B = {'%s-%s@%.4f' % ('c1' if cfg == 'M' else 'c2', st, w): dict(cfg=cfg, w={st: w}, kind='path scan', path=st, t=w) for w in ws}
BD = os.path.join(OD, 'bodies'); os.makedirs(BD, exist_ok=True); BL.precompute(BD, B); os.makedirs(OD, exist_ok=True)
for nm, b in B.items():
    fo = os.path.join(OD, nm + '.json')
    if os.path.exists(fo): continue
    r = BL.evaluate(nm, b, BD, BL.FRACS, poses); json.dump(r, open(fo, 'w'), indent=1); t = r['totals']
    bad = sorted({(pn, fr) for pn, v in r['poses'].items() for fr, c in v.items() if c['prod']['rig_flips'] or c['prod']['rig_pen'] or c['prod']['rig_tears'] or not c['prod']['volume_ok']})
    print('%-22s clean %s | flips %d pen %d tears %d volfail %d | %s' % (nm, r['clean'], t['rig_flips'], t['rig_pen'], t['rig_tears'], t['vol_fail'], bad), flush=True)
