# sa6_bake_integrity.py NAME BODYDIR ARTDIR [OUTDIR] : RP5 / package integrity of a per-body offline bake (offline bake validation order 8e3b7b4d §1).
#   Reopens ARTDIR/BK_<NAME>.json/.npz from disk and records:
#     frozen RP5 package : every file listed in SAURIN_RP5_FREEZE.json 'frozen_files' re-hashed against the manifest (files absent from this machine are listed,
#                          never assumed); cage topology sha256 (Q) == manifest topology_sha256; semantic face array / semantic map hashes == manifest.
#     body               : vertex / quad count and face list identical to the frozen topology (same order); quad semantic labels identical in order;
#                          body file sha256 == the roster hash (bodies.json, recorded before fitting) + vertex-array sha256; base bodies (no state weights) == the frozen-workspace base geometry.
#     neutral            : max |packaged blend + K| at the rest pose (must be exactly 0); baked neutral skin == plain-LBS neutral skin (exactly); plain-LBS neutral
#                          vs the body (float round-off of the identity pose through the skinning sum, recorded, < 1e-4 cm).
#     ranges             : signature of every gated pose definition (pose, bone, degrees) for 'anat', the 50 special gates and the RP5-literal suite:
#                          the bake adds K only, so the accepted biological ranges and RP5-literal diagnostics are unchanged (same signature on every body).
#   -> OUTDIR/IN_<NAME>.json
import sys, os, json, hashlib, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v005.json' if os.environ.get('RP6_RIG') == 'v002' else 'SA_RP6_creator_layers_v004.json')   # rig v002: layers v005
import sa6_common as C, sa6_correctives as CC, sa6_layer_harness as H, sa6_blend as BL, sa6_gates as GT
def h(a): return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
nm, BD, AD = sys.argv[1:4]; OD = sys.argv[4] if len(sys.argv) > 4 else AD; os.makedirs(OD, exist_ok=True)
b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]; art = os.path.join(AD, 'BK_%s.json' % nm)
man = json.load(open(C.FZ + '/SAURIN_RP5_FREEZE.json')); ff = man['frozen_files']
files = {}
for f, hx in ff.items():
    p = os.path.join(C.FZ, f); files[f] = ('match' if C.sha(p) == hx else 'MISMATCH') if os.path.exists(p) else 'absent on this machine'
d = C.load(); z0 = np.load(C.FZ + '/SA_RP5_full_cage_freeze_candidate_v001.npz')
R, z = BL.rig_of(nm, b, BD); K = CC.Correctives.load(R, art)
P0 = H.Blend(H.load_base(R, b['cfg']), [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()]); T0 = R.pose([])
dn = P0.delta(T0) + K.delta(T0); Pn = R.skin(T0, R.V + dn); Pl = R.skin(T0)
Vs = np.load(os.path.join(BD, nm + '.npz'))['Vs']
base_geo = None
if not b['w']:
    ref = d['V1'] if b['cfg'] == 'M' else d['V2']; base_geo = float(np.abs(Vs - ref).max())
def sig(P): return hashlib.sha256(json.dumps(sorted([pn, [[e[0], round(float(e[3]), 6)] for e in P[pn]]] for pn in P)).encode()).hexdigest()
out = dict(status='RP6 RIG PILOT / NOT FROZEN', name=nm, artifact=os.path.basename(art), artifact_sha256=C.sha(art), artifact_npz_sha256=C.sha(art.replace('.json', '.npz')),
           frozen_files=files, frozen_ok=all(v != 'MISMATCH' for v in files.values()),
           topology=dict(manifest=man['topology']['topology_sha256'], frozen_Q=h(z0['Q'].astype(np.int64)), body_Q=h(R.Q.astype(np.int64)), nv=int(R.nv), nq=int(len(R.Q)),
                         manifest_verts=man['topology']['verts'], manifest_quads=man['topology']['quads']),
           semantic=dict(face_semantic_array=C.sha(C.FZ + '/SA_RP5_freeze_candidate_v001_face_semantic.npy'), manifest_face_semantic_array=man['hashes']['face_semantic_array'],
                         semantic_map=C.sha(C.FZ + '/SA_RP5_freeze_candidate_v001_semantic_map.json'), manifest_semantic_map=man['hashes']['semantic_map'],
                         quad_labels_identical_order=bool(np.array_equal(np.asarray(R.ql).astype(str), z0['qlab'].astype(str)))),
           geometry=dict(body_npz_sha256=C.sha(os.path.join(BD, nm + '.npz')), roster_sha256=b['sha256'], body_vertices_sha256=h(Vs), base_vs_frozen_workspace_max_cm=base_geo),
           neutral=dict(max_corrective_cm=float(np.abs(dn).max()), baked_vs_plain_lbs_neutral_cm=float(np.abs(Pn - Pl).max()), plain_lbs_neutral_vs_body_cm=float(np.abs(Pl - Vs).max())),
           ranges=dict(anat=sig(R.suite('anat')), special_gates=sig(GT.gate_poses(R)), rp5_literal=sig(R.suite('rp5'))))
t = out['topology']; s = out['semantic']; g = out['geometry']; n = out['neutral']
out['checks'] = dict(frozen_files=out['frozen_ok'], topology=t['manifest'] == t['frozen_Q'] == t['body_Q'] and t['nv'] == t['manifest_verts'] and t['nq'] == t['manifest_quads'],
                     semantic=s['face_semantic_array'] == s['manifest_face_semantic_array'] and s['semantic_map'] == s['manifest_semantic_map'] and s['quad_labels_identical_order'],
                     geometry=g['body_npz_sha256'] == g['roster_sha256'] and (g['base_vs_frozen_workspace_max_cm'] is None or g['base_vs_frozen_workspace_max_cm'] < 1e-9),
                     neutral=n['max_corrective_cm'] == 0.0 and n['baked_vs_plain_lbs_neutral_cm'] == 0.0 and n['plain_lbs_neutral_vs_body_cm'] < 1e-4)
out['clean'] = all(out['checks'].values())
json.dump(out, open(os.path.join(OD, 'IN_%s.json' % nm), 'w'), indent=1)
print(nm, 'INTEGRITY clean', out['clean'], out['checks'], 'absent:', [f for f, v in files.items() if v.startswith('absent')], flush=True)
