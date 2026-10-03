# Gate 5 evidence prep: lock accounting, render inputs, isolated hands in the hand frame.
import numpy as np, json
from scipy.spatial import cKDTree
import hand
SK={-1:dict(S=(-23.5,-6.0,147.0),E=(-30.5,-4.5,117.0),W=(-36.8,6.0,97.0)),1:dict(S=(23.0,-5.0,147.0),E=(28.8,-3.5,117.0),W=(35.2,7.0,97.0))}
a4=np.load('g4_body.npz'); V4,F4=a4['V'],a4['F']
z=np.load('g5_body.npz'); V,F,origin,mv=z['V'],z['F'],z['origin'],z['moved']
kept=origin>=0; ident=kept&(mv<1e-9)
R=np.where(ident,3,np.where(kept,22,21))
np.savez('cur_g5.npz',P=V,f=F,R=np.zeros(len(V),int)); np.savez('cur_g4.npz',P=V4,f=F4,R=np.zeros(len(V4),int)); np.savez('acct5.npz',P=V,f=F,R=R)
# per-region identity on Gate-4 vertices
idg4=np.zeros(len(V4),bool); idg4[origin[ident]]=True
import g1
P1=g1.P1; AV=np.load('arm_vert_mask.npy'); AT=cKDTree(P1[AV]); da,_=AT.query(V4)
x,f_,u=V4.T
REG={'free tail (F < -45)':f_<-45,
     'torso / pelvis / tail root / head / neck (|x| < 19.5)':(np.abs(x)<19.5),
     'head + neck (U > 150, |x| < 19.5)':(u>150)&(np.abs(x)<19.5),
     'Gate 4 legs + feet (U < 86, > 3 cm from B1 arm/hand surface)':(u<86)&(da>3.0),
     'Gate 4 hips / thighs (U 60-100, |x| > 19.5, > 3 cm from B1 arm/hand)':(u>60)&(u<100)&(np.abs(x)>19.5)&(da>3.0)}
acc={k:[int(m.sum()),int((m&idg4).sum())] for k,m in REG.items()}
ch=~idg4; P=V4[ch]
acc['_changed_gate4_verts']=int(ch.sum()); acc['_changed_bbox']=[P.min(0).round(2).tolist(),P.max(0).round(2).tolist()]
acc['_changed_min_dist_to_B1_arm']=float(da[ch].max().round(2))
acc['_out']=dict(verts=len(V),faces=len(F),identical=int(ident.sum()),relaxed=int((kept&~ident).sum()),relaxed_max=float(mv[kept].max().round(3)),new=int((~kept).sum()))
acc['_height']=[float(np.ptp(V[:,2]).round(3)),float(np.ptp(V4[:,2]).round(3))]
for sg in (-1,1):
    m=np.sign(P[:,0])==sg; acc['_changed_absx_min_side%+d'%sg]=float(np.abs(P[m,0]).min().round(2))
json.dump(acc,open('acct5.json','w'),indent=1); print(json.dumps(acc,indent=1))
# isolated hands: crop beyond the wrist and express in hand frame -> x'=dorsal(+), f'=radial/thumb(+), u'=proximal(+)
for sg in (-1,1):
    S=SK[sg]; a,b,c=hand.frame(S['W'],S['E'],sg); Q=V-np.asarray(S['W'])
    keep=((Q@a)>-4.0)&(np.linalg.norm(Q,axis=1)<26); kk=np.where(keep)[0]; hd=hand.hand_world(*V[kk].T,S['W'],S['E'],sg); keep[kk[hd>2.5]]=False
    fk=F[keep[F].all(1)]; idx=np.unique(fk); remap=-np.ones(len(V),int); remap[idx]=np.arange(len(idx))
    L=np.stack([-(Q[idx]@c),Q[idx]@b,-(Q[idx]@a)],1)
    np.savez('hand5_%d.npz'%(sg>0),P=L,f=remap[fk],R=np.zeros(len(idx),int)); print('hand',sg,len(idx),L.min(0).round(1),L.max(0).round(1))
# same crop on Gate 4 for the before/after
for sg in (-1,1):
    S=SK[sg]; a,b,c=hand.frame(S['W'],S['E'],sg); Q=V4-np.asarray(S['W'])
    keep=((Q@a)>-4.0)&(np.linalg.norm(Q,axis=1)<26)&(da<1.0)
    fk=F4[keep[F4].all(1)]; idx=np.unique(fk); remap=-np.ones(len(V4),int); remap[idx]=np.arange(len(idx))
    L=np.stack([-(Q[idx]@c),Q[idx]@b,-(Q[idx]@a)],1)
    np.savez('hand4_%d.npz'%(sg>0),P=L,f=remap[fk],R=np.zeros(len(idx),int))
