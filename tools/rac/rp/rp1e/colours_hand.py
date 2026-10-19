import numpy as np
w=np.load('/home/claude/stc/rp1/weld.npz'); n=len(w['V'])
col=np.ones(n,int)
roles={'R':{0:'middle',1:'ring',2:'index',3:'thumb',4:'pinky'},'L':{0:'pinky',1:'thumb',2:'ring',3:'middle',4:'index'}}
for s in 'RL':
    z=np.load('segH_%s.npz'%s); used=z['used']; lab=z['lab']
    for k in range(5): col[used[lab==k]]=4 if roles[s][k] in ('index','ring') else (5 if roles[s][k]=='thumb' else 3)
    col[used[lab==9]]=3
np.save('col_handtest.npy',col)
