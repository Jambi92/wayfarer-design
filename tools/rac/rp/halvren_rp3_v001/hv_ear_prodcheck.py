# hv_ear_prodcheck.py OUT.json LABEL=BRANCH.npz ... (bpy python) : Halvren HE2 closure order §10 item 10 -- production-readiness regression of ear realizations:
#   mirroring   left vs mirrored right ear (same branch patch indices; x -> -x): max / mean vertex distance (cm) and identical patch connectivity per side
#   export      write the mesh to a .blend (Blender data block), reload, compare V / faces (max abs dV, faces equal)
#   LOD         Decimate (collapse) 50 % and 25 % of the whole mesh; non-manifold edges and zero-area faces inside the ear region after decimation
# Compared like-for-like with the frozen Vael ear parameters realized on the same head (VA-E2-RI3) as the accepted production class.
import sys, os, json, numpy as np, tempfile
import bpy, bmesh
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
OUT = a[0]; items = [x.split('=', 1) for x in a[1:]]; R = {}
def mk(V, Q):
    bpy.ops.wm.read_factory_settings(use_empty=True); me = bpy.data.meshes.new('ear'); me.from_pydata((V / 100).tolist(), [], Q.tolist()); me.update()
    ob = bpy.data.objects.new('ear', me); bpy.context.scene.collection.objects.link(ob); return ob
for lab, p in items:
    z = np.load(p); V = z['V'].astype(float); Q = np.asarray(z['Q']); side = z['side']; part = z['part']; r = {}
    os.environ.setdefault('EAR_TOPO', 'v002'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001'); import ear_branch_lib as E
    ns = len(E.canonical_layout()['st']); l0 = np.nonzero(side == 'l')[0][0]; r0 = np.nonzero(side == 'r')[0][0]
    d = np.linalg.norm(V[l0:l0 + ns] - V[r0:r0 + ns] * np.array([-1, 1, 1]), axis=1)
    def sheetF(o): m = ((Q >= o) & (Q < o + ns)).all(1); return Q[m] - o
    Fl, Fr = sheetF(l0), sheetF(r0); key = lambda F: (lambda S: S[np.lexsort(S.T[::-1])])(np.sort(F, 1))   # orientation-free (the mirrored side winds the other way)
    cl = np.isin(np.arange(len(V)), np.nonzero((side == 'l') & (part == 'cuff'))[0]); cr = (side == 'r') & (part == 'cuff')
    r['mirroring'] = dict(sheet_vertices_per_side=int(ns), sheet_max_cm=round(float(d.max()), 4), sheet_mean_cm=round(float(d.mean()), 4), sheet_connectivity_identical=bool(Fl.shape == Fr.shape and np.array_equal(key(Fl), key(Fr))),
                          cuff_vertices_l_r=[int(cl.sum()), int(cr.sum())], note='sheet (front / back / rim) shares one layout order per side -> mirrored correspondence; the cuff band transitions are canonical PER SIDE (Fenn / Vael cuff canon), as in the frozen elf ears; position differences = per-side root frames on the (slightly asymmetric) family head')
    ob = mk(V, Q); f = os.path.join(tempfile.mkdtemp(), lab + '.blend'); bpy.ops.wm.save_as_mainfile(filepath=f); bpy.ops.wm.open_mainfile(filepath=f)
    me = bpy.data.objects['ear'].data; V2 = np.array([v.co[:] for v in me.vertices]) * 100; F2 = np.array([list(pp.vertices) for pp in me.polygons])
    r['export'] = dict(max_abs_dV_cm=float(np.abs(V2 - V).max()), faces_equal=bool(F2.shape == Q.shape and np.array_equal(F2, Q)), file_bytes=os.path.getsize(f))
    earv = set(np.nonzero(part != 'v005')[0].tolist()); lod = {}
    for ratio in (0.5, 0.25):
        ob = mk(V, Q); vg = ob.vertex_groups.new(name='ear'); vg.add(sorted(earv), 1.0, 'REPLACE')
        md = ob.modifiers.new('dec', 'DECIMATE'); md.ratio = ratio; dg = bpy.context.evaluated_depsgraph_get(); oe = ob.evaluated_get(dg); m2 = oe.to_mesh()
        bm = bmesh.new(); bm.from_mesh(m2); P = np.array([v.co[:] for v in bm.verts]) * 100
        rd = R.get('_ear_bbox') or None; lo, hi = V[sorted(earv)].min(0) - 0.2, V[sorted(earv)].max(0) + 0.2
        inb = lambda co: bool(np.all(co * 100 >= lo) and np.all(co * 100 <= hi))
        nm = sum(1 for e in bm.edges if not e.is_manifold and inb(np.array(e.verts[0].co)))
        za = sum(1 for fc in bm.faces if fc.calc_area() < 1e-10 and inb(np.array(fc.verts[0].co)))
        lod[str(ratio)] = dict(faces=len(bm.faces), ear_region_nonmanifold_edges=nm, ear_region_zero_area_faces=za); bm.free(); oe.to_mesh_clear()
    r['lod_decimate'] = lod; R[lab] = r; print(lab, json.dumps(r)[:600], flush=True)
json.dump(R, open(OUT, 'w'), indent=1)
