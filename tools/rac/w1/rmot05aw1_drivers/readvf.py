import bpy, numpy as np, sys
bpy.ops.wm.open_mainfile(filepath=sys.argv[1]); o=[x for x in bpy.data.objects if x.type=='MESH'][0]; me=o.data
print('objects',[(x.name,x.type) for x in bpy.data.objects],'mods',[m.name for m in o.modifiers])
V=np.zeros(len(me.vertices)*3); me.vertices.foreach_get('co',V); me.calc_loop_triangles(); T=np.zeros(len(me.loop_triangles)*3,np.int64); me.loop_triangles.foreach_get('vertices',T)
np.savez(sys.argv[2],V=V.reshape(-1,3),F=T.reshape(-1,3)); print('NV',len(V)//3,'NT',len(T)//3)
