# build_part.py : narrow-band SDF evaluation on a world grid + marching cubes + isotropic remesh
import numpy as np, sys, time
from skimage.measure import marching_cubes
def evaluate(fun, lo, hi, h, band_coarse=4.0):
    lo=np.asarray(lo,float); hi=np.asarray(hi,float)
    n=np.ceil((hi-lo)/h).astype(int)+1
    # coarse pass
    hc=h*4; nc=np.ceil((hi-lo)/hc).astype(int)+1
    gc=[lo[i]+hc*np.arange(nc[i]) for i in range(3)]
    Pc=np.stack(np.meshgrid(*gc,indexing='ij'),-1).reshape(-1,3)
    Dc=np.concatenate([fun(Pc[i:i+400000]) for i in range(0,len(Pc),400000)]).reshape(nc)
    # upsample coarse to fine (nearest, for far field sign) and refine near-surface blocks
    Dc=Dc.astype(np.float32)
    D=np.empty(tuple(n),np.float32)
    for i in range(n[0]):
        D[i]=np.repeat(np.repeat(Dc[min(i//4,nc[0]-1)],4,0)[:n[1]],4,1)[:,:n[2]]
    B=16; cnt=0
    for i0 in range(0,n[0],B):
        for j0 in range(0,n[1],B):
            for k0 in range(0,n[2],B):
                blk=D[i0:i0+B,j0:j0+B,k0:k0+B]
                if np.abs(blk).min()>band_coarse*h*4: continue
                ii=lo[0]+h*np.arange(i0,min(i0+B,n[0])); jj=lo[1]+h*np.arange(j0,min(j0+B,n[1])); kk=lo[2]+h*np.arange(k0,min(k0+B,n[2]))
                P=np.stack(np.meshgrid(ii,jj,kk,indexing='ij'),-1).reshape(-1,3)
                D[i0:i0+B,j0:j0+B,k0:k0+B]=fun(P).reshape(len(ii),len(jj),len(kk)); cnt+=len(P)
    return D,lo,h,cnt
def polygonize(D,lo,h):
    neg=D<0
    ax=[np.nonzero(neg.any(axis=tuple(j for j in range(3) if j!=i)))[0] for i in range(3)]
    s=[slice(max(a.min()-2,0),a.max()+3) for a in ax]
    Dc=np.ascontiguousarray(D[s[0],s[1],s[2]]); del neg
    off=np.array([s[0].start,s[1].start,s[2].start])*h
    v,f,_,_=marching_cubes(Dc,0.0,spacing=(h,h,h))
    return v+lo+off, f[:,::-1].copy()
def remesh(V,F,target):
    import pymeshlab
    ms=pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(V,F))
    ms.meshing_decimation_quadric_edge_collapse(targetfacenum=int(target),preservetopology=True,preservenormal=True,qualitythr=0.5,optimalplacement=True,planarquadric=True)
    m=ms.current_mesh(); return m.vertex_matrix(), m.face_matrix()
def genus(V,F):
    import trimesh, collections
    m=trimesh.Trimesh(V,F,process=True); parts=m.split(only_watertight=False); m=max(parts,key=lambda q:len(q.faces))
    e=np.sort(m.edges,1); u,c=np.unique(e,axis=0,return_counts=True); be=u[c==1]
    adj=collections.defaultdict(list)
    for a_,b_ in be: adj[a_].append(b_); adj[b_].append(a_)
    seen=set(); loops=0
    for v in adj:
        if v in seen: continue
        loops+=1; st=[v]
        while st:
            x=st.pop()
            if x in seen: continue
            seen.add(x); st+=adj[x]
    chi=len(m.vertices)-len(u)+len(m.faces); return (2-chi-loops)/2
