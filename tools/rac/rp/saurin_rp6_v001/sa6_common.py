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
def have_workspace(): return os.path.exists(W + '/work/SA_RP5_WORK_v001.npz')
def frozen_blend_coords(c):
    """vertex array (cm, object space) of the frozen SA_<c>_REF_RP5 .blend; cached as npy keyed by the frozen file sha (extracted with bpy 5.2.2)."""
    f = 'SA_%s_REF_RP5_freeze_candidate_v001.blend' % c; cp = '/tmp/claude-0/rp6/blend_co_%s_%s.npy' % (c, FROZEN[f][:12])
    if not os.path.exists(cp):
        import subprocess; os.makedirs(os.path.dirname(cp), exist_ok=True)
        code = ("import bpy,numpy as np;bpy.ops.wm.open_mainfile(filepath=%r);me=[o for o in bpy.data.objects if o.type=='MESH'][0].data;"
                "a=np.zeros(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',a);np.save(%r,a.reshape(-1,3))") % (FZ + '/' + f, cp)
        subprocess.run(['/home/claude/stc/bin/python3', '-c', code], check=True, capture_output=True)
    return np.load(cp)
_cache = {}
def load():
    """-> dict(Q, V1, V2, qlab, face_sem, names(per vertex), loops{name: fine vertex list}, LM{name: c1 point}, tail_rings[(idx array)], n_body, tail_ring)"""
    if _cache: return _cache
    check_frozen()
    z = np.load(FZ + '/SA_RP5_full_cage_freeze_candidate_v001.npz'); Q = z['Q'].astype(np.int64); assert hashlib.sha256(np.ascontiguousarray(Q).tobytes()).hexdigest() == TOPO
    if os.path.exists(W + '/work/SA_RP5_WORK_v001.npz'):
        w = np.load(W + '/work/SA_RP5_WORK_v001.npz'); F = w['f'].astype(np.int64)
        V1 = (z['bc'][:, :, None] * w['v_M'].astype(float)[F[z['tri']]]).sum(1); V2 = (z['bc'][:, :, None] * w['v_F'].astype(float)[F[z['tri']]]).sum(1)
        assert np.abs(V1 - z['V']).max() < 1e-9
    else:   # cage-only mode (clean workspace not staged): c1 = frozen npz V; c2 = the frozen SA-F188 .blend vertex array (float32 cm, readback err < 1e-5 cm)
        V1 = z['V'].astype(float); V2 = frozen_blend_coords('F').astype(float)
        assert np.abs(frozen_blend_coords('M') - V1).max() < 1e-5
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
_dig = {}
def digit_components():
    """per digit: the vertices of its own authored digit quads + its claw cap (one mesh component per digit of the {finger|toe|thumb, claw cap} quad set),
    identified by the nearest base ring (fingers / toes: <side>_<f|t>k_base; thumb: <side>_th_r1).  Topology-only (c1 positions only used to name the
    components; identical on c2).  -> {(side, 'f'|'t'|'th', k): vertex index array}"""
    if _dig: return _dig
    import scipy.sparse as sp
    from scipy.sparse.csgraph import connected_components
    d = load(); Q = d['Q']; fs = d['face_sem']; V = d['V1']; nv = len(V)
    for lab, pre, ks in (('toe', 't', range(1, 6)), ('finger', 'f', range(1, 5)), ('thumb', 'th', [0])):
        qm = np.isin(fs, (lab, 'claw cap')); qq = Q[qm]; fq = fs[qm]; rr = np.repeat(np.arange(len(qq)), 4)
        Aq = sp.coo_matrix((np.ones(len(rr)), (rr, qq.ravel())), shape=(len(qq), nv)).tocsr(); nc, lq = connected_components(Aq @ Aq.T)
        comps = [np.unique(qq[lq == c]) for c in range(nc) if (lq == c).sum() > 300 and (fq[lq == c] == lab).any()]
        for s_ in ('xpos', 'xneg'):
            for k in ks:
                lp = ('%s_th_r1' % s_) if pre == 'th' else ('%s_%s%d_base' % (s_, pre, k)); cen = V[d['loops'][lp]].mean(0)
                dist = [np.linalg.norm(V[c] - cen, axis=1).min() for c in comps]; j = int(np.argmin(dist)); assert dist[j] < 3.0, (lp, dist[j])
                _dig[(s_, pre, k)] = comps[j]
    return _dig
