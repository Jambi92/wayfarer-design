# refine2.py IN OUT PARAMS_JSON : v002 refinement = symmetry of major masses + glute/pelvis rebuild + multi-band neutral cleanup + finger mass
import sys, json, numpy as np, igl
from scipy.sparse.linalg import factorized
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from lowpass import lowpass
from cotfair import ss
d=np.load(sys.argv[1]); X=d['V'].astype(float); F=d['Q'].astype(np.int64); Q4=np.c_[F,F[:,0]]; n=len(X)
p=json.loads(open(sys.argv[3]).read()); keep=np.load(p['keep']) if p.get('keep') else np.zeros(n)
masks={}
def regions(X):
    x,f,z=X.T; ax=np.abs(x)
    R={}
    R['head']=ss((z-188)/3)
    R['face']=R['head']*(1-ss((ax-9)/3))
    R['ear']=np.maximum(ss((ax-6.0)/1.5)*ss((z-193)/2)*(1-ss((z-214)/2)),ss((z-189)/3)*ss((ax-5.5)/1.5))
    R['hand']=ss((ax-21)/2)*ss((114-z)/3)*ss((z-62)/3)
    R['finger']=R['hand']*ss((88-z)/2)
    R['foot']=ss((13-z)/2)
    R['toe']=R['foot']*ss((f-p.get('toe_f',16))/1.5)*(1-ss((z-p.get('toe_z',99))/1.0))
    R['torso']=ss((z-108)/4)*(1-ss((z-186)/3))*(1-ss((ax-18.5)/1.5))
    R['pelvis']=ss((z-92)/3)*(1-ss((z-130)/4))*(1-ss((ax-18)/2))
    R['cheek']=np.exp(-0.5*(((ax-p.get('ck',[7.2,2.5,195.5])[0])/1.6)**2+((f-p.get('ck',[7.2,2.5,195.5])[1])/3.0)**2+((z-p.get('ck',[7.2,2.5,195.5])[2])/4.0)**2))
    return R
R=regions(X)
# ---- 1. symmetry of major masses (head, ears, torso, pelvis): average with the mirrored surface, smoothed displacement
if p.get('sym',1):
    Xm=X*np.array([-1,1,1]); Fm=F[:,[0,2,1]]
    _,I,C=igl.point_mesh_squared_distance(X,Xm,Fm)
    N=igl.per_vertex_normals(X,F); Nm=igl.per_face_normals(Xm,Fm,np.array([0,0,1.0]))[I]
    ok=(np.einsum('ij,ij->i',N,Nm)>0.6)&(np.linalg.norm(C-X,axis=1)<p.get('sym_maxd',2.5))
    D=lowpass(Q4,n,(C-X)*ok[:,None],p.get('sym_lam',25.0),w=ok*1.0+0.02)
    w=np.clip(np.maximum.reduce([R['head'],R['torso'],R['pelvis']*0.8]),0,1)*(1-R['hand'])*(1-keep)*(1-p.get('sym_skip_ear',0)*ss((np.abs(X[:,0])-7.8)/0.6))
    X=X+0.5*w[:,None]*D; masks['symmetry_move_mm']=np.linalg.norm(0.5*w[:,None]*D,axis=1)*10
    print('sym: ok %.2f  move p95 %.2f max %.2f mm'%(ok.mean(),np.percentile(masks['symmetry_move_mm'],95),masks['symmetry_move_mm'].max()))
# ---- 1b. local mirror spots: replace one side's local generator deformity by the mirrored other side
for k_,sp_ in enumerate(p.get('mirror_spots',[])):
    sg=sp_[6]; r_=np.exp(-0.5*(((X[:,0]-sg*sp_[0])/sp_[3])**2+((X[:,1]-sp_[1])/sp_[4])**2+((X[:,2]-sp_[2])/sp_[5])**2))*(sg*X[:,0]>0)
    Xm=X*np.array([-1,1,1]); _,I,C=igl.point_mesh_squared_distance(X,Xm,F[:,[0,2,1]])
    D=lowpass(Q4,n,(C-X),2.0)
    X=X+(r_*(1-keep))[:,None]*D; masks['mirror_spot%d_move_mm'%k_]=np.linalg.norm(r_[:,None]*D,axis=1)*10
    print('mirror spot',k_,'max move mm %.2f'%masks['mirror_spot%d_move_mm'%k_].max())
# ---- 2. glute mass / gluteal fold (pelvis F)
G=p.get('glute',{})
if G:
    x,f,z=X.T; N=igl.per_vertex_normals(X,F)
    zc=G['zc']; dz=z-zc; sz=np.where(dz<0,G['sz_lo'],G['sz_hi'])
    g=sum(np.exp(-0.5*((x-s*G['xc'])/G['sx'])**2) for s in (1,-1))*np.exp(-0.5*(dz/sz)**2)
    g*=1-G.get('cleft',0.6)*np.exp(-0.5*(x/1.6)**2)
    post=np.clip(-N[:,1],0,1)**0.7*ss((-f-2)/2)
    disp=-G['A']*g*post*(1-keep)
    X=X+np.c_[np.zeros(n),disp,np.zeros(n)]; masks['glute_move_mm']=np.abs(disp)*10
    print('glute max move %.2f cm'%np.abs(disp).max())
    from region_fair import region_fair
    r=np.clip(np.abs(disp)/0.3,0,1); X=region_fair(X,Q4,r,4.0,it=1)
# ---- 3. multi-band neutral cleanup
L=igl.cotmatrix(X,F); M=igl.massmatrix(X,F,igl.MASSMATRIX_TYPE_BARYCENTRIC)
def smooth(lam):
    s=factorized((M-lam*L).tocsc()); B=M@X; return np.stack([s(B[:,j]) for j in range(3)],1)
S1=smooth(p['lam'][0]); S2=smooth(p['lam'][1]); S3=smooth(p['lam'][2])
lo=lambda A: A-lowpass(Q4,n,A,100.0)
bf=lo(X-S1); bm=lo(S1-S2); bl=lo(S2-S3)
R=regions(X)
def gain(k):
    g=p['gain']; b=np.ones(n)*g['body'][k]
    for reg in ('torso','pelvis','foot','toe','hand','finger','face','ear')+(('cheek',) if 'cheek' in g else ()):
        b=b+(g[reg][k]-b)*R[reg]
    return b+(1-b)*keep
af,am,al=gain(0),gain(1),gain(2)
Y=X-(1-af)[:,None]*bf-(1-am)[:,None]*bm-(1-al)[:,None]*bl
masks['neutral_v2_move_mm']=np.linalg.norm(Y-X,axis=1)*10; X=Y
# ---- 3b. cheek hollow fair (generator crease under the zygoma)
if p.get('cheek_fair',0):
    R=regions(X); from region_fair import region_fair
    X=region_fair(X,Q4,np.clip(R['cheek']*1.3,0,1)*(1-keep),p['cheek_fair'],it=2); masks['cheek_fair_weight']=R['cheek']
for k_,sp_ in enumerate(p.get('fair_spots',[])):
    from region_fair import region_fair
    ax_=np.abs(X[:,0]); r_=np.exp(-0.5*(((ax_-sp_[0])/sp_[3])**2+((X[:,1]-sp_[1])/sp_[4])**2+((X[:,2]-sp_[2])/sp_[5])**2))
    X=region_fair(X,Q4,np.clip(r_*1.3,0,1)*(1-keep),sp_[6],it=2); masks['fair_spot%d_weight'%k_]=r_
# ---- 4. finger mass (troll fingers: not delicate)
if p.get('finger_inflate',0):
    N=igl.per_vertex_normals(X,F); R=regions(X); w=R['finger']*(1-keep)
    w=lowpass(Q4,n,w[:,None],4.0)[:,0]
    X=X+p['finger_inflate']*w[:,None]*N; masks['finger_inflate_mm']=p['finger_inflate']*w*10
# ---- 5. ground + canonical height
X[:,2]-=X[:,2].min(); s=218.0/X[:,2].max(); X*=s
print('height rescale %.6f'%s)
np.savez(sys.argv[2],V=X,Q=F,**masks)
