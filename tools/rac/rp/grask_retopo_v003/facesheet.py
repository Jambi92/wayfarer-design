# facesheet.py OUT.png : the 8 audit-named v002 faces (zero-based polygon index of the submitted blend): local wire with the
# face filled red and its shortest edge in blue, v002 (left) vs v003 at the same place (right; worst edge ratio there marked)
import numpy as np, sys, json, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
sys.path.insert(0,'/tmp/claude-0/rt'); from common import PARTS
A=np.load('/tmp/claude-0/rt/v002_rb.npz'); B=np.load('/tmp/claude-0/rt/v003_rb.npz')
faces=[14853,19204,30301,30562,60332,110879,141725,153946]
def er(V,Q):
    el=np.stack([np.linalg.norm(V[Q[:,(i+1)%4]]-V[Q[:,i]],axis=1) for i in range(4)],1); return el.max(1)/el.min(1),el
rA,elA=er(A['V'],A['Q']); rB,elB=er(B['V'],B['Q'])
def draw(ax,M,r,el,f,c,n,title):
    V=M['V']; Q=M['Q']; u=np.cross(n,[0,0,1.0]); u=u/np.linalg.norm(u) if np.linalg.norm(u)>1e-3 else np.array([1.0,0,0]); w=np.cross(n,u)
    fc=V[Q].mean(1); m=np.nonzero(np.linalg.norm(fc-c,axis=1)<0.9)[0]; m=m[np.argsort(((V[Q[m]]-c)@n).mean(1))]
    P=np.stack([(V[Q[m]]-c)@u,(V[Q[m]]-c)@w],2); nr=np.cross(V[Q[m,2]]-V[Q[m,0]],V[Q[m,3]]-V[Q[m,1]]); front=(nr@n)>0
    col=[(1,.25,.25) if k==f else ((1,.8,.3) if r[k]>6 else ((.86,.86,.9) if fr else (.62,.62,.66))) for k,fr in zip(m,front)]
    ax.add_collection(PolyCollection(P,facecolors=col,edgecolors='k',linewidths=0.4))
    q=Q[f]; i=int(np.argmin(el[f])); a_,b_=V[q[i]],V[q[(i+1)%4]]; ax.plot([(a_-c)@u,(b_-c)@u],[(a_-c)@w,(b_-c)@w],color='blue',lw=3)
    ax.set_xlim(-0.9,0.9); ax.set_ylim(-0.9,0.9); ax.set_aspect('equal'); ax.set_title(title,fontsize=9); ax.set_xticks([]); ax.set_yticks([])
fig,axs=plt.subplots(4,4,figsize=(16,16.5)); rows=[]
for k,f in enumerate(faces):
    V=A['V']; Q=A['Q']; c=V[Q[f]].mean(0); n=np.cross(V[Q[f,2]]-V[Q[f,0]],V[Q[f,3]]-V[Q[f,1]]); n/=np.linalg.norm(n)
    part=PARTS[A['FP'][f]]
    fcB=B['V'][B['Q']].mean(1); near=np.nonzero(np.linalg.norm(fcB-c,axis=1)<0.6)[0]; g=near[np.argmax(rB[near])]
    ax=axs[k//2,(k%2)*2]; draw(ax,A,rA,elA,f,c,n,'v002 face %d (%s) at (%.1f, %.1f, %.1f) cm\nlongest/shortest edge %.2f, shortest %.2f mm'%(f,part,*c,rA[f],elA[f].min()*10))
    ax=axs[k//2,(k%2)*2+1]; draw(ax,B,rB,elB,g,c,n,'v003 same place: worst face %d ratio %.2f (shortest %.2f mm)'%(g,rB[g],elB[g].min()*10))
    rows.append(dict(v002_face=f,region_tag=part,centre_cm=np.round(c,2).tolist(),v002_edge_ratio=round(float(rA[f]),3),v002_shortest_mm=round(float(elA[f].min()*10),3),v003_worst_face_within_6mm=int(g),v003_edge_ratio=round(float(rB[g]),3)))
fig.suptitle('Audit-named v002 short-edge faces (red = the face, blue = its shortest edge, orange = other faces with edge ratio > 6) and the same place in v003',fontsize=13)
fig.tight_layout(); fig.savefig(sys.argv[1],dpi=75); json.dump(rows,open(sys.argv[1].replace('.png','.json'),'w'),indent=1)
for r in rows: print(r)
