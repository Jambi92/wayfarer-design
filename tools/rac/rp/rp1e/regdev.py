import numpy as np, sys
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V']
box=np.array([float(v) for v in sys.argv[1].split(',')]).reshape(3,2)
m=((V>box[:,0])&(V<box[:,1])).all(1)
for p in sys.argv[2:]:
    d=np.load(p)[m]; print(p,'n',m.sum(),'median %.2f p95 %.2f max %.1f  over1.5 %.1f%%  over3 %.1f%%'%(np.median(d),np.percentile(d,95),d.max(),(d>1.5).mean()*100,(d>3).mean()*100))
