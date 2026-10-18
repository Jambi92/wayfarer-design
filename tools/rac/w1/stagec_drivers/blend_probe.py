import bpy, sys, json, collections
p=sys.argv[-1]; bpy.ops.wm.open_mainfile(filepath=p)
res={'file':p,'objects':[]}
for o in bpy.data.objects:
    d={'name':o.name,'type':o.type,'loc':list(o.location),'rot':list(o.rotation_euler),'scale':list(o.scale),'parent':o.parent.name if o.parent else None}
    if o.type=='MESH':
        me=o.data
        d.update(verts=len(me.vertices),edges=len(me.edges),polys=len(me.polygons),poly_sizes=dict(collections.Counter(min(len(q.vertices),5) for q in me.polygons)),
                 uv=[u.name for u in me.uv_layers],materials=[m.name if m else None for m in me.materials],vgroups=[v.name for v in o.vertex_groups][:40],n_vgroups=len(o.vertex_groups),
                 shape_keys=[k.name for k in me.shape_keys.key_blocks] if me.shape_keys else [],modifiers=[m.type for m in o.modifiers],
                 attributes=[a.name for a in me.attributes],color_attrs=[a.name for a in me.color_attributes])
    if o.type=='ARMATURE': d['bones']=len(o.data.bones)
    res['objects'].append(d)
res['scene_unit_scale']=bpy.context.scene.unit_settings.scale_length; res['unit_system']=bpy.context.scene.unit_settings.system
print('BPROBE',json.dumps(res))
