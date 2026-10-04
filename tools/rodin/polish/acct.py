import numpy as np, igl, json
from scipy.spatial import cKDTree
G='/tmp/claude-0/rodin/g1/'
b0=np.load(G+'g9_body.npz'); b1=np.load('g12_body.npz')
V0=b0['V'].astype(float); F0=b0['F'].astype(np.int64); V1=b1['V'].astype(float); F1=b1['F'].astype(np.int64)
d1,_,_=igl.point_mesh_squared_distance(V1,V0,F0); d1=np.sqrt(d1)        # base geometry change, per new base vertex
x,f,u=V1.T
reg={'head (brow surgery box)':(np.abs(x)<16)&(f>-34)&(f<28)&(u>161),'tail (s<98, f<-26)':(f<-26)&(u>40)&(u<120)}
reg['everything else']=~(reg['head (brow surgery box)']|reg['tail (s<98, f<-26)'])
st=lambda d: dict(verts=int(len(d)),median_mm=round(float(np.median(d))*10,3),p99_mm=round(float(np.percentile(d,99))*10,2),max_mm=round(float(d.max())*10,2),changed_gt_0p1mm=int((d>0.01).sum()))
A={'base_geometry_change_vs_gate6_closed':{k:st(d1[m]) for k,m in reg.items()}}
A['base_mesh']=dict(gate6_verts=len(V0),polish_verts=len(V1),identical_copies=int((d1<1e-7).sum()))
# envelope
A['envelope_cm']={k:[round(float(np.ptp(V0[:,i])),2),round(float(np.ptp(V1[:,i])),2)] for i,k in enumerate(('width','depth','height'))}
# surface level: new closure surface vs Gate 7 closure surface
s0=np.load(G+'g7_surfc.npz'); s1=np.load('g12_surf.npz'); r0=np.load(G+'g7regc.npz'); r1=np.load('g12reg.npz')
S0=s0['V'].astype(float); S1=s1['V'].astype(float)
tr=cKDTree(S0); dd,ii=tr.query(S1)
x,f,u=S1.T
sreg={'head (brow surgery box)':(np.abs(x)<16)&(f>-34)&(f<28)&(u>161),'tail (s<98, f<-26)':(f<-26)&(u>40)&(u<120)}
sreg['everything else']=~(sreg['head (brow surgery box)']|sreg['tail (s<98, f<-26)'])
A['surface_vs_gate7_closure_nearest_vertex']={k:st(dd[m]) for k,m in sreg.items()}
same=(r1['FAM']==r0['FAM'][ii])
A['scale_family_agreement_pct']={k:round(100*float(same[m].mean()),2) for k,m in sreg.items()}
A['family_counts']={'gate7':{int(k):int((r0['FAM']==k).sum()) for k in range(1,8)},'polish':{int(k):int((r1['FAM']==k).sum()) for k in range(1,8)}}
np.save('dbase.npy',d1); np.save('dsurf.npy',dd)
json.dump(A,open('acct_p9.json','w'),indent=1); print(json.dumps(A,indent=1))
