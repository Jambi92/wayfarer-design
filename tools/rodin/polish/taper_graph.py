import numpy as np, json, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def L(fn):
    x=np.load(fn); x=x[~np.isnan(x[:,1])]; return np.stack([x[:,0],x[:,1],np.sqrt(x[:,1]/np.pi)],1)
a=L('sl_g6.npy'); b=L('sl_g12.npy'); T=np.load('taper_target.npy')   # true planar sections perpendicular to the axis; T=np.load('taper_target.npy')
z0=np.load('/tmp/claude-0/rodin/g1/g9_body.npz'); z1=np.load('g12_body.npz'); C=np.load('/tmp/claude-0/rodin/g8/axis.npy')
V0=z0['V']; V1=z1['V']; MV=z1['MV'] if 'MV' in z1.files else None
fig,ax=plt.subplots(1,3,figsize=(21,6.2),dpi=110); fig.patch.set_facecolor('#1b1b20')
for x in ax: x.set_facecolor('#24242a'); x.tick_params(colors='#ccc'); [s.set_color('#666') for s in x.spines.values()]; x.grid(color='#3a3a44')
def d(s,y): return s[1:-1],(y[2:]-y[:-2])/(s[2:]-s[:-2])
ax[0].plot(a[:,0],a[:,2],color='#e07a5f',lw=2.2,label='Gate 8 / current'); ax[0].plot(b[:,0],b[:,2],color='#81b29a',lw=2.2,label='Polish'); ax[0].plot(T[:,0],T[:,2],'--',color='#f2cc8f',lw=1.2,label='design target (outline-radius measure)')
ax[0].set_title('Equivalent radius  r_eq = sqrt(A/π)  (planar sections perpendicular to axis)',color='w'); ax[0].set_xlabel('arc length from tail tip s (cm)  →  sacral base',color='#ccc'); ax[0].set_ylabel('cm',color='#ccc')
ax[1].plot(a[:,0],a[:,1],color='#e07a5f',lw=2.2); ax[1].plot(b[:,0],b[:,1],color='#81b29a',lw=2.2); ax[1].set_title('Cross-sectional area A(s)',color='w'); ax[1].set_xlabel('s (cm)',color='#ccc'); ax[1].set_ylabel('cm²',color='#ccc')
s,da=d(a[:,0],a[:,1]); s2,db=d(b[:,0],b[:,1])
from scipy.ndimage import uniform_filter1d
ax[2].plot(s,uniform_filter1d(da,3),color='#e07a5f',lw=2.0); ax[2].plot(s2,uniform_filter1d(db,3),color='#81b29a',lw=2.0); ax[2].set_title('dA/ds (taper rate)',color='w'); ax[2].set_xlabel('s (cm)',color='#ccc'); ax[2].set_ylabel('cm²/cm',color='#ccc')
for x in ax: x.axvspan(98,110,color='#555',alpha=0.35); x.axvspan(0,12,color='#555',alpha=0.35)
ax[0].legend(facecolor='#2a2a30',labelcolor='w'); ax[0].text(99,2,'root\nunchanged',color='#bbb',fontsize=9); ax[0].text(1,9,'terminal\ntaper\nunchanged',color='#bbb',fontsize=9)
plt.tight_layout(); plt.savefig('taper_graph.png',facecolor=fig.get_facecolor())
# numbers
m=(a[:,0]>=12)&(a[:,0]<=98); mb=(b[:,0]>=12)&(b[:,0]<=98)
vol0=np.trapz(a[m,1],a[m,0]); vol1=np.trapz(b[mb,1],b[mb,0])
tip0=V0[np.argmin(V0[:,1])]; tip1=V1[np.argmin(V1[:,1])]
# tail length along axis = station of the tip (axis unchanged); tail-vertex arc extent
res=dict(volume_s12_98_cm3=[round(float(vol0),0),round(float(vol1),0)],volume_change_pct=round(100*(vol1-vol0)/vol0,2),
 tail_tip_gate6=tip0.round(3).tolist(),tail_tip_polish=tip1.round(3).tolist(),tail_tip_shift_cm=round(float(np.linalg.norm(tip1-tip0)),4),
 max_dA_ds_gate6=round(float(np.abs(da[(s>12)&(s<98)]).max()),1),max_dA_ds_polish=round(float(np.abs(db[(s2>12)&(s2<98)]).max()),1),
 max_d2r_gate6=round(float(np.abs(np.diff(a[m,2],2)).max()/0.25),3),max_d2r_polish=round(float(np.abs(np.diff(b[mb,2],2)).max()/0.25),3),
 root_req_s100_gate6=round(float(np.interp(100,a[:,0],a[:,2])),3),root_req_s100_polish=round(float(np.interp(100,b[:,0],b[:,2])),3),
 tail_max_move_cm=round(float(MV.max()),2) if MV is not None else None)
json.dump(res,open('taper.json','w'),indent=1); print(json.dumps(res,indent=1))
