# dome-sheath Stage B: masked inflate (dome height field) + translation/curl hook (no lateral pinch) + masked smooth
import numpy as np, sys, json, pickle; sys.path.insert(0,'/home/claude/aw1'); sys.path.insert(0,'/home/claude/aw'); import aw1lib as L
from nails2 import empty_mat, apply_hook, YAW
from stageB import shield
ss=L.ss
def diffuse(h,k,lim):
    for _ in range(k): h=np.where(lim,L.Avg@h,h)
    return h
def dome(X,n,hwf,taper,s_end,diff,edge=None,root=0.25,keel=None,grow=0.0):
    w,s=shield(X,n,s_end=s_end,taper=taper,hw_frac=hwf,edge=0.0008)
    fr=L.FR[n]; x=(X-fr['Pp'])@fr['lat']
    hw=fr['W']*hwf*np.clip(1-taper*np.clip(s,0,None)**1.5/(s_end**1.5),0.08,1)
    prof=ss((s+0.05)/root)*(1-ss((s-s_end)/0.12))
    if edge: h=(1-ss((np.abs(x)-(hw-edge))/edge))*prof
    elif keel: u=np.clip(np.abs(x)/hw,0,1); h=(1-u**2)**keel*prof
    else: u=np.clip(np.abs(x)/hw,0,1); h=(1-u**2)*prof
    if grow: h=h*((1-grow)+grow*ss(np.clip(s,0,None)/s_end))
    h[(s<-0.5)|(s>s_end+0.3)]=0; h[~np.isfinite(s)]=0
    lim=(s>-0.6)&(s<s_end+0.5)&(np.abs(x)<fr['W']*0.9)
    h=diffuse(h,diff,lim); return h/max(h.max(),1e-9), s, lim
if __name__=='__main__':
    cfg=json.loads(sys.argv[1]); src=sys.argv[2]; tag=sys.argv[3]
    X0=np.load(src)['V']; X=X0.copy(); H=np.zeros(len(X)); info={}; LIM=np.zeros(len(X),bool)
    for n in L.FR:
        h,s,lim=dome(X,n,cfg['hwf']*(cfg.get('bighwf',1.0) if n[1]=='1' else 1.0),cfg.get('bigtaper',cfg['taper']) if n[1]=='1' else cfg['taper'],cfg.get('s_end',1.15),cfg.get('diff',6),cfg.get('edge'),cfg.get('root',0.25),cfg.get('keel'),cfg.get('grow',0.0)); sc=cfg.get('bigh',1.0) if n[1]=='1' else 1.0; h=h*sc; info[n]=(h,s); H=np.maximum(H,h); LIM|=lim
    H[L.dup_left]=0
    if cfg.get('support'): H[~np.load(cfg['support'])]=0
    hs=max(cfg.get('bigh',1.0),1.0); H=H/hs
    M=1-H; X=L.inflate(X,M,cfg['height']*hs)
    hk=cfg.get('hook')
    if hk:
        for n in L.FR:
            h,s=info[n]; fr=L.FR[n]; wh=np.clip(h,0,1)*np.clip(s/1.15,0,1)**hk.get('pow',2); wh[L.dup_left]=0
            loc0=np.round(fr['Pp'],5); M0=empty_mat(loc0,[0,0,YAW[n[0]]],[1,1,1])
            M1=empty_mat(np.round(loc0+fr['e']*hk['te']+fr['n']*hk['tn'],5),[hk['curl'],0,YAW[n[0]]],[hk.get('sx',1.0),1,1]); X=apply_hook(X,wh,M0,M1)
    if cfg.get('smooth'):
        Ms=1-np.clip(diffuse(H,6,LIM)*1.5,0,1); Ms[L.dup_left]=1; X=L.smooth(X,Ms,cfg['smooth'])
    np.save(f'MB_{tag}.npy',M); np.savez(f'{tag}_VF.npz',V=X,F=L.F)
    print(tag,'max move %.2f mm'%(np.linalg.norm(X-X0,axis=1).max()*1000))
