import sys,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001')
import sa6_pose as SP,sa6_correctives as CC
R=SP.Rig('M','/tmp/claude-0/rp6/W_M.npz');Cr=CC.Correctives.load(R,'/tmp/claude-0/rp6/CF_M.json')
vl=np.empty(R.nv,object)
for l in np.unique(R.ql): vl[np.unique(R.Q[R.ql==l])]=l
for key,f in Cr.F.items():
    if f['bone'] not in ('forearm_r','thigh_l','spine_01'): continue
    piv=np.array(f['pivot'])
    for s,(i,d) in zip(f['samples'],f['D']):
        if abs(abs(s)-130)>1 and abs(s-70)>1 and abs(abs(s)-25)>1: continue
        m=np.linalg.norm(d,axis=1);dist=np.linalg.norm(R.V[i]-piv,axis=1);k=(m>0.3)&(dist>25)
        print(f['bone'],s,'pivot',piv.round(1),'n far>25cm & >3mm',k.sum(),'labels',dict(zip(*np.unique(vl[i[k]].astype(str),return_counts=True))) if k.any() else {},'centroid',R.V[i[k]].mean(0).round(1) if k.any() else '','max',m[k].max().round(2) if k.any() else '','dom bones',dict(zip(*np.unique(np.array(R.DB)[R.W[i[k]].argmax(1)],return_counts=True))) if k.any() else '')
