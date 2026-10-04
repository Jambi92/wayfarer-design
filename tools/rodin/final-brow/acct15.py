# final brow/orbit accounting against the accepted convergence (c11/g14)
import numpy as np, igl, json
from PIL import Image
C11='/tmp/claude-0/rodin/c11/'
b0=np.load(C11+'g14_body.npz'); V0=b0['V'].astype(float); F0=b0['F'].astype(np.int64)
c=np.load('g15_body.npz'); V=c['V'].astype(float); F=c['F'].astype(np.int64); org=c['origin']; n=len(V)
k=org>=0; mv=np.zeros(n); mv[k]=np.linalg.norm(V[k]-V0[org[k]],axis=1)
sq,_,_=igl.point_mesh_squared_distance(V[~k],V0,F0); mv[~k]=np.sqrt(sq)
x,f,u=V.T; headbox=(np.abs(x)<16)&(f>-34)&(f<28)&(u>161)
zone=headbox&((~k)|(mv>0))
st=lambda d: dict(verts=int(len(d)),median_mm=round(float(np.median(d))*10,3),p95_mm=round(float(np.percentile(d,95))*10,2),p99_mm=round(float(np.percentile(d,99))*10,2),max_mm=round(float(d.max())*10,2))
A={'base_movement':{'brow/postorbital zone':st(mv[zone]),'outside zone':dict(verts=int((~zone).sum()),max_mm_exact=float(mv[~zone].max()*10))}}
A['zone_extent_world_cm']=dict(f=[round(float(f[zone].min()),2),round(float(f[zone].max()),2)],u=[round(float(u[zone].min()),2),round(float(u[zone].max()),2)],abs_x=[round(float(np.abs(x[zone]).min()),2),round(float(np.abs(x[zone]).max()),2)])
ek=np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1); _,cc=np.unique(ek,axis=0,return_counts=True)
from scipy.sparse.csgraph import connected_components
A['topology']=dict(verts=n,faces=len(F),boundary_edges=int((cc==1).sum()),nonmanifold_edges=int((cc>2).sum()),components=int(connected_components(igl.adjacency_matrix(F))[0]))
A['envelope_cm']={kk:[round(float(np.ptp(V0[:,i])),3),round(float(np.ptp(V[:,i])),3)] for i,kk in enumerate(('width','depth','height'))}
# tail bit-identity: every convergence base vertex behind the pelvis (f < -24, u < 120) must survive with identical coordinates
t0=np.where((V0[:,1]<-24)&(V0[:,2]<120))[0]; inv=-np.ones(len(V0),np.int64); inv[org[k]]=np.where(k)[0]
surv=inv[t0]>=0; same=surv.copy(); same[surv]=(V[inv[t0[surv]]]==V0[t0[surv]]).all(1)
s0=np.load(C11+'g14_surf.npz')['V']; s1=np.load('g15_surf.npz')['V']
tm0=(s0[:,1]<-24)&(s0[:,2]<120); tm1=(s1[:,1]<-24)&(s1[:,2]<120)
a0=np.ascontiguousarray(s0[tm0]).view([('',s0.dtype)]*3).ravel(); a1=np.ascontiguousarray(s1[tm1]).view([('',s1.dtype)]*3).ravel()
A['tail_bit_identity']=dict(base_tail_verts=int(len(t0)),survived=int(surv.sum()),bit_identical=int(same.sum()),
    surface_tail_verts_before=int(tm0.sum()),surface_tail_verts_after=int(tm1.sum()),surface_tail_bit_identical=bool(len(a0)==len(a1) and np.array_equal(np.sort(a0),np.sort(a1))))
sil={}
for v in ('front','profile','rear','front34','rear34'):
    a=np.asarray(Image.open(C11+'Y14_%s.png'%v).convert('RGBA'))[...,3]>127; b=np.asarray(Image.open('Y15_%s.png'%v).convert('RGBA'))[...,3]>127
    sil[v]=dict(pct=round(100*float((a^b).sum())/a.sum(),3),pixels=int((a^b).sum()))
A['silhouette_changed']=sil
r0=np.load(C11+'g14reg.npz'); r1=np.load('g15reg.npz'); ii=np.load('nn15.npy'); dd=np.load('dsurf15.npy')
same=r1['FAM']==r0['FAM'][ii]; A['scale_family_agreement_pct']=round(100*float(same.mean()),4)
A['scale_family_agreement_outside_head_pct']=round(100*float(same[np.asarray(s1[:,2])<160].mean()),4)
A['surface_moved_gt_0p1mm_pct']=round(100*float((dd>0.01).mean()),3)
hs=s1[:,2]>160; A['surface_moved_gt_0p1mm_outside_head_verts']=int(((dd>0.01)&~hs).sum())
json.dump(A,open('acct15.json','w'),indent=1); print(json.dumps(A,indent=1))
