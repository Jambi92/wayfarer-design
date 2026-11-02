import sys,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001');import sa6_pose as SP,sa6_fit as FT,sa6_correctives as CC,sa6_common as C
R=SP.Rig('M','/tmp/claude-0/rp6/W_M.npz');S=CC.Solver(R);V0=S.body_volume(R.V);X,Y,Z=np.eye(3);LM=C.load()['LM']
print('dorsal',LM['tail_root_dorsal'].round(1),'ventral',LM['tail_root_ventral'].round(1),'trc',LM['tail_root_centre'].round(1))
def ev(nm,spec):
    T=R.pose(spec);P=R.skin(T);print('%-40s flips %4d dV %7.0f'%(nm,(R.relcos(P,T)<0).sum(),S.body_volume(P)-V0))
for ax,an in ((X,'vert'),(Z,'lat')):
  for deg in (25,-25):
    ev(an+' %d trc'%deg,[('tail_01',LM['tail_root_centre'],ax,deg)])
    ev(an+' %d head'%deg,[('tail_01',R.H('tail_01'),ax,deg)])
    ev(an+' %d dist3 heads'%deg,[('tail_%02d'%i,R.H('tail_%02d'%i),ax,deg/3) for i in (1,2,3)])
    ev(an+' %d pelvis-tail split'%deg,[('tail_01',R.H('tail_01'),ax,deg)])
