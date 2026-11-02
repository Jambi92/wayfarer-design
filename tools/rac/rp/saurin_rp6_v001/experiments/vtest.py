import sys,os,time,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001');import sa6_pose as SP,sa6_fit as FT,sa6_correctives as CC
import os;R=SP.Rig(os.environ.get('CFG','M'),os.environ.get('WF','/tmp/claude-0/rp6/W_M.npz'));S=CC.Solver(R);S.V0=S.body_volume(R.V);PS=FT.pose_set(R)
F=np.r_[R.Q[:,[0,1,2]],R.Q[:,[0,2,3]]].astype(np.int64);w0=FT.wn_out(R.V,F)
for pn in sys.argv[1].split(','):
    C=CC.Correctives(R);t=time.time();a,b,c=FT.solve_one(R,C,S,PS[pn],F,w0,[])
    T=R.pose(PS[pn]);P=R.skin(T,R.V+C.delta(T));te,el=S.tear_edges(P);print('%-24s in %4d after %3d | final flips %d pen %d dV %.0f tears %d maxel %.2f  %.0fs'%(pn,a,b,(R.relcos(P,T)<0).sum(),FT.penetration(R,P,F,w0).sum(),S.body_volume(P)-S.V0,te.sum(),el.max(),time.time()-t),flush=True)
