import sys, numpy as np, bpy
a=sys.argv[sys.argv.index('--')+1:]
z=np.load(a[0]); V=z['V']*np.array([1,-1,1])/100; Q=z['Q']
bpy.ops.wm.read_factory_settings(use_empty=True)
me=bpy.data.meshes.new('m'); me.from_pydata(V.tolist(),[],[list(map(int,q[q>=0])) for q in Q]); me.update()
o=bpy.data.objects.new('m',me); bpy.context.scene.collection.objects.link(o); bpy.context.view_layer.objects.active=o; o.select_set(True)
bpy.ops.object.mode_set(mode='SCULPT')
for t in ['RELAX']:
    try:
        r=bpy.ops.sculpt.mesh_filter(type=t, strength=float(a[2]), iteration_count=int(a[3]) if len(a)>3 else 1)
        print('OP',r)
    except Exception as e: print('ERR',e)
bpy.ops.object.mode_set(mode='OBJECT')
W=np.array([v.co[:] for v in me.vertices])*100; W=np.c_[W[:,0],-W[:,1],W[:,2]]
print('moved max',np.abs(W-z['V']).max())
np.savez_compressed(a[1],V=W,Q=Q,F=z['F'])
