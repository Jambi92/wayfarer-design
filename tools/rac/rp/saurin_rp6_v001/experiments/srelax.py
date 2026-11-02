import sys,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001')
import sa6_pose as SP,sa6_fit as FT,sa6_correctives as CC
c=sys.argv[1];R=SP.Rig(c,'/tmp/claude-0/rp6/W_%s.npz'%c);Cr=CC.Correctives.load(R,'/tmp/claude-0/rp6/CF_%s.json'%c);S=CC.Solver(R);S.V0=S.body_volume(R.V);PS=FT.pose_set(R)
F=np.r_[R.Q[:,[0,1,2]],R.Q[:,[0,2,3]]].astype(np.int64);w0=FT.wn_out(R.V,F)
E_=np.unique(np.sort(np.r_[R.Q[:,[0,1]],R.Q[:,[1,2]],R.Q[:,[2,3]],R.Q[:,[3,0]]],1),axis=0);L0=np.linalg.norm(R.V[E_[:,0]]-R.V[E_[:,1]],axis=1)
deg=np.asarray(S.A1.sum(1)).ravel()
def stretch(P): return np.linalg.norm(P[E_[:,0]]-P[E_[:,1]],axis=1)/L0
def st(P,T): s=stretch(P);return int((R.relcos(P,T)<0).sum()),int(FT.penetration(R,P,F,w0).sum()),round(S.body_volume(P)-S.V0),round(float(s.max()),2),round(float(np.percentile(s,99.99)),2)
def relax(P,Pl,T,thr,rounds=30,grow=3,it=10,lam=0.5):
    D=P-Pl
    for k in range(rounds):
        s=stretch(Pl+D); s0=stretch(Pl); bad=(s>np.maximum(thr,1.25*s0))
        if not bad.any(): break
        m=np.zeros(R.nv,bool);m[E_[bad].ravel()]=True;m=S.dilate(m,grow)&~S.protect;idx=np.nonzero(m)[0]
        for _ in range(it): D[idx]=(1-lam)*D[idx]+lam*((S.A1@D)/deg[:,None])[idx]
    return Pl+D
for pn in sys.argv[2].split(','):
    T=R.pose(PS[pn]);Pl=R.skin(T);P=R.skin(T,R.V+Cr.delta(T));s=stretch(P);i=np.argmax(s)
    vl=R.ql;print(pn,'lbs',st(Pl,T),'corr',st(P,T),'worst edge at',R.V[E_[i]].mean(0).round(1),'stretched edges>2.5:',(s>2.5).sum())
    for thr in (2.0,2.5):
        Pr=relax(P,Pl,T,thr);print('   relax thr',thr,st(Pr,T))
        Pu,_=S.unfold(T,Pr,R.relcos);print('     +unfold',st(Pu,T))
