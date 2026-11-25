# sa6_pleat_allow.py OUTDIR V001_NPZ... : pleat allowances for the rig v002 pass-9b state and knot fits (PLEAT_ALLOW, read by sa6_pd2_fit.py / sa6_node_fit.py).
#   Input: sa6_pleat_audit.py measurements of the rig v001 states (KIND state, RP6_RIG unset).  Output per state: OUTDIR/pleat_allow_<STATE>.npz with
#   names (pose@fraction), P (packbits per pose of the edges the v001 state turns more than ALLOW_DEG from rest) and ev (edge list; the fit asserts the
#   same edge order).  ALLOW_DEG = 88: the pleat threshold 90 less 2 deg of measurement tolerance (found on MUFAHI hip_flex70_xpos: one pelvis edge at
#   v001 90.0 deg / layer 90.x deg that no solve cleared).  An allowed edge is a crease the accepted v001 state already has at that pose (knuckle creases in
#   fist / hand_opposition: 2-7 edges of v001's 3-33).
import sys, os, numpy as np
OUT = sys.argv[1]; LIM = float(os.environ.get('ALLOW_DEG', 88.0)); os.makedirs(OUT, exist_ok=True)
for f in sys.argv[2:]:
    A = dict(np.load(f)); nm = str(A['name']); assert str(A['kind']) in ('state', 'body') and str(A['rigv']) == 'v001', f   # body: knot bodies (sa6_node_fit)
    P = np.stack([np.packbits(x.astype(float) > LIM) for x in A['X']])
    np.savez_compressed(os.path.join(OUT, 'pleat_allow_%s.npz' % nm), names=A['names'], P=P, ev=A['ev'], source=os.path.basename(f),
                        rule='edges the rig v001 state turns > %.0f deg from rest at the pose' % LIM)
    print(nm, P.shape, flush=True)
