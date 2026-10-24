# sculpt_digits.py IN OUT PARAMS : v003 extremity anatomy -- finger/toe phalange rhythm, joints, creases, pads, nail beds,
#                                   MCP knuckle hierarchy, thenar mass, interdigital toe separation. Hands/feet only.
import sys, json, numpy as np, igl
from scipy.sparse.csgraph import dijkstra
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from digits import segment, frames, graph
from lowpass import lowpass
from cotfair import ss
d=np.load(sys.argv[1]); V=d['V'].astype(float); F=d['Q'].astype(np.int64); n=len(V); Q4=np.c_[F,F[:,0]]
p=json.load(open(sys.argv[3])); keep=np.load(p['keep']) if p.get('keep') else np.zeros(n)
G_=lambda x,s: np.exp(-0.5*(x/s)**2)
N=igl.per_vertex_normals(V,F)
D=np.zeros((n,3)); info={}
import scipy.sparse as sp_
_E=np.unique(np.sort(np.r_[F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]],1),axis=0)
_A=sp_.coo_matrix((np.ones(2*len(_E)),(np.r_[_E[:,0],_E[:,1]],np.r_[_E[:,1],_E[:,0]])),(n,n)).tocsr(); _deg=np.asarray(_A.sum(1)).ravel()
_S=V.copy()
for _ in range(p.get('normal_smooth_it',12)): _S=0.5*_S+0.5*(_A@_S)/_deg[:,None]
Nn=igl.per_vertex_normals(_S,F); N=Nn
cur_idx=[None]
def digit_disp(fr,dorsal,L,joints,kind,P):
    s=fr['s']; u=fr['u']; R=fr['R']; t=fr['t']
    dp=dorsal[None,:]-(t@dorsal)[:,None]*t; dp/=np.linalg.norm(dp,axis=1)[:,None]
    c=(u*dp).sum(1); dors=np.clip(c,0,1); palm=np.clip(-c,0,1); side=1-np.abs(c)
    sj=max(P['sig_joint'],P.get('sig_joint_cm',0)/L); sc=max(P['crease_cm']/L,0.012)
    dr=np.zeros(len(s)); shaftmask=np.ones(len(s))
    for xj in joints:
        g=G_(s-xj,sj); shaftmask=np.minimum(shaftmask,1-G_(s-xj,sj*1.7))
        dr+=P['a_swell']*g*(0.55+0.45*side)*(1-palm)
        dr+=P['a_knuckle']*G_(s-xj+0.012,sj*0.85)*dors**2
        dr-=P['a_crease']*G_(s-xj,sc)*palm**1.5
    xn0=P['nail_start']
    shaftmask*=1-ss((s-xn0+0.02)/0.04)
    dr-=P['a_flat']*shaftmask*dors**3
    dr-=P['a_side']*shaftmask*side**4
    segs=np.r_[0,joints,1.0]
    for a_,b_ in zip(segs[:-1],segs[1:]):
        dr+=P['a_pad']*palm*G_(s-(a_+b_)/2,(b_-a_)*0.28)
    dr+=P['a_tippad']*palm**1.2*G_(s-0.88,0.06)
    dr-=P['a_taper']*ss((s-0.80)/0.2)*(1-0.7*palm)
    # nail bed: flatten the dorsal dome, proximal fold + lateral grooves
    cn=np.cos(np.radians(P['nail_half_deg']))
    nw=ss((s-xn0)/0.03)*(1-ss((s-0.985)/0.02))
    dr-=P['a_nail_flat']*nw*np.clip((c-cn)/(1-cn),0,1)
    gf=max(P['nail_groove_cm']/L,0.01)
    dr-=P['a_nail_fold']*G_(s-xn0,gf)*ss((c-cn)/0.08)
    dr-=P['a_nail_side']*nw*G_(c-cn,0.07)
    dr*=ss(s/P['root_fade'])*R
    nrm=Nn[cur_idx[0]]
    return dr[:,None]*nrm
# ---------------- hands
hands=[]
for sg,seed in ((1,np.array(p['wrist_L'])),(-1,np.array(p['wrist_R']))):
    idx=np.nonzero((sg*V[:,0]>18)&(V[:,2]<108)&(V[:,2]>60))[0]
    Dg,_=segment(V,F,idx,seed,min_pers=1.0)
    assert len(Dg)==5, 'hand %d digits %d'%(sg,len(Dg))
    th=min(Dg,key=lambda g:g['root']); fing=[g for g in Dg if g is not th]
    G,loc=graph(V,F,idx); s0=np.argmin(np.linalg.norm(V[idx]-seed,axis=1)); dist=dijkstra(G,indices=s0)
    root=min(g['root'] for g in fing); thset=np.zeros(n,bool); thset[th['idx']]=True
    m=(dist>9)&(dist<root-0.8)&~thset[idx]; Pp=V[idx[m]]; pc=Pp.mean(0); _,_,Wt=np.linalg.svd(Pp-pc,full_matrices=False); dors=Wt[2]*np.sign(Wt[2][0]*sg)
    # order fingers index->pinky by forward position of the tips
    fing=sorted(fing,key=lambda g:-V[g['idx']][np.argmax(g['d'])][1])
    names=['index','middle','ring','pinky']
    for nm,g in zip(names,fing):
        fr=frames(V,g); cur_idx[0]=g['idx']; D[g['idx']]+=digit_disp(fr,dors,g['L'],p['finger_joints'],'finger',p['finger'])
        # MCP knuckle (metacarpal head) on the dorsal hand
        c0=fr['C'][0]; t0=fr['T'][0]; P0=c0-t0*p['mcp_back_cm']
        w=G_(np.linalg.norm(V-P0,axis=1),p['mcp_sigma'])*np.clip((N@dors-0.25)/0.5,0,1)*(sg*V[:,0]>18)
        D+=(p['mcp_amp'][nm]*w)[:,None]*N
        info['%s_%s'%('L' if sg>0 else 'R',nm)]=dict(L=float(g['L']),root=float(g['root']))
    frt=frames(V,th); tc=frt['C'][len(frt['C'])//2]; ro=tc-pc; tt=frt['T'][len(frt['T'])//2]; ro-=(ro@tt)*tt; ro/=np.linalg.norm(ro)
    dth=dors*p['thumb_dorsal_mix'][0]+ro*p['thumb_dorsal_mix'][1]; dth/=np.linalg.norm(dth)
    cur_idx[0]=th['idx']; D[th['idx']]+=digit_disp(frt,dth,th['L'],p['thumb_joints'],'thumb',p['thumb'])
    # thenar mass: between thumb root and the wrist, palm-facing
    P1=frt['C'][0]+(seed-frt['C'][0])*p['thenar_frac']
    w=G_(np.linalg.norm(V-P1,axis=1),p['thenar_sigma'])*np.clip((-(N@dors)+0.1)/0.5,0,1)*(sg*V[:,0]>18)*(1-thset)
    D+=(p['thenar_amp']*w)[:,None]*N
    info['%s_thumb'%('L' if sg>0 else 'R')]=dict(L=float(th['L']),root=float(th['root']))
    hands.append(dict(dorsal=dors.tolist(),palm_c=pc.tolist()))
# ---------------- toes
up=np.array([0,0,1.0])
for sg,peaks in ((1,p['toe_peaks_L']),(-1,p['toe_peaks_R'])):
    tips=[]
    for xp in peaks:
        q=np.nonzero((np.abs(V[:,0]-sg*xp)<0.7)&(V[:,2]<5))[0]; tips.append(V[q[np.argmax(V[q,1])]])
    tips=np.array(tips); conv=np.array([sg*p['toe_converge_x'],p['toe_converge_f'],0])
    axes=[]
    for k,tp in enumerate(tips):
        L=p['toe_len'][k]; dxy=tp-conv; dxy[2]=0; dxy/=np.linalg.norm(dxy)
        tip_c=tp-dxy*0.9; tip_c[2]=p['toe_tip_z'][k]
        mtp=tip_c-dxy*L; mtp[2]=p['toe_mtp_z'][k]
        axes.append((mtp,tip_c))
    cand=np.nonzero((sg*V[:,0]>3)&(V[:,2]<9)&(V[:,1]>min(a[0][1] for a in axes)-2.5))[0]
    P_=V[cand]; dist=[]; proj=[]
    for a,b in axes:
        ab=b-a; tpar=np.clip(((P_-a)@ab)/(ab@ab),-0.4,1.3); cp=a+tpar[:,None]*ab; dist.append(np.linalg.norm(P_-cp,axis=1)); proj.append(tpar)
    dist=np.array(dist); proj=np.array(proj); o=np.argsort(dist,0); k1=o[0]; k2=o[1]
    d1=dist[k1,np.arange(len(cand))]; d2=dist[k2,np.arange(len(cand))]
    # interdigital separation on the dorsum, between neighbouring toes, forward of the MTP line
    sp1=proj[k1,np.arange(len(cand))]
    cleft=G_(d2-d1,p['cleft_sigma'])*np.clip((N[cand,2]+0.2)/0.6,0,1)*ss((sp1+0.15)/0.25)*(np.abs(k1-k2)==1)*ss((p['cleft_maxd']-d1)/0.5)
    D[cand]-=(p['cleft_amp']*cleft)[:,None]*N[cand]
    names=['hallux','toe2','toe3','toe4','toe5']
    for k in range(len(axes)):
        sel=(k1==k)&(d1<p['toe_capsule'])&(sp1>-0.1)
        idxk=cand[sel]
        if len(idxk)<30: continue
        a,b=axes[k]; L=np.linalg.norm(b-a)
        g=dict(idx=idxk,d=np.clip(proj[k,sel],0,1)*L,root=0.0,L=L)
        fr=frames(V,g)
        jt=p['hallux_joints'] if k==0 else p['toe_joints']
        cur_idx[0]=idxk; D[idxk]+=digit_disp(fr,up,L,jt,'toe',p['toe'])
        info['%s_%s'%('L' if sg>0 else 'R',names[k])]=dict(L=float(L),n=int(len(idxk)),tip=tips[k].round(2).tolist())
# smooth the displacement field slightly (removes per-digit assignment seams), protect contacts, apply
D=lowpass(Q4,n,D,p.get('disp_smooth',0.6))
D*=(1-keep)[:,None]
# never push below the ground plane
Y=V+D; Y[:,2]=np.maximum(Y[:,2],np.minimum(V[:,2],0)+0.0)
mv=np.linalg.norm(Y-V,axis=1)*10
out={k:d[k] for k in d.files}; out['V']=Y; out['extremity_move_mm']=mv
np.savez(sys.argv[2],**out); json.dump(dict(info=info,hands=hands),open(sys.argv[2].replace('.npz','_info.json'),'w'),indent=1)
print('move mm max %.2f p95(moved) %.2f'%(mv.max(),np.percentile(mv[mv>0.01],95)))
