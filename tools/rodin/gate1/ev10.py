import numpy as np, json
from PIL import Image
z=np.load('g7_surf.npz'); disp=z['disp'].astype(float); r=np.load('g7reg.npz'); FAM=r['FAM']
base=np.load('g7up.npz')['V'].astype(float); x,f,u=base.T
names={1:'structural',2:'transitional articulation',3:'fine expressive',4:'ventral',5:'palmar/plantar contact (incl. pads)',6:'claw keratin (no scales)',7:'eye (pupil slit, nictitating fold)'}
acc={}
for k,nm in names.items():
    m=FAM==k; d=disp[m]
    acc[nm]=dict(verts=int(m.sum()),out_max_mm=round(float(d.max())*10,2),in_max_mm=round(float(-d.min())*10,2),mean_mm=round(float(d.mean())*10,3),rms_mm=round(float(np.sqrt((d*d).mean()))*10,3))
acc['_all']=dict(verts=len(disp),out_max_mm=round(float(disp.max())*10,2),in_max_mm=round(float(-disp.min())*10,2),mean_mm=round(float(disp.mean())*10,3),rms_mm=round(float(np.sqrt((disp*disp).mean()))*10,3))
V=z['V'].astype(float)
acc['_envelope']=dict(height=[round(float(np.ptp(V[:,2])),2),round(float(np.ptp(base[:,2])),2)],width=[round(float(np.ptp(V[:,0])),2),round(float(np.ptp(base[:,0])),2)],depth=[round(float(np.ptp(V[:,1])),2),round(float(np.ptp(base[:,1])),2)])
sil={}
for v in ('front','profile','rear','front34','rear34'):
    a=np.asarray(Image.open('E9_%s.png'%v).convert('RGBA'))[...,3]>127; b=np.asarray(Image.open('E10_%s.png'%v).convert('RGBA'))[...,3]>127
    sil[v]=dict(changed_px=int((a^b).sum()),silhouette_px=int(a.sum()),pct=round(100*float((a^b).sum())/a.sum(),3))
acc['_silhouette_vs_gate6']=sil
json.dump(acc,open('acct10.json','w'),indent=1); print(json.dumps(acc,indent=1))
