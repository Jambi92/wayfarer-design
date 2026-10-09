# RAC W2I5 §13 canonicalization package (built only after the §12 conditions pass): writes the W2 Saurin reference set in the same formats
# as the accepted W1 'final' set (RaceBodies/out conventions), plus hashes. W1 files are never overwritten; the W2 set uses new names.
#   saurin_w2_final_base.npz            {v float32, f int32}  W2 SA-M188 base (W2I3 L1 + F2 rebuild + W2I4 finish + W2I5 thigh sculpt)
#   saurin_w2_final_surface_delta.npz   {d float16}  normal-only scale-surface delta (format of saurin_final_surface_delta.npz)
#   rebuild_w2_final.py                 final surface = igl.upsample(base) + d   (same as rebuild_final.py)
#   saurin_w2_seeds.npy                 the accepted W2I4 seed realization (vertex indices on the upsampled mesh)
#   saurin_w2_SA-F188_realization.npz   §263 female centre on the W2 base (parameter state; traceability)
#   saurin_w2_regfields.npz             carried region labels + recomputed N / T (scratch / hash only: 238 MB)
#   SaurinW2Final.blend / .fbx          preview export exactly as the accepted chain (fast-simplification 0.875 reduction, metres, y = -f)
# Usage: python3 sa_canon5.py OUT.json
import sys, os, json, hashlib, shutil, subprocess, numpy as np, igl
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i4_drivers'))
import sa_sculpt as SC5; import sa_finish as FN
B = FN.B; S = FN.C.S; ST = S + '/w2i5/canon'; os.makedirs(ST, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest(); fsha = lambda f: sha(open(f, 'rb').read())
REBUILD = '''# Rebuild the full-resolution W2 Saurin reference surface (RAC W2I5 canonical W2 reference; W1 'final' set kept as provenance).
# Usage: python rebuild_w2_final.py saurin_w2_final_base.npz saurin_w2_final_surface_delta.npz out.npz [out.obj]
# Needs numpy + libigl (pip install libigl). Units cm; frame x right, f forward, u up.
import sys, numpy as np, igl
b=np.load(sys.argv[1]); V,F=igl.upsample(b['v'].astype(np.float64),b['f'].astype(np.int64))
V=V+np.load(sys.argv[2])['d'].astype(np.float64)
np.savez_compressed(sys.argv[3],v=V.astype(np.float32),f=F.astype(np.int32))
if len(sys.argv)>4:
    with open(sys.argv[4],'w') as o:
        o.write(''.join('v %.5f %.5f %.5f\\n'%tuple(p) for p in V)); o.write(''.join('f %d %d %d\\n'%tuple(t+1) for t in F))
print('final surface:',len(V),'verts',len(F),'tris; height %.2f cm'%np.ptp(V[:,2]))
'''
EXPORT = '''import bpy, numpy as np, sys
for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
z=np.load(sys.argv[-3]); v=z['v'].astype(np.float64)/100.0; f=z['f']
vb=np.stack([v[:,0],-v[:,1],v[:,2]],1).astype(np.float32)
me=bpy.data.meshes.new("SaurinW2Final"); me.vertices.add(len(vb)); me.vertices.foreach_set("co",vb.ravel())
me.loops.add(f.size); me.loops.foreach_set("vertex_index",f.ravel().astype(np.int32)); me.polygons.add(len(f))
me.polygons.foreach_set("loop_start",(np.arange(len(f))*3).astype(np.int32)); me.polygons.foreach_set("loop_total",np.full(len(f),3,np.int32)); me.update(); me.validate(verbose=False)
ob=bpy.data.objects.new("SaurinW2Final",me); bpy.context.scene.collection.objects.link(ob); bpy.context.view_layer.objects.active=ob; ob.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=sys.argv[-2]); bpy.ops.export_scene.fbx(filepath=sys.argv[-1],use_selection=True); print("EXPORT_DONE")
'''
def main():
    out = {'W1_provenance_kept': {}}
    for nm in ('saurin_final_base.npz', 'saurin_final_surface_delta.npz', 'rebuild_final.py', 'SaurinFinal.blend', 'SaurinFinal.fbx'):
        f = '/mnt/attach/outputs/racebodies_v35/' + nm
        if os.path.exists(f): out['W1_provenance_kept'][nm] = fsha(f)
    P = SC5.build_s({})[0].astype(np.float32); F0 = FN.F0.astype(np.int32)
    fb = ST + '/saurin_w2_final_base.npz'; np.savez_compressed(fb, v=P, f=F0)
    Vu, Fu = igl.upsample(P.astype(np.float64), F0.astype(np.int64)); Vu5 = np.load(S + '/w2i5/surf/fin_up.npz')['V'].astype(np.float64)
    d = np.load(S + '/w2i5/surf/saurin_w2i5_surface_delta.npz')['d'].astype(np.float32)
    fd = ST + '/saurin_w2_final_surface_delta.npz'; np.savez_compressed(fd, d=d.astype(np.float16))
    Vs = Vu + np.load(fd)['d'].astype(np.float64)
    fp = ST + '/rebuild_w2_final.py'; open(fp, 'w').write(REBUILD)
    seeds = np.load(S + '/w2i5/surf/fin_seeds.npy').astype(np.int32); fs = ST + '/saurin_w2_seeds.npy'; np.save(fs, seeds)
    Pf = SC5.build_s(B.CEN)[0].astype(np.float32); ff = ST + '/saurin_w2_SA-F188_realization.npz'; np.savez_compressed(ff, v=Pf, f=F0)
    fg = ST + '/saurin_w2_regfields.npz'; shutil.copy(S + '/w2i5/surf/fin_reg.npz', fg)
    import fast_simplification
    Vd, Td = fast_simplification.simplify(Vs.astype(np.float32), Fu, target_reduction=0.875); fdec = ST + '/_dec.npz'; np.savez_compressed(fdec, v=Vd, f=Td.astype(np.int32))
    from scipy.spatial import cKDTree; dev = cKDTree(Vd).query(Vs[::20])[0]
    fe = ST + '/_export.py'; open(fe, 'w').write(EXPORT)
    r = subprocess.run(['python3', fe, fdec, ST + '/SaurinW2Final.blend', ST + '/SaurinW2Final.fbx'], capture_output=True, text=True); assert 'EXPORT_DONE' in r.stdout, r.stdout[-500:] + r.stderr[-500:]
    files = dict(base=fb, surface_delta=fd, rebuild=fp, seeds=fs, female_realization=ff, regfields=fg, blend=ST + '/SaurinW2Final.blend', fbx=ST + '/SaurinW2Final.fbx')
    out['files'] = {k: dict(name=os.path.basename(f), sha256=fsha(f), bytes=os.path.getsize(f)) for k, f in files.items()}
    out['arrays'] = dict(base_v_sha256=sha(P.tobytes()), base_f_sha256=sha(F0.tobytes()), female_v_sha256=sha(Pf.tobytes()), seeds_sha256=sha(seeds.tobytes()),
                         surface_v_sha256=sha(Vs.astype(np.float32).tobytes()), surface_n_vertices=int(len(Vs)), surface_n_faces=int(len(Fu)), surface_height=float(Vs[:, 2].max()))
    out['checks'] = dict(base_height=float(P[:, 2].max()), faces_identical_to_W1=bool(np.array_equal(F0, np.load('/mnt/attach/outputs/racebodies_v35/saurin_final_base.npz')['f'])),
                         upsample_vs_regeneration_max_cm=float(np.abs(Vu - Vu5).max()), float16_delta_quantization_max_cm=float(np.abs(np.load(fd)['d'].astype(np.float64) - d).max()),
                         seeds_identical_to_W2I4=bool(np.array_equal(seeds, np.load(S + '/w2i4/surf/fin_seeds.npy'))),
                         export_vertices=int(len(Vd)), export_triangles=int(len(Td)), export_max_dev_mm=float(dev.max() * 10))
    json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
if __name__ == '__main__': main()
