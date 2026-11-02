import sys,json,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001')
import sa6_pose as SP,sa6_correctives as CC
for c in 'MF':
    R=SP.Rig(c,'/tmp/claude-0/rp6/W_%s.npz'%c);Cr=CC.Correctives.load(R,'/tmp/claude-0/rp6/CF_%s.json'%c);out=[]
    for key,f in Cr.F.items():
        piv=np.array(f['pivot'])
        for s,(i,d) in zip(f['samples'],f['D']):
            m=np.linalg.norm(d,axis=1);dist=np.linalg.norm(R.V[i]-piv,axis=1)
            for th in (0.1,0.5):
                k=m>th
                if k.any(): out.append((th,dist[k].max(),f['bone'],s,m.max()))
    for th in (0.1,0.5):
        o=sorted([x for x in out if x[0]==th],key=lambda x:-x[1])[:5];print(c,'>%.1f cm displacement: farthest from pivot'%th,[(b,round(s,1),round(dd,1),round(mx,2)) for _,dd,b,s,mx in o])
