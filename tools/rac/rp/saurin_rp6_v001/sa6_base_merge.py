# sa6_base_merge.py CFG ARM.json REST.json OUT.json : rig v002 base correctives v004 (order 07a3f24c §4, regression found by the v002 tail review).
#   Base v003 (PC pass 5) started from sa6_fair_keys.py, which low-pass filtered EVERY corrective key of the body, and refit with sa6_fit.fair after every
#   clean solve.  That was meant for the corrected shoulder cap; applied to the unaffected systems it weakened their accepted v001 shapes, and the fold
#   align then cleared the LBS folds only just past the flip threshold (relcos ~0.15): near-vertical pleats between neighbouring quads (posed dihedral
#   change > 90 deg) at the ankle, toes, tail root, pelvis and thumb, and a visible tail-root crease (tail concentration 0.49 -> 1.73 deg, BASE_c1
#   tail_root_biased_60).  No gate sees them (no quad flips).  Pass 4 (before fairing) still has the v001 shapes there.
#   v004 = the corrected systems from ARM (v003: families on clavicle_* / upperarm_* / forearm_*, incl. the elbow muscle layer, and the pose keys driven by
#   those bones) + every other family and pose key from REST (pass 4, unfaired).  Checked by sa6_eval.py (full suite + special gates) and sa6_pleat_audit.py.
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
assert os.environ.get('RP6_RIG') == 'v002'
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_layer_harness as H
cfg, A, B, OUT = sys.argv[1:5]
ARM = tuple(os.environ.get('MERGE_ARM', 'clavicle_,upperarm_,forearm_').split(','))
def arm(b): return b.startswith(ARM)
R = SP.Rig(cfg, C.w_path(cfg, H.PKG)); KA = CC.Correctives.load(R, A); KB = CC.Correctives.load(R, B); K = CC.Correctives(R)
for k, f in KA.F.items():
    if arm(f['bone']): K.F[k] = f
for k, f in KB.F.items():
    if not arm(f['bone']): assert k not in K.F; K.F[k] = f
for n, p in KA.PK.items():
    if any(arm(d[0]) for d in p['drivers']): K.PK[n] = p
for n, p in KB.PK.items():
    if not any(arm(d[0]) for d in p['drivers']): assert n not in K.PK; K.PK[n] = p
ja, jb = json.load(open(A)), json.load(open(B))
meta = {k: v for k, v in ja.items() if k not in ('families', 'pose_keys', 'fit_log', 'method', 'init', 'converged')}
meta.update(merge=dict(tool='sa6_base_merge.py', arm_bones=list(ARM), arm_source=dict(path=A, sha256=C.sha(A)), rest_source=dict(path=B, sha256=C.sha(B)),
                       families=dict(arm=sum(arm(f['bone']) for f in K.F.values()), rest=sum(not arm(f['bone']) for f in K.F.values())),
                       pose_keys=dict(arm=sum(any(arm(d[0]) for d in p['drivers']) for p in K.PK.values()), rest=sum(not any(arm(d[0]) for d in p['drivers']) for p in K.PK.values()))))
K.save(OUT, meta); print(cfg, 'families', len(K.F), 'pose keys', len(K.PK), meta['merge']['families'], meta['merge']['pose_keys'], flush=True)
