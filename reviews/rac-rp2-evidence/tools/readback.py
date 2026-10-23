import bpy, numpy as np, sys
a=sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.open_mainfile(filepath=a[0]); obs=[o for o in bpy.data.objects]; print('objects',[(o.name,o.type) for o in obs])
me=bpy.data.objects['GR_U_REF_RP2_production_v001'].data; print('mw identity', np.allclose(np.array(bpy.data.objects[0].matrix_world),np.eye(4)))
co=np.empty(len(me.vertices)*3,np.float32); me.vertices.foreach_get('co',co); co=co.reshape(-1,3).astype(float)
lv=np.empty(len(me.loops),np.int32); me.loops.foreach_get('vertex_index',lv)
ls=np.empty(len(me.polygons),np.int32); me.polygons.foreach_get('loop_total',ls); print('all quads', (ls==4).all(), 'attrs',[x.name for x in me.attributes])
V=np.c_[co[:,0],-co[:,1],co[:,2]]*100; Q=lv.reshape(-1,4)
np.savez(a[1],V=V,Q=lv.reshape(-1,4))
