# twsec.py OUT.png : transverse sections (u = const) through the thumb-index hollow, v005 (black) vs v002 (red, from the
# exported blend read back with the production translation undone), both hands
import numpy as np, sys, json, trimesh, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, igl
sys.path.insert(0,'/tmp/claude-0/rt'); from common import *
SV,SF=load_src(); z=np.load(sys.argv[2] if len(sys.argv)>2 else '/tmp/claude-0/rt/v002_rb.npz'); PV=z['V']; PQ=z['Q']
S=trimesh.Trimesh(SV,SF,process=False); P=trimesh.Trimesh(PV,np.r_[PQ[:,[0,1,2]],PQ[:,[0,2,3]]],process=False)
H={'R':np.array([-27.23,6.89,94.89]),'L':np.array([27.35,7.4,94.81])}
fig,axs=plt.subplots(2,3,figsize=(18,12)); out={}
for i,(s,h) in enumerate(H.items()):
    for j,dz in enumerate((-1.5,0,1.5)):
        ax=axs[i,j]; zz=h[2]+dz
        for M,col,lw,lab in ((S,'k',2.2,'v005 source'),(P,'r',1.0,(sys.argv[3] if len(sys.argv)>3 else 'v002')+' retopo')):
            sec=M.section(plane_origin=[0,0,zz],plane_normal=[0,0,1])
            for e in sec.discrete:
                m=np.linalg.norm(e[:,:2]-h[:2],axis=1)<5
                if m.any(): ax.plot(e[:,0],e[:,1],col,lw=lw,label=lab); lab=None
        ax.plot(h[0],h[1],'o',color='orange',ms=9) if dz==0 else None
        ax.set_xlim(h[0]-4.5,h[0]+4.5); ax.set_ylim(h[1]-4.5,h[1]+4.5); ax.set_aspect('equal'); ax.grid(alpha=.3)
        ax.set_title('%s hand  transverse section u = %.1f cm%s'%('RIGHT' if s=='R' else 'LEFT',zz,'  (through the hollow, orange)' if dz==0 else ''))
        ax.set_xlabel('x (cm, subject left +)'); ax.set_ylabel('f (cm, forward +)'); ax.legend(loc='lower left')
    d=np.sqrt(igl.point_mesh_squared_distance(SV[np.linalg.norm(SV-h,axis=1)<2.5],PV,np.r_[PQ[:,[0,1,2]],PQ[:,[0,2,3]]])[0])*10
    out[s]=dict(hollow_cm=h.tolist(),src_to_v002_within_2_5cm_mm=dict(median=float(np.median(d)),p95=float(np.percentile(d,95)),max=float(d.max())))
fig.suptitle('Thumb-index hollow: the indentation is in the frozen v005 surface (black); '+(sys.argv[3] if len(sys.argv)>3 else 'v002')+' (red) follows it',fontsize=16)
fig.tight_layout(); fig.savefig(sys.argv[1],dpi=80); json.dump(out,open(sys.argv[1].replace('.png','.json'),'w'),indent=1); print(json.dumps(out))
