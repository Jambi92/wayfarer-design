import sys,numpy as np
from scipy.spatial.transform import Rotation as Rot
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001');import sa6_pose as SP,sa6_fit as FT,sa6_correctives as CC
def qmul(a,b):
    w1,x1,y1,z1=np.moveaxis(a,-1,0);w2,x2,y2,z2=np.moveaxis(b,-1,0)
    return np.stack([w1*w2-x1*x2-y1*y2-z1*z2,w1*x2+x1*w2+y1*z2-z1*y2,w1*y2-x1*z2+y1*w2+z1*x2,w1*z2+x1*y2-y1*x2+z1*w2],-1)
def dqs(R,T,P=None,W=None):
    P=R.V if P is None else P; W=R.W if W is None else W
    q=np.array([np.roll(Rot.from_matrix(T[b][0]).as_quat(),1) for b in R.DB]); t=np.array([T[b][1] for b in R.DB])
    d=0.5*qmul(np.c_[np.zeros(len(t)),t],q)
    # sign align to the vertex's dominant bone
    dom=W.argmax(1); s=np.sign((q[None]*q[dom][:,None]).sum(-1)); s[s==0]=1
    Wq=W*s; b0=Wq@q; be=Wq@d; n=np.linalg.norm(b0,axis=1,keepdims=True); b0/=n; be/=n
    w,v=b0[:,0:1],b0[:,1:]; we,ve=be[:,0:1],be[:,1:]
    rp=P+2*np.cross(v,np.cross(v,P)+w*P)
    tr=2*(w*ve-we*v+np.cross(v,ve))
    return rp+tr
if __name__=='__main__':
    R=SP.Rig('M',sys.argv[1]);PS=FT.pose_set(R);S=CC.Solver(R);V0=S.body_volume(R.V)
    for pn in ['shoulder_abd45_xpos','shoulder_abd90_xpos','shoulder_flex60_xpos','shoulder_abd90_xneg','elbow_130_xpos','hip_flex70_xpos','knee_90_xpos','neck_rot_40','neck_flex_30','trunk_twist_30','lower_axial_flex_25','tail_root_lateral_30','tail_root_vertical_25','tail_twist_30','hip_flex70_xpos_rp5lit','fist_xpos']:
        T=R.pose(PS[pn]);P0=R.skin(T);P1=dqs(R,T)
        print('%-24s LBS flips %4d dV %6.0f | DQS flips %4d dV %6.0f  maxdiff %.2f'%(pn,(R.relcos(P0,T)<0).sum(),S.body_volume(P0)-V0,(R.relcos(P1,T)<0).sum(),S.body_volume(P1)-V0,np.linalg.norm(P1-P0,axis=1).max()),flush=True)
