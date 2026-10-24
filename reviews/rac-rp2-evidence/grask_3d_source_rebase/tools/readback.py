import bpy, numpy as np, sys
a=sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.open_mainfile(filepath=a[0]); print('objects',[(o.name,o.type) for o in bpy.data.objects])
me=bpy.data.objects[0].data; co=np.empty(len(me.vertices)*3,np.float32); me.vertices.foreach_get('co',co); co=co.reshape(-1,3).astype(float)
lv=np.empty(len(me.loops),np.int32); me.loops.foreach_get('vertex_index',lv)
V=np.c_[co[:,0],-co[:,1],co[:,2]]*100; np.savez(a[1],V=V,Q=lv.reshape(-1,3))
