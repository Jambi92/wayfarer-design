# skel2.py PROD.npz OUT.json : diagnostic joint estimates per digit on the production mesh.
#  centerline = centroids of geodesic level-set rings from the claw apex (closed rings around the digit);
#  the digit root is where the ring spread jumps (merge into palm/web);
#  IP joints = the two largest centerline bends (fingers) / the largest bend (thumb IP) in the reference curl.
import sys,numpy as np,json; sys.path.insert(0,'/tmp/claude-0/hand/tools'); from hm import *
from scipy.ndimage import gaussian_filter1d
z=np.load(sys.argv[1]); V=z['V']*np.array([1,-1,1]); Q=z['Q']
E=edges_q(Q); G=graph(V,E); D=json.load(open('/tmp/claude-0/hand/digits.json'))
res={}
step=0.25
for k,d in D.items():
    apex=np.array(d['claw_tip']); s=int(np.argmin(np.linalg.norm(V-apex,axis=1))); g=geod(G,[s],limit=26.0)
    cs=[];sp_=[];ns=[];gs=[]
    for g0 in np.arange(0.5,25,step):
        m=(g>=g0)&(g<g0+step)
        if m.sum()<3: break
        P=V[m]; c=P.mean(0); cs.append(c); sp_.append(np.sqrt(((P-c)**2).sum(1).mean())); ns.append(int(m.sum())); gs.append(g0)
    cs=np.array(cs); sp_=np.array(sp_); gs=np.array(gs)
    # claw part: rings around the claw have small spread; finger starts where spread exceeds 60% of the finger median
    fmed=np.median(sp_[(gs>6)&(gs<12)]) if ((gs>6)&(gs<12)).any() else np.median(sp_)
    i0=int(np.argmax(sp_>0.6*fmed))
    # root: first ring beyond i0+8 whose spread exceeds 1.45 x running median of the finger rings
    root=None
    for i in range(i0+12,len(sp_)):
        if sp_[i]>1.45*np.median(sp_[i0+4:i]): root=i; break
    if root is None: root=len(sp_)-1
    C=gaussian_filter1d(cs[i0:root],2,axis=0); n=len(C)
    tng=np.gradient(C,axis=0); tng/=np.linalg.norm(tng,axis=1)[:,None]
    W=6; bend=np.zeros(n)
    for i in range(W,n-W): bend[i]=np.degrees(np.arccos(np.clip(tng[i-W]@tng[i+W],-1,1)))
    # peaks
    order=np.argsort(-bend); peaks=[]
    for i in order:
        if bend[i]<5: break
        if all(abs(i-j)>=int(1.6/step) for j in peaks): peaks.append(int(i))
        if len(peaks)==(1 if 'thumb' in k else 2): break
    peaks=sorted(peaks)
    res[k]=dict(centerline=C.tolist(),geod=gs[i0:root].tolist(),spread=sp_[i0:root].tolist(),bend=bend.tolist(),ip_idx=peaks,
                root_ring_geod=float(gs[root]),claw_end_geod=float(gs[i0]),root_point=cs[root].tolist())
    print(k,'claw->finger at %.2f cm, root at %.2f cm, finger rings %d, bend peaks'%(gs[i0],gs[root],n),[(round(float(gs[i0+p]),2),round(float(bend[p]),1)) for p in peaks])
json.dump(res,open(sys.argv[2],'w'))
