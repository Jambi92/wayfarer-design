# planar cross-sections perpendicular to the anatomical axis (true section area), tail only
import numpy as np, sys
def sections(V,F,C,stations,rmax=22.0):
    E=np.unique(np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1),axis=0)
    out=[]
    for k in stations:
        k=int(k); k=min(max(k,1),len(C)-2); c=C[k]; t=C[k+1]-C[k-1]; t/=np.linalg.norm(t)
        d=(V-c)@t; a,b=E[:,0],E[:,1]; cr=(d[a]*d[b]<0)
        ea,eb=a[cr],b[cr]; w=d[ea]/(d[ea]-d[eb]); P=V[ea]+w[:,None]*(V[eb]-V[ea])
        r=P-c; ok=np.linalg.norm(r,axis=1)<rmax; P=P[ok]; r=r[ok]
        if len(P)<20: out.append((k*0.5,np.nan)); continue
        e1=np.cross(np.array([1.0,0,0]),t); e1/=np.linalg.norm(e1); e2=np.cross(t,e1)
        x=r@e2; y=r@e1; ang=np.arctan2(y,x); o=np.argsort(ang); x=x[o]; y=y[o]
        A=0.5*abs(np.sum(x*np.roll(y,-1)-np.roll(x,-1)*y)); out.append((k*0.5,A))
    return np.array(out)
if __name__=='__main__':
    C=np.load('/tmp/claude-0/rodin/g8/axis.npy'); st=np.arange(2,214)
    for fn,o in zip(sys.argv[1::2],sys.argv[2::2]):
        z=np.load(fn); V=z['V'].astype(float); F=z['F'].astype(np.int64); r=sections(V,F,C,st); np.save(o,r)
        print(fn, ' '.join('%.0f:%.0f'%(s,a) for s,a in r[::8]))
