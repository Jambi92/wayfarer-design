# jawrings2.py CAGE COL OUT spec.json : rows with anchors. spec = [{"ring":json,"end":"a"|"b","z":z,"anchors":{k:[x,y] or "auto-..."}}]
import numpy as np, sys, json
from earsl import slice_loops
cg,colf,out,spec=sys.argv[1:5]; SP=json.load(open(spec))
z=np.load(cg); V=z['V'].copy(); F=z['F']
def outline(zz):
    L=slice_loops(2,zz); return max([P for P,c in L if c],key=lambda P:np.ptp(P[:,0])*np.ptp(P[:,1]))
def ar(Q): return 0.5*np.sum(Q[:,0]*np.roll(Q[:,1],-1)-np.roll(Q[:,0],-1)*Q[:,1])
for row in SP:
    R=json.load(open(row['ring']))['rungs'][:-1]; ring=[a if row['end']=='a' else b for a,b in R]; N=len(ring)
    P=outline(row['z']); cur=V[ring]
    if np.sign(ar(P))!=np.sign(ar(cur)): P=P[::-1]
    j0=int(np.argmin(cur[:,1]+5*abs(cur[:,0]-2))); ring=[ring[(j0+k)%N] for k in range(N)]
    # outline arc param
    Q=np.vstack([P,P[:1]]); L=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]; T=L[-1]
    anc={int(k):np.array(v) for k,v in row['anchors'].items()}
    if 0 not in anc: anc[0]=np.array([2.0,-80.0])
    s={k:L[int(np.argmin(np.linalg.norm(P[:,:2]-v,axis=1)))] for k,v in anc.items()}
    ks=sorted(s); s0=s[0]
    u={k:(s[k]-s0)%T for k in ks}
    # make monotone
    ks=sorted(ks); vals=[u[k] for k in ks]
    assert all(np.diff(vals)>0), ('non-monotone anchors',row['z'],list(zip(ks,np.round(vals,1))))
    ks2=ks+[N]; vals2=vals+[T]
    pos=[]
    for k in range(N):
        i=np.searchsorted(ks2,k,side='right')-1; ka,kb=ks2[i],ks2[i+1]; ua,ub=vals2[i],vals2[i+1]
        sv=(s0+ua+(ub-ua)*(k-ka)/(kb-ka))%T
        m=int(np.clip(np.searchsorted(L,sv),1,len(L)-1)); al=(sv-L[m-1])/max(L[m]-L[m-1],1e-12); pos.append(Q[m-1]+(Q[m]-Q[m-1])*al)
    for k in range(N): V[ring[k]]=pos[k]
    print('z',row['z'],'anchors',{k:np.round(V[ring[k]][:2],1).tolist() for k in ks})
np.savez_compressed(out,V=V,F=F); np.save(out.replace('.npz','_col.npy'),np.load(colf))
