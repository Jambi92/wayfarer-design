import bpy, bmesh, numpy as np, sys
bpy.ops.wm.open_mainfile(filepath=sys.argv[1]); o=[x for x in bpy.data.objects if x.type=='MESH'][0]
bpy.context.view_layer.objects.active=o; o.select_set(True)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='DESELECT')
o.vertex_groups.active_index=o.vertex_groups['AW1_weld'].index; bpy.ops.object.vertex_group_select()
r=bpy.ops.mesh.remove_doubles(threshold=0.00001); bpy.ops.object.mode_set(mode='OBJECT')
me=o.data; V=np.zeros(len(me.vertices)*3); me.vertices.foreach_get('co',V); V=V.reshape(-1,3)
me.calc_loop_triangles(); T=np.zeros(len(me.loop_triangles)*3,np.int64); me.loop_triangles.foreach_get('vertices',T)
np.savez(sys.argv[2],V=V,F=T.reshape(-1,3)); print('NV',len(V),'NF',len(T)//3)
if len(sys.argv)>3: bpy.ops.wm.save_as_mainfile(filepath=sys.argv[3],compress=True)
