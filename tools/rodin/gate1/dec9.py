import bpy, numpy as np, os
for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
z=np.load('/tmp/claude-0/rb/out/saurin_gate6_closed.npz'); v=z['v'].astype(np.float64)/100.0; f=z['f']
vb=np.stack([v[:,0],-v[:,1],v[:,2]],1).astype(np.float32)
me=bpy.data.meshes.new("SaurinGate6_Closed"); me.vertices.add(len(vb)); me.vertices.foreach_set("co",vb.ravel())
me.loops.add(f.size); me.loops.foreach_set("vertex_index",f.ravel().astype(np.int32)); me.polygons.add(len(f))
me.polygons.foreach_set("loop_start",(np.arange(len(f))*3).astype(np.int32)); me.polygons.foreach_set("loop_total",np.full(len(f),3,np.int32)); me.update(); me.validate(verbose=False)
ob=bpy.data.objects.new("SaurinGate6_Closed",me); bpy.context.scene.collection.objects.link(ob); bpy.context.view_layer.objects.active=ob; ob.select_set(True)
m=ob.modifiers.new("dec","DECIMATE"); m.ratio=0.5; m.use_symmetry=False
bpy.ops.object.modifier_apply(modifier="dec")
me=ob.data; print("decimated",len(me.vertices),len(me.polygons))
V=np.zeros(len(me.vertices)*3,np.float32); me.vertices.foreach_get("co",V); V=V.reshape(-1,3)
me.calc_loop_triangles(); T=np.zeros(len(me.loop_triangles)*3,np.int32); me.loop_triangles.foreach_get("vertices",T)
np.savez_compressed('/tmp/claude-0/rb/out/dec9.npz',v=np.stack([V[:,0],-V[:,1],V[:,2]],1)*100.0,f=T.reshape(-1,3))
bpy.ops.wm.save_as_mainfile(filepath="/tmp/claude-0/rb/out/SaurinGate6_Closed.blend")
bpy.ops.export_scene.fbx(filepath="/tmp/claude-0/rb/out/SaurinGate6_Closed.fbx",use_selection=True)
print("DEC_DONE")
