# Gate 6 closure accounting vs Pass 3: head-scale region, posterior-pelvic closure region, everything else.
import numpy as np, json, igl
a=np.load('g8_body.npz'); V0,F0=a['V'].astype(float),a['F'].astype(np.int64)
b=np.load('g9_body.npz'); V,F=b['V'].astype(float),b['F'].astype(np.int64); origin=b['origin']
d=np.sqrt(igl.point_mesh_squared_distance(V,V0,F0)[0]); d0=np.sqrt(igl.point_mesh_squared_distance(V0,V,F)[0])
x,f,u=V.T
head=(np.abs(x)<16)&(f>-20)&(f<28)&(u>150)
pelv=(np.abs(x)<30)&(f>-75)&(f<15)&(u>55)&(u<115)
REG={'head-scale region (head + upper neck)':head,'posterior-pelvic closure region':pelv&~head,'EVERYTHING ELSE':~head&~pelv,
     '  of which free tail beyond F -75':f<-75,'  of which legs + feet (U < 55)':u<55,'  of which torso / arms / shoulders (U 115-150)':(u>=115)&(u<150)}
acc={}
for k,m in REG.items():
    dm=d[m]; acc[k]=dict(verts=int(m.sum()),identical=int(((origin>=0)&m).sum()),median_mm=round(float(np.median(dm))*10,3),p99_mm=round(float(np.percentile(dm,99))*10,3),max_mm=round(float(dm.max())*10,3))
acc['_global']=dict(verts=len(V),faces=len(F),identical_copies=int((origin>=0).sum()),hausdorff_cm=round(float(max(d.max(),d0.max())),2),height=[round(float(np.ptp(V[:,2])),3),round(float(np.ptp(V0[:,2])),3)],
    width_x=[round(float(np.ptp(V[:,0])),2),round(float(np.ptp(V0[:,0])),2)],depth_f=[round(float(np.ptp(V[:,1])),2),round(float(np.ptp(V0[:,1])),2)])
json.dump(acc,open('acct9.json','w'),indent=1); print(json.dumps(acc,indent=1))
R=np.where(d<0.1,3,np.where(d<0.5,22,21)); np.savez('acct9.npz',P=V,f=F,R=R)
