# identical hand/foot crops (same vertex set) from the diagnostic and closure surfaces, world frame
import sys, numpy as np; sys.path.insert(0,'/tmp/claude-0/rodin/g1')
import g7geo as G, hand
B=np.load('g7up.npz'); V=B['V'].astype(np.float64); F=B['F']
S=G.ARM[1]; a,b,c=hand.frame(S['W'],S['E'],1); W=np.asarray(S['W']); Q=V-W
mh=((Q@a)>-3)&(np.linalg.norm(Q,axis=1)<26)&(V[:,0]>24)
mf=(V[:,0]>14.7)&(V[:,0]<32.2)&(V[:,1]>-5)&(V[:,1]<29.2)&(V[:,2]<13)
for src,tag in (('g7_surf.npz','D'),('g7_surfc.npz','C')):
    P=np.load(src)['V']
    for m,nm in ((mh,'hand'),(mf,'foot')):
        fm=m[F].all(1); ff=F[fm]; idx=np.unique(ff); rm=-np.ones(len(V),np.int64); rm[idx]=np.arange(len(idx))
        np.savez('%s8%s.npz'%(nm,tag),P=P[idx],f=rm[ff].astype(np.int32),R=np.zeros(len(idx),np.int8)); print(nm,tag,len(idx))
z=np.load('g7_surfc.npz'); np.savez('cs7c.npz',P=z['V'],f=z['F'],R=np.zeros(len(z['V']),np.int8))
