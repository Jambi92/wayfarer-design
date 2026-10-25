import bpy, numpy as np, sys, hashlib
a=sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.open_mainfile(filepath=a[0]); obs=[o for o in bpy.data.objects]; ob=obs[0]; me=ob.data
co=np.empty(len(me.vertices)*3,np.float32); me.vertices.foreach_get('co',co); lv=np.empty(len(me.loops),np.int32); me.loops.foreach_get('vertex_index',lv)
P=np.load(a[1]); V=P['V']; Vb=np.c_[co.reshape(-1,3)[:,0],-co.reshape(-1,3)[:,1],co.reshape(-1,3)[:,2]]*100
print('objects',[(o.name,o.type) for o in obs],'verts',len(me.vertices),'polys',len(me.polygons),'loops/poly',set(p.loop_total for p in me.polygons))
print('max pos diff cm',np.abs(Vb-V).max(),'loc',tuple(ob.location),'rot',tuple(ob.rotation_euler),'scale',tuple(ob.scale),'dims m',tuple(round(d,4) for d in ob.dimensions))
print('attrs',[at.name for at in me.attributes],'vgroups',len(ob.vertex_groups),'uv layers',len(me.uv_layers))
print('GEOMHASH',hashlib.sha256(co.tobytes()+lv.tobytes()).hexdigest()); print('FILESHA',hashlib.sha256(open(a[0],'rb').read()).hexdigest())
