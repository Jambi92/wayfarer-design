import sys,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001')
import sa6_pose as SP,sa6_fit as FT,sa6_correctives as CC
R=SP.Rig('M',sys.argv[1]);S=CC.Solver(R);S.V0=S.body_volume(R.V);PS=FT.pose_set(R)
F=np.r_[R.Q[:,[0,1,2]],R.Q[:,[0,2,3]]].astype(np.int64);w0=FT.wn_out(R.V,F)
E_=np.unique(np.sort(np.r_[R.Q[:,[0,1]],R.Q[:,[1,2]],R.Q[:,[2,3]],R.Q[:,[3,0]]],1),axis=0);L0=np.linalg.norm(R.V[E_[:,0]]-R.V[E_[:,1]],axis=1)
def tears(P):
    L=np.linalg.norm(P[E_[:,0]]-P[E_[:,1]],axis=1);el=L-L0;m=(el>0.5)&(L/L0>2.0);return m,el
def st(P,T): m,el=tears(P);return int((R.relcos(P,T)<0).sum()),int(FT.penetration(R,P,F,w0).sum()),round(S.body_volume(P)-S.V0),int(m.sum()),round(float(el.max()),2)
for pn in sys.argv[2].split(','):
    T=R.pose(PS[pn]);P=R.skin(T);print(pn,'lbs',st(P,T),flush=True)
    for ring,it in ((6,1),(12,1),(12,4),(24,4)):
        m,_=tears(P);seed=np.zeros(R.nv,bool);seed[E_[m].ravel()]=True
        S.pin=True;Ps,I,M=S.solve(T,P,np.zeros(0,int),iters=it,ring=ring,spread_tol=1e-4,local=True,seed=seed)
        a=st(Ps,T);Pu,_=S.unfold(T,Ps,R.relcos);print('   ring %d it %d'%(ring,it),a,'+unfold',st(Pu,T),flush=True)
