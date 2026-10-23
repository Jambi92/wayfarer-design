# ident_head.py : Grask craniofacial + ear identity edit as smooth space warps on the 13 380-vertex body (analysis cm).
import numpy as np
R='/tmp/claude-0/rp2/'
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
def ramp(x,a,b): return ss((x-a)/(b-a)) if b!=a else (x>=a).astype(float)
def gauss(P,c,sig): d=(P-np.asarray(c))/np.asarray(sig); return np.exp(-0.5*(d*d).sum(1))
def head_delta(V, Wb, N, p):
    """V body verts, Wb weights dict, N vertex normals (physical outward), p params dict -> delta (n,3)."""
    x,f,z=V.T; ear=Wb['ears']; headw=np.clip(Wb['head']+Wb['ears']+Wb['neck_01'],0,1)
    D=np.zeros_like(V)
    ax=np.abs(x)
    # --- bony relief bumps (along outward normal), front face only
    front=ramp(f,p.get('front_f0',6),p.get('front_f1',10))*(1-ear)
    def bump(c,sig,amp,mirror=True,mask=front):
        g=gauss(V,c,sig)
        if mirror: g=g+gauss(V,(-c[0],c[1],c[2]),sig) if abs(c[0])>1e-6 else g
        return (amp*g*mask)[:,None]*N
    zb=p['brow_z']
    # deep-set orbit (eyelid skin set back under the brow)
    D+=bump((3.4,14.8,p['brow_z']-2.2),(1.5,1.5,1.1),-p.get('orbit_deep',0))
    # nasolabial groove with cheek mass lateral to it (positions before the facial stretch)
    if p.get('nasolabial'):
        for t_ in np.linspace(0,0.75,5):
            c=np.array([2.4,16.8,198.3])*(1-t_)+np.array([4.2,15.2,194.0])*t_
            D+=bump(tuple(c),(0.6,1.5,0.7),-p['nasolabial'])
    # supraorbital torus: horizontal band at the brow line (left and right arcs + glabella)
    if p.get('brow_arcs'):
        # brow follows each orbital rim: medial-upper, central, lateral-lower lobes
        D+=bump((2.2,15.6,zb+0.5),(1.3,2.2,0.9),p['brow_amp'])
        D+=bump((3.9,15.0,zb+0.3),(1.3,2.2,0.9),p['brow_amp']*0.95)
        D+=bump((5.5,13.6,zb-0.4),(1.1,2.2,0.9),p['brow_amp']*0.7)
    else:
        D+=bump((3.2,15.0,zb+0.4),(2.2,2.5,0.9),p['brow_amp'])
    D+=bump((0.0,16.0,zb),(1.4,2.5,1.0),p['glabella_amp'],mirror=False)
    # zygomatic body, vertically elongated (supports the long midface rather than lateral width)
    D+=bump((5.6,11.5,p['zyg_z']),(1.3,2.5,p.get('zyg_sz',2.6)),p['zyg_amp'])
    # mandible: gonial angle and ramus edge, chin breadth
    D+=bump((6.6,6.0,p['gon_z']),(1.4,2.2,1.6),p['gon_amp'],mask=ramp(f,2,4)*(1-ear))
    D+=bump((0.0,13.0,p['chin_z']),(2.4,2.0,1.4),p['chin_amp'],mirror=False)
    # nasal root raised into a continuous brow-nose line (less human nasion dip)
    D+=bump((0.0,16.8,p['nasion_z']),(0.9,1.5,1.4),p.get('nasion_amp',0),mirror=False)
    # infra-zygomatic flattening (vertical cheek planes)
    D+=bump((4.6,11.0,p['zyg_z']-3.2),(1.4,2.0,1.4),-p.get('cheek_hollow',0))
    # mandibular body / lower-face depth along the jaw line
    D+=bump((5.0,9.5,p['gon_z']-0.3),(1.6,2.5,1.2),p.get('jaw_amp',0))
    # --- facial vertical elongation below the brow line (face in front of the ear plane; cranium and ears fixed)
    Vb=V+D
    fm=ramp(Vb[:,1],p['stretch_f0'],p['stretch_f1'])*(1-ear)
    z0=p['neck_z']              # below this the neck is untouched
    zz=Vb[:,2]
    dz=-(zb-zz)*p['k_vert']*(zz<zb)
    dz=np.where(zz<p['chin_z0'], -(zb-p['chin_z0'])*p['k_vert']*ramp(zz,z0,p['chin_z0']), dz)   # submandibular: fade to 0 at neck_z
    dz=dz*ramp(zz,z0-0.01,z0+0.01) if False else dz
    dh=np.sqrt(Vb[:,0]**2+(0.8*(Vb[:,1]-3.0))**2)
    rz=p.get('neck_r',7.5)+5.5*ss((zz-182)/8)
    nm=1-ss((dh-rz)/2.5)   # spatial neck/head mask (no vertex-group edges)
    D[:,2]+=dz*fm*nm
    # midface narrowing (relative), keeps cranium breadth
    mid=ramp(zz,p['chin_z0'],p['chin_z0']+3)*(1-ramp(zz,zb-1,zb+1))*fm
    D[:,0]+=-x*p['k_narrow']*mid*headw
    # lower-face breadth at the mandibular angle (relative), fading above the mouth
    low=(1-ramp(zz,p['chin_z0']+4,p['chin_z0']+8))*ramp(zz,z0,p['chin_z0'])*fm
    D[:,0]+=x*p.get('k_jaw_wide',0)*low*headw
    return D
def relief(V, Q, mask, amp, it=4):
    n=len(V); e=np.r_[Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]
    import scipy.sparse as sp
    A=sp.coo_matrix((np.ones(2*len(e)),(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),(n,n)).tocsr(); A.data[:]=1; d=np.asarray(A.sum(1)).ravel()
    S=V.copy()
    for _ in range(it): S=0.5*S+0.5*(A@S)/d[:,None]
    return amp*mask[:,None]*(V-S)
def ear_delta(V, Wb, p, side):
    """late-taper Grask ear warp for one side (+1 left, -1 right)."""
    e=Wb['ears']*(np.sign(V[:,0])==side)
    m=ss(e/0.9)
    o=np.array([side*p['ear_root_x'],p['ear_root_f'],p['ear_root_z']])
    a=np.deg2rad(p['ear_back_deg']); u=np.array([0,-np.sin(a),np.cos(a)])      # axis: up and back
    nrm=np.array([side*1.0,0,0]); w=np.cross(u,nrm); w/=np.linalg.norm(w)
    P=V-o; s=P@u; c=P@w; l=P@nrm
    s0=p['ear_s0']; L=max(s.max() if (m>0.5).any() else 1,1e-3)
    smax=(s[m>0.5]).max(); k=p['ear_k']
    s_new=np.where(s>s0, s0+(s-s0)*k, s)
    smax_new=s0+(smax-s0)*k
    t=np.clip((s_new-s0)/(smax_new-s0),0,1)
    tau=p['ear_taper']*ss((t-p['ear_t0'])/(1-p['ear_t0']))
    # sustained upper body: widen mid-upper ear slightly before the taper
    wid=p['ear_body']*np.sin(np.pi*np.clip(t/p['ear_t0'],0,1))*(t<p['ear_t0'])
    c_new=c*(1-tau+wid)
    l_new=l*(1+p['ear_flare']*t)                   # a little more lateral stand-off toward the top
    Pn=o+np.outer(s_new,u)+np.outer(c_new,w)+np.outer(l_new,nrm)
    return (Pn-V)*m[:,None]
