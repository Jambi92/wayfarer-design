import bpy, numpy as np, sys
src,out=sys.argv[1],sys.argv[2]; QC=sys.argv[3]; blend=sys.argv[4] if len(sys.argv)>4 else None
bpy.ops.wm.open_mainfile(filepath=src); o=[x for x in bpy.data.objects if x.type=='MESH'][0]
bpy.context.view_layer.objects.active=o; o.select_set(True)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_mode(type='VERT'); bpy.ops.mesh.select_all(action='DESELECT')
o.vertex_groups.active_index=o.vertex_groups['AW2_subd'].index; bpy.ops.object.vertex_group_select(); print('sel',o.data.total_vert_sel)
bpy.ops.mesh.subdivide(number_cuts=2, smoothness=0, ngon=False, quadcorner=QC)
import bmesh
bpy.ops.mesh.select_mode(type='FACE'); bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.mesh.select_face_by_sides(number=3, type='GREATER'); print('ngons',o.data.total_face_sel)
bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
bpy.ops.object.mode_set(mode='OBJECT'); me=o.data
V=np.zeros(len(me.vertices)*3); me.vertices.foreach_get('co',V); me.calc_loop_triangles(); T=np.zeros(len(me.loop_triangles)*3,np.int64); me.loop_triangles.foreach_get('vertices',T)
np.savez(out,V=V.reshape(-1,3),F=T.reshape(-1,3)); print('NV',len(V)//3,'NT',len(T)//3,'polys',len(me.polygons))
if blend: bpy.ops.wm.save_as_mainfile(filepath=blend)
