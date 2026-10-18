# Stage B v3: nail plates re-placed from toe geometry (centred on the toe, standard length), soft-edged raised plate + tip thickening
import numpy as np, sys, json; sys.path.insert(0,'/home/claude/aw1'); import aw1lib as L
ss=L.ss
FF=json.load(open('/home/claude/aw1/footframes.json'))
def plate(X,n,c):
    fr=L.FR[n]; big=n[1]=='1'; g=lambda k,d: c.get(k+('_big' if big else ''),c.get(k,d))
    a=np.array(FF[n[0]]['a']); p=np.array(FF[n[0]]['p'])
    b=L.nearest(fr['Pd'],None); dg=L.geo(b,0.03); S=np.isfinite(dg)
    ta=X@a; it=np.flatnonzero(S)[np.argmax(ta[S])]; T=X[it]          # frontmost point of this toe
    gu=L.geo(it,0.03); x=(X-T)@p; z=X[:,2]-T[2]
    near=np.isfinite(gu)&(gu<0.012); TW=np.percentile(x[near],95)-np.percentile(x[near],5)
    Ln=g('len',0.011); u=np.where(np.isfinite(gu),gu,1.0)
    hw=TW*g('hwf',0.36)*(g('tipw',0.45)+(1-g('tipw',0.45))*ss(np.clip(u/(Ln*g('tl',0.7)),0,1)))
    ed=c.get('edge',0.0012)
    w=(1-ss((np.abs(x)-(hw-ed))/ed))*(1-ss((u-(Ln-ed))/ed))*ss((z+c.get('zdrop',0.0015))/0.0015)
    vn=L.vnormals(X); up=vn@np.array([0,0,1.0])+0.8*(vn@a); w*=ss((up-0.1)/0.3)
    w*=(1-c.get('grow',0.4))+c.get('grow',0.4)*(1-np.clip(u/Ln,0,1))
    w[~np.isfinite(gu)]=0
    return w,dict(TW=float(TW),tipz=float(T[2]))
if __name__=='__main__':
    cfg=json.loads(sys.argv[1]); src=sys.argv[2]; tag=sys.argv[3]
    X0=np.load(src)['V']; H=np.zeros(len(X0)); info={}
    for n in L.FR:
        w,i=plate(X0,n,cfg); sc=cfg.get('bigh',1.0) if n[1]=='1' else 1.0; H=np.maximum(H,w*sc/max(cfg.get('bigh',1.0),1.0)); info[n]=i
    for _ in range(cfg.get('diff',1)): H=np.where(H>0,L.Avg@H,H) if False else L.Avg@H
    H[~np.load(cfg.get('support','support_c2.npy'))]=0; H[L.dup_left]=0; H=np.clip(H,0,1)
    M=1-H; hs=max(cfg.get('bigh',1.0),1.0); X=L.inflate(X0,M,cfg['height']*hs)
    np.save(f'MB_{tag}.npy',M); np.savez(f'{tag}_VF.npz',V=X,F=L.F); np.save(f'w{tag}.npy',H)
    print(tag,'max move %.2f'%(np.linalg.norm(X-X0,axis=1).max()*1000), json.dumps({k:{kk:round(vv*1000,1) for kk,vv in v.items()} for k,v in info.items()}))
