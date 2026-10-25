# shoulder.py : armpit apex A, shoulder-top point T, arm-root plane per side -> shoulder.json
import numpy as np, trimesh, json, sys
sys.path.insert(0,'/tmp/claude-0/rt')
from common import *
V,F=load_src(); m=trimesh.Trimesh(V,F,process=False); L=json.load(open('lm_src.json'))
out={}
for s,sg in (('l',1),('r',-1)):
    last=None
    for z in np.arange(148,160,0.1):
        seg=trimesh.intersections.mesh_plane(m,[0,0,1.0],[0,0,z]); P=seg.reshape(-1,3); P=P[sg*P[:,0]>8]
        # gap: x-values of the contour points near the armpit f-range; find a gap between torso side and arm
        xs=np.sort(sg*P[:,0][(P[:,1]>-14)&(P[:,1]<-2)])
        if len(xs)<4: continue
        gaps=np.diff(xs); i=np.argmax(gaps)
        if gaps[i]>0.25 and 15<xs[i]<24: last=(z,xs[i],xs[i+1])
        else: break
    z,x0,x1=last; fA=np.median(P[:,1][(np.abs(sg*P[:,0]-0.5*(x0+x1))<1.5)&(P[:,1]>-14)&(P[:,1]<-2)]) if False else None
    # f of the gap: centroid of contour points within the gap x-band at that z
    seg=trimesh.intersections.mesh_plane(m,[0,0,1.0],[0,0,z]); P=seg.reshape(-1,3); band=P[(np.abs(sg*P[:,0]-0.5*(x0+x1))<1.0)]
    A=np.array([sg*0.5*(x0+x1),np.median(band[:,1]),z+0.3])
    ac=np.array(L['acromion_'+s]['p']); T=ac+np.array([sg*2.0,0,0])
    d=T-A; n=np.cross(d,[0,1.0,0]); n/=np.linalg.norm(n); n*=np.sign(n[0])*sg
    out[s]=dict(A=A.tolist(),T=T.tolist(),n=n.tolist())
    print(s,'A',np.round(A,2),'T',np.round(T,2),'n',np.round(n,3))
json.dump(out,open('shoulder.json','w'),indent=1)
