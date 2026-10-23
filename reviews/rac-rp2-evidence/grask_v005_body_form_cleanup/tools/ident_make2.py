# ident_make2.py PARAMS.json OUT.npz : identity-corrected production candidate, procedural maps evaluated at production resolution.
#  1 base     : production v001 geometry; head region rebuilt from SS(H) (removes v001 lip/eyelid freeze artefacts)
#  2 targets  : MakeHuman CC0 hm08 targets + ear cartilage relief, defined on the 13 380 body, transferred by SS
#  3 warps    : craniofacial warp, ear late-taper warp, hands, feet, limb breadth profiles, trunk, bony relief: evaluated per production vertex
#  4 fairing  : screened smoothing inside head / hands / feet masks (outside unchanged)
import sys, json, numpy as np, igl
sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from ident_apply import SS
from region_fair import region_fair
from ident_targets import compose
import ident_head as IH, ident_body as IB
R='/tmp/claude-0/rp2/'
p=json.load(open(sys.argv[1])); out=sys.argv[2]
H=np.load(R+'hstar.npz'); HV=H['V'].astype(float); HQ=H['Q']
P=dict(np.load(R+p.get('prod_base','cand_h4_12.npz'))); V0=P['V'].astype(float); Q=P['Q']
Wb={k:v for k,v in np.load(R+'weights_body.npz').items()}; S=SS(); W2={k:S@v for k,v in Wb.items()}
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
def nrm(V,Q): T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]; return -igl.per_vertex_normals(V,T)
# 1
rh=ss((W2['head']+W2['ears']-0.15)/0.5)
X=V0*(1-rh[:,None])+(S@HV)*rh[:,None]
if p.get('head_fair_lam') and p.get('fair_head_first',False):
    g=lambda c,sg: np.exp(-0.5*(((X-np.array(c))/np.array(sg))**2).sum(1))
    lip=g((0,18.0,195.3),(3.0,2.0,1.4)); eye=np.maximum(g((3.4,14.5,204.9),(1.8,1.5,1.0)),g((-3.4,14.5,204.9),(1.8,1.5,1.0)))
    keep0=(1-0.95*ss((X[:,2]-208)/4))
    rf=rh*keep0*(1-ss(W2['ears']/0.4))*(1-p.get('lip_keep',0.75)*lip)*(1-p.get('eye_keep',0.7)*eye)
    X=region_fair(X,Q,rf,p['head_fair_lam'],it=p.get('head_fair_it',3))
# 2
Dt=compose(p.get('targets',{})) if p.get('targets') else np.zeros_like(HV)
Db=HV+Dt
if p.get('ear_relief'):
    Nb=nrm(Db,HQ); Dh=IH.head_delta(Db,Wb,Nb,p['head']) if p.get('head') else 0; Dbb=Db+Dh
    for s_ in (1,-1): Dbb=Dbb+IH.ear_delta(Dbb,Wb,p['ear'],s_)
    Dt=Dt+IH.relief(Dbb,HQ,IH.ss(Wb['ears']/0.9),p['ear_relief'])
Dt2=S@Dt
if p.get('target_lowpass'):
    from lowpass import lowpass
    ew2=ss(W2['ears']/0.4)
    Dt2=Dt2*ew2[:,None]+lowpass(Q,len(X),Dt2,p['target_lowpass'])*(1-ew2)[:,None]
X=X+Dt2
# 3
N=nrm(X,Q)
if p.get('head'): X=X+IH.head_delta(X,W2,N,p['head'])
if p.get('ear'):
    for s_ in (1,-1): X=X+IH.ear_delta(X,W2,p['ear'],s_)
if p.get('head_scale'):     # small overall head-mass increase: x/f about the head centre, z down from the crown (stature kept); blended by head weight
    sxy,sz=p['head_scale']; hw=IH.ss(np.clip(W2['head']+W2['ears'],0,1)/0.9)
    ctr=np.array([0.0,X[hw>0.9,1].mean(),X[:,2].max()]); Dh=np.zeros_like(X)
    Dh[:,0]=(sxy-1)*(X[:,0]-ctr[0]); Dh[:,1]=(sxy-1)*(X[:,1]-ctr[1]); Dh[:,2]=(sz-1)*(X[:,2]-ctr[2])
    X=X+hw[:,None]*Dh
N=nrm(X,Q)
if p.get('body'):
    bp=dict(p['body']); macro_keys=('arm_shift','profile','torso','trunk_zones','macro_extra','trunk_field','masses')
    pm={k:bp[k] for k in macro_keys if k in bp}; pd={k:v for k,v in bp.items() if k not in macro_keys}
    if 'macro_extra' in pm: pm['relief']={'bumps':{},'extra':pm.pop('macro_extra')}
    if 'trunk_field' in pm and pm['trunk_field'].get('smooth_it'):
        from lowpass import lowpass as _lp
        IB._XS=_lp(Q,len(X),X,pm['trunk_field']['smooth_it'])
    if pm.get('profile',{}).get('_smooth_lam'):
        from lowpass import lowpass as _lp
        IB._XSL=_lp(Q,len(X),X,pm['profile']['_smooth_lam'])
    Dm=IB.body_delta(X,W2,N,pm); IB._XS=None; IB._XSL=None
    if p.get('macro_lowpass'):
        from lowpass import lowpass
        Dm=lowpass(Q,len(X),Dm,p['macro_lowpass'])
    X=X+Dm+IB.body_delta(X,W2,N,pd)
# 4
e=np.r_[Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]
def dil(m,k):
    for _ in range(k):
        s_=np.zeros(len(m)); c=np.zeros(len(m)); np.add.at(s_,e[:,0],m[e[:,1]]); np.add.at(s_,e[:,1],m[e[:,0]]); np.add.at(c,e[:,0],1); np.add.at(c,e[:,1],1); m=np.maximum(m,s_/c)
    return m
ext=W2['hand_l']+W2['hand_r']+W2['fingers_l']+W2['fingers_r']+W2['foot_l']+W2['foot_r']+W2['ball_l']+W2['ball_r']
zz=X[:,2]; dh=np.sqrt(X[:,0]**2+(0.8*(X[:,1]-3.0))**2)
neckz=ss((zz-168)/5)*(1-ss((dh-11)/3))
fm=dil(np.maximum(np.maximum(rh,ss((ext-0.05)/0.4)),neckz),4)
rr=fm*(1-p.get('ear_keep',0.6)*ss(W2['ears']/0.5))*np.where(ext>0.05,p.get('ext_fair',1.0),1.0)
keep=(1-0.95*ss((X[:,2]-208)/4))*(1-0.95*ss((2.5-X[:,2])/2))     # cranial vault and sole kept (stature / ground contact)
rr=rr*keep
if p.get('fair_head_first',False): rr=rr*(1-rh*(1-ss(W2['ears']/0.4))*0.85)
X=region_fair(X,Q,rr,p.get('fair_lam',3.0),it=p.get('fair_it',2))
if p.get('head_fair_lam') and not p.get('fair_head_first',False):     # extra facet removal on the face (E3 13k facets reproduced densely), ears protected
    g=lambda c,sg: np.exp(-0.5*(((X-np.array(c))/np.array(sg))**2).sum(1))
    lip=g((0,18.0,193.8),(3.0,2.0,1.4)); eye=np.maximum(g((3.4,14.5,204.4),(1.8,1.5,1.0)),g((-3.4,14.5,204.4),(1.8,1.5,1.0)))
    rf=rh*keep*(1-ss(W2['ears']/0.4))*(1-p.get('lip_keep',0.75)*lip)*(1-p.get('eye_keep',0.7)*eye)
    X=region_fair(X,Q,rf,p['head_fair_lam'],it=p.get('head_fair_it',3))
def cot_fair(P0,Q,r,lam,it=2):
    """geometric (cotangent / mass-matrix) screened fairing inside mask r: (M - lam R L) X = M X0 ; lam in cm^2"""
    import scipy.sparse as sp
    from scipy.sparse.linalg import splu
    F=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]].astype(np.int64); Xc=P0.astype(float)
    for _ in range(it):
        L=igl.cotmatrix(Xc,F); M=igl.massmatrix(Xc,F,igl.MASSMATRIX_TYPE_VORONOI)
        A=(M-lam*sp.diags(r)@L).tocsc(); lu=splu(A); B=M@Xc
        Xn=np.stack([lu.solve(B[:,j]) for j in range(3)],1)
        Xc=Xn
    return Xc
for lf in p.get('local_fair',[]):      # localized fairing of specific secondary forms: [x,f,z,r,lam] (mirrored when x != 0)
    x_,f_,z_,r_,lam_=lf; w_=np.zeros(len(X))
    for sg_ in ((1,-1) if abs(x_)>1e-6 else (1,)): w_=np.maximum(w_,np.exp(-0.5*(np.linalg.norm(X-np.array([sg_*x_,f_,z_]),axis=1)/r_)**2))
    X=cot_fair(X,Q,w_*(w_>0.002),lam_,it=2) if p.get('local_fair_cot') else region_fair(X,Q,w_*(w_>0.002),lam_,it=2)
dm=np.linalg.norm(X-V0,axis=1); P['V']=X; P['fair_mask']=fm; P['edit_mask']=dil(ss(dm/0.05),2)
np.savez(out,**P); print('faired %d, edited (>0.5mm) %d, max delta %.2f cm'%((fm>0.5).sum(),(dm>0.05).sum(),dm.max()))
