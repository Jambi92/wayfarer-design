# sa6_ctrl_v2.py BODIES_DIR OUTDIR [BODY ...] : empty-K control artifacts for the rig v002 standard bakes (order 07a3f24c §4).
#   OUTDIR/<body>/BK_<body>.json/.npz with no families and no pose keys: baked(T) == packaged blend v005(T) (base v003 + creator layers v005), the
#   unbaked starting point and the "before" of every bake.  Recipe / cfg / weights metadata are copied from bodies.json (geometry comes from there too).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa6_common as C
assert C.RIGV == 'v002'
BD, OD = sys.argv[1:3]; B = json.load(open(os.path.join(BD, 'bodies.json')))['bodies']
for nm in sys.argv[3:] or ['BASE_c1', 'BASE_c2', 'END_FAHI', 'END_MUFAHI']:
    b = B[nm]; d = os.path.join(OD, nm); os.makedirs(d, exist_ok=True)
    json.dump(dict(status='RP6 RIG PILOT / NOT FROZEN', name='SA_RP6_control_%s_rigv002' % nm, body=nm, rig_version=C.RIGV, recipe=b.get('recipe', ''), cfg=b['cfg'], w=b['w'],
                   initialised_from='empty', layers=os.environ.get('RP6_LAYERS', 'SA_RP6_creator_layers_v005.json'), base_correctives=C.BASE_CORR,
                   semantics='CONTROL: empty K -> baked(T) == packaged blend v005(T) (rig v002 base v003 + creator layers v005)', converged=True, fit_log=[], families=[], pose_keys=[]),
              open(os.path.join(d, 'BK_%s.json' % nm), 'w'), indent=1)
    np.savez(os.path.join(d, 'BK_%s.npz' % nm)); print(nm, b['cfg'], b['w'])
