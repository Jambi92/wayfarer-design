import bpy, numpy as np, json, sys
from scipy.spatial import cKDTree
bpy.ops.wm.open_mainfile(filepath=sys.argv[sys.argv.index('--')+1])
R={}
print([(o.name,o.type,len(o.data.vertices) if o.type=='MESH' else 0,len(o.modifiers)) for o in bpy.data.objects])
def arr(o):
    me=o.data; V=np.array([o.matrix_world@v.co for v in me.vertices]); F=[list(p.vertices) for p in me.polygons]; return V,F
# cage
o=bpy.data.objects['Cylinder']; V,F=arr(o); z=np.load('/home/claude/wayfarer-design/reviews/rac-rp1e-evidence/designs/design_v014.npz')
D=z['V']/100; R['cage']=dict(V=len(V),F=len(F),index_max_dev_mm=float(np.abs(V-D).max()*1000) if len(V)==len(D) else None,
  faces_identical=all(list(f)==[int(i) for i in q if i>=0] for f,q in zip(F,z['F'])) and len(F)==len(z['F']), matrix_identity=bool(np.allclose(np.array(o.matrix_world),np.eye(4))))
# production
o=bpy.data.objects['RP1E_production_v014']; V,F=arr(o); p=np.load('/home/claude/wayfarer-design/reviews/rac-rp1e-evidence/designs/design_v014_production_L4.npz')
P=p['V']*np.array([1,-1,1])/100; d,i=cKDTree(V).query(P)
S1=set(tuple(sorted(q)) for q in i[p['Q']].tolist()); S2=set(tuple(sorted(f)) for f in F)
R['production']=dict(V=len(V),F=len(F),max_dev_mm=float(d.max()*1000),bijective=len(np.unique(i))==len(V)==len(P),faces_identical=S1==S2,matrix_identity=bool(np.allclose(np.array(o.matrix_world),np.eye(4))),modifiers=len(o.modifiers))
R['weldsrc_vertices']=len(bpy.data.objects['GO_U_REF_RP1_weldsrc'].data.vertices) if 'GO_U_REF_RP1_weldsrc' in bpy.data.objects else None
json.dump(R,open('/tmp/claude-0/verify_v014.json','w'),indent=1); print(json.dumps(R))
