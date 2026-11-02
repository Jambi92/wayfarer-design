import sys,json,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001')
import sa6_pose as SP,sa6_fit as FT,sa6_correctives as CC
c='M';R=SP.Rig(c,'/tmp/claude-0/rp6/W_M.npz');Cr=CC.Correctives.load(R,'/tmp/claude-0/rp6/CF_M.json');PS=FT.pose_set(R)
lmv={k:int(np.argmin(np.linalg.norm(R.V-p,axis=1))) for k,p in R.LM.items()}
for pn in ('gate:jaw_open_32','fist_xneg','lower_axial_flex_25_rp5lit'):
    T=R.pose(PS[pn]);d,act=Cr.delta(T,True)
    rig=R.W.max(1)>0.999; hd=R.W[:,R.bi['head']]>0.999
    print(pn,'max |d| head-rigid %.3f'%np.linalg.norm(d[hd],axis=1).max(),'rigid %.3f'%np.linalg.norm(d[rig],axis=1).max())
    for key,(x,ws) in act.items():
        if not ws: continue
        if key.startswith('PK:'): pk=Cr.PK[key[3:]];dd=np.zeros_like(R.V);dd[pk['idx']]=ws[0][1]*pk['d']
        else:
            f=Cr.F[key];dd=np.zeros_like(R.V)
            for k,w in ws: i,v=f['D'][k];dd[i]+=w*v
        a=np.linalg.norm(dd[hd],axis=1).max();b=np.linalg.norm(dd[rig],axis=1).max()
        if a>0.01 or b>0.05: print('   ',key[:40],'x=%.1f'%x if not key.startswith('PK') else '','head %.3f rigid %.3f'%(a,b))
    for k,vi in lmv.items():
        if R.W[vi].max()>0.999 and np.linalg.norm(d[vi])>0.03: print('   LM',k,'|d| %.3f'%np.linalg.norm(d[vi]),'bone',R.DB[R.W[vi].argmax()])
