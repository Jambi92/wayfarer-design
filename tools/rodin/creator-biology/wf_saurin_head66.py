# Creator-variation diagnostics: Cranial Keratin Display family RANGE study on the frozen skull. Wraps head65 (unchanged)
# and rescales its display structures: DSP_LEN (length from base), DSP_BASE (base/footprint radius), DSP_SWEEP (deg, + = swept
# lower/back, - = raised), DSP_ASYM (left/right length ratio for paired structures), DSP_COUNT (number of hornlet pairs kept,
# low_hornlets: 1 = brow only, 2 = brow + squamosal, 3 = all), CREST_H (crest height above roof, cm).
import os, numpy as np
_dv=os.environ.get("DISPLAY_VARIANT",""); os.environ["DISPLAY_VARIANT"]=""
import wf_saurin_head65 as H5
os.environ["DISPLAY_VARIANT"]=_dv
from wf_saurin_head61 import horn as _horn, smin
H=H5.H; P=H5.P; EYE=H5.EYE; RINGS=H5.RINGS
LEN=float(os.environ.get("DSP_LEN","1")); BASE=float(os.environ.get("DSP_BASE","1")); SW=np.radians(float(os.environ.get("DSP_SWEEP","0")))
ASYM=float(os.environ.get("DSP_ASYM","1")); COUNT=int(os.environ.get("DSP_COUNT","3"))
def _tr(a,p,side):
    v=np.array(p,float)-np.array(a,float); L=LEN*(ASYM if side<0 else 1.0)
    c,s=np.cos(SW),np.sin(SW); vf,vu=v[1],v[2]; v2=np.array([v[0], c*vf-s*vu, s*vf+c*vu])   # + sweep: back-pointing axis rotates lower
    return tuple(np.array(a,float)+L*v2)
_cnt=[0]
def hornV(X,F,U,a,m,t,r0,r1,**kw):
    side=np.sign(a[0]) if abs(a[0])>1e-6 else 1.0
    return _horn(X,F,U,a,_tr(a,m,side),_tr(a,t,side),r0*BASE,r1*BASE**0.5,**kw)
H5.horn=hornV
H5.CREST_H=float(os.environ.get("CREST_H","2.40"))
if _dv=="low_hornlets" and COUNT<3:
    # rebuild with a subset: 1 = postorbital brow hornlets only, 2 = + squamosal corner
    S=H5.S; a=S(4.6,3.6); b=S(4.4,-3.2)
    h1=lambda X,F,U: hornV(X,F,U,a,(a[0]+0.5,a[1]-0.6,a[2]+0.9),(a[0]+0.8,a[1]-1.2,a[2]+1.5),0.62,0.10)
    h2=lambda X,F,U: hornV(X,F,U,b,(b[0]+0.5,b[1]-0.9,b[2]+0.9),(b[0]+0.8,b[1]-1.8,b[2]+1.5),0.72,0.10)
    _D=H5._sym(h1) if COUNT==1 else H5._sym(lambda X,F,U: smin(h1(X,F,U),h2(X,F,U),0.2))
else:
    _D=H5.build(_dv) if _dv else None
def head_sdf(X,F,U,neck_rings,cut_u):
    d=H.head_sdf(X,F,U,neck_rings,cut_u)
    if _D is None: return d
    k=(np.abs(X)<11)&(F>-26)&(F<9)&(U>2)
    if k.any():
        d=d.copy(); d[k]=smin(d[k],_D(X[k],F[k],U[k]),0.5)
    return d
def eye_centers(): return H.eye_centers()
