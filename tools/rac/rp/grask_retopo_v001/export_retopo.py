# export_retopo.py (bpy) PROD.npz LOOPS.json SEAMS.json META.json OUT.blend : write the RP2 Grask production retopology
# (Blender frame (x,-f,u)/100 m), all quads, with part/zone face attributes, tagged identity loops (vertex groups LOOP_* and
# edge attribute identity_loop) and the UV seam PROPOSAL (edge attribute seam_proposal; no UVs, no seams marked).
import bpy, numpy as np, sys, json, hashlib
a=sys.argv[sys.argv.index('--')+1:]
P=np.load(a[0]); V=P['V'].astype(np.float64); Q=P['Q'].astype(np.int64); FP=P['FP']
loops=json.load(open(a[1])); seams=json.load(open(a[2]))['seams']; meta=json.load(open(a[3]))
sys.path.insert(0,'/tmp/claude-0/rt'); from common import PARTS
Vb=np.c_[V[:,0],-V[:,1],V[:,2]]/100.0
Qb=Q[:,::-1].copy()                     # (x,-f,u) is a reflection: reverse winding to keep outward normals
bpy.ops.wm.read_factory_settings(use_empty=True)
name='GR_U_REF_RP2_retopo_v001'
me=bpy.data.meshes.new(name)
me.vertices.add(len(Vb)); me.vertices.foreach_set('co',Vb.ravel().astype(np.float32))
me.loops.add(Qb.size); me.loops.foreach_set('vertex_index',Qb.ravel().astype(np.int32))
me.polygons.add(len(Qb)); me.polygons.foreach_set('loop_start',np.arange(0,Qb.size,4,dtype=np.int32))
me.update(); bad=me.validate(verbose=False)
co=np.empty(len(me.vertices)*3,np.float32); me.vertices.foreach_get('co',co); co=co.reshape(-1,3).astype(float)
lv=np.empty(len(me.loops),np.int32); me.loops.foreach_get('vertex_index',lv); L4=lv.reshape(-1,4)
T=np.r_[L4[:,[0,1,2]],L4[:,[0,2,3]]]; vol=np.einsum('ij,ij->i',co[T[:,0]],np.cross(co[T[:,1]],co[T[:,2]])).sum()/6
print('validate_changed',bad,'signed volume L',vol*1000,'polys',len(me.polygons),'all quads',all(p.loop_total==4 for p in me.polygons))
assert vol>0
for p in me.polygons: p.use_smooth=True
# face attributes
at=me.attributes.new('rac_part','INT','FACE'); at.data.foreach_set('value',np.asarray(FP,np.int32))
zone_of=lambda n: 'ears' if n.startswith('ear') else 'hands' if n.startswith(('hand','thumb','index','middle','ring','pinky')) else 'feet' if n.startswith(('foot','hallux','toe')) else 'axial_limbs'
ZN=['axial_limbs','ears','hands','feet']; zf=np.array([ZN.index(zone_of(PARTS[p])) for p in FP],np.int32)
at=me.attributes.new('rac_zone','INT','FACE'); at.data.foreach_set('value',zf)
ob=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(ob)
# edges: identity loops + seam proposal
ek={}
eds=np.empty(len(me.edges)*2,np.int32); me.edges.foreach_get('vertices',eds); eds=eds.reshape(-1,2)
for i,(u,v) in enumerate(eds): ek[(min(u,v),max(u,v))]=i
def mark(path,closed,arr):
    n=len(path)
    for i in range(n if closed else n-1):
        u,v=path[i],path[(i+1)%n]; arr[ek[(min(u,v),max(u,v))]]=1
idl=np.zeros(len(eds),np.int32); sem=np.zeros(len(eds),np.int32)
for k,p in loops.items(): mark(p,True,idl)
for k,s in seams.items(): mark(s['verts'],s['kind']=='closed_loop',sem)
at=me.attributes.new('identity_loop','BOOLEAN','EDGE'); at.data.foreach_set('value',idl.astype(bool))
at=me.attributes.new('seam_proposal','BOOLEAN','EDGE'); at.data.foreach_set('value',sem.astype(bool))
for k,p in loops.items():
    g=ob.vertex_groups.new(name='LOOP_'+k); g.add([int(i) for i in p],1.0,'REPLACE')
for k,v in meta.items(): ob['rac_'+k]=v if isinstance(v,(str,int,float)) else json.dumps(v)
bpy.context.scene.unit_settings.system='METRIC'
bpy.ops.wm.save_as_mainfile(filepath=a[4],compress=True)
co2=np.empty(len(me.vertices)*3,np.float32); me.vertices.foreach_get('co',co2)
print('GEOMHASH',hashlib.sha256(co2.tobytes()+lv.astype(np.int32).tobytes()).hexdigest())
print('identity_loop_edges',int(idl.sum()),'seam_edges',int(sem.sum()),'vgroups',len(ob.vertex_groups))
