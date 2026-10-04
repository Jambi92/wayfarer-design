# Gate 8: anatomical centreline of the frozen Gate 6/7 organism (tail tip -> pelvis -> neck -> snout), in world cm (x, f, u).
import numpy as np
z=np.load('/tmp/claude-0/rodin/g1/g7up.npz'); V=z['V'].astype(float); x,f,u=V.T; ax=np.abs(x)
P=[]
for ff in np.arange(-128,-27,2.0):                       # tail: slices along f
    m=(np.abs(f-ff)<1.0)&(u>35)&(ax<14)
    if m.sum()>50: P.append(V[m].mean(0))
P=P[::-1][::-1]
tail=np.array(P)
T=[]
for uu in np.arange(100,178,2.0):                         # trunk + neck: slices along u, arms and tail excluded
    m=(np.abs(u-uu)<1.0)&(ax<(9 if uu<106 else (13 if uu<146 else 9)))&(f>-24)
    if m.sum()>50: T.append(V[m].mean(0))
trunk=np.array(T)
H=[]
for ff in np.arange(-2,29,1.5):                          # head: slices along f
    m=(np.abs(f-ff)<0.75)&(u>172)&(ax<10)
    if m.sum()>30: H.append(V[m].mean(0))
head=np.array(H)
C=np.concatenate([tail,trunk,head]); C[:,0]=0.0
for _ in range(6): C[1:-1]=0.25*C[:-2]+0.5*C[1:-1]+0.25*C[2:]
seg=np.linalg.norm(np.diff(C,axis=0),axis=1); s=np.concatenate([[0],np.cumsum(seg)])
S=np.arange(0,s[-1],0.5); Cr=np.stack([np.interp(S,s,C[:,k]) for k in range(3)],1)
np.save('axis.npy',Cr); print(len(Cr),'pts, length %.1f cm'%S[-1]); print(Cr[::40].round(1))
