# fitdonor.py : coarse per-height affine fit of the v006 donor's lower body onto the source at the cloth-free boundary heights
import numpy as np, trimesh, json, sys
S=np.load('/tmp/claude-0/src3d/in/front_aligned.npz'); SV=S['V']; SF=S['Q']
D=np.load('/tmp/claude-0/rp2/fin/v006.npz'); DV=D['V'].astype(float); DQ=D['Q']
ZB,ZT=float(sys.argv[1]),float(sys.argv[2])
MS={}
def stats(V,z,half):
    key=id(V)
    if key not in MS:
        F=SF if V is SV else np.r_[DQ[:,[0,1,2]],DQ[:,[0,2,3]]]
        MS[key]=trimesh.Trimesh(V,F,process=False)
    sec=MS[key].section(plane_origin=[0,0,z],plane_normal=[0,0,1]); P3=sec.vertices
    best=None
    for ent in sec.entities:
        pts=P3[ent.points]; cx=pts[:,0].mean()
        if len(pts)<20: continue
        if pts[:,0].min()<-1 and pts[:,0].max()>1: cand=pts[(pts[:,0]*half)>0]   # trunk loop spanning the midline: take this half
        elif cx*half>0 and abs(cx)<21: cand=pts                                  # leg loop on this side
        else: continue
        if best is None or len(cand)>len(best): best=cand
    P=best; return np.array([np.abs(P[:,0]).max(), P[:,1].min(), P[:,1].max(), np.abs(P[:,0]).min()])
def mapping(z):
    out=[]
    for zz in (ZB,ZT):
        s=np.mean([stats(SV,zz,1),stats(SV,zz,-1)],0); d=np.mean([stats(DV,zz,1),stats(DV,zz,-1)],0)
        sx=s[0]/d[0]; sf=(s[2]-s[1])/(d[2]-d[1]); fcs=(s[1]+s[2])/2; fcd=(d[1]+d[2])/2
        out.append((sx,sf,fcs,fcd))
    t=np.clip((z-ZB)/(ZT-ZB),0,1)[:,None]; a=np.array(out[0]); b=np.array(out[1])
    return a*(1-t)+b*t
M=mapping(DV[:,2])
X=DV.copy(); X[:,0]=DV[:,0]*M[:,0]; X[:,1]=(DV[:,1]-M[:,3])*M[:,1]+M[:,2]
np.savez('/tmp/claude-0/src3d/work/donor_coarse.npz',V=X,Q=DQ)
for zz in (ZB,ZT): print(zz,'src',np.mean([stats(SV,zz,1),stats(SV,zz,-1)],0).round(2),'donor',np.mean([stats(DV,zz,1),stats(DV,zz,-1)],0).round(2),'fitted',np.mean([stats(X,zz,1),stats(X,zz,-1)],0).round(2))
