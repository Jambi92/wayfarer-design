# sa6_common.py : Saurin RP6 rig pilot -- shared loaders (frozen RP5 package only; read-only).
#   Frozen package = reviews/rac-rp5-evidence/saurin/full_cage/final_consolidation (SAURIN_RP5_FREEZE.json). c1 = SA-M188, c2 = SA-F188, cm, x right (+x = subject
#   left = suffix _l), y forward, z up. Geometry = barycentric embedding realised on SA_RP5_WORK_v001 (rebuilt clean workspace SA_W, or the staged scratch copy).
import os, json, pickle, hashlib, numpy as np
R = '/home/claude/wayfarer-design'; FZ = R + '/reviews/rac-rp5-evidence/saurin/full_cage/final_consolidation'
EV6 = R + '/reviews/rac-rp6-evidence/saurin/rig_pilot'; W = os.environ.get('SA_W', '/tmp/claude-0/rp5clean')
FROZEN = {'SA_RP5_full_cage_freeze_candidate_v001.npz': 'ca1c635c1c3c234cc675c2471a31cf9646f95b597c0896b93486cd2b57f99839',
          'SA_M_REF_RP5_freeze_candidate_v001.blend': 'a37cc37723f1a25fed3320c972341883c05e7df30c4f6f44d112746c86880a07',
          'SA_F_REF_RP5_freeze_candidate_v001.blend': 'fd5dad4f3cc5ba598ba0f2198f062c8845f17f1317e948399398bc8e5c6403d7'}
TOPO = '255645a12a8dc59ae8dace55dcf2af2b196a4f5a799fdf425b394b831ffb2d49'
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def check_frozen():
    for f, h in FROZEN.items(): assert sha(FZ + '/' + f) == h, 'frozen RP5 file changed: ' + f
_cache = {}
def load():
    """-> dict(Q, V1, V2, qlab, face_sem, names(per vertex), loops{name: fine vertex list}, LM{name: c1 point}, tail_rings[(idx array)], n_body, tail_ring)"""
    if _cache: return _cache
    check_frozen()
    z = np.load(FZ + '/SA_RP5_full_cage_freeze_candidate_v001.npz'); Q = z['Q'].astype(np.int64); assert hashlib.sha256(np.ascontiguousarray(Q).tobytes()).hexdigest() == TOPO
    w = np.load(W + '/work/SA_RP5_WORK_v001.npz'); F = w['f'].astype(np.int64)
    V1 = (z['bc'][:, :, None] * w['v_M'].astype(float)[F[z['tri']]]).sum(1); V2 = (z['bc'][:, :, None] * w['v_F'].astype(float)[F[z['tri']]]).sum(1)
    assert np.abs(V1 - z['V']).max() < 1e-9
    sem = json.load(open(FZ + '/SA_RP5_freeze_candidate_v001_semantic_map.json')); loops = {l['name']: np.array(l['fine_vertices']) for l in sem['loops']}
    LM = {k: np.array(v['p_cm'], float) for k, v in json.load(open(FZ + '/SA_RP5_freeze_candidate_v001_landmarks_SA-M188.json'))['landmarks'].items()}
    d = pickle.load(open(R + '/reviews/rac-rp5-evidence/saurin/full_cage/optionb_final/SA_coarse_cage_design_optionb_final.pkl', 'rb'))
    names = {n: i for i, n in enumerate(d['name']) if n}
    TM = np.load(R + '/reviews/rac-rp5-evidence/saurin/tail_module/SA_tail_module.npz'); nb = int(z['n_body'])
    mapv = np.r_[z['tail_ring'], nb + np.arange(len(TM['V']) - 128)]
    trings = [mapv[TM['ring_start'][k]:TM['ring_start'][k] + TM['ring_N'][k]] for k in range(len(TM['ring_start']))]
    _cache.update(Q=Q, V1=V1, V2=V2, qlab=z['qlab'].astype(str), face_sem=np.load(FZ + '/SA_RP5_freeze_candidate_v001_face_semantic.npy', allow_pickle=True).astype(str),
                  loops=loops, LM=LM, names=names, tail_rings=trings, n_body=nb, tail_ring=z['tail_ring'])
    return _cache
def side_tag(s): return 'l' if s == 'xpos' else 'r'
