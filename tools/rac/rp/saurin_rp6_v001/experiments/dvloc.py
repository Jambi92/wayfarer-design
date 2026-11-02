import sys,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001');import sa6_pose as SP,sa6_fit as FT
R=SP.Rig('M',sys.argv[1]);PS=FT.pose_set(R);Q=R.Q
def tv(P,o):
    P=P-o; a,b,c,d=P[Q[:,0]],P[Q[:,1]],P[Q[:,2]],P[Q[:,3]]
    return (np.einsum('ij,ij->i',a,np.cross(b,c))+np.einsum('ij,ij->i',a,np.cross(c,d)))/6
for pn in sys.argv[2].split(','):
    spec=PS[pn]; piv=np.asarray(spec[0][1],float); T=R.pose(spec); P=R.skin(T)
    dv=tv(P,piv)-tv(R.V,piv); print(pn,'pivot',piv.round(2),'bone',spec[0][0],'head',R.H(spec[0][0]).round(2),'total',dv.sum().round(0))
    labs=np.unique(R.ql)
    for l in labs:
        m=R.ql==l; s=dv[m].sum()
        if abs(s)>30: print('   %-14s %8.0f'%(l,s))
    # rigid one-hot
    W1=np.zeros_like(R.W); W1[np.arange(R.nv),R.W.argmax(1)]=1; P1=R.skin(T,W=W1); print('   one-hot rigid total',(tv(P1,piv)-tv(R.V,piv)).sum().round(0))
    # where is the body: pivot relative to the local cross-section
