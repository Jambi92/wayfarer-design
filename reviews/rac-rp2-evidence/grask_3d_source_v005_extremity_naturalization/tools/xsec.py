# xsec.py OUT.png : cross-section outlines (v004 vs v005) through finger phalanges and toes -> shape-language proof
import sys, numpy as np, trimesh, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,'/tmp/claude-0/src3d/v5/tools')
from hand_model import DEF, scaled, finger_chain
from hand_frame import frame
import foot_model as fm
R='/tmp/claude-0/src3d/v5/'
meshes={k:trimesh.Trimesh(np.load(R+f)['V'],np.load(R+f)['Q'],process=False) for k,f in (('v004','v004.npz'),('v005','v005.npz'))}
p=scaled(DEF); W,M=frame('L')
cuts=[]
for nm in ('index','middle','ring'):
    f=p['fingers'][nm]; J,dirs,dors=finger_chain(f['mcp'],f['L'],f['splay'],f['flex'])
    for k,lab in ((0,'proximal phalanx mid'),(1,'PIP joint'),(1,'middle phalanx mid')):
        c=J[k]+dirs[k]*(0.5*f['L'][k]) if 'mid' in lab else J[k+0]
        if lab=='PIP joint': c=J[1]; dd=dirs[0]+dirs[1]; dr=dors[0]+dors[1]
        else: dd=dirs[k]; dr=dors[k]
        dd=dd/np.linalg.norm(dd); dr=dr-(dr@dd)*dd; dr/=np.linalg.norm(dr)
        cuts.append(('%s %s'%(nm,lab),W+M@c,M@dd,M@dr,2.2))
t=fm.DEF['toes'][1]; J,dirs,dors=fm.chain(t)
for k,lab in ((0,'toe2 proximal mid'),(1,'toe2 PIP joint')):
    c=J[k]+dirs[k]*(0.5*t['L'][k]) if 'mid' in lab else J[1]
    dd=dirs[k] if 'mid' in lab else (dirs[0]+dirs[1]); dd=dd/np.linalg.norm(dd); dr=dors[k]-(dors[k]@dd)*dd; dr/=np.linalg.norm(dr)
    cuts.append((lab,c,dd,dr,2.0))   # left foot frame == world for x>0
fig,axs=plt.subplots(2,(len(cuts)+1)//2,figsize=(4*((len(cuts)+1)//2),8.5))
for ax,(lab,o,n,up,hs) in zip(axs.ravel(),cuts):
    rt=np.cross(n,up)
    for k,col in (('v004','#999999'),('v005','#c0392b')):
        s=meshes[k].section(plane_origin=o,plane_normal=n)
        if s is None: continue
        for e in s.discrete:
            q=e-o; x=q@rt; y=q@up; keep=(np.abs(x)<hs*1.6)&(np.abs(y)<hs*1.6)
            if keep.sum()<5: continue
            ax.plot(x,y,color=col,lw=2 if k=='v005' else 1.5,label=k)
    ax.set_aspect('equal'); ax.set_xlim(-hs*1.5,hs*1.5); ax.set_ylim(-hs*1.5,hs*1.5); ax.set_title(lab,fontsize=10); ax.grid(alpha=.3)
    ax.text(0.02,0.95,'dorsal ↑',transform=ax.transAxes,fontsize=8,va='top')
h,l=axs.ravel()[0].get_legend_handles_labels(); d=dict(zip(l,h)); fig.legend(d.values(),d.keys(),loc='upper right')
for ax in axs.ravel()[len(cuts):]: ax.axis('off')
fig.suptitle('D. Cross-sections through digits (cm, local frame; dorsal up) - v004 grey vs v005 red',fontsize=13)
fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(sys.argv[1],dpi=110)
