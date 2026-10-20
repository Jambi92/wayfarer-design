import numpy as np, sys, igl
S=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); tag=sys.argv[1]; d=np.load('sim_%s_L4_dsp.npy'%tag)
c=np.array(eval(sys.argv[2])); R=float(sys.argv[3]); lim=float(sys.argv[4]) if len(sys.argv)>4 else 1.5
m=(np.linalg.norm(S-c,axis=1)<R)&(d>lim); P=S[m]; dd=d[m]
u,s,vt=np.linalg.svd(P-P.mean(0)); t=vt[0]; q=(P-P.mean(0))@t
z=np.load('sim_%s_L4.npz'%tag); V=z['V'].astype(float).copy(); V[:,1]*=-1; F=z['F'].astype(np.int64)
for b in np.linspace(q.min(),q.max(),8):
    k=np.abs(q-b)<(q.max()-q.min())/14
    if k.sum()==0: continue
    i=np.argmax(np.where(k,dd,-1)); f=P[i]
    _,_,cp=igl.point_mesh_squared_distance(f[None],V,F); o=cp[0]-f; print(np.round(f,2).tolist(), round(float(dd[i]),2),'out',np.round(o/np.linalg.norm(o),2).tolist())
print('t',t.round(2))
