import numpy as np, sys
p=sys.argv[1]; d=np.load(p.replace('.npz','_dsp.npy'))
for h,roles in [('R',{0:'middle',1:'ring',2:'index',3:'thumb',4:'pinky',9:'palm'}),('L',{0:'pinky',1:'thumb',2:'ring',3:'middle',4:'index',9:'palm'})]:
    q=np.load('segH_%s.npz'%h); u=q['used']; l=q['lab']
    for k,r in roles.items():
        x=d[u[l==k]]; print(h,r,'n',len(x),'over1.5 %.2f%%'%((x>1.5).mean()*100),'p95 %.2f max %.1f'%(np.percentile(x,95),x.max()))
