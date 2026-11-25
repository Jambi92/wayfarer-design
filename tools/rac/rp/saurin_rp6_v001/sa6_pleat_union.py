# sa6_pleat_union.py BODIES_JSON V001_DIR OUTDIR BODY... : per-body pleat allowance for the rig v002 bakes (PLEAT_ALLOW_UNION, read by sa6_correctives.Solver.pleat_edges).
#   The bake tools (sa6_bake*.py) evaluate poses without a pose name, so the per-pose allowance of the layer / knot fits (sa6_pleat_allow.py) cannot be used.
#   Allowance per body = union over every anatomical pose and special gate at 0.25 / 0.5 / 0.75 / 1.0 of the edges the body's rig v001 references turn > ALLOW_DEG
#   (88 = the pleat threshold 90 less 2 deg tolerance, as sa6_pleat_allow.py): the base configuration (V001_DIR/v001_base_<cfg>.npz) and each state with
#   weight > 0 (V001_DIR/v001_state_<state>.npz), sa6_pleat_audit.py measurements of rig v001; mouth-slit edges plain LBS pleats and corrected-system edges
#   are left to the gate's own exemptions.  The per-pose verdict on a baked body is the pleat audit of the baked artifact against the same references.
import sys, os, json, numpy as np
BJ, VD, OUT = sys.argv[1:4]; LIM = float(os.environ.get('ALLOW_DEG', 88.0)); os.makedirs(OUT, exist_ok=True); bm = json.load(open(BJ))['bodies']
for nm in sys.argv[4:]:
    b = bm[nm]; refs = ['v001_base_%s.npz' % b['cfg']] + ['v001_state_%s.npz' % s for s, w in b['w'].items() if w > 0]; U = None; ev = None
    for f in refs:
        A = dict(np.load(os.path.join(VD, f))); assert str(A['rigv']) == 'v001', f
        if ev is None: ev = A['ev']
        assert (A['ev'] == ev).all(), f
        u = (A['X'].astype(float) > LIM).any(0); U = u if U is None else U | u
    np.savez_compressed(os.path.join(OUT, 'pleat_union_%s.npz' % nm), P=np.packbits(U), ev=ev, refs=np.array(refs), body=nm,
                        rule='union over poses / fractions of edges the rig v001 references turn > %.0f deg' % LIM)
    print(nm, refs, int(U.sum()), flush=True)
