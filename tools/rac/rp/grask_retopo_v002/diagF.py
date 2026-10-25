# diagF.py PROD.npz LOOPS.json OUTPREFIX : topology diagnostics -- poles (valence 3 / 5 / other), tagged identity loops
# by family, joint transitions; whole body front + side, and hand / foot / head insets.
import numpy as np, sys, json, collections, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; loops=json.load(open(sys.argv[2])); O=sys.argv[3]
E=np.unique(np.sort(np.concatenate([Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]),1),axis=0)
val=np.bincount(E.ravel(),minlength=len(V))
fam=[('orbit','#d62728'),('mouth','#ff7f0e'),('neck','#8c564b'),('ear_root','#e377c2'),('shoulder','#1f77b4'),('elbow','#17becf'),('wrist','#2ca02c'),
     ('palm','#2ca02c'),('mcp_palm','#bcbd22'),('thumb','#9467bd'),('index','#9467bd'),('middle','#9467bd'),('ring','#9467bd'),('pinky','#9467bd'),
     ('groin','#1f77b4'),('hip_groin','#1f77b4'),('knee','#17becf'),('ankle','#2ca02c'),('forefoot','#bcbd22'),('hallux','#9467bd'),('toe','#9467bd'),('arm','#aaaaaa'),('leg','#aaaaaa')]
def color(k):
    for f,c in fam:
        if k.startswith(f): return c
    return '#555555'
def panel(ax,proj,crop,title,ms=6,lw=0.8):
    m=crop(V); sub=np.nonzero(m)[0]; s=sub[::max(1,len(sub)//60000)]
    p=proj(V[s]); ax.scatter(p[:,0],p[:,1],s=0.2,c='0.85',lw=0)
    for k,lp in loops.items():
        lp=np.array(lp+lp[:1]); 
        if not crop(V[lp]).any(): continue
        q=proj(V[lp]); ax.plot(q[:,0],q[:,1],color=color(k),lw=lw)
    for v,c,lab in ((3,'red','valence 3'),(5,'blue','valence 5'),(6,'black','valence 6+')):
        sel=np.nonzero(((val==v) if v<6 else (val>=6))&m)[0]
        if len(sel): q=proj(V[sel]); ax.scatter(q[:,0],q[:,1],s=ms,c=c,label='%s (%d)'%(lab,len(sel)),zorder=5)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title,fontsize=10); ax.legend(loc='lower right',fontsize=7,markerscale=1.5)
front=lambda P: P[:,[0,2]]*np.array([-1,1]); side=lambda P: P[:,[1,2]]; top=lambda P: P[:,[0,1]]*np.array([-1,1])
all_=lambda P: np.ones(len(P),bool)
fig,ax=plt.subplots(1,2,figsize=(16,14)); panel(ax[0],front,all_,'front: tagged identity loops (colour = family) + poles',4,0.6); panel(ax[1],side,all_,'side',4,0.6)
fig.savefig(O+'_body.png',dpi=90); plt.close(fig)
fig,ax=plt.subplots(2,3,figsize=(21,14))
panel(ax[0,0],front,lambda P:(P[:,2]>186),'head front'); panel(ax[0,1],side,lambda P:(P[:,2]>186)&(P[:,0]>-1),'head side')
panel(ax[0,2],front,lambda P:(P[:,0]>8)&(P[:,2]>140)&(P[:,2]<190),'shoulder / axilla front')
panel(ax[1,0],lambda P: P[:,[1,2]],lambda P:(P[:,0]>24)&(P[:,2]<110),'left hand (side)',8)
panel(ax[1,1],top,lambda P:(P[:,0]>6)&(P[:,2]<12),'left foot (top)',8)
panel(ax[1,2],front,lambda P:(P[:,2]>95)&(P[:,2]<130),'pelvis / groin front')
fig.savefig(O+'_zoom.png',dpi=80); plt.close(fig)
# pole inventory by part
sys.path.insert(0,'/tmp/claude-0/rt'); from common import PARTS
FP=z['FP']; vp=np.zeros(len(V),int); vp[Q.ravel()]=np.repeat(FP,4)
c=collections.Counter([(PARTS[vp[i]],int(val[i])) for i in np.nonzero(val!=4)[0]])
json.dump({'%s|v%d'%k:n for k,n in sorted(c.items())},open(O+'_poles.json','w'),indent=1)
print('poles',int((val!=4).sum()),dict(collections.Counter(val[val!=4].tolist())))
