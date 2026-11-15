import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001')
import sa6_pose as SP, sa6_layer_harness as H, sa6_blend as BL
bm = json.load(open('/tmp/claude-0/rp6/blend_bodies/bodies.json'))['bodies']
for nm in ('BASE_c1', 'END_MUFAHI'):
    b = bm[nm]; R, z = BL.rig_of(nm, b, '/tmp/claude-0/rp6/blend_bodies'); Bc = H.load_base(R, 'M')
    Ss = [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()]; P = H.Blend(Bc, Ss)
    for pn in ('trunk_twist_30', 'hip_flex70_xpos', 'shoulder_abd90_xneg'):
        spec = R.suite('anat')[pn]; T = R.pose(spec); c = R.relcos(R.skin(T, R.V + P.delta(T)), T); cl = R.relcos(R.skin(T), T)
        print(nm, pn, 'prod quads relcos<0: %d, 0..0.02: %d, 0.02..0.05: %d, 0.05..0.1: %d | LBS<0.05: %d' % ((c < 0).sum(), ((c >= 0) & (c < .02)).sum(), ((c >= .02) & (c < .05)).sum(), ((c >= .05) & (c < .1)).sum(), (cl < .05).sum()))
