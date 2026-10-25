# lm.py MESH.npz OUT.json : Grask landmark package on a mesh (analysis frame, cm).
# Methods: 'prior-seed+surface-fit' = old Grask E3 (MPFB) joint seed moved by the section-centroid difference
#          between the E3 surface and this mesh on the same plane; 'surface-fit' = feature on this mesh;
#          'manual' = exact source-construction point (v004/v005 parametric extremity model / v003 eye params).
import sys, json, numpy as np, trimesh
sys.path.insert(0,'/tmp/claude-0/src3d/v5/tools')
from hand_model import DEF as HDEF, scaled, finger_chain
from hand_frame import frame
import foot_model as fm
M=np.load(sys.argv[1]); V=M['V'].astype(float); F=M['Q'].astype(np.int64)
mesh=trimesh.Trimesh(V,F,process=False)
# surface-fit features are measured on area-weighted surface samples (triangle centroids), never on raw vertices, so the
# result does not depend on the mesh's vertex sampling; extremal features use the area-weighted centroid of the top band
SP=mesh.triangles_center; SA=mesh.area_faces
def topc(mask,score,k):
    i=np.nonzero(mask)[0]; sc=score[i]; j=i[sc>=sc.max()-k]; w=SA[j]; return (SP[j]*w[:,None]).sum(0)/w.sum()
def bandc(mask):
    i=np.nonzero(mask)[0]; w=SA[i]; return (SP[i]*w[:,None]).sum(0)/w.sum()
E3=np.load('/tmp/claude-0/rp2/GR5DE3_r6.npz',allow_pickle=True)
J=json.loads(str(E3['joints'])); _k=E3['keep']; _F=E3['F']; e3=trimesh.Trimesh(E3['V'],_F[_k[_F].all(1)],process=False)
def sec_centroid(m,o,n,pick,rmax=40):
    s=m.section(plane_origin=o,plane_normal=n)
    if s is None: return None
    n=n/np.linalg.norm(n); a=np.cross(n,[0,0,1.0]) if abs(n[2])<0.9 else np.cross(n,[1.0,0,0]); a/=np.linalg.norm(a); b=np.cross(n,a)
    best=None
    for e in s.discrete:
        if len(e)<4: continue
        q=e-o; x=q@a; y=q@b; A=0.5*np.sum(x[:-1]*y[1:]-x[1:]*y[:-1])
        if abs(A)<1e-6: continue
        cx=np.sum((x[:-1]+x[1:])*(x[:-1]*y[1:]-x[1:]*y[:-1]))/(6*A); cy=np.sum((y[:-1]+y[1:])*(x[:-1]*y[1:]-x[1:]*y[:-1]))/(6*A)
        c=o+cx*a+cy*b; d=np.linalg.norm(c-pick)
        if d<rmax and (best is None or d<best[0]): best=(d,c)
    return None if best is None else best[1]
def transfer(seed,n,offs=(0.0,)):
    """seed moved by mean (C_mesh - C_E3) over sections at seed+off*n"""
    n=n/np.linalg.norm(n); ds=[]
    for off in offs:
        o=seed+off*n; c1=sec_centroid(mesh,o,n,o); c0=sec_centroid(e3,o,n,o)
        if c1 is not None and c0 is not None: d=c1-c0; ds.append(d-(d@n)*n/(n@n))
    return seed+np.mean(ds,0) if ds else seed
L={}
def put(k,p,meth,axis=None,note=None):
    L[k]=dict(p=[float(v) for v in p],method=meth);
    if axis is not None: L[k]['axis']=[float(v) for v in axis/np.linalg.norm(axis)]
    if note: L[k]['note']=note
H=lambda k: np.array(J[k][0]); T=lambda k: np.array(J[k][1])
up=np.array([0,0,1.0])
# axial / spine (horizontal sections)
for k in ('pelvis','spine_01','spine_02','spine_03'):
    put('spine_'+k if k=='pelvis' else k, transfer(H(k),up,(-1.5,0,1.5)),'prior-seed+surface-fit')
L['pelvis_root']=L.pop('spine_pelvis')
put('neck_base',transfer(H('neck_01'),up,(-1,0,1)),'prior-seed+surface-fit')
put('head_pivot',transfer(H('head'),up,(-1,0,1)),'prior-seed+surface-fit',note='atlanto-occipital pivot')
put('crown',topc(np.ones(len(SP),bool),SP[:,2],0.05),'surface-fit',note='area-weighted centroid of the top 0.5 mm of the cranium')
for s,sg in (('l',1),('r',-1)):
    # legs
    th=T('thigh_'+s)-H('thigh_'+s); kn=T('calf_'+s)-H('calf_'+s)
    hip=transfer(H('thigh_'+s),th,(16,19,22)); put('hip_'+s,hip,'prior-seed+surface-fit',axis=th,note='femoral-head proxy: seed + thigh-section centroid shift 14-22 cm distal')
    put('knee_'+s,transfer(H('calf_'+s),th,(-3,0,3)),'prior-seed+surface-fit',axis=np.array([1.0,0,0]),note='axis = flexion (mediolateral)')
    put('ankle_'+s,transfer(H('foot_'+s),kn,(-6,-4)),'prior-seed+surface-fit',axis=np.array([1.0,0,0]),note='seed + distal shin-section shift')
    # girdle / arm
    ua=T('upperarm_'+s)-H('upperarm_'+s); fa=T('lowerarm_'+s)-H('lowerarm_'+s)
    put('sternoclavicular_'+s,transfer(H('clavicle_'+s),up,(0,)),'prior-seed+surface-fit')
    put('glenohumeral_'+s,transfer(H('upperarm_'+s),ua,(26,28,30)),'prior-seed+surface-fit',axis=ua,note='seed + upper-arm section shift 26-30 cm distal (arm free of torso below z~152)')
    g=np.array(L['glenohumeral_'+s]['p']); o_=np.array([[g[0]+sg*2.5,g[1],g[2]+30]]); loc,_,_=mesh.ray.intersects_location(o_,np.array([[0,0,-1.0]]),multiple_hits=False)
    put('acromion_'+s,loc[0],'surface-fit',note='shoulder-cap surface point vertically above the glenohumeral centre, 2.5 cm lateral (ray construction)')
    put('elbow_'+s,transfer(H('lowerarm_'+s),ua,(-3,0,3)),'prior-seed+surface-fit',axis=np.array([0,1.0,0])*0+np.cross(ua,[0,1.0,0]),note='axis ~ mediolateral flexion')
    W,Mh=frame(s.upper())
    put('wrist_'+s,W,'manual',axis=Mh[:,0],note='hand-frame origin of the v004/v005 extremity construction')
    p=scaled(HDEF)
    for nm,f in p['fingers'].items():
        Jc,_,_=finger_chain(f['mcp'],f['L'],f['splay'],f['flex'])
        put('%s_mcp_%s'%(nm,s),W+Mh@Jc[0],'manual',note='exact v005 construction joint'); put('%s_tip_%s'%(nm,s),W+Mh@Jc[3],'manual',note='exact v005 construction distal-phalanx end')
    put('thumb_cmc_'+s,W+Mh@np.array(p['thumb']['cmc']),'manual',note='exact v005 construction joint')
    # scapular proxy: posterior surface point at mid-scapula height behind the glenohumeral centre
    g=np.array(L['glenohumeral_'+s]['p']); m=(sg*SP[:,0]>4)&(sg*SP[:,0]<g[0]*sg-4)&(np.abs(SP[:,2]-(g[2]-12))<1.5)&(SP[:,1]<g[1])
    if m.any(): put('scapular_inferior_proxy_'+s,topc(m,-SP[:,1]-0.01*(SP[:,2]-(g[2]-12))**2,0.1),'surface-fit',note='posterior summit of the back 12 cm below the glenohumeral centre, medial of it (area-weighted top 1 mm)')
    # feet
    for t in fm.DEF['toes']:
        Jt,_,_=fm.chain(t); P=np.array(Jt); P[:,0]*=sg
        put('%s_mtp_%s'%(t['n'],s),P[0],'manual',note='exact v004/v005 construction joint'); put('%s_tip_%s'%(t['n'],s),P[-1],'manual',note='exact construction distal end')
    put('eye_'+s,np.array([sg*3.65,10.4,203.85]),'manual',note='v003 eyeball-volume centre (eye_params_v003.json)')
# face surface fits
mid=(SP[:,1]>5)&(np.abs(SP[:,0])<0.6)&(SP[:,2]<196)&(SP[:,2]>182)
put('chin',topc(mid,-(SP[:,2]-0.6*SP[:,1]),0.05),'surface-fit',note='midline chin point minimising z-0.6f (area-weighted top 0.5 mm)')
for s,sg in (('l',1),('r',-1)):
    m=(SP[:,2]>193)&(SP[:,2]<215)&(SP[:,1]<7)&(SP[:,1]>-6)&(sg*SP[:,0]>8.5)
    put('ear_tip_'+s,topc(m,sg*SP[:,0]+0.5*SP[:,2],0.05),'surface-fit',note='max lateral+up ear point (area-weighted top 0.5 mm)')
    m2=(sg*SP[:,0]>6.5)&(sg*SP[:,0]<8.2)&(SP[:,2]>196)&(SP[:,2]<206)&(SP[:,1]<4)&(SP[:,1]>-3)
    put('ear_root_'+s,bandc(m2),'surface-fit',note='area-weighted centroid of the cranial attachment band')
    er=np.array(L['ear_root_'+s]['p']); put('jaw_hinge_'+s,er+np.array([-sg*1.5,2.2,-2.0]),'manual',note='estimated TMJ: 2.2 cm anterior, 2 cm below, 1.5 cm medial of ear root (no jaw in source)')
    # mouth corner (section construction, sampling-independent): stomion height = most recessed point of the midline
    # lip-line profile (193.6-195.4 cm); on the horizontal section at that height the corner is where the frontal contour
    # has receded 1.0 cm behind the midline lip front
    if s=='l':
        zz=np.arange(193.6,195.4,0.01); O=np.c_[np.zeros_like(zz),np.full_like(zz,40.0),zz]; Dd=np.tile([0,-1.0,0],(len(zz),1))
        loc,ri,_=mesh.ray.intersects_location(O,Dd,multiple_hits=False); prof=np.full(len(zz),np.inf); prof[ri]=loc[:,1]
        k_=30; lm_=[i_ for i_ in range(k_,len(zz)-k_) if prof[i_]<=prof[i_-k_:i_+k_+1].min()]   # local minimum (lip seam), +/-3 mm window
        STOM=float(zz[lm_[int(np.argmin(prof[lm_]))]]) if lm_ else float(zz[np.argmin(prof)])
    sec_=mesh.section(plane_origin=[0,0,STOM],plane_normal=[0,0,1.0]); pts=np.vstack([e for e in sec_.discrete])
    fr_=pts[(pts[:,1]>3)&(np.abs(pts[:,0])<6)]; f0=fr_[np.abs(fr_[:,0])<0.2][:,1].max()
    xs=np.linspace(0,5.5,1101); fx=np.array([fr_[np.abs(sg*fr_[:,0]-x_)<0.02][:,1].max() if (np.abs(sg*fr_[:,0]-x_)<0.02).any() else np.nan for x_ in xs])
    k=np.nonzero(fx<f0-1.0)[0][0]; put('mouth_corner_'+s,np.array([sg*xs[k],fx[k],STOM]),'surface-fit',note='stomion-height section: frontal contour 1.0 cm behind the midline lip front (stomion z = lip-seam local minimum of the midline ray profile, 193.6-195.4 cm)')
json.dump(L,open(sys.argv[2],'w'),indent=1); print(len(L),'landmarks')
