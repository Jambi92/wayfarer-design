# identity.py PROD.npz OUT.json : race-specific identity audit -- station readings on v005 vs retopo (cm, diffs in mm)
import numpy as np, sys, json, trimesh
sys.path.insert(0,'/tmp/claude-0/rt'); from common import load_src
SV,SF=load_src(); S=trimesh.Trimesh(SV,SF,process=False)
z=np.load(sys.argv[1]); Q=z['Q']; P=trimesh.Trimesh(z['V'],np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]],process=False)
def sec(m,zz,xsel=None):
    s=m.section(plane_origin=[0,0,zz],plane_normal=[0,0,1.0]); out=[]
    for e in s.discrete:
        c=e.mean(0)
        if xsel is None or xsel(c): out.append(e)
    return out
def stats(m,zz,xsel,label):
    L=sec(m,zz,xsel)
    if not L: return None
    A=np.vstack(L); per=sum(np.linalg.norm(np.diff(e,axis=0),axis=1).sum() for e in L)
    return dict(width=float(A[:,0].max()-A[:,0].min()),depth=float(A[:,1].max()-A[:,1].min()),perimeter=float(per))
ST=[('chest_axilla',150,lambda c: abs(c[0])<17),('chest_nipple',140,lambda c: abs(c[0])<20),('waist',130,lambda c: abs(c[0])<17),
    ('pelvis_iliac',120,lambda c: abs(c[0])<22),('hip_glute',108,None),('thigh_l',95,lambda c: c[0]>0 and c[0]<22),('knee_l',71,lambda c: c[0]>0 and c[0]<22),
    ('calf_l',52,lambda c: c[0]>0),('ankle_l',14,lambda c: c[0]>0),('neck',188,lambda c: abs(c[0])<10),('head_brow',205,None),
    ('upperarm_l',145,lambda c: c[0]>21),('forearm_l',130,lambda c: c[0]>21),('wrist_l',111,lambda c: c[0]>21)]
R={}
for nm,zz,fn in ST:
    a=stats(S,zz,fn,nm); b=stats(P,zz,fn,nm)
    R[nm]=dict(z=zz,source=a,retopo=b,diff_mm={k:round(10*(b[k]-a[k]),3) for k in a})
def ext(m,sel):
    V=m.vertices[sel(m.vertices)]; return V.min(0),V.max(0)
for nm,sel in (('foot_l',lambda V:(V[:,2]<10)&(V[:,0]>0)),('foot_r',lambda V:(V[:,2]<10)&(V[:,0]<0)),('hand_l',lambda V:(V[:,2]<112)&(V[:,2]>75)&(V[:,0]>24)),
               ('hand_r',lambda V:(V[:,2]<112)&(V[:,2]>75)&(V[:,0]<-24)),('head',lambda V:V[:,2]>189),('shoulders',lambda V:(V[:,2]>150)&(V[:,2]<185))):
    a0,a1=ext(S,sel); b0,b1=ext(P,sel); R[nm+'_extent']=dict(source=(a1-a0).tolist(),retopo=(b1-b0).tolist(),diff_mm=(10*((b1-b0)-(a1-a0))).round(3).tolist())
mx=max(abs(v) for r in R.values() for v in (r['diff_mm'].values() if isinstance(r['diff_mm'],dict) else r['diff_mm']))
json.dump(dict(max_abs_diff_mm=mx,stations=R),open(sys.argv[2],'w'),indent=1)
print('identity stations',len(R),'max |diff| mm',round(mx,3))
