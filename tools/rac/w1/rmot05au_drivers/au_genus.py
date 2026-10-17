# Topology of the welded AC3 surface: Euler characteristic -> genus; locate the handles by planar section scans. A tunnel through the
# surface shows up as a HOLE (interior ring) in sections cut across it; holes that persist over several parallel planes are clustered.
import json, numpy as np, trimesh
from shapely.geometry import Polygon
V=np.load('/home/claude/at/final/ac3.npz')['V'].astype(float); F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']
z0=V[:,2].min(); H=V[:,2].max()-z0
k,inv=np.unique(np.round(V,7),axis=0,return_inverse=True); inv=inv.ravel(); Fw=inv[F]
Fw=Fw[(Fw[:,0]!=Fw[:,1])&(Fw[:,1]!=Fw[:,2])&(Fw[:,0]!=Fw[:,2])]
E=np.unique(np.sort(np.concatenate([Fw[:,[0,1]],Fw[:,[1,2]],Fw[:,[2,0]]]),1),axis=0)
chi=len(np.unique(Fw))-len(E)+len(Fw); g=(2-chi)//2
print('welded V',len(np.unique(Fw)),'E',len(E),'F',len(Fw),'chi',chi,'genus',g,flush=True)
m=trimesh.Trimesh(k,Fw,process=False)
holes=[]
for axis in range(3):
    lo,hi=k[:,axis].min(),k[:,axis].max(); step=0.004
    for v in np.arange(lo+step,hi,step):
        o=np.zeros(3); o[axis]=v; nrm=np.zeros(3); nrm[axis]=1
        s=m.section(plane_origin=o,plane_normal=nrm)
        if s is None: continue
        p2,T=s.to_2D(to_2D=None) if False else (None,None)
        loops=[s.vertices[e.points] for e in s.entities]
        polys=[]
        for L in loops:
            if len(L)<4: continue
            q=np.delete(L,axis,1)
            try:
                P=Polygon(q)
                if P.is_valid and P.area>0: polys.append((P,L))
            except Exception: pass
        # a loop strictly inside another loop of the same section = a hole in that body cross-section
        for i,(Pi,Li) in enumerate(polys):
            for j,(Pj,Lj) in enumerate(polys):
                if i!=j and Pj.area>Pi.area and Pj.contains(Pi):
                    holes.append(dict(axis='xyz'[axis],pos=Li.mean(0).tolist(),area_cm2=Pi.area*1e4,perim_cm=Pi.length*100)); break
print('hole sections',len(holes),flush=True)
json.dump(dict(chi=int(chi),genus=int(g),holes=holes),open('au_genus_raw.json','w'))
