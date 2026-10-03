# Gate 7 closure accounting: closure vs diagnostic vs frozen Gate 6
import numpy as np, json
from PIL import Image
base=np.load('g7up.npz'); V0=base['V'].astype(float); F=base['F']
D=np.load('g7_surf.npz'); C=np.load('g7_surfc.npz'); rd=np.load('g7reg.npz'); rc=np.load('g7regc.npz')
Vd=D['V'].astype(float); Vc=C['V'].astype(float); dd=D['disp'].astype(float); dc=C['disp'].astype(float); FAM=rc['FAM']
names={1:'structural',2:'transitional articulation',3:'fine expressive',4:'ventral',5:'palmar/plantar contact (incl. pads)',6:'claw keratin',7:'eye'}
st=lambda d:dict(out_max_mm=round(float(d.max())*10,2),in_max_mm=round(float(-d.min())*10,2),mean_mm=round(float(d.mean())*10,3),rms_mm=round(float(np.sqrt((d*d).mean()))*10,3))
acc={'closure_relief_vs_gate6':{},'closure_vs_diagnostic':{}}
mv=np.linalg.norm(Vc-Vd,axis=1)*10
for k,nm in names.items():
    m=FAM==k; acc['closure_relief_vs_gate6'][nm]=dict(verts=int(m.sum()),**st(dc[m]))
    acc['closure_vs_diagnostic'][nm]=dict(median_mm=round(float(np.median(mv[m])),3),p99_mm=round(float(np.percentile(mv[m],99)),2),max_mm=round(float(mv[m].max()),2))
acc['closure_relief_vs_gate6']['_all']=st(dc); acc['diagnostic_relief_vs_gate6_all']=st(dd)
acc['closure_vs_diagnostic']['_all']=dict(median_mm=round(float(np.median(mv)),3),p99_mm=round(float(np.percentile(mv,99)),2),max_mm=round(float(mv.max()),2))
# transition sharpness: change of scale spacing R per cm along mesh edges (p99 / max), diagnostic vs closure
E=np.concatenate([F[:,[0,1]],F[:,[1,2]]]); L=np.linalg.norm(V0[E[:,0]]-V0[E[:,1]],axis=1)
for key,r in (('diagnostic',rd),('closure',rc)):
    for fld in ('R','H'):
        g=np.abs(r[fld][E[:,0]].astype(float)-r[fld][E[:,1]].astype(float))/L
        acc.setdefault('transition_gradient_per_cm',{})['%s_%s'%(key,fld)]=dict(p99=round(float(np.percentile(g,99)),4),p999=round(float(np.percentile(g,99.9)),4),max=round(float(g.max()),3))
acc['_envelope_cm']={k:dict(gate6=round(float(np.ptp(V0[:,i])),2),diagnostic=round(float(np.ptp(Vd[:,i])),2),closure=round(float(np.ptp(Vc[:,i])),2)) for i,k in enumerate(('width','depth','height'))}
sil={}
for v in ('front','profile','rear','front34','rear34'):
    a=np.asarray(Image.open('E9_%s.png'%v).convert('RGBA'))[...,3]>127; b=np.asarray(Image.open('E11_%s.png'%v).convert('RGBA'))[...,3]>127
    sil[v]=dict(changed_px=int((a^b).sum()),pct=round(100*float((a^b).sum())/a.sum(),3))
acc['_silhouette_closure_vs_gate6']=sil
json.dump(acc,open('acct11.json','w'),indent=1); print(json.dumps(acc,indent=1))
