import sys, json, numpy as np, trimesh
from scipy.spatial import cKDTree
import shapely.geometry as sg
V=np.load('/home/claude/at/final/ac3.npz')['V'].astype(float); F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']
P=np.load('/home/claude/ag/protected_05AF.npz'); Wv=np.load('/home/claude/ao/vgroups.npz'); names=list(Wv['names']); lab=Wv['W'].argmax(1)
z0=V[:,2].min(); H=V[:,2].max()-z0; cm=lambda x: round(float(x)*100,2); m=trimesh.Trimesh(V,F,process=False); R=json.load(open('au_measure_head_feet.json'))
hs=V[P['head']]; xm=(hs[:,0].max()+hs[:,0].min())/2
# head breadth: widest central (non-ear) contour of horizontal sections between menton+5 cm and 192 cm
me=R['head']['menton_cm'][2]/100+z0; best=0
for z in np.arange(me+0.05, z0+1.92, 0.005):
    s=m.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
    for e in s.entities:
        p=s.vertices[e.points]
        if abs(p[:,0].mean()-xm)<0.05 and abs(p[:,1].mean()-hs[:,1].mean())<0.15: best=max(best,np.ptp(p[:,0]))
R['head']['head_breadth_ex_ears_cm']=cm(best); R['head']['head_breadth_over_bideltoid']=round(best/(R['head']['bideltoid_cm']/100),3)
# feet: footprint width (plantar verts < 3 cm) and minimum leg circumference above the ankle (anthropometric ankle circumference)
for side in 'LR':
    fm=lab==names.index(f'foot_{side}'); X=V[fm]; c=X.mean(0); _,_,vt=np.linalg.svd((X-c)[:,:2],full_matrices=False); ax=np.r_[vt[0],0]; perp=np.array([-ax[1],ax[0],0])
    pl=X[(X[:,2]-z0)<0.03]; R['feet'][side]['footprint_width_cm']=cm(np.ptp((pl-c)@perp)); R['feet'][side]['footprint_width_pct_H']=round(np.ptp((pl-c)@perp)/H*100,2)
    sh=lab==names.index(f'shin_{side}'); cxy=V[sh&((V[:,2]-z0)<0.25)][:, :2].mean(0); circs=[]
    for z in np.arange(0.10,0.30,0.005):
        s=m.section(plane_origin=[0,0,z0+z],plane_normal=[0,0,1]); bestc=None
        for e in s.entities:
            p=s.vertices[e.points]; d=np.linalg.norm(p[:,:2].mean(0)-cxy)
            if d<0.08: L=float(np.linalg.norm(np.diff(p,axis=0),axis=1).sum()); bestc=L if bestc is None else min(bestc,L)
        if bestc: circs.append((bestc,z))
    cmin=min(circs); R['feet'][side]['ankle_min_circ_cm']=cm(cmin[0]); R['feet'][side]['ankle_min_circ_height_cm']=cm(cmin[1]); R['feet'][side]['ankle_min_circ_pct_H']=round(cmin[0]/H*100,2)
    R['feet'][side].pop('ankle_circ_cm',None); R['feet'][side].pop('ankle_circ_pct_H',None)
    # toe count: section perpendicular to the foot axis at 92 % of foot length; count closed contours below 6 cm
    s_=(X-c)@ax; t=(s_-s_.min())/np.ptp(s_); cnt={}
    for tt in (0.88,0.92,0.95):
        o=c+ax*(s_.min()+tt*np.ptp(s_)); sec=m.section(plane_origin=o,plane_normal=ax)
        n=0
        for e in sec.entities:
            p=sec.vertices[e.points]
            if (p[:,2].mean()-z0)<0.06 and np.linalg.norm((p.mean(0)-o)[:2])<0.15: n+=1
        cnt[str(tt)]=n
    R['feet'][side]['toe_contours_at_frac_length']=cnt
json.dump(R,open('au_measure_head_feet.json','w'),indent=1)
print(json.dumps({'head':R['head'],'feet':{s:{k:R['feet'][s][k] for k in ['footprint_width_cm','footprint_width_pct_H','ankle_min_circ_cm','ankle_min_circ_height_cm','ankle_min_circ_pct_H','toe_contours_at_frac_length']} for s in 'LR'}},indent=1))
