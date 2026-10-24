# export_source.py (bpy) -- SOURCE.npz OUT.blend OUT.glb : write the anatomical source (Blender frame (x,-f,u)/100 m) + GLB copy
import bpy, numpy as np, sys, hashlib
a=sys.argv[sys.argv.index('--')+1:]
P=np.load(a[0]); V=P['V'].astype(np.float64); F=P['Q'].astype(np.int64)
Vb=np.c_[V[:,0],-V[:,1],V[:,2]]/100.0
bpy.ops.wm.read_factory_settings(use_empty=True)
me=bpy.data.meshes.new('GR_U_REF_RP2_SOURCE_3D_v005')
me.vertices.add(len(Vb)); me.vertices.foreach_set('co',Vb.ravel().astype(np.float32))
me.loops.add(F.size); me.loops.foreach_set('vertex_index',F.ravel().astype(np.int32))
me.polygons.add(len(F)); me.polygons.foreach_set('loop_start',np.arange(0,F.size,3,dtype=np.int32)); me.update(); me.validate()
co=np.empty(len(me.vertices)*3,np.float32); me.vertices.foreach_get('co',co); co=co.reshape(-1,3).astype(float)
lv=np.empty(len(me.loops),np.int32); me.loops.foreach_get('vertex_index',lv); T=lv.reshape(-1,3)
vol=np.einsum('ij,ij->i',co[T[:,0]],np.cross(co[T[:,1]],co[T[:,2]])).sum()/6
if vol<0: me.flip_normals(); me.loops.foreach_get('vertex_index',lv); T=lv.reshape(-1,3); vol=-vol
print('signed volume L',vol*1000)
for p in me.polygons: p.use_smooth=True
ob=bpy.data.objects.new('GR_U_REF_RP2_SOURCE_3D_v005',me); bpy.context.scene.collection.objects.link(ob)
ob['rac_status']='RP2 Grask 3D anatomical source v005 extremity naturalization (hands, fingers, toes naturalized from v004) - ready for author freeze review (not a production cage)'
ob['rac_source']='Tyler base.glb (Downloads) sha256 363b4566...ce9 -> left/front-derived figure (157442 V / 314892 tris) = ChatGPT dense extraction 03aed1aa...'
ob['rac_frame']='Blender metres, (x, -f, u)/100 of the RAC analysis frame (cm, x=left, f=forward, u=up); 218 cm; ground z=0'
bpy.context.scene.unit_settings.system='METRIC'
bpy.ops.wm.save_as_mainfile(filepath=a[1],compress=True)
bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active=ob
bpy.ops.export_scene.gltf(filepath=a[2],export_format='GLB',use_selection=True,export_apply=False,export_normals=True,export_materials='NONE')
me.vertices.foreach_get('co',co.reshape(-1).astype(np.float32)) if False else None
co2=np.empty(len(me.vertices)*3,np.float32); me.vertices.foreach_get('co',co2)
print('GEOMHASH',hashlib.sha256(co2.tobytes()+lv.astype(np.int32).tobytes()).hexdigest())
