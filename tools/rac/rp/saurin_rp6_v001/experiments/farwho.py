import sys,os,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001')
import sa6_pose as SP,sa6_fit as FT,sa6_correctives as CC
R=SP.Rig('M','/tmp/claude-0/rp6/W_M.npz');S=CC.Solver(R);S.V0=S.body_volume(R.V);PS=FT.pose_set(R)
F=np.r_[R.Q[:,[0,1,2]],R.Q[:,[0,2,3]]].astype(np.int64);w0=FT.wn_out(R.V,F)
for pn in sys.argv[1].split(','):
    C=CC.Correctives(R);FT.solve_one(R,C,S,PS[pn],F,w0,[]);T=R.pose(PS[pn]);P=R.skin(T,R.V+C.delta(T));dd=np.linalg.norm(P-R.skin(T),axis=1)
    dom=np.array(R.DB)[R.W.argmax(1)];m=dd>0.3
    u,c=np.unique(dom[m],return_counts=True);o=np.argsort(-c);print(pn,'moved>3mm by dominant bone:',[(u[i],int(c[i]),round(float(dd[m&(dom==u[i])].max()),2)) for i in o])
