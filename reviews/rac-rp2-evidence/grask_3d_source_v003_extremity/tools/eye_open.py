# eye_open.py IN OUT PARAMS : minimal correction of generator-compressed eyes -- eyeball volume, upper/lower lid seating, narrow almond fissure
import sys, json, numpy as np, igl
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from cotfair import ss
from region_fair import region_fair
d=np.load(sys.argv[1]); X=d['V'].astype(float).copy(); F=d['Q'].astype(np.int64); n=len(X); Q4=np.c_[F,F[:,0]]
p=json.load(open(sys.argv[3])); keep=np.load(p['keep']) if p.get('keep') else np.zeros(n)
N=igl.per_vertex_normals(X,F)
X0=X.copy(); W=np.zeros(n); DF=np.zeros(n)
sys.path.insert(0,'/tmp/claude-0/rp2/tools'); from lowpass import lowpass
for sg in (1,-1):
    x=sg*X[:,0]; f=X[:,1]; z=X[:,2]
    x0,x1=p['canthi']; xc=(x0+x1)/2; hw=(x1-x0)/2; zf=p['fissure_z']+p['fissure_tilt']*(x-xc)/hw
    t=np.clip((x-x0)/(x1-x0),0,1); h=p['opening']*np.sin(np.pi*t)**0.8
    dx=(x-xc)/p['eye_rx']; dz=(z-p['fissure_z'])/p['eye_rz']
    q=np.clip(1-dx**2-dz**2,0,None)
    fe=p['eye_fc']+p['eye_rf']*np.sqrt(q)                       # eyeball front
    ql=np.clip(1-(dx*p['eye_rx']/(p['eye_rx']+p['lid']))**2-(dz*p['eye_rz']/(p['eye_rz']+p['lid']))**2,0,None)
    fl=p['eye_fc']+(p['eye_rf']+p['lid'])*np.sqrt(ql)          # lid surface over the eyeball
    up=zf+h/2; lo=zf-h/2
    inside=ss((up-z)/p.get('margin',0.04))*ss((z-lo)/p.get('margin',0.04))*(h>0.02)
    ft=fl*(1-inside)+fe*inside
    # region: almond-shaped orbit window, below the brow, forward-facing, not the brow itself
    xf=p.get('x_fall',0.35); wx=ss((x-(x0-xf))/xf)*(1-ss((x-(x1+xf))/xf))
    wz=ss((z-(zf-p['lower_extent']))/p.get('lower_fall',0.45))*(1-ss((z-(zf+p['upper_extent']))/0.12))
    w=wx*wz*np.clip((N[:,1]-p.get('nf_min',0.2))/0.3,0,1)*(f<p['brow_f_guard'])*(f>p['eye_fc']-0.5)*(1-keep)
    w*=(q>0)|(ql>0)
    DF+=w*np.clip(ft-f,-p.get('max_move',1.0),p.get('max_move',1.0))
    W=np.maximum(W,w)
DF=lowpass(Q4,n,DF[:,None],p.get('disp_lam',2.0))[:,0]
X[:,1]+=DF
# soften the outer transition only
edge=np.clip(W*(1-W)*4,0,1)
X=region_fair(X,Q4,edge*0.8,1.0,it=1)
if p.get('post_fair',0): X=region_fair(X,Q4,W*p['post_fair'],1.0,it=2)
out={k:d[k] for k in d.files}; out['V']=X; out['eye_move_mm']=np.linalg.norm(X-X0,axis=1)*10; out['eye_weight']=W
np.savez(sys.argv[2],**out); m=out['eye_move_mm']; print('eye move max %.2f p95 %.2f mm'%(m.max(),np.percentile(m[m>0.01],95)))
