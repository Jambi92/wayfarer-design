import sys,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001')
import sa6_pose as SP,sa6_fit as FT
c=sys.argv[1];R=SP.Rig(c,sys.argv[2]);PS=FT.pose_set(R)
E_=np.unique(np.sort(np.r_[R.Q[:,[0,1]],R.Q[:,[1,2]],R.Q[:,[2,3]],R.Q[:,[3,0]]],1),axis=0);L0=np.linalg.norm(R.V[E_[:,0]]-R.V[E_[:,1]],axis=1)
vl=np.empty(R.nv,object)
for l in np.unique(R.ql): vl[np.unique(R.Q[R.ql==l])]=l
for pn in sorted(PS):
    if pn in FT.NONREAL or 'rp5lit' in pn: continue
    T=R.pose(PS[pn]);P=R.skin(T);L=np.linalg.norm(P[E_[:,0]]-P[E_[:,1]],axis=1);el=L-L0;s=L/L0
    m=(el>0.5)&(s>2.0)
    if m.any():
        i=np.argmax(el);a,b=E_[i];print('%-30s n %4d max elong %.2f cm (x%.1f) at %s labels %s/%s dom %s/%s'%(pn,m.sum(),el[i],s[i],R.V[a].round(1),vl[a],vl[b],R.DB[R.W[a].argmax()],R.DB[R.W[b].argmax()]))
