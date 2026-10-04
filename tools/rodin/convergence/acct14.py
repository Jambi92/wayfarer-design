import numpy as np, igl, json, sys
sys.path.insert(0,'/tmp/claude-0/rodin/p9'); from slicearea import sections
from PIL import Image
C10='/tmp/claude-0/rodin/c10/'
b13=np.load(C10+'g13_body.npz'); V13=b13['V'].astype(float); F13=b13['F'].astype(np.int64)
org=np.load('g14a_body.npz')['origin']; bb=np.load('g14b_body.npz'); keep=bb['KEEP']; WSEAM=bb['WSEAM']
c=np.load('g14_body.npz'); V=c['V'].astype(float); F=c['F'].astype(np.int64); n=len(V)
o=org[keep]; k=o>=0; mv=np.zeros(n); mv[k]=np.linalg.norm(V[k]-V13[o[k]],axis=1)
sq,_,_=igl.point_mesh_squared_distance(V[~k],V13,F13); mv[~k]=np.sqrt(sq)
x,f,u=V.T
lab=np.full(n,'outside',dtype=object)
headbox=(np.abs(x)<16)&(f>-34)&(f<28)&(u>161)
lab[headbox&((~k)|(mv>1e-7))]='orbital/postorbital patch'
lab[(WSEAM>1e-6)]='forearm seam repair'
tailz=(f<-24)&(u>40)&(u<120)&(mv>1e-7)&(lab=='outside')
lab[tailz]='tail mass redistribution'
st=lambda d: dict(verts=int(len(d)),median_mm=round(float(np.median(d))*10,3),p95_mm=round(float(np.percentile(d,95))*10,2),p99_mm=round(float(np.percentile(d,99))*10,2),max_mm=round(float(d.max())*10,2))
A={'base_movement_by_zone':{z:st(mv[lab==z]) for z in sorted(set(lab))}}
ek=np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1); _,cc=np.unique(ek,axis=0,return_counts=True)
nc=igl.connected_components(igl.adjacency_matrix(F))[0] if hasattr(igl,'connected_components') else None
A['topology']=dict(verts=n,faces=len(F),boundary_edges=int((cc==1).sum()),nonmanifold_edges=int((cc>2).sum()),components=int(nc) if nc is not None else None)
A['envelope_cm']={kk:[round(float(np.ptp(V13[:,i])),2),round(float(np.ptp(V[:,i])),2)] for i,kk in enumerate(('width','depth','height'))}
tip0=V13[np.argmin(V13[:,1])]; tip1=V[np.argmin(V[:,1])]; A['tail_tip_shift_cm']=round(float(np.linalg.norm(tip1-tip0)),4)
C=np.load('/tmp/claude-0/rodin/g8/axis.npy'); ST=np.arange(2,214)
s0=sections(V13,F13,C,ST); s1=sections(V,F,C,ST); np.save('sl13.npy',s0); np.save('sl14.npy',s1)
ok=~np.isnan(s0[:,1])&~np.isnan(s1[:,1]); m=ok&(s0[:,0]>=12)&(s0[:,0]<=98)
def rate(s):
    x=s[m,0]; a=s[m,1]; return np.diff(a)/np.diff(x)
A['tail']=dict(volume_s12_98_before=round(float(np.trapz(s0[m,1],s0[m,0])),0),volume_s12_98_after=round(float(np.trapz(s1[m,1],s1[m,0])),0),
  peak_dAds_before=round(float(np.percentile(rate(s0),99)),2),peak_dAds_after=round(float(np.percentile(rate(s1),99)),2),
  root_area_s100_before=round(float(np.interp(100,s0[ok,0],s0[ok,1])),1),root_area_s100_after=round(float(np.interp(100,s1[ok,0],s1[ok,1])),1),
  tip_area_s8_before=round(float(np.interp(8,s0[ok,0],s0[ok,1])),2),tip_area_s8_after=round(float(np.interp(8,s1[ok,0],s1[ok,1])),2))
# normalized table
tab=[]
for q in (0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9):
    s=12+q*(98-12); tab.append(dict(norm_from_tip=q,s_cm=round(s,1),area_before=round(float(np.interp(s,s0[ok,0],s0[ok,1])),1),area_after=round(float(np.interp(s,s1[ok,0],s1[ok,1])),1)))
A['tail_table']=tab
sil={}
for v in ('front','profile','rear','front34','rear34'):
    a=np.asarray(Image.open('Y13_%s.png'%v).convert('RGBA'))[...,3]>127; b=np.asarray(Image.open('Y14_%s.png'%v).convert('RGBA'))[...,3]>127
    sil[v]=round(100*float((a^b).sum())/a.sum(),3)
A['silhouette_changed_pct']=sil
r0=np.load(C10+'g13reg.npz'); r1=np.load('g14reg.npz'); ii=np.load('nn14.npy'); dd=np.load('dsurf14.npy')
same=r1['FAM']==r0['FAM'][ii]; A['scale_family_agreement_pct']=round(100*float(same.mean()),3)
R0=r0['R'][ii].astype(float); R1=r1['R'].astype(float); A['structural_scale_size_cm']=dict(fine_p50=round(float(np.median(R1[r1['FAM']!=1])),2),structural_p50_before=round(float(np.median(R0[r1['FAM']==1])),2),structural_p50_after=round(float(np.median(R1[r1['FAM']==1])),2),structural_p99_after=round(float(np.percentile(R1[r1['FAM']==1],99)),2))
A['surface_moved_gt_0p1mm_pct']=round(100*float((dd>0.01).mean()),2)
json.dump(A,open('acct14.json','w'),indent=1); print(json.dumps(A,indent=1))
