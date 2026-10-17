import json, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
V=np.load('/home/claude/at/final/ac3.npz')['V'].astype(float); F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']
P=np.load('/home/claude/ag/protected_05AF.npz'); St=np.load('/home/claude/ar/sets.npz'); Wv=np.load('/home/claude/ao/vgroups.npz'); names=list(Wv['names']); lab=Wv['W'].argmax(1)
z0=V[:,2].min(); H=V[:,2].max()-z0; cm=lambda x: round(float(x)*100,2)
T=P['tail']; J=P['tail_junction']; I=St['iface']; n=len(V)
# body midline: pelvis/sacral region trunk verts z 0.45-0.55 H (median of symmetric extremes per slice)
tr=lab==names.index('trunk'); xs=[]
for zz in np.linspace(0.46,0.56,11):
    s=tr&(np.abs((V[:,2]-z0)/H-zz)<0.005)
    if s.sum(): xs.append((V[s,0].max()+V[s,0].min())/2)
xmid=float(np.median(xs))
c=V[I].mean(0)
# geodesic distance along the tail surface from the interface
e=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); keep=T[e[:,0]]&T[e[:,1]]; e=e[keep]; w=np.linalg.norm(V[e[:,0]]-V[e[:,1]],axis=1)
G=sp.coo_matrix((np.r_[w,w],(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),shape=(n,n)).tocsr()
src=np.flatnonzero(I); D=dijkstra(G,indices=src,min_only=True)
ti=np.flatnonzero(T&np.isfinite(D)); s=D[ti]
body=(~T)&(~J); tb=cKDTree(V[body]); gap,_=tb.query(V[ti])
rows=[]; fused_end=None
for a in np.arange(0,0.60,0.02):
    b=(s>=a)&(s<a+0.02)
    if not b.any(): continue
    g=float(gap[b].min()); cen=V[ti[b]].mean(0); rows.append(dict(s_cm=round(a*100,1),min_gap_to_body_mm=round(g*1000,2),centre_cm=[cm(cen[0]-xmid),cm(cen[1]),cm(cen[2]-z0)]))
    if fused_end is None and g>0.005: fused_end=a
# root axis: centreline points from the first 12 cm of arc length
cl=np.array([V[ti[(s>=a)&(s<a+0.01)]].mean(0) for a in np.arange(0.0,0.12,0.01) if ((s>=a)&(s<a+0.01)).any()])
d=cl[-1]-cl[0]; d/=np.linalg.norm(d)
elev=np.degrees(np.arcsin(-d[2]))   # angle below horizontal (positive = descending)
lat=np.degrees(np.arctan2(d[0],d[1]))
# gluteal cleft top: highest point of the cleft = where the midline posterior surface meets the junction; take junction top
jz=V[J][:,2]; R=dict(body_midline_x_cm=cm(xmid),interface_centroid_cm=dict(x_from_midline=cm(c[0]-xmid),y=cm(c[1]),z=cm(c[2]-z0),z_pct_H=round((c[2]-z0)/H*100,2)),
  interface_extent_cm=[cm(x) for x in np.ptp(V[I],0)],junction_z_range_cm=[cm(jz.min()-z0),cm(jz.max()-z0)],
  root_direction=dict(unit=[round(float(x),3) for x in d],angle_below_horizontal_deg=round(float(elev),1),lateral_yaw_deg_from_posterior=round(float(lat),1)),
  fused_length_cm=(None if fused_end is None else round(fused_end*100,1)),gap_profile=rows[:20])
# posterior sacral / glute landmarks for context: posterior-most glute point z and the cleft top (highest point where L and R glute surfaces meet behind)
json.dump(R,open('au_tail.json','w'),indent=1); print(json.dumps({k:v for k,v in R.items() if k!='gap_profile'},indent=1)); print(json.dumps(R['gap_profile'][:15]))
