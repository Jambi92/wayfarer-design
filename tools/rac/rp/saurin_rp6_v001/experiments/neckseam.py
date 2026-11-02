import sys,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001');import sa6_pose as SP,sa6_common as C,sa6_correctives as CC,sa6_fit as FT
R=SP.Rig('M','/tmp/claude-0/rp6/W_M.npz');V=R.V;Q=R.Q;ql=R.ql
def seam(a,b):
    va=np.zeros(R.nv,bool);va[Q[ql==a].ravel()]=True;vb=np.zeros(R.nv,bool);vb[Q[np.isin(ql,b)].ravel()]=True;m=va&vb;return np.nonzero(m)[0]
s=seam('neck',['trunk','shoulder']); print('neck/trunk seam n',len(s),'centroid',V[s].mean(0).round(2),'z',V[s,2].min().round(1),V[s,2].max().round(1),'y',V[s,1].min().round(1),V[s,1].max().round(1))
h=seam('neck',['head']); print('neck/head seam n',len(h),'centroid',V[h].mean(0).round(2))
# section centroid of neck-labelled verts near z of neck_base landmark: plane cut perpendicular to neck axis
c0=V[s].mean(0); c1=V[h].mean(0); ax=(c1-c0)/np.linalg.norm(c1-c0); print('neck axis',ax.round(3))
nv=np.zeros(R.nv,bool);nv[Q[ql=='neck'].ravel()]=True
for t in (0.0,0.1,0.2,0.5,0.8):
    p=c0+t*(c1-c0); m=nv&(np.abs((V-p)@ax)<0.4); print(' t',t,'section centroid',V[m].mean(0).round(2),'n',m.sum())
S=CC.Solver(R);V0=S.body_volume(R.V);PS=FT.pose_set(R);X,Y,Z=np.eye(3)
for piv,nm in ((R.H('neck_01'),'current'),(c0,'seam centroid')):
    for pn,ax_,dg in (('neck_flex_30',X,-30),('neck_rot_40',Z,40),('neck_ext',X,30)):
        T=R.pose([('neck_01',piv,ax_,dg)]);P=R.skin(T);print('%-14s %-12s flips %4d dV %6.0f'%(nm,pn,(R.relcos(P,T)<0).sum(),S.body_volume(P)-V0))
print('anat neck_flex spec',[(b,np.round(p,1),a,d) for b,p,a,d in PS['neck_flex_30']])
