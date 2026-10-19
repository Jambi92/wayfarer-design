import numpy as np
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V']; n=len(V)
col=np.ones(n,int)
for k in ['upperarm_L','forearm_L','upperarm_R','forearm_R','thigh_L','shin_L','thigh_R','shin_R']: col[w['w_'+k]>0.5]=2
for k in ['foot_L','foot_R']: col[w['w_'+k]>0.5]=3
col[(w['w_trunk']>0.5)&(V[:,2]>183.4)]=2      # head+neck above neck_min
roles={'R':{0:'middle',1:'ring',2:'index',3:'thumb',4:'pinky'},'L':{0:'pinky',1:'thumb',2:'ring',3:'middle',4:'index'}}
for s in 'RL':
    z=np.load('segH_%s.npz'%s); used=z['used']; lab=z['lab']
    for k in range(5): col[used[lab==k]]=4 if roles[s][k] in ('index','ring') else (5 if roles[s][k]=='thumb' else 3)
    col[used[lab==9]]=3
np.save('col_full.npy',col); print(np.bincount(col))
