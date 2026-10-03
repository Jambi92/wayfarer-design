# Gate 7 preview export: quadric decimation (fast-simplification) of the 8.96 M-tri surface to ~1.12 M tris, then bpy .blend/.fbx.
import numpy as np, fast_simplification, subprocess, sys, os
if 'bpy' not in sys.modules and not os.environ.get('IN_BPY'):
    z=np.load('/tmp/claude-0/rodin/g1/cur_s7.npz'); P=z['P'].astype(np.float32); F=z['f'].astype(np.int64)
    V,T=fast_simplification.simplify(P,F,target_reduction=0.875); print('decimated',len(V),len(T))
    np.savez_compressed('/tmp/claude-0/rb/out7/dec10.npz',v=V,f=T.astype(np.int32))
    from scipy.spatial import cKDTree; d,_=cKDTree(V).query(P[::20]); print('max dev (vertex sample) mm %.2f'%(d.max()*10))
    os.environ['IN_BPY']='1'; subprocess.run([sys.executable,__file__],check=True); sys.exit()
import bpy
for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
z=np.load('/tmp/claude-0/rb/out7/dec10.npz'); v=z['v'].astype(np.float64)/100.0; f=z['f']
vb=np.stack([v[:,0],-v[:,1],v[:,2]],1).astype(np.float32)
me=bpy.data.meshes.new("SaurinGate7_Surface"); me.vertices.add(len(vb)); me.vertices.foreach_set("co",vb.ravel())
me.loops.add(f.size); me.loops.foreach_set("vertex_index",f.ravel().astype(np.int32)); me.polygons.add(len(f))
me.polygons.foreach_set("loop_start",(np.arange(len(f))*3).astype(np.int32)); me.polygons.foreach_set("loop_total",np.full(len(f),3,np.int32)); me.update(); me.validate(verbose=False)
ob=bpy.data.objects.new("SaurinGate7_Surface",me); bpy.context.scene.collection.objects.link(ob); bpy.context.view_layer.objects.active=ob; ob.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath="/tmp/claude-0/rb/out7/SaurinGate7_Surface.blend")
bpy.ops.export_scene.fbx(filepath="/tmp/claude-0/rb/out7/SaurinGate7_Surface.fbx",use_selection=True)
print("DEC_DONE")
