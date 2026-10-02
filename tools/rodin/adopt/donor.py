# Canonical-frame extraction of a Rodin component (+F forward, U up, ground 0); optional tail-donor tagging.
import numpy as np, sys
z=np.load("/tmp/claude-0/rodin/mesh.npz"); V=z["v"]; Fa=z["f"]; lab=np.load("/tmp/claude-0/rodin/lab.npy")
def canon(cid, facing):
    fs=Fa[lab[Fa[:,0]]==cid]; used=np.unique(fs); rm=-np.ones(len(V),int); rm[used]=np.arange(len(used))
    v=V[used]; f=rm[fs]; P=np.stack([v[:,0],v[:,2],v[:,1]],1); P[:,2]-=P[:,2].min(); H=np.ptp(P[:,2])
    c=P[P[:,2]>0.5*H][:,:2].mean(0); a=np.radians(facing); ca,sa=np.cos(-a),np.sin(-a)
    x=P[:,0]-c[0]; ff=P[:,1]-c[1]; P[:,0],P[:,1]=x*ca+ff*sa,-x*sa+ff*ca
    if P[P[:,2]>0.93*H][:,1].mean()<P[(P[:,2]>0.82*H)&(P[:,2]<0.88*H)][:,1].mean(): P[:,:2]*=-1
    return P,f,H
if __name__=="__main__":
    for cid,fac,nm in ((11,60.0,"b2"),(7,132.0,"b5")):
        P,f,H=canon(cid,fac); F=P[:,1]/H; U=P[:,2]/H
        R=np.zeros(len(P),int)
        if cid==11:
            back=np.percentile(F[(U>0.44)&(U<0.52)&(np.abs(P[:,0]/H)<0.06)&(F>-0.2)],1)
            R[(F<-0.20)&(U<0.56)]=20          # donor free tail (PRESERVE)
            R[(F>=-0.20)&(F<-0.08)&(U<0.56)&(U>0.36)]=21   # B2 tail root: not used (rebuilt)
            print(nm,"posterior pelvis F/H ~",round(float(back),3))
        np.savez(nm+"_canon.npz",P=P,f=f,R=R,H=H)
        print(nm,len(P),"tail-tagged",int((R==20).sum()),"min F/H",round(float(F.min()),3))
