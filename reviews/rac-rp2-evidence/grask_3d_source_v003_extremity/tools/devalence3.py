# devalence3.py IN OUT "expr on x,f,z" : remove valence-3 poke vertices (generator tri-fan artefacts) inside a region; their 3 faces become 1
import sys, numpy as np
d=np.load(sys.argv[1]); V=d['V'].astype(float); F=d['Q'].astype(np.int64); n=len(V)
x,f,z=V.T; reg=eval(sys.argv[3])
for it in range(5):
    E=np.unique(np.sort(np.r_[F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]],1),axis=0); deg=np.bincount(E.ravel(),minlength=n)
    vf={}  
    for k,t in enumerate(F):
        for v in t:
            if deg[v]==3 and reg[v]: vf.setdefault(v,[]).append(k)
    kill=np.zeros(len(F),bool); add=[]; used=set(); dev=[]
    for v,fs in vf.items():
        if len(fs)!=3 or any(k in used for k in fs): continue
        # ordered ring from face (v,a,b) orientation
        nxt={}
        for k in fs:
            t=list(F[k]); i=t.index(v); nxt[t[(i+1)%3]]=t[(i+2)%3]
        a=next(iter(nxt)); b=nxt.get(a); c=nxt.get(b) if b is not None else None
        if c is None or nxt.get(c)!=a: continue
        # skip if the triangle (a,b,c) already exists
        add.append((a,b,c)); kill[fs]=True; used.update(fs)
        P=V[[a,b,c]]; nrm=np.cross(P[1]-P[0],P[2]-P[0]); nrm/=np.linalg.norm(nrm); dev.append(abs((V[v]-P[0])@nrm))
    if not add: break
    F=np.r_[F[~kill],np.array(add,np.int64)]
    print('iter',it,'removed',len(add),'max height mm %.3f'%(max(dev)*10))
u=np.unique(F); r=-np.ones(n,int); r[u]=np.arange(len(u)); V2=V[u]; F2=r[F]
Es=np.sort(np.r_[F2[:,[0,1]],F2[:,[1,2]],F2[:,[2,0]]],1); uu,cc=np.unique(Es,axis=0,return_counts=True)
print('V',len(V2),'F',len(F2),'boundary',(cc==1).sum(),'nonmanifold',(cc>2).sum(),'euler',len(V2)-len(uu)+len(F2))
np.savez(sys.argv[2],V=V2,Q=F2)
