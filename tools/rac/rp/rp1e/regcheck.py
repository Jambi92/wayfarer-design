import sys,numpy as np,igl
p=sys.argv[1]; c=np.array(eval(sys.argv[2])); R=float(sys.argv[3])
S=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float)
z=np.load(p); V=z['V'].astype(float).copy(); V[:,1]*=-1
m=np.linalg.norm(S-c,axis=1)<R; d,_,_=igl.point_mesh_squared_distance(S[m],V,z['F'].astype(np.int64)); d=np.sqrt(d)*10
print('region src->prod max %.2f mm, p95 %.2f, over1.5: %d'%(d.max(),np.percentile(d,95),(d>1.5).sum()))
