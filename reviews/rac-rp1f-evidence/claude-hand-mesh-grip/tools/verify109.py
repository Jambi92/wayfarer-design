import bpy,sys,numpy as np,json
from scipy.spatial import cKDTree
a=sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.open_mainfile(filepath=a[0]); obs=[o for o in bpy.data.objects if o.type=='MESH']
o=obs[0]; m=o.data
V=np.zeros(len(m.vertices)*3); m.vertices.foreach_get('co',V); V=V.reshape(-1,3)
z=np.load(a[1]); P=z['V']*np.array([1,-1,1])/100; Q=z['Q']
d,i=cKDTree(V).query(P)
nf=len(m.polygons); ls=np.zeros(nf,int); m.polygons.foreach_get('loop_total',ls)
Fb=np.zeros(nf*4,int); m.polygons.foreach_get('vertices',Fb); Fb=Fb.reshape(-1,4)
# faces as sets mapped through i
s1=set(map(lambda q: tuple(sorted(q)), i[Q].tolist())); s2=set(map(lambda q: tuple(sorted(q)), Fb.tolist()))
r=dict(objects=[x.name for x in obs], vertices=len(V), faces=nf, all_quads=bool((ls==4).all()), bijective=bool(len(np.unique(i))==len(P)==len(V)), max_dev_mm=float(d.max()*1000), faces_identical=bool(s1==s2), matrix_identity=bool(np.allclose(np.array(o.matrix_world),np.eye(4))))
print(json.dumps(r)); json.dump(r,open(a[2],'w'),indent=1)
