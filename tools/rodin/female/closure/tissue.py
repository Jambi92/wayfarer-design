# Female Pass 2 soft-tissue diagnostics: smooth displacement fields defined on the frozen reference (applied before vary.warp,
# like the composition offsets). Direction = radial from the torso section centre (x, f - fc(u)): a smooth shell-following
# expansion, so the existing scale fields deform with the tissue instead of being re-sculpted.
import numpy as np, sys; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); import vary
from vary import ss, band
_FC={}
def _fc(L):
    if id(L) not in _FC:
        c=np.array(L.torso_cf,float); k=np.exp(-0.5*(np.arange(-24,25)/8.0)**2); k/=k.sum()
        _FC[id(L)]=np.convolve(np.pad(c,24,mode='edge'),k,mode='same')[24:-24]   # heavily smoothed section centre (no 1-cm bin steps)
    return _FC[id(L)]
def _frame(V,L):
    x,f,u=V.T; fc=np.interp(u,np.arange(200),_fc(L)); dx=x; df=f-fc
    r=np.hypot(dx,df)+1e-9; d=np.stack([dx/r,df/r,np.zeros_like(r)],1); ang=np.arctan2(np.abs(dx),df)   # 0 = straight ventral
    return x,f,u,d,ang
def ventral(V,L):
    """B/C: unpaired, non-mammalian ventral / ventrolateral fullness over the lower thorax and upper abdomen:
    one continuous field across the midline, peaking low on the thorax, fading into the flanks (no paired peaks)."""
    x,f,u,d,ang=_frame(V,L)
    w=band(u,106,124,140,154)*ss((1.20-ang)/0.75)*L.torso*(1-L.arm)
    return w,d
def breast(V,L,c=8.8,u0=134.5):
    """D (comparison only, NOT canon): restrained paired mounds on the upper thorax; no nipples."""
    x,f,u,d,ang=_frame(V,L); ax=np.abs(x)
    dx=np.where(ax>c,(ax-c)/7.6,(ax-c)/6.2); du=np.where(u>u0,(u-u0)/10.5,(u-u0)/6.0)
    r2=dx*dx+du*du; w=np.clip(1-r2,0,None)**2*(1-0.30*ss(du))            # upper pole tapers into the chest wall
    w*=ss((1.45-ang)/0.5)*L.torso*(1-L.arm)
    # direction: forward-dominant, slightly lateral and down (soft tissue on an upright thorax)
    dd=np.stack([0.30*np.sign(x),np.ones_like(x),-0.18*np.ones_like(x)],1); dd/=np.linalg.norm(dd,axis=1)[:,None]
    return w,dd
def flank(V,L):
    """E (additional candidate): coelomic-capacity body wall. Ventrolateral-to-lateral fullness of the lower rib cage and upper
    abdomen (the body cavity that houses the reproductive tract), so the waist fills in rather than pinching: the opposite of an hourglass."""
    x,f,u,d,ang=_frame(V,L)
    w=band(u,98,110,126,140)*ss((ang-0.25)/0.55)*ss((1.95-ang)/0.5)*(1-L.arm)*(1-L.tail)*(1-L.leg)
    return w,d
def offset(V,L,p):
    o=np.zeros_like(V)
    if p.get('vfull',0): w,d=ventral(V,L); o+=(p['vfull']*w)[:,None]*d
    if p.get('flank',0): w,d=flank(V,L); o+=(p['flank']*w)[:,None]*d
    if p.get('breast',0): w,d=breast(V,L); o+=(p['breast']*w)[:,None]*d
    return o
def fwarp(V,L,p,eye=None):
    o=offset(V,L,p)
    return vary.warp(V+o,L,p,eye=eye)
