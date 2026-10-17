# RM-OT-05AU diagnostics on frozen GO-05AT_AC3 (read-only). Units: model metres -> reported cm.
import sys, json, numpy as np, trimesh, scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
V=np.load('/home/claude/at/final/ac3.npz')['V'].astype(float); F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']
P=np.load('/home/claude/ag/protected_05AF.npz'); St=np.load('/home/claude/ar/sets.npz'); Wv=np.load('/home/claude/ao/vgroups.npz'); names=list(Wv['names']); Wt=Wv['W']; lab=Wt.argmax(1)
z0=V[:,2].min(); H=V[:,2].max()-z0; cm=lambda x: round(float(x)*100,2); R={}
m=trimesh.Trimesh(V,F,process=False)
# ---------- head: menton-vertex (W1 arm_measure definition: vertex = highest head point excluding ears; menton = lowest chin point near MSP)
hs=V[P['head']]; xm=(hs[:,0].max()+hs[:,0].min())/2
mid=P['head']&(np.abs(V[:,0]-xm)<0.04)
vtx=V[mid][np.argmax(V[mid,2])]
sec=m.section(plane_origin=[xm,0,0],plane_normal=[1,0,0]); pts=np.vstack([sec.vertices[e.points] for e in sec.entities])
# chin: anterior jaw region in front of the throat (y below -0.50), z between 1.70 and 1.80 above floor -> lowest point
jaw=pts[(pts[:,1]<-0.52)&((pts[:,2]-z0)>1.70)&((pts[:,2]-z0)<1.82)]
me=jaw[np.argmin(jaw[:,2])]
HH=vtx[2]-me[2]; stature_vertex=vtx[2]-z0
# head breadth excluding ears: max x-extent of head verts between menton+5cm and vertex-6cm (below the ear roots)
band=P['head']&(V[:,2]>me[2]+0.05)&(V[:,2]<vtx[2]-0.06)
hb=np.ptp(V[band,0])
# bideltoid breadth: max x-extent of trunk+upperarm verts within z 0.80-0.86 H
sh=(np.isin(lab,[names.index(k) for k in ['trunk','upperarm_L','upperarm_R']]))&((V[:,2]-z0)/H>0.78)&((V[:,2]-z0)/H<0.86)
bid=np.ptp(V[sh,0])
R['stature']=dict(bbox_height_cm=cm(H),vertex_height_cm=cm(stature_vertex),note='bbox top is the ear tips; skull vertex is %.2f cm lower'%((H-stature_vertex)*100))
R['head']=dict(vertex_cm=[cm(vtx[0]),cm(vtx[1]),cm(vtx[2]-z0)],menton_cm=[cm(me[0]),cm(me[1]),cm(me[2]-z0)],HH_menton_vertex_cm=cm(HH),HH_share_of_bbox_pct=round(HH/H*100,2),HH_share_of_vertex_stature_pct=round(HH/stature_vertex*100,2),
  head_breadth_ex_ears_cm=cm(hb),bideltoid_cm=cm(bid),head_breadth_over_bideltoid=round(hb/bid,3),head_set_05AF_z_extent_cm=cm(np.ptp(hs[:,2])))
# W1 accepted guide (GO r6; arm_measure output) + same breadth ratios on the guide mesh
W=np.load('/home/claude/wayfarer-design/reviews/rac-w1i-evidence/geometry/GO_r6.npz',allow_pickle=True); Vw=W['V']; Hw=np.ptp(Vw[:,2]); zw=Vw[:,2].min()
gm=json.load(open('/home/claude/wayfarer-design/reviews/rac-w1i-evidence/candidates/GO_meas.json'))['r6']
wh=(W['w_head']>0.5)&(W['w_ears']<0.2); hw_=Vw[wh]; HHw=gm['cranio']['HH']; mew=gm['cranio']['Me']
bandw=wh&(Vw[:,2]>mew[2]+5)&(Vw[:,2]<gm['cranio']['V'][2]-6); hbw=np.ptp(Vw[bandw,0])
shw=((W['w_spine_03']+W['w_clavicle_l']+W['w_clavicle_r']+W['w_upperarm_l']+W['w_upperarm_r'])>0.5)&((Vw[:,2]-zw)/Hw>0.78)&((Vw[:,2]-zw)/Hw<0.86); bidw=np.ptp(Vw[shw,0])
R['head_W1']=dict(source='reviews/rac-w1i-evidence/candidates/GO_meas.json r6 + geometry/GO_r6.npz',stature_cm=round(float(Hw),2),HH_cm=round(HHw,2),HH_share_pct=round(gm['ratio']['HH_share']*100,2),
  head_breadth_ex_ears_cm=round(float(hbw),2),bideltoid_cm=round(float(bidw),2),head_breadth_over_bideltoid=round(float(hbw/bidw),3))
R['head']['diff_vs_W1_HH_share_pts']=round(R['head']['HH_share_of_vertex_stature_pct']-R['head_W1']['HH_share_pct'],2)
# ---------- feet: heel lift, size
def foot(side):
    fm=lab==names.index(f'foot_{side}'); X=V[fm]; c=X.mean(0); _,_,vt=np.linalg.svd((X-c)[:,:2],full_matrices=False); ax=np.r_[vt[0],0]
    if ax[1]>0: ax=-ax   # point toward the toes (front is -Y)
    s=(X-c)@ax; L=np.ptp(s); t=(s-s.min())/L; perp=np.array([-ax[1],ax[0],0]); w=np.ptp((X-c)@perp)
    zr=lambda a,b: float(X[(t>=a)&(t<=b),2].min()-z0)
    heel=zr(0,0.15); mid=zr(0.35,0.6); ball=zr(0.65,0.82); toes=zr(0.85,1.0)
    cont=(X[:,2]-z0)<0.003; tc=t[cont]
    # ankle: shin-foot weight blend ring centroid; knee: thigh-shin ring
    def ring(a,b):
        w_=Wt[:,names.index(a)]; w2=Wt[:,names.index(b)]; r=(w_>0.25)&(w_<0.75)&(w2>0.25); return V[r].mean(0)
    ank=ring(f'shin_{side}',f'foot_{side}'); kn=ring(f'thigh_{side}',f'shin_{side}')
    # ankle circumference: section of shin+foot verts at ankle height
    s_=m.section(plane_origin=[0,0,ank[2]],plane_normal=[0,0,1]); circ=None
    if s_ is not None:
        best=None
        for e in s_.entities:
            p=s_.vertices[e.points]; d=np.linalg.norm(p.mean(0)[:2]-ank[:2])
            if best is None or d<best[0]: best=(d,float(np.linalg.norm(np.diff(p,axis=0),axis=1).sum()))
        circ=best[1]
    return dict(length_cm=cm(L),width_cm=cm(w),length_pct_H=round(L/H*100,2),width_pct_H=round(w/H*100,2),ankle_height_cm=cm(ank[2]-z0),knee_height_cm=cm(kn[2]-z0),
        tibial_segment_cm=cm(kn[2]-ank[2]),length_over_tibial=round(L/(kn[2]-ank[2]),3),ankle_circ_cm=cm(circ) if circ else None,ankle_circ_pct_H=round(circ/H*100,2) if circ else None,
        plantar_min_z_cm=dict(heel=cm(heel),midfoot=cm(mid),ball=cm(ball),toes=cm(toes)),heel_lift_vs_ball_cm=cm(heel-ball),heel_lift_vs_ground_cm=cm(heel),
        ground_contact_span=[round(float(tc.min()),2),round(float(tc.max()),2)] if len(tc) else None,ground_contact_vertices=int(cont.sum()))
R['feet']={s:foot(s) for s in 'LR'}
# W1 foot: foot + ball weights, length along the same horizontal PCA
fw=(W['w_foot_l']+W['w_ball_l'])>0.5; X=Vw[fw]; c=X.mean(0); _,_,vt=np.linalg.svd((X-c)[:,:2],full_matrices=False); s=(X-c)@np.r_[vt[0],0]; Lw=np.ptp(s); ww=np.ptp((X-c)@np.r_[-vt[0][1],vt[0][0],0])
j=json.loads(str(W['joints'])) if W['joints'].shape==() else None
R['feet_W1']=dict(length_cm=round(float(Lw),2),width_cm=round(float(ww),2),length_pct_H=round(float(Lw/Hw*100),2),width_pct_H=round(float(ww/Hw*100),2),
   heel_min_z_cm=round(float(X[(s-s.min())/Lw<0.15,2].min()-zw),2),ball_min_z_cm=round(float(X[((s-s.min())/Lw>0.65)&((s-s.min())/Lw<0.82),2].min()-zw),2))
json.dump(R,open('au_measure_head_feet.json','w'),indent=1); print(json.dumps(R,indent=1))
