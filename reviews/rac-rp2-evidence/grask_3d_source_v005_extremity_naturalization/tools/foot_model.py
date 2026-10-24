# foot_model.py : Grask forefoot + toes SDF in the foot frame (a forward, b lateral(outer), z up), cm; left-foot coordinates
import numpy as np
from sdf import smin, smax, round_cone, ellipsoid, flat_cone, rot
from hand_model import nail_sdf, nail_groove
Z=np.array([0,0,1.0])
DEF=dict(
 toes=[ # name, mtp(b,a,z), L(phalanges), r(base..tip), splay(deg, + = lateral), flex(deg, + = plantar)
  dict(n='hallux',mtp=[13.6,16.0,2.3],L=[4.9,4.3],     r=[2.15,2.02,1.9,1.68], splay=-1, flex=[-4,6]),
  dict(n='toe2',  mtp=[17.75,15.6,1.85],L=[4.6,2.6,2.1],r=[1.38,1.28,1.2,1.12,1.02],splay=2, flex=[-10,30,-14]),
  dict(n='toe3',  mtp=[20.8,14.6,1.72],L=[4.0,2.3,1.9], r=[1.3,1.2,1.13,1.06,0.97],splay=4, flex=[-10,32,-14]),
  dict(n='toe4',  mtp=[23.55,13.2,1.62],L=[3.5,2.0,1.7],r=[1.22,1.13,1.07,1.0,0.92],splay=7,flex=[-9,34,-14]),
  dict(n='toe5',  mtp=[26.0,11.6,1.55],L=[2.9,1.7,1.45],r=[1.14,1.06,1.0,0.94,0.86],splay=11,flex=[-8,36,-14])],
 flat=0.80, meta_base_a=3.0, meta_base_z=4.3,
 ball=dict(c=[19.6,13.3,1.25],rad=[8.6,3.6,1.45]),
 nat=dict(seg_k=0.2, ja=1.3, jw=0.94, jk=0.25, fs=0.0, fz=0.8, kn=[0.7,0.55,0.2], knk=0.2, kno=0.40, pad=[0.42,0.85,0.55], padk=0.3, padoff=0.34, nk=(0.15,0.06)),
 nail=dict(start=0.24, half_lat=0.80, thick=0.05, groove=0.085, raise_=0.025, curv=0.5, tube2=0.2, lift=0.11, proud=0.03),
)
def chain(t):
    a=np.array([0,1.0,0]); d=rot(Z,-np.radians(t['splay']))@a   # +splay -> toward +b (lateral)
    if (d@np.array([1.0,0,0]))*np.sign(t['splay']+1e-9)<0: d=rot(Z,np.radians(t['splay']))@a
    dor=Z.copy(); J=[np.array(t['mtp'],float)]; dirs=[]; dors=[]
    for k,L in enumerate(t['L']):
        lat=np.cross(d,dor); lat/=np.linalg.norm(lat); R=rot(lat,np.radians(abs(t['flex'][k])))
        want_down=t['flex'][k]>0
        if ((R@d)[2]<d[2])!=want_down: R=rot(lat,-np.radians(abs(t['flex'][k])))
        d=R@d; dor=R@dor; dirs.append(d.copy()); dors.append(dor.copy()); J.append(J[-1]+L*d)
    return J,dirs,dors
def foot_sdf(P,p=DEF,zg=0.0):
    d=np.full(len(P),1e3)
    for t in p['toes']:
        J,dirs,dors=chain(t); r=t['r']; n=len(t['L'])
        d=np.minimum(d,ellipsoid(P,J[0]+np.array([0,0,0.25*r[0]]),np.eye(3),np.array([1.05,0.95,0.85])*r[0]*1.05))   # MTP head
        d0=dirs[0]*np.array([1,1,0]); d0/=np.linalg.norm(d0)
        ramp=flat_cone(P,J[0]-d0*3.8+Z*(1.0+0.35*r[0]),J[0]+dirs[0]*1.2+Z*0.25,r[0]*1.3,r[0]*1.02,Z,0.72)
        dt=ramp
        for k in range(n):
            end=J[k+1]-dirs[k]*(r[k+1]*0.5 if k==n-1 else 0)
            seg=flat_cone(P,J[k],end,r[k],r[k+1],dors[k],p['flat'])
            dt=smin(dt,seg,0.6 if k==0 else p['nat']['seg_k'])
        for k in range(1,n):
            N_=p['nat']; rj=r[k]*N_['jw']; bj=dirs[k-1]+dirs[k]; bj/=np.linalg.norm(bj); oj=dors[k-1]+dors[k]; oj/=np.linalg.norm(oj)
            fr=np.stack([bj,np.cross(bj,oj),oj],1)
            dt=smin(dt,ellipsoid(P,J[k],fr,[N_['ja']*r[k],rj,rj*p['flat']]),N_['jk'])
            kn=N_['kn']; dt=smin(dt,ellipsoid(P,J[k]+oj*(N_['kno']*r[k]),fr,[kn[0]*r[k],kn[1]*r[k],kn[2]*r[k]]),N_['knk'])
        for k in range(n-1):
            Lk=t['L'][k]; N_=p['nat']; ck=J[k]+dirs[k]*(0.5*Lk)-dors[k]*(N_['padoff']*r[k])
            dt=smin(dt,ellipsoid(P,ck,np.stack([dirs[k],np.cross(dirs[k],dors[k]),dors[k]],1),[N_['pad'][0]*Lk,N_['pad'][1]*r[k],N_['pad'][2]*r[k]]),N_['padk'])
        # distal pad (plantar) + dorsal nail-bed flattening
        Ld=t['L'][-1]; Jd=J[n-1]; dd=dirs[-1]; do=dors[-1]; rt=r[n]
        dt=smin(dt,ellipsoid(P,Jd+dd*(0.62*Ld)-do*(0.32*rt),np.stack([dd,np.cross(dd,do),do],1),[0.55*Ld,0.95*rt,0.6*rt]),0.22)
        flatcut=(P-Jd)@do-rt*p['flat']*0.96; zone=np.clip(((P-Jd)@dd-p['nat'].get('fs',0.2)*Ld)/(p['nat'].get('fz',0.15)*Ld),0,1)
        dt=smax(dt,flatcut-(1-zone)*5,0.15)
        rg,pl=nail_groove(P,Jd,dd,do,Ld,rt,p['flat'],p['nail'])
        dt=smax(dt,-rg,p['nat']['nk'][0]); dt=smin(dt,pl,p['nat']['nk'][1])
        d=np.minimum(d,dt) if t['n']!='hallux' else smin(d,dt,0.3)
    d=smax(d,zg-P[:,2],0.35)
    return d
