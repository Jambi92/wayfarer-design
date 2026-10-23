# xsec.py IN.npz OUT.png axis value [xlim] [ylim] : planar cross-section of a quad mesh (cm)
import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
def sec(V,Q,ax,val):
    T=Q if Q.shape[1]==3 else np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]; s=V[:,ax]-val; segs=[]
    for t in T:
        d=s[t]; 
        if (d>0).all() or (d<0).all(): continue
        p=[]
        for i,j in ((0,1),(1,2),(2,0)):
            if (d[i]>0)!=(d[j]>0): u=d[i]/(d[i]-d[j]); p.append(V[t[i]]+u*(V[t[j]]-V[t[i]]))
        if len(p)==2: segs.append(p)
    oth=[i for i in range(3) if i!=ax]
    return np.array(segs)[:,:,oth] if segs else np.zeros((0,2,2))
if __name__=='__main__':
    a=sys.argv[1:]; ax={'x':0,'f':1,'u':2}[a[2]]; val=float(a[3])
    fig,axp=plt.subplots(figsize=(6,6))
    cols=['k','r','b','g']
    for k,f in enumerate(a[0].split(',')):
        z=np.load(f); S=sec(z['V'],z['Q'],ax,val); axp.add_collection(LineCollection(S,colors=cols[k],linewidths=0.8,label=f.split('/')[-1]))
    if len(a)>4: axp.set_xlim(*map(float,a[4].split(':')))
    if len(a)>5: axp.set_ylim(*map(float,a[5].split(':')))
    axp.set_aspect('equal'); axp.legend(fontsize=7); axp.set_title('%s = %s cm'%(a[2],a[3])); axp.grid(alpha=.3); fig.savefig(a[1],dpi=110)
