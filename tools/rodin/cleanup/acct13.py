import numpy as np, igl, json, sys
sys.path.insert(0,'/tmp/claude-0/rodin/c10'); sys.path.insert(0,'/tmp/claude-0/rodin/p9')
from zones import zones
P9='/tmp/claude-0/rodin/p9/'
b12=np.load(P9+'g12_body.npz'); V12=b12['V'].astype(float); F12=b12['F'].astype(np.int64)
a=np.load('g13a_body.npz'); org=a['origin']; b=np.load('g13b_body.npz'); keep=b['KEEP']; WSEAM=b['WSEAM']
c=np.load('g13_body.npz'); V=c['V'].astype(float); F=c['F'].astype(np.int64); WB=c['WB']; n=len(V)
o=org[keep]
mv=np.full(n,np.nan); k=o>=0; mv[k]=np.linalg.norm(V[k]-V12[o[k]],axis=1)
sq,_,_=igl.point_mesh_squared_distance(V[~k],V12,F12); mv[~k]=np.sqrt(sq)       # re-meshed postorbital patch: distance to the old surface
N=igl.per_vertex_normals(V,F); Z=zones(b['V'].astype(float),igl.per_vertex_normals(b['V'].astype(float),F))
x,f,u=V.T
headpatch=(np.abs(x)<16)&(f>-34)&(f<28)&(u>161)&(~k|(mv>1e-6))&(WB<0.01)
lab=np.full(n,'outside',dtype=object)
lab[headpatch]='postorbital/brow patch'
for kz in Z: lab[(Z[kz]>0.01)&(lab=='outside')]=kz
lab[(WB>0.01)&(lab=='outside')]='head-neck splice band'
lab[(WSEAM>0.01)&(lab=='outside')]='ankle seam repair'
WZ=c['WZ']; from scipy.spatial import cKDTree
fe=(lab=='outside')&((WZ>1e-6)|(WB>1e-6)|(WSEAM>1e-6))           # feathered blend margins of the zones above
zl=np.where(lab!='outside')[0]; _,nn=cKDTree(V[zl]).query(V[fe]); lab[np.where(fe)[0]]=lab[zl[nn]]
st=lambda d: dict(verts=int(len(d)),median_mm=round(float(np.median(d))*10,3),p95_mm=round(float(np.percentile(d,95))*10,2),p99_mm=round(float(np.percentile(d,99))*10,2),max_mm=round(float(d.max())*10,2))
A={'base_movement_by_zone':{z:st(mv[lab==z]) for z in sorted(set(lab))}}
ek=np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1); _,cc=np.unique(ek,axis=0,return_counts=True)
A['topology']=dict(verts=n,faces=len(F),boundary_edges=int((cc==1).sum()),nonmanifold_edges=int((cc>2).sum()),components=int(igl.connected_components(igl.adjacency_matrix(F))[0]) if hasattr(igl,'connected_components') else None)
A['envelope_cm']={kk:[round(float(np.ptp(V12[:,i])),2),round(float(np.ptp(V[:,i])),2)] for i,kk in enumerate(('width','depth','height'))}
from slicearea import sections
C=np.load('/tmp/claude-0/rodin/g8/axis.npy'); st_=np.arange(2,214)
s12=sections(V12,F12,C,st_); s13=sections(V,F,C,st_)
ok=~np.isnan(s12[:,1])&~np.isnan(s13[:,1]); m=ok&(s12[:,0]>=12)&(s12[:,0]<=98)
A['tail_taper']=dict(volume_s12_98_polish=round(float(np.trapz(s12[m,1],s12[m,0])),0),volume_s12_98_cleanup=round(float(np.trapz(s13[m,1],s13[m,0])),0),
  max_section_area_diff_pct=round(float(np.nanmax(np.abs(s13[ok,1]-s12[ok,1])/s12[ok,1]))*100,3),
  max_dA_ds_cleanup=round(float(np.abs(np.diff(s13[m,1])/np.diff(s13[m,0])).max()),1))
np.save('sl13.npy',s13)
s0=np.load(P9+'g12_surf.npz'); s1=np.load('g13_surf.npz'); r0=np.load(P9+'g12reg.npz'); r1=np.load('g13reg.npz')
dd=np.load('dsurf13.npy'); ii=np.load('nn13.npy'); S1=s1['V'].astype(float); xs,fs,us=S1.T
same=r1['FAM']==r0['FAM'][ii]
A['surface_moved_gt_0p1mm_pct']=round(100*float((dd>0.01).mean()),2)
A['scale_family_agreement_pct_all']=round(100*float(same.mean()),3)
A['scale_family_agreement_pct_unmoved_surface']=round(100*float(same[dd<1e-4].mean()),3)
A['scale_family_agreement_pct_moved_surface']=round(100*float(same[dd>=1e-4].mean()),3)
A['surface_outside_zones_max_mm']=None
json.dump(A,open('acct13.json','w'),indent=1); print(json.dumps(A,indent=1))
np.save('lab13.npy',lab.astype(str))
