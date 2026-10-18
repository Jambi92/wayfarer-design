# 05AW3 design fields on the AW2 topology (diagnostics/masks only)
import numpy as np, sys, json; sys.path.insert(0,'/home/claude/aw1'); sys.path.insert(0,'/home/claude/aw1/aw2')
import aw1lib as L
from scipy.sparse.csgraph import dijkstra
ss=L.ss; FF=json.load(open('/home/claude/aw1/footframes.json'))
CFG={"support":"support_S.npy","euclid":1,"round":1,"sidepow":2.2,"rootR":0.9,"height":0.0014,"len":0.019,"len_big":0.025,"hwf":0.40,"tipw":0.15,"tl":0.85,"edge":0.0008,"over":0.0018,"keel":0.3,"grow":0.35,"bigh":1.2,"diff":2}
def plate(X,n,c=CFG):
    fr=L.FR[n]; big=n[1]=='1'; g=lambda k,d: c.get(k+('_big' if big else ''),c.get(k,d))
    a=np.array(FF[n[0]]['a']); p=np.array(FF[n[0]]['p'])
    b=L.nearest(fr['Pd'],None); dg=L.geo(b,0.03); S=np.isfinite(dg)
    ta=X@a; it=np.flatnonzero(S)[np.argmax(ta[S])]; T=X[it]
    gu=L.geo(it,c.get('glim',0.045)); x=(X-T)@p; z=X[:,2]-T[2]
    near=np.isfinite(gu)&(gu<c.get('twin',0.02)); TW=np.percentile(x[near],95)-np.percentile(x[near],5)
    Ln=g('len',0.011); gu0=np.where(np.isfinite(gu),np.sqrt(z**2+((X-T)@a)**2),1.0)
    u=np.where(z>=0,gu0,-gu0); up_=np.clip(u,0,None)
    tt=np.clip(up_/(Ln*g('tl',0.7)),0,1); prof=1-(1-tt)**c.get('sidepow',2.2)
    hw=TW*g('hwf',0.36)*(g('tipw',0.45)+(1-g('tipw',0.45))*prof)
    u2=u+(x**2)/(2*c.get('rootR',1.0)*TW*g('hwf',0.36))
    ed=c.get('edge',0.0012)
    w=(1-ss((np.abs(x)-(hw-ed))/ed))*(1-ss((u2-(Ln-ed))/ed))*ss((u2+c.get('over',0.0015))/c.get('overramp',0.001))
    vn=L.vnormals(X); upn=vn@np.array([0,0,1.0])+0.8*(vn@a); w*=ss((upn-0.1)/0.3)
    w[~np.isfinite(gu)]=0
    return dict(w=w,u=u,up=up_,Ln=Ln,T=T,a=a,x=x,hw=hw,dom=np.isfinite(gu),it=it)
def multigeo(src,limit):
    return dijkstra(L.G,directed=False,indices=np.flatnonzero(src),limit=limit,min_only=True)
if __name__=='__main__':
    XA=np.load('/home/claude/aw1/aw2/real/GO-05AW2_A_VF.npz')['V']
    out={}
    for n in L.FR:
        P=plate(XA,n); out[n]=P
    np.save('plates.npy',out,allow_pickle=True); print({n:(round(out[n]['Ln']*1000,1),int((out[n]['w']>0.5).sum())) for n in out})
