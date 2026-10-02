# Gate 2 torso translation field = accepted Gate 1 field (g2) with the ventral/lateral torso re-organised:
# low-pass of B1's own torso (removes pec plates/shelf, rectus ladder, linea alba, navel) + designed Saurin load paths
# expressed as smooth surface-normal offsets (height functions in x,u) so volume and silhouette stay B1's.
import numpy as np, sys
from scipy.interpolate import RegularGridInterpolator
import g1, g2
from g1 import ss, smin, smax, BIG
from scipy.ndimage import spline_filter, map_coordinates
z=np.load("blur_torso.npz"); _A,_B,_C=z["a"],z["b"],z["c"]; _CO=spline_filter(z["d"].astype(np.float64),order=3)
def TB(Q):                                                   # C2 cubic-spline lookup (trilinear left shading facets)
    c=np.stack([(Q[:,0]-_A[0])/0.6,(Q[:,1]-_B[0])/0.6,(Q[:,2]-_C[0])/0.6])
    return map_coordinates(_CO,c,order=3,prefilter=False,mode="nearest")
def seg_d(x,u,p,q):
    p=np.array(p,float); q=np.array(q,float); v=q-p; t=np.clip(((x-p[0])*v[0]+(u-p[1])*v[1])/(v@v),0,1)
    return np.hypot(x-(p[0]+t*v[0]),u-(p[1]+t*v[1])),t
def band(x,u,p,q,w0,w1,h0,h1):
    d,t=seg_d(x,u,p,q); w=w0+(w1-w0)*t; h=h0+(h1-h0)*t
    prof=1-ss(0.25*w,w,d)                                   # flat-topped strap with bevelled edges
    endfade=ss(0.0,0.08,t)*(1-ss(0.92,1.0,t)); return h*prof*np.maximum(endfade,0.0)
def weight(X,F,U):
    ax=np.abs(X)
    vert=ss(103.0,109.0,U)*(1-ss(150.0,152.5,U))
    lat_ab=1-ss(15.5,18.8,ax); lat_ch=1-ss(15.5,18.5,ax); tch=ss(132.0,138.0,U)
    lat=lat_ab*(1-tch)+lat_ch*tch
    vent=ss(-2.0,3.0,F)
    keel=ss(1.2,2.6,ax)                                    # protect B1's sternal keel strap (|x|<1.2 kept original)
    keel=1-(1-keel)*ss(134.0,138.0,U)                       # ... above U 138; below, the keel end is re-blended
    return vert*lat*vent*keel
def heights(X,U):
    ax=np.abs(X); h=np.zeros_like(X)
    # (a) ventral shield: one continuous, unsegmented central plate from the costal apex to the pelvic platform,
    #     with a faint longitudinal crown (not a linea alba groove) and bevelled lateral margins
    hw=6.4+(3.8-6.4)*np.clip((132.0-U)/27.0,0,1)
    sh=(1-ss(hw-1.6,hw+0.2,ax))*ss(103.0,108.0,U)*(1-ss(130.5,133.5,U))
    h+=sh*(0.85+0.25*(1-ss(0.0,hw*0.7,ax)))
    # (b) costal arches: sternal apex -> lateral costal margin (B1's inverted-V made continuous and load-bearing)
    h+=band(ax,U,(1.2,134.0),(12.5,124.0),1.7,1.9,0.95,0.80)+band(ax,U,(12.5,124.0),(17.6,113.5),1.9,1.7,0.80,0.0)
    # (c) long oblique load paths: lateral thorax -> pelvic platform (thorax -> lower axial trunk -> Gate-1 pelvis)
    h+=band(ax,U,(14.6,133.5),(6.0,103.5),4.2,3.2,0.95,0.55)
    # (d) counter-diagonal from the shield margin to the hip (cross-bracing the flank; X-tension with (c))
    # (e) grooves that separate the paths (definition without segmentation)
    gx=hw+0.7; h-=0.40*(1-ss(0.25,0.95,np.abs(ax-gx)))*ss(104.0,108.0,U)*(1-ss(128.0,131.0,U))
    # (f) pectoral fan: four flat fascicles from the sternal keel converging on the humeral insertion, separated by grooves
    ins=(17.4,146.5)
    for (u0,w0,hh) in ((150.0,2.8,0.42),(145.0,3.0,0.50),(140.0,2.7,0.40)):
        h+=band(ax,U,(1.8,u0),ins,w0,1.6,hh,0.18)
    return h
def chest_plane(X,F,U):
    # keeled shield: replaces the rounded human pectoral plate + under-pec shelf by a planar facet each side
    ax=np.abs(X); fp=16.2-0.44*ax-0.62*(U-146.0)-0.4
    return F-fp                                           # signed distance-like (positive in front of the facet)
def chest_w(X,U):
    ax=np.abs(X); rho=np.sqrt(((ax-9.0)/8.0)**2+((U-145.0)/6.5)**2)
    return (1-ss(0.55,1.0,rho))*ss(1.5,3.5,ax)
def field(X,F,U):
    e=g2.field(X,F,U)
    w=weight(X,F,U); m=w>1e-4
    if m.any():
        b=TB(np.stack([X[m],F[m],U[m]],-1))+0.15             # low-passed B1 torso (volume kept: 0.15 cm recession only)
        cw=chest_w(X[m],U[m]); cp=chest_plane(X[m],F[m],U[m])
        b=b*(1-cw)+smax(b,cp,2.4)*cw                          # planar keeled facet over the old pectoral plate
        b=b-heights(X[m],U[m])
        e[m]=e[m]*(1-w[m])+b*w[m]
    return e
import wf_saurin_body8 as B8
B8.sdf=lambda X,F,U: field(X,F,U)
B8.BOX=(-22.0,22.0,-10.0,24.0,99.0,158.0)
if __name__=="__main__":
    import time; t=time.time(); v,f=B8.mesh(float(sys.argv[1]) if len(sys.argv)>1 else 0.3,log=lambda *a: None)
    np.savez_compressed(sys.argv[2] if len(sys.argv)>2 else "edit3_mc.npz",v=v,f=f); print("DONE",len(v),len(f),round(time.time()-t,1))
