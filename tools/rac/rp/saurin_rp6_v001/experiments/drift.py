import sys,json,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001')
import sa6_pose as SP,sa6_fit as FT,sa6_correctives as CC
c=sys.argv[1];R=SP.Rig(c,'/tmp/claude-0/rp6/W_%s.npz'%c);Cr=CC.Correctives.load(R,'/tmp/claude-0/rp6/CF_%s.json'%c);PS=FT.pose_set(R)
e=json.load(open('/tmp/claude-0/rp6/ev_%s.json'%c))['poses']
print('landmark rigid max over poses',max((r['landmarks']['max_rigid_cm'],pn) for pn,r in e.items() if pn not in FT.NONREAL and 'rp5lit' not in pn[:0]))
rv=R.W.max(1)>0.999;bd=R.W.argmax(1)
for pn in sys.argv[2].split(','):
    T=R.pose(PS[pn]);P=R.skin(T,R.V+Cr.delta(T));Rb=np.stack([T[b][0] for b in R.DB]);tb=np.stack([T[b][1] for b in R.DB])
    dr=np.linalg.norm(P-(np.einsum('vij,vj->vi',Rb[bd],R.V)+tb[bd]),axis=1);dr[~rv]=0
    piv=np.array([e_[1] for e_ in PS[pn]]);dj=np.linalg.norm(R.V[:,None]-piv[None],axis=2).min(1)
    m=dr>0.5;i=np.argmax(dr)
    vl=np.empty(R.nv,object)
    for l in np.unique(R.ql): vl[np.unique(R.Q[R.ql==l])]=l
    print('%-24s max %.2f at %s label %s bone %s dist-to-joint %.1f | n>0.5cm %d, their joint dist p50 %.1f max %.1f, labels %s'%(pn,dr[i],R.V[i].round(1),vl[i],R.DB[bd[i]],dj[i],m.sum(),np.median(dj[m]) if m.any() else 0,dj[m].max() if m.any() else 0,dict(zip(*np.unique(vl[m].astype(str),return_counts=True))) if m.any() else {}))
