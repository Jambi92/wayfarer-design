import sys,json,numpy as np
sys.argv=['x']+sys.argv[1:]
exec(open('/home/claude/wayfarer-design/tools/rac/rp/rp1_landmarks_len.py').read().split('S, SF = load')[0])
def segs(V,F,p,n,R):
    d=(V-p)@n; s=np.sign(d[F]); m=(s.min(1)<0)&(s.max(1)>0); T=F[m]; D=d[T]; P=V[T]; pts=[]
    for a,b in ((0,1),(1,2),(2,0)):
        c=D[:,a]*D[:,b]<0; t=np.where(c,D[:,a]/np.where(c,D[:,a]-D[:,b],1),np.nan); pts.append(P[:,a]+(P[:,b]-P[:,a])*t[:,None])
    pts=np.stack(pts,1); ok=~np.isnan(pts[...,0]); k=ok.sum(1)==2; pts=pts[k]; ok=ok[k]
    seg=np.array([q[o][:2] for q,o in zip(pts,ok)]); mid=seg.mean(1); L=np.linalg.norm(seg[:,1]-seg[:,0],axis=1); sel=np.linalg.norm(mid-p,axis=1)<R
    return mid[sel],L[sel]
LM=json.load(open('/home/claude/stc/rp1/landmarks_source.json')); v=LM[sys.argv[3]]
p,n,r=np.array(v['plane_point']),np.array(v['plane_normal']),v['radius_cm']
for f in sys.argv[1:3]:
    V,F=load(f); M,L=segs(V,F,p,n,r)
    for nm,msk in (('x<-25',M[:,0]<-25),('x>=-25',M[:,0]>=-25)):
        print(f.split('/')[-1],nm,'len %.2f'%L[msk].sum(),'cent',((M[msk]*L[msk,None]).sum(0)/L[msk].sum()).round(3))
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial import cKDTree
V,F=load(sys.argv[1]); Ms,Ls=segs(V,F,p,n,r); V,F=load(sys.argv[2]); Mp,Lp=segs(V,F,p,n,r)
idx=np.random.default_rng(0).choice(len(Ms),min(3000,len(Ms)),replace=False); lab=fcluster(linkage(Ms[idx],'single'),1.0,'distance')
T=cKDTree(Ms[idx]); _,i1=T.query(Ms); ls=lab[i1]; _,i2=T.query(Mp); lp=lab[i2]
for k in set(lab):
    a=ls==k; b=lp==k
    if a.sum()<5: continue
    ca=(Ms[a]*Ls[a,None]).sum(0)/Ls[a].sum(); cb=(Mp[b]*Lp[b,None]).sum(0)/Lp[b].sum()
    print('cluster',k,'src len %.1f prod len %.1f'%(Ls[a].sum(),Lp[b].sum()),'cent',ca.round(1),'drift mm %.2f'%(np.linalg.norm(ca-cb)*10))
