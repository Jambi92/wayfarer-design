# sa_freeze_candidate_export.py CANDIDATE.npz FACE_SEM.npy SEMANTIC.json OUTDIR : Saurin RP5 freeze-candidate Blender files (order cd87d9c §6).
#   SA_M_REF_RP5_freeze_candidate_v001.blend (c1, SA-M188 working source) / SA_F_REF_RP5_freeze_candidate_v001.blend (c2, SA-F188): ONE mesh object each,
#   no other scene objects, no modifiers / shape keys / constraints / materials / images / libraries / node groups; mesh data in cm exactly as the
#   approved cage (barycentric embedding realised on the rebuilt SA_RP5_WORK_v001), object transform = identity location / rotation and the established
#   pilot unit convention scale 0.01 (cm data -> metres in Blender). Face attribute 'semantic' (INT, table in a custom property). Custom properties carry
#   status FREEZE CANDIDATE / NOT FROZEN and provenance. Read-back is done separately by sa_freeze_candidate_readback.py (fresh Blender process).
#   Run with the bpy 5.2.2 interpreter (/home/claude/stc/bin/python3). Env SA_W = clean consolidation workspace.
import sys, os, json, hashlib, numpy as np, bpy
CG, FSEM, SEM, OUT = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:5]; os.makedirs(OUT, exist_ok=True); W = os.environ.get('SA_W', '/tmp/claude-0/rp5clean')
z = np.load(CG); Q = z['Q'].astype(np.int64); fi = z['tri']; bc = z['bc']; w = np.load(W + '/work/SA_RP5_WORK_v001.npz'); F = w['f'].astype(np.int64)
prov = json.loads(str(z['provenance'])); fsem = np.load(FSEM, allow_pickle=True); labs = sorted(set(map(str, fsem))); lid = {l: i for i, l in enumerate(labs)}
fsi = np.array([lid[str(x)] for x in fsem], np.int32); topo = hashlib.sha256(np.ascontiguousarray(Q).tobytes()).hexdigest()
for tag, key, cfg in (('SA_M_REF_RP5_freeze_candidate_v001', 'v_M', 'c1 SA-M188'), ('SA_F_REF_RP5_freeze_candidate_v001', 'v_F', 'c2 SA-F188')):
    V = (bc[:, :, None] * w[key].astype(float)[F[fi]]).sum(1)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for coll in list(bpy.data.collections): bpy.data.collections.remove(coll)
    me = bpy.data.meshes.new(tag); me.from_pydata(V.tolist(), [], Q.tolist()); me.update(); me.validate(verbose=False)
    at = me.attributes.new('semantic', 'INT', 'FACE'); at.data.foreach_set('value', fsi.tolist())
    ob = bpy.data.objects.new(tag, me); bpy.context.scene.collection.objects.link(ob); ob.scale = (0.01, 0.01, 0.01)
    for k, v in dict(status='FREEZE CANDIDATE / NOT FROZEN', race='Saurin', stage='RP5', configuration=cfg, architecture=prov['architecture'],
                     approved_commit=prov['approved_commit'], approved_cage_sha256=prov['approved_sha256'], candidate_npz='SA_RP5_full_cage_freeze_candidate_v001.npz',
                     topology_sha256=topo, semantic_table=json.dumps(labs), semantic_map=os.path.basename(SEM),
                     units='mesh data in cm; object scale 0.01 (cm -> m), identity location / rotation', frame='x right (+x = subject left, xpos), y forward, z up',
                     source='SA_RP5_WORK_v001 %s via the barycentric map on the canonical W2I6 face list' % key).items(): ob[k] = v
    bpy.context.scene['status'] = 'FREEZE CANDIDATE / NOT FROZEN'
    fp = os.path.join(OUT, tag + '.blend'); bpy.ops.wm.save_as_mainfile(filepath=fp, compress=False)
    print(tag, 'saved', os.path.getsize(fp))
