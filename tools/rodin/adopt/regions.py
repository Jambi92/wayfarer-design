# B1 (c12) canonical frame + correction-zone classification (analysis only; geometry untouched)
import numpy as np, json
z=np.load("/tmp/claude-0/rodin/mesh.npz"); V=z["v"]; Fa=z["f"]; lab=np.load("/tmp/claude-0/rodin/lab.npy")
CID=12
fs=Fa[lab[Fa[:,0]]==CID]; used=np.unique(fs); rm=-np.ones(len(V),int); rm[used]=np.arange(len(used))
v=V[used]; f=rm[fs]
P=np.stack([v[:,0],v[:,2],v[:,1]],1)              # x, f(objZ), u(objY)  (same frame as measure.py)
u0=P[:,2].min(); H=np.ptp(P[:,2]); P[:,2]-=u0
up=P[P[:,2]>0.5*H]; c=up[:,:2].mean(0)
ang=np.radians(-4.0); ca,sa=np.cos(-ang),np.sin(-ang)
x=P[:,0]-c[0]; ff=P[:,1]-c[1]; P[:,0],P[:,1]=x*ca+ff*sa,-x*sa+ff*ca
hd=P[P[:,2]>0.93*H]; nk=P[(P[:,2]>0.82*H)&(P[:,2]<0.88*H)]
if hd[:,1].mean()<nk[:,1].mean(): P[:,1]*=-1; P[:,0]*=-1      # +F forward
X,F,U=P[:,0]/H,P[:,1]/H,P[:,2]/H; ax=np.abs(X)
# torso midline f per height (median of |x|<0.05)
def cf_at(u):
    m=(np.abs(U-u)<0.01)&(ax<0.05)
    return (0.5*(F[m].min()+F[m].max()),F[m].max()-F[m].min()) if m.sum()>20 else (0.0,0.15)
gu=np.arange(0,1.01,0.02); cd=np.array([cf_at(u) for u in gu])
CF=np.interp(U,gu,cd[:,0]); DP=np.interp(U,gu,cd[:,1])
R=np.zeros(len(U),int)
arm=((U>0.40)&(U<0.80)&(ax>0.118))|((U>0.18)&(U<=0.40)&(ax>0.15))
R[:]=13                                            # default: thigh/leg PRESERVE, refined below
R[U>0.905]=1
R[(U>0.80)&(U<=0.905)]=2
R[(U>0.70)&(U<=0.82)&(ax>0.075)]=3
R[arm]=4
torso=(~arm)&(U>0.50)&(U<=0.80)&~((U>0.70)&(ax>0.075))
R[torso]=5
R[torso&(U>0.62)&(F>CF+0.22*DP)]=6
R[torso&(U>0.50)&(U<=0.62)&(F>CF+0.22*DP)]=7
R[torso&(U<=0.62)&(R==5)]=8
R[(~arm)&(U>0.48)&(U<0.88)&(ax<0.022)&(F<CF-0.36*DP)]=9
pel=(~arm)&(U>0.40)&(U<=0.50)
R[pel]=12
R[(~arm)&(U>0.415)&(U<=0.60)&(F<CF-0.08*DP)&(ax<0.135)&(R!=9)]=10
R[(~arm)&(U>0.405)&(U<=0.50)&(ax<0.045)&(F>CF)]=11
R[(~arm)&(U<=0.40)&(U>0.06)]=14
R[U<=0.06]=15
# thin-sheet generation artifacts on the legs (shape-diameter test: opposite-facing surface within 0.012H)
from scipy.spatial import cKDTree
nrm=np.zeros_like(P); fn=np.cross(P[f[:,1]]-P[f[:,0]],P[f[:,2]]-P[f[:,0]])
for k in range(3): np.add.at(nrm,f[:,k],fn)
nrm/=np.linalg.norm(nrm,axis=1,keepdims=True)+1e-12
legs=np.where((U<0.42)&(U>0.07)&(R==14))[0]
d,idx=cKDTree(P[legs]).query(P[legs],k=40); nb=legs[idx]
dd=np.where((nrm[nb]*nrm[legs][:,None,:]).sum(-1)<-0.3,d,np.inf).min(1)/H
thin=legs[dd<0.012]
ART=[]
for sgn in (-1,1):
    t=thin[np.sign(X[thin])==sgn]
    if len(t)<10: continue
    c0=P[t].mean(0)/H; ART.append(c0.tolist())
    R[(np.linalg.norm(P/H-c0,axis=1)<0.045)&(R==14)]=16
print("leg artifacts (x,f,u)/H:",np.round(ART,3).tolist())
np.savez("b1_regions.npz",v=v,f=f,P=P,R=R,H=H)
print({int(k):int((R==k).sum()) for k in np.unique(R)})
