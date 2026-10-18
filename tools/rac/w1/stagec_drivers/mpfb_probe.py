import sys, json, collections
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/w1')
import arm_lib as A, bpy
cfg=json.load(open('/home/claude/wayfarer-design/reviews/reference-assets/builds/MF-M-R_build.json'))
cfg=cfg.get('cfg',cfg)
body,rig=A.build(cfg)
me=body.data
sizes=collections.Counter(len(p.vertices) for p in me.polygons)
g=A.groups(body); keep=[g['body'].get(i,0)>0.5 for i in range(len(me.vertices))]
bodyp=[p for p in me.polygons if all(keep[i] for i in p.vertices)]
out=dict(verts=len(me.vertices),polys=len(me.polygons),poly_sizes=dict(sizes),body_verts=sum(keep),body_polys=len(bodyp),
 body_poly_sizes=dict(collections.Counter(len(p.vertices) for p in bodyp)),
 uv_layers=[u.name for u in me.uv_layers],materials=[m.name if m else None for m in me.materials],
 vertex_groups=len(body.vertex_groups),vg_sample=[v.name for v in body.vertex_groups][:12],
 shape_keys=(len(me.shape_keys.key_blocks) if me.shape_keys else 0),modifiers=[m.type for m in body.modifiers],
 rig_bones=len(rig.data.bones), rig_name=rig.data.name, objects=[o.name+':'+o.type for o in bpy.data.objects])
print('PROBE',json.dumps(out))
