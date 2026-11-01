# sa_pilot_export.py CAGE.npz SEMANTIC.json FACE_SEM.npy OUTDIR : pilot production files (order 236dddc §16), created ONLY after the internal PASS gate.
#   SA_M_REF_RP5_pilot_v001.blend (c1 SA-M188) / SA_F_REF_RP5_pilot_v001.blend (c2 SA-F188): one mesh, same face list / vertex order, cm (scale 0.01 on the
#   object -> metres in Blender), face attribute 'semantic' (int, table in the object's custom property), landmark empties, status PILOT / NOT FROZEN.
#   Sidecar JSON, barycentric source map (base face id + barycentrics on the canonical face list), semantic map copy, landmarks, read-back verification.
#   Run with the bpy 5.2.2 interpreter (/home/claude/stc/bin/python3).
import sys, os, json, hashlib, numpy as np, bpy
CG, SEM, FSEM, OUT = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:5]; os.makedirs(OUT, exist_ok=True); W = '/tmp/claude-0/rt/sa'
z = np.load(CG); Q = z['Q'].astype(np.int64); fi = z['tri']; bc = z['bc']; w = np.load(W + '/work/SA_RP5_WORK_v001.npz'); F = w['f'].astype(np.int64)
fsem = np.load(FSEM, allow_pickle=True); labs = sorted(set(map(str, fsem))); lid = {l: i for i, l in enumerate(labs)}; fsi = np.array([lid[str(x)] for x in fsem], np.int32)
LM = json.load(open(W + '/lm/SA-M188_landmarks.json'))['landmarks']
topo = hashlib.sha256(np.ascontiguousarray(Q).tobytes()).hexdigest()
res = {}
for tag, key in (('SA_M_REF_RP5_pilot_v001', 'v_M'), ('SA_F_REF_RP5_pilot_v001', 'v_F')):
    V = (bc[:, :, None] * w[key].astype(float)[F[fi]]).sum(1)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    me = bpy.data.meshes.new(tag); me.from_pydata(V.tolist(), [], Q.tolist()); me.update()
    at = me.attributes.new('semantic', 'INT', 'FACE'); at.data.foreach_set('value', fsi.tolist())
    ob = bpy.data.objects.new(tag, me); bpy.context.scene.collection.objects.link(ob); ob.scale = (0.01, 0.01, 0.01)
    ob['status'] = 'PILOT / NOT FROZEN'; ob['units'] = 'cm (object scale 0.01)'; ob['frame'] = 'x right (+x = subject left xpos), y forward, z up'
    ob['semantic_table'] = json.dumps(labs); ob['topology_sha256'] = topo; ob['source'] = 'SA_RP5_WORK_v001 (%s) via barycentric map on the canonical W2I6 face list' % key
    for k, p in (LM.items() if isinstance(LM, dict) else []):
        pp = p['p_cm'] if isinstance(p, dict) and 'p_cm' in p else p
        if key == 'v_F': continue
        e = bpy.data.objects.new('LM_' + k, None); e.location = [c * 0.01 for c in pp]; e.empty_display_size = 0.01; bpy.context.scene.collection.objects.link(e)
    fp = os.path.join(OUT, tag + '.blend'); bpy.ops.wm.save_as_mainfile(filepath=fp)
    # read-back
    bpy.ops.wm.open_mainfile(filepath=fp); ob2 = bpy.data.objects[tag]; me2 = ob2.data
    co = np.zeros(len(me2.vertices) * 3); me2.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    lt = np.zeros(len(me2.polygons) * 4, np.int64); me2.polygons.foreach_get('vertices', lt) if all(len(p.vertices) == 4 for p in me2.polygons) else None
    sv = np.zeros(len(me2.polygons), np.int32); me2.attributes['semantic'].data.foreach_get('value', sv)
    res[tag] = dict(file=os.path.basename(fp), sha256=hashlib.sha256(open(fp, 'rb').read()).hexdigest(), verts=len(me2.vertices), quads=len(me2.polygons),
                    readback_max_vertex_error_cm=float(np.abs(co - V).max()), readback_face_list_identical=bool(np.array_equal(lt.reshape(-1, 4), Q)),
                    readback_semantic_identical=bool(np.array_equal(sv, fsi)), readback_topology_sha256=hashlib.sha256(np.ascontiguousarray(lt.reshape(-1, 4)).tobytes()).hexdigest(),
                    status=ob2['status'])
np.savez_compressed(os.path.join(OUT, 'SA_RP5_pilot_v001_barycentric_map.npz'), base_face=fi, barycentric=bc, face_list_note=np.array('canonical W2I6 base face list (saurin_w2_final_base.npz f)'))
side = dict(asset='Saurin RP5 full authored cage pilot v001', status='PILOT / NOT FROZEN', cage_npz=os.path.basename(CG), cage_sha256=hashlib.sha256(open(CG, 'rb').read()).hexdigest(),
            verts=int(len(z['V'])), quads=int(len(Q)), topology_sha256=topo, shared_topology_c1_c2=True, semantic_labels=labs, files=res,
            barycentric_map='SA_RP5_pilot_v001_barycentric_map.npz', semantic_map=os.path.basename(SEM), tail_module='accepted module unchanged (sha 559565cc...)',
            prohibited_not_done=['freeze', 'rig', 'UV / materials', 'LOD', 'creator implementation', 'UE5'])
json.dump(side, open(os.path.join(OUT, 'SA_RP5_pilot_v001_sidecar.json'), 'w'), indent=1); print(json.dumps(res, indent=1))
