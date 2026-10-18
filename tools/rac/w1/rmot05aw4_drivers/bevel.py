import numpy as np, sys, json; sys.path.insert(0,'/home/claude/aw1'); sys.path.insert(0,'/home/claude/aw1/aw4')
import aw1lib as L; from fields import multigeo, ss
c=json.loads(sys.argv[1]); src=sys.argv[2]; tag=sys.argv[3]
X0=np.load(src)['V']; PL=np.load('plates.npy',allow_pickle=True).item(); sup=np.load('support_S.npy')
w=np.zeros(len(X0))
for n,P in PL.items():
    H=P['w']; inside=H>0.5
    din=multigeo(~inside & P['dom'],0.004); dout=multigeo(inside,0.004)
    din=np.nan_to_num(din,posinf=1); dout=np.nan_to_num(dout,posinf=1)
    d=np.where(inside,-din,dout)          # signed: <0 inside plate, >0 outside
    r=ss((d+c.get('in',0.0007))/c.get('ramp',0.0004))*(1-ss((d-c.get('out',0.0004))/c.get('ramp',0.0004)))
    r*=ss((P['up']/P['Ln']-c.get('tip0',0.3))/0.1)      # leave distal free edge crisp
    if n[1]=='1' and c.get('big',1)==0: r*=0
    w=np.maximum(w,r)
w[~sup]=0; w[L.dup_left]=0; M=1-w
X=L.smooth(X0,M,c.get('n',20)) if not c.get('hc') else L.hc_smooth(X0,M,c['n'],alpha=0.0,beta=0.6)
np.save(f'MA_{tag}.npy',M); np.savez(f'A_{tag}_VF.npz',V=X,F=L.F)
print(tag,'max mm %.3f n %d'%(np.linalg.norm(X-X0,axis=1).max()*1000,(w>0.01).sum()))
