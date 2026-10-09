# RAC W2I4 §15 canonicalization PREP (no overwrite): writes the exact candidate files to $S/w2i4/canon_stage and reports SHA-256 of each file
# and of the arrays, beside the frozen references (kept as W1 / W2I provenance):
#   saurin_w2i4_base.npz           {v, f}  finished SA-M188 base (L1 + F2 rebuild + W2I4 finish), same format / topology as saurin_final_base.npz
#   saurin_w2i4_surface_relief.npz {s, seeds}  scalar normal relief per upsampled vertex (float32) + the scale seed vertex indices
#   saurin_w2i4_surface_delta.npz  {d}  normal-only delta, same format as saurin_final_surface_delta.npz (large; produced, hashed, staged only
#                                       if within the transfer limit)
#   rebuild_w2i4.py                       final surface = igl.upsample(base) + s * per-vertex normals (or + d)
#   saurin_w2i4_SA-F188_realization.npz {v, f}  the §263 female centre realized on the finished base (a parameter state; for traceability)
#   saurin_w2i4_regfields.npz      carried g15reg fields with the recomputed N / T (input of the regeneration)
# Usage: python3 sa_canon_prep.py OUT.json
import sys, os, json, hashlib, shutil, numpy as np, igl
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import sa_finish as FN
B = FN.B; S = FN.C.S; ST = S + '/w2i4/canon_stage'; os.makedirs(ST, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest(); fsha = lambda f: sha(open(f, 'rb').read())
REBUILD = '''# Saurin W2I4 final surface (candidate). final = igl.upsample(base) + s[:, None] * per_vertex_normals(upsampled base)
import sys, numpy as np, igl
b = np.load(sys.argv[1]); s = np.load(sys.argv[2])['s'].astype(np.float64)
V, F = igl.upsample(b['v'].astype(np.float64), b['f'].astype(np.int64)); V = V + s[:, None] * igl.per_vertex_normals(V, F)
np.savez_compressed(sys.argv[3], v=V.astype(np.float32), f=F.astype(np.int32)); print('final surface', V.shape, 'height %.3f' % V[:, 2].max())
'''
def main():
    out = {'frozen_provenance': {}}
    for nm in ('saurin_final_base.npz', 'saurin_final_surface_delta.npz', 'rebuild_final.py'):
        f = '/mnt/attach/outputs/racebodies_v35/' + nm
        if os.path.exists(f): out['frozen_provenance'][nm] = fsha(f)
    P = FN.build_f({})[0].astype(np.float32); F0 = FN.F0.astype(np.int32)
    fb = ST + '/saurin_w2i4_base.npz'; np.savez_compressed(fb, v=P, f=F0)
    out['saurin_w2i4_base.npz'] = dict(file_sha256=fsha(fb), v_sha256=sha(P.tobytes()), f_sha256=sha(F0.tobytes()), n_vertices=int(len(P)), height=float(P[:, 2].max()), bytes=os.path.getsize(fb),
                                       f_identical_to_frozen=bool(np.array_equal(F0, np.load('/mnt/attach/outputs/racebodies_v35/saurin_final_base.npz')['f'].astype(np.int32))))
    Vu = np.load(S + '/w2i4/surf/fin_up.npz')['V'].astype(np.float64); Fu = np.load(S + '/w2i4/surf/fin_up.npz')['F'].astype(np.int64)
    Vu2, _ = igl.upsample(P.astype(np.float64), F0.astype(np.int64)); out['upsample_check_max_cm'] = float(np.abs(Vu2 - Vu).max())
    d = np.load(S + '/w2i4/surf/saurin_w2i4_surface_delta.npz')['d'].astype(np.float32); s = (d.astype(np.float64) * igl.per_vertex_normals(Vu2, Fu)).sum(1).astype(np.float32)
    seeds = np.load(S + '/w2i4/surf/fin_seeds.npy').astype(np.int32)
    fr = ST + '/saurin_w2i4_surface_relief.npz'; np.savez_compressed(fr, s=s, seeds=seeds)
    fd = ST + '/saurin_w2i4_surface_delta.npz'; np.savez_compressed(fd, d=d)
    fp = ST + '/rebuild_w2i4.py'; open(fp, 'w').write(REBUILD)
    rec = Vu2 + s[:, None].astype(np.float64) * igl.per_vertex_normals(Vu2, Fu); out['relief_vs_delta_reconstruction_max_cm'] = float(np.abs(rec - (Vu2 + d)).max())
    for nm, f in (('saurin_w2i4_surface_relief.npz', fr), ('saurin_w2i4_surface_delta.npz', fd), ('rebuild_w2i4.py', fp)): out[nm] = dict(file_sha256=fsha(f), bytes=os.path.getsize(f))
    out['saurin_w2i4_surface_relief.npz'].update(s_sha256=sha(s.tobytes()), n_seeds=int(len(seeds)))
    out['final_surface'] = dict(v_sha256=sha((Vu2 + d).astype(np.float32).tobytes()), n_vertices=int(len(Vu2)), n_faces=int(len(Fu)), height=float((Vu2 + d)[:, 2].max()))
    Pf = FN.build_f(B.CEN)[0].astype(np.float32); ff = ST + '/saurin_w2i4_SA-F188_realization.npz'; np.savez_compressed(ff, v=Pf, f=F0)
    out['saurin_w2i4_SA-F188_realization.npz'] = dict(file_sha256=fsha(ff), v_sha256=sha(Pf.tobytes()), height=float(Pf[:, 2].max()), bytes=os.path.getsize(ff))
    fg = ST + '/saurin_w2i4_regfields.npz'; shutil.copy(S + '/w2i4/surf/fin_reg.npz', fg); out['saurin_w2i4_regfields.npz'] = dict(file_sha256=fsha(fg), bytes=os.path.getsize(fg))
    fdel = S + '/w2i4/finish_delta.npz'; out['finish_delta.npz'] = dict(file_sha256=fsha(fdel), bytes=os.path.getsize(fdel))
    json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
if __name__ == '__main__': main()
