# dflood.py : explicit topological D mask = seeded source-face flood fill bounded by two explicit throat loops
# (ruling dc9d48f s3.1; order 647fa4e s6).  Throat loop = the outermost planar section (perpendicular to the handle axis) in which the
# hidden handle is still a separate closed loop around the axis; its crossed source faces form a closed band that is the boundary.
import numpy as np, sys, json; sys.path.insert(0,'/home/claude/stc/rp1e'); from ploops import plane_loops, src
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
def handle_loop(c,ax,t,rmax):
    best=None
    for l in plane_loops(c+t*ax,ax,c+t*ax,rmax*2):
        if not l['closed']: continue
        P=l['pts']; cc=P.mean(0); 
        rad=np.linalg.norm(P-cc,axis=1).max()
        if rad<rmax and np.linalg.norm(cc-(c+t*ax))<rmax:
            if best is None or np.linalg.norm(cc-(c+t*ax))<np.linalg.norm(best['pts'].mean(0)-(c+t*ax)): best=l
    return best
def build(name,c,ax,rmax,step=0.025,tmax=3.0,tover=None,rb=None):
    V,F=src(); ax=np.asarray(ax,float); ax/=np.linalg.norm(ax); c=np.asarray(c,float)
    l0=handle_loop(c,ax,0.0,rmax); assert l0 is not None,'no closed handle loop at t=0'
    throats=[]
    for sgn in (-1,1):
        t=0.0; last=(0.0,l0)
        while abs(t)<tmax:
            t+=sgn*step; l=handle_loop(c,ax,t,rmax)
            if l is None: break
            last=(t,l)
        if tover is not None and tover[(sgn+1)//2] is not None:
            tt=tover[(sgn+1)//2]; Lb=[l for l in plane_loops(c+tt*ax,ax,c+tt*ax,rb)]
            last=(tt,dict(faces=np.concatenate([l['faces'] for l in Lb]),edges=np.concatenate([l['edges'] for l in Lb]),pts=np.vstack([l['pts'] for l in Lb]),closed=False))
        throats.append(last)
    # face adjacency
    nf=len(F); E=np.vstack([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); E.sort(1); fid=np.tile(np.arange(nf),3)
    o=np.lexsort((E[:,1],E[:,0])); Es=E[o]; fs=fid[o]; same=(Es[1:]==Es[:-1]).all(1)
    a=fs[:-1][same]; b=fs[1:][same]
    block=np.zeros(nf,bool)
    for t,l in throats: block[l['faces']]=True
    keep=~block; idx=np.where(keep)[0]; loc=-np.ones(nf,int); loc[idx]=np.arange(len(idx))
    m=keep[a]&keep[b]; A=sp.coo_matrix((np.ones(m.sum()),(loc[a[m]],loc[b[m]])),shape=(len(idx),len(idx)))
    n,lab=connected_components(A,directed=False)
    seed=[f for f in l0['faces'] if keep[f]][0]; comp=lab[loc[seed]]; mask=idx[lab==comp]
    area=0.5*np.linalg.norm(np.cross(V[F[:,1]]-V[F[:,0]],V[F[:,2]]-V[F[:,0]]),axis=1)
    info=dict(name=name,axis_centre_blender_cm=c.round(3).tolist(),axis=ax.round(4).tolist(),seed_face=int(seed),
              throat_t_cm=[round(t,3) for t,_ in throats],throat_loop_faces=[l['faces'].tolist() for _,l in throats],
              throat_loop_edges=[l['edges'].tolist() for _,l in throats],mask_faces=int(len(mask)),
              mask_vertices=int(len(np.unique(F[mask]))),mask_area_cm2=round(float(area[mask].sum()),4),
              source_area_cm2=round(float(area.sum()),2),area_share_pct=round(float(area[mask].sum()/area.sum()*100),5),
              mask_bbox=[V[F[mask]].reshape(-1,3).min(0).round(2).tolist(),V[F[mask]].reshape(-1,3).max(0).round(2).tolist()])
    return mask,np.unique(F[mask]),info,throats
if __name__=='__main__':
    name=sys.argv[1]; c=eval(sys.argv[2]); ax=eval(sys.argv[3]); rmax=float(sys.argv[4]); out=sys.argv[5]
    tov=eval(sys.argv[6]) if len(sys.argv)>6 else None; rb=float(sys.argv[7]) if len(sys.argv)>7 else None
    mask,vids,info,th=build(name,c,ax,rmax,tover=tov,rb=rb)
    import os; os.makedirs(out,exist_ok=True)
    np.save(os.path.join(out,name+'_source_faces.npy'),mask); np.save(os.path.join(out,name+'_source_vertices.npy'),vids)
    json.dump(info,open(os.path.join(out,name+'_info.json'),'w'))
    print({k:v for k,v in info.items() if 'loop' not in k})
