# ident_make.py PARAMS.json OUT.npz : identity-corrected production candidate.
#   body delta D (13 380) -> production: head region rebuilt as SS(H + D) (removes v001 lip/eyelid freeze artefacts),
#   elsewhere v001 + SS(D); then screened fairing inside the edited-region mask (outside: v001 unchanged).
import sys, json, subprocess, numpy as np
sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from ident_apply import SS
from region_fair import region_fair
R='/tmp/claude-0/rp2/'
pj=sys.argv[1]; out=sys.argv[2]; p=json.load(open(pj))
subprocess.run(['python3',R+'tools/ident_build.py',pj,out,'--base-only'],check=True)
D=np.load(out.replace('.npz','_D.npy')); H=np.load(R+'hstar.npz')['V']
P=dict(np.load(R+p.get('prod_base','cand_h4_12.npz'))); V0=P['V']; Q=P['Q']
Wb=dict(np.load(R+'weights_body.npz')); S=SS()
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
hw=S@(Wb['head']+Wb['ears']); ew=S@Wb['ears']
rh=ss((hw-0.15)/0.5)                                   # head rebuild weight
X=V0+S@D
X=X*(1-rh[:,None])+(S@(H+D))*rh[:,None]
dm=np.linalg.norm(S@D,axis=1)
e=np.r_[Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]
r=ss(dm/0.05)
for _ in range(6):                                     # dilate/smooth the edit mask a few rings
    s_=np.zeros(len(r)); c=np.zeros(len(r)); np.add.at(s_,e[:,0],r[e[:,1]]); np.add.at(s_,e[:,1],r[e[:,0]]); np.add.at(c,e[:,0],1); np.add.at(c,e[:,1],1); r=np.maximum(r,s_/c)
r=np.maximum(r,rh)
fm=np.maximum(rh, ss((S@(Wb['hand_l']+Wb['hand_r']+Wb['fingers_l']+Wb['fingers_r']+Wb['foot_l']+Wb['foot_r']+Wb['ball_l']+Wb['ball_r'])-0.05)/0.4))
for _ in range(4):
    s_=np.zeros(len(fm)); c=np.zeros(len(fm)); np.add.at(s_,e[:,0],fm[e[:,1]]); np.add.at(s_,e[:,1],fm[e[:,0]]); np.add.at(c,e[:,0],1); np.add.at(c,e[:,1],1); fm=np.maximum(fm,s_/c)
lam=p.get('fair_lam',3.0)
rr=fm*(1-p.get('ear_keep',0.6)*ss(ew/0.5))
X=region_fair(X,Q,rr,lam,it=p.get('fair_it',2))
P['V']=X; P['edit_mask']=r; P['fair_mask']=fm; np.savez(out,**P)
print('faired verts %d, edited verts (r>0.5) %d, max prod delta from v001 %.2f cm'%((fm>0.5).sum(),(r>0.5).sum(),np.linalg.norm(X-V0,axis=1).max()))
