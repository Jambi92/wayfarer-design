# poleaudit.py PROD.npz LOOPAUDIT.json OUT.json OUTDIR TAG : pole inventory (valence, part, distance to the nearest audited joint
# plane in local loops) + labelled wire crops (v3 red, v5 blue, v6 black; label = pole id : valence)
import numpy as np, sys, json, collections, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
sys.path.insert(0,'/tmp/claude-0/rt'); from common import PARTS
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; FP=z['FP']; la=json.load(open(sys.argv[2]))['joints']; O=sys.argv[4]; T=sys.argv[5]
val=np.bincount(Q.ravel(),minlength=len(V)); E=np.unique(np.sort(np.concatenate([Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]),1),axis=0)
deg=np.bincount(E.ravel(),minlength=len(V)); P=np.nonzero(deg!=4)[0]
vp=np.zeros(len(V),int); vp[Q.ravel()]=np.repeat(FP,4); el=np.linalg.norm(V[E[:,0]]-V[E[:,1]],axis=1)
from scipy.spatial import cKDTree; kd=cKDTree(V)
rows=[]
for p in P:
    nb=kd.query_ball_point(V[p],1.0); h=np.median(el[np.isin(E[:,0],nb)]) if len(nb) else 0.3
    rows.append(dict(id=int(p),valence=int(deg[p]),part=PARTS[vp[p]],pos=np.round(V[p],2).tolist(),local_edge_mm=round(float(h*10),2)))
cnt=collections.Counter((r['valence'],r['part'].rsplit('_',1)[0] if r['part'].endswith(('_l','_r')) else r['part']) for r in rows)
onc=sum(v['poles_within_2_loops'] for v in la.values()); inb=sum(v['poles_in_band'] for v in la.values())
R=dict(poles=len(rows),valence_hist=dict(collections.Counter(int(deg[p]) for p in P)),by_valence_and_part={'v%d %s'%k:n for k,n in sorted(cnt.items())},
  poles_within_2_loops_of_audited_crease_planes=onc,poles_inside_joint_bands=inb,joints_audited=len(la),
  web_space_high_valence_clusters=int(sum(1 for r in rows if r['valence']>=6 and any(r['part'].startswith(t) for t in ('index','middle','ring','pinky','thumb','hallux','toe')) and sum(1 for s in rows if s['valence']>=5 and np.linalg.norm(np.array(s['pos'])-np.array(r['pos']))<0.6)>1)),
  note='pole set = authored-cage construction poles carried through subdivision unchanged (v001 166 -> v002 166); no density-transition poles exist because v002 is a uniform x2 subdivision of the cage',
  list=rows)
json.dump(R,open(sys.argv[3],'w'),indent=1); print('poles',len(rows),R['valence_hist'],'on-crease',onc,'in band',inb,'web clusters',R['web_space_high_valence_clusters'])
def crop(name,mask,az,elv):
    a=np.radians(az); e=np.radians(elv); cam=np.array([np.cos(e)*np.sin(a),np.cos(e)*np.cos(a),np.sin(e)]); r=np.cross([0,0,1.0],cam); r/=np.linalg.norm(r); u=np.cross(cam,r)
    x,f,zz=V.T; m=eval(mask); F=Q[m[Q].all(1)]; Tv=V[F]; N=np.cross(Tv[:,2]-Tv[:,0],Tv[:,3]-Tv[:,1]); N/=np.linalg.norm(N,axis=1)[:,None]+1e-12
    vis=N@cam>0; Tv=Tv[vis]; N=N[vis]; o=np.argsort(Tv.mean(1)@cam); Tv=Tv[o]; N=N[o]; sh=0.45+0.5*np.clip(N@cam,0,1)
    fig=plt.figure(figsize=(8,8),dpi=130); ax=fig.add_axes([0,0,1,1]); ax.set_aspect('equal'); ax.axis('off')
    ax.add_collection(PolyCollection(np.stack([Tv@r,Tv@u],-1),facecolors=np.stack([sh*.86,sh*.84,sh*.8],1),edgecolors=(0.1,0.1,0.15,0.5),linewidths=0.3)); ax.autoscale_view()
    VN=np.zeros_like(V); 
    for k in range(4): np.add.at(VN,Q[:,k],np.cross(V[Q[:,2]]-V[Q[:,0]],V[Q[:,3]]-V[Q[:,1]]))
    for p in P:
        if not m[p] or VN[p]@cam<=0: continue
        c={3:'red',5:'blue'}.get(int(deg[p]),'black'); X=V[p]@r; Y=V[p]@u
        ax.plot(X,Y,'o',color=c,ms=6); ax.text(X,Y,' %d:v%d'%(p,deg[p]),color=c,fontsize=7)
    fig.savefig('%s/pole_%s_%s.png'%(O,T,name)); plt.close(fig)
crop('head',"(zz>186)&(f>-2)",0,5); crop('shoulder_axilla',"(x>8)&(zz>140)&(zz<190)",40,-10)
crop('hand_dorsal',"(x>22)&(zz>75)&(zz<105)",90,0); crop('hand_palmar',"(x>22)&(zz>75)&(zz<105)",-90,0)
crop('pelvis_groin',"(zz>95)&(zz<130)",0,-10); crop('foot_top',"(x>6)&(zz<12)&(f>-12)",0,70); crop('foot_sole',"(x>6)&(zz<12)",0,-80)
