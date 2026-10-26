# freeze_readback.py (bpy) -- BLEND OUT.json OUT.npz ORIGIN.json : read-only freeze read-back (never saves the file)
import bpy, numpy as np, hashlib, json, sys
a=sys.argv[sys.argv.index('--')+1:]
fsha=hashlib.sha256(open(a[0],'rb').read()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=a[0])
obs=[(o.name,o.type) for o in bpy.data.objects]; ob=[o for o in bpy.data.objects if o.type=='MESH'][0]; me=ob.data
co=np.empty(len(me.vertices)*3,np.float32); me.vertices.foreach_get('co',co); lv=np.empty(len(me.loops),np.int32); me.loops.foreach_get('vertex_index',lv)
gh=hashlib.sha256(co.tobytes()+lv.tobytes()).hexdigest()
R=dict(file_sha256=fsha,geometry_hash=gh,objects=obs,armatures=len(bpy.data.armatures),materials=len(bpy.data.materials),
  mesh=dict(name=ob.name,verts=len(me.vertices),polys=len(me.polygons),loops_per_poly=sorted(set(p.loop_total for p in me.polygons)),uv_layers=len(me.uv_layers),
    shape_keys=0 if me.shape_keys is None else len(me.shape_keys.key_blocks),modifiers=[m.type for m in ob.modifiers],vertex_groups=len(ob.vertex_groups),
    attributes=sorted(at.name for at in me.attributes if not at.name.startswith('.')),
    identity_loop_edges=int(sum(d.value for d in me.attributes['identity_loop'].data)),seam_proposal_edges=int(sum(d.value for d in me.attributes['seam_proposal'].data)),
    marked_seams=int(sum(e.use_seam for e in me.edges)),location=list(ob.location),rotation=list(ob.rotation_euler),scale=list(ob.scale),parent=None if ob.parent is None else ob.parent.name,
    custom_props={k:str(ob[k])[:200] for k in ob.keys() if k.startswith('rac_')}))
json.dump(R,open(a[1],'w'),indent=1)
T=np.array(json.load(open(a[3]))['translation_analysis_cm']); c=co.reshape(-1,3).astype(float)
V=np.c_[c[:,0],-c[:,1],c[:,2]]*100-T; fp=np.empty(len(me.polygons),np.int32); me.attributes['rac_part'].data.foreach_get('value',fp)
np.savez(a[2],V=V,Q=lv.reshape(-1,4)[:,::-1].astype(np.int64),FP=fp); print(json.dumps({k:R[k] for k in ('file_sha256','geometry_hash')}))
