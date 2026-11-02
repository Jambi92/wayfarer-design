import sys,numpy as np
from scipy.spatial.transform import Rotation as Rot, Slerp
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001');import sa6_pose as SP,sa6_fit as FT,sa6_correctives as CC
R=SP.Rig('M','/tmp/claude-0/rp6/W_M.npz');PS=FT.pose_set(R);S=CC.Solver(R);V0=S.body_volume(R.V)
HJ=sys.argv[1].split(',') if len(sys.argv)>1 else ['neck_01','tail_01','upperarm_l','upperarm_r','thigh_l','thigh_r','spine_01']
frac=float(sys.argv[2]) if len(sys.argv)>2 else 0.5
W=R.W.copy();cols=[]
for b in HJ:
    sub=[R.bi[x] for x in R.sub(b) if x in R.bi];a=W[:,sub].sum(1);c=1-a;wh=2*np.minimum(a,c)
    sa=np.where(a>0,(a-wh/2)/np.maximum(a,1e-12),0);sc=np.where(c>0,(c-wh/2)/np.maximum(c,1e-12),0)
    m=np.zeros(W.shape[1],bool);m[sub]=True;W[:,m]*=sa[:,None];W[:,~m]*=sc[:,None];W=np.c_[W,wh];cols.append(b)
def pose_h(spec):
    T=R.pose(spec);Ts=[]
    for b in HJ:
        p=R.par[b];Rp,tp=T[p];Rb,tb=T[b];Rl=Rp.T@Rb;h=Rot.from_matrix(Rl).as_rotvec()*frac;Rh=Rp@Rot.from_rotvec(h).as_matrix()
        piv=R.H(b);pivp=Rb@piv+tb;Ts.append((Rh,pivp-Rh@piv))
    return T,Ts
def skin(T,Ts):
    out=np.zeros_like(R.V);n=len(R.DB)
    for i,b in enumerate(R.DB):
        m=W[:,i]>0
        if m.any(): Rr,t=T[b];out[m]+=W[m,i:i+1]*(R.V[m]@Rr.T+t)
    for j,(Rr,t) in enumerate(Ts):
        m=W[:,n+j]>0
        if m.any(): out[m]+=W[m,n+j:n+j+1]*(R.V[m]@Rr.T+t)
    return out
for pn in ['shoulder_abd45_xpos','shoulder_abd90_xpos','shoulder_flex60_xpos','hip_flex70_xpos','knee_90_xpos','neck_rot_40','neck_flex_30','trunk_twist_30','lower_axial_flex_25','tail_root_lateral_30','tail_root_vertical_25','tail_twist_30','hip_flex70_xpos_rp5lit','elbow_130_xpos']:
    T,Ts=pose_h(PS[pn]);P0=R.skin(T);P1=skin(T,Ts)
    print('%-26s LBS flips %4d dV %6.0f | helper flips %4d dV %6.0f'%(pn,(R.relcos(P0,T)<0).sum(),S.body_volume(P0)-V0,(R.relcos(P1,T)<0).sum(),S.body_volume(P1)-V0),flush=True)
