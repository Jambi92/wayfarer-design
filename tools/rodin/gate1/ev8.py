# Gate 6 accounting: deviation of every Gate 6 vertex from the Gate 5 surface, by region.
import numpy as np, json, igl
a=np.load('g7_body.npz'); V5,F5=a['V'].astype(float),a['F'].astype(np.int64)
b=np.load('g8_body.npz'); V,F=b['V'].astype(float),b['F'].astype(np.int64); origin=b['origin']
d=np.sqrt(igl.point_mesh_squared_distance(V,V5,F5)[0])
d5=np.sqrt(igl.point_mesh_squared_distance(V5,V,F)[0])       # reverse (Gate 5 surface to Gate 6) for Hausdorff
x,f,u=V.T
REG={'free tail (F < -45)':f<-45,'feet (U < 17)':u<17,'skull (U > 172)':(u>172)&(np.abs(x)<10),
 'neck (U 150-172, |x|<13)':(u>150)&(u<=172)&(np.abs(x)<13),'torso (U 100-150, |x|<17)':(u>100)&(u<=150)&(np.abs(x)<17),
 'pelvis / tail root (U 66-100, |x|<20, F > -45)':(u>66)&(u<=100)&(np.abs(x)<20)&(f>-45),
 'legs (U 17-66)':(u>=17)&(u<=66),'arms + hands (|x| > 21, U 66-158)':(np.abs(x)>21)&(u>66)&(u<158)}
acc={}
for k,m in REG.items():
    dm=d[m]; acc[k]=dict(verts=int(m.sum()),identical=int(((origin>=0)&m).sum()),median_cm=round(float(np.median(dm)),3),p95_cm=round(float(np.percentile(dm,95)),3),max_cm=round(float(dm.max()),3),
                         frac_under_1mm=round(float((dm<0.1).mean()),3))
acc['_global']=dict(verts=len(V),faces=len(F),identical_copies=int((origin>=0).sum()),hausdorff_cm=round(float(max(d.max(),d5.max())),2),height=[round(float(np.ptp(V[:,2])),3),round(float(np.ptp(V5[:,2])),3)],
                    width_x=[round(float(np.ptp(V[:,0])),2),round(float(np.ptp(V5[:,0])),2)],depth_f=[round(float(np.ptp(V[:,1])),2),round(float(np.ptp(V5[:,1])),2)])
json.dump(acc,open('acct8.json','w'),indent=1); print(json.dumps(acc,indent=1))
R=np.where(d<0.1,3,np.where(d<0.5,22,21)); np.savez('acct8.npz',P=V,f=F,R=R)
