# p2s.py PROD.npz : product face-centroid / edge-midpoint samples beyond zone limit (as rp1_gate T-1/T-2 prod->src), blender coords
import sys,numpy as np,igl
p=np.load(sys.argv[1]); V=p['V'].astype(float); F=p['F'].astype(np.int64)
w=np.load('/home/claude/stc/rp1/weld_a.npz'); S=w['V']; SF=w['F'].astype(np.int64); zz=np.load('/home/claude/stc/rp1/zones.npz'); zone=zz['zone']; names=list(zz['names'])
lim=np.array([3.0 if n=='general' else 1.5 for n in names])
Smp=np.vstack([V[F].mean(1),(V[F[:,0]]+V[F[:,1]])/2]); d,I,_=igl.point_mesh_squared_distance(Smp,S,SF); d=np.sqrt(d)*10; z=zone[SF[I,0]]
o=np.where(d>lim[z])[0]; print('over',len(o))
for k in o[np.argsort(-d[o])][:30]: print((Smp[k]*[1,-1,1]).round(2).tolist(),'%.2f'%d[k],names[z[k]])
np.save(sys.argv[1].replace('.npz','_p2s_over.npy'),Smp[o])
