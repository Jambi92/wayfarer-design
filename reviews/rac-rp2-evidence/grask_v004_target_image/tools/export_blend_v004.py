# export_blend.py (bpy) -- PROD.npz OUT.blend : write the RP2 production candidate in the Blender frame (x, -f, u) / 100 m.
import bpy, numpy as np, sys, json, hashlib
a=sys.argv[sys.argv.index('--')+1:]; R='/tmp/claude-0/rp2/'
P=np.load(a[0]); V=P['V'].astype(np.float64); Q=P['Q'].astype(np.int64)
Vb=np.c_[V[:,0],-V[:,1],V[:,2]]/100.0
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
me=bpy.data.meshes.new('GR_U_REF_RP2_production_v004')
me.vertices.add(len(Vb)); me.vertices.foreach_set('co',Vb.ravel().astype(np.float32))
me.loops.add(Q.size); me.loops.foreach_set('vertex_index',Q.ravel().astype(np.int32))
me.polygons.add(len(Q)); me.polygons.foreach_set('loop_start',np.arange(0,Q.size,4,dtype=np.int32)); me.update(); me.validate()
# orientation: make outward (positive signed volume in the right-handed Blender frame)
co=np.empty(len(me.vertices)*3,np.float32); me.vertices.foreach_get('co',co); co=co.reshape(-1,3).astype(float)
lv=np.empty(len(me.loops),np.int32); me.loops.foreach_get('vertex_index',lv); F=lv.reshape(-1,4)
def vol(F): T=np.r_[F[:,[0,1,2]],F[:,[0,2,3]]]; return np.einsum('ij,ij->i',co[T[:,0]],np.cross(co[T[:,1]],co[T[:,2]])).sum()/6
if vol(F)<0: me.flip_normals(); me.loops.foreach_get('vertex_index',lv); F=lv.reshape(-1,4)
print('signed volume L', vol(F)*1000)
# mapping back to the shared MPFB hm08 base
mp=np.load(R+'out4/GR_U_REF_RP2_production_v004_mpfb_mapping.npz')
at=me.attributes.new('mpfb_hm08_vertex','INT','POINT'); at.data.foreach_set('value',mp['hm08_vertex'].astype(np.int32))
at=me.attributes.new('rp2_base_vertex','INT','POINT'); at.data.foreach_set('value',mp['base_vertex'].astype(np.int32))
at=me.attributes.new('rp2_base_quad','INT','FACE'); at.data.foreach_set('value',mp['base_quad'].astype(np.int32))
for p in me.polygons: p.use_smooth=True
ob=bpy.data.objects.new('GR_U_REF_RP2_production_v004',me); bpy.context.scene.collection.objects.link(ob)
ob['rac_source']='reviews/reference-assets/r6/GR5DE3_r6.npz sha256 d859eb189ef11881cae2f92ac77414ee630a899d4c1dcf95c0ac78e5a558d778'
ob['rac_status']='RP2 target-image grounded-troll production v004 - BUILD PASS / ready for author review'
ob['rac_frame']='Blender metres, (x, -f, u)/100 of the RAC analysis frame (cm, x=left, f=forward, u=up)'
bpy.context.scene.unit_settings.system='METRIC'
bpy.ops.wm.save_as_mainfile(filepath=a[1],compress=False)
lv=np.empty(len(me.loops),np.int32); me.loops.foreach_get('vertex_index',lv); co=np.empty(len(me.vertices)*3,np.float32); me.vertices.foreach_get('co',co)
print('GEOMHASH', hashlib.sha256(co.tobytes()+lv.astype(np.int32).tobytes()).hexdigest())
