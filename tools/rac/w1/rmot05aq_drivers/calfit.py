import sys; sys.path.insert(0,'/home/claude/aq'); import numpy as np, aqsim as A
V0=np.load('/home/claude/ao/ao2/ao2_VF.npz')['V']; F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; R=np.load(sys.argv[1]); V=R['V']; M=np.load('/home/claude/aq/mask_aq_c8_n150.npy')
d=V-V0; N=A.vnormals(V0,F); f=1-M; s=f>0.05
proj=(d*N).sum(1); tang=np.linalg.norm(d-proj[:,None]*N,axis=1)
c=(proj[s]*f[s]).sum()/(f[s]**2).sum(); res=proj[s]-c*f[s]
print('mask unchanged',np.abs(R['M']-M).max(),'max |d| mm',np.linalg.norm(d,axis=1).max()*1000,'masked(M=1) max mm',np.linalg.norm(d[M>=1],axis=1).max()*1000)
print('fit c (mm per unit fade)',c*1000,'corr',np.corrcoef(proj[s],f[s])[0,1],'resid rms mm',np.sqrt((res**2).mean())*1000,'tangential p95 mm',np.percentile(tang[s],95)*1000)
