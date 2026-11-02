import sys,os,time,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001')
import sa6_pose as SP,sa6_fit as FT,sa6_correctives as CC
cfg=os.environ.get('CFG','M');R=SP.Rig(cfg,'/tmp/claude-0/rp6/W_%s.npz'%cfg);S=CC.Solver(R);S.V0=S.body_volume(R.V);PS=FT.pose_set(R)
F=np.r_[R.Q[:,[0,1,2]],R.Q[:,[0,2,3]]].astype(np.int64);w0=FT.wn_out(R.V,F)
k,n=int(sys.argv[1]),int(sys.argv[2]);names=sorted(PS)[k::n]
for pn in names:
    C=CC.Correctives(R);t=time.time();a,b,c=FT.solve_one(R,C,S,PS[pn],F,w0,[])
    T=R.pose(PS[pn]);P=R.skin(T,R.V+C.delta(T));vp=any(e[0] in FT.VOL_BONES or e[0].rsplit('_',1)[0] in FT.VOL_BONES for e in PS[pn])
    print('%-34s in %4d flips %d pen %d dV %6.0f vol %d %.0fs'%(pn,a,(R.relcos(P,T)<0).sum(),FT.penetration(R,P,F,w0).sum(),S.body_volume(P)-S.V0,vp,time.time()-t),flush=True)
