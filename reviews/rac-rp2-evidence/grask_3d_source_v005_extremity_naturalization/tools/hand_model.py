# hand_model.py : articulated Grask hand as an SDF in the hand frame (u distal, v radial/thumb, w dorsal), cm
import numpy as np, json
from sdf import smin, smax, round_cone, ellipsoid, round_box, flat_cone, rot
E=np.eye(3); U,Vv,W=E
ABL=set()
DEF=dict(
 fingers=dict(
  index =dict(mcp=[13.8, 3.85, 0.05], L=[5.6,3.45,2.8], r=[1.29,1.17,1.07,0.97], splay=6,  flex=[18,26,14]),
  middle=dict(mcp=[14.25,1.28, 0.25], L=[6.05,3.9,3.0], r=[1.34,1.21,1.10,0.99], splay=1,  flex=[20,30,16]),
  ring  =dict(mcp=[13.75,-1.36,0.08], L=[5.8,3.7,2.9],  r=[1.27,1.14,1.05,0.95], splay=-4, flex=[24,34,18]),
  pinky =dict(mcp=[12.65,-3.9,-0.3],  L=[4.75,2.95,2.45],r=[1.1,1.0,0.92,0.83], splay=-10,flex=[28,38,20])),
 flat=0.86, mcp_amp={'index':0.95,'middle':1.0,'ring':0.88,'pinky':0.72},
 thumb=dict(cmc=[3.0,2.9,-1.2], dir=[0.86,0.27,-0.43], L=[6.2,4.5,3.6], r=[1.62,1.45,1.36,1.2,1.07,0.95], dors=[0.0,0.72,0.69], flex=[20,26]),
 palm=dict(c=[7.6,0,0.0], rad=[7.4,5.3,1.95]),
 wrist=dict(a=[-7.0,0,0.1], b=[2.2,0,0.1], r1=4.0, r2=4.4, flat=0.68),
 thenar=dict(c=[5.8,3.0,-1.55], rad=[3.8,2.3,1.75]), hypo=dict(c=[8.0,-4.0,-1.15], rad=[4.8,1.6,1.35]),
 nat=dict(rmul=[1.13,1.10,1.06,1.04], seg_k=0.1, ja=1.2, jw=0.97, jwd=0.93, fs=0.05, fz=0.7, jk=0.15, kn=[1.0,0.65,0.3], knk=0.2, kno=0.40, pad=[0.40,0.80,0.52], padk=0.3, padoff=0.36,
          cr_r=0.28, cr_off=0.20, cr_k=0.16, web={'index':1.15,'middle':1.3,'ring':1.25,'pinky':1.05}, th_r=1.10, th_base_k=1.5, th_k=0.65, thenar_mul=1.15, thenar_k=1.3),
 nail=dict(start=0.40, half_lat=0.66, thick=0.05, groove=0.13, raise_=0.03, curv=0.5, tube=0.1, gk=0.15, pk=0.06, tube2=0.2, lift=0.11, proud=0.03, lend=0.85, lexit=0.2),
)
def finger_chain(mcp,L,splay,flex):
    J=[np.array(mcp,float)]; d=rot(W,np.radians(splay))@U; dor=W.copy(); dirs=[]; dors=[]
    for k in range(3):
        lat=np.cross(d,dor); lat/=np.linalg.norm(lat)
        R=rot(lat,np.radians(flex[k]))      # positive -> toward palm (-w)?  verified below
        if (R@d)@dor>d@dor: R=rot(lat,-np.radians(flex[k]))
        d=R@d; dor=R@dor; dirs.append(d.copy()); dors.append(dor.copy()); J.append(J[-1]+L[k]*d)
    return J,dirs,dors
def nail_sdf(P,J,d,dor,L3,rt,flat,N):
    lat=np.cross(d,dor); q=P-J; a=q@d; l=q@lat; h=q@dor
    top=rt*flat*0.98+N['raise_']
    h2=h+N['curv']*l*l/rt
    s0=N['start']*L3; s1=L3+0.02*rt
    c_a=(s0+s1)/2; ha=(s1-s0)/2; hl=N['half_lat']*rt
    qa=np.abs(a-c_a)-ha; ql=np.abs(l)-hl; qh=np.abs(h2-(top-0.2))-0.2
    plate=np.linalg.norm(np.maximum(np.stack([qa,ql,qh],1),0),axis=1)+np.minimum(np.maximum(np.maximum(qa,ql),qh),0)
    # groove ring (proximal + lateral only)
    g=N['groove']; qa2=np.abs(a-(c_a+0.15))-(ha+0.15+g*0.0); qa2b=np.abs(a-(c_a+0.15))-(ha+0.15+g)
    inner=np.maximum(np.maximum(np.abs(a-(c_a+0.3))-(ha+0.3),ql),np.abs(h2-top)-0.35)
    outer=np.maximum(np.maximum(np.abs(a-(c_a+0.3))-(ha+0.3+g),np.abs(l)-(hl+g)),np.abs(h2-top)-0.30)
    ring=np.maximum(outer,-inner)
    return plate,ring
def scaled(p,su=1.1,sv=1.22,sr=1.06,sw=1.2):
    import copy; q=copy.deepcopy(p)
    for f in q['fingers'].values():
        f['mcp']=[f['mcp'][0]*su,f['mcp'][1]*sv,f['mcp'][2]]; f['L']=[x*su for x in f['L']]; f['r']=[x*sr for x in f['r']]
    T=q['thumb']; T['cmc']=[T['cmc'][0]*su,T['cmc'][1]*sv,T['cmc'][2]*sw]; T['L']=[x*su for x in T['L']]; T['r']=[x*sr*1.04 for x in T['r']]
    q['palm']['c'][0]*=su; q['palm']['rad']=[q['palm']['rad'][0]*su,q['palm']['rad'][1]*sv,q['palm']['rad'][2]*sw]
    for k in ('thenar','hypo'):
        q[k]['c']=[q[k]['c'][0]*su,q[k]['c'][1]*sv,q[k]['c'][2]*sw]; q[k]['rad']=[q[k]['rad'][0]*su,q[k]['rad'][1]*sv,q[k]['rad'][2]*sw]
    q['wrist']['b'][0]*=su
    return q
def nail_groove(P,J,d,dor,L3,rt,flat,N):
    # v2: wide shallow perimeter trough (tube centre lifted above skin) + proud curved plate + proximal fold
    lat=np.cross(d,dor); hl=N['half_lat']*rt; s0=N['start']*L3
    lift=N.get('lift',0.06); tb=N.get('tube2',0.16)
    htop=rt*flat*0.98+lift; hlat=0.62*rt+lift; hmid=0.5*(htop+hlat)
    Ra=N.get('arc',0.20)*L3; th=np.linspace(-np.pi/2,np.pi/2,13)
    arc=[(s0+Ra*(1-np.cos(t)),hl*np.sin(t),htop+(hlat-htop)*abs(np.sin(t))**1.5) for t in th]
    le=N.get('lend',0.97); lx=N.get('lexit',0.0); lm=N.get('lmid',0.62)
    pts=[(le*L3,-hl,hlat+lx),(lm*L3,-hl,hlat)]+arc+[(lm*L3,hl,hlat),(le*L3,hl,hlat+lx)]
    W_=[J+a*d+l*lat+h*dor for a,l,h in pts]
    g=None
    for A,B in zip(W_[:-1],W_[1:]):
        q=round_cone(P,A,B,tb,tb); g=q if g is None else np.minimum(g,q)
    plate=ellipsoid(P,J+d*(0.68*L3)+dor*(rt*flat*0.98-0.30+N.get('proud',0.045)),np.stack([d,lat,dor],1),[0.31*L3,0.90*hl,0.30])
    return g,plate
def hand_sdf(Pl,p=None):
    if p is None: p=scaled(DEF)
    """Pl: points in hand frame (n,3)"""
    Q=Pl.copy(); Q[:,2]=Q[:,2]+0.03*Q[:,1]**2
    d=ellipsoid(Q,np.array(p['palm']['c']),np.eye(3),p['palm']['rad'])
    Wd=p['wrist']; d=smin(d,flat_cone(Pl,np.array(Wd['a']),np.array(Wd['b']),Wd['r1'],Wd['r2'],W,Wd['flat']),1.6)
    N_=p['nat']; d=smin(d,ellipsoid(Pl,np.array(p['thenar']['c']),rot(W,np.radians(40)),np.array(p['thenar']['rad'])*N_['thenar_mul']),N_['thenar_k'])
    d=smin(d,ellipsoid(Pl,np.array(p['hypo']['c']),np.eye(3),p['hypo']['rad']),1.0)
    creases=[]; nails=[]; rings=[]; fings=[]
    for nm,f in p['fingers'].items():
        J,dirs,dors=finger_chain(f['mcp'],f['L'],f['splay'],f['flex']); r=f['r']
        # metacarpal ridge
        base=np.array([1.8,f['mcp'][1]*0.42,0.45])
        d=smin(d,flat_cone(Pl,base,J[0]+W*0.1,1.2,r[0]*1.08,W,0.72),1.0)
        # MCP head (dorsal knuckle)
        d=smin(d,ellipsoid(Pl,J[0]+W*(0.62*r[0]),np.eye(3),np.array([0.95,0.85,0.55])*r[0]*p['mcp_amp'][nm]),0.45)
        rr=[r[i]*N_['rmul'][i] for i in range(4)]
        df=flat_cone(Pl,J[0],J[1],rr[0],rr[1],dors[0],p['flat'])
        for k in (1,2):
            seg=flat_cone(Pl,J[k],J[k+1]-dirs[k]*(0.0 if k<2 else rr[3]*0.55),rr[k],rr[k+1],dors[k],p['flat'])
            df=smin(df,seg,N_['seg_k'])
        for k in (1,2):   # PIP, DIP: joint widening + dorsal knuckle + palmar crease
            rj=rr[k]*(N_['jw'] if k==1 else N_.get('jwd',N_['jw'])); bj=(dirs[k-1]+dirs[k]); bj/=np.linalg.norm(bj); oj=(dors[k-1]+dors[k]); oj/=np.linalg.norm(oj); FR=np.stack([bj,np.cross(bj,oj),oj],1)
            df=smin(df,ellipsoid(Pl,J[k],FR,[N_['ja']*rr[k],rj,rj*p['flat']*0.95]),N_['jk'])
            kn=N_['kn']; df=smin(df,ellipsoid(Pl,J[k]+oj*(N_.get('kno',0.40)*rr[k])-bj*0.12+np.cross(bj,oj)*0.06*rr[k],FR,[kn[0]*rr[k],kn[1]*rr[k],kn[2]*rr[k]]),N_['knk'])
            lat=np.cross(dirs[k],dors[k]); c=J[k]-((dors[k-1]+dors[k])/2)*(rr[k]*p['flat']*1.02+0.13)
            c=c-((dors[k-1]+dors[k])/2)*(N_['cr_off']-0.13); creases.append(round_cone(Pl,c-lat*0.75*rr[k],c+lat*0.75*rr[k],N_['cr_r'],N_['cr_r']))
        for k in (0,1):
            Lk=f['L'][k]; ck=J[k]+dirs[k]*(0.5*Lk)-dors[k]*(N_['padoff']*rr[k])
            df=smin(df,ellipsoid(Pl,ck,np.stack([dirs[k],np.cross(dirs[k],dors[k]),dors[k]],1),[N_['pad'][0]*Lk,N_['pad'][1]*rr[k],N_['pad'][2]*rr[k]]),N_['padk'])
        # distal pad + dorsal flattening for the nail bed
        L3=f['L'][2]; Jd=J[2]; dd=dirs[2]; do=dors[2]
        df=smin(df,ellipsoid(Pl,Jd+dd*(0.62*L3)-do*(0.3*rr[3]),np.stack([dd,np.cross(dd,do),do],1),[0.5*L3,0.9*rr[3],0.62*rr[3]]),0.25)
        flatcut=(Pl-Jd)@do-rr[3]*p['flat']*0.98
        zone=np.clip(((Pl-Jd)@dd-N_.get('fs',0.25)*L3)/(N_.get('fz',0.15)*L3),0,1)
        df=smax(df,flatcut-(1-zone)*5,0.18)
        fings.append(df)
        g_,pl_=nail_groove(Pl,Jd,dd,do,L3,rr[3],p['flat'],p['nail']); rings.append(g_); nails.append(pl_)
    # thumb
    T=p['thumb']; dth=np.array(T['dir']); dth/=np.linalg.norm(dth); dor=np.array(T['dors']); dor-=(dor@dth)*dth; dor/=np.linalg.norm(dor)
    J=[np.array(T['cmc'],float)]; dirs=[dth]; dors=[dor]; J.append(J[0]+T['L'][0]*dth)
    for k in range(2):
        lat=np.cross(dirs[-1],dors[-1]); R=rot(lat,np.radians(T['flex'][k]))
        if ((R@dirs[-1])@dors[-1]>0)==(T.get('flexsign',1)>0): R=rot(lat,-np.radians(T['flex'][k]))
        dirs.append(R@dirs[-1]); dors.append(R@dors[-1]); J.append(J[-1]+T['L'][k+1]*dirs[-1])
    r=[x*(N_['th_r'] if i<4 else 1.05) for i,x in enumerate(T['r'])]
    d=smin(d,flat_cone(Pl,J[0],J[1],r[0],r[1],dors[0],0.85),N_['th_base_k'])
    dp=d
    d=dp.copy()
    for nm_,df in zip(p['fingers'].keys(),fings): d=np.minimum(d,smin(dp,df,N_['web'][nm_]))
    dt=flat_cone(Pl,J[1],J[2],r[2],r[3],dors[1],p['flat'])
    dt=smin(dt,flat_cone(Pl,J[2],J[3]-dirs[2]*r[5]*0.55,r[4],r[5],dors[2],p['flat']),N_['seg_k'])
    d=smin(d,ellipsoid(Pl,J[1]+dors[0]*0.55*r[1],np.stack([dirs[0],np.cross(dirs[0],dors[0]),dors[0]],1),[0.8*r[1],0.85*r[1],0.5*r[1]]),0.35)
    for k in (2,):
        rj=r[3]*N_['jw']
        dt=smin(dt,ellipsoid(Pl,J[k],np.stack([dirs[k-1],np.cross(dirs[k-1],dors[k-1]),dors[k-1]],1),[N_['ja']*r[3],rj,rj*p['flat']]),N_['jk'])
        lat=np.cross(dirs[k],dors[k]); c=J[k]-((dors[k-1]+dors[k])/2)*(r[3]*p['flat']*1.02+0.13)
        creases.append(round_cone(Pl,c-lat*0.75*r[3],c+lat*0.75*r[3],0.26,0.26))
    L3=T['L'][2]; Jd=J[2]; dd=dirs[2]; do=dors[2]
    dt=smin(dt,ellipsoid(Pl,Jd+dd*(0.6*L3)-do*(0.3*r[5]),np.stack([dd,np.cross(dd,do),do],1),[0.5*L3,0.92*r[5],0.62*r[5]]),0.25)
    flatcut=(Pl-Jd)@do-r[5]*p['flat']*0.98; zone=np.clip(((Pl-Jd)@dd-0.25*L3)/(0.15*L3),0,1)
    dt=smax(dt,flatcut-(1-zone)*5,0.18)
    d=smin(d,dt,N_['th_k'])
    g_,pl_=nail_groove(Pl,Jd,dd,do,L3,r[5],p['flat'],p['nail']); rings.append(g_); nails.append(pl_)
    if 'crease' not in ABL:
        for c in creases: d=smax(d,-c,N_['cr_k'])
    if 'ring' not in ABL:
        for rg in rings: d=smax(d,-rg,p['nail'].get('gk',0.07))
    if 'nail' not in ABL:
        for pl in nails: d=smin(d,pl,p['nail'].get('pk',0.015))
    return d
def joints(p=DEF):
    out={}
    for nm,f in p['fingers'].items():
        J,_,_=finger_chain(f['mcp'],f['L'],f['splay'],f['flex']); out[nm]=[j.tolist() for j in J]
    return out
