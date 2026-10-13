# field toolkit for the RD surgical sculpt: winding grid -> mirrored signed distance field (cm), mesh out
import numpy as np
from scipy import ndimage as ndi
D='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/rd'
def load(mirror=True, xmax=56.0):
    d=np.load(D+'/wn.npz'); G=d['G']; lo=d['lo'].astype(float); h=float(d['h'])
    xs=lo[0]+h*np.arange(G.shape[0]); O=G>0.5
    if mirror:   # keep the clean +X half and mirror it (bilateral symmetry; the -X arm is open at the F1/F2 slab cut)
        nx=int(round(xmax/h)); X=h*np.arange(-nx,nx+1); idx=np.round((np.abs(X)-lo[0])/h).astype(int)
        ok=(idx>=0)&(idx<G.shape[0]); O2=np.zeros((len(X),)+G.shape[1:],bool); O2[ok]=O[idx[ok]]; O=O2; lo=lo.copy(); lo[0]=X[0]
    return O, lo, h
def sdf(O,h):
    return (ndi.distance_transform_edt(~O)-ndi.distance_transform_edt(O))*h
def coords(shape,lo,h):
    return [lo[i]+h*np.arange(shape[i]) for i in range(3)]
def mesh(S,lo,h,fn,level=0.0):
    from skimage import measure; import trimesh
    v,f,_,_=measure.marching_cubes(S,level,spacing=(h,h,h)); v+=lo
    m=trimesh.Trimesh(v,f[:,::-1],process=True)   # S negative inside: flip for outward winding
    if m.volume<0: m.invert()
    m.export(fn); return m
