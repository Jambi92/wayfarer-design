import numpy as np, json, sys
a=np.load('ui_v005.npz')['V']; b=np.load(sys.argv[1])['V']
mv={int(k):np.array(v) for k,v in json.load(open('ui_moves_e30.json')).items()}
d=np.linalg.norm(a-b,axis=1); ch=np.where(d>0.005)[0]
done=[k for k in ch if k in mv and np.linalg.norm(b[k]-mv[k])<0.01]
bad=[k for k in ch if k not in done]
print('changed',len(ch),'done ok',len(done),'bad',[(int(k), a[k].round(2).tolist(), b[k].round(2).tolist()) for k in bad])
