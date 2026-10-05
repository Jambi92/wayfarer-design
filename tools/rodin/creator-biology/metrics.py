import numpy as np, sys
sys.path.insert(0,'/tmp/claude-0/rodin/v1'); import vary
from meas import tail_sections, mass_props
LM=None
def landmarks(V,L):
    x,f,u=V.T; hd=L.head>0.95
    i_tip=np.where(hd)[0][np.argmax(f[hd])]
    i_occ=np.where(hd&(u>176))[0][np.argmin(f[hd&(u>176)])]
    i_top=np.argmax(u)
    # eye surface points: nearest vertices to head63 eye centres (world)
    sys.path.insert(0,'/tmp/claude-0/rb'); import wf_saurin_head63 as H
    E=np.array([vary.head_world(np.array(c)) for c in H.eye_centers()[0]])
    from scipy.spatial import cKDTree; tr=cKDTree(V); i_eye=tr.query(E)[1]
    i_chin=np.where(hd)[0][np.argmin(u[hd])]
    return dict(tip=i_tip,occ=i_occ,top=i_top,eyeR=i_eye[0],eyeL=i_eye[1],chin=i_chin)
def measure(P,F,L,p,lm,ref=None):
    x,f,u=P.T; M={}
    M['height']=u.max()
    M['head_len']=f[lm['tip']]-f[lm['occ']]
    M['head_len_ratio']=M['head_len']/M['height']
    e=0.5*(P[lm['eyeR']]+P[lm['eyeL']]); M['rostral_proj']=f[lm['tip']]-e[1]; M['rostral_index']=M['rostral_proj']/M['head_len']
    hd=L.head>0.9; M['head_width']=np.ptp(x[hd&(u>u[lm['chin']]+1)])
    M['head_depth']=u[lm['top']]-u[lm['chin']]
    tor=(L.torso>0.6)
    for nm,(a,b) in {'shoulder_b':(140,156),'thorax_w':(118,140),'pelvis_w':(86,100)}.items():
        m=tor&(vary_u(L)>=a)&(vary_u(L)<=b); M[nm]=np.ptp(x[m])
    m=tor&(np.abs(vary_u(L)-132)<2)&(np.abs(x)<4); M['thorax_d']=np.ptp(f[m])
    M['thorax_d_over_w']=M['thorax_d']/M['thorax_w']
    # tail
    C2=p['_C2']; k_root=int(vary.S_ROOT*2)
    if not hasattr(L,'_tE'):
        EE=np.unique(np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1),axis=0)
        near=(L.s<128)&(L._u0>50)&(L._u0<115)&(L._f0<-8); L._tE=EE[near[EE[:,0]]|near[EE[:,1]]]
    A=tail_sections(P,F,C2[:k_root+16],step=2,E=L._tE)
    s=A[:,0]; a=A[:,1]; ok=~np.isnan(a); s=s[ok]; a=a[ok]
    seg=np.linalg.norm(np.diff(C2,axis=0),axis=1); S=np.concatenate([[0],np.cumsum(seg)])
    kL=p.get('tail_len',1.0); ext=vary.TIP_EXT*kL*p.get('_s',1.0)
    s_root=S[k_root]; s_free=S[200]
    M['tail_len']=s_root+ext; M['tail_len_pct']=100*M['tail_len']/M['height']
    m=s<=s_free; aa=a[m]; sss=s[m]
    A_r=np.interp(s_free,s,a); M['tail_root_area']=A_r
    vol=np.trapz(aa,sss); M['tail_vol_L']=vol/1000
    com=np.trapz(aa*sss,sss)/vol; d_com=s_free-com+0.0; M['tail_com_from_root']=d_com
    M['tail_RSI_raw']=vol*d_com/A_r**1.5
    sm=np.convolve(aa,np.ones(5)/5,mode='same'); r=-np.diff(sm)/np.diff(sss)*-1   # dA/ds increasing toward root
    r=np.diff(sm)/np.diff(sss); M['tail_taper_raw']=np.percentile(r[2:-2],99)*M['tail_len']/A_r
    Lt=s_free; M['tail_A50']=np.interp(0.5*Lt,sss,aa)/A_r; M['tail_A25']=np.interp(0.25*Lt,sss,aa)/A_r; M['tail_A75']=np.interp(0.75*Lt,sss,aa)/A_r
    tl=L.tail>0.9; M['tail_min_u']=u[tl].min()
    M['tail_reach_behind_heel']=np.percentile(f[u<1.5],1)-f[tl].min(); M['total_length']=f.max()-f.min()
    vol_b,com_b=mass_props(P,F); M['body_vol_L']=vol_b/1000; M['com_f']=com_b[1]; M['com_u']=com_b[2]
    ft=u<1.5; heel=np.percentile(f[ft],1); M['heel_f']=heel
    M['lean_req_deg']=np.degrees(np.arctan2((heel+8.4)-com_b[1], com_b[2]-9.0))   # lean to put COM 8.4 cm ahead of heel (ref-human-like, over the ankle+5)
    M['tail_mass_share']=M['tail_vol_L']/M['body_vol_L']
    if ref is not None:
        M['tail_RSI']=M['tail_RSI_raw']/ref['tail_RSI_raw']; M['tail_taper']=M['tail_taper_raw']/ref['tail_taper_raw']
        M['d_com_f']=M['com_f']-ref['com_f']*M['height']/ref['height']
    M['_A']=(sss,aa)
    return M
def vary_u(L): return L._u0
